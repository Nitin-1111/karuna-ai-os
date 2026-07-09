# Changelog

All notable changes to Karuna AI OS are documented in this file.

## [1.0.0] - 2026-07-09

### Added

- FastAPI backend foundation with application factory, lifespan management,
  middleware, dependencies, exception handlers, health endpoints, and version
  metadata.
- Versioned REST API under `/api/v1`.
- Agent endpoints for listing, inspecting, and running supported framework
  agents.
- Workflow endpoint for executing the supported sequential LangGraph workflow.
- Document endpoints for local document create, read, list, and delete flows.
- Provider-agnostic LLM abstraction with Groq and Google Gemini providers.
- Dynamic provider and model routing through environment configuration.
- Local filesystem document storage with JSON metadata.
- Reusable agent framework with research, nutrition, content, and review agents.
- LangGraph workflow builder, state, validation, nodes, and execution interface.
- Structured JSON logging and centralized shared exception handling.
- Automated pytest suite covering configuration, providers, storage, agents,
  workflows, APIs, and import smoke checks.
- Release documentation, setup guide, architecture guide, contribution guide,
  and release notes.

### Changed

- Package metadata updated for Version 1.0.0 release readiness.
- Documentation updated from phase-foundation wording to implemented Version 1.0
  behavior.
- Pytest configuration disables cache writes for deterministic local runs.
- FastAPI request validation handler now uses the non-deprecated 422 status
  constant.

### Security

- API error responses avoid stack trace exposure.
- Document storage validates filenames, IDs, content, metadata, and storage
  paths.
- Environment secrets are not committed; `.env.example` documents required
  variables.
