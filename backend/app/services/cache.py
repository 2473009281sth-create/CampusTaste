import logging
import random
import secrets
import time
import uuid
from collections.abc import Callable
from typing import Any, cast

from redis.exceptions import RedisError
from sqlmodel import Session, col, select

from app.core.config import settings
from app.core.redis import get_redis
from app.models import Canteen, Dish, Stall

logger = logging.getLogger(__name__)
NULL_VALUE = "__NULL__"
RELEASE_LOCK_SCRIPT = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
  return redis.call('DEL', KEYS[1])
end
return 0
"""


def _ttl(base: int) -> int:
    return base + random.randint(0, settings.CACHE_TTL_JITTER_SECONDS)


def get_or_build_json(*, key: str, builder: Callable[[], str | None]) -> str | None:
    try:
        redis = get_redis()
        cached = redis.get(key)
        if cached is not None:
            return None if cached == NULL_VALUE else str(cached)
    except RedisError:
        logger.warning("Redis cache read failed; falling back to PostgreSQL")
        return builder()

    lock_key = f"lock:{key}"
    lock_token = secrets.token_hex(16)
    try:
        acquired = bool(
            redis.set(
                lock_key,
                lock_token,
                nx=True,
                ex=settings.CACHE_LOCK_TTL_SECONDS,
            )
        )
        if acquired:
            try:
                value = builder()
                try:
                    redis.setex(
                        key,
                        _ttl(
                            settings.CACHE_NULL_TTL_SECONDS
                            if value is None
                            else settings.CACHE_TTL_SECONDS
                        ),
                        NULL_VALUE if value is None else value,
                    )
                except RedisError:
                    logger.warning(
                        "Redis cache write failed; returning database result"
                    )
                return value
            finally:
                try:
                    redis.eval(RELEASE_LOCK_SCRIPT, 1, lock_key, lock_token)
                except RedisError:
                    logger.warning("Redis cache lock release failed; lease will expire")

        deadline = time.monotonic() + (settings.CACHE_LOCK_WAIT_MILLISECONDS / 1000)
        while time.monotonic() < deadline:
            time.sleep(0.03)
            cached = redis.get(key)
            if cached is not None:
                return None if cached == NULL_VALUE else str(cached)
        return builder()
    except RedisError:
        logger.warning("Redis cache rebuild failed; falling back to PostgreSQL")
        return builder()


def get_ranking_version(school_id: uuid.UUID) -> int:
    try:
        value = cast(Any, get_redis().get(f"cache:ranking-version:{school_id}"))
        return int(value) if value is not None else 0
    except RedisError:
        return 0


def invalidate_dish_and_rankings(session: Session, dish_id: uuid.UUID) -> None:
    school_id = session.exec(
        select(Canteen.school_id)
        .join(Stall, col(Canteen.id) == col(Stall.canteen_id))
        .join(Dish, col(Stall.id) == col(Dish.stall_id))
        .where(Dish.id == dish_id)
    ).one_or_none()
    try:
        redis = get_redis()
        redis.delete(f"cache:dish:{dish_id}")
        if school_id:
            redis.incr(f"cache:ranking-version:{school_id}")
    except RedisError:
        logger.warning("Redis cache invalidation failed after database commit")
