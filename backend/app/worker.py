from celery import Celery  # type: ignore[import-untyped]

from app.core.config import settings
from app.core.observability import configure_logging

configure_logging()

celery_app = Celery("campustaste", broker=settings.RABBITMQ_URL)
celery_app.conf.update(
    task_serializer="json",
    task_default_queue=settings.IMAGE_TASK_QUEUE,
    accept_content=["json"],
    result_backend=None,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    worker_enable_remote_control=False,
    broker_connection_timeout=3,
    task_publish_retry=False,
    broker_connection_retry_on_startup=True,
    imports=("app.tasks",),
    beat_schedule={
        "dispatch-pending-image-jobs": {
            "task": "app.dispatch_pending_image_jobs",
            "schedule": 30.0,
        }
    },
)
celery_app.autodiscover_tasks(["app"])
