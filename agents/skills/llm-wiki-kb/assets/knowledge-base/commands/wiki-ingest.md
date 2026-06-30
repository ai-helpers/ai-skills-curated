---
name: wiki-ingest
description: Ingest raw documents into the repo-local wiki workspace.
usage: /wiki-ingest [raw/file.md | scan | --RESET-ALL]
trigger: user_args
---

# Wiki Ingest Command

Use this command to ingest raw documents, approved questions, and approved lint fixes into `memory/llm-wiki/`.

## Workflow

1. Scan `memory/llm-wiki/raw/` for Markdown files.
2. Create or update source pages under `memory/llm-wiki/wiki/sources/`.
3. Refresh `memory/llm-wiki/wiki/index.md`, `memory/llm-wiki/README.md`, and append to `memory/llm-wiki/wiki/log.md`.
4. The repository implementation lives in `scripts/wiki-ingest.py` and is exposed through `make wiki-ingest`.

## Rules

- Write all content in English.
- Preserve code blocks verbatim.
- Use standard GitHub Markdown links (`[]()`) for wiki navigation and citations.
- Store pending outputs under `memory/llm-wiki/questions_pending/` and `memory/llm-wiki/lint_pending/`.
- Use `--RESET-ALL` only when explicitly requested.
