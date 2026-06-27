# Architecture

Karuna AI OS is planned as a production-oriented Python backend with clear module boundaries. Phase 1 defines only the project foundation and reserves directories for later implementation.

No runtime application, API routes, agents, providers, workflows, storage logic, schemas, or business logic are included in this phase.

## Design Principles

- Keep modules focused and independently understandable.
- Separate backend application concerns from configuration, providers, workflows, tools, memory, and persistence.
- Prefer typed, testable Python modules.
- Add implementation only in the phase where it is explicitly required.

## Project Modules

```text
agents/      Specialist AI agent implementations in future phases.
backend/     FastAPI backend application layer in future phases.
config/      Application configuration in future phases.
database/    Database and persistence code in future phases.
docs/        Project documentation.
llm/         Provider-agnostic LLM abstractions and providers in future phases.
memory/      Memory-related components in future phases.
scripts/     Development and test scripts.
tests/       Automated tests.
tools/       Tool integrations in future phases.
workflows/   LangGraph workflows in future phases.
```

## Phase 1 Scope

Phase 1 includes:

- Project directory layout.
- Python packaging metadata.
- Runtime and development dependency declarations.
- Environment variable template.
- Documentation skeleton.
- Development scripts.
- Empty package markers.

Phase 1 excludes:

- FastAPI app creation.
- Routes or APIs.
- Agent implementations.
- LLM provider implementations.
- LangGraph workflow definitions.
- Storage or memory implementation.
- Configuration classes.
- Business logic.
