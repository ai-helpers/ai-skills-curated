---
name: wiki-query
description: Query the repo-local wiki knowledge base.
usage: /wiki-query <question>
trigger: user_args
---

# Wiki Query Command

Answer using only `memory/llm-wiki/wiki/` content.

## Workflow

1. Read `memory/llm-wiki/wiki/index.md`.
2. Follow relevant Markdown links one page at a time.
3. Read at least 3 pages and no more than 8.
4. Save the answer under `memory/llm-wiki/questions_pending/`.
5. Append a log entry to `memory/llm-wiki/wiki/log.md`.

## Rules

- Retrieval-only: do not use training data.
- Answer in the user’s language.
- Cite every claim with standard Markdown links to the corresponding wiki pages.
- Preserve code blocks verbatim.
