---
name: convert
description: Convert a notebook into Markdown and clone it to the wiki raw area.
usage: /convert <file.ipynb>
trigger: user_args
---

# Notebook Convert Command

Convert a notebook-style file from `notebooks/` into Markdown, then clone the result into both `memory/bookmarks/md/` and `memory/llm-wiki/raw/`.
After the conversion, suggest running `/wiki-ingest` so the new raw document is indexed immediately.

## Workflow

1. Convert the notebook with the same stem name, replacing `.ipynb` with `.md`.
2. Write the Markdown file to `memory/bookmarks/md/`.
3. Clone the same Markdown file into `memory/llm-wiki/raw/`.
4. Refresh the wiki index with `make wiki-ingest`.
5. Use `make convert NOTEBOOK=<path>` or `uv run python scripts/ipynb-to-md.py <path> --name-mode exact --clone-to memory/llm-wiki/raw` followed by `make wiki-ingest`.

## Rules

- Keep the source notebook intact.
- Preserve the notebook filename stem exactly for the shortcut path.
- Use the repo-local bookmark and wiki raw directories only.
