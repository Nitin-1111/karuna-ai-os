"""Version 1 document REST endpoints."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.api.v1.presenters import present_document, present_document_metadata
from backend.api.v1.schemas import (
    DocumentCreateRequest,
    DocumentCreateResponse,
    DocumentDeleteResponse,
    DocumentListResponse,
    DocumentReadResponse,
)
from backend.api.v1.validation import (
    validate_api_document_id,
    validate_api_metadata,
    validate_base64_document_content,
)
from backend.dependencies import get_document_repository, get_logger_dependency
from memory.repository import LocalDocumentRepository

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post(
    "",
    response_model=DocumentCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a document",
    description="Persist a local document using the filesystem repository.",
)
async def create_document(
    request: DocumentCreateRequest,
    repository: Annotated[LocalDocumentRepository, Depends(get_document_repository)],
    logger: Annotated[logging.Logger, Depends(get_logger_dependency)],
) -> DocumentCreateResponse:
    """Create a local document."""

    content = validate_base64_document_content(request.content_base64)
    metadata = validate_api_metadata(request.metadata)
    document_metadata = repository.create_document(
        filename=request.filename,
        content=content,
        content_type=request.content_type,
        metadata=metadata,
    )
    logger.info(
        "Document API create completed.",
        extra={"document_id": document_metadata.document_id},
    )
    return DocumentCreateResponse(
        document=present_document_metadata(document_metadata),
    )


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List documents",
    description="Return metadata for all locally stored documents.",
)
async def list_documents(
    repository: Annotated[LocalDocumentRepository, Depends(get_document_repository)],
) -> DocumentListResponse:
    """List stored local documents."""

    documents = [
        present_document_metadata(metadata) for metadata in repository.list_documents()
    ]
    return DocumentListResponse(documents=documents)


@router.get(
    "/{document_id}",
    response_model=DocumentReadResponse,
    summary="Read a document",
    description="Return stored document metadata and base64-encoded content.",
)
async def read_document(
    document_id: str,
    repository: Annotated[LocalDocumentRepository, Depends(get_document_repository)],
) -> DocumentReadResponse:
    """Read a stored local document."""

    validated_document_id = validate_api_document_id(document_id)
    document = repository.read_document(validated_document_id)
    return present_document(document)


@router.delete(
    "/{document_id}",
    response_model=DocumentDeleteResponse,
    summary="Delete a document",
    description="Delete a stored local document by ID.",
)
async def delete_document(
    document_id: str,
    repository: Annotated[LocalDocumentRepository, Depends(get_document_repository)],
    logger: Annotated[logging.Logger, Depends(get_logger_dependency)],
) -> DocumentDeleteResponse:
    """Delete a stored local document."""

    validated_document_id = validate_api_document_id(document_id)
    repository.delete_document(validated_document_id)
    logger.info(
        "Document API delete completed.",
        extra={"document_id": validated_document_id},
    )
    return DocumentDeleteResponse(
        document_id=validated_document_id,
        status="deleted",
    )
