import uuid
from datetime import UTC, datetime
from io import BytesIO

import pytest
from celery.exceptions import Retry
from fastapi.testclient import TestClient
from PIL import Image
from sqlmodel import Session, select

from app.core.config import settings
from app.models import (
    ImageAsset,
    ImageJobStatus,
    ImageProcessingJob,
    ImageStatus,
    Review,
)
from app.tasks import dispatch_pending_image_jobs, process_image
from tests.api.routes.test_reviews_rankings import (
    create_published_dish,
    create_user_with_headers,
)


def png_bytes() -> bytes:
    output = BytesIO()
    Image.new("RGB", (80, 60), color=(30, 160, 90)).save(output, format="PNG")
    return output.getvalue()


def test_upload_validates_content_and_persists_pending_job(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    monkeypatch: object,
) -> None:
    dish = create_published_dish(client, superuser_token_headers)
    user_id, headers = create_user_with_headers(client, db)
    stored: list[tuple[str, bytes, str]] = []

    def fake_put(*, object_key: str, data: bytes, content_type: str) -> None:
        stored.append((object_key, data, content_type))

    monkeypatch.setattr("app.services.images.put_bytes", fake_put)  # type: ignore[attr-defined]
    monkeypatch.setattr(  # type: ignore[attr-defined]
        "app.services.images.dispatch_image_job", lambda _job_id: False
    )

    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish['id']}/images",
        headers=headers,
        files={"file": ("../../fake.jpg", png_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["owner_id"] == str(user_id)
    assert payload["content_type"] == "image/png"
    assert payload["status"] == "pending"
    assert stored[0][0].startswith("originals/")
    assert stored[0][0].endswith(".png")
    assert "fake" not in stored[0][0]
    image_id = uuid.UUID(payload["id"])
    job = db.exec(
        select(ImageProcessingJob).where(ImageProcessingJob.image_id == image_id)
    ).one()
    assert job.status == ImageJobStatus.PENDING

    invalid = client.post(
        f"{settings.API_V1_STR}/dishes/{dish['id']}/images",
        headers=headers,
        files={"file": ("looks-valid.png", b"not an image", "image/png")},
    )
    assert invalid.status_code == 422


def test_thumbnail_task_is_idempotent(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    monkeypatch: object,
) -> None:
    dish = create_published_dish(client, superuser_token_headers)
    user_id, _ = create_user_with_headers(client, db)
    image = ImageAsset(
        owner_id=user_id,
        dish_id=uuid.UUID(dish["id"]),
        original_object_key=f"originals/{uuid.uuid4()}.png",
        content_type="image/png",
        byte_size=len(png_bytes()),
        width=80,
        height=60,
    )
    db.add(image)
    db.flush()
    job = ImageProcessingJob(image_id=image.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    writes: list[str] = []
    monkeypatch.setattr("app.tasks.get_bytes", lambda _key: png_bytes())  # type: ignore[attr-defined]
    monkeypatch.setattr(  # type: ignore[attr-defined]
        "app.tasks.put_bytes",
        lambda *, object_key, data, content_type: writes.append(object_key),
    )

    process_image.run(str(job.id))
    process_image.run(str(job.id))

    db.expire_all()
    current_image = db.get(ImageAsset, image.id)
    current_job = db.get(ImageProcessingJob, job.id)
    assert current_image and current_image.status == ImageStatus.READY
    assert current_job and current_job.status == ImageJobStatus.SUCCEEDED
    assert current_job.attempts == 1
    assert writes == [f"thumbnails/{image.id}.webp"]


def test_compensation_dispatches_committed_pending_job(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    monkeypatch: object,
) -> None:
    dish = create_published_dish(client, superuser_token_headers)
    user_id, _ = create_user_with_headers(client, db)
    image = ImageAsset(
        owner_id=user_id,
        dish_id=uuid.UUID(dish["id"]),
        original_object_key=f"originals/{uuid.uuid4()}.png",
        content_type="image/png",
        byte_size=10,
        width=1,
        height=1,
    )
    db.add(image)
    db.flush()
    job = ImageProcessingJob(image_id=image.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    dispatched: list[uuid.UUID] = []
    monkeypatch.setattr(  # type: ignore[attr-defined]
        "app.tasks.dispatch_image_job",
        lambda job_id: dispatched.append(job_id) or True,
    )

    count = dispatch_pending_image_jobs.run()

    assert count >= 1
    assert job.id in dispatched
    db.expire_all()
    current = db.get(ImageProcessingJob, job.id)
    assert current and current.dispatched_at is not None


def test_transient_retry_bound_and_permanent_failure(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dish = create_published_dish(client, superuser_token_headers)
    user_id, headers = create_user_with_headers(client, db)
    image = ImageAsset(
        owner_id=user_id,
        dish_id=uuid.UUID(dish["id"]),
        original_object_key=f"originals/{uuid.uuid4()}.png",
        content_type="image/png",
        byte_size=20,
        width=10,
        height=10,
    )
    db.add(image)
    db.flush()
    job = ImageProcessingJob(image_id=image.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    job_id, image_id = job.id, image.id

    def unavailable(_key: str) -> bytes:
        raise ConnectionError("temporary outage")

    monkeypatch.setattr("app.tasks.get_bytes", unavailable)
    for attempt in range(1, settings.IMAGE_TASK_MAX_ATTEMPTS + 1):
        if attempt < settings.IMAGE_TASK_MAX_ATTEMPTS:
            with pytest.raises(Retry):
                process_image.run(str(job_id))
        else:
            process_image.run(str(job_id))
        db.expire_all()
        job = db.get(ImageProcessingJob, job_id)
        assert job and job.attempts == attempt
        if attempt < settings.IMAGE_TASK_MAX_ATTEMPTS:
            assert job.status == ImageJobStatus.PENDING
            assert job.next_attempt_at > datetime.now(UTC)
            # A duplicate arriving before the backoff deadline does not consume an attempt.
            process_image.run(str(job_id))
            job.next_attempt_at = datetime.now(UTC)
            db.commit()
    assert db.get(ImageAsset, image_id).status == ImageStatus.FAILED
    process_image.run(str(job_id))
    db.expire_all()
    assert (
        db.get(ImageProcessingJob, job_id).attempts == settings.IMAGE_TASK_MAX_ATTEMPTS
    )
    failed = client.get(
        f"{settings.API_V1_STR}/image-jobs/failed", headers=superuser_token_headers
    )
    assert failed.status_code == 200
    assert image_id.hex in str(failed.json()).replace("-", "")

    monkeypatch.setattr("app.services.images.dispatch_image_job", lambda _job_id: False)
    assert (
        client.post(
            f"{settings.API_V1_STR}/images/{image_id}/retry", headers=headers
        ).status_code
        == 200
    )
    monkeypatch.setattr("app.tasks.get_bytes", lambda _key: b"bad image")
    process_image.run(str(job_id))
    db.expire_all()
    assert db.get(ImageProcessingJob, job_id).status == ImageJobStatus.FAILED
    assert (
        db.get(ImageAsset, image_id).error_message
        == "Stored original is not a valid image"
    )


def test_review_image_ownership_and_hidden_access(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dish = create_published_dish(client, superuser_token_headers)
    _, owner_headers = create_user_with_headers(client, db)
    _, other_headers = create_user_with_headers(client, db)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish['id']}/reviews",
        headers=owner_headers,
        json={"rating": 4},
    )
    review_id = response.json()["id"]
    path = f"{settings.API_V1_STR}/reviews/{review_id}/images"
    monkeypatch.setattr("app.services.images.put_bytes", lambda **_kwargs: None)
    monkeypatch.setattr("app.services.images.dispatch_image_job", lambda _job_id: False)
    files = {"file": ("a.png", png_bytes(), "image/png")}
    assert client.post(path, headers=other_headers, files=files).status_code == 403
    response = client.post(path, headers=owner_headers, files=files)
    assert response.status_code == 200
    image_id = response.json()["id"]
    metadata = f"{settings.API_V1_STR}/images/{image_id}"
    assert client.get(metadata, headers=other_headers).status_code == 200
    assert (
        client.get(metadata + "/thumbnail-url", headers=owner_headers).status_code
        == 409
    )
    monkeypatch.setattr(
        "app.services.images.presigned_get_url",
        lambda _key: "http://example.test/image",
    )
    assert (
        client.get(metadata + "/original-url", headers=owner_headers).status_code == 200
    )
    assert client.post(metadata + "/retry", headers=owner_headers).status_code == 409
    assert (
        client.get(
            f"{settings.API_V1_STR}/images/{uuid.uuid4()}", headers=owner_headers
        ).status_code
        == 404
    )
    review = db.get(Review, uuid.UUID(review_id))
    assert review
    review.is_hidden = True
    db.commit()
    assert client.get(metadata, headers=other_headers).status_code == 403
    assert (
        client.get(metadata + "/original-url", headers=other_headers).status_code == 403
    )
    assert client.get(metadata, headers=owner_headers).status_code == 200
    review.is_deleted = True
    db.commit()
    assert client.post(path, headers=owner_headers, files=files).status_code == 409
