# Architecture

Karuna AI OS Version 1.0 is a production-oriented Python backend with clear
module boundaries. The system is built around FastAPI, shared infrastructure,
provider-agnostic LLM access, local document storage, reusable agents, and a
sequential LangGraph workflow.

The architecture is intentionally incremental. Each layer exposes a focused
contract and avoids depending on higher-level layers.

## Design Principles

- Preserve clear module boundaries.
- Keep API handlers thin.
- Reuse shared configuration, logging, validation, and exceptions.
- Keep provider selection and model routing in configuration.
- Keep agents provider-agnostic.
- Keep storage filesystem-only in Version 1.0.
- Avoid future-phase features until explicitly implemented.

## Runtime Flow

```text
Client
  |
FastAPI application
  |
Middleware
  |
Router
  |
Versioned API endpoints
  |
+-------------------+----------------------+----------------------+
| Agent factory     | Sequential workflow  | Document repository  |
+-------------------+----------------------+----------------------+
        |                    |                       |
   BaseAgent          LangGraph StateGraph     Local filesystem
        |                    |                       |
Concrete agents       Workflow state          Metadata JSON
```

## Module Responsibilities

### `backend/`

Owns the HTTP application layer.

- `app.py`: FastAPI application factory.
- `lifespan.py`: startup and shutdown initialization.
- `middleware.py`: request ID, timing, request logging, CORS, trusted hosts.
- `dependencies.py`: dependency providers for settings, logger, agents,
  workflows, LLM provider factory, and document repository.
- `exception_handlers.py`: centralized JSON error responses.
- `health.py`: root, health, readiness, liveness, and version metadata routes.
- `api/v1/`: versioned REST API routes, schemas, validators, and presenters.

### `config/`

Owns shared infrastructure.

- Environment loading.
- Validated settings.
- Application constants.
- Path and filesystem helpers.
- Structured logging.
- Shared exception hierarchy.

### `llm/`

Owns provider-agnostic language model access.

- `BaseLlmProvider` defines `generate`, `health_check`, and `provider_name`.
- `create_llm_provider` selects the provider from `LLM_PROVIDER`.
- Supported providers are Groq and Google Gemini.
- API keys and models are read from settings.
- Model names are not hardcoded in Python.

### `memory/`

Owns local filesystem document persistence.

- Documents are stored under `DOCUMENT_STORAGE_PATH`.
- Metadata is persisted as JSON.
- Content is stored as bytes.
- Validation protects document IDs, filenames, metadata, content, and paths.

### `agents/`

Owns the reusable agent framework.

- `BaseAgent` provides common validation, logging, and execution shape.
- `AgentType` defines supported agent identifiers.
- `AgentRegistry` registers agent classes.
- `AgentFactory` creates agents.
- Concrete Version 1.0 agents: research, nutrition, content, review.

### `workflows/`

Owns LangGraph orchestration.

- `WorkflowState` carries request, metadata, current agent, outputs, status,
  and errors.
- `WorkflowBuilder` builds the supported `StateGraph`.
- `SequentialAgentWorkflow` executes the graph.
- Supported sequence: research, nutrition, content, review.

### `tests/`

Owns automated verification.

- Config validation tests.
- LLM factory/provider tests with focused SDK fakes.
- Document repository tests.
- Agent framework tests.
- Workflow tests.
- FastAPI integration tests.
- Import smoke tests.

## API Surface

Infrastructure:

- `GET /`
- `GET /health`
- `GET /health/live`
- `GET /health/ready`
- `GET /version`

Versioned API:

- `GET /api/v1/agents`
- `GET /api/v1/agents/{agent_type}`
- `POST /api/v1/agents/{agent_type}/run`
- `POST /api/v1/workflows/run`
- `POST /api/v1/documents`
- `GET /api/v1/documents`
- `GET /api/v1/documents/{document_id}`
- `DELETE /api/v1/documents/{document_id}`

## Error Handling

Shared application exceptions are mapped to JSON responses:

- `ValidationError` and `ConfigurationError`: 400
- missing document `StorageError`: 404
- other `StorageError` and `ProviderError`: 503
- unexpected exceptions: 500

FastAPI request validation errors return a consistent 422 response.

## Logging

The application uses structured JSON console logging. Middleware logs request
start, request completion, request IDs, status codes, and execution timing.

## Storage Format

Each stored document has:

- unique document ID
- original filename
- sanitized stored filename
- creation timestamp
- modification timestamp
- content type
- file size
- content storage path
- metadata JSON path
- JSON-compatible user metadata

## Package Boundaries

`database/` and `tools/` remain package boundaries for future expansion. Version
1.0 does not implement database persistence or tool execution.
