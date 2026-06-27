"""Validation helpers for the reusable agent framework."""

from typing import Any

from agents.types import AgentType
from config.exceptions import ValidationError


def validate_agent_type(agent_type: AgentType | str) -> AgentType:
    """Validate and normalize an agent type."""

    if isinstance(agent_type, AgentType):
        return agent_type

    if not isinstance(agent_type, str):
        raise ValidationError(
            "Agent type must be a string or AgentType.",
            details={"type": type(agent_type).__name__},
        )

    normalized_agent_type = agent_type.strip().lower()
    if not normalized_agent_type:
        raise ValidationError("Agent type must not be empty.")

    try:
        return AgentType(normalized_agent_type)
    except ValueError as exc:
        raise ValidationError(
            "Unsupported agent type.",
            details={"agent_type": agent_type},
        ) from exc


def validate_agent_input(agent_input: str) -> str:
    """Validate and normalize user input for agent execution."""

    if not isinstance(agent_input, str):
        raise ValidationError(
            "Agent input must be a string.",
            details={"type": type(agent_input).__name__},
        )

    normalized_input = agent_input.strip()
    if not normalized_input:
        raise ValidationError("Agent input must not be empty.")

    return normalized_input


def validate_agent_class(agent_class: Any) -> None:
    """Validate that a registry value is a BaseAgent subclass."""

    from agents.base import BaseAgent

    if not isinstance(agent_class, type) or not issubclass(agent_class, BaseAgent):
        raise ValidationError(
            "Registered agent must inherit BaseAgent.",
            details={"agent_class": repr(agent_class)},
        )
