"""Workflow execution interface for LangGraph orchestration."""

from collections.abc import Mapping
from typing import Any, cast

from agents.factory import AgentFactory
from config.exceptions import ApplicationError
from config.logger import get_logger
from workflows.builder import WorkflowBuilder
from workflows.state import (
    WorkflowState,
    create_initial_workflow_state,
    get_workflow_id,
    mark_workflow_failed,
)
from workflows.validation import validate_workflow_request, validate_workflow_state


class SequentialAgentWorkflow:
    """Executable sequential workflow for the supported agents."""

    def __init__(self, *, agent_factory: AgentFactory | None = None) -> None:
        self._builder = WorkflowBuilder(agent_factory=agent_factory)
        self._compiled_graph = self._builder.compile()
        self._logger = get_logger(__name__)

    def execute(
        self,
        original_request: str,
        *,
        workflow_metadata: Mapping[str, str] | None = None,
    ) -> WorkflowState:
        """Execute the sequential agent workflow."""

        validated_request = validate_workflow_request(original_request)
        state = create_initial_workflow_state(
            validated_request,
            workflow_metadata=dict(workflow_metadata or {}),
        )
        workflow_id = get_workflow_id(state)

        self._logger.info(
            "Workflow started.",
            extra={"workflow_id": workflow_id},
        )

        try:
            result = self._compiled_graph.invoke(state)
            completed_state = cast(WorkflowState, result)
            validate_workflow_state(completed_state)
        except ApplicationError as exc:
            failed_state = mark_workflow_failed(state, str(exc))
            self._logger.error(
                "Workflow failed.",
                extra={"workflow_id": workflow_id, "error_type": type(exc).__name__},
            )
            return failed_state
        except Exception as exc:
            failed_state = mark_workflow_failed(state, str(exc))
            self._logger.error(
                "Workflow failed.",
                extra={"workflow_id": workflow_id, "error_type": type(exc).__name__},
            )
            return failed_state

        self._logger.info(
            "Workflow completed.",
            extra={"workflow_id": workflow_id},
        )
        return completed_state

    def compiled_graph(self) -> Any:
        """Return the compiled LangGraph object."""

        return self._compiled_graph


def create_sequential_workflow(
    *,
    agent_factory: AgentFactory | None = None,
) -> SequentialAgentWorkflow:
    """Create the default sequential agent workflow."""

    return SequentialAgentWorkflow(agent_factory=agent_factory)
