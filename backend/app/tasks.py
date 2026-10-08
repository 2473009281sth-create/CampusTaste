import uuid
from datetime import UTC, datetime, timedelta
from io import BytesIO
from typing import Any

from celery import shared_task  # type: ignore[import-untyped]
from minio.error import S3Error
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy import and_, or_
from sqlmodel import Session, col, select

from app.core.config import settings
from app.core.db import engine
from app.core.object_storage import get_bytes, put_bytes
from app.models import ImageAsset, ImageJobStatus, ImageProcessingJob, ImageStatus
from app.services.images import dispatch_image_job


class PermanentImageError(Exception):
    pass


def _thumbnail(data: bytes) -> bytes:
    try:
        with Image.open(BytesIO(data)) as source:
            if source.width * source.height > settings.IMAGE_MAX_PIXELS:
                raise PermanentImageError("Image dimensions exceed the limit")
            source.load()
            image = ImageOps.exif_transpose(source)
            image.thumbnail(
                (settings.IMAGE_THUMBNAIL_SIZE, settings.IMAGE_THUMBNAIL_SIZE)
            )
            converted = (
                image if image.mode in {"RGB", "RGBA", "L"} else image.convert("RGB")
            )
            output = BytesIO()
            converted.save(output, format="WEBP", quality=85, method=6)
            return output.getvalue()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise PermanentImageError("Stored original is not a valid image") from exc


def _fail_job(job: ImageProcessingJob, image: ImageAsset, message: str) -> None:
    now = datetime.now(UTC)
    job.status = ImageJobStatus.FAILED
    job.last_error = message
    job.finished_at = now
    job.updated_at = now
    image.status = ImageStatus.FAILED
    image.error_message = message
    image.updated_at = now


@shared_task(
    bind=True,
    name="app.process_image",
    acks_late=True,
    reject_on_worker_lost=True,
    max_retries=5,
)  # type: ignore[untyped-decorator]
def process_image(self: Any, job_id: str) -> None:
    parsed_job_id = uuid.UUID(job_id)
    with Session(engine) as session:
        job = session.exec(
            select(ImageProcessingJob)
            .where(ImageProcessingJob.id == parsed_job_id)
            .with_for_update()
        ).one_or_none()
        if (
            not job
            or job.status != ImageJobStatus.PENDING
            or job.next_attempt_at > datetime.now(UTC)
        ):
            return
        image = session.get(ImageAsset, job.image_id)
        if not image:
            return
        if job.attempts >= settings.IMAGE_TASK_MAX_ATTEMPTS:
            _fail_job(job, image, "Processing attempt limit reached")
            session.commit()
            return
        job.status = ImageJobStatus.PROCESSING
        job.attempts += 1
        attempt = job.attempts
        job.updated_at = datetime.now(UTC)
        image.status = ImageStatus.PROCESSING
        image.updated_at = job.updated_at
        session.commit()

    countdown: int | None = None
    # Hold the job lock during I/O. Compensation skips active locked jobs;
    # process death releases the lock, but leaves the durable attempt recorded.
    with Session(engine) as session:
        job = session.exec(
            select(ImageProcessingJob)
            .where(ImageProcessingJob.id == parsed_job_id)
            .with_for_update()
        ).one()
        if job.status != ImageJobStatus.PROCESSING or job.attempts != attempt:
            return
        image = session.get(ImageAsset, job.image_id)
        if not image:
            return
        try:
            thumbnail = _thumbnail(get_bytes(image.original_object_key))
            thumbnail_key = f"thumbnails/{image.id}.webp"
            put_bytes(
                object_key=thumbnail_key, data=thumbnail, content_type="image/webp"
            )
        except Exception as exc:
            permanent = isinstance(exc, PermanentImageError) or (
                isinstance(exc, S3Error)
                and exc.code
                in {
                    "NoSuchKey",
                    "AccessDenied",
                    "InvalidAccessKeyId",
                    "SignatureDoesNotMatch",
                }
            )
            message = (
                str(exc) if isinstance(exc, PermanentImageError) else type(exc).__name__
            )
            if permanent or attempt >= settings.IMAGE_TASK_MAX_ATTEMPTS:
                _fail_job(job, image, message)
            else:
                now = datetime.now(UTC)
                countdown = min(2**attempt, 60)
                job.status = ImageJobStatus.PENDING
                job.next_attempt_at = now + timedelta(seconds=countdown)
                job.last_error = message
                job.updated_at = now
                job.dispatched_at = None
                image.status = ImageStatus.PENDING
                image.error_message = message
                image.updated_at = now
        else:
            now = datetime.now(UTC)
            image.thumbnail_object_key = thumbnail_key
            image.status = ImageStatus.READY
            image.error_message = None
            image.updated_at = now
            job.status = ImageJobStatus.SUCCEEDED
            job.finished_at = now
            job.last_error = None
            job.updated_at = now
        session.commit()
    if countdown is not None:
        raise self.retry(countdown=countdown)


@shared_task(name="app.dispatch_pending_image_jobs")  # type: ignore[untyped-decorator]
def dispatch_pending_image_jobs() -> int:
    now = datetime.now(UTC)
    stale = now - timedelta(minutes=5)
    with Session(engine) as session:
        jobs = session.exec(
            select(ImageProcessingJob)
            .where(
                or_(
                    and_(
                        col(ImageProcessingJob.status) == ImageJobStatus.PENDING,
                        col(ImageProcessingJob.next_attempt_at) <= now,
                        or_(
                            col(ImageProcessingJob.dispatched_at).is_(None),
                            col(ImageProcessingJob.dispatched_at) <= stale,
                        ),
                    ),
                    and_(
                        col(ImageProcessingJob.status) == ImageJobStatus.PROCESSING,
                        col(ImageProcessingJob.updated_at) <= stale,
                    ),
                )
            )
            .order_by(col(ImageProcessingJob.created_at))
            .limit(100)
            .with_for_update(skip_locked=True)
        ).all()
        ids: list[uuid.UUID] = []
        for job in jobs:
            image = session.get(ImageAsset, job.image_id)
            if not image:
                continue
            if job.attempts >= settings.IMAGE_TASK_MAX_ATTEMPTS:
                _fail_job(job, image, "Processing attempt limit reached")
                continue
            job.status = ImageJobStatus.PENDING
            image.status = ImageStatus.PENDING
            job.dispatched_at = now
            job.updated_at = now
            ids.append(job.id)
        session.commit()
    dispatched = 0
    for job_id in ids:
        if dispatch_image_job(job_id):
            dispatched += 1
        else:
            with Session(engine) as session:
                job = session.exec(
                    select(ImageProcessingJob)
                    .where(ImageProcessingJob.id == job_id)
                    .with_for_update()
                ).one()
                if job.status == ImageJobStatus.PENDING and job.dispatched_at == now:
                    job.dispatched_at = None
                    session.commit()
    return dispatched
