import uuid
from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, col, select

from app.api.deps import SessionDep
from app.core.config import settings
from app.models import (
    Canteen,
    Dish,
    DishPublic,
    DishStatus,
    RankingEntry,
    RankingsPublic,
    School,
    Stall,
)
from app.services.cache import get_or_build_json, get_ranking_version

router = APIRouter(prefix="/rankings", tags=["rankings"])
SCORE_SCALE = Decimal("0.0001")


def _school_totals(session: Session, school_id: uuid.UUID) -> tuple[int, int]:
    dishes = session.exec(
        select(Dish)
        .join(Stall, col(Dish.stall_id) == col(Stall.id))
        .join(Canteen, col(Stall.canteen_id) == col(Canteen.id))
        .where(Canteen.school_id == school_id, Dish.status == DishStatus.PUBLISHED)
    ).all()
    return sum(dish.rating_sum for dish in dishes), sum(
        dish.rating_count for dish in dishes
    )


def _build_rankings(
    *, session: Session, school_id: uuid.UUID, canteen_id: uuid.UUID | None, limit: int
) -> RankingsPublic:
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    if canteen_id:
        canteen = session.get(Canteen, canteen_id)
        if not canteen or canteen.school_id != school_id:
            raise HTTPException(status_code=404, detail="Canteen not found")

    statement = (
        select(Dish)
        .join(Stall, col(Dish.stall_id) == col(Stall.id))
        .join(Canteen, col(Stall.canteen_id) == col(Canteen.id))
        .where(Canteen.school_id == school_id, Dish.status == DishStatus.PUBLISHED)
    )
    if canteen_id:
        statement = statement.where(Canteen.id == canteen_id)
    dishes = session.exec(statement).all()

    school_sum, school_count = _school_totals(session, school_id)
    scope_average = (
        Decimal(school_sum) / Decimal(school_count) if school_count else Decimal(0)
    )
    prior = settings.RANKING_PRIOR_WEIGHT
    entries: list[RankingEntry] = []
    for dish in dishes:
        average = (
            Decimal(dish.rating_sum) / Decimal(dish.rating_count)
            if dish.rating_count
            else Decimal(0)
        )
        if dish.rating_count + prior:
            weighted = (
                Decimal(dish.rating_count) * average + Decimal(prior) * scope_average
            ) / Decimal(dish.rating_count + prior)
        else:
            weighted = Decimal(0)
        entries.append(
            RankingEntry(
                dish=DishPublic.model_validate(dish),
                average_rating=average.quantize(SCORE_SCALE, rounding=ROUND_HALF_UP),
                rating_count=dish.rating_count,
                weighted_score=weighted.quantize(SCORE_SCALE, rounding=ROUND_HALF_UP),
            )
        )

    entries.sort(
        key=lambda entry: (
            -entry.weighted_score,
            -entry.rating_count,
            -entry.average_rating,
            str(entry.dish.id),
        )
    )
    return RankingsPublic(
        data=entries[:limit],
        scope_average=scope_average.quantize(SCORE_SCALE, rounding=ROUND_HALF_UP),
        prior_weight=prior,
        generated_at=datetime.now(UTC),
    )


@router.get("/schools/{school_id}", response_model=RankingsPublic)
def read_school_rankings(
    session: SessionDep,
    school_id: uuid.UUID,
    limit: int = Query(default=100, ge=1, le=500),
) -> Any:
    version = get_ranking_version(school_id)
    cached = get_or_build_json(
        key=f"cache:ranking:school:{school_id}:v{version}:limit:{limit}",
        builder=lambda: _build_rankings(
            session=session, school_id=school_id, canteen_id=None, limit=limit
        ).model_dump_json(),
    )
    assert cached is not None
    return RankingsPublic.model_validate_json(cached)


@router.get("/canteens/{canteen_id}", response_model=RankingsPublic)
def read_canteen_rankings(
    session: SessionDep,
    canteen_id: uuid.UUID,
    limit: int = Query(default=100, ge=1, le=500),
) -> Any:
    canteen = session.get(Canteen, canteen_id)
    if not canteen:
        raise HTTPException(status_code=404, detail="Canteen not found")
    version = get_ranking_version(canteen.school_id)
    cached = get_or_build_json(
        key=(f"cache:ranking:canteen:{canteen_id}:v{version}:limit:{limit}"),
        builder=lambda: _build_rankings(
            session=session,
            school_id=canteen.school_id,
            canteen_id=canteen_id,
            limit=limit,
        ).model_dump_json(),
    )
    assert cached is not None
    return RankingsPublic.model_validate_json(cached)
