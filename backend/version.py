"""Application version metadata."""

from importlib.metadata import PackageNotFoundError, version

PACKAGE_NAME = "karuna-ai-os"
APPLICATION_VERSION = "0.1.0"


def get_application_version() -> str:
    """Return the installed package version."""

    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return APPLICATION_VERSION
