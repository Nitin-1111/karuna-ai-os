"""Low-level filesystem operations for local document storage."""

import json
import shutil
from json import JSONDecodeError
from pathlib import Path

from pydantic import ValidationError as PydanticValidationError

from config.exceptions import StorageError
from config.filesystem import ensure_directory
from config.paths import normalize_path
from memory.metadata import DocumentMetadata
from memory.validation import validate_document_id, validate_storage_path


class LocalDocumentStorage:
    """Filesystem storage backend for document bytes and metadata JSON."""

    metadata_filename = "metadata.json"

    def __init__(self, root_path: str | Path) -> None:
        self.root_path = ensure_directory(root_path)

    def document_directory(self, document_id: str) -> Path:
        """Return the directory path for a document ID."""

        validated_id = validate_document_id(document_id)
        return validate_storage_path(self.root_path / validated_id, self.root_path)

    def metadata_path(self, document_id: str) -> Path:
        """Return the metadata JSON path for a document ID."""

        return validate_storage_path(
            self.document_directory(document_id) / self.metadata_filename,
            self.root_path,
        )

    def content_path(self, document_id: str, stored_filename: str) -> Path:
        """Return the content file path for a stored document."""

        return validate_storage_path(
            self.document_directory(document_id) / stored_filename,
            self.root_path,
        )

    def create_document_directory(self, document_id: str) -> Path:
        """Create a new document directory with overwrite protection."""

        directory = self.document_directory(document_id)
        if directory.exists():
            raise StorageError(
                "Document ID already exists.",
                details={"document_id": document_id},
            )

        directory.mkdir(parents=False, exist_ok=False)
        return directory

    def write_content(self, path: str | Path, content: bytes) -> None:
        """Write document content using exclusive creation."""

        content_path = validate_storage_path(path, self.root_path)
        try:
            with content_path.open("xb") as file:
                file.write(content)
        except FileExistsError as exc:
            raise StorageError(
                "Document content already exists.",
                details={"path": str(content_path)},
            ) from exc
        except OSError as exc:
            raise StorageError(
                "Failed to write document content.",
                details={"path": str(content_path)},
            ) from exc

    def write_metadata(self, metadata: DocumentMetadata) -> None:
        """Persist document metadata as JSON using exclusive creation."""

        metadata_path = validate_storage_path(metadata.metadata_path, self.root_path)
        try:
            with metadata_path.open("x", encoding="utf-8") as file:
                json.dump(metadata.to_json_dict(), file, indent=2, sort_keys=True)
                file.write("\n")
        except FileExistsError as exc:
            raise StorageError(
                "Document metadata already exists.",
                details={"path": str(metadata_path)},
            ) from exc
        except OSError as exc:
            raise StorageError(
                "Failed to write document metadata.",
                details={"path": str(metadata_path)},
            ) from exc

    def read_content(self, path: str | Path) -> bytes:
        """Read document content from a validated storage path."""

        content_path = validate_storage_path(path, self.root_path)
        try:
            return content_path.read_bytes()
        except OSError as exc:
            raise StorageError(
                "Failed to read document content.",
                details={"path": str(content_path)},
            ) from exc

    def read_metadata(self, document_id: str) -> DocumentMetadata:
        """Read and validate persisted metadata JSON."""

        metadata_path = self.metadata_path(document_id)
        try:
            metadata_data = json.loads(metadata_path.read_text(encoding="utf-8"))
            return DocumentMetadata.model_validate(metadata_data)
        except FileNotFoundError as exc:
            raise StorageError(
                "Document metadata was not found.",
                details={"document_id": document_id},
            ) from exc
        except JSONDecodeError as exc:
            raise StorageError(
                "Document metadata is invalid JSON.",
                details={"document_id": document_id},
            ) from exc
        except PydanticValidationError as exc:
            raise StorageError(
                "Document metadata failed validation.",
                details={"document_id": document_id, "errors": exc.errors()},
            ) from exc
        except OSError as exc:
            raise StorageError(
                "Failed to read document metadata.",
                details={"document_id": document_id},
            ) from exc

    def list_metadata(self) -> list[DocumentMetadata]:
        """Return all valid document metadata records."""

        metadata_records: list[DocumentMetadata] = []
        for child_path in sorted(self.root_path.iterdir()):
            if not child_path.is_dir():
                continue
            try:
                metadata_records.append(self.read_metadata(child_path.name))
            except StorageError as exc:
                raise StorageError(
                    "Failed to list document metadata.",
                    details={"directory": str(child_path)},
                ) from exc
        return sorted(metadata_records, key=lambda metadata: metadata.created_at)

    def delete_document_directory(self, document_id: str) -> None:
        """Delete a document directory after validating its path."""

        directory = self.document_directory(document_id)
        if not directory.exists():
            raise StorageError(
                "Document was not found.",
                details={"document_id": document_id},
            )
        if not directory.is_dir():
            raise StorageError(
                "Document path is not a directory.",
                details={"document_id": document_id, "path": str(directory)},
            )

        try:
            shutil.rmtree(directory)
        except OSError as exc:
            raise StorageError(
                "Failed to delete document.",
                details={"document_id": document_id},
            ) from exc

    def cleanup_document_directory(self, document_id: str) -> None:
        """Best-effort cleanup for partially created document directories."""

        directory = normalize_path(self.root_path / validate_document_id(document_id))
        if not directory.exists():
            return
        if not validate_storage_path(directory, self.root_path).is_dir():
            return
        shutil.rmtree(directory, ignore_errors=True)
