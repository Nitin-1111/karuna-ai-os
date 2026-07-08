"""Pydantic models for version 1 REST API requests and responses."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentSummaryResponse(BaseModel):
    """Public metadata for a supported agent."""

    agent_type: str = Field(description="Stable agent type identifier.")
    display_name: str = Field(description="Human-readable agent name.")
    healthy: bool = Field(description="Framework-level agent health status.")


class AgentListResponse(BaseModel):
    """Response containing all registered agents."""

    agents: list[AgentSummaryResponse]


class AgentRunRequest(BaseModel):
    """Request body for running a single agent."""

    input: str = Field(min_length=1, description="Input text for the agent.")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "input": "Create a phase-safe nutrition planning outline.",
                }
            ]
        }
    )


class AgentRunResponse(BaseModel):
    """Response returned after running a single agent."""

    agent_type: str
    output: str


class WorkflowRunRequest(BaseModel):
    """Request body for running the sequential workflow."""

    request: str = Field(min_length=1, description="Original workflow request.")
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Optional workflow metadata.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "request": "Prepare a reviewed wellness content outline.",
                    "metadata": {"source": "manual-smoke-test"},
                }
            ]
        }
    )


class WorkflowRunResponse(BaseModel):
    """Public workflow execution state."""

    original_request: str
    workflow_metadata: dict[str, str]
    current_agent: str | None
    intermediate_outputs: dict[str, str]
    final_output: str | None
    execution_status: str
    errors: list[str]


class DocumentCreateRequest(BaseModel):
    """Request body for creating a local document."""

    filename: str = Field(min_length=1, description="Original document filename.")
    content_base64: str = Field(
        min_length=1,
        description="Base64-encoded document content.",
    )
    content_type: str | None = Field(
        default=None,
        description="Optional document content type.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional JSON-compatible document metadata.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "filename": "sample.txt",
                    "content_base64": "SGVsbG8gS2FydW5h",
                    "content_type": "text/plain",
                    "metadata": {"source": "api"},
                }
            ]
        }
    )


class DocumentMetadataResponse(BaseModel):
    """Document metadata returned by the REST API."""

    document_id: str
    original_filename: str
    stored_filename: str
    created_at: str
    modified_at: str
    content_type: str
    file_size: int
    storage_path: str
    metadata_path: str
    metadata: dict[str, Any]


class DocumentCreateResponse(BaseModel):
    """Response returned after creating a document."""

    document: DocumentMetadataResponse


class DocumentListResponse(BaseModel):
    """Response containing document metadata records."""

    documents: list[DocumentMetadataResponse]


class DocumentReadResponse(BaseModel):
    """Response returned when reading a stored document."""

    document: DocumentMetadataResponse
    content_base64: str


class DocumentDeleteResponse(BaseModel):
    """Response returned after deleting a stored document."""

    document_id: str
    status: str
