"""Validation helpers for workflow orchestration."""

from collections.abc import Sequence

from agents.factory import AgentFactory
from agents.types import AgentType
from agents.validation import validate_agent_input, validate_agent_type
from config.exceptions import ValidationError
from workflows.state import WorkflowState, WorkflowStatus

DEFAULT_AGENT_SEQUENCE: tuple[AgentType, ...] = (
    AgentType.RESEARCH,
    AgentType.NUTRITION,
    AgentType.CONTENT,
    AgentType.REVIEW,
)


def validate_workflow_request(original_request: str) -> str:
    """Validate the original workflow request."""

    return validate_agent_input(original_request)


def validate_agent_sequence(
    agent_sequence: Sequence[AgentType | str],
) -> tuple[AgentType, ...]:
    """Validate the required sequential workflow agent order."""

    normalized_sequence = tuple(
        validate_agent_type(agent_type) for agent_type in agent_sequence
    )
    if not normalized_sequence:
        raise ValidationError("Agent sequence must not be empty.")

    if normalized_sequence != DEFAULT_AGENT_SEQUENCE:
        raise ValidationError(
            "Agent sequence does not match the supported workflow.",
            details={
                "expected": [agent_type.value for agent_type in DEFAULT_AGENT_SEQUENCE],
                "received": [agent_type.value for agent_type in normalized_sequence],
            },
        )

    if len(set(normalized_sequence)) != len(normalized_sequence):
        raise ValidationError("Agent sequence must not contain duplicates.")

    return normalized_sequence


def validate_workflow_state(state: WorkflowState) -> None:
    """Validate workflow state shape and values."""

    validate_workflow_request(state["original_request"])

    try:
        WorkflowStatus(state["execution_status"])
    except ValueError as exc:
        raise ValidationError(
            "Workflow state has an invalid execution status.",
            details={"execution_status": state["execution_status"]},
        ) from exc

    current_agent = state["current_agent"]
    if current_agent is not None:
        validate_agent_type(current_agent)

    if not isinstance(state["workflow_metadata"], dict):
        raise ValidationError("Workflow metadata must be a dictionary.")

    if "workflow_id" not in state["workflow_metadata"]:
        raise ValidationError("Workflow metadata must include workflow_id.")

    if not isinstance(state["intermediate_outputs"], dict):
        raise ValidationError("Intermediate outputs must be a dictionary.")

    if not isinstance(state["errors"], list):
        raise ValidationError("Workflow errors must be a list.")


def validate_transition(
    *,
    current_agent: str | None,
    next_agent: AgentType,
    agent_sequence: Sequence[AgentType | str],
) -> None:
    """Validate a sequential transition between workflow agents."""

    sequence = validate_agent_sequence(agent_sequence)
    next_agent_index = sequence.index(next_agent)

    if current_agent is None:
        if next_agent_index != 0:
            raise ValidationError(
                "Workflow must start with the first configured agent.",
                details={"next_agent": next_agent.value},
            )
        return

    current_agent_type = validate_agent_type(current_agent)
    current_agent_index = sequence.index(current_agent_type)
    if next_agent_index != current_agent_index + 1:
        raise ValidationError(
            "Invalid workflow transition.",
            details={
                "current_agent": current_agent_type.value,
                "next_agent": next_agent.value,
            },
        )


def validate_factory_supports_sequence(
    agent_factory: AgentFactory,
    agent_sequence: Sequence[AgentType | str],
) -> None:
    """Validate that a factory can create every agent in a sequence."""

    available_agent_types = set(agent_factory.list_agent_types())
    required_agent_types = set(validate_agent_sequence(agent_sequence))
    missing_agent_types = required_agent_types - available_agent_types

    if missing_agent_types:
        raise ValidationError(
            "Agent factory is missing required workflow agents.",
            details={
                "missing": [
                    agent_type.value for agent_type in sorted(missing_agent_types)
                ]
            },
        )
