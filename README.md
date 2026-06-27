# Karuna AI OS

Karuna AI OS is a production-oriented AI operating system backend planned around FastAPI, LangGraph orchestration, provider-agnostic language model access, specialist agents, local document storage, APIs, testing, and documentation.

This repository currently contains Phase 1 only: the project foundation. It establishes the folder structure, dependency management, development scripts, environment template, and documentation skeleton needed for later implementation phases.

## Features

- Python 3.12 project configuration.
- Installable package foundation with explicit dependencies.
- Development and test dependency groups.
- Environment variable template for local setup.
- PowerShell scripts for developer bootstrap and test execution.
- Documentation skeleton for architecture, setup, and roadmap.
- Empty package directories reserved for later implementation phases.

No application runtime, API routes, agents, providers, workflows, models, storage logic, or business logic are implemented in Phase 1.

## Architecture Summary

Karuna AI OS will be organized as a modular backend. The Phase 1 layout reserves top-level modules for backend application code, configuration, database access, language model integrations, memory, tools, agents, and workflows.

Future phases will fill these modules while preserving separation of concerns:

- `backend/` will contain the backend application layer.
- `config/` will contain application configuration.
- `database/` will contain database-related code.
- `llm/` will contain provider-agnostic LLM integration.
- `agents/` will contain specialist AI agents.
- `memory/` will contain memory-related components.
- `tools/` will contain tool integrations.
- `workflows/` will contain orchestration workflows.

## Folder Structure

```text
karuna-ai-os/
├── agents/
├── backend/
├── config/
├── database/
├── docs/
├── llm/
├── memory/
├── scripts/
├── tests/
├── tools/
├── workflows/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

## Setup

Prerequisites:

- Python 3.12
- PowerShell

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project with development dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Update `.env` with provider and storage values appropriate for your local environment.

## Installation

For application dependencies only:

```powershell
python -m pip install -e .
```

For development:

```powershell
python -m pip install -e ".[dev]"
```

## Running Locally

Phase 1 does not include a FastAPI app or runtime entry point. Later phases will add the backend application and local run command.

For now, use the development script to validate that the Python environment is ready:

```powershell
.\scripts\dev.ps1
```

## Testing

Run the test suite with:

```powershell
.\scripts\test.ps1
```

Phase 1 contains no business logic tests yet. The command is included so the testing workflow is ready for later phases.

## Future Phases

Future implementation phases will add:

- FastAPI backend application.
- LangGraph orchestration.
- Provider-agnostic LLM layer.
- Groq provider integration.
- Google Gemini provider integration.
- Specialist AI agents.
- Local document storage.
- API endpoints.
- Automated tests.
- Expanded documentation.

Phase 1 stops at the project foundation.
