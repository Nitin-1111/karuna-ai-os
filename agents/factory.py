"""Agent factory for creating supported agents."""

from agents.base import BaseAgent
from agents.content import ContentAgent
from agents.nutrition import NutritionAgent
from agents.registry import AgentRegistry, create_agent_registry
from agents.research import ResearchAgent
from agents.review import ReviewAgent
from agents.types import AgentType
from agents.validation import validate_agent_type
from config.logger import get_logger
from llm.base import BaseLlmProvider
from memory.repository import LocalDocumentRepository


class AgentFactory:
    """Factory responsible for creating agent instances."""

    def __init__(
        self,
        *,
        registry: AgentRegistry | None = None,
        llm_provider: BaseLlmProvider | None = None,
        document_repository: LocalDocumentRepository | None = None,
    ) -> None:
        self._registry = registry or create_default_agent_registry()
        self._llm_provider = llm_provider
        self._document_repository = document_repository
        self._logger = get_logger(__name__)

    def create_agent(self, agent_type: AgentType | str) -> BaseAgent:
        """Create an agent instance for a supported agent type."""

        validated_agent_type = validate_agent_type(agent_type)
        agent_class = self._registry.get(validated_agent_type)

        self._logger.info(
            "Creating agent.",
            extra={"agent_type": validated_agent_type.value},
        )
        return agent_class(
            llm_provider=self._llm_provider,
            document_repository=self._document_repository,
        )

    def list_agent_types(self) -> list[AgentType]:
        """Return agent types available through this factory."""

        return self._registry.list_agents()


def create_default_agent_registry() -> AgentRegistry:
    """Create the default registry for Phase 5 agents."""

    return create_agent_registry(
        [
            (AgentType.CONTENT, ContentAgent),
            (AgentType.NUTRITION, NutritionAgent),
            (AgentType.RESEARCH, ResearchAgent),
            (AgentType.REVIEW, ReviewAgent),
        ]
    )


def create_agent_factory(
    *,
    llm_provider: BaseLlmProvider | None = None,
    document_repository: LocalDocumentRepository | None = None,
) -> AgentFactory:
    """Create a factory configured with optional shared dependencies."""

    return AgentFactory(
        llm_provider=llm_provider,
        document_repository=document_repository,
    )
