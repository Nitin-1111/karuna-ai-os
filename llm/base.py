"""Provider-agnostic LLM provider interface."""

from abc import ABC, abstractmethod


class BaseLlmProvider(ABC):
    """Abstract interface implemented by all LLM providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text for a prompt."""

    @abstractmethod
    def health_check(self) -> bool:
        """Return whether the configured provider is reachable."""

    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider identifier."""
