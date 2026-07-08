"""Validation adapters for version 1 REST API endpoints."""

import base64
import binascii
from collections.abc import Mapping
from typing import Any

from agents.types import AgentType
from agents.validation import validate_agent_type
from config.exceptions import ValidationError
from memory.validation import (
    JsonObject,
    validate_content,
    validate_document_id,
    validate_metadata,
)
from workflows.validation import validate_workflow_request


def validate_api_agent_type(agent_type: str) -> AgentType:
    """Validate an API path agent type."""

    return validate_agent_type(agent_type)


def validate_api_document_id(document_id: str) -> str:
    """Validate an API path document ID."""

    return validate_document_id(document_id)


def validate_base64_document_content(content_base64: str) -> bytes:
    """Validate and decode base64 document content."""

    if not isinstance(content_base64, str):
        raise ValidationError("Document content must be base64 text.")

    normalized_content = content_base64.strip()
    if not normalized_content:
        raise ValidationError("Document content must not be empty.")

    try:
        decoded_content = base64.b64decode(normalized_content, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValidationError("Document content must be valid base64.") from exc

    return validate_content(decoded_content)


def validate_api_metadata(metadata: Mapping[str, Any] | None) -> JsonObject:
    """Validate API metadata as a JSON-compatible object."""

    return validate_metadata(metadata)


def validate_api_workflow_request(workflow_request: str) -> str:
    """Validate a workflow request body field."""

    return validate_workflow_request(workflow_request)


def validate_api_workflow_metadata(
    metadata: Mapping[str, str] | None,
) -> dict[str, str]:
    """Validate workflow metadata values."""

    if metadata is None:
        return {}

    validated_metadata: dict[str, str] = {}
    for key, value in metadata.items():
        normalized_key = key.strip()
        normalized_value = value.strip()
        if not normalized_key:
            raise ValidationError("Workflow metadata keys must not be empty.")
        if not normalized_value:
            raise ValidationError("Workflow metadata values must not be empty.")
        validated_metadata[normalized_key] = normalized_value

    return validated_metadata
