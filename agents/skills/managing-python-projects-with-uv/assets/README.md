# my-project

[![CI](https://github.com/<owner>/my-new-python-project/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/my-new-python-project/actions/workflows/ci.yml)

**Note:** Replace `<owner>` with your GitHub username or organization after
pushing the repository.

Initial Python project scaffold managed with `uv`.

## References

### Data Engineering Helpers

* [Data Engineering Helpers - Knowledge Sharing - Python](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/programming/python/) -
  Cheat sheet for how to set up and use Python, especially detailing the
  installation and use of uv

### uv

* [Astral doc - uv](https://docs.astral.sh/uv/)
* [GitHub - Astral - uv](https://github.com/astral-sh/uv)
* [Astral doc - uv installation](https://docs.astral.sh/uv/getting-started/installation/)
* [Astral doc - uv migration guides](https://docs.astral.sh/uv/guides/)

## Quick start

```bash
make init-uv-python PYTHON_VERSION=3.12
make init update
make check
make test
make run
```

## Useful commands

* `make check` — run lint + type checks
* `make format` — fix formatting
* `make test` — run tests with coverage
* `make build` — build source and wheel distributions
* `make publish` — publish distributions to PyPI

## Publishing to PyPI

### Local publish

Set a token first:

```bash
export UV_PUBLISH_TOKEN=<your-pypi-token>
make publish
```

Or configure `~/.pypirc`:

```ini
[distutils]
index-servers =
        pypi
        testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <your-pypi-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-testpypi-token>
```

With a TestPyPI token set as `UV_PUBLISH_TOKEN`, you can publish to TestPyPI:

```bash
make publish-testpypi
```

### GitHub Actions publish

The `publish.yml` workflow uses PyPI trusted publishing (OIDC) on release.

