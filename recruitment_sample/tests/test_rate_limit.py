import pytest
from fastapi import HTTPException

from app.services.rate_limit import enforce_rate_limit


def test_exact_limit_allowed_then_rejected(redis_fake):
    for _ in range(3):
        enforce_rate_limit(key='requests', limit=3, window_seconds=60)
    assert redis_fake.expirations['requests'] == 60
    with pytest.raises(HTTPException) as error:
        enforce_rate_limit(key='requests', limit=3)
    assert error.value.status_code == 429
    assert error.value.headers == {'Retry-After': '60'}


@pytest.mark.parametrize('ttl', [-1, 0, 12])
def test_retry_after_is_at_least_one(redis_fake, ttl):
    redis_fake.rate_ttl = ttl
    with pytest.raises(HTTPException) as error:
        enforce_rate_limit(key='requests', limit=0)
    assert error.value.headers == {'Retry-After': str(max(ttl, 1))}


def test_unavailable_redis_fails_closed(redis_fake):
    redis_fake.fail.add('eval')
    with pytest.raises(HTTPException) as error:
        enforce_rate_limit(key='requests', limit=10)
    assert error.value.status_code == 503


def test_keys_are_isolated(redis_fake):
    enforce_rate_limit(key='a', limit=1)
    enforce_rate_limit(key='b', limit=1)
    assert redis_fake.values == {'a': 1, 'b': 1}
