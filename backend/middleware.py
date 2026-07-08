"""FastAPI middleware configuration."""

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from config.logger import get_logger

REQUEST_ID_HEADER = "X-Request-ID"


async def request_context_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Add request IDs, timing, and structured request logging."""

    logger = get_logger("backend.middleware")
    request_id = request.headers.get(REQUEST_ID_HEADER, uuid.uuid4().hex)
    request.state.request_id = request_id
    start_time = time.perf_counter()

    logger.info(
        "HTTP request started.",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 3)
        logger.exception(
            "Unhandled HTTP request exception.",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms,
            },
        )
        raise

    duration_ms = round((time.perf_counter() - start_time) * 1000, 3)
    response.headers[REQUEST_ID_HEADER] = request_id
    response.headers["X-Process-Time-MS"] = str(duration_ms)

    logger.info(
        "HTTP request completed.",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


def register_middleware(app: FastAPI) -> None:
    """Register production backend middleware."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    app.middleware("http")(request_context_middleware)
