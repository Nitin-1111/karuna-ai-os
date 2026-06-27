"""Environment loading helpers for Karuna AI OS."""

import os
from collections.abc import Mapping
from pathlib import Path

from dotenv import load_dotenv

from config.constants import ENV_FILE_NAME
from config.exceptions import ConfigurationError
from config.paths import PROJECT_ROOT, resolve_project_path


def get_default_env_file_path() -> Path:
    """Return the default project-level environment file path."""

    return PROJECT_ROOT / ENV_FILE_NAME


def load_environment_file(env_file: str | Path | None = None) -> Path | None:
    """Load environment variables from a dotenv file when it exists.

    Existing operating system environment variables take precedence over values
    loaded from the dotenv file.
    """

    env_path = (
        resolve_project_path(env_file)
        if env_file is not None
        else get_default_env_file_path()
    )

    if not env_path.exists():
        return None

    if not env_path.is_file():
        raise ConfigurationError(
            "Environment path exists but is not a file.",
            details={"path": str(env_path)},
        )

    load_dotenv(dotenv_path=env_path, override=False)
    return env_path


def get_environment_value(
    name: str,
    *,
    default: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> str | None:
    """Read an environment value from a mapping or the process environment."""

    source = environ if environ is not None else os.environ
    value = source.get(name, default)
    if value is None:
        return None

    stripped_value = value.strip()
    return stripped_value if stripped_value else None


def require_environment_value(
    name: str,
    *,
    environ: Mapping[str, str] | None = None,
) -> str:
    """Read a required environment value or raise a configuration error."""

    value = get_environment_value(name, environ=environ)
    if value is None:
        raise ConfigurationError(
            "Required environment value is missing.",
            details={"name": name},
        )
    return value
