# managing-python-projects-with-uv — Python Projects with uv Skill

## What this skill does

Helps you initialize, manage, and operate Python projects using
[uv](https://github.com/astral-sh/uv), an extremely fast Python package and project
manager written in Rust — dependencies, virtual environments, running scripts,
testing, and publishing packages to PyPI.

## When to use it

- You are setting up a new Python project from scratch.
- You are converting an existing project to use uv.
- You need to manage dependencies (add, remove, update packages) or virtual
  environments.
- You are running Python scripts/applications in a uv-managed project.
- You are building distributions for PyPI or checking which Python version/packages
  are installed.

## Quick start (for humans)

1. Install this skill, either globally or locally:

   ```bash
   # Globally
   npx skills add https://github.com/ai-helpers/ai-skills-curated \
       --skill managing-python-projects-with-uv -g

   # Or locally, in a specific project
   npx skills add https://github.com/ai-helpers/ai-skills-curated \
       --skill managing-python-projects-with-uv
   ```

2. Create an empty project directory and open it in your editor:

   ```bash
   mkdir -p ~/tmp/my-new-python-project && cd ~/tmp/my-new-python-project
   git init
   code .
   ```

3. Prompt the agent, for example:

   > With the managing-python-projects-with-uv skill, create a Python project, with
   > testing, CI/CD and publishing capability on PyPI.

4. The agent scaffolds `pyproject.toml`, a `Makefile`, `src/<project>/`, `tests/`,
   `.github/workflows/{ci,publish}.yml`, and a `.gitignore`, using the
   [`assets/`](assets/) templates as a base, then walks you through `make init`,
   `make run`, `make test`, `make build`, and `make publish`.

## What's inside

- **Ready-to-copy asset templates** in [`assets/`](assets/):
  [`Makefile`](assets/Makefile), [`pyproject.toml`](assets/pyproject.toml),
  [`README.md`](assets/README.md), [`main.py`](assets/main.py),
  [`test_main.py`](assets/test_main.py), [`.gitignore`](assets/.gitignore),
  [`ci.yml`](assets/ci.yml), and [`publish.yml`](assets/publish.yml).
- **Quick reference** — the full command sequence to bootstrap a project (init,
  install a specific Python version, run, build, check, test, publish).
- **Context on uv vs. PyEnv** — when uv's standalone-script mode
  (`#!/usr/bin/env -S uv`) is a good fit versus the more established PyEnv workflow.

## Related resources

- [Skills.sh listing](https://skills.sh/ai-helpers/ai-skills-curated/managing-python-projects-with-uv)
  for this skill.
- [Data Engineering Helpers — Python cheat sheet](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/programming/python/)
- [uv documentation](https://docs.astral.sh/uv/) and
  [migration guides](https://docs.astral.sh/uv/guides/)
- [uv on GitHub](https://github.com/astral-sh/uv)
