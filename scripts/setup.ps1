Write-Host "Setting up fin-copilot-mcp virtual environment for PowerShell..." -ForegroundColor Green

if (-not (Test-Path -Path ".venv")) {
    python -m venv .venv
    Write-Host "Created .venv virtual environment." -ForegroundColor Green
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

Write-Host "Setup completed successfully! Activate environment using: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan