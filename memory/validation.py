"""Validation helpers for local document storage."""

import json
import re
import uuid
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path, PurePath
from typing import Any

from config.exceptions import StorageError, ValidationError
from config.paths import is_path_within_directory, normalize_path

_DOCUMENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{8,128}$")
_WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}
_INVALID_FILENAME_CHARACTERS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_SAFE_FILENAME_CHARACTERS = re.compile(r"[^A-Za-z0-9._ -]")

JsonValue = (
    str
    | int
    | float
    | bool
    | None
    | list["JsonValue"]
    | dict[str, "JsonValue"]
)
JsonObject = dict[str, Any]


def generate_document_id() -> str:
    """Generate a unique document identifier."""

    return uuid.uuid4().hex


def generate_timestamp() -> datetime:
    """Generate a timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def validate_document_id(document_id: str) -> str:
    """Validate a document identifier for filesystem-safe storage."""

    normalized_id = document_id.strip()
    if not normalized_id:
        raise ValidationError("Document ID must not be empty.")
    if not _DOCUMENT_ID_PATTERN.fullmatch(normalized_id):
        raise ValidationError(
            "Document ID contains unsupported characters.",
            details={"document_id": document_id},
        )
    return normalized_id


def sanitize_filename(filename: str) -> str:
    """Validate and sanitize an original filename for local storage."""

    original_filename = filename.strip()
    if not original_filename:
        raise ValidationError("Filename must not be empty.")

    if PurePath(original_filename).name != original_filename:
        raise ValidationError(
            "Filename must not include path components.",
            details={"filename": filename},
        )

    if original_filename in {".", ".."} or ".." in PurePath(original_filename).parts:
        raise ValidationError(
            "Filename must not include path traversal.",
            details={"filename": filename},
        )

    if _INVALID_FILENAME_CHARACTERS.search(original_filename):
        raise ValidationError(
            "Filename contains invalid characters.",
            details={"filename": filename},
        )

    sanitized_name = _SAFE_FILENAME_CHARACTERS.sub("_", original_filename)
    sanitized_name = re.sub(r"\s+", " ", sanitized_name).strip(" .")
    if not sanitized_name:
        raise ValidationError("Filename is invalid after sanitization.")

    stem = sanitized_name.split(".", maxsplit=1)[0].upper()
    if stem in _WINDOWS_RESERVED_NAMES:
        raise ValidationError(
            "Filename uses a reserved system name.",
            details={"filename": filename},
        )

    return sanitized_name


def validate_content(content: bytes) -> bytes:
    """Validate document content before persistence."""

    if not content:
        raise ValidationError("Document content must not be empty.")
    return content


def validate_content_type(content_type: str | None) -> str:
    """Validate and normalize a content type value."""

    if content_type is None:
        return "application/octet-stream"

    normalized_content_type = content_type.strip()
    if not normalized_content_type:
        return "application/octet-stream"

    if any(character.isspace() for character in normalized_content_type):
        raise ValidationError(
            "Content type must not contain whitespace.",
            details={"content_type": content_type},
        )
    return normalized_content_type


def validate_storage_path(path: str | Path, root_path: str | Path) -> Path:
    """Validate that a path stays within the configured storage root."""

    normalized_path = normalize_path(path)
    normalized_root = normalize_path(root_path)
    if not is_path_within_directory(normalized_path, normalized_root):
        raise StorageError(
            "Storage path escapes configured root.",
            details={"path": str(normalized_path), "root_path": str(normalized_root)},
        )
    return normalized_path


def validate_metadata(metadata: Mapping[str, Any] | None) -> JsonObject:
    """Validate user metadata as a JSON object."""

    if metadata is None:
        return {}

    metadata_dict = dict(metadata)
    if not all(isinstance(key, str) and key.strip() for key in metadata_dict):
        raise ValidationError("Metadata keys must be non-empty strings.")

    try:
        json.dumps(metadata_dict)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Metadata must be JSON serializable.") from exc

    return _coerce_json_object(metadata_dict)


def _coerce_json_object(metadata: Mapping[str, Any]) -> JsonObject:
    """Return metadata after recursive JSON value validation."""

    return {key: _coerce_json_value(value) for key, value in metadata.items()}


def _coerce_json_value(value: Any) -> JsonValue:
    """Validate and return a JSON-compatible metadata value."""

    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, list):
        return [_coerce_json_value(item) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValidationError("Nested metadata keys must be strings.")
        return {key: _coerce_json_value(item) for key, item in value.items()}

    raise ValidationError(
        "Metadata contains a non-JSON-compatible value.",
        details={"value_type": type(value).__name__},
    )
