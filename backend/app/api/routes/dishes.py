import uuid
from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep, get_current_reviewer
from app.models import (
    Dish,
    DishCreate,
    DishesPublic,
    DishPublic,
    DishReview,
    DishStatus,
    DishUpdate,
    User,
    UserRole,
)
from app.services.cache import get_or_build_json, invalidate_dish_and_rankings
from app.services.dishes import create_dish, review_dish, validate_dish_references

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.get("/", response_model=DishesPublic)
def read_published_dishes(
    session: SessionDep,
    stall_id: uuid.UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    statement = select(Dish).where(Dish.status == DishStatus.PUBLISHED)
    count_statement = (
        select(func.count())
        .select_from(Dish)
        .where(Dish.status == DishStatus.PUBLISHED)
    )
    if stall_id:
        statement = statement.where(Dish.stall_id == stall_id)
        count_statement = count_statement.where(Dish.stall_id == stall_id)
    count = session.exec(count_statement).one()
    dishes = session.exec(
        statement.order_by(col(Dish.created_at).desc()).offset(skip).limit(limit)
    ).all()
    return DishesPublic(data=dishes, count=count)


@router.get("/mine", response_model=DishesPublic)
def read_my_dishes(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    condition = Dish.submitted_by_id == current_user.id
    count = session.exec(select(func.count()).select_from(Dish).where(condition)).one()
    dishes = session.exec(
        select(Dish)
        .where(condition)
        .order_by(col(Dish.created_at).desc())
        .offset(skip)
        .limit(limit)
    ).all()
    return DishesPublic(data=dishes, count=count)


@router.get("/pending", response_model=DishesPublic)
def read_pending_dishes(
    session: SessionDep,
    reviewer: Annotated[User, Depends(get_current_reviewer)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    del reviewer
    condition = Dish.status == DishStatus.PENDING
    count = session.exec(select(func.count()).select_from(Dish).where(condition)).one()
    dishes = session.exec(
        select(Dish)
        .where(condition)
        .order_by(col(Dish.created_at))
        .offset(skip)
        .limit(limit)
    ).all()
    return DishesPublic(data=dishes, count=count)


@router.get("/{dish_id}", response_model=DishPublic)
def read_dish(session: SessionDep, dish_id: uuid.UUID) -> Any:
    def build() -> str | None:
        dish = session.get(Dish, dish_id)
        if not dish or dish.status != DishStatus.PUBLISHED:
            return None
        return DishPublic.model_validate(dish).model_dump_json()

    cached = get_or_build_json(key=f"cache:dish:{dish_id}", builder=build)
    if cached is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return DishPublic.model_validate_json(cached)


@router.post("/", response_model=DishPublic)
def submit_dish(
    session: SessionDep, current_user: CurrentUser, dish_in: DishCreate
) -> Any:
    return create_dish(session=session, dish_in=dish_in, current_user=current_user)


@router.patch("/{dish_id}", response_model=DishPublic)
def update_dish(
    session: SessionDep,
    current_user: CurrentUser,
    dish_id: uuid.UUID,
    dish_in: DishUpdate,
) -> Any:
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    is_admin = current_user.is_superuser or current_user.role == UserRole.ADMIN
    if not is_admin and dish.submitted_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not is_admin and dish.status != DishStatus.PENDING:
        raise HTTPException(status_code=409, detail="Only pending dishes can be edited")
    updates = dish_in.model_dump(exclude_unset=True)
    validate_dish_references(
        session=session,
        stall_id=updates.get("stall_id", dish.stall_id),
        category_id=updates.get("category_id", dish.category_id),
    )
    dish.sqlmodel_update(updates)
    dish.updated_at = datetime.now(UTC)
    session.add(dish)
    session.commit()
    session.refresh(dish)
    invalidate_dish_and_rankings(session, dish.id)
    return dish


@router.post("/{dish_id}/review", response_model=DishPublic)
def review_pending_dish(
    session: SessionDep,
    dish_id: uuid.UUID,
    review: DishReview,
    reviewer: Annotated[User, Depends(get_current_reviewer)],
) -> Any:
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return review_dish(session=session, dish=dish, review=review, reviewer=reviewer)
