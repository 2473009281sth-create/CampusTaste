import json
import logging
import re
import time
import uuid
from contextvars import ContextVar
from datetime import UTC, datetime

from starlette.types import ASGIApp, Message, Receive, Scope, Send

request_id_context: ContextVar[str] = ContextVar("request_id", default="-")
logger = logging.getLogger("app.requests")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "request_id": request_id_context.get(),
            "message": record.getMessage(),
        }
        for key in ("method", "route", "status_code", "duration_ms"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info and record.exc_info[0]:
            # 不输出异常参数或堆栈，避免连接字符串等敏感信息进入日志。
            payload["exception_type"] = record.exc_info[0].__name__
        return json.dumps(payload, ensure_ascii=False)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    app_logger = logging.getLogger("app")
    app_logger.handlers = [handler]
    app_logger.setLevel(logging.INFO)
    app_logger.propagate = False


class RequestLogMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        supplied = (
            dict(scope["headers"])
            .get(b"x-request-id", b"")
            .decode("ascii", errors="ignore")
        )
        request_id = (
            supplied
            if re.fullmatch(r"[A-Za-z0-9_-]{1,64}", supplied)
            else uuid.uuid4().hex
        )
        token = request_id_context.set(request_id)
        started = time.perf_counter()
        status = 500

        async def send_with_id(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                headers = [
                    (key, value)
                    for key, value in message.get("headers", [])
                    if key.lower() != b"x-request-id"
                ]
                message["headers"] = headers + [(b"x-request-id", request_id.encode())]
            await send(message)

        try:
            await self.app(scope, receive, send_with_id)
        finally:
            route = scope.get("route")
            logger.info(
                "http_request",
                extra={
                    "method": scope["method"],
                    "route": getattr(route, "path", "unmatched"),
                    "status_code": status,
                    "duration_ms": round((time.perf_counter() - started) * 1000, 3),
                },
            )
            request_id_context.reset(token)
