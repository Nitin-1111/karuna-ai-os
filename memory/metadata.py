"""Document metadata models for local filesystem storage."""

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

from memory.validation import JsonObject, validate_document_id


class DocumentMetadata(BaseModel):
    """Metadata persisted beside each locally stored document."""

    document_id: str = Field(min_length=8, max_length=128)
    original_filename: str = Field(min_length=1)
    stored_filename: str = Field(min_length=1)
    created_at: datetime
    modified_at: datetime
    content_type: str = Field(min_length=1)
    file_size: int = Field(ge=1)
    storage_path: Path
    metadata_path: Path
    metadata: JsonObject = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @field_validator("document_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        """Validate document IDs loaded from metadata JSON."""

        return validate_document_id(value)

    @field_validator("original_filename", "stored_filename", "content_type")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        """Normalize required text fields."""

        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("Value must not be empty.")
        return stripped_value

    def to_json_dict(self) -> dict[str, object]:
        """Return JSON-ready metadata for persistence."""

        return self.model_dump(mode="json")
