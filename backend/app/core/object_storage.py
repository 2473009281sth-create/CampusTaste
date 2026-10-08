from datetime import timedelta
from io import BytesIO

from minio import Minio
from minio.error import S3Error
from urllib3 import PoolManager, Timeout

from app.core.config import settings


def get_object_storage() -> Minio:
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
        http_client=PoolManager(timeout=Timeout(connect=5, read=20), retries=0),
    )


def ensure_image_bucket() -> None:
    client = get_object_storage()
    if not client.bucket_exists(settings.MINIO_BUCKET):
        try:
            client.make_bucket(settings.MINIO_BUCKET)
        except S3Error as exc:
            if exc.code not in {"BucketAlreadyOwnedByYou", "BucketAlreadyExists"}:
                raise


def put_bytes(*, object_key: str, data: bytes, content_type: str) -> None:
    ensure_image_bucket()
    get_object_storage().put_object(
        settings.MINIO_BUCKET,
        object_key,
        BytesIO(data),
        length=len(data),
        content_type=content_type,
    )


def get_bytes(object_key: str) -> bytes:
    response = get_object_storage().get_object(settings.MINIO_BUCKET, object_key)
    try:
        return response.read()
    finally:
        response.close()
        response.release_conn()


def delete_object(object_key: str) -> None:
    get_object_storage().remove_object(settings.MINIO_BUCKET, object_key)


def presigned_get_url(object_key: str) -> str:
    client = Minio(
        settings.MINIO_PUBLIC_ENDPOINT or settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
        region="us-east-1",
    )
    return client.presigned_get_object(
        settings.MINIO_BUCKET,
        object_key,
        expires=timedelta(seconds=settings.IMAGE_URL_EXPIRE_SECONDS),
    )
