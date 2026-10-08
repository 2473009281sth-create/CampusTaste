"""New demo adapter; fixture data is synthetic and is not a database."""
import json

from fastapi import FastAPI, HTTPException

from app.services.cache import get_or_build_json
from app.services.rate_limit import enforce_rate_limit

app = FastAPI(title="CampusTaste recruitment sample")
DEMO_DISHES = {"demo-dish": {"id": "demo-dish", "name": "示例菜品"}}


def load_demo_dish(dish_id: str) -> str | None:
    dish = DEMO_DISHES.get(dish_id)
    return json.dumps(dish, ensure_ascii=False) if dish else None


@app.get("/dishes/{dish_id}")
def get_dish(dish_id: str) -> dict:
    enforce_rate_limit(key="sample:rate-limit:dishes", limit=10)
    value = get_or_build_json(
        key=f"sample:cache:dish:{dish_id}",
        builder=lambda: load_demo_dish(dish_id),
    )
    if value is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return json.loads(value)
