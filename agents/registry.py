"""Agent registry for supported agent implementations."""

from collections.abc import Iterable

from agents.base import BaseAgent
from agents.types import AgentType
from agents.validation import validate_agent_class, validate_agent_type
from config.exceptions import ConfigurationError, ValidationError


class AgentRegistry:
    """Registry for mapping agent types to agent classes."""

    def __init__(self) -> None:
        self._agents: dict[AgentType, type[BaseAgent]] = {}

    def register(
        self,
        agent_type: AgentType | str,
        agent_class: type[BaseAgent],
    ) -> None:
        """Register an agent class for an agent type."""

        validated_agent_type = validate_agent_type(agent_type)
        validate_agent_class(agent_class)

        if validated_agent_type in self._agents:
            raise ValidationError(
                "Agent type is already registered.",
                details={"agent_type": validated_agent_type.value},
            )

        if agent_class.agent_type is not validated_agent_type:
            raise ValidationError(
                "Agent class type does not match registry type.",
                details={
                    "registered_type": validated_agent_type.value,
                    "agent_class_type": agent_class.agent_type.value,
                },
            )

        self._agents[validated_agent_type] = agent_class

    def get(self, agent_type: AgentType | str) -> type[BaseAgent]:
        """Return the registered class for an agent type."""

        validated_agent_type = validate_agent_type(agent_type)
        agent_class = self._agents.get(validated_agent_type)
        if agent_class is None:
            raise ConfigurationError(
                "Agent type is not registered.",
                details={"agent_type": validated_agent_type.value},
            )
        return agent_class

    def list_agents(self) -> list[AgentType]:
        """Return all registered agent types."""

        return sorted(self._agents, key=lambda agent_type: agent_type.value)

    def validate_registrations(self) -> None:
        """Validate all registered agent mappings."""

        for agent_type, agent_class in self._agents.items():
            validate_agent_class(agent_class)
            if agent_class.agent_type is not agent_type:
                raise ValidationError(
                    "Agent registry contains an invalid mapping.",
                    details={
                        "registered_type": agent_type.value,
                        "agent_class_type": agent_class.agent_type.value,
                    },
                )


def create_agent_registry(
    registrations: Iterable[tuple[AgentType, type[BaseAgent]]],
) -> AgentRegistry:
    """Create a registry from explicit registrations."""

    registry = AgentRegistry()
    for agent_type, agent_class in registrations:
        registry.register(agent_type, agent_class)
    registry.validate_registrations()
    return registry
