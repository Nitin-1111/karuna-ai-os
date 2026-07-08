"""LangGraph workflow builder."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from agents.factory import AgentFactory
from agents.types import AgentType
from workflows.nodes import create_agent_node
from workflows.state import WorkflowState
from workflows.validation import (
    DEFAULT_AGENT_SEQUENCE,
    validate_agent_sequence,
    validate_factory_supports_sequence,
)


class WorkflowBuilder:
    """Builds the supported sequential LangGraph workflow."""

    def __init__(
        self,
        *,
        agent_factory: AgentFactory | None = None,
        agent_sequence: tuple[AgentType, ...] = DEFAULT_AGENT_SEQUENCE,
    ) -> None:
        self._agent_factory = agent_factory or AgentFactory()
        self._agent_sequence = validate_agent_sequence(agent_sequence)
        validate_factory_supports_sequence(self._agent_factory, self._agent_sequence)

    def build(self) -> StateGraph[WorkflowState, None, WorkflowState, WorkflowState]:
        """Build the sequential StateGraph."""

        graph: StateGraph[WorkflowState, None, WorkflowState, WorkflowState] = (
            StateGraph(WorkflowState)
        )

        for index, agent_type in enumerate(self._agent_sequence):
            graph.add_node(
                agent_type.value,
                create_agent_node(
                    agent_type=agent_type,
                    agent_factory=self._agent_factory,
                    agent_sequence=self._agent_sequence,
                    is_final=index == len(self._agent_sequence) - 1,
                ),
            )

        graph.add_edge(START, self._agent_sequence[0].value)
        for current_agent, next_agent in zip(
            self._agent_sequence,
            self._agent_sequence[1:],
            strict=False,
        ):
            graph.add_edge(current_agent.value, next_agent.value)
        graph.add_edge(self._agent_sequence[-1].value, END)

        return graph

    def compile(self) -> Any:
        """Compile the sequential StateGraph."""

        return self.build().compile()


def create_workflow_builder(
    *,
    agent_factory: AgentFactory | None = None,
) -> WorkflowBuilder:
    """Create the default workflow builder."""

    return WorkflowBuilder(agent_factory=agent_factory)
