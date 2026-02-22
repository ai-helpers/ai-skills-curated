---
name: managing-python-projects-with-uv
description: Use when working with Python projects that use uv for dependency management, virtual environments, project initialization, or package publishing. Covers setup, workflows, and best practices for uv-based projects.
license: MIT
compatibility: Requires uv
metadata:
  author: ai-helpers
  version: "0.0.6"
---

# Managing Python Projects with uv

## Overview

This skill helps you work with Python projects managed by
[uv](https://github.com/astral-sh/uv), an extremely fast Python package and project
manager written in Rust. Use this skill for:

* Initializing new Python projects
* Managing dependencies and virtual environments
* Running scripts and applications
* Building and publishing packages
* Optimizing Python workflows with uv's speed

* There are several ways to install and use Python and the ecosystem built
  upon Python.
  * [PyEnv](https://github.com/pyenv/pyenv) has been available
  for a while and is now mature enough to be widely used by the majority of
  users. PyEnv is the solution be default used in
  [these cheat sheets](https://github.com/data-engineering-helpers/ks-cheat-sheets)
  * [uv](https://github.com/astral-sh/uv) is the new, shiny, kid on the block,
  and may appeal to those seeking to be on the edge of technological trends.
  There is at least a very specific use case where uv proves useful, it is
  to power standalone Python scripts: it is enough to add the magic
  `#!/usr/bin/env -S uv` command as the first line of any Python script,
  and that latter becomes standalone, self-served on any platform, any where,
  whithout requiring the users to install anything like dependencies (apart
  uv itself, obviously)

## When to Use This Skill

Use this skill when:

* Setting up a new Python project from scratch
* Converting an existing project to use uv
* Managing dependencies (adding, removing, updating packages)
* Working with virtual environments
* Running Python scripts or applications in a uv project
* Building distributions for PyPI
* The user asks about uv commands or workflows
* You need to check which Python version or packages are installed

## Additional Resources

### Assets for this skill

* [Makefile](assets/Makefile) — Example of Makefile excerpts with relevant targets
* [pyproject.toml](assets/pyproject.toml) — Example of Python project file,
  compatible with uv
* [README.md](assets/README.md) — Example of relevant excerpts in the README file
* [main.py](assets/main.py) — Example of working standalone main.py file, to be
  copied in the `src/<project>/` directory (if not existing, be sure to create
  that directory, adapting to your project)
* [`test_main.py`](assets/test_main.py) — Example of working `test_main.py`
  Python test script, to be copied in the `tests/` directory (if not existing,
  be sure to create that directory)
* [.gitignore](assets/.gitignore) - Example of relevant excerpts in the `.gitignore`
  file, Git-ignoring Python-/uv-related files
* [ci.yml](assets/ci.yml) - Example of relevant excerpts in the `ci.yml` CI/CD
  (GitHub Actions) dev pipeline, to be copied into the `.github/workflows/`
  directory (if not existing, be sure to create that directory)
* [publish.yml](assets/publish.yml) - Example of relevant excerpts in the
  `publish.yml` CI/CD (GitHub Actions) release pipeline, to be copied into the
  `.github/workflows/` directory

### Data Engineering Helpers

* [Data Engineering Helpers - Knowledge Sharing - Python](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/programming/python/) -
  Cheat sheet for how to set up and use Python, especially detailing the
  installation and use of uv

### uv

* [Astral doc - uv](https://docs.astral.sh/uv/)
* [GitHub - Astral - uv](https://github.com/astral-sh/uv)
* [Astral doc - uv installation](https://docs.astral.sh/uv/getting-started/installation/)
* [Astral doc - uv migration guides](https://docs.astral.sh/uv/guides/)

## Quick Reference

* Integrate the sample files into your project directory (if you had not any such
  file, just copy them; otherwise, merge their content within your corresponding
  files):
  * [Makefile](assets/Makefile)
  * [pyproject.toml](assets/pyproject.toml)
  * [README.md](assets/README.md)
  * [main.py](assets/main.py)
  * [`test_main.py`](assets/test_main.py)
  * [.gitignore](assets/.gitignore)
  * [ci.yml](assets/ci.yml)
  * [publish.yml](assets/publish.yml)

### Quick start

* If not already done so, install a specific Python version for uv:

```bash
make init-uv-python PYTHON_VERSION=3.13
```

* Clean all previous work:

```bash
make clean
```

* Note that uv is expecting that the Python source code be in the
  `src/<project>/` sub-directory
  * The `<project>` name is specified in the [pyproject.toml](assets/pyproject.toml)
  Python project specification file. Change it to reflect your project name
  * For the next commands to work, that source directory should at least contain
  a Python script. If need, copy the [main.py](assets/main.py) into the
  `src/<project>/` directory:

```bash
mkdir -p src/<project> tests .github/workflows
cp assets/main.py src/<project>/
cp assets/test_main.py tests/
cp assets/*.yml .github/workflows/
git add src/<project>/main.py tests/test_main.py .github/workflows/*.yml
```

* Initialize the Python environment with uv:

```bash
make init update
```

* Run the Python script:

```bash
make run
```

### Useful commands

* Build the artifact (Python wheel):

```bash
make build
```

* Check (with the linter and type checkers) that there is no Python issue:

```bash
make check
```

* Test the Python package:

```bash
make test
```

* Publish the artifact (Python wheel):

```bash
make publish
```
