# Karuna AI OS

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Karuna AI OS is a production-oriented AI operating system backend built with
FastAPI. Version 1.0 provides the backend foundation, provider-agnostic LLM
layer, local document storage, reusable agent framework, LangGraph orchestration,
REST APIs, structured logging, and automated tests.

The project is intentionally modular. API handlers stay thin and delegate to the
existing configuration, provider, storage, agent, and workflow layers.

## Features

- FastAPI application factory with lifespan startup and shutdown handling.
- Versioned REST API under `/api/v1`.
- Health, readiness, version, agent, workflow, and document endpoints.
- Provider-agnostic LLM abstraction with Groq and Google Gemini support.
- Dynamic provider and model selection through environment configuration.
- Local filesystem document storage with JSON metadata.
- Reusable agent framework for research, nutrition, content, and review agents.
- Sequential LangGraph workflow connecting the supported agents.
- Structured JSON console logging with request IDs and timing.
- Shared exception hierarchy and centralized API error responses.
- Pytest coverage for config, LLM providers, storage, agents, workflows, APIs,
  imports, and smoke flows.

## Current Scope

Version 1.0 includes backend infrastructure and phase-safe agent/workflow
execution. The concrete agents currently return deterministic framework
responses. Provider integrations exist and can generate text when used directly,
but API workflows do not call LLMs or perform prompt engineering.

The following are intentionally out of scope for Version 1.0:

- Authentication and authorization.
- User accounts and sessions.
- Streaming, WebSockets, and server-sent events.
- Vector databases, embeddings, RAG, and memory retrieval.
- Prompt templates and tool execution.
- Frontend applications.
- Docker, Kubernetes, CI/CD, and cloud deployment assets.

## Architecture Summary

```text
HTTP client
    |
FastAPI backend
    |
Versioned REST API
    |
+----------------------+----------------------+----------------------+
| Agent framework      | LangGraph workflow   | Document repository  |
+----------------------+----------------------+----------------------+
    |                         |                         |
Provider abstraction      Shared state              Filesystem storage
    |                                                   |
Groq / Google Gemini                                 JSON metadata
```

The main package boundaries are:

- `backend/`: FastAPI app, middleware, dependencies, exception handlers, health
  routes, and versioned REST APIs.
- `config/`: validated settings, constants, environment loading, filesystem
  helpers, logging, and shared exceptions.
- `llm/`: provider-agnostic LLM interface, provider factory, Groq provider, and
  Google Gemini provider.
- `memory/`: local document model, metadata model, validation, filesystem
  storage, and repository.
- `agents/`: base agent abstraction, agent types, registry, factory, validation,
  and concrete framework agents.
- `workflows/`: LangGraph state, nodes, builder, validation, and sequential
  execution interface.
- `tests/`: automated unit, integration, import, and smoke tests.

## Folder Structure

```text
karuna-ai-os/
|-- agents/
|-- backend/
|   `-- api/
|       `-- v1/
|-- config/
|-- database/
|-- docs/
|-- llm/
|-- memory/
|-- scripts/
|-- tests/
|-- tools/
|-- workflows/
|-- .env.example
|-- .gitignore
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- README.md
|-- RELEASE_NOTES.md
`-- pyproject.toml
```

`database/` and `tools/` are reserved package boundaries and do not contain
runtime database or tool-execution implementations in Version 1.0.

## Requirements

- Python 3.12
- PowerShell on Windows for the included helper scripts
- A Groq or Google Gemini API key only when directly using the LLM provider layer

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install runtime and development dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` for your environment.

## Environment Configuration

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `APP_NAME` | No | `Karuna AI OS` | Public application name. |
| `APP_ENV` | No | `development` | Runtime environment: `development`, `test`, `staging`, or `production`. |
| `LOG_LEVEL` | No | `INFO` | Structured logger level. |
| `HOST` | No | `127.0.0.1` | Local server host used by scripts/manual runs. |
| `PORT` | No | `8000` | Local server port used by scripts/manual runs. |
| `LLM_PROVIDER` | No | `groq` | Supported values: `groq`, `google`. |
| `LLM_API_KEY` | Production | empty | Provider API key. Required in production and for direct provider calls. |
| `LLM_MODEL` | Production | empty | Provider model identifier. No model names are hardcoded in Python. |
| `DOCUMENT_STORAGE_PATH` | No | `./storage/documents` | Filesystem root for local documents. |
| `MEMORY_STORAGE_PATH` | No | `./storage/memory` | Filesystem root reserved for memory data. |

Supported providers are exactly:

- `groq`
- `google`

## Running the Backend

Start the API server:

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Then open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

The included development script prepares the environment:

```powershell
.\scripts\dev.ps1
```

## API Reference

Infrastructure endpoints:

- `GET /`
- `GET /health`
- `GET /health/live`
- `GET /health/ready`
- `GET /version`

Versioned API endpoints:

- `GET /api/v1/agents`
- `GET /api/v1/agents/{agent_type}`
- `POST /api/v1/agents/{agent_type}/run`
- `POST /api/v1/workflows/run`
- `POST /api/v1/documents`
- `GET /api/v1/documents`
- `GET /api/v1/documents/{document_id}`
- `DELETE /api/v1/documents/{document_id}`

### Agent Example

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/agents/research/run" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"input":"Prepare a wellness research outline."}'
```

### Workflow Example

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/workflows/run" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"request":"Prepare reviewed wellness content.","metadata":{"source":"manual"}}'
```

The workflow runs the sequence:

```text
Research -> Nutrition -> Content -> Review -> Final Result
```

### Document Example

`content_base64` must contain base64-encoded bytes.

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/documents" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"filename":"sample.txt","content_base64":"SGVsbG8gS2FydW5h","content_type":"text/plain","metadata":{"source":"manual"}}'
```

## Logging

Logging is configured through `config.logger`. The backend emits structured JSON
logs to the console. Request middleware attaches:

- `X-Request-ID`
- HTTP method and path
- response status code
- request duration in milliseconds

Application errors are handled centrally and returned as consistent JSON error
responses without stack traces.

## Document Storage

Documents are stored on the local filesystem under `DOCUMENT_STORAGE_PATH`.
Each document receives a unique document ID and is stored in its own directory
with:

- original filename
- sanitized stored filename
- content bytes
- content type
- file size
- creation and modification timestamps
- JSON metadata

The storage layer validates filenames, content, metadata, document IDs, and
filesystem paths.

## Agents

Version 1.0 includes four framework agents:

- `research`
- `nutrition`
- `content`
- `review`

Agents inherit the shared base class, support validation and health checks, and
are created through the agent factory. They do not contain prompt templates or
business-specific AI behavior in Version 1.0.

## Workflow

The workflow layer uses LangGraph `StateGraph` to execute the supported agent
sequence. Workflow state carries:

- original request
- workflow metadata
- current agent
- intermediate outputs
- final output
- execution status
- errors

Workflow execution is exposed through `POST /api/v1/workflows/run`.

## Testing

Run all tests:

```powershell
python -m pytest
```

Run quality checks:

```powershell
python -m ruff check backend workflows agents config llm memory tests
python -m mypy backend workflows agents config llm memory
python -m mypy tests
python -m compileall -q agents backend config database llm memory tools workflows tests
```

Or use the script:

```powershell
.\scripts\test.ps1
```

If local PowerShell execution policy blocks scripts, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test.ps1
```

For managed runtimes, set `KARUNA_PYTHON` to a Python 3.12 executable before
running the script.

## Release Notes

Version 1.0 release notes are available in `RELEASE_NOTES.md`.
The changelog is available in `CHANGELOG.md`.

## Contributing

See `CONTRIBUTING.md` for development workflow, verification commands, and
scope-control rules.

## License

Karuna AI OS is released under the MIT License. See `LICENSE`.
