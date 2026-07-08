"""Shared pytest fixtures for Karuna AI OS tests."""

from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from config.settings import Settings, clear_settings_cache, load_settings


@pytest.fixture(autouse=True)
def isolated_settings_cache() -> Generator[None]:
    """Clear cached settings before and after each test."""

    clear_settings_cache()
    yield
    clear_settings_cache()


@pytest.fixture
def settings_environ(tmp_path: Path) -> dict[str, str]:
    """Return deterministic environment values for tests."""

    return {
        "APP_NAME": "Karuna AI OS Test",
        "APP_ENV": "test",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "LOG_LEVEL": "INFO",
        "LLM_PROVIDER": "groq",
        "LLM_API_KEY": "test-api-key",
        "LLM_MODEL": "test-model",
        "DOCUMENT_STORAGE_PATH": str(tmp_path / "documents"),
        "MEMORY_STORAGE_PATH": str(tmp_path / "memory"),
    }


@pytest.fixture
def test_settings(settings_environ: dict[str, str]) -> Settings:
    """Load settings from deterministic test environment values."""

    return load_settings(environ=settings_environ)


@pytest.fixture
def api_client(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> Generator[TestClient]:
    """Create a FastAPI TestClient with isolated storage paths."""

    monkeypatch.setenv("APP_NAME", "Karuna AI OS Test")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    monkeypatch.setenv("HOST", "127.0.0.1")
    monkeypatch.setenv("PORT", "8000")
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("DOCUMENT_STORAGE_PATH", str(tmp_path / "api-documents"))
    monkeypatch.setenv("MEMORY_STORAGE_PATH", str(tmp_path / "api-memory"))
    clear_settings_cache()

    from backend.app import create_app

    with TestClient(create_app()) as client:
        yield client

    clear_settings_cache()


@pytest.fixture
def document_payload() -> dict[str, Any]:
    """Return a valid API document creation payload."""

    return {
        "filename": "phase9.txt",
        "content_base64": "UGhhc2UgOSBkb2N1bWVudA==",
        "content_type": "text/plain",
        "metadata": {"source": "pytest"},
    }
