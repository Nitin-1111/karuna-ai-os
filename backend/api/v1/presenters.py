"""Response presentation helpers for version 1 REST API endpoints."""

import base64

from agents.base import BaseAgent
from backend.api.v1.schemas import (
    AgentSummaryResponse,
    DocumentMetadataResponse,
    DocumentReadResponse,
    WorkflowRunResponse,
)
from memory.document import Document
from memory.metadata import DocumentMetadata
from workflows.state import WorkflowState


def present_agent(agent: BaseAgent) -> AgentSummaryResponse:
    """Convert an agent instance into public response metadata."""

    return AgentSummaryResponse(
        agent_type=agent.agent_type.value,
        display_name=agent.display_name,
        healthy=agent.health_check(),
    )


def present_document_metadata(
    metadata: DocumentMetadata,
) -> DocumentMetadataResponse:
    """Convert document metadata into an API response model."""

    return DocumentMetadataResponse(
        document_id=metadata.document_id,
        original_filename=metadata.original_filename,
        stored_filename=metadata.stored_filename,
        created_at=metadata.created_at.isoformat(),
        modified_at=metadata.modified_at.isoformat(),
        content_type=metadata.content_type,
        file_size=metadata.file_size,
        storage_path=str(metadata.storage_path),
        metadata_path=str(metadata.metadata_path),
        metadata=dict(metadata.metadata),
    )


def present_document(document: Document) -> DocumentReadResponse:
    """Convert a stored document into an API response model."""

    return DocumentReadResponse(
        document=present_document_metadata(document.metadata),
        content_base64=base64.b64encode(document.content).decode("ascii"),
    )


def present_workflow_state(state: WorkflowState) -> WorkflowRunResponse:
    """Convert workflow state into an API response model."""

    return WorkflowRunResponse(
        original_request=state["original_request"],
        workflow_metadata=dict(state["workflow_metadata"]),
        current_agent=state["current_agent"],
        intermediate_outputs=dict(state["intermediate_outputs"]),
        final_output=state["final_output"],
        execution_status=state["execution_status"],
        errors=list(state["errors"]),
    )
