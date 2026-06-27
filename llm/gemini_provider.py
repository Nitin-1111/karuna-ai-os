"""Google Gemini LLM provider implementation."""

from typing import Any

from google import genai
from google.genai import errors as genai_errors

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


class GeminiProvider(BaseLlmProvider):
    """Provider implementation backed by the Google GenAI SDK."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._logger = get_logger(__name__)
        self._api_key = require_provider_api_key(
            self._settings,
            self.provider_name(),
        )
        self._model = require_provider_model(self._settings, self.provider_name())
        self._client = genai.Client(api_key=self._api_key)

    def generate(self, prompt: str) -> str:
        """Generate text using the configured Gemini model."""

        normalized_prompt = normalize_prompt(prompt)
        self._logger.info(
            "Generating text with Gemini.",
            extra={"provider": self.provider_name(), "model": self._model},
        )

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=normalized_prompt,
            )
        except genai_errors.APIError as exc:
            raise ProviderError(
                "Gemini text generation failed.",
                details={"provider": self.provider_name(), "model": self._model},
            ) from exc

        generated_text = self._extract_text(response)
        self._logger.info(
            "Gemini text generation completed.",
            extra={"provider": self.provider_name(), "model": self._model},
        )
        return generated_text

    def health_check(self) -> bool:
        """Verify Gemini connectivity using the configured model."""

        self._logger.info(
            "Running Gemini health check.",
            extra={"provider": self.provider_name(), "model": self._model},
        )

        try:
            self._client.models.generate_content(
                model=self._model,
                contents="health check",
                config={"max_output_tokens": 1},
            )
        except genai_errors.APIError as exc:
            raise ProviderError(
                "Gemini health check failed.",
                details={"provider": self.provider_name(), "model": self._model},
            ) from exc

        self._logger.info(
            "Gemini health check completed.",
            extra={"provider": self.provider_name(), "model": self._model},
        )
        return True

    def provider_name(self) -> str:
        """Return the Google provider identifier."""

        return LlmProvider.GOOGLE.value

    @staticmethod
    def _extract_text(response: Any) -> str:
        text = getattr(response, "text", None)
        if not isinstance(text, str) or not text.strip():
            raise ProviderError("Gemini response did not include generated text.")
        return text
