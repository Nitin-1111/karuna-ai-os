"""Generic path helpers for Karuna AI OS."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def normalize_path(path: str | Path) -> Path:
    """Return an expanded absolute path without requiring it to exist."""

    return Path(path).expanduser().resolve(strict=False)


def resolve_project_path(
    path: str | Path,
    *,
    base_path: str | Path = PROJECT_ROOT,
) -> Path:
    """Resolve a path relative to the project root when it is not absolute."""

    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve(strict=False)

    return (Path(base_path).expanduser() / candidate).resolve(strict=False)


def is_path_within_directory(path: str | Path, directory: str | Path) -> bool:
    """Return whether a path resolves within the given directory."""

    resolved_path = normalize_path(path)
    resolved_directory = normalize_path(directory)
    return (
        resolved_path == resolved_directory
        or resolved_directory in resolved_path.parents
    )
