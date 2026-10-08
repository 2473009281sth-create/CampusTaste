import uuid
from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models import Dish, DishStatus, Review, ReviewCreate, ReviewUpdate, User
from app.services.cache import invalidate_dish_and_rankings


def _lock_dish(session: Session, dish_id: uuid.UUID) -> Dish:
    dish = session.exec(
        select(Dish).where(Dish.id == dish_id).with_for_update()
    ).one_or_none()
    if not dish or dish.status != DishStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Published dish not found")
    return dish


def _lock_review(session: Session, review_id: uuid.UUID) -> Review:
    review = session.exec(
        select(Review).where(Review.id == review_id).with_for_update()
    ).one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


def _require_owner(review: Review, user: User) -> None:
    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")


def _get_review_identity(
    session: Session, review_id: uuid.UUID
) -> tuple[uuid.UUID, uuid.UUID]:
    identity = session.exec(
        select(Review.dish_id, Review.user_id).where(Review.id == review_id)
    ).one_or_none()
    if not identity:
        raise HTTPException(status_code=404, detail="Review not found")
    return identity


def create_review(
    *, session: Session, dish_id: uuid.UUID, review_in: ReviewCreate, user: User
) -> Review:
    dish = _lock_dish(session, dish_id)
    existing = session.exec(
        select(Review).where(
            Review.user_id == user.id,
            Review.dish_id == dish_id,
        )
    ).one_or_none()
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Review already exists; update or restore the existing review",
        )

    review = Review.model_validate(
        review_in, update={"user_id": user.id, "dish_id": dish_id}
    )

    dish.rating_sum += review.rating
    dish.rating_count += 1
    dish.updated_at = datetime.now(UTC)
    session.add(review)
    session.add(dish)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Review already exists")
    session.refresh(review)
    invalidate_dish_and_rankings(session, dish.id)
    return review


def update_review(
    *, session: Session, review_id: uuid.UUID, review_in: ReviewUpdate, user: User
) -> Review:
    dish_id, user_id = _get_review_identity(session, review_id)
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    dish = _lock_dish(session, dish_id)
    review = _lock_review(session, review_id)
    _require_owner(review, user)
    if review.is_deleted:
        raise HTTPException(
            status_code=409, detail="Deleted review must be restored first"
        )

    updates = review_in.model_dump(exclude_unset=True)
    if updates.get("rating") is None and "rating" in updates:
        raise HTTPException(status_code=422, detail="Rating cannot be null")
    old_rating = review.rating
    review.sqlmodel_update(updates)
    now = datetime.now(UTC)
    review.updated_at = now
    if not review.is_hidden and review.rating != old_rating:
        dish.rating_sum += review.rating - old_rating
        dish.updated_at = now
    session.add(review)
    session.add(dish)
    session.commit()
    session.refresh(review)
    invalidate_dish_and_rankings(session, dish.id)
    return review


def delete_review(*, session: Session, review_id: uuid.UUID, user: User) -> Review:
    dish_id, user_id = _get_review_identity(session, review_id)
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    dish = _lock_dish(session, dish_id)
    review = _lock_review(session, review_id)
    _require_owner(review, user)
    if review.is_deleted:
        raise HTTPException(status_code=409, detail="Review is already deleted")

    now = datetime.now(UTC)
    review.is_deleted = True
    review.deleted_at = now
    review.updated_at = now
    if not review.is_hidden:
        dish.rating_sum -= review.rating
        dish.rating_count -= 1
        dish.updated_at = now
    session.add(review)
    session.add(dish)
    session.commit()
    session.refresh(review)
    invalidate_dish_and_rankings(session, dish.id)
    return review


def restore_review(*, session: Session, review_id: uuid.UUID, user: User) -> Review:
    dish_id, user_id = _get_review_identity(session, review_id)
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    dish = _lock_dish(session, dish_id)
    review = _lock_review(session, review_id)
    _require_owner(review, user)
    if not review.is_deleted:
        raise HTTPException(status_code=409, detail="Review is not deleted")

    now = datetime.now(UTC)
    review.is_deleted = False
    review.deleted_at = None
    review.updated_at = now
    if not review.is_hidden:
        dish.rating_sum += review.rating
        dish.rating_count += 1
        dish.updated_at = now
    session.add(review)
    session.add(dish)
    session.commit()
    session.refresh(review)
    invalidate_dish_and_rankings(session, dish.id)
    return review
