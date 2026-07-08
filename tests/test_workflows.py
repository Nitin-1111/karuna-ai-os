"""Tests for LangGraph workflow orchestration."""

import pytest

from agents.factory import AgentFactory
from config.exceptions import ValidationError
from workflows import DEFAULT_AGENT_SEQUENCE, WorkflowBuilder
from workflows.graph import create_sequential_workflow
from workflows.validation import validate_agent_sequence


def test_workflow_executes_supported_sequence() -> None:
    """The sequential workflow should propagate state through all agents."""

    workflow = create_sequential_workflow(agent_factory=AgentFactory())

    state = workflow.execute(
        "prepare a wellness outline",
        workflow_metadata={"source": "pytest"},
    )

    assert state["execution_status"] == "completed"
    assert state["workflow_metadata"]["source"] == "pytest"
    assert state["current_agent"] == "review"
    assert state["final_output"] == state["intermediate_outputs"]["review"]
    assert list(state["intermediate_outputs"]) == [
        "research",
        "nutrition",
        "content",
        "review",
    ]


def test_workflow_builder_compiles_graph() -> None:
    """The workflow builder should compile the supported StateGraph."""

    compiled_graph = WorkflowBuilder(agent_factory=AgentFactory()).compile()

    assert compiled_graph is not None


def test_workflow_rejects_blank_request() -> None:
    """Workflow request validation should reject blank input."""

    workflow = create_sequential_workflow(agent_factory=AgentFactory())

    with pytest.raises(ValidationError):
        workflow.execute("  ")


def test_workflow_rejects_invalid_sequence() -> None:
    """The supported workflow sequence should remain locked."""

    with pytest.raises(ValidationError):
        validate_agent_sequence((DEFAULT_AGENT_SEQUENCE[0],))
