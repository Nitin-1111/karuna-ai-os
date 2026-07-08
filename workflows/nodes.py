"""LangGraph node implementations for agent execution."""

from collections.abc import Sequence

from agents.factory import AgentFactory
from agents.types import AgentType
from config.logger import get_logger
from workflows.state import (
    WorkflowState,
    get_next_agent_input,
    get_workflow_id,
    record_agent_output,
)
from workflows.validation import validate_transition, validate_workflow_state


class AgentExecutionNode:
    """Callable LangGraph node that executes one configured agent."""

    def __init__(
        self,
        *,
        agent_type: AgentType,
        agent_factory: AgentFactory,
        agent_sequence: Sequence[AgentType],
        is_final: bool = False,
    ) -> None:
        self._agent_type = agent_type
        self._agent_factory = agent_factory
        self._agent_sequence = tuple(agent_sequence)
        self._is_final = is_final
        self._logger = get_logger(__name__)

    def __call__(self, state: WorkflowState) -> WorkflowState:
        """Execute the configured agent and return updated workflow state."""

        validate_workflow_state(state)
        validate_transition(
            current_agent=state["current_agent"],
            next_agent=self._agent_type,
            agent_sequence=self._agent_sequence,
        )

        workflow_id = get_workflow_id(state)
        self._logger.info(
            "Workflow node entered.",
            extra={
                "workflow_id": workflow_id,
                "agent_type": self._agent_type.value,
            },
        )

        agent = self._agent_factory.create_agent(self._agent_type)
        agent_input = get_next_agent_input(state)
        agent_output = agent.execute(agent_input)
        updated_state = record_agent_output(
            state,
            agent_type=self._agent_type,
            output=agent_output,
            is_final=self._is_final,
        )

        self._logger.info(
            "Workflow node completed.",
            extra={
                "workflow_id": workflow_id,
                "agent_type": self._agent_type.value,
            },
        )
        return updated_state


def create_agent_node(
    *,
    agent_type: AgentType,
    agent_factory: AgentFactory,
    agent_sequence: Sequence[AgentType],
    is_final: bool = False,
) -> AgentExecutionNode:
    """Create an agent execution node."""

    return AgentExecutionNode(
        agent_type=agent_type,
        agent_factory=agent_factory,
        agent_sequence=agent_sequence,
        is_final=is_final,
    )
