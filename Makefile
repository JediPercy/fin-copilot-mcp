.PHONY: install lint format test dev-mcp clean

install:
	uv pip install -e ".[dev]"
	pre-commit install

lint:
	ruff check src/ tests/
	mypy src/

format:
	ruff format src/ tests/

test:
	pytest tests/unit tests/integration --cov=src/fin_copilot --cov-report=term-missing

eval:
	pytest tests/evals/

run-orchestrator:
	python -m fin_copilot.agents.orchestrator

clean:
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info