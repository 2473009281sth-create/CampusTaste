from typing import Any, cast

from fastapi import HTTPException
from redis.exceptions import RedisError

from app.core.redis import get_redis

RATE_LIMIT_SCRIPT = """
local current = redis.call('INCR', KEYS[1])
if current == 1 then
  redis.call('EXPIRE', KEYS[1], ARGV[1])
end
local ttl = redis.call('TTL', KEYS[1])
return {current, ttl}
"""


def enforce_rate_limit(*, key: str, limit: int, window_seconds: int = 60) -> None:
    try:
        result = cast(
            Any,
            get_redis().eval(RATE_LIMIT_SCRIPT, 1, key, str(window_seconds)),
        )
        current, ttl = int(result[0]), max(int(result[1]), 1)
    except RedisError:
        raise HTTPException(
            status_code=503,
            detail="Rate limit service unavailable",
        )
    if current > limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
            headers={"Retry-After": str(ttl)},
        )
