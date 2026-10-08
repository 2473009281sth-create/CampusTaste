import json
import os
import random
from pathlib import Path
from typing import Any

from locust import HttpUser, between, events, task
from locust.env import Environment


@events.quitting.add_listener
def save_summary(environment: Environment, **_kwargs: Any) -> None:
    total = environment.stats.total
    summary = {
        "requests": total.num_requests,
        "failures": total.num_failures,
        "error_rate": total.fail_ratio,
        "rps": total.total_rps,
        "p50_ms": total.get_response_time_percentile(0.5),
        "p95_ms": total.get_response_time_percentile(0.95),
    }
    Path(os.environ["LOADTEST_SUMMARY"]).write_text(json.dumps(summary, indent=2))


class CampusReader(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self) -> None:
        manifest = Path(os.environ["LOADTEST_MANIFEST"])
        self.dataset = json.loads(manifest.read_text())

    @task(6)
    def dish_detail(self) -> None:
        dish_id = random.choice(self.dataset["dish_ids"])
        self.client.get(f"/api/v1/dishes/{dish_id}", name="菜品详情")

    @task(3)
    def school_rankings(self) -> None:
        school_id = self.dataset["school_id"]
        self.client.get(f"/api/v1/rankings/schools/{school_id}", name="学校榜单")

    @task(1)
    def review_list(self) -> None:
        dish_id = random.choice(self.dataset["dish_ids"])
        self.client.get(f"/api/v1/dishes/{dish_id}/reviews", name="评价列表")
