"""Groq LLM provider implementation."""

from typing import Any

from groq import Groq, GroqError

from config.constants import LlmProvider
from config.exceptions import ProviderError
from config.logger import get_logger
from config.settings import Settings, get_settings
from llm.base import BaseLlmProvider
from llm.validation import (
    normalize_prompt,
    require_provider_api_key,
    require_provider_model,
)


class GroqProvider(BaseLlmProvider):
    """Provider implementation backed by the Groq SDK."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._logger = get_logger(__name__)
        self._api_key = require_provider_api_key(
            self._settings,
            self.provider_name(),
        )
        self._model = require_provider_model(self._settings, self.provider_name())
        self._client = Groq(api_key=self._api_key)

    def generate(self, prompt: str) -> str:
        """Generate text using the configured Groq model."""

        normalized_prompt = normalize_prompt(prompt)
        self._logger.info(
            "Generating text with Groq.",
            extra={"provider": self.provider_name(), "model": self._model},
        )

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": normalized_prompt}],
            )
        except GroqError as exc:
            raise ProviderError(
                "Groq text generation failed.",
                details={"provider": self.provider_name(), "model": self._model},
            ) from exc

        generated_text = self._extract_text(response)
        self._logger.info(
            "Groq text generation completed.",
            extra={"provider": self.provider_name(), "model": self._model},
        )
        return generated_text

    def health_check(self) -> bool:
        """Verify Groq connectivity using the configured model."""

        self._logger.info(
            "Running Groq health check.",
            extra={"provider": self.provider_name(), "model": self._model},
        )

        try:
            self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": "health check"}],
                max_tokens=1,
            )
        except GroqError as exc:
            raise ProviderError(
                "Groq health check failed.",
                details={"provider": self.provider_name(), "model": self._model},
            ) from exc

        self._logger.info(
            "Groq health check completed.",
            extra={"provider": self.provider_name(), "model": self._model},
        )
        return True

    def provider_name(self) -> str:
        """Return the Groq provider identifier."""

        return LlmProvider.GROQ.value

    @staticmethod
    def _extract_text(response: Any) -> str:
        choices = getattr(response, "choices", None)
        if not choices:
            raise ProviderError("Groq response did not include choices.")

        message = getattr(choices[0], "message", None)
        content = getattr(message, "content", None)
        if not isinstance(content, str) or not content.strip():
            raise ProviderError("Groq response did not include generated text.")

        return content
