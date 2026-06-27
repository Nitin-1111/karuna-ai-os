"""Agent type definitions for Karuna AI OS."""

from enum import StrEnum


class AgentType(StrEnum):
    """Supported agent identifiers."""

    RESEARCH = "research"
    NUTRITION = "nutrition"
    CONTENT = "content"
    REVIEW = "review"
