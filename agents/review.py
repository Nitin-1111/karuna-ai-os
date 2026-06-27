"""Review agent foundation."""

from agents.base import BaseAgent
from agents.types import AgentType


class ReviewAgent(BaseAgent):
    """Reusable review agent foundation."""

    agent_type = AgentType.REVIEW
    display_name = "Review Agent"

    def _execute(self, agent_input: str) -> str:
        """Return a phase-safe review agent response."""

        return "ReviewAgent received the request for future review handling."
