---
name: convert
description: Convert a notebook into Markdown and clone it to the wiki raw area.
usage: /convert <file.ipynb>
trigger: user_args
---

# Notebook Convert Command

Convert a notebook-style file from `notebooks/` into Markdown, then run the same downstream sync used for manual Markdown edits.

## Workflow

1. Convert the notebook with the same stem name, replacing `.ipynb` with `.md`.
2. Write the Markdown file to `memory/kb/md/`.
3. Refresh or replace the generated table of contents in the base Markdown document.
4. Clone the same Markdown file into `memory/llm-wiki/raw/`.
5. Refresh the wiki index with `make wiki-ingest`.
6. Use `make convert NOTEBOOK=<path>`, which now reuses `make base-md-sync` for the downstream sync.

## Rules

- Keep the source notebook intact.
- Preserve the notebook filename stem exactly for the shortcut path.
- Use the repo-local bookmark and wiki raw directories only.
