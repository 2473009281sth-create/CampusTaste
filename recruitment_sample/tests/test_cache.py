from unittest.mock import Mock

import pytest

from app.services import cache


@pytest.mark.parametrize("value, expected", [('{}', '{}'), (cache.NULL_VALUE, None)])
def test_hit_skips_builder(redis_fake, builder, value, expected):
    redis_fake.values['dish'] = value
    assert cache.get_or_build_json(key='dish', builder=builder) == expected
    builder.assert_not_called()


@pytest.mark.parametrize("value, ttl", [('{}', 307), (None, 37)])
def test_rebuild_caches_with_jitter_and_releases_lock(redis_fake, value, ttl):
    build = Mock(return_value=value)
    assert cache.get_or_build_json(key='dish', builder=build) == value
    build.assert_called_once_with()
    assert redis_fake.values['dish'] == (cache.NULL_VALUE if value is None else value)
    assert redis_fake.expirations['dish'] == ttl
    assert redis_fake.expirations['lock:dish'] == 10
    assert 'lock:dish' not in redis_fake.values


@pytest.mark.parametrize('operation', ['get', 'set', 'setex', 'eval'])
def test_redis_failure_returns_source_result(redis_fake, builder, operation):
    redis_fake.fail.add(operation)
    assert cache.get_or_build_json(key='dish', builder=builder) == builder.return_value
    builder.assert_called_once_with()


def test_builder_error_propagates_and_unlocks(redis_fake):
    def broken():
        raise ValueError('synthetic source failure')
    with pytest.raises(ValueError, match='synthetic source failure'):
        cache.get_or_build_json(key='dish', builder=broken)
    assert 'lock:dish' not in redis_fake.values
    assert 'dish' not in redis_fake.values


def test_release_does_not_delete_another_owners_lock(redis_fake):
    def rebuild():
        redis_fake.values['lock:dish'] = 'synthetic-new-owner'
        return '{}'
    assert cache.get_or_build_json(key='dish', builder=rebuild) == '{}'
    assert redis_fake.values['lock:dish'] == 'synthetic-new-owner'


def test_busy_lock_reads_other_workers_result(redis_fake, builder, monkeypatch):
    redis_fake.lock_busy = True
    times = iter([0, 0.01])
    monkeypatch.setattr(cache.time, 'monotonic', lambda: next(times))
    monkeypatch.setattr(cache.time, 'sleep', lambda _: redis_fake.values.update(dish='{}'))
    assert cache.get_or_build_json(key='dish', builder=builder) == '{}'
    builder.assert_not_called()


def test_busy_lock_times_out_and_builds_without_writing(redis_fake, builder, monkeypatch):
    redis_fake.lock_busy = True
    times = iter([0, 1])
    monkeypatch.setattr(cache.time, 'monotonic', lambda: next(times))
    assert cache.get_or_build_json(key='dish', builder=builder) == builder.return_value
    builder.assert_called_once_with()
    assert 'dish' not in redis_fake.values


def test_redis_read_fails_while_waiting(redis_fake, builder, monkeypatch):
    redis_fake.lock_busy = True
    times = iter([0, 0.01])
    monkeypatch.setattr(cache.time, 'monotonic', lambda: next(times))
    monkeypatch.setattr(cache.time, 'sleep', lambda _: redis_fake.fail.add('get'))
    assert cache.get_or_build_json(key='dish', builder=builder) == builder.return_value
    builder.assert_called_once_with()
