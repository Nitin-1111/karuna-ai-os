"""Application version metadata."""

from importlib.metadata import PackageNotFoundError, version

PACKAGE_NAME = "karuna-ai-os"
APPLICATION_VERSION = "1.0.0"


def get_application_version() -> str:
    """Return the release version for public application metadata."""

    try:
        installed_version = version(PACKAGE_NAME)
    except PackageNotFoundError:
        return APPLICATION_VERSION

    if installed_version != APPLICATION_VERSION:
        return APPLICATION_VERSION
    return installed_version
