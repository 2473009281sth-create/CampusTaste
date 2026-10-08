import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app import crud
from app.api.routes.rankings import SCORE_SCALE
from app.core.config import settings
from app.core.db import engine
from app.models import Dish, Review, ReviewCreate, ReviewUpdate, Stall, User, UserCreate
from app.services.rating_stats import validate_or_rebuild_rating_stats
from app.services.reviews import create_review, update_review
from tests.api.routes.test_catalog_dishes import create_catalog
from tests.utils.user import user_authentication_headers
from tests.utils.utils import random_email, random_lower_string


def create_user_with_headers(
    client: TestClient, db: Session
) -> tuple[uuid.UUID, dict[str, str]]:
    password = random_lower_string()
    user = crud.create_user(
        session=db,
        user_create=UserCreate(email=random_email(), password=password),
    )
    return user.id, user_authentication_headers(
        client=client, email=user.email, password=password
    )


def create_published_dish(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> dict[str, object]:
    stall_id, category_id = create_catalog(client, superuser_token_headers)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/",
        headers=superuser_token_headers,
        json={
            "stall_id": stall_id,
            "category_id": category_id,
            "name": f"评分菜品-{random_lower_string()}",
            "price": "12.00",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_review_lifecycle_updates_aggregate(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish_data = create_published_dish(client, superuser_token_headers)
    _, headers = create_user_with_headers(client, db)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish_data['id']}/reviews",
        headers=headers,
        json={"rating": 5, "content": "很好吃"},
    )
    assert response.status_code == 200
    review_id = response.json()["id"]
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    assert dish and (dish.rating_sum, dish.rating_count) == (5, 1)

    response = client.patch(
        f"{settings.API_V1_STR}/reviews/{review_id}",
        headers=headers,
        json={"rating": 3, "content": "重新评分"},
    )
    assert response.status_code == 200
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    assert dish and (dish.rating_sum, dish.rating_count) == (3, 1)

    response = client.delete(
        f"{settings.API_V1_STR}/reviews/{review_id}", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["is_deleted"] is True
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    assert dish and (dish.rating_sum, dish.rating_count) == (0, 0)

    response = client.post(
        f"{settings.API_V1_STR}/reviews/{review_id}/restore", headers=headers
    )
    assert response.status_code == 200
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    assert dish and (dish.rating_sum, dish.rating_count) == (3, 1)

    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish_data['id']}/reviews",
        headers=headers,
        json={"rating": 4},
    )
    assert response.status_code == 409


def test_review_owner_validation_and_public_filter(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish = create_published_dish(client, superuser_token_headers)
    _, owner_headers = create_user_with_headers(client, db)
    _, other_headers = create_user_with_headers(client, db)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish['id']}/reviews",
        headers=owner_headers,
        json={"rating": 4},
    )
    review_id = response.json()["id"]
    response = client.patch(
        f"{settings.API_V1_STR}/reviews/{review_id}",
        headers=other_headers,
        json={"rating": 1},
    )
    assert response.status_code == 403

    client.delete(f"{settings.API_V1_STR}/reviews/{review_id}", headers=owner_headers)
    response = client.get(f"{settings.API_V1_STR}/dishes/{dish['id']}/reviews")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_review_cursor_handles_equal_timestamps(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish = create_published_dish(client, superuser_token_headers)
    created_ids: list[str] = []
    for rating in (3, 4, 5):
        _, headers = create_user_with_headers(client, db)
        response = client.post(
            f"{settings.API_V1_STR}/dishes/{dish['id']}/reviews",
            headers=headers,
            json={"rating": rating},
        )
        created_ids.append(response.json()["id"])
    same_time = datetime(2026, 1, 1, tzinfo=UTC)
    for review_id in created_ids:
        review = db.get(Review, review_id)
        assert review
        review.created_at = same_time
        db.add(review)
    db.commit()

    seen: list[str] = []
    cursor = None
    while True:
        params = {"limit": 1}
        if cursor:
            params["cursor"] = cursor
        response = client.get(
            f"{settings.API_V1_STR}/dishes/{dish['id']}/reviews", params=params
        )
        assert response.status_code == 200
        body = response.json()
        seen.extend(item["id"] for item in body["data"])
        cursor = body["next_cursor"]
        if not cursor:
            break
    assert set(seen) == set(created_ids)
    assert len(seen) == len(set(seen))


def test_rankings_use_school_average_and_stable_order(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    first = create_published_dish(client, superuser_token_headers)
    stall = db.get(Stall, first["stall_id"])
    assert stall
    canteen_id = stall.canteen_id
    for rating in (5, 5):
        _, headers = create_user_with_headers(client, db)
        response = client.post(
            f"{settings.API_V1_STR}/dishes/{first['id']}/reviews",
            headers=headers,
            json={"rating": rating},
        )
        assert response.status_code == 200
    db.refresh(stall)
    school_id = stall.canteen.school_id if stall.canteen else None
    assert school_id

    response = client.get(f"{settings.API_V1_STR}/rankings/schools/{school_id}")
    assert response.status_code == 200
    body = response.json()
    entry = next(item for item in body["data"] if item["dish"]["id"] == first["id"])
    assert entry["average_rating"] == "5.0000"
    assert entry["weighted_score"] == "5.0000"
    assert body["scope_average"] == "5.0000"
    assert SCORE_SCALE.as_tuple().exponent == -4

    response = client.get(f"{settings.API_V1_STR}/rankings/canteens/{canteen_id}")
    assert response.status_code == 200


def test_rating_rebuild_repairs_drift(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish_data = create_published_dish(client, superuser_token_headers)
    dish = db.get(Dish, dish_data["id"])
    assert dish
    dish.rating_sum = 99
    dish.rating_count = 9
    db.add(dish)
    db.commit()
    mismatches = validate_or_rebuild_rating_stats(db)
    assert any(str(item.dish_id) == dish_data["id"] for item in mismatches)
    validate_or_rebuild_rating_stats(db, repair=True)
    db.refresh(dish)
    assert (dish.rating_sum, dish.rating_count) == (0, 0)


def test_concurrent_reviews_and_updates_keep_aggregate_consistent(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish_data = create_published_dish(client, superuser_token_headers)
    user_ids = [create_user_with_headers(client, db)[0] for _ in range(4)]

    def submit(user_id: uuid.UUID, rating: int) -> None:
        with Session(engine) as session:
            user = session.get(User, user_id)
            assert user
            create_review(
                session=session,
                dish_id=uuid.UUID(str(dish_data["id"])),
                review_in=ReviewCreate(rating=rating),
                user=user,
            )

    ratings = [1, 2, 4, 5]
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(submit, user_ids, ratings))
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    assert dish and (dish.rating_sum, dish.rating_count) == (sum(ratings), 4)

    review = db.exec(
        select(Review).where(
            Review.dish_id == uuid.UUID(str(dish_data["id"])),
            Review.user_id == user_ids[0],
        )
    ).one()

    def change_rating(rating: int) -> None:
        with Session(engine) as session:
            user = session.get(User, user_ids[0])
            assert user
            update_review(
                session=session,
                review_id=review.id,
                review_in=ReviewUpdate(rating=rating),
                user=user,
            )

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(change_rating, [3, 5]))
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    current_review = db.get(Review, review.id)
    assert dish and current_review
    assert dish.rating_sum == sum(ratings[1:]) + current_review.rating
    assert dish.rating_count == 4


def test_same_user_concurrent_create_has_one_winner(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish_data = create_published_dish(client, superuser_token_headers)
    user_id, _ = create_user_with_headers(client, db)

    def submit(rating: int) -> int:
        with Session(engine) as session:
            user = session.get(User, user_id)
            assert user
            try:
                create_review(
                    session=session,
                    dish_id=uuid.UUID(str(dish_data["id"])),
                    review_in=ReviewCreate(rating=rating),
                    user=user,
                )
                return 200
            except HTTPException as error:
                return error.status_code

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(submit, [2, 5]))
    assert sorted(results) == [200, 409]
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    reviews = db.exec(
        select(Review).where(
            Review.dish_id == uuid.UUID(str(dish_data["id"])),
            Review.user_id == user_id,
        )
    ).all()
    assert dish and len(reviews) == 1
    assert (dish.rating_sum, dish.rating_count) == (reviews[0].rating, 1)
