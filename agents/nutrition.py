"""Nutrition agent foundation."""

from agents.base import BaseAgent
from agents.types import AgentType


class NutritionAgent(BaseAgent):
    """Reusable nutrition agent foundation."""

    agent_type = AgentType.NUTRITION
    display_name = "Nutrition Agent"

    def _execute(self, agent_input: str) -> str:
        """Return a phase-safe nutrition agent response."""

        return "NutritionAgent received the request for future nutrition handling."
