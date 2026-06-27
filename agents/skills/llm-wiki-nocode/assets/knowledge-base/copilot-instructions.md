# Copilot instructions

This repository is a private knowledge base for visited web sites and related context. It is organized around Chrome profiles and the topics they track.

## Core conventions

- Keep `notebooks/` intact; they are the historical source format and must not be deleted or rewritten as part of routine updates.
- Use `memory/bookmarks/md/` for the curated Markdown knowledge base migrated from notebooks.
- Use `memory/bookmarks/snapshots/` for dated captures of the current browser tab state, named like `05-main-profile-YYYY-MM-DD.md`.
- Keep reusable context in `memory/` so long-lived knowledge can be referenced without inflating instructions.
- Treat browser-tab snapshots as snapshots, not curated knowledge.
- Preserve source order when converting tab lists unless the user asks otherwise.

## Markdown workflow

- Prefer plain Markdown for new knowledge documents.
- When updating Markdown files, keep a table of contents in sync.
- Use `gh-md-toc` to generate or replace the ToC.
- Batch updates are preferred when the same change applies to many documents.

## Reusable automation

- The `bookmark-manager` skill is the reusable entry point for browser tab lists and bookmark-style documents.
- The `llm-wiki-nocode` skill is the reusable entry point for the repo-local wiki workflow under `memory/llm-wiki/`.
- The `ipynb-to-md` skill is the reusable entry point for converting notebook sources into Markdown under `memory/bookmarks/md/`.
- Use `make convert NOTEBOOK=<path>` for exact-stem notebook conversion that also clones into `memory/llm-wiki/raw/` and refreshes the wiki index; if the raw clone is created separately, follow up with `make wiki-ingest`.
- Future automation should include a small CLI for Markdown ToC updates, a GitHub Actions workflow to run it, a `Makefile`, and Markdown linting for `memory/bookmarks/md/`.

## Notebook conversion

- Convert iPython notebooks from `notebooks/` into Markdown documents under `memory/bookmarks/md/`.
- Keep the original notebooks intact.
- Prefer plain Markdown for durable notebook-derived content.
- Use `uv` with `jupyter nbconvert --to markdown` for the conversion utility, with `make init` creating/updating the uv environment and lockfile.
- Use the exact-stem shortcut when you also need a clone in `memory/llm-wiki/raw/` and an updated wiki index.
- After creating or updating files in `memory/llm-wiki/raw/`, run `make wiki-ingest` so the wiki catalog stays current.

## LLM Wiki

- The repo-local nocode wiki lives under `memory/llm-wiki/`.
- Use the `llm-wiki-nocode` skill as the primary implementation guide for this capability.
- Use the three slash commands: `/wiki-ingest`, `/wiki-query`, and `/wiki-lint`.
- Follow `memory/llm-wiki/wiki/index.md`, `memory/llm-wiki/wiki/log.md`, and the pages under `memory/llm-wiki/wiki/` as the wiki source of truth.
- Use standard GitHub Markdown links (`[]()`) inside wiki pages and generated wiki catalogs.
- Keep all wiki artifacts inside `memory/llm-wiki/`.

## Journal reporting

The repository keeps a regular activity journal under `memory/journal/`. Use it to record session activity consistently.

At the end of every session, or when the user asks to report the session activity:

1. Update `memory/` files as needed.
2. Add a journal entry under `memory/journal/YYYY/YYYY-MM/YYYY-MM-DD/<member>-<topic>-<HH-mm>.md`.
3. Update or create `memory/journal/YYYY/YYYY-MM/YYYY-MM-DD/summary.md` with a row pointing to the new entry.
4. Commit and push directly to `main`.

Do not use `sessions/` for activity logs. The `sessions/` directory is outside `memory/` and is not the canonical place for session records.

If the user pivots mid-flow, pause the reporting sequence and execute the new request first.

## Chrome tab access

- For implementation details and current operational guidance, use `memory/guides/chrome-browser-tab-fetcher-reader.md`.
- **macOS AppleScript method (recommended on Mac):** use `make tabs-sync NOTEBOOK="<notebook_path>"` (which calls `scripts/chrome_tabs_sync.py`) to fetch open Chrome tabs quickly with no remote-debugging setup.
- **Cross-platform MCP method:** use `chrome-devtools-mcp` only when remote-debugging is explicitly enabled for the target browser instance/profile.
- For the MCP method, follow https://developer.chrome.com/docs/devtools/agents/use-cases/auto-connect and enable **Allow remote debugging for this browser instance** at `chrome://inspect/#remote-debugging`.
- MCP-based tab inspection can consume significant resources on both terminal and browser; close other applications before large tab reads when possible.

## Repository workflow

- All changes in this repository are direct-to-main: commit and push without feature branches or PRs.
- When adding new knowledge, prefer the smallest durable representation that keeps the repository useful over time.
