@echo off
echo Setting up fin-copilot-mcp virtual environment for Windows Command Prompt...

if not exist ".venv" (
    python -m venv .venv
    echo Created .venv virtual environment.
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

echo Setup completed successfully! Activate environment using: .venv\Scripts\activate.bat