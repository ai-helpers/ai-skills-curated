---
name: wiki-lint
description: Run deterministic and semantic checks on the repo-local wiki.
usage: /wiki-lint
trigger: no_args
---

# Wiki Lint Command

Run health checks on `memory/llm-wiki/` and save the report under `memory/llm-wiki/lint_pending/`.

## Workflow

1. Check broken Markdown links, orphan pages, and frontmatter.
2. Review semantic issues like contradictions and stale claims.
3. Append a log entry to `memory/llm-wiki/wiki/log.md`.

## Rules

- Use deterministic checks first.
- Then perform semantic review.
- Do not modify wiki pages during linting.
