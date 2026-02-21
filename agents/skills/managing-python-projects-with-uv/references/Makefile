UV ?= uv

.PHONY: help init update install test lint format clean

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

init: ## uv - Creates/updates the uv.lock file
	@uv lock
	@uv export --format requirements.txt > requirements.txt

update: ## uv - Upgrades the uv.lock file
	@uv sync
	@uv export --format requirements.txt > requirements.txt

install: ## uv - Install dependencies from lock file
	@$(UV) sync

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
	@rm -rf .venv
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .mypy_cache
	@rm -rf .ruff_cache
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

build: ## Build distribution packages
	@$(UV) build

publish: ## Publish to PyPI
	@$(UV) publish

run: ## Run the application
	@$(UV) run python -m my_project
