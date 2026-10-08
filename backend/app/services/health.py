from collections.abc import Callable
from urllib.request import ProxyHandler, build_opener

from kombu import Connection  # type: ignore[import-untyped]
from redis import Redis
from sqlalchemy import create_engine, text

from app.core.config import settings


def check_postgresql() -> None:
    probe = create_engine(
        str(settings.DATABASE_URL),
        connect_args={"connect_timeout": 2, "options": "-c statement_timeout=2000"},
    )
    try:
        with probe.connect() as connection:
            connection.execute(text("SELECT 1"))
    finally:
        probe.dispose()


def check_redis() -> None:
    with Redis.from_url(
        settings.REDIS_URL, socket_connect_timeout=2, socket_timeout=2
    ) as client:
        client.ping()


def check_rabbitmq() -> None:
    with Connection(settings.RABBITMQ_URL, connect_timeout=2) as connection:
        connection.connect()


def check_minio() -> None:
    scheme = "https" if settings.MINIO_SECURE else "http"
    url = f"{scheme}://{settings.MINIO_ENDPOINT}/minio/health/ready"
    with build_opener(ProxyHandler({})).open(url, timeout=2) as response:
        if response.status != 200:
            raise RuntimeError("MinIO is not ready")


def readiness() -> dict[str, str]:
    checks: dict[str, Callable[[], None]] = {
        "postgresql": check_postgresql,
        "redis": check_redis,
        "rabbitmq": check_rabbitmq,
        "minio": check_minio,
    }
    results = {}
    for name, check in checks.items():
        try:
            check()
        except Exception:
            results[name] = "unavailable"
        else:
            results[name] = "ok"
    return results
