"""Factory for provider-agnostic LLM provider creation."""

from config.constants import LlmProvider
from config.exceptions import ConfigurationError
from config.logger import get_logger
from config.settings import Settings, get_settings
from llm.base import BaseLlmProvider
from llm.gemini_provider import GeminiProvider
from llm.groq_provider import GroqProvider


def create_llm_provider(settings: Settings | None = None) -> BaseLlmProvider:
    """Create the configured LLM provider."""

    resolved_settings = settings or get_settings()
    provider = resolved_settings.provider.provider
    logger = get_logger(__name__)

    logger.info(
        "Creating LLM provider.",
        extra={"provider": provider.value, "model": resolved_settings.provider.model},
    )

    match provider:
        case LlmProvider.GROQ:
            return GroqProvider(settings=resolved_settings)
        case LlmProvider.GOOGLE:
            return GeminiProvider(settings=resolved_settings)
        case _:
            raise ConfigurationError(
                "Unsupported LLM provider.",
                details={"provider": str(provider)},
            )
