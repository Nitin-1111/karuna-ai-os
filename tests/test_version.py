"""Tests for application version metadata."""

from backend.version import APPLICATION_VERSION, get_application_version


def test_application_version_matches_release_metadata() -> None:
    """Application version should report the Version 1.0 release value."""

    assert APPLICATION_VERSION == "1.0.0"
    assert get_application_version() == APPLICATION_VERSION
