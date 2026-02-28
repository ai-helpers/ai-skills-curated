
PYTHON_VERSION := 3.12
UV ?= uv

.PHONY: help init update install test lint format clean

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

git-add: ## Git stage the main files
	@git add .gitignore Makefile README.md pyproject.toml src/ tests/ uv.lock

init-uv-python: ## Install Python $(PYTHON_VERSION) if necessary
	@$(UV) python install $(PYTHON_VERSION)

init: ## uv - Creates/updates the uv.lock file
	@$(UV) lock
	@$(UV) export --format requirements.txt > requirements.txt

update: ## uv - Upgrades the uv.lock file
	@$(UV) sync
	@$(UV) export --format requirements.txt > requirements.txt

build: ## Build the software artifact (wheel)
	@$(UV) build

test: ## Run tests with pytest
	@$(UV) run pytest

test-cov: ## Run tests with coverage report
	@$(UV) run pytest --cov=src --cov-report=html --cov-report=term

lint: ## Run ruff linter
	@$(UV) run ruff check .

format: ## Format code with ruff
	@$(UV) run ruff format .

type-check: ## Run mypy type checker
	@$(UV) run mypy src/

check: lint type-check ## Run all checks (lint + type-check)

clean: ## Remove build artifacts and cache files
	@rm -rf .venv dist/ build/ *.egg-info .pytest_cache .coverage htmlcov/ .mypy_cache .ruff_cache
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

publish: ## Publish to PyPI
	@$(UV) publish

publish-testpypi: ## Publish built artifacts to TestPyPI
	@$(UV) publish --publish-url https://test.pypi.org/legacy/

run: ## Run the application
	@$(UV) run src/my_project/main.py

