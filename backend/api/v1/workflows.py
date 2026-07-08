"""Version 1 workflow REST endpoints."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from backend.api.v1.presenters import present_workflow_state
from backend.api.v1.schemas import WorkflowRunRequest, WorkflowRunResponse
from backend.api.v1.validation import (
    validate_api_workflow_metadata,
    validate_api_workflow_request,
)
from backend.dependencies import get_logger_dependency, get_sequential_workflow
from workflows.graph import SequentialAgentWorkflow

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.post(
    "/run",
    response_model=WorkflowRunResponse,
    summary="Run the sequential workflow",
    description="Run the existing LangGraph sequential agent workflow.",
)
async def run_workflow(
    request: WorkflowRunRequest,
    workflow: Annotated[SequentialAgentWorkflow, Depends(get_sequential_workflow)],
    logger: Annotated[logging.Logger, Depends(get_logger_dependency)],
) -> WorkflowRunResponse:
    """Run the supported sequential workflow."""

    validated_request = validate_api_workflow_request(request.request)
    validated_metadata = validate_api_workflow_metadata(request.metadata)
    logger.info("Workflow API execution requested.")
    state = workflow.execute(
        validated_request,
        workflow_metadata=validated_metadata,
    )
    return present_workflow_state(state)
