#!/usr/bin/env bash
set -e

echo "Setting up fin-copilot-mcp virtual environment for Bash..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Created .venv virtual environment."
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"

echo "Setup completed successfully! Activate environment using: source .venv/bin/activate"