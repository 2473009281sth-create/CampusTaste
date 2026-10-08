from dataclasses import dataclass
from typing import Any, cast

import jwt
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError
from redis.exceptions import RedisError

from app.core import security
from app.core.config import settings
from app.core.redis import get_redis
from app.models import TokenPayload

ROTATE_SCRIPT = """
if redis.call('EXISTS', KEYS[4]) == 1 then return -2 end
if redis.call('EXISTS', KEYS[1]) == 0 then return 0 end
if redis.call('HGET', KEYS[1], 'token_hash') ~= ARGV[1] then return 0 end
if redis.call('HGET', KEYS[1], 'state') ~= 'active' then
  redis.call('SET', KEYS[4], '1', 'EX', ARGV[6])
  return -1
end
redis.call('HSET', KEYS[1], 'state', 'rotated', 'successor', ARGV[2])
redis.call('HSET', KEYS[2],
  'user_id', ARGV[3], 'family', ARGV[4],
  'token_hash', ARGV[5], 'state', 'active')
redis.call('EXPIRE', KEYS[2], ARGV[6])
redis.call('SADD', KEYS[3], ARGV[2])
redis.call('EXPIRE', KEYS[3], ARGV[6])
return 1
"""

REVOKE_SCRIPT = """
if redis.call('EXISTS', KEYS[1]) == 0 then return 0 end
if redis.call('HGET', KEYS[1], 'token_hash') ~= ARGV[1] then return 0 end
redis.call('SET', KEYS[2], '1', 'EX', ARGV[2])
redis.call('HSET', KEYS[1], 'state', 'revoked')
return 1
"""


@dataclass(frozen=True)
class RefreshClaims:
    user_id: str
    jti: str
    family: str


def _decode(token: str) -> RefreshClaims:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if (
            token_data.type != "refresh"
            or not token_data.sub
            or not token_data.jti
            or not token_data.family
        ):
            raise InvalidTokenError
        return RefreshClaims(
            user_id=token_data.sub,
            jti=token_data.jti,
            family=token_data.family,
        )
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")


def issue_refresh_token(user_id: object) -> str:
    token, jti, family, ttl = security.create_refresh_token(user_id)
    try:
        redis = get_redis()
        key = f"auth:refresh:{jti}"
        family_key = f"auth:refresh-family:{family}"
        with redis.pipeline(transaction=True) as pipe:
            pipe.hset(
                key,
                mapping={
                    "user_id": str(user_id),
                    "family": family,
                    "token_hash": security.hash_token(token),
                    "state": "active",
                },
            )
            pipe.expire(key, ttl)
            pipe.sadd(family_key, jti)
            pipe.expire(family_key, ttl)
            pipe.execute()
    except RedisError:
        raise HTTPException(
            status_code=503, detail="Authentication service unavailable"
        )
    return token


def inspect_refresh_token(token: str) -> RefreshClaims:
    return _decode(token)


def rotate_refresh_token(token: str) -> tuple[str, RefreshClaims]:
    claims = _decode(token)
    new_token, new_jti, family, ttl = security.create_refresh_token(
        claims.user_id, family=claims.family
    )
    try:
        result = int(
            cast(
                Any,
                get_redis().eval(
                    ROTATE_SCRIPT,
                    4,
                    f"auth:refresh:{claims.jti}",
                    f"auth:refresh:{new_jti}",
                    f"auth:refresh-family:{family}",
                    f"auth:refresh-family-revoked:{family}",
                    security.hash_token(token),
                    new_jti,
                    claims.user_id,
                    family,
                    security.hash_token(new_token),
                    str(ttl),
                ),
            )
        )
    except RedisError:
        raise HTTPException(
            status_code=503, detail="Authentication service unavailable"
        )
    if result == 1:
        return new_token, claims
    if result == -1:
        raise HTTPException(
            status_code=403,
            detail="Refresh token reuse detected; token family revoked",
        )
    if result == -2:
        raise HTTPException(status_code=403, detail="Refresh token family revoked")
    raise HTTPException(status_code=403, detail="Invalid refresh token")


def revoke_refresh_family(token: str) -> None:
    claims = _decode(token)
    ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    try:
        result = int(
            cast(
                Any,
                get_redis().eval(
                    REVOKE_SCRIPT,
                    2,
                    f"auth:refresh:{claims.jti}",
                    f"auth:refresh-family-revoked:{claims.family}",
                    security.hash_token(token),
                    str(ttl),
                ),
            )
        )
    except RedisError:
        raise HTTPException(
            status_code=503, detail="Authentication service unavailable"
        )
    if result != 1:
        raise HTTPException(status_code=403, detail="Invalid refresh token")
