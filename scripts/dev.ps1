Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

& $Python --version
if ($LASTEXITCODE -ne 0) {
    throw "Virtual environment Python is not runnable. Remove .venv and rerun .\scripts\dev.ps1 with Python 3.12 available."
}

& $Python -m pip install --upgrade pip
& $Python -m pip install -e ".[dev]"
& $Python --version

Write-Host "Karuna AI OS development environment is ready."
Write-Host "Start the API with: python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000"
