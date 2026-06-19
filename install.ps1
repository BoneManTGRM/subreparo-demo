$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $RootDir "immune")

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .

Write-Host "SubReparo Immune installed."
Write-Host ""
Write-Host "Run:"
Write-Host "  cd immune"
Write-Host "  .\.venv\Scripts\subreparo-immune.exe scan ."
Write-Host "  .\.venv\Scripts\subreparo-immune.exe inventory create ."
Write-Host "  .\.venv\Scripts\subreparo-immune.exe watch . --once --write-ledger"
