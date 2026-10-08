import uuid
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient
from sqlmodel import Session, func, select

from app.core.config import settings
from app.core.db import engine
from app.models import (
    Dish,
    ModerationAction,
    ModerationAudit,
    ReportStatus,
    Review,
    ReviewLike,
    ReviewUpdate,
    ReviewVisibilityUpdate,
    User,
)
from app.services.governance import set_review_like, set_review_visibility
from app.services.reviews import update_review
from tests.api.routes.test_catalog_dishes import create_reviewer
from tests.api.routes.test_reviews_rankings import (
    create_published_dish,
    create_user_with_headers,
)


def create_review(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    rating: int = 5,
) -> tuple[dict[str, object], uuid.UUID, uuid.UUID, dict[str, str]]:
    dish = create_published_dish(client, superuser_token_headers)
    user_id, headers = create_user_with_headers(client, db)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish['id']}/reviews",
        headers=headers,
        json={"rating": rating, "content": "阶段四评价"},
    )
    assert response.status_code == 200
    return dish, uuid.UUID(response.json()["id"]), user_id, headers


def test_like_target_state_is_idempotent_and_user_scoped(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    _, review_id, _, _ = create_review(client, db, superuser_token_headers)
    review = db.get(Review, review_id)
    assert review
    _, first_headers = create_user_with_headers(client, db)
    _, second_headers = create_user_with_headers(client, db)
    path = f"{settings.API_V1_STR}/reviews/{review.id}/like"

    for _ in range(2):
        response = client.put(path, headers=first_headers, json={"liked": True})
        assert response.status_code == 200
        assert response.json()["liked"] is True
        assert response.json()["like_count"] == 1

    response = client.put(path, headers=second_headers, json={"liked": True})
    assert response.status_code == 200
    assert response.json()["like_count"] == 2

    for _ in range(2):
        response = client.put(path, headers=first_headers, json={"liked": False})
        assert response.status_code == 200
        assert response.json()["like_count"] == 1

    db.expire_all()
    assert (
        db.exec(
            select(func.count())
            .select_from(ReviewLike)
            .where(ReviewLike.review_id == review.id)
        ).one()
        == 1
    )


def test_concurrent_duplicate_like_has_one_row(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    _, review_id, _, _ = create_review(client, db, superuser_token_headers)
    review = db.get(Review, review_id)
    assert review
    user_id, _ = create_user_with_headers(client, db)

    def like(_: int) -> None:
        with Session(engine) as session:
            user = session.get(User, user_id)
            assert user
            set_review_like(session=session, review_id=review.id, user=user, liked=True)

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(like, range(2)))

    db.expire_all()
    current = db.get(Review, review.id)
    assert current and current.like_count == 1
    assert (
        db.exec(
            select(func.count())
            .select_from(ReviewLike)
            .where(ReviewLike.review_id == review.id)
        ).one()
        == 1
    )


def test_report_resolution_hide_unhide_and_audit(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish_data, review_id, _, owner_headers = create_review(
        client, db, superuser_token_headers, rating=5
    )
    review = db.get(Review, review_id)
    assert review
    _, reporter_headers = create_user_with_headers(client, db)
    reviewer_headers, reviewer_id = create_reviewer(client, db)

    report_path = f"{settings.API_V1_STR}/reviews/{review.id}/reports"
    response = client.post(
        report_path,
        headers=reporter_headers,
        json={"reason": "abuse", "details": "包含不当内容"},
    )
    assert response.status_code == 200
    report_id = response.json()["id"]
    assert response.json()["status"] == ReportStatus.PENDING
    assert response.json()["reporter_id"] != str(review.user_id)

    duplicate = client.post(
        report_path,
        headers=reporter_headers,
        json={"reason": "spam"},
    )
    assert duplicate.status_code == 409
    assert (
        client.get(
            f"{settings.API_V1_STR}/reports", headers=reporter_headers
        ).status_code
        == 403
    )
    assert (
        client.put(
            f"{settings.API_V1_STR}/reviews/{review.id}/visibility",
            headers=reporter_headers,
            json={"is_hidden": True},
        ).status_code
        == 403
    )

    queue = client.get(
        f"{settings.API_V1_STR}/reports",
        headers=reviewer_headers,
        params={"status": "pending", "limit": 10},
    )
    assert queue.status_code == 200
    assert queue.json()["count"] == 1
    assert queue.json()["data"][0]["id"] == report_id

    response = client.post(
        f"{settings.API_V1_STR}/reports/{report_id}/resolve",
        headers=reviewer_headers,
        json={
            "status": "resolved",
            "hide_review": True,
            "resolution_note": "举报成立",
        },
    )
    assert response.status_code == 200
    assert response.json()["handled_by_id"] == reviewer_id
    assert response.json()["status"] == ReportStatus.RESOLVED

    db.expire_all()
    current_review = db.get(Review, review.id)
    dish = db.get(Dish, dish_data["id"])
    assert current_review and current_review.is_hidden
    assert dish and (dish.rating_sum, dish.rating_count) == (0, 0)
    assert (
        client.get(f"{settings.API_V1_STR}/dishes/{dish_data['id']}/reviews").json()[
            "data"
        ]
        == []
    )

    repeated = client.post(
        f"{settings.API_V1_STR}/reports/{report_id}/resolve",
        headers=reviewer_headers,
        json={"status": "resolved", "hide_review": True},
    )
    assert repeated.status_code == 409

    response = client.patch(
        f"{settings.API_V1_STR}/reviews/{review.id}",
        headers=owner_headers,
        json={"rating": 3, "content": "隐藏期间修改"},
    )
    assert response.status_code == 200
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    assert dish and (dish.rating_sum, dish.rating_count) == (0, 0)

    response = client.put(
        f"{settings.API_V1_STR}/reviews/{review.id}/visibility",
        headers=reviewer_headers,
        json={"is_hidden": False, "note": "复核后恢复"},
    )
    assert response.status_code == 200
    assert response.json()["is_hidden"] is False
    db.expire_all()
    dish = db.get(Dish, dish_data["id"])
    assert dish and (dish.rating_sum, dish.rating_count) == (3, 1)

    audits = db.exec(
        select(ModerationAudit)
        .where(ModerationAudit.review_id == review.id)
        .order_by(ModerationAudit.created_at)
    ).all()
    assert [audit.action for audit in audits] == [
        ModerationAction.REPORT_RESOLVED,
        ModerationAction.REVIEW_UNHIDDEN,
    ]
    assert all(str(audit.actor_id) == reviewer_id for audit in audits)
    audit_response = client.get(
        f"{settings.API_V1_STR}/moderation/audits",
        headers=reviewer_headers,
        params={"review_id": str(review.id)},
    )
    assert audit_response.status_code == 200
    assert audit_response.json()["count"] == 2
    assert {item["action"] for item in audit_response.json()["data"]} == {
        "report_resolved",
        "review_unhidden",
    }


def test_concurrent_edit_and_hide_keep_rating_consistent(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
) -> None:
    dish_data, review_id, owner_id, _ = create_review(
        client, db, superuser_token_headers, rating=5
    )
    review = db.get(Review, review_id)
    assert review
    _, reviewer_id = create_reviewer(client, db)

    def edit() -> None:
        with Session(engine) as session:
            owner = session.get(User, owner_id)
            assert owner
            update_review(
                session=session,
                review_id=review.id,
                review_in=ReviewUpdate(rating=2),
                user=owner,
            )

    def hide() -> None:
        with Session(engine) as session:
            reviewer = session.get(User, uuid.UUID(reviewer_id))
            assert reviewer
            set_review_visibility(
                session=session,
                review_id=review.id,
                visibility_in=ReviewVisibilityUpdate(is_hidden=True, note="并发治理"),
                actor=reviewer,
            )

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(lambda operation: operation(), [edit, hide]))

    db.expire_all()
    current_review = db.get(Review, review.id)
    dish = db.get(Dish, dish_data["id"])
    assert current_review and current_review.is_hidden and current_review.rating == 2
    assert dish and (dish.rating_sum, dish.rating_count) == (0, 0)
