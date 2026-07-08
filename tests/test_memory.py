"""Tests for local filesystem document storage."""

from pathlib import Path

import pytest

from config.exceptions import StorageError, ValidationError
from config.settings import load_settings
from memory.repository import LocalDocumentRepository
from memory.validation import sanitize_filename, validate_storage_path


def test_document_repository_crud(settings_environ: dict[str, str]) -> None:
    """Documents should be created, read, listed, and deleted locally."""

    settings = load_settings(environ=settings_environ)
    repository = LocalDocumentRepository(settings=settings)

    metadata = repository.create_document(
        filename="example.txt",
        content=b"hello",
        content_type="text/plain",
        metadata={"source": "test"},
        document_id="document_123",
    )

    assert metadata.document_id == "document_123"
    assert metadata.file_size == 5
    assert metadata.metadata == {"source": "test"}
    assert repository.read_document("document_123").content == b"hello"
    assert [document.document_id for document in repository.list_documents()] == [
        "document_123"
    ]

    repository.delete_document("document_123")
    assert repository.list_documents() == []


def test_document_repository_rejects_duplicate_id(
    settings_environ: dict[str, str],
) -> None:
    """Document IDs should be protected from accidental overwrite."""

    settings = load_settings(environ=settings_environ)
    repository = LocalDocumentRepository(settings=settings)
    repository.create_document(
        filename="example.txt",
        content=b"hello",
        document_id="duplicate_123",
    )

    with pytest.raises(StorageError):
        repository.create_document(
            filename="example.txt",
            content=b"hello again",
            document_id="duplicate_123",
        )


@pytest.mark.parametrize(
    "filename",
    ["", "../secret.txt", "nested/file.txt", "bad:name.txt", "CON"],
)
def test_sanitize_filename_rejects_unsafe_names(filename: str) -> None:
    """Unsafe filenames should be rejected before storage."""

    with pytest.raises(ValidationError):
        sanitize_filename(filename)


def test_validate_storage_path_rejects_path_escape(tmp_path: Path) -> None:
    """Storage paths should not escape the configured root."""

    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside.txt"

    with pytest.raises(StorageError):
        validate_storage_path(outside, root)
