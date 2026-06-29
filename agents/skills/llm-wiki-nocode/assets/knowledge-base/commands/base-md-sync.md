---
name: base-md-sync
description: Refresh base Markdown ToCs and sync the downstream wiki raw and index artifacts.
usage: /base-md-sync [memory/kb/md/*.md | memory/kb/md/]
trigger: user_args
---

# Base Markdown Sync Command

Use this command to keep curated base Markdown documents and the repo-local wiki in sync after manual edits.

## Workflow

1. Refresh or replace the document table of contents in each base Markdown file under `memory/kb/md/`.
2. Copy the updated base Markdown files into `memory/llm-wiki/raw/`.
3. Re-index the repo-local wiki with `make wiki-ingest`.
4. Use `make base-md-sync` to process the whole curated Markdown tree, or provide a path list file when only selected files should be synced.

## Rules

- The implementation lives in `scripts/base_md_sync.py` and is exposed through `make base-md-sync`.
- The ToC must be idempotent and replace the previous generated ToC instead of appending duplicates.
- Only curated base Markdown documents under `memory/kb/md/` should be synced.
