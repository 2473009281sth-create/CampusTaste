import os
import subprocess
import sys
import time
import uuid
from datetime import UTC, datetime, timedelta
from io import BytesIO

import httpx
from fastapi.testclient import TestClient
from PIL import Image
from sqlmodel import Session, select

from app.core.config import settings
from app.core.object_storage import delete_object, get_bytes, put_bytes
from app.models import ImageAsset, ImageJobStatus, ImageProcessingJob, ImageStatus
from app.tasks import dispatch_pending_image_jobs
from app.worker import celery_app
from tests.api.routes.test_reviews_rankings import (
    create_published_dish,
    create_user_with_headers,
)


def wait_status(db: Session, image_id: uuid.UUID, expected: ImageStatus) -> ImageAsset:
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        db.expire_all()
        image = db.get(ImageAsset, image_id)
        assert image
        if image.status == expected:
            return image
        db.rollback()
        time.sleep(0.1)
    raise AssertionError(f"Image did not reach {expected}")


def test_real_minio_rabbitmq_worker_recovery(
    client: TestClient, db: Session, superuser_token_headers: dict[str, str]
) -> None:
    dish = create_published_dish(client, superuser_token_headers)
    _, headers = create_user_with_headers(client, db)
    queue = f"stage5-{uuid.uuid4().hex}"
    old_queue = celery_app.conf.task_default_queue
    celery_app.conf.task_default_queue = queue
    env = os.environ.copy()
    env["DATABASE_URL"] = str(settings.DATABASE_URL)
    env["IMAGE_TASK_QUEUE"] = queue
    worker: subprocess.Popen[bytes] | None = None
    original_key: str | None = None
    thumbnail_key: str | None = None

    def start_worker() -> subprocess.Popen[bytes]:
        return subprocess.Popen(
            [
                sys.executable,
                "-m",
                "celery",
                "-A",
                "app.worker.celery_app",
                "worker",
                "--concurrency=1",
                "--without-mingle",
                "--without-gossip",
                "--loglevel=ERROR",
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    try:
        content = BytesIO()
        Image.new("RGB", (900, 600), color=(10, 80, 120)).save(content, "PNG")
        data = content.getvalue()
        response = client.post(
            f"{settings.API_V1_STR}/dishes/{dish['id']}/images",
            headers=headers,
            files={"file": ("untrusted.jpg", data, "image/jpeg")},
        )
        assert response.status_code == 200
        image_id = uuid.UUID(response.json()["id"])
        image = db.get(ImageAsset, image_id)
        assert image
        original_key = image.original_object_key
        assert get_bytes(original_key) == data
        worker = start_worker()
        image = wait_status(db, image_id, ImageStatus.READY)
        thumbnail_key = image.thumbnail_object_key
        assert thumbnail_key
        with Image.open(BytesIO(get_bytes(thumbnail_key))) as thumbnail:
            assert thumbnail.format == "WEBP"
            assert thumbnail.size == (480, 320)
        url = client.get(
            f"{settings.API_V1_STR}/images/{image_id}/thumbnail-url", headers=headers
        )
        assert url.status_code == 200
        with httpx.Client(trust_env=False) as http:
            assert http.get(url.json()["url"]).status_code == 200
            assert (
                http.get(
                    f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{thumbnail_key}"
                ).status_code
                == 403
            )

        job = db.exec(
            select(ImageProcessingJob).where(ImageProcessingJob.image_id == image_id)
        ).one()
        job_id = job.id
        celery_app.send_task("app.process_image", args=[str(job_id)])
        time.sleep(1)
        db.expire_all()
        assert db.get(ImageProcessingJob, job_id).attempts == 1

        # A stopped worker leaves the durable claim recoverable after restart.
        worker.terminate()
        worker.wait(timeout=15)
        db.rollback()
        job = db.get(ImageProcessingJob, job_id)
        image = db.get(ImageAsset, image_id)
        assert job and image
        job.status = ImageJobStatus.PROCESSING
        job.updated_at = datetime.now(UTC) - timedelta(minutes=6)
        image.status = ImageStatus.PROCESSING
        db.commit()
        assert dispatch_pending_image_jobs.run() >= 1
        worker = start_worker()
        wait_status(db, image_id, ImageStatus.READY)
        assert db.get(ImageProcessingJob, job_id).attempts == 2

        # Invalid stored content is permanent; owner retry works after repair.
        worker.terminate()
        worker.wait(timeout=15)
        put_bytes(
            object_key=original_key, data=b"broken image", content_type="image/png"
        )
        db.rollback()
        job = db.get(ImageProcessingJob, job_id)
        image = db.get(ImageAsset, image_id)
        assert job and image
        job.status = ImageJobStatus.PENDING
        job.dispatched_at = None
        image.status = ImageStatus.PENDING
        db.commit()
        dispatch_pending_image_jobs.run()
        worker = start_worker()
        wait_status(db, image_id, ImageStatus.FAILED)
        _, other_headers = create_user_with_headers(client, db)
        assert (
            client.post(
                f"{settings.API_V1_STR}/images/{image_id}/retry", headers=other_headers
            ).status_code
            == 403
        )
        put_bytes(object_key=original_key, data=data, content_type="image/png")
        assert (
            client.post(
                f"{settings.API_V1_STR}/images/{image_id}/retry", headers=headers
            ).status_code
            == 200
        )
        wait_status(db, image_id, ImageStatus.READY)
    finally:
        if worker and worker.poll() is None:
            worker.terminate()
            worker.wait(timeout=15)
        celery_app.conf.task_default_queue = old_queue
        for key in (original_key, thumbnail_key):
            if key:
                delete_object(key)
