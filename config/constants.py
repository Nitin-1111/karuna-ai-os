"""Application-wide constants for Karuna AI OS."""

from enum import StrEnum


class AppEnvironment(StrEnum):
    """Supported application runtime environments."""

    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class LlmProvider(StrEnum):
    """Supported language model provider identifiers."""

    GROQ = "groq"
    GOOGLE = "google"


class LogLevel(StrEnum):
    """Supported logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


APP_LOGGER_NAME = "karuna_ai_os"
ENV_FILE_NAME = ".env"

ENV_APP_NAME = "APP_NAME"
ENV_APP_ENV = "APP_ENV"
ENV_HOST = "HOST"
ENV_PORT = "PORT"
ENV_LOG_LEVEL = "LOG_LEVEL"
ENV_LLM_PROVIDER = "LLM_PROVIDER"
ENV_LLM_API_KEY = "LLM_API_KEY"
ENV_LLM_MODEL = "LLM_MODEL"
ENV_DOCUMENT_STORAGE_PATH = "DOCUMENT_STORAGE_PATH"
ENV_MEMORY_STORAGE_PATH = "MEMORY_STORAGE_PATH"

DEFAULT_APP_NAME = "Karuna AI OS"
DEFAULT_APP_ENV = AppEnvironment.DEVELOPMENT
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_LOG_LEVEL = LogLevel.INFO
DEFAULT_LLM_PROVIDER = LlmProvider.GROQ
DEFAULT_DOCUMENT_STORAGE_PATH = "./storage/documents"
DEFAULT_MEMORY_STORAGE_PATH = "./storage/memory"

SUPPORTED_LLM_PROVIDERS = frozenset(provider.value for provider in LlmProvider)
SUPPORTED_LOG_LEVELS = frozenset(level.value for level in LogLevel)
