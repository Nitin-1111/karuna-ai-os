"""FastAPI dependency providers for backend infrastructure."""

import logging
from collections.abc import Callable
from typing import cast

from fastapi import Request

from agents.factory import AgentFactory
from config.logger import get_logger
from config.settings import Settings
from llm.base import BaseLlmProvider
from llm.factory import create_llm_provider
from memory.repository import LocalDocumentRepository, create_document_repository
from workflows.builder import WorkflowBuilder
from workflows.graph import SequentialAgentWorkflow


def get_settings_dependency(request: Request) -> Settings:
    """Return application settings from FastAPI state."""

    return cast(Settings, request.app.state.settings)


def get_logger_dependency() -> logging.Logger:
    """Return the shared application logger."""

    return get_logger("backend")


def get_llm_provider_factory(request: Request) -> Callable[[], BaseLlmProvider]:
    """Return a callable that creates the configured LLM provider."""

    settings = cast(Settings, request.app.state.settings)

    def factory() -> BaseLlmProvider:
        return create_llm_provider(settings=settings)

    return factory


def get_document_repository(request: Request) -> LocalDocumentRepository:
    """Return the configured local document repository."""

    return cast(LocalDocumentRepository, request.app.state.document_repository)


def get_agent_factory(request: Request) -> AgentFactory:
    """Return the configured agent factory."""

    return cast(AgentFactory, request.app.state.agent_factory)


def get_workflow_builder(request: Request) -> WorkflowBuilder:
    """Return the configured workflow builder."""

    return cast(WorkflowBuilder, request.app.state.workflow_builder)


def get_sequential_workflow(request: Request) -> SequentialAgentWorkflow:
    """Return the configured sequential workflow."""

    return cast(SequentialAgentWorkflow, request.app.state.sequential_workflow)


def create_document_repository_dependency(
    settings: Settings,
) -> LocalDocumentRepository:
    """Create a document repository from settings."""

    return create_document_repository(settings=settings)
