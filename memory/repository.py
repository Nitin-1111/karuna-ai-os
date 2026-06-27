"""Repository API for local filesystem document persistence."""

from collections.abc import Mapping
from typing import Any

from config.exceptions import StorageError
from config.logger import get_logger
from config.settings import Settings, get_settings
from memory.document import Document
from memory.metadata import DocumentMetadata
from memory.storage import LocalDocumentStorage
from memory.validation import (
    generate_document_id,
    generate_timestamp,
    sanitize_filename,
    validate_content,
    validate_content_type,
    validate_document_id,
    validate_metadata,
)


class LocalDocumentRepository:
    """Filesystem-backed repository for storing local documents."""

    def __init__(
        self,
        settings: Settings | None = None,
        storage: LocalDocumentStorage | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._storage = storage or LocalDocumentStorage(
            self._settings.paths.document_storage_path
        )
        self._logger = get_logger(__name__)

    def create_document(
        self,
        *,
        filename: str,
        content: bytes,
        content_type: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        document_id: str | None = None,
    ) -> DocumentMetadata:
        """Persist a document and return its metadata."""

        validated_content = validate_content(content)
        original_filename = filename.strip()
        stored_filename = sanitize_filename(filename)
        resolved_content_type = validate_content_type(content_type)
        resolved_metadata = validate_metadata(metadata)
        resolved_document_id = (
            validate_document_id(document_id)
            if document_id is not None
            else generate_document_id()
        )

        self._logger.info(
            "Creating local document.",
            extra={
                "document_id": resolved_document_id,
                "original_filename": original_filename,
            },
        )

        created_at = generate_timestamp()
        self._storage.create_document_directory(resolved_document_id)
        storage_path = self._storage.content_path(resolved_document_id, stored_filename)
        metadata_path = self._storage.metadata_path(resolved_document_id)

        document_metadata = DocumentMetadata(
            document_id=resolved_document_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            created_at=created_at,
            modified_at=created_at,
            content_type=resolved_content_type,
            file_size=len(validated_content),
            storage_path=storage_path,
            metadata_path=metadata_path,
            metadata=resolved_metadata,
        )

        try:
            self._storage.write_content(storage_path, validated_content)
            self._storage.write_metadata(document_metadata)
        except StorageError:
            self._storage.cleanup_document_directory(resolved_document_id)
            raise

        self._logger.info(
            "Local document created.",
            extra={"document_id": resolved_document_id, "path": str(storage_path)},
        )
        return document_metadata

    def read_document(self, document_id: str) -> Document:
        """Read a stored document and its metadata."""

        resolved_document_id = validate_document_id(document_id)
        self._logger.info(
            "Reading local document.",
            extra={"document_id": resolved_document_id},
        )

        metadata = self._storage.read_metadata(resolved_document_id)
        content = self._storage.read_content(metadata.storage_path)
        return Document(metadata=metadata, content=content)

    def list_documents(self) -> list[DocumentMetadata]:
        """List all persisted document metadata records."""

        self._logger.info("Listing local documents.")
        return self._storage.list_metadata()

    def delete_document(self, document_id: str) -> None:
        """Delete a stored document and its metadata."""

        resolved_document_id = validate_document_id(document_id)
        self._logger.info(
            "Deleting local document.",
            extra={"document_id": resolved_document_id},
        )
        self._storage.delete_document_directory(resolved_document_id)
        self._logger.info(
            "Local document deleted.",
            extra={"document_id": resolved_document_id},
        )


def create_document_repository(
    settings: Settings | None = None,
) -> LocalDocumentRepository:
    """Create a local document repository using configured storage paths."""

    return LocalDocumentRepository(settings=settings)
