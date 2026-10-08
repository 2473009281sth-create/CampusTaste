from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import (
    Canteen,
    Category,
    Dish,
    DishStatus,
    School,
    Stall,
    User,
    UserCreate,
    UserRole,
    get_datetime_utc,
)

engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            role=UserRole.ADMIN,
        )
        user = crud.create_user(session=session, user_create=user_in)
    elif user.role != UserRole.ADMIN or not user.is_superuser:
        user.role = UserRole.ADMIN
        user.is_superuser = True
        session.add(user)
        session.commit()

    school = session.exec(select(School).where(School.code == "DEMO")).first()
    if not school:
        school = School(name="示范大学", code="DEMO")
        session.add(school)
        session.flush()

    canteen = session.exec(
        select(Canteen).where(
            Canteen.school_id == school.id, Canteen.name == "第一食堂"
        )
    ).first()
    if not canteen:
        canteen = Canteen(school_id=school.id, name="第一食堂", address="校园东区")
        session.add(canteen)
        session.flush()

    stall = session.exec(
        select(Stall).where(Stall.canteen_id == canteen.id, Stall.name == "家常菜档口")
    ).first()
    if not stall:
        stall = Stall(canteen_id=canteen.id, name="家常菜档口", floor="1F")
        session.add(stall)
        session.flush()

    category = session.exec(select(Category).where(Category.name == "主食")).first()
    if not category:
        category = Category(name="主食")
        session.add(category)
        session.flush()

    dish = session.exec(
        select(Dish).where(Dish.stall_id == stall.id, Dish.name == "番茄炒蛋盖饭")
    ).first()
    if not dish:
        now = get_datetime_utc()
        session.add(
            Dish(
                stall_id=stall.id,
                category_id=category.id,
                submitted_by_id=user.id,
                name="番茄炒蛋盖饭",
                description="阶段 1 演示菜品",
                price="12.00",
                status=DishStatus.PUBLISHED,
                reviewed_by_id=user.id,
                reviewed_at=now,
                published_at=now,
            )
        )
    session.commit()
