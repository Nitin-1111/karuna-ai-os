"""Document model for local filesystem storage."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from memory.metadata import DocumentMetadata
from memory.validation import validate_content


class Document(BaseModel):
    """A stored document and its persisted metadata."""

    metadata: DocumentMetadata
    content: bytes = Field(min_length=1)

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @field_validator("content")
    @classmethod
    def validate_document_content(cls, value: bytes) -> bytes:
        """Validate document bytes loaded from storage."""

        return validate_content(value)
