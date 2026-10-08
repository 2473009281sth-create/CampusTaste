from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine, init_db
from app.core.redis import get_redis
from app.main import app
from app.models import (
    Canteen,
    Category,
    Dish,
    ImageAsset,
    ImageProcessingJob,
    Item,
    ModerationAudit,
    Review,
    ReviewLike,
    ReviewReport,
    School,
    Stall,
    User,
)
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session]:
    with Session(engine) as session:
        init_db(session)
        yield session
        session.execute(delete(ImageProcessingJob))
        session.execute(delete(ImageAsset))
        session.execute(delete(ModerationAudit))
        session.execute(delete(ReviewReport))
        session.execute(delete(ReviewLike))
        session.execute(delete(Review))
        session.execute(delete(Dish))
        session.execute(delete(Stall))
        session.execute(delete(Canteen))
        session.execute(delete(Category))
        session.execute(delete(School))
        statement = delete(Item)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest.fixture(autouse=True)
def clean_redis() -> Generator[None]:
    redis = get_redis()
    redis.flushdb()
    yield
    redis.flushdb()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
