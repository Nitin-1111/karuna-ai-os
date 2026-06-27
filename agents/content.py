"""Content agent foundation."""

from agents.base import BaseAgent
from agents.types import AgentType


class ContentAgent(BaseAgent):
    """Reusable content agent foundation."""

    agent_type = AgentType.CONTENT
    display_name = "Content Agent"

    def _execute(self, agent_input: str) -> str:
        """Return a phase-safe content agent response."""

        return "ContentAgent received the request for future content handling."
