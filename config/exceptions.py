"""Shared exception hierarchy for Karuna AI OS."""

from collections.abc import Mapping
from typing import Any


class ApplicationError(Exception):
    """Base exception for expected application-level failures."""

    def __init__(
        self,
        message: str,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = dict(details or {})

    def __str__(self) -> str:
        if not self.details:
            return self.message
        return f"{self.message} | details={self.details}"


class ConfigurationError(ApplicationError):
    """Raised when application configuration is missing or invalid."""


class ProviderError(ApplicationError):
    """Raised by provider-facing infrastructure."""


class StorageError(ApplicationError):
    """Raised by storage-facing infrastructure."""


class ValidationError(ApplicationError):
    """Raised when input validation fails outside framework-specific layers."""
