"""创建独立压测库并运行真实 HTTP 只读负载；不触碰开发库数据。"""

import json
import os
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx
import psutil
import psycopg

from app.core.config import settings


def main() -> None:
    database_url = str(settings.DATABASE_URL).replace(
        "postgresql+psycopg://", "postgresql://", 1
    )
    with psycopg.connect(database_url, autocommit=True) as connection:
        if not connection.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", ("campustaste_loadtest",)
        ).fetchone():
            connection.execute("CREATE DATABASE campustaste_loadtest")
    environment = os.environ.copy()
    environment["DATABASE_URL"] = (
        database_url.rsplit("/", 1)[0] + "/campustaste_loadtest"
    )
    # 与开发缓存和测试缓存隔离；不执行 FLUSHDB。
    environment["REDIS_URL"] = settings.REDIS_URL.rsplit("/", 1)[0] + "/14"
    environment["LOADTEST_MANIFEST"] = str(Path("loadtests/dataset.json").resolve())
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        env=environment,
        check=True,
    )
    subprocess.run(
        [sys.executable, "scripts/seed-loadtest.py"], env=environment, check=True
    )
    output = Path("loadtests/results") / datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output.mkdir(parents=True)
    metadata = {
        "started_at": datetime.now(UTC).isoformat(),
        "platform": platform.platform(),
        "cpu": platform.processor(),
        "logical_cpus": psutil.cpu_count(),
        "available_memory_bytes": psutil.virtual_memory().available,
        "total_memory_bytes": psutil.virtual_memory().total,
        "dataset": json.loads(Path(environment["LOADTEST_MANIFEST"]).read_text()),
        "workload": "只读：详情/榜单/评价列表，权重6/3/1，等待0.1到0.5秒",
        "api_workers": 1,
        "users": [10, 30],
        "seconds_per_run": 60,
        "note": "API、Locust及依赖共享本机资源；含启动升压和缓存冷启动，非容量上限测定。",
    }
    (output / "environment.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2)
    )
    with (output / "api.jsonl").open("w") as log:
        server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8010",
                "--no-access-log",
            ],
            env=environment,
            stdout=log,
            stderr=log,
        )
        try:
            with httpx.Client(trust_env=False) as client:
                for _ in range(50):
                    if server.poll() is not None:
                        raise RuntimeError("压测 API 启动失败，检查 api.jsonl")
                    try:
                        response = client.get(
                            "http://127.0.0.1:8010/api/v1/utils/health-check/",
                            timeout=1,
                        )
                        if response.status_code == 200:
                            break
                    except httpx.HTTPError:
                        pass
                    time.sleep(0.2)
                else:
                    raise RuntimeError("压测 API 启动超时")
            for users in metadata["users"]:
                environment["LOADTEST_SUMMARY"] = str(
                    (output / f"users-{users}-summary.json").resolve()
                )
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "locust",
                        "-f",
                        "loadtests/locustfile.py",
                        "--headless",
                        "--only-summary",
                        "--host",
                        "http://127.0.0.1:8010",
                        "-u",
                        str(users),
                        "-r",
                        "5",
                        "-t",
                        "60s",
                        "--stop-timeout",
                        "5",
                        "--csv",
                        str(output / f"users-{users}"),
                        "--html",
                        str(output / f"users-{users}.html"),
                    ],
                    env=environment,
                    check=True,
                )
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()


if __name__ == "__main__":
    main()
