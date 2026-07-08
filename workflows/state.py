"""Shared workflow state for LangGraph orchestration."""

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import NotRequired, TypedDict

from agents.types import AgentType


class WorkflowStatus(StrEnum):
    """Supported workflow execution statuses."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowState(TypedDict):
    """State carried through the sequential agent workflow."""

    original_request: str
    workflow_metadata: dict[str, str]
    current_agent: str | None
    intermediate_outputs: dict[str, str]
    final_output: str | None
    execution_status: str
    errors: list[str]
    last_output: NotRequired[str | None]


def create_initial_workflow_state(
    original_request: str,
    *,
    workflow_metadata: dict[str, str] | None = None,
) -> WorkflowState:
    """Create an initial workflow state for execution."""

    metadata = dict(workflow_metadata or {})
    metadata.setdefault("workflow_id", uuid.uuid4().hex)
    metadata.setdefault("created_at", datetime.now(UTC).isoformat())

    return WorkflowState(
        original_request=original_request,
        workflow_metadata=metadata,
        current_agent=None,
        intermediate_outputs={},
        final_output=None,
        execution_status=WorkflowStatus.PENDING.value,
        errors=[],
        last_output=None,
    )


def get_workflow_id(state: WorkflowState) -> str:
    """Return the workflow ID from state metadata."""

    return state["workflow_metadata"]["workflow_id"]


def get_next_agent_input(state: WorkflowState) -> str:
    """Return the input for the next agent in sequence."""

    last_output = state.get("last_output")
    if last_output:
        return last_output
    return state["original_request"]


def record_agent_output(
    state: WorkflowState,
    *,
    agent_type: AgentType,
    output: str,
    is_final: bool = False,
) -> WorkflowState:
    """Return workflow state updated with an agent output."""

    intermediate_outputs = dict(state["intermediate_outputs"])
    intermediate_outputs[agent_type.value] = output

    return WorkflowState(
        original_request=state["original_request"],
        workflow_metadata=dict(state["workflow_metadata"]),
        current_agent=agent_type.value,
        intermediate_outputs=intermediate_outputs,
        final_output=output if is_final else state["final_output"],
        execution_status=(
            WorkflowStatus.COMPLETED.value
            if is_final
            else WorkflowStatus.RUNNING.value
        ),
        errors=list(state["errors"]),
        last_output=output,
    )


def mark_workflow_failed(state: WorkflowState, error: str) -> WorkflowState:
    """Return workflow state marked as failed."""

    errors = list(state["errors"])
    errors.append(error)

    return WorkflowState(
        original_request=state["original_request"],
        workflow_metadata=dict(state["workflow_metadata"]),
        current_agent=state["current_agent"],
        intermediate_outputs=dict(state["intermediate_outputs"]),
        final_output=state["final_output"],
        execution_status=WorkflowStatus.FAILED.value,
        errors=errors,
        last_output=state.get("last_output"),
    )
