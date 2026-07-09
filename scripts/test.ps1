Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$Python = if ($env:KARUNA_PYTHON) {
    $env:KARUNA_PYTHON
} else {
    Join-Path $ProjectRoot ".venv\Scripts\python.exe"
}

if (-not $env:KARUNA_PYTHON -and -not (Test-Path $Python)) {
    throw "Virtual environment not found. Run .\scripts\dev.ps1 first."
}

& $Python --version
if ($LASTEXITCODE -ne 0) {
    throw "Configured Python is not runnable. Run .\scripts\dev.ps1 or set KARUNA_PYTHON to a valid Python 3.12 executable."
}

$PytestTemp = Join-Path $ProjectRoot ".pytest-tmp"
if (-not (Test-Path $PytestTemp)) {
    New-Item -ItemType Directory -Path $PytestTemp | Out-Null
}

$env:TEMP = $PytestTemp
$env:TMP = $PytestTemp

& $Python -m pytest
$PytestExitCode = $LASTEXITCODE
if ($PytestExitCode -ne 0) {
    throw "pytest failed with exit code $PytestExitCode."
}
