Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

& $Python -m pip install --upgrade pip
& $Python -m pip install -e ".[dev]"
& $Python --version

Write-Host "Karuna AI OS Phase 1 development environment is ready."
Write-Host "No application server is started in Phase 1."
