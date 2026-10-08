from functools import lru_cache

from redis import Redis

from app.core.config import settings


@lru_cache
def get_redis() -> Redis:
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)
