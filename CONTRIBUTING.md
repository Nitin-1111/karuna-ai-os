# Contributing

Thank you for contributing to Karuna AI OS. This project is developed in
explicit phases. Keep changes focused, verified, and aligned with the existing
architecture.

## Development Principles

- Preserve the current architecture.
- Reuse shared configuration, logging, validation, and exceptions.
- Keep API handlers thin.
- Do not hardcode provider names, model names, secrets, or storage paths.
- Do not add future-scope functionality unless the current phase explicitly
  requires it.
- Prefer focused tests over broad, brittle tests.

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

## Verification

Run the full test suite:

```powershell
python -m pytest
```

The PowerShell helper is also available:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test.ps1
```

Set `KARUNA_PYTHON` to a Python 3.12 executable when using a managed runtime
instead of the project `.venv`.

Run quality checks:

```powershell
python -m ruff check backend workflows agents config llm memory tests
python -m mypy backend workflows agents config llm memory
python -m mypy tests
python -m compileall -q agents backend config database llm memory tools workflows tests
```

Run the backend:

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

## Commit Guidelines

- Keep commits scoped to one phase or one focused fix.
- Include tests for code changes.
- Do not commit `.env`, `storage/`, caches, virtual environments, or generated
  build artifacts.
- Use clear commit messages, such as:

```text
Phase 10 - Release Readiness & Documentation
```

## Pull Request Checklist

- Documentation matches implemented behavior.
- `python -m pytest` passes.
- Ruff passes.
- MyPy passes for application code.
- Compile checks pass.
- No unrelated files are changed.
- No secrets are committed.
