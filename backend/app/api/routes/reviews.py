import base64
import json
import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import col, select

from app.api.deps import CurrentUser, SessionDep
from app.core.config import settings
from app.models import (
    Dish,
    DishStatus,
    Review,
    ReviewCreate,
    ReviewPublic,
    ReviewsPage,
    ReviewUpdate,
)
from app.services.rate_limit import enforce_rate_limit
from app.services.reviews import (
    create_review,
    delete_review,
    restore_review,
    update_review,
)

router = APIRouter(tags=["reviews"])


def _encode_cursor(review: Review) -> str:
    payload = json.dumps(
        {"created_at": review.created_at.isoformat(), "id": str(review.id)},
        separators=(",", ":"),
    ).encode()
    return base64.urlsafe_b64encode(payload).decode().rstrip("=")


def _decode_cursor(cursor: str) -> tuple[datetime, uuid.UUID]:
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded).decode())
        return datetime.fromisoformat(data["created_at"]), uuid.UUID(data["id"])
    except ValueError, KeyError, TypeError, json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid review cursor")


@router.get("/dishes/{dish_id}/reviews", response_model=ReviewsPage)
def read_reviews(
    session: SessionDep,
    dish_id: uuid.UUID,
    cursor: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> Any:
    dish = session.get(Dish, dish_id)
    if not dish or dish.status != DishStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Published dish not found")
    statement = select(Review).where(
        Review.dish_id == dish_id,
        col(Review.is_deleted).is_(False),
        col(Review.is_hidden).is_(False),
    )
    if cursor:
        created_at, review_id = _decode_cursor(cursor)
        statement = statement.where(
            (col(Review.created_at) < created_at)
            | ((col(Review.created_at) == created_at) & (col(Review.id) < review_id))
        )
    reviews = session.exec(
        statement.order_by(col(Review.created_at).desc(), col(Review.id).desc()).limit(
            limit + 1
        )
    ).all()
    has_more = len(reviews) > limit
    page = list(reviews[:limit])
    return ReviewsPage(
        data=[ReviewPublic.model_validate(review) for review in page],
        next_cursor=_encode_cursor(page[-1]) if has_more and page else None,
    )


@router.post("/dishes/{dish_id}/reviews", response_model=ReviewPublic)
def submit_review(
    session: SessionDep,
    current_user: CurrentUser,
    dish_id: uuid.UUID,
    review_in: ReviewCreate,
) -> Any:
    enforce_rate_limit(
        key=f"rate:reviews:{current_user.id}",
        limit=settings.REVIEW_RATE_LIMIT_PER_MINUTE,
    )
    return create_review(
        session=session, dish_id=dish_id, review_in=review_in, user=current_user
    )


@router.patch("/reviews/{review_id}", response_model=ReviewPublic)
def edit_review(
    session: SessionDep,
    current_user: CurrentUser,
    review_id: uuid.UUID,
    review_in: ReviewUpdate,
) -> Any:
    enforce_rate_limit(
        key=f"rate:reviews:{current_user.id}",
        limit=settings.REVIEW_RATE_LIMIT_PER_MINUTE,
    )
    return update_review(
        session=session, review_id=review_id, review_in=review_in, user=current_user
    )


@router.delete("/reviews/{review_id}", response_model=ReviewPublic)
def remove_review(
    session: SessionDep, current_user: CurrentUser, review_id: uuid.UUID
) -> Any:
    enforce_rate_limit(
        key=f"rate:reviews:{current_user.id}",
        limit=settings.REVIEW_RATE_LIMIT_PER_MINUTE,
    )
    return delete_review(session=session, review_id=review_id, user=current_user)


@router.post("/reviews/{review_id}/restore", response_model=ReviewPublic)
def restore_deleted_review(
    session: SessionDep, current_user: CurrentUser, review_id: uuid.UUID
) -> Any:
    enforce_rate_limit(
        key=f"rate:reviews:{current_user.id}",
        limit=settings.REVIEW_RATE_LIMIT_PER_MINUTE,
    )
    return restore_review(session=session, review_id=review_id, user=current_user)
