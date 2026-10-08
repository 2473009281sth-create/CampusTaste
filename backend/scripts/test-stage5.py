"""在独立测试数据库上执行阶段 5 和完整后端验收。"""

import os
import subprocess
import sys

import psycopg

from app.core.config import settings


def main() -> None:
    database_url = str(settings.DATABASE_URL).replace(
        "postgresql+psycopg://", "postgresql://", 1
    )
    with psycopg.connect(database_url, autocommit=True) as connection:
        exists = connection.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", ("campustaste_test",)
        ).fetchone()
        if not exists:
            connection.execute("CREATE DATABASE campustaste_test")
    environment = os.environ.copy()
    environment["DATABASE_URL"] = database_url.rsplit("/", 1)[0] + "/campustaste_test"
    environment["REDIS_URL"] = settings.REDIS_URL.rsplit("/", 1)[0] + "/15"
    for command in (
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "pytest",
            "tests/",
            "-q",
            "--tb=short",
        ],
        [sys.executable, "-m", "coverage", "report", "--fail-under=90"],
        [sys.executable, "-m", "alembic", "check"],
    ):
        subprocess.run(command, env=environment, check=True)


if __name__ == "__main__":
    main()
