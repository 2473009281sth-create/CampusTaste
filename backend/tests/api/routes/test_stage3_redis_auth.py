import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from time import sleep
from typing import Any
from unittest.mock import patch

import jwt
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.redis import get_redis
from app.models import Dish
from app.services.cache import get_or_build_json
from app.services.rate_limit import enforce_rate_limit
from app.services.refresh_tokens import rotate_refresh_token
from tests.api.routes.test_catalog_dishes import create_catalog


class BrokenRedis:
    def __getattr__(self, name: str) -> Any:
        del name
        raise ConnectionError("Redis unavailable")


def login(client: TestClient) -> dict[str, str]:
    response = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        },
    )
    assert response.status_code == 200
    return response.json()


def create_dish(client: TestClient, headers: dict[str, str]) -> dict[str, object]:
    stall_id, category_id = create_catalog(client, headers)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/",
        headers=headers,
        json={
            "stall_id": stall_id,
            "category_id": category_id,
            "name": "缓存测试菜品",
            "price": "10.00",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_refresh_rotation_reuse_revokes_family(client: TestClient) -> None:
    tokens = login(client)
    first_refresh = tokens["refresh_token"]
    response = client.post(
        f"{settings.API_V1_STR}/login/refresh",
        json={"refresh_token": first_refresh},
    )
    assert response.status_code == 200
    second_refresh = response.json()["refresh_token"]
    assert second_refresh != first_refresh

    response = client.post(
        f"{settings.API_V1_STR}/login/refresh",
        json={"refresh_token": first_refresh},
    )
    assert response.status_code == 403
    assert "reuse" in response.json()["detail"].lower()

    response = client.post(
        f"{settings.API_V1_STR}/login/refresh",
        json={"refresh_token": second_refresh},
    )
    assert response.status_code == 403


def test_refresh_store_contains_hash_not_plaintext(client: TestClient) -> None:
    tokens = login(client)
    refresh_token = tokens["refresh_token"]
    payload = jwt.decode(
        refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    stored = get_redis().hgetall(f"auth:refresh:{payload['jti']}")
    assert stored["token_hash"] == security.hash_token(refresh_token)
    assert refresh_token not in stored.values()


def test_concurrent_refresh_has_no_two_valid_successors(client: TestClient) -> None:
    refresh_token = login(client)["refresh_token"]

    def rotate() -> tuple[bool, str | None]:
        try:
            token, _ = rotate_refresh_token(refresh_token)
            return True, token
        except HTTPException:
            return False, None

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: rotate(), range(2)))
    successes = [token for ok, token in results if ok]
    assert len(successes) == 1
    with pytest.raises(HTTPException):
        rotate_refresh_token(successes[0])


def test_logout_revokes_refresh_but_access_lives_until_expiry(
    client: TestClient,
) -> None:
    tokens = login(client)
    response = client.post(
        f"{settings.API_V1_STR}/login/logout",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert response.status_code == 200
    access_headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.post(
        f"{settings.API_V1_STR}/login/test-token", headers=access_headers
    )
    assert response.status_code == 200
    response = client.post(
        f"{settings.API_V1_STR}/login/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert response.status_code == 403


def test_dish_cache_hit_and_redis_failure_fallback(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish_data = create_dish(client, superuser_token_headers)
    path = f"{settings.API_V1_STR}/dishes/{dish_data['id']}"
    first = client.get(path)
    assert first.status_code == 200
    dish = db.get(Dish, dish_data["id"])
    assert dish
    original_name = dish.name
    dish.name = "数据库中的新名称"
    db.add(dish)
    db.commit()
    cached = client.get(path)
    assert cached.json()["name"] == original_name

    with patch("app.services.cache.get_redis", return_value=BrokenRedis()):
        fallback = client.get(path)
    assert fallback.status_code == 200
    assert fallback.json()["name"] == "数据库中的新名称"


def test_negative_cache_avoids_repeated_database_lookup() -> None:
    key = f"cache:test:missing:{uuid.uuid4()}"
    calls = 0

    def missing_builder() -> None:
        nonlocal calls
        calls += 1
        return None

    assert get_or_build_json(key=key, builder=missing_builder) is None
    assert get_or_build_json(key=key, builder=missing_builder) is None
    assert calls == 1
    assert get_redis().get(key) == "__NULL__"
    ttl = get_redis().ttl(key)
    assert (
        0 < ttl <= (settings.CACHE_NULL_TTL_SECONDS + settings.CACHE_TTL_JITTER_SECONDS)
    )


def test_hot_key_mutex_only_rebuilds_once() -> None:
    key = f"cache:test:hot:{uuid.uuid4()}"
    calls = 0
    calls_lock = Lock()

    def builder() -> str:
        nonlocal calls
        with calls_lock:
            calls += 1
        sleep(0.08)
        return '{"name":"同一份结果"}'

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(
            executor.map(
                lambda _: get_or_build_json(key=key, builder=builder), range(10)
            )
        )
    assert results == ['{"name":"同一份结果"}'] * 10
    assert calls == 1


def test_review_invalidates_school_ranking_version(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish_data = create_dish(client, superuser_token_headers)
    dish_id = uuid.UUID(str(dish_data["id"]))
    from app.models import Canteen, Stall

    stall = db.get(Stall, dish_data["stall_id"])
    assert stall
    canteen = db.get(Canteen, stall.canteen_id)
    assert canteen
    version_key = f"cache:ranking-version:{canteen.school_id}"
    version_before = int(get_redis().get(version_key) or 0)
    ranking_path = f"{settings.API_V1_STR}/rankings/schools/{canteen.school_id}"
    before = client.get(ranking_path)
    assert before.status_code == 200
    assert before.json()["data"][0]["rating_count"] == 0

    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish_id}/reviews",
        headers=superuser_token_headers,
        json={"rating": 5},
    )
    assert response.status_code == 200
    assert int(get_redis().get(version_key) or 0) == version_before + 1
    after = client.get(ranking_path)
    assert after.status_code == 200
    assert after.json()["data"][0]["rating_count"] == 1
    assert after.json()["data"][0]["average_rating"] == "5.0000"


def test_rate_limit_is_atomic_and_fails_closed() -> None:
    def attempt(_: int) -> int:
        try:
            enforce_rate_limit(key="rate:test:atomic", limit=10)
            return 200
        except HTTPException as error:
            return error.status_code

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(attempt, range(20)))
    assert results.count(200) == 10
    assert results.count(429) == 10

    with (
        patch("app.services.rate_limit.get_redis", return_value=BrokenRedis()),
        pytest.raises(HTTPException) as error,
    ):
        enforce_rate_limit(key="rate:test:failure", limit=1)
    assert error.value.status_code == 503
