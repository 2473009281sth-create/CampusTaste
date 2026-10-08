from datetime import UTC, datetime

from fastapi import HTTPException
from sqlmodel import Session

from app.models import (
    Category,
    Dish,
    DishCreate,
    DishReview,
    DishStatus,
    Stall,
    User,
    UserRole,
)
from app.services.cache import invalidate_dish_and_rankings


def validate_dish_references(
    *, session: Session, stall_id: object, category_id: object | None
) -> None:
    stall = session.get(Stall, stall_id)
    if not stall or not stall.is_active:
        raise HTTPException(status_code=400, detail="Active stall not found")
    if category_id is not None:
        category = session.get(Category, category_id)
        if not category or not category.is_active:
            raise HTTPException(status_code=400, detail="Active category not found")


def create_dish(*, session: Session, dish_in: DishCreate, current_user: User) -> Dish:
    validate_dish_references(
        session=session,
        stall_id=dish_in.stall_id,
        category_id=dish_in.category_id,
    )
    is_admin = current_user.is_superuser or current_user.role == UserRole.ADMIN
    now = datetime.now(UTC)
    dish = Dish.model_validate(
        dish_in,
        update={
            "submitted_by_id": current_user.id,
            "status": DishStatus.PUBLISHED if is_admin else DishStatus.PENDING,
            "reviewed_by_id": current_user.id if is_admin else None,
            "reviewed_at": now if is_admin else None,
            "published_at": now if is_admin else None,
        },
    )
    session.add(dish)
    session.commit()
    session.refresh(dish)
    if dish.status == DishStatus.PUBLISHED:
        invalidate_dish_and_rankings(session, dish.id)
    return dish


def review_dish(
    *, session: Session, dish: Dish, review: DishReview, reviewer: User
) -> Dish:
    if dish.status != DishStatus.PENDING:
        raise HTTPException(
            status_code=409, detail="Only pending dishes can be reviewed"
        )
    if review.status not in {DishStatus.PUBLISHED, DishStatus.REJECTED}:
        raise HTTPException(
            status_code=422, detail="Review status must be published or rejected"
        )
    if review.status == DishStatus.REJECTED and not review.review_note:
        raise HTTPException(status_code=422, detail="Rejection requires a review note")

    now = datetime.now(UTC)
    dish.status = review.status
    dish.review_note = review.review_note
    dish.reviewed_by_id = reviewer.id
    dish.reviewed_at = now
    dish.published_at = now if review.status == DishStatus.PUBLISHED else None
    dish.updated_at = now
    session.add(dish)
    session.commit()
    session.refresh(dish)
    invalidate_dish_and_rankings(session, dish.id)
    return dish
