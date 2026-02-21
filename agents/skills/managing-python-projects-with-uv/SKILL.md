---
name: managing-python-projects-with-uv
description: Use when working with Python projects that use uv for dependency management, virtual environments, project initialization, or package publishing. Covers setup, workflows, and best practices for uv-based projects.
metadata:
  author: denis.arnaud_fedora@m4x.org
---

# Managing Python Projects with uv

## Overview

This skill helps you work with Python projects managed by [uv](https://github.com/astral-sh/uv), an extremely fast Python package and project manager written in Rust. Use this skill for:

- Initializing new Python projects
- Managing dependencies and virtual environments
- Running scripts and applications
- Building and publishing packages
- Optimizing Python workflows with uv's speed

## When to Use This Skill

Use this skill when:

- Setting up a new Python project from scratch
- Converting an existing project to use uv
- Managing dependencies (adding, removing, updating packages)
- Working with virtual environments
- Running Python scripts or applications in a uv project
- Building distributions for PyPI
- The user asks about uv commands or workflows
- You need to check which Python version or packages are installed

## Additional Resources

- [Makefile](references/Makefile) — Example of Makefile with relevant targets
- [pyproject.toml](references/pyproject.toml) — Example of Python project file, compatible with uv
- [.gitignore](references/.gitignore) - Example of `.gitignore` file, Git-ignoring Python-/uv-related files

## Quick Reference

```bash
# Initialize a new project
uv init my-project
uv init --package my-package  # For a library/package

# Manage dependencies
uv add requests pandas          # Add packages
uv add --dev pytest ruff        # Add dev dependencies
uv remove requests              # Remove a package
uv sync                         # Install/sync all dependencies

# Run commands in the project environment
uv run python script.py         # Run a Python script
uv run pytest                   # Run tests
uv run --with httpx -- python   # Run with ad-hoc dependency

# Virtual environment management
uv venv                         # Create virtual environment
uv venv .venv --python 3.11     # Specify Python version
source .venv/bin/activate       # Activate (Unix/macOS)

# Package management
uv pip install requests         # Install in current environment
uv pip list                     # List installed packages
uv pip freeze                   # Output installed packages

# Build and publish
uv build                        # Build package distributions
uv publish                      # Publish to PyPI

# Python version management
uv python list                  # List available Python versions
uv python install 3.12          # Install a Python version
uv python pin 3.11              # Pin project to Python 3.11
```

## Project Structure

A typical uv project structure:

```
my-project/
├── pyproject.toml          # Project metadata and dependencies
├── uv.lock                 # Locked dependencies (commit this!)
├── .python-version         # Pinned Python version (optional)
├── README.md
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
└── .venv/                  # Virtual environment (don't commit)
```

## Key Workflows

### 1. Creating a New Project

**Application project:**
```bash
uv init my-app
cd my-app
uv add requests httpx
uv run python -m my_app
```

**Library/package project:**
```bash
uv init --package my-lib
cd my-lib
uv add --dev pytest ruff mypy
uv run pytest
```

### 2. Working with Existing Projects

```bash
# Clone and set up
git clone <repo-url>
cd <repo>

# Sync dependencies (reads pyproject.toml and uv.lock)
uv sync

# Run the application
uv run python -m my_app
```

### 3. Dependency Management

```bash
# Add production dependencies
uv add pandas numpy scipy

# Add with version constraints
uv add "django>=4.0,<5.0"

# Add development dependencies
uv add --dev pytest pytest-cov black ruff mypy

# Add optional/extra dependencies
uv add --optional docs sphinx sphinx-rtd-theme

# Update all dependencies
uv lock --upgrade

# Update specific package
uv lock --upgrade-package requests

# Remove a dependency
uv remove requests
```

### 4. Running Scripts and Applications

```bash
# Run a Python module
uv run python -m my_package

# Run a script
uv run python scripts/process_data.py

# Run with ad-hoc dependencies (no install needed)
uv run --with pandas --with matplotlib -- python analyze.py

# Run installed CLI tools
uv run pytest
uv run ruff check .
uv run mypy src/
```

### 5. Python Version Management

```bash
# List available Python versions
uv python list

# Install a specific version
uv python install 3.12

# Pin project to a version
uv python pin 3.11

# Use specific version for venv
uv venv --python 3.11
```

### 6. Building and Publishing

```bash
# Build wheel and sdist
uv build

# Publish to PyPI (requires PyPI token)
uv publish

# Publish to test PyPI
uv publish --publish-url https://test.pypi.org/legacy/
```

## Common Tasks

### Converting from pip/pip-tools

If you have `requirements.txt`:
```bash
uv init
uv add $(cat requirements.txt)
```

If you have `requirements-dev.txt`:
```bash
uv add --dev $(cat requirements-dev.txt)
```

### Converting from Poetry

```bash
# Poetry uses pyproject.toml, so you can:
uv sync  # This will read Poetry's pyproject.toml

# Or initialize fresh and add dependencies
uv init
# Manually add dependencies from poetry's pyproject.toml
```

### Checking Installation and Environment

```bash
# Check uv version
uv --version

# Show project info
uv pip list

# Show dependency tree
uv tree

# Verify lock file is up to date
uv lock --check
```

### Working with Multiple Python Versions

```bash
# Create venv with specific Python
uv venv .venv-311 --python 3.11
uv venv .venv-312 --python 3.12

# Test against multiple versions
uv run --python 3.11 pytest
uv run --python 3.12 pytest
```

## pyproject.toml Configuration

Key sections in a uv-managed `pyproject.toml`:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A sample project"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "pandas>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]

[tool.ruff]
line-length = 100
```

## Best Practices

1. **Always commit `uv.lock`** - This ensures reproducible installations across environments
2. **Use `uv sync`** instead of `uv pip install` for project dependencies
3. **Use `uv run`** to execute commands in the project environment
4. **Pin Python version** with `uv python pin` or `.python-version` file
5. **Separate dev dependencies** using `--dev` flag or `tool.uv.dev-dependencies`
6. **Use version constraints** in `pyproject.toml` for stability
7. **Regularly update** with `uv lock --upgrade` and test
8. **Use `--with` for one-off dependencies** instead of installing them

## Troubleshooting

### uv not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Or with Homebrew (macOS)
brew install uv
```

### Lock file out of sync
```bash
# Update lock file
uv lock

# Force sync even if lock is outdated
uv sync --inexact
```

### Python version not found
```bash
# Install the required Python version
uv python install 3.12

# Or specify a different version
uv venv --python 3.11
```

### Dependency conflicts
```bash
# Show dependency tree to identify conflicts
uv tree

# Try updating conflicting packages
uv lock --upgrade-package <package-name>
```

### Virtual environment issues
```bash
# Remove and recreate
rm -rf .venv
uv venv

# Sync dependencies again
uv sync
```

## Integration with Other Tools

### With Ruff (linting/formatting)
```bash
uv add --dev ruff
uv run ruff check .
uv run ruff format .
```

### With pytest (testing)
```bash
uv add --dev pytest pytest-cov
uv run pytest
uv run pytest --cov=src/
```

### With mypy (type checking)
```bash
uv add --dev mypy
uv run mypy src/
```

### With pre-commit
```bash
uv add --dev pre-commit
uv run pre-commit install
uv run pre-commit run --all-files
```

## Differences from Other Tools

| Feature | uv | pip | Poetry | PDM |
|---------|-----|-----|--------|-----|
| Speed | ⚡️ Fastest | Slow | Medium | Fast |
| Lock file | ✅ uv.lock | ❌ | ✅ poetry.lock | ✅ pdm.lock |
| Python install | ✅ | ❌ | ❌ | ❌ |
| Build backend | 🏗️ Any | N/A | ✅ | ✅ |
| Workspace support | ✅ | ❌ | ✅ | ✅ |

## Resources

- Documentation: https://docs.astral.sh/uv/
- GitHub: https://github.com/astral-sh/uv
- Installation: https://docs.astral.sh/uv/getting-started/installation/
- Migration guides: https://docs.astral.sh/uv/guides/
