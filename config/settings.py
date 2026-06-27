"""Validated application settings for Karuna AI OS."""

import os
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic import ValidationError as PydanticValidationError

from config.constants import (
    DEFAULT_APP_ENV,
    DEFAULT_APP_NAME,
    DEFAULT_DOCUMENT_STORAGE_PATH,
    DEFAULT_HOST,
    DEFAULT_LLM_PROVIDER,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MEMORY_STORAGE_PATH,
    DEFAULT_PORT,
    ENV_APP_ENV,
    ENV_APP_NAME,
    ENV_DOCUMENT_STORAGE_PATH,
    ENV_HOST,
    ENV_LLM_API_KEY,
    ENV_LLM_MODEL,
    ENV_LLM_PROVIDER,
    ENV_LOG_LEVEL,
    ENV_MEMORY_STORAGE_PATH,
    ENV_PORT,
    AppEnvironment,
    LlmProvider,
    LogLevel,
)
from config.environment import get_environment_value, load_environment_file
from config.exceptions import ConfigurationError
from config.paths import resolve_project_path


class ApplicationSettings(BaseModel):
    """Validated application-level settings."""

    app_name: str = Field(default=DEFAULT_APP_NAME, min_length=1)
    app_env: AppEnvironment = DEFAULT_APP_ENV
    host: str = Field(default=DEFAULT_HOST, min_length=1)
    port: int = Field(default=DEFAULT_PORT, ge=1, le=65535)
    log_level: LogLevel = DEFAULT_LOG_LEVEL

    model_config = ConfigDict(frozen=True)

    @field_validator("app_name", "host", mode="before")
    @classmethod
    def strip_required_text(cls, value: object) -> object:
        """Normalize required string values before validation."""

        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("app_env", mode="before")
    @classmethod
    def normalize_app_environment(cls, value: object) -> object:
        """Normalize environment names before enum validation."""

        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, value: object) -> object:
        """Normalize log level names before enum validation."""

        if isinstance(value, str):
            return value.strip().upper()
        return value


class ProviderSettings(BaseModel):
    """Validated provider selection and credential settings."""

    provider: LlmProvider = DEFAULT_LLM_PROVIDER
    api_key: str | None = None
    model: str | None = None

    model_config = ConfigDict(frozen=True)

    @field_validator("provider", mode="before")
    @classmethod
    def normalize_provider(cls, value: object) -> object:
        """Normalize provider names before enum validation."""

        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("api_key", "model", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object) -> object:
        """Convert blank optional strings to None."""

        if value is None:
            return None
        if isinstance(value, str):
            stripped_value = value.strip()
            return stripped_value if stripped_value else None
        return value


class PathSettings(BaseModel):
    """Validated filesystem path settings."""

    document_storage_path: Path
    memory_storage_path: Path

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @field_validator("document_storage_path", "memory_storage_path", mode="before")
    @classmethod
    def resolve_storage_path(cls, value: object) -> Path:
        """Resolve configured storage paths relative to the project root."""

        if not isinstance(value, str | Path):
            raise ValueError("Path value must be a string or pathlib.Path.")
        return resolve_project_path(value)


class Settings(BaseModel):
    """Complete validated configuration for Karuna AI OS."""

    application: ApplicationSettings
    provider: ProviderSettings
    paths: PathSettings

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def validate_environment_requirements(self) -> Self:
        """Require production secrets without blocking local development."""

        if self.application.app_env is not AppEnvironment.PRODUCTION:
            return self

        missing_values: list[str] = []
        if self.provider.api_key is None:
            missing_values.append(ENV_LLM_API_KEY)
        if self.provider.model is None:
            missing_values.append(ENV_LLM_MODEL)

        if missing_values:
            raise ValueError(
                "Production configuration is missing required provider values: "
                + ", ".join(missing_values)
            )

        return self


def load_settings(
    *,
    env_file: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Settings:
    """Load and validate application settings.

    When ``environ`` is provided, values are read from that mapping and no dotenv
    file is loaded. This keeps tests deterministic without mutating ``os.environ``.
    """

    source: Mapping[str, str]

    if environ is None:
        load_environment_file(env_file)
        source = os.environ
    else:
        source = environ

    try:
        settings_data: dict[str, Any] = {
            "application": {
                "app_name": get_environment_value(
                    ENV_APP_NAME,
                    default=DEFAULT_APP_NAME,
                    environ=source,
                ),
                "app_env": get_environment_value(
                    ENV_APP_ENV,
                    default=DEFAULT_APP_ENV.value,
                    environ=source,
                ),
                "host": get_environment_value(
                    ENV_HOST,
                    default=DEFAULT_HOST,
                    environ=source,
                ),
                "port": get_environment_value(
                    ENV_PORT,
                    default=str(DEFAULT_PORT),
                    environ=source,
                ),
                "log_level": get_environment_value(
                    ENV_LOG_LEVEL,
                    default=DEFAULT_LOG_LEVEL.value,
                    environ=source,
                ),
            },
            "provider": {
                "provider": get_environment_value(
                    ENV_LLM_PROVIDER,
                    default=DEFAULT_LLM_PROVIDER.value,
                    environ=source,
                ),
                "api_key": get_environment_value(ENV_LLM_API_KEY, environ=source),
                "model": get_environment_value(ENV_LLM_MODEL, environ=source),
            },
            "paths": {
                "document_storage_path": get_environment_value(
                    ENV_DOCUMENT_STORAGE_PATH,
                    default=DEFAULT_DOCUMENT_STORAGE_PATH,
                    environ=source,
                ),
                "memory_storage_path": get_environment_value(
                    ENV_MEMORY_STORAGE_PATH,
                    default=DEFAULT_MEMORY_STORAGE_PATH,
                    environ=source,
                ),
            },
        }
        return Settings.model_validate(settings_data)
    except PydanticValidationError as exc:
        raise ConfigurationError(
            "Invalid application configuration.",
            details={"errors": _serialize_validation_errors(exc.errors())},
        ) from exc


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings loaded from the environment."""

    return load_settings()


def clear_settings_cache() -> None:
    """Clear cached settings so a process can reload configuration."""

    get_settings.cache_clear()


def _serialize_validation_errors(errors: list[Any]) -> list[dict[str, Any]]:
    """Convert Pydantic validation details into exception-safe data."""

    serialized_errors: list[dict[str, Any]] = []
    for error in errors:
        serialized_errors.append(
            {
                key: str(value) if isinstance(value, ValueError) else value
                for key, value in error.items()
            }
        )
    return serialized_errors
