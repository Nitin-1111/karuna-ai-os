"""Generic filesystem helpers for Karuna AI OS infrastructure."""

import os
from pathlib import Path

from config.paths import normalize_path


def ensure_directory(path: str | Path) -> Path:
    """Create a directory when missing and return its absolute path."""

    directory = normalize_path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def path_exists(path: str | Path) -> bool:
    """Return whether a filesystem path exists."""

    return normalize_path(path).exists()


def is_readable_file(path: str | Path) -> bool:
    """Return whether a path exists, is a file, and can be read."""

    candidate = normalize_path(path)
    return candidate.is_file() and os.access(candidate, os.R_OK)


def is_writable_directory(path: str | Path) -> bool:
    """Return whether a path exists, is a directory, and can be written."""

    candidate = normalize_path(path)
    return candidate.is_dir() and os.access(candidate, os.W_OK)
