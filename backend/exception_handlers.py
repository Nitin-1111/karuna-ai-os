"""Centralized FastAPI exception handlers."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config.exceptions import (
    ApplicationError,
    ConfigurationError,
    ProviderError,
    StorageError,
    ValidationError,
)
from config.logger import get_logger


def _request_id(request: Request) -> str | None:
    """Return the request ID attached by middleware when available."""

    request_id = getattr(request.state, "request_id", None)
    if isinstance(request_id, str):
        return request_id
    return request.headers.get("X-Request-ID")


def _error_response(
    *,
    request: Request,
    status_code: int,
    error_type: str,
    message: str,
) -> JSONResponse:
    """Create a consistent JSON error response."""

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "type": error_type,
                "message": message,
                "request_id": _request_id(request),
            }
        },
    )


async def application_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle shared application exceptions."""

    if not isinstance(exc, ApplicationError):
        return await unhandled_exception_handler(request, exc)

    logger = get_logger("backend.exception_handlers")
    status_code = _status_code_for_application_error(exc)
    logger.warning(
        "Handled application error.",
        extra={
            "error_type": type(exc).__name__,
            "path": request.url.path,
            "status_code": status_code,
        },
    )
    return _error_response(
        request=request,
        status_code=status_code,
        error_type=type(exc).__name__,
        message=exc.message,
    )


async def request_validation_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle FastAPI request validation errors."""

    if not isinstance(exc, RequestValidationError):
        return await unhandled_exception_handler(request, exc)

    get_logger("backend.exception_handlers").warning(
        "Handled request validation error.",
        extra={
            "path": request.url.path,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        },
    )
    return _error_response(
        request=request,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_type="RequestValidationError",
        message="Request validation failed.",
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle unexpected exceptions without exposing stack traces."""

    get_logger("backend.exception_handlers").exception(
        "Unhandled application exception.",
        extra={"path": request.url.path, "error_type": type(exc).__name__},
    )
    return _error_response(
        request=request,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_type="InternalServerError",
        message="Internal server error.",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register global FastAPI exception handlers."""

    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)


def _status_code_for_application_error(exc: ApplicationError) -> int:
    """Map shared application errors to HTTP status codes."""

    if isinstance(exc, (ValidationError, ConfigurationError)):
        return status.HTTP_400_BAD_REQUEST
    if isinstance(exc, (ProviderError, StorageError)):
        return status.HTTP_503_SERVICE_UNAVAILABLE
    return status.HTTP_500_INTERNAL_SERVER_ERROR
