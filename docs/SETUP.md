# Setup Guide

This guide describes how to install, configure, run, and verify Karuna AI OS
Version 1.0 locally.

## Requirements

- Python 3.12
- PowerShell on Windows for the included helper scripts
- Git for source control workflows

Provider credentials are only required when directly using the LLM provider
layer. The FastAPI health, agent, workflow, and document endpoints can start in
local development without provider credentials.

## Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

Runtime dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

Runtime and development dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The development install includes pytest, pytest-cov, Ruff, and MyPy.

## Environment File

Create a local `.env` file:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`.

```dotenv
APP_NAME=Karuna AI OS
APP_ENV=development
LOG_LEVEL=INFO
HOST=127.0.0.1
PORT=8000
LLM_PROVIDER=groq
LLM_API_KEY=
LLM_MODEL=
DOCUMENT_STORAGE_PATH=./storage/documents
MEMORY_STORAGE_PATH=./storage/memory
```

## Configuration Reference

| Variable | Values | Notes |
| --- | --- | --- |
| `APP_NAME` | non-empty string | Used in health and version metadata. |
| `APP_ENV` | `development`, `test`, `staging`, `production` | Production requires `LLM_API_KEY` and `LLM_MODEL`. |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | Controls structured console logging. |
| `HOST` | hostname or IP | Used by local run commands. |
| `PORT` | 1-65535 | Used by local run commands. |
| `LLM_PROVIDER` | `groq`, `google` | Selects the configured provider. |
| `LLM_API_KEY` | provider API key | Required for provider calls and production settings. |
| `LLM_MODEL` | provider model identifier | Passed through to the provider; not hardcoded. |
| `DOCUMENT_STORAGE_PATH` | filesystem path | Local document storage root. |
| `MEMORY_STORAGE_PATH` | filesystem path | Reserved local memory storage root. |

## Development Script

```powershell
.\scripts\dev.ps1
```

The script creates `.venv` when missing, upgrades pip, installs the project with
development dependencies, and prints the Python version.

## Run the Backend

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health: `http://127.0.0.1:8000/health`
- Readiness: `http://127.0.0.1:8000/health/ready`
- Version: `http://127.0.0.1:8000/version`

## API Smoke Examples

List agents:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/agents" -Method Get
```

Run a single agent:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/agents/research/run" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"input":"Prepare a research outline."}'
```

Run the workflow:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/workflows/run" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"request":"Prepare reviewed wellness content.","metadata":{"source":"setup-guide"}}'
```

Create a document:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/documents" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"filename":"sample.txt","content_base64":"SGVsbG8gS2FydW5h","content_type":"text/plain","metadata":{"source":"setup-guide"}}'
```

## Run Tests

```powershell
python -m pytest
```

Or:

```powershell
.\scripts\test.ps1
```

If local PowerShell execution policy blocks scripts, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test.ps1
```

If your local `.venv` is broken or you are using a managed Python runtime, set
`KARUNA_PYTHON` to a Python 3.12 executable before running the script:

```powershell
$env:KARUNA_PYTHON="C:\Path\To\Python312\python.exe"
powershell -ExecutionPolicy Bypass -File .\scripts\test.ps1
```

## Quality Checks

```powershell
python -m ruff check backend workflows agents config llm memory tests
python -m mypy backend workflows agents config llm memory
python -m mypy tests
python -m compileall -q agents backend config database llm memory tools workflows tests
```

## Troubleshooting

- If `.\scripts\test.ps1` fails because `.venv` is missing, run
  `.\scripts\dev.ps1` first.
- If provider creation fails, confirm `LLM_PROVIDER`, `LLM_API_KEY`, and
  `LLM_MODEL` are set correctly.
- If document creation fails, confirm the filename is safe, content is base64
  encoded when using the API, and `DOCUMENT_STORAGE_PATH` is writable.
