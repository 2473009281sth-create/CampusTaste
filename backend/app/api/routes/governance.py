import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep, get_current_reviewer
from app.models import (
    ModerationAudit,
    ModerationAuditPublic,
    ModerationAuditsPublic,
    ReportStatus,
    ReviewLikePublic,
    ReviewLikeUpdate,
    ReviewPublic,
    ReviewReport,
    ReviewReportCreate,
    ReviewReportPublic,
    ReviewReportResolve,
    ReviewReportsPublic,
    ReviewVisibilityUpdate,
    User,
)
from app.services.governance import (
    create_review_report,
    process_review_report,
    report_count,
    set_review_like,
    set_review_visibility,
)

router = APIRouter(tags=["governance"])


@router.put("/reviews/{review_id}/like", response_model=ReviewLikePublic)
def update_review_like(
    session: SessionDep,
    current_user: CurrentUser,
    review_id: uuid.UUID,
    like_in: ReviewLikeUpdate,
) -> Any:
    return set_review_like(
        session=session,
        review_id=review_id,
        user=current_user,
        liked=like_in.liked,
    )


@router.post("/reviews/{review_id}/reports", response_model=ReviewReportPublic)
def report_review(
    session: SessionDep,
    current_user: CurrentUser,
    review_id: uuid.UUID,
    report_in: ReviewReportCreate,
) -> Any:
    return create_review_report(
        session=session,
        review_id=review_id,
        report_in=report_in,
        reporter=current_user,
    )


@router.get("/reports", response_model=ReviewReportsPublic)
def read_reports(
    session: SessionDep,
    reviewer: Annotated[User, Depends(get_current_reviewer)],
    status: ReportStatus | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> Any:
    del reviewer
    statement = select(ReviewReport)
    if status:
        statement = statement.where(ReviewReport.status == status)
    reports = session.exec(
        statement.order_by(col(ReviewReport.created_at), col(ReviewReport.id))
        .offset(skip)
        .limit(limit)
    ).all()
    return ReviewReportsPublic(data=reports, count=report_count(session, status))


@router.post("/reports/{report_id}/resolve", response_model=ReviewReportPublic)
def resolve_report(
    session: SessionDep,
    report_id: uuid.UUID,
    resolution: ReviewReportResolve,
    reviewer: Annotated[User, Depends(get_current_reviewer)],
) -> Any:
    return process_review_report(
        session=session,
        report_id=report_id,
        resolution=resolution,
        actor=reviewer,
    )


@router.put("/reviews/{review_id}/visibility", response_model=ReviewPublic)
def update_review_visibility(
    session: SessionDep,
    review_id: uuid.UUID,
    visibility_in: ReviewVisibilityUpdate,
    reviewer: Annotated[User, Depends(get_current_reviewer)],
) -> Any:
    return set_review_visibility(
        session=session,
        review_id=review_id,
        visibility_in=visibility_in,
        actor=reviewer,
    )


@router.get("/moderation/audits", response_model=ModerationAuditsPublic)
def read_moderation_audits(
    session: SessionDep,
    reviewer: Annotated[User, Depends(get_current_reviewer)],
    review_id: uuid.UUID | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> Any:
    del reviewer
    statement = select(ModerationAudit)
    count_statement = select(func.count()).select_from(ModerationAudit)
    if review_id:
        statement = statement.where(ModerationAudit.review_id == review_id)
        count_statement = count_statement.where(ModerationAudit.review_id == review_id)
    audits = session.exec(
        statement.order_by(col(ModerationAudit.created_at).desc())
        .offset(skip)
        .limit(limit)
    ).all()
    return ModerationAuditsPublic(
        data=[ModerationAuditPublic.model_validate(audit) for audit in audits],
        count=session.exec(count_statement).one(),
    )
