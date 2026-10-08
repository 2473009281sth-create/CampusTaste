import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, col, func, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (
    Canteen,
    CanteenCreate,
    CanteenPublic,
    CanteensPublic,
    CanteenUpdate,
    CategoriesPublic,
    Category,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
    School,
    SchoolCreate,
    SchoolPublic,
    SchoolsPublic,
    SchoolUpdate,
    Stall,
    StallCreate,
    StallPublic,
    StallsPublic,
    StallUpdate,
)

router = APIRouter(tags=["catalog"])


def commit_or_conflict(session: Session, obj: SQLModel) -> None:
    try:
        session.add(obj)
        session.commit()
        session.refresh(obj)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Resource already exists")


def get_or_404[ModelT: SQLModel](
    session: Session, model: type[ModelT], resource_id: uuid.UUID
) -> ModelT:
    obj = session.get(model, resource_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj


@router.get("/schools", response_model=SchoolsPublic)
def read_schools(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    condition = col(School.is_active).is_(True)
    count = session.exec(
        select(func.count()).select_from(School).where(condition)
    ).one()
    schools = session.exec(
        select(School)
        .where(condition)
        .order_by(col(School.name))
        .offset(skip)
        .limit(limit)
    ).all()
    return SchoolsPublic(data=schools, count=count)


@router.post(
    "/schools",
    response_model=SchoolPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def create_school(session: SessionDep, school_in: SchoolCreate) -> Any:
    school = School.model_validate(school_in)
    commit_or_conflict(session, school)
    return school


@router.patch(
    "/schools/{school_id}",
    response_model=SchoolPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def update_school(
    session: SessionDep, school_id: uuid.UUID, school_in: SchoolUpdate
) -> Any:
    school = get_or_404(session, School, school_id)
    school.sqlmodel_update(school_in.model_dump(exclude_unset=True))
    commit_or_conflict(session, school)
    return school


@router.get("/canteens", response_model=CanteensPublic)
def read_canteens(
    session: SessionDep,
    school_id: uuid.UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    statement = select(Canteen).where(col(Canteen.is_active).is_(True))
    count_statement = (
        select(func.count())
        .select_from(Canteen)
        .where(col(Canteen.is_active).is_(True))
    )
    if school_id:
        statement = statement.where(Canteen.school_id == school_id)
        count_statement = count_statement.where(Canteen.school_id == school_id)
    count = session.exec(count_statement).one()
    canteens = session.exec(
        statement.order_by(col(Canteen.name)).offset(skip).limit(limit)
    ).all()
    return CanteensPublic(data=canteens, count=count)


@router.post(
    "/canteens",
    response_model=CanteenPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def create_canteen(session: SessionDep, canteen_in: CanteenCreate) -> Any:
    school = get_or_404(session, School, canteen_in.school_id)
    if not school.is_active:
        raise HTTPException(status_code=400, detail="School is inactive")
    canteen = Canteen.model_validate(canteen_in)
    commit_or_conflict(session, canteen)
    return canteen


@router.patch(
    "/canteens/{canteen_id}",
    response_model=CanteenPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def update_canteen(
    session: SessionDep, canteen_id: uuid.UUID, canteen_in: CanteenUpdate
) -> Any:
    canteen = get_or_404(session, Canteen, canteen_id)
    canteen.sqlmodel_update(canteen_in.model_dump(exclude_unset=True))
    commit_or_conflict(session, canteen)
    return canteen


@router.get("/stalls", response_model=StallsPublic)
def read_stalls(
    session: SessionDep,
    canteen_id: uuid.UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    statement = select(Stall).where(col(Stall.is_active).is_(True))
    count_statement = (
        select(func.count()).select_from(Stall).where(col(Stall.is_active).is_(True))
    )
    if canteen_id:
        statement = statement.where(Stall.canteen_id == canteen_id)
        count_statement = count_statement.where(Stall.canteen_id == canteen_id)
    count = session.exec(count_statement).one()
    stalls = session.exec(
        statement.order_by(col(Stall.name)).offset(skip).limit(limit)
    ).all()
    return StallsPublic(data=stalls, count=count)


@router.post(
    "/stalls",
    response_model=StallPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def create_stall(session: SessionDep, stall_in: StallCreate) -> Any:
    canteen = get_or_404(session, Canteen, stall_in.canteen_id)
    if not canteen.is_active:
        raise HTTPException(status_code=400, detail="Canteen is inactive")
    stall = Stall.model_validate(stall_in)
    commit_or_conflict(session, stall)
    return stall


@router.patch(
    "/stalls/{stall_id}",
    response_model=StallPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def update_stall(
    session: SessionDep, stall_id: uuid.UUID, stall_in: StallUpdate
) -> Any:
    stall = get_or_404(session, Stall, stall_id)
    stall.sqlmodel_update(stall_in.model_dump(exclude_unset=True))
    commit_or_conflict(session, stall)
    return stall


@router.get("/categories", response_model=CategoriesPublic)
def read_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    condition = col(Category.is_active).is_(True)
    count = session.exec(
        select(func.count()).select_from(Category).where(condition)
    ).one()
    categories = session.exec(
        select(Category)
        .where(condition)
        .order_by(col(Category.name))
        .offset(skip)
        .limit(limit)
    ).all()
    return CategoriesPublic(data=categories, count=count)


@router.post(
    "/categories",
    response_model=CategoryPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def create_category(session: SessionDep, category_in: CategoryCreate) -> Any:
    category = Category.model_validate(category_in)
    commit_or_conflict(session, category)
    return category


@router.patch(
    "/categories/{category_id}",
    response_model=CategoryPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def update_category(
    session: SessionDep, category_id: uuid.UUID, category_in: CategoryUpdate
) -> Any:
    category = get_or_404(session, Category, category_id)
    category.sqlmodel_update(category_in.model_dump(exclude_unset=True))
    commit_or_conflict(session, category)
    return category
