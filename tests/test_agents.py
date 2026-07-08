"""Tests for the reusable agent framework."""

import pytest

from agents import AgentFactory, AgentRegistry, AgentType, ResearchAgent
from agents.validation import validate_agent_input
from config.exceptions import ConfigurationError, ValidationError


def test_agent_factory_creates_all_supported_agents() -> None:
    """The default factory should expose every supported agent type."""

    factory = AgentFactory()

    assert factory.list_agent_types() == [
        AgentType.CONTENT,
        AgentType.NUTRITION,
        AgentType.RESEARCH,
        AgentType.REVIEW,
    ]
    agent = factory.create_agent(AgentType.RESEARCH)
    assert agent.display_name == "Research Agent"
    assert agent.execute("hello").startswith("ResearchAgent")
    assert agent.health_check() is True


def test_agent_factory_rejects_unknown_agent() -> None:
    """Unsupported agent types should raise shared validation errors."""

    with pytest.raises(ValidationError):
        AgentFactory().create_agent("unknown")


def test_registry_prevents_duplicate_registration() -> None:
    """Agent registry should prevent duplicate agent mappings."""

    registry = AgentRegistry()
    registry.register(AgentType.RESEARCH, ResearchAgent)

    with pytest.raises(ValidationError):
        registry.register(AgentType.RESEARCH, ResearchAgent)


def test_registry_rejects_missing_registration() -> None:
    """Agent registry should fail fast for missing registrations."""

    with pytest.raises(ConfigurationError):
        AgentRegistry().get(AgentType.RESEARCH)


def test_validate_agent_input_rejects_empty_text() -> None:
    """Agent input validation should reject blank strings."""

    with pytest.raises(ValidationError):
        validate_agent_input("   ")
