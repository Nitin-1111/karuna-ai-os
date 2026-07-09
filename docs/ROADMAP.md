# Roadmap

Karuna AI OS is implemented incrementally. Version 1.0 completes the first
release-ready backend foundation.

## Completed in Version 1.0

### Phase 1: Project Foundation

- Project structure.
- Python packaging.
- Dependency management.
- Development scripts.
- Environment template.
- Documentation skeleton.

### Phase 2: Configuration and Infrastructure

- Validated settings.
- Environment loading.
- Path helpers.
- Structured logging.
- Shared exceptions.
- Constants and utilities.

### Phase 3: LLM Provider Layer

- Provider interface.
- Groq provider.
- Google Gemini provider.
- Provider factory.
- Dynamic model routing from settings.

### Phase 4: Local Document Storage

- Document model.
- Metadata model.
- Filesystem repository.
- JSON metadata persistence.
- Validation and safe overwrite protection.

### Phase 5: Agent Framework

- Base agent abstraction.
- Agent type enum.
- Agent registry.
- Agent factory.
- Research, nutrition, content, and review agents.

### Phase 6: LangGraph Orchestration

- Shared workflow state.
- StateGraph builder.
- Sequential workflow.
- Agent execution nodes.
- Workflow validation.

### Phase 7: FastAPI Backend Foundation

- FastAPI application factory.
- Lifespan startup and shutdown.
- Middleware.
- Dependency injection foundation.
- Centralized exception handlers.
- Health and version endpoints.

### Phase 8: REST API Endpoints

- Versioned API routing.
- Pydantic request and response models.
- Agent endpoints.
- Workflow endpoint.
- Document endpoints.
- OpenAPI documentation.

### Phase 9: Testing and Production Hardening

- Unit tests.
- API integration tests.
- Workflow smoke tests.
- Import smoke tests.
- Deterministic test fixtures.
- Small reliability hardening.

### Phase 10: Documentation and Release Readiness

- Version 1.0 documentation refresh.
- Setup and API usage documentation.
- Architecture documentation update.
- Changelog and release notes.
- Contribution guidelines.

## Version 1.0 Status

Version 1.0 is release-ready as a backend foundation. It intentionally excludes
future product features such as authentication, frontend applications, vector
databases, embeddings, memory retrieval, prompt engineering, streaming, and
deployment automation.

## Future Work Candidates

Future versions may add functionality only through explicit implementation
phases. Candidate areas include:

- Production authentication and authorization.
- Rich AI request APIs.
- Prompt and tool orchestration.
- Memory retrieval and indexing.
- Embeddings and vector storage.
- Deployment and operations assets.
- Observability integrations.

These items are not implemented in Version 1.0.
