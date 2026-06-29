# llm-wiki-nocode

Unified public skill for:

* bookmark/tab snapshot management
* notebook-to-Markdown conversion
* repo-local nocode LLM wiki workflows
* curated Markdown ToC + wiki synchronization automation

## Install

```bash
npx skills add ai-helpers/ai-skills-curated llm-wiki-nocode --global
```

## Setup

When adopting this skill, create a symlink for snapshot cross-linking:

```bash
cd memory/llm-wiki && ln -s ../kb/snapshots snapshots
```

This enables wiki sources to link to browser tab snapshots and is excluded from wiki indexing.

## Skill file

* `agents/skills/llm-wiki-nocode/SKILL.md`
* assets in `agents/skills/llm-wiki-nocode/assets/knowledge-base/`

## Included automation assets

* `Makefile` targets for conversion, snapshots, ToC sync, and wiki ingest
* `scripts/base_md_sync.py` for idempotent ToC replacement and raw wiki syncing
* `.github/actions/install-project/action.yml` for Python + uv setup in CI
* `.github/workflows/base-md-sync.yml` for automatic post-commit ToC and wiki refreshes
