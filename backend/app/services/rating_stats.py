import uuid
from dataclasses import dataclass

from sqlalchemy import case, func
from sqlmodel import Session, col, select

from app.models import Dish, Review
from app.services.cache import invalidate_dish_and_rankings


@dataclass(frozen=True)
class RatingMismatch:
    dish_id: uuid.UUID
    stored_sum: int
    stored_count: int
    actual_sum: int
    actual_count: int


def validate_or_rebuild_rating_stats(
    session: Session, *, repair: bool = False
) -> list[RatingMismatch]:
    mismatches: list[RatingMismatch] = []
    dish_ids = session.exec(select(Dish.id).order_by(col(Dish.id))).all()
    for dish_id in dish_ids:
        dish = session.exec(
            select(Dish).where(Dish.id == dish_id).with_for_update()
        ).one()
        active = (~col(Review.is_deleted)) & (~col(Review.is_hidden))
        totals = session.exec(
            select(
                func.coalesce(func.sum(case((active, Review.rating), else_=0)), 0),
                func.coalesce(func.sum(case((active, 1), else_=0)), 0),
            ).where(Review.dish_id == dish_id)
        ).one()
        actual_sum, actual_count = int(totals[0]), int(totals[1])
        if (dish.rating_sum, dish.rating_count) != (actual_sum, actual_count):
            mismatches.append(
                RatingMismatch(
                    dish_id=dish.id,
                    stored_sum=dish.rating_sum,
                    stored_count=dish.rating_count,
                    actual_sum=actual_sum,
                    actual_count=actual_count,
                )
            )
            if repair:
                dish.rating_sum = actual_sum
                dish.rating_count = actual_count
                session.add(dish)
    if repair:
        session.commit()
        for mismatch in mismatches:
            invalidate_dish_and_rankings(session, mismatch.dish_id)
    else:
        session.rollback()
    return mismatches
