import logging
import uuid
from datetime import UTC, datetime
from io import BytesIO

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.object_storage import delete_object, presigned_get_url, put_bytes
from app.models import (
    Dish,
    DishStatus,
    ImageAccessPublic,
    ImageAsset,
    ImageJobStatus,
    ImageProcessingJob,
    ImageStatus,
    Review,
    User,
    UserRole,
)

ALLOWED_FORMATS = {
    "JPEG": ("jpg", "image/jpeg"),
    "PNG": ("png", "image/png"),
    "WEBP": ("webp", "image/webp"),
}
logger = logging.getLogger(__name__)


def _is_reviewer(user: User) -> bool:
    return user.is_superuser or user.role in {UserRole.REVIEWER, UserRole.ADMIN}


def validate_image(file: UploadFile) -> tuple[bytes, str, str, int, int]:
    data = file.file.read(settings.IMAGE_MAX_BYTES + 1)
    if not data:
        raise HTTPException(status_code=422, detail="Image file is empty")
    if len(data) > settings.IMAGE_MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image file is too large")
    try:
        with Image.open(BytesIO(data)) as image:
            width, height = image.size
            if width * height > settings.IMAGE_MAX_PIXELS:
                raise HTTPException(
                    status_code=422, detail="Image dimensions are too large"
                )
            if getattr(image, "n_frames", 1) != 1:
                raise HTTPException(
                    status_code=422, detail="Animated images are not supported"
                )
            image_format = image.format
            image.verify()
        with Image.open(BytesIO(data)) as image:
            image.load()
    except UnidentifiedImageError, OSError, Image.DecompressionBombError:
        raise HTTPException(status_code=422, detail="Invalid or undecodable image")
    if image_format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=422, detail="Unsupported image format")
    extension, content_type = ALLOWED_FORMATS[image_format]
    return data, extension, content_type, width, height


def _create_asset(
    *,
    session: Session,
    user: User,
    data: bytes,
    extension: str,
    content_type: str,
    width: int,
    height: int,
    dish_id: uuid.UUID | None = None,
    review_id: uuid.UUID | None = None,
) -> ImageAsset:
    image_id = uuid.uuid4()
    object_key = f"originals/{image_id}.{extension}"
    try:
        put_bytes(object_key=object_key, data=data, content_type=content_type)
    except Exception:
        logger.exception("Image original upload failed")
        raise HTTPException(status_code=503, detail="Object storage is unavailable")
    image = ImageAsset(
        id=image_id,
        owner_id=user.id,
        dish_id=dish_id,
        review_id=review_id,
        original_object_key=object_key,
        content_type=content_type,
        byte_size=len(data),
        width=width,
        height=height,
    )
    job = ImageProcessingJob(image_id=image.id)
    session.add(image)
    session.add(job)
    try:
        session.commit()
    except Exception:
        session.rollback()
        try:
            delete_object(object_key)
        except Exception:
            logger.exception("Failed to remove orphaned image object")
        raise
    session.refresh(image)
    if dispatch_image_job(job.id):
        job.dispatched_at = datetime.now(UTC)
        job.updated_at = job.dispatched_at
        session.add(job)
        session.commit()
    return image


def create_dish_image(
    *, session: Session, dish_id: uuid.UUID, file: UploadFile, user: User
) -> ImageAsset:
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    if (
        dish.status != DishStatus.PUBLISHED
        and dish.submitted_by_id != user.id
        and not _is_reviewer(user)
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    data, extension, content_type, width, height = validate_image(file)
    return _create_asset(
        session=session,
        user=user,
        data=data,
        extension=extension,
        content_type=content_type,
        width=width,
        height=height,
        dish_id=dish.id,
    )


def create_review_image(
    *, session: Session, review_id: uuid.UUID, file: UploadFile, user: User
) -> ImageAsset:
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if review.is_deleted:
        raise HTTPException(
            status_code=409, detail="Deleted review cannot receive images"
        )
    data, extension, content_type, width, height = validate_image(file)
    return _create_asset(
        session=session,
        user=user,
        data=data,
        extension=extension,
        content_type=content_type,
        width=width,
        height=height,
        review_id=review.id,
    )


def dispatch_image_job(job_id: uuid.UUID) -> bool:
    try:
        from app.worker import celery_app

        celery_app.send_task("app.process_image", args=[str(job_id)], retry=False)
        return True
    except Exception:
        logger.warning("Image task dispatch failed; compensation will retry")
        return False


def can_access_image(session: Session, image: ImageAsset, user: User) -> bool:
    if image.owner_id == user.id or _is_reviewer(user):
        return True
    if image.dish_id:
        dish = session.get(Dish, image.dish_id)
        return bool(dish and dish.status == DishStatus.PUBLISHED)
    if image.review_id:
        review = session.get(Review, image.review_id)
        if not review or review.is_deleted or review.is_hidden:
            return False
        dish = session.get(Dish, review.dish_id)
        return bool(dish and dish.status == DishStatus.PUBLISHED)
    return False


def get_image_url(
    *, session: Session, image: ImageAsset, user: User, thumbnail: bool
) -> ImageAccessPublic:
    if not can_access_image(session, image, user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    object_key = image.thumbnail_object_key if thumbnail else image.original_object_key
    if thumbnail and (image.status != ImageStatus.READY or not object_key):
        raise HTTPException(status_code=409, detail="Thumbnail is not ready")
    assert object_key
    try:
        url = presigned_get_url(object_key)
    except Exception:
        logger.exception("Image URL signing failed")
        raise HTTPException(status_code=503, detail="Object storage is unavailable")
    return ImageAccessPublic(url=url, expires_in=settings.IMAGE_URL_EXPIRE_SECONDS)


def retry_image(*, session: Session, image: ImageAsset, user: User) -> ImageAsset:
    if image.owner_id != user.id and not _is_reviewer(user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if image.status != ImageStatus.FAILED:
        raise HTTPException(status_code=409, detail="Only failed images can be retried")
    job = session.exec(
        select(ImageProcessingJob)
        .where(ImageProcessingJob.image_id == image.id)
        .with_for_update()
    ).one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Image processing job not found")
    session.refresh(image)
    if job.status != ImageJobStatus.FAILED:
        raise HTTPException(status_code=409, detail="Only failed images can be retried")
    now = datetime.now(UTC)
    image.status = ImageStatus.PENDING
    image.error_message = None
    image.updated_at = now
    job.status = ImageJobStatus.PENDING
    job.attempts = 0
    job.next_attempt_at = now
    job.finished_at = None
    job.last_error = None
    job.dispatched_at = None
    job.updated_at = now
    session.add(image)
    session.add(job)
    session.commit()
    session.refresh(image)
    dispatch_image_job(job.id)
    return image
