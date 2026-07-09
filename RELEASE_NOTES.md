# Release Notes

## Karuna AI OS 1.0.0

Release date: 2026-07-09

Karuna AI OS 1.0.0 is the first release-ready backend foundation. It delivers a
modular FastAPI backend with provider-agnostic LLM infrastructure, local
document storage, a reusable agent framework, LangGraph orchestration, REST API
endpoints, structured logging, shared validation, and automated tests.

## Highlights

- FastAPI application with production-oriented middleware and lifespan startup.
- Versioned REST API at `/api/v1`.
- OpenAPI documentation through Swagger UI and ReDoc.
- Supported providers: Groq and Google Gemini.
- Provider/model changes through `.env`, without Python code changes.
- Local filesystem document persistence with JSON metadata.
- Agent framework for research, nutrition, content, and review agents.
- Sequential workflow: research -> nutrition -> content -> review.
- Centralized JSON error responses.
- Pytest suite for unit, integration, smoke, and import validation.

## Included Endpoints

- `GET /`
- `GET /health`
- `GET /health/live`
- `GET /health/ready`
- `GET /version`
- `GET /api/v1/agents`
- `GET /api/v1/agents/{agent_type}`
- `POST /api/v1/agents/{agent_type}/run`
- `POST /api/v1/workflows/run`
- `POST /api/v1/documents`
- `GET /api/v1/documents`
- `GET /api/v1/documents/{document_id}`
- `DELETE /api/v1/documents/{document_id}`

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

## Run

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

## Verify

```powershell
python -m pytest
python -m ruff check backend workflows agents config llm memory tests
python -m mypy backend workflows agents config llm memory
python -m compileall -q agents backend config database llm memory tools workflows tests
```

## Known Limits

Version 1.0 intentionally does not include authentication, frontend UI,
streaming, embeddings, vector databases, memory retrieval, prompt engineering,
tool execution, Docker, Kubernetes, CI/CD, or cloud deployment automation.
