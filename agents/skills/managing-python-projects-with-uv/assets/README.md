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
make init
make update
make run
```

## Useful commands

- `make test`
- `make lint`
- `make format`
- `make type-check`
- `make build`
