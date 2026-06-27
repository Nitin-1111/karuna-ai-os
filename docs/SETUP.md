# Setup

This document describes the Phase 1 setup process for Karuna AI OS.

## Requirements

- Python 3.12
- PowerShell

## Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

Install runtime dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

Install runtime and development dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Configure Environment Variables

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Supported `LLM_PROVIDER` values are:

- `groq`
- `google`

Fill in `LLM_API_KEY`, `LLM_MODEL`, and storage paths according to your local setup.

## Development Script

Run the Phase 1 development bootstrap:

```powershell
.\scripts\dev.ps1
```

This creates `.venv` if needed, installs development dependencies, and verifies the Python interpreter.

## Test Script

Run tests with:

```powershell
.\scripts\test.ps1
```

Phase 1 contains no business logic. Test coverage will be added in later phases as implementation is introduced.
