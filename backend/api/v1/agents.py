"""Version 1 agent REST endpoints."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from agents.factory import AgentFactory
from backend.api.v1.presenters import present_agent
from backend.api.v1.schemas import (
    AgentListResponse,
    AgentRunRequest,
    AgentRunResponse,
    AgentSummaryResponse,
)
from backend.api.v1.validation import validate_api_agent_type
from backend.dependencies import get_agent_factory, get_logger_dependency

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get(
    "",
    response_model=AgentListResponse,
    summary="List supported agents",
    description="Return metadata for all registered agents.",
)
async def list_agents(
    agent_factory: Annotated[AgentFactory, Depends(get_agent_factory)],
) -> AgentListResponse:
    """List supported agents."""

    agents = [
        present_agent(agent_factory.create_agent(agent_type))
        for agent_type in agent_factory.list_agent_types()
    ]
    return AgentListResponse(agents=agents)


@router.get(
    "/{agent_type}",
    response_model=AgentSummaryResponse,
    summary="Get agent metadata",
    description="Return metadata for one supported agent.",
)
async def get_agent(
    agent_type: str,
    agent_factory: Annotated[AgentFactory, Depends(get_agent_factory)],
) -> AgentSummaryResponse:
    """Return metadata for one agent."""

    validated_agent_type = validate_api_agent_type(agent_type)
    return present_agent(agent_factory.create_agent(validated_agent_type))


@router.post(
    "/{agent_type}/run",
    response_model=AgentRunResponse,
    summary="Run an agent",
    description="Run a supported agent through the existing agent framework.",
)
async def run_agent(
    agent_type: str,
    request: AgentRunRequest,
    agent_factory: Annotated[AgentFactory, Depends(get_agent_factory)],
    logger: Annotated[logging.Logger, Depends(get_logger_dependency)],
) -> AgentRunResponse:
    """Run a supported agent."""

    validated_agent_type = validate_api_agent_type(agent_type)
    agent = agent_factory.create_agent(validated_agent_type)
    logger.info(
        "Agent API execution requested.",
        extra={"agent_type": validated_agent_type.value},
    )
    output = agent.execute(request.input)
    return AgentRunResponse(agent_type=validated_agent_type.value, output=output)
