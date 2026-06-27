"""Base agent abstraction for Karuna AI OS."""

from abc import ABC, abstractmethod

from agents.types import AgentType
from agents.validation import validate_agent_input
from config.logger import get_logger
from llm.base import BaseLlmProvider
from memory.repository import LocalDocumentRepository


class BaseAgent(ABC):
    """Base class for all reusable agents."""

    agent_type: AgentType
    display_name: str

    def __init__(
        self,
        *,
        llm_provider: BaseLlmProvider | None = None,
        document_repository: LocalDocumentRepository | None = None,
    ) -> None:
        self._llm_provider = llm_provider
        self._document_repository = document_repository
        self._logger = get_logger(f"{__name__}.{self.agent_type.value}")

    def execute(self, agent_input: str) -> str:
        """Validate input and execute the concrete agent."""

        validated_input = validate_agent_input(agent_input)
        self._logger.info(
            "Executing agent.",
            extra={
                "agent_type": self.agent_type.value,
                "input_length": len(validated_input),
            },
        )
        return self._execute(validated_input)

    def health_check(self) -> bool:
        """Return whether this agent is ready for framework-level use."""

        self._logger.info(
            "Running agent health check.",
            extra={"agent_type": self.agent_type.value},
        )
        return True

    def provider_name(self) -> str | None:
        """Return the injected provider name without calling the provider."""

        if self._llm_provider is None:
            return None
        return self._llm_provider.provider_name()

    @abstractmethod
    def _execute(self, agent_input: str) -> str:
        """Execute an agent after shared validation has completed."""
