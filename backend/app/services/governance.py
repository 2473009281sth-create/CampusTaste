import uuid
from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, col, func, select

from app.models import (
    Dish,
    ModerationAction,
    ModerationAudit,
    ReportStatus,
    Review,
    ReviewLike,
    ReviewLikePublic,
    ReviewReport,
    ReviewReportCreate,
    ReviewReportResolve,
    ReviewVisibilityUpdate,
    User,
)
from app.services.cache import invalidate_dish_and_rankings


def _lock_review(session: Session, review_id: uuid.UUID) -> Review:
    review = session.exec(
        select(Review).where(Review.id == review_id).with_for_update()
    ).one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


def _lock_dish_then_review(
    session: Session, review_id: uuid.UUID
) -> tuple[Dish, Review]:
    dish_id = session.exec(
        select(Review.dish_id).where(Review.id == review_id)
    ).one_or_none()
    if not dish_id:
        raise HTTPException(status_code=404, detail="Review not found")
    dish = session.exec(select(Dish).where(Dish.id == dish_id).with_for_update()).one()
    review = _lock_review(session, review_id)
    return dish, review


def set_review_like(
    *, session: Session, review_id: uuid.UUID, user: User, liked: bool
) -> ReviewLikePublic:
    review = _lock_review(session, review_id)
    if review.is_deleted or review.is_hidden:
        raise HTTPException(status_code=404, detail="Visible review not found")
    existing = session.exec(
        select(ReviewLike).where(
            ReviewLike.user_id == user.id,
            ReviewLike.review_id == review_id,
        )
    ).one_or_none()
    if liked and not existing:
        session.add(ReviewLike(user_id=user.id, review_id=review_id))
        review.like_count += 1
        session.add(review)
    elif not liked and existing:
        session.delete(existing)
        review.like_count -= 1
        session.add(review)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Like state conflict")
    session.refresh(review)
    return ReviewLikePublic(
        review_id=review.id, liked=liked, like_count=review.like_count
    )


def create_review_report(
    *,
    session: Session,
    review_id: uuid.UUID,
    report_in: ReviewReportCreate,
    reporter: User,
) -> ReviewReport:
    review = _lock_review(session, review_id)
    if review.is_deleted or review.is_hidden:
        raise HTTPException(status_code=404, detail="Visible review not found")
    existing = session.exec(
        select(ReviewReport).where(
            ReviewReport.reporter_id == reporter.id,
            ReviewReport.review_id == review_id,
        )
    ).one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Review already reported")
    report = ReviewReport.model_validate(
        report_in, update={"reporter_id": reporter.id, "review_id": review_id}
    )
    session.add(report)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Review already reported")
    session.refresh(report)
    return report


def _apply_visibility(
    *, dish: Dish, review: Review, is_hidden: bool, now: datetime
) -> bool:
    previous = review.is_hidden
    if previous == is_hidden:
        return False
    if not review.is_deleted:
        if is_hidden:
            dish.rating_sum -= review.rating
            dish.rating_count -= 1
        else:
            dish.rating_sum += review.rating
            dish.rating_count += 1
        dish.updated_at = now
    review.is_hidden = is_hidden
    review.updated_at = now
    return True


def set_review_visibility(
    *,
    session: Session,
    review_id: uuid.UUID,
    visibility_in: ReviewVisibilityUpdate,
    actor: User,
) -> Review:
    dish, review = _lock_dish_then_review(session, review_id)
    now = datetime.now(UTC)
    previous = review.is_hidden
    changed = _apply_visibility(
        dish=dish, review=review, is_hidden=visibility_in.is_hidden, now=now
    )
    if changed:
        session.add(dish)
        session.add(review)
        session.add(
            ModerationAudit(
                actor_id=actor.id,
                action=(
                    ModerationAction.REVIEW_HIDDEN
                    if visibility_in.is_hidden
                    else ModerationAction.REVIEW_UNHIDDEN
                ),
                review_id=review.id,
                previous_hidden=previous,
                new_hidden=review.is_hidden,
                note=visibility_in.note,
            )
        )
    session.commit()
    session.refresh(review)
    if changed:
        invalidate_dish_and_rankings(session, dish.id)
    return review


def process_review_report(
    *,
    session: Session,
    report_id: uuid.UUID,
    resolution: ReviewReportResolve,
    actor: User,
) -> ReviewReport:
    if resolution.status not in {ReportStatus.RESOLVED, ReportStatus.DISMISSED}:
        raise HTTPException(
            status_code=422, detail="Report status must be resolved or dismissed"
        )
    if resolution.status == ReportStatus.DISMISSED and resolution.hide_review:
        raise HTTPException(
            status_code=422, detail="Dismissed report cannot hide review"
        )

    identity = session.exec(
        select(ReviewReport.review_id, Review.dish_id)
        .join(Review, col(ReviewReport.review_id) == col(Review.id))
        .where(ReviewReport.id == report_id)
    ).one_or_none()
    if not identity:
        raise HTTPException(status_code=404, detail="Report not found")
    review_id, dish_id = identity
    dish = session.exec(select(Dish).where(Dish.id == dish_id).with_for_update()).one()
    review = _lock_review(session, review_id)
    report = session.exec(
        select(ReviewReport).where(ReviewReport.id == report_id).with_for_update()
    ).one()
    if report.status != ReportStatus.PENDING:
        raise HTTPException(status_code=409, detail="Report already processed")

    now = datetime.now(UTC)
    previous = review.is_hidden
    changed = False
    if resolution.hide_review:
        changed = _apply_visibility(dish=dish, review=review, is_hidden=True, now=now)
    report.status = resolution.status
    report.resolution_note = resolution.resolution_note
    report.handled_by_id = actor.id
    report.handled_at = now
    session.add(report)
    session.add(
        ModerationAudit(
            actor_id=actor.id,
            action=(
                ModerationAction.REPORT_RESOLVED
                if resolution.status == ReportStatus.RESOLVED
                else ModerationAction.REPORT_DISMISSED
            ),
            review_id=review.id,
            report_id=report.id,
            previous_hidden=previous,
            new_hidden=review.is_hidden,
            note=resolution.resolution_note,
        )
    )
    if changed:
        session.add(dish)
        session.add(review)
    session.commit()
    session.refresh(report)
    if changed:
        invalidate_dish_and_rankings(session, dish.id)
    return report


def report_count(session: Session, status: ReportStatus | None) -> int:
    statement = select(func.count()).select_from(ReviewReport)
    if status:
        statement = statement.where(ReviewReport.status == status)
    return session.exec(statement).one()
