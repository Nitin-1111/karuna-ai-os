"""Shared validation helpers for LLM providers."""

from config.exceptions import ConfigurationError, ProviderError
from config.settings import Settings


def require_provider_api_key(settings: Settings, provider_name: str) -> str:
    """Return the configured API key or raise a configuration error."""

    api_key = settings.provider.api_key
    if api_key is None:
        raise ConfigurationError(
            "LLM provider requires LLM_API_KEY.",
            details={"provider": provider_name},
        )
    return api_key


def require_provider_model(settings: Settings, provider_name: str) -> str:
    """Return the configured model or raise a configuration error."""

    model = settings.provider.model
    if model is None:
        raise ConfigurationError(
            "LLM provider requires LLM_MODEL.",
            details={"provider": provider_name},
        )
    return model


def normalize_prompt(prompt: str) -> str:
    """Normalize and validate text generation prompts."""

    normalized_prompt = prompt.strip()
    if not normalized_prompt:
        raise ProviderError("Prompt must not be empty.")
    return normalized_prompt
