"""Deterministic fake: tests never connect to Redis or read a real .env."""
import os
from unittest.mock import Mock

import pytest
from redis.exceptions import RedisError

for name, value in {
    "REDIS_URL": "redis://localhost:6379/0",
    "CACHE_TTL_SECONDS": "300",
    "CACHE_NULL_TTL_SECONDS": "30",
    "CACHE_TTL_JITTER_SECONDS": "60",
    "CACHE_LOCK_TTL_SECONDS": "10",
    "CACHE_LOCK_WAIT_MILLISECONDS": "300",
}.items():
    os.environ[name] = value

from app.services import cache, rate_limit


class FakeRedis:
    def __init__(self):
        self.values = {}
        self.expirations = {}
        self.fail = set()
        self.lock_busy = False
        self.rate_ttl = 60

    def check(self, operation):
        if operation in self.fail:
            raise RedisError("synthetic Redis failure")

    def get(self, key):
        self.check("get")
        return self.values.get(key)

    def set(self, key, value, *, nx, ex):
        self.check("set")
        assert nx is True
        if self.lock_busy or key in self.values:
            return False
        self.values[key] = value
        self.expirations[key] = ex
        return True

    def setex(self, key, ttl, value):
        self.check("setex")
        self.values[key] = value
        self.expirations[key] = ttl

    def eval(self, script, count, key, argument):
        self.check("eval")
        assert count == 1
        if script == cache.RELEASE_LOCK_SCRIPT:
            if self.values.get(key) == argument:
                del self.values[key]
                return 1
            return 0
        assert script == rate_limit.RATE_LIMIT_SCRIPT
        current = int(self.values.get(key, 0)) + 1
        self.values[key] = current
        if current == 1:
            self.expirations[key] = int(argument)
        return [current, self.rate_ttl]


@pytest.fixture
def redis_fake(monkeypatch):
    fake = FakeRedis()
    monkeypatch.setattr(cache, "get_redis", lambda: fake)
    monkeypatch.setattr(rate_limit, "get_redis", lambda: fake)
    monkeypatch.setattr(cache.random, "randint", lambda lower, upper: 7)
    return fake


@pytest.fixture
def builder():
    return Mock(return_value='{"id":"demo-dish"}')
