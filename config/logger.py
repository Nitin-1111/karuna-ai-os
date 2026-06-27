"""Structured console logging for Karuna AI OS."""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from config.constants import APP_LOGGER_NAME, DEFAULT_LOG_LEVEL, LogLevel
from config.exceptions import ConfigurationError

_CONSOLE_HANDLER_MARKER = "_karuna_ai_os_console_handler"


class StructuredJsonFormatter(logging.Formatter):
    """Format log records as JSON for structured console logging."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info is not None:
            payload["exception"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            payload["stack"] = self.formatStack(record.stack_info)

        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(
    *,
    log_level: str | LogLevel = DEFAULT_LOG_LEVEL,
    logger_name: str = APP_LOGGER_NAME,
) -> logging.Logger:
    """Configure and return the application logger."""

    resolved_level = _resolve_log_level(log_level)
    application_logger = logging.getLogger(logger_name)
    application_logger.setLevel(resolved_level)
    application_logger.propagate = False

    console_handler = _get_or_create_console_handler(application_logger)
    console_handler.setLevel(resolved_level)
    console_handler.setFormatter(StructuredJsonFormatter())

    return application_logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger scoped under the application logger name."""

    if name is None:
        return logging.getLogger(APP_LOGGER_NAME)

    if name == APP_LOGGER_NAME or name.startswith(f"{APP_LOGGER_NAME}."):
        return logging.getLogger(name)

    return logging.getLogger(f"{APP_LOGGER_NAME}.{name}")


def _get_or_create_console_handler(
    application_logger: logging.Logger,
) -> logging.StreamHandler[Any]:
    """Return the reusable console handler for the application logger."""

    for handler in application_logger.handlers:
        if getattr(handler, _CONSOLE_HANDLER_MARKER, False):
            if isinstance(handler, logging.StreamHandler):
                return handler

    console_handler: logging.StreamHandler[Any] = logging.StreamHandler()
    setattr(console_handler, _CONSOLE_HANDLER_MARKER, True)
    application_logger.addHandler(console_handler)
    return console_handler


def _resolve_log_level(log_level: str | LogLevel) -> int:
    """Convert a configured log level into the logging module's integer level."""

    if isinstance(log_level, LogLevel):
        normalized_level = log_level.value
    else:
        normalized_level = log_level.strip().upper()

    try:
        return logging._nameToLevel[LogLevel(normalized_level).value]
    except (KeyError, ValueError) as exc:
        raise ConfigurationError(
            "Unsupported log level.",
            details={"log_level": str(log_level)},
        ) from exc


logger = get_logger()
