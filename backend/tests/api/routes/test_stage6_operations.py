import json
import logging
from io import StringIO

import pytest
from fastapi.testclient import TestClient

from app.core.observability import JsonFormatter
from app.main import app
from app.services import health


def test_request_logging_omits_credentials_and_query() -> None:
    output = StringIO()
    handler = logging.StreamHandler(output)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger("app.requests")
    logger.addHandler(handler)
    try:
        response = TestClient(app).get(
            "/api/v1/utils/health-check/?token=secret-query",
            headers={"X-Request-ID": "demo-42", "Authorization": "Bearer secret-token"},
        )
        assert response.headers["x-request-id"] == "demo-42"
        event = json.loads(output.getvalue())
        assert event["request_id"] == "demo-42"
        assert event["status_code"] == 200
        assert event["duration_ms"] >= 0
        assert "secret" not in output.getvalue()
    finally:
        logger.removeHandler(handler)
    response = TestClient(app).get(
        "/api/v1/utils/health-check/", headers={"X-Request-ID": "bad id"}
    )
    assert len(response.headers["x-request-id"]) == 32


def test_readiness_failure_does_not_break_liveness(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in ("check_postgresql", "check_redis", "check_rabbitmq", "check_minio"):
        monkeypatch.setattr(health, name, lambda: None)
    client = TestClient(app)
    assert client.get("/api/v1/utils/ready/").status_code == 200

    def unavailable() -> None:
        raise ConnectionError("password=must-not-leak")

    monkeypatch.setattr(health, "check_redis", unavailable)
    response = client.get("/api/v1/utils/ready/")
    assert response.status_code == 503
    assert response.json()["checks"]["redis"] == "unavailable"
    assert "must-not-leak" not in response.text
    assert client.get("/api/v1/utils/health-check/").status_code == 200
