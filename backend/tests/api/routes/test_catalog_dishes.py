from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app import crud
from app.core.config import settings
from app.models import Dish, DishStatus, User, UserCreate, UserRole, UserUpdate
from tests.utils.user import create_random_user, user_authentication_headers
from tests.utils.utils import random_email, random_lower_string


def create_catalog(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> tuple[str, str]:
    suffix = random_lower_string()
    response = client.post(
        f"{settings.API_V1_STR}/schools",
        headers=superuser_token_headers,
        json={"name": f"测试大学-{suffix}", "code": suffix[:16]},
    )
    assert response.status_code == 200
    school_id = response.json()["id"]

    response = client.post(
        f"{settings.API_V1_STR}/canteens",
        headers=superuser_token_headers,
        json={"school_id": school_id, "name": f"测试食堂-{suffix}"},
    )
    assert response.status_code == 200
    canteen_id = response.json()["id"]

    response = client.post(
        f"{settings.API_V1_STR}/stalls",
        headers=superuser_token_headers,
        json={"canteen_id": canteen_id, "name": f"测试档口-{suffix}"},
    )
    assert response.status_code == 200
    stall_id = response.json()["id"]

    response = client.post(
        f"{settings.API_V1_STR}/categories",
        headers=superuser_token_headers,
        json={"name": f"分类-{suffix}"},
    )
    assert response.status_code == 200
    return stall_id, response.json()["id"]


def create_reviewer(client: TestClient, db: Session) -> tuple[dict[str, str], str]:
    email = random_email()
    password = random_lower_string()
    user = crud.create_user(
        session=db, user_create=UserCreate(email=email, password=password)
    )
    crud.update_user(
        session=db,
        db_user=user,
        user_in=UserUpdate(role=UserRole.REVIEWER),
    )
    return (
        user_authentication_headers(client=client, email=email, password=password),
        str(user.id),
    )


def test_public_can_read_catalog_without_token(client: TestClient) -> None:
    for path in ("schools", "canteens", "stalls", "categories", "dishes/"):
        response = client.get(f"{settings.API_V1_STR}/{path}")
        assert response.status_code == 200
        assert "data" in response.json()


def test_normal_user_cannot_maintain_catalog(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/schools",
        headers=normal_user_token_headers,
        json={"name": "越权学校", "code": random_lower_string()[:16]},
    )
    assert response.status_code == 403


def test_admin_can_update_catalog_and_duplicates_conflict(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    suffix = random_lower_string()
    payload = {"name": f"唯一学校-{suffix}", "code": suffix[:16]}
    response = client.post(
        f"{settings.API_V1_STR}/schools",
        headers=superuser_token_headers,
        json=payload,
    )
    assert response.status_code == 200
    school_id = response.json()["id"]

    response = client.post(
        f"{settings.API_V1_STR}/schools",
        headers=superuser_token_headers,
        json=payload,
    )
    assert response.status_code == 409

    response = client.patch(
        f"{settings.API_V1_STR}/schools/{school_id}",
        headers=superuser_token_headers,
        json={"name": f"更新学校-{suffix}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == f"更新学校-{suffix}"

    response = client.patch(
        f"{settings.API_V1_STR}/schools/00000000-0000-0000-0000-000000000000",
        headers=superuser_token_headers,
        json={"name": "不存在"},
    )
    assert response.status_code == 404


def test_user_submit_reviewer_publish_workflow(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    normal_user_token_headers: dict[str, str],
) -> None:
    stall_id, category_id = create_catalog(client, superuser_token_headers)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/",
        headers=normal_user_token_headers,
        json={
            "stall_id": stall_id,
            "category_id": category_id,
            "name": "待审核菜品",
            "description": "普通用户提交",
            "price": "15.50",
        },
    )
    assert response.status_code == 200
    dish = response.json()
    assert dish["status"] == DishStatus.PENDING
    assert dish["reviewed_by_id"] is None

    response = client.get(f"{settings.API_V1_STR}/dishes/{dish['id']}")
    assert response.status_code == 404

    response = client.get(
        f"{settings.API_V1_STR}/dishes/pending",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403

    response = client.get(
        f"{settings.API_V1_STR}/dishes/mine",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    assert any(item["id"] == dish["id"] for item in response.json()["data"])

    reviewer_headers, reviewer_id = create_reviewer(client, db)
    response = client.get(
        f"{settings.API_V1_STR}/dishes/pending",
        headers=reviewer_headers,
    )
    assert response.status_code == 200
    assert any(item["id"] == dish["id"] for item in response.json()["data"])
    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish['id']}/review",
        headers=reviewer_headers,
        json={"status": DishStatus.PUBLISHED, "review_note": "内容合规"},
    )
    assert response.status_code == 200
    reviewed = response.json()
    assert reviewed["status"] == DishStatus.PUBLISHED
    assert reviewed["reviewed_by_id"] == reviewer_id
    assert reviewed["published_at"] is not None

    response = client.get(f"{settings.API_V1_STR}/dishes/{dish['id']}")
    assert response.status_code == 200

    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish['id']}/review",
        headers=reviewer_headers,
        json={"status": DishStatus.REJECTED, "review_note": "重复审核"},
    )
    assert response.status_code == 409


def test_rejection_requires_note(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    normal_user_token_headers: dict[str, str],
) -> None:
    stall_id, category_id = create_catalog(client, superuser_token_headers)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/",
        headers=normal_user_token_headers,
        json={
            "stall_id": stall_id,
            "category_id": category_id,
            "name": "需要驳回的菜品",
            "price": "8.00",
        },
    )
    dish_id = response.json()["id"]
    reviewer_headers, _ = create_reviewer(client, db)

    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish_id}/review",
        headers=reviewer_headers,
        json={"status": DishStatus.REJECTED},
    )
    assert response.status_code == 422
    dish = db.get(Dish, dish_id)
    assert dish
    db.refresh(dish)
    assert dish.status == DishStatus.PENDING

    response = client.post(
        f"{settings.API_V1_STR}/dishes/{dish_id}/review",
        headers=reviewer_headers,
        json={"status": DishStatus.REJECTED, "review_note": "信息不完整"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == DishStatus.REJECTED
    assert response.json()["published_at"] is None

    response = client.patch(
        f"{settings.API_V1_STR}/dishes/{dish_id}",
        headers=normal_user_token_headers,
        json={"name": "试图修改已拒绝菜品"},
    )
    assert response.status_code == 409


def test_user_cannot_edit_another_users_dish(
    client: TestClient,
    db: Session,
    superuser_token_headers: dict[str, str],
    normal_user_token_headers: dict[str, str],
) -> None:
    stall_id, category_id = create_catalog(client, superuser_token_headers)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/",
        headers=normal_user_token_headers,
        json={
            "stall_id": stall_id,
            "category_id": category_id,
            "name": "归属测试菜品",
            "price": "9.00",
        },
    )
    dish_id = response.json()["id"]
    other_user = create_random_user(db)
    other_password = random_lower_string()
    crud.update_user(
        session=db,
        db_user=other_user,
        user_in=UserUpdate(password=other_password),
    )
    other_headers = user_authentication_headers(
        client=client, email=other_user.email, password=other_password
    )

    response = client.patch(
        f"{settings.API_V1_STR}/dishes/{dish_id}",
        headers=other_headers,
        json={"name": "越权修改"},
    )
    assert response.status_code == 403


def test_admin_created_dish_is_published(
    client: TestClient, db: Session, superuser_token_headers: dict[str, str]
) -> None:
    stall_id, category_id = create_catalog(client, superuser_token_headers)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/",
        headers=superuser_token_headers,
        json={
            "stall_id": stall_id,
            "category_id": category_id,
            "name": "管理员菜品",
            "price": "18.00",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == DishStatus.PUBLISHED
    user = db.exec(select(Dish).where(Dish.id == response.json()["id"])).one()
    assert user.published_at is not None

    response = client.patch(
        f"{settings.API_V1_STR}/dishes/{user.id}",
        headers=superuser_token_headers,
        json={"name": "管理员更新菜品"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "管理员更新菜品"


def test_submit_dish_validates_references(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    normal_user_token_headers: dict[str, str],
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/dishes/",
        headers=normal_user_token_headers,
        json={
            "stall_id": "00000000-0000-0000-0000-000000000000",
            "name": "无效档口菜品",
            "price": "10.00",
        },
    )
    assert response.status_code == 400

    stall_id, _ = create_catalog(client, superuser_token_headers)
    response = client.post(
        f"{settings.API_V1_STR}/dishes/",
        headers=normal_user_token_headers,
        json={
            "stall_id": stall_id,
            "category_id": "00000000-0000-0000-0000-000000000000",
            "name": "无效分类菜品",
            "price": "10.00",
        },
    )
    assert response.status_code == 400


def test_signup_cannot_escalate_role(client: TestClient, db: Session) -> None:
    email = random_email()
    response = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json={
            "email": email,
            "password": random_lower_string(),
            "role": UserRole.ADMIN,
            "is_superuser": True,
        },
    )
    assert response.status_code == 200
    created_user = db.exec(select(User).where(User.email == email)).one()
    assert created_user.role == UserRole.USER
    assert created_user.is_superuser is False
