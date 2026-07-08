"""FastAPI application lifespan management."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from agents.factory import AgentFactory
from config.filesystem import ensure_directory
from config.logger import configure_logging, get_logger
from config.settings import get_settings
from memory.repository import create_document_repository
from workflows.builder import WorkflowBuilder


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize and tear down backend infrastructure."""

    settings = get_settings()
    configure_logging(log_level=settings.application.log_level)
    logger = get_logger("backend.lifespan")

    logger.info(
        "Application startup started.",
        extra={
            "application": settings.application.app_name,
            "environment": settings.application.app_env.value,
        },
    )

    ensure_directory(settings.paths.document_storage_path)
    ensure_directory(settings.paths.memory_storage_path)

    agent_factory = AgentFactory()
    workflow_builder = WorkflowBuilder(agent_factory=agent_factory)
    workflow_builder.build().compile()

    app.state.settings = settings
    app.state.logger = logger
    app.state.document_repository = create_document_repository(settings=settings)
    app.state.workflow_builder = workflow_builder
    app.state.agent_factory = agent_factory

    logger.info("Application startup completed.")

    try:
        yield
    finally:
        logger.info("Application shutdown started.")
        logger.info("Application shutdown completed.")
