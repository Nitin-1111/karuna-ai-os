"""Research agent foundation."""

from agents.base import BaseAgent
from agents.types import AgentType


class ResearchAgent(BaseAgent):
    """Reusable research agent foundation."""

    agent_type = AgentType.RESEARCH
    display_name = "Research Agent"

    def _execute(self, agent_input: str) -> str:
        """Return a phase-safe research agent response."""

        return "ResearchAgent received the request for future research handling."
