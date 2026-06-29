---
name: llm-wiki-nocode
description: Unified skill for bookmark snapshots, notebook-to-Markdown conversion, and repo-local LLM wiki maintenance workflows.
license: MIT
compatibility: "Requires: make, Python 3, uv, jupyter nbconvert"
metadata:
  author: ai-helpers
  version: "0.1.0"
  keywords:
    - bookmarks
    - chrome-tabs
    - notebook-conversion
    - markdown
    - llm-wiki
---

# LLM Wiki Nocode (Unified)

## Overview

Use this unified skill to manage the end-to-end knowledge workflow:

* Browser tab capture and snapshotting
* Notebook (`.ipynb`) to Markdown conversion
* Repo-local nocode wiki ingest/query/lint workflows

## Scope and conventions

* Keep `notebooks/` intact; do not rewrite notebook sources during routine updates.
* Write curated knowledge under `memory/kb/md/`.
* Write dated tab snapshots under `memory/kb/snapshots/` as `*-YYYY-MM-DD.md`.
* Keep reusable context under `memory/`.
* Preserve source order unless the user explicitly asks for sorting/grouping.
* Prefer plain Markdown and keep table of contents sections synchronized with `make base-md-sync`.

## Browser tab capture

### Preferred method on macOS

Use AppleScript-backed capture through:

```bash
make tabs-sync NOTEBOOK="<notebook_path>"
```

This uses `scripts/chrome_tabs_sync.py` and avoids remote-debugging setup.

### Cross-platform alternative

Use `chrome-devtools-mcp` only when remote debugging is explicitly enabled for the target browser instance/profile (`chrome://inspect/#remote-debugging`).

## Notebook conversion

Use:

```bash
make init
make convert NOTEBOOK=<path-to-ipynb>
```

This keeps exact filename stem naming, writes to `memory/kb/md/`, refreshes the generated table of contents, clones to `memory/llm-wiki/raw/`, and refreshes the wiki index.

For separate raw cloning flows, run:

```bash
make wiki-ingest
```

For manual edits to curated Markdown, run:

```bash
make base-md-sync
```

## Wiki workflow

Use the slash-command workflows:

* `/wiki-ingest` — ingest documents and refresh wiki artifacts
* `/wiki-query` — answer with retrieval from `memory/llm-wiki/wiki/` only
* `/wiki-lint` — run deterministic + semantic wiki checks

Keep all wiki artifacts under `memory/llm-wiki/` and use standard GitHub Markdown links (`[]()`), not wiki-link syntax.

## Journal/reporting convention

When a repository follows session journaling, record activity under `memory/journal/YYYY/YYYY-MM/YYYY-MM-DD/` with:

* one entry file (`<member>-<topic>-<HH-mm>.md`)
* a `summary.md` row for that entry

## Assets

This skill includes reusable assets from a production knowledge-base repository:

* `assets/knowledge-base/Makefile`
* `assets/knowledge-base/.github/actions/install-project/action.yml`
* `assets/knowledge-base/.github/workflows/base-md-sync.yml`
* `assets/knowledge-base/scripts/`
* `assets/knowledge-base/commands/` — slash commands: `base-md-sync`, `convert`, `fix-home`, `rename`, `snapshots-sync`, `tabs-sync`, `wiki-ingest`, `wiki-lint`, `wiki-query`
* `assets/knowledge-base/copilot-instructions.md`

Use these as reference or copy-adapt templates for repositories implementing the same workflow.
