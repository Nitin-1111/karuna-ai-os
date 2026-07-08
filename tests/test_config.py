"""Tests for configuration loading and validation."""

from pathlib import Path

import pytest

from config.constants import AppEnvironment, LlmProvider, LogLevel
from config.exceptions import ConfigurationError
from config.settings import load_settings


def test_load_settings_normalizes_values(settings_environ: dict[str, str]) -> None:
    """Settings should normalize enum values and resolve storage paths."""

    settings_environ.update(
        {
            "APP_ENV": " TEST ",
            "LOG_LEVEL": " debug ",
            "LLM_PROVIDER": " GOOGLE ",
        }
    )

    settings = load_settings(environ=settings_environ)

    assert settings.application.app_env is AppEnvironment.TEST
    assert settings.application.log_level is LogLevel.DEBUG
    assert settings.provider.provider is LlmProvider.GOOGLE
    assert settings.provider.api_key == "test-api-key"
    assert settings.provider.model == "test-model"
    assert settings.paths.document_storage_path.is_absolute()


def test_load_settings_rejects_unsupported_provider(
    settings_environ: dict[str, str],
) -> None:
    """Unsupported providers should fail configuration validation."""

    settings_environ["LLM_PROVIDER"] = "openai"

    with pytest.raises(ConfigurationError):
        load_settings(environ=settings_environ)


def test_load_settings_requires_production_provider_values(
    settings_environ: dict[str, str],
) -> None:
    """Production settings should require provider secrets and model values."""

    settings_environ["APP_ENV"] = "production"
    settings_environ.pop("LLM_API_KEY")
    settings_environ.pop("LLM_MODEL")

    with pytest.raises(ConfigurationError) as exc_info:
        load_settings(environ=settings_environ)

    assert "Production configuration is missing" in str(exc_info.value)


def test_load_settings_rejects_invalid_storage_path_type() -> None:
    """Path settings should reject non-path-compatible values."""

    with pytest.raises(ConfigurationError):
        load_settings(
            environ={
                "DOCUMENT_STORAGE_PATH": "",
                "MEMORY_STORAGE_PATH": str(Path("memory")),
            }
        )
