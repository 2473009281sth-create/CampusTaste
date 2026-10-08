"""仅允许写入独立压测库，生成确定性数据与不含密钥的清单。"""

import json
import uuid
from pathlib import Path

from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import engine, init_db
from app.models import Canteen, Dish, DishStatus, Review, School, Stall, User


def identity(label: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, f"campustaste-loadtest/{label}")


def main() -> None:
    if settings.DATABASE_URL.path != "/campustaste_loadtest":
        raise SystemExit("只允许在 campustaste_loadtest 数据库生成压测数据")
    with Session(engine) as session:
        init_db(session)
        admin = session.exec(select(User).where(User.is_superuser)).first()
        assert admin
        school_id = identity("school")
        if not session.get(School, school_id):
            session.add(School(id=school_id, name="压测大学", code="LOADTEST"))
            session.flush()
            canteen = Canteen(
                id=identity("canteen"), school_id=school_id, name="压测食堂"
            )
            session.add(canteen)
            session.flush()
            stall = Stall(id=identity("stall"), canteen_id=canteen.id, name="压测档口")
            session.add(stall)
            session.flush()
            users = [
                User(
                    id=identity(f"user-{i}"),
                    email=f"load-{i}@example.com",
                    hashed_password=admin.hashed_password,
                )
                for i in range(100)
            ]
            session.add_all(users)
            session.flush()
            for i in range(100):
                dish = Dish(
                    id=identity(f"dish-{i}"),
                    stall_id=stall.id,
                    submitted_by_id=admin.id,
                    name=f"压测菜品 {i}",
                    price="12.00",
                    status=DishStatus.PUBLISHED,
                    rating_count=100,
                    rating_sum=300,
                )
                session.add(dish)
                session.flush()
                session.add_all(
                    [
                        Review(
                            id=identity(f"review-{i}-{j}"),
                            dish_id=dish.id,
                            user_id=user.id,
                            rating=j % 5 + 1,
                            content="压测评价",
                        )
                        for j, user in enumerate(users)
                    ]
                )
            session.commit()
    manifest = {
        "school_id": str(school_id),
        "dish_ids": [str(identity(f"dish-{i}")) for i in range(100)],
        "dishes": 100,
        "users": 100,
        "reviews": 10000,
    }
    Path("loadtests/dataset.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )


if __name__ == "__main__":
    main()
