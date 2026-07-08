"""Tests for provider-agnostic LLM creation and providers."""

from types import SimpleNamespace

import pytest

from config.constants import LlmProvider
from config.exceptions import ConfigurationError, ProviderError
from config.settings import load_settings
from llm.factory import create_llm_provider
from llm.gemini_provider import GeminiProvider
from llm.groq_provider import GroqProvider
from llm.validation import normalize_prompt


class FakeGroqCompletions:
    """Fake Groq completions client for deterministic tests."""

    def create(self, **_: object) -> SimpleNamespace:
        """Return a minimal Groq-like response object."""

        message = SimpleNamespace(content="groq response")
        choice = SimpleNamespace(message=message)
        return SimpleNamespace(choices=[choice])


class FakeGroqClient:
    """Fake Groq SDK client."""

    def __init__(self, *, api_key: str) -> None:
        self.api_key = api_key
        self.chat = SimpleNamespace(
            completions=FakeGroqCompletions(),
        )


class FakeGeminiModels:
    """Fake Gemini models client for deterministic tests."""

    def generate_content(self, **_: object) -> SimpleNamespace:
        """Return a minimal Gemini-like response object."""

        return SimpleNamespace(text="gemini response")


class FakeGeminiClient:
    """Fake Google GenAI SDK client."""

    def __init__(self, *, api_key: str) -> None:
        self.api_key = api_key
        self.models = FakeGeminiModels()


def test_create_llm_provider_selects_groq(
    monkeypatch: pytest.MonkeyPatch,
    settings_environ: dict[str, str],
) -> None:
    """The LLM factory should create the configured Groq provider."""

    monkeypatch.setattr("llm.groq_provider.Groq", FakeGroqClient)
    settings_environ["LLM_PROVIDER"] = LlmProvider.GROQ.value
    settings = load_settings(environ=settings_environ)

    provider = create_llm_provider(settings=settings)

    assert isinstance(provider, GroqProvider)
    assert provider.provider_name() == "groq"
    assert provider.generate("hello") == "groq response"
    assert provider.health_check() is True


def test_create_llm_provider_selects_google(
    monkeypatch: pytest.MonkeyPatch,
    settings_environ: dict[str, str],
) -> None:
    """The LLM factory should create the configured Gemini provider."""

    monkeypatch.setattr("llm.gemini_provider.genai.Client", FakeGeminiClient)
    settings_environ["LLM_PROVIDER"] = LlmProvider.GOOGLE.value
    settings = load_settings(environ=settings_environ)

    provider = create_llm_provider(settings=settings)

    assert isinstance(provider, GeminiProvider)
    assert provider.provider_name() == "google"
    assert provider.generate("hello") == "gemini response"
    assert provider.health_check() is True


def test_provider_requires_api_key(settings_environ: dict[str, str]) -> None:
    """Provider construction should fail without required credentials."""

    settings_environ.pop("LLM_API_KEY")
    settings = load_settings(environ=settings_environ)

    with pytest.raises(ConfigurationError):
        create_llm_provider(settings=settings)


def test_normalize_prompt_rejects_empty_prompt() -> None:
    """Provider prompt validation should reject blank prompts."""

    with pytest.raises(ProviderError):
        normalize_prompt("   ")
