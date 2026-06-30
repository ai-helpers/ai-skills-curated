---
name: rename
description: Rename/move a base markdown document and update all cross-references.
usage: /rename "memory/kb/md/Old Name.md" "memory/kb/md/New Name.md"
trigger: user_message
---

# Rename Command

Rename (or move) a base markdown document and keep all cross-references consistent across the repository.

## Workflow

1. **Identify paths**: Parse `file-path-1` (source) and `file-path-2` (destination) from the user's request.
2. **Run rename**: Execute `make rename SRC="<file-path-1>" DST="<file-path-2>"`, which:
   - Moves the source base MD file to the destination path via `scripts/rename_md.py`.
   - Renames the corresponding raw wiki clone in `memory/llm-wiki/raw/` (if present).
   - Updates all Markdown links referencing the old filename in `memory/kb/md/`.
   - Updates all snapshot header links in `memory/kb/snapshots/` referencing the old filename.
   - Re-runs `make base-md-sync` on the renamed file to refresh the ToC and wiki index.
   - Re-runs `make snapshots-sync` to keep snapshot ↔ base-doc cross-links consistent.
3. **Commit**: Commit and push directly to `main`.

## Example

```bash
make rename \
  SRC="memory/kb/md/50 - Personal and DKT prod.md" \
  DST="memory/kb/md/50 - Personal.md"
```

## Rules

- Always use `make rename SRC=... DST=...` — never a bare `mv` — so cross-references are updated.
- SRC must be an existing base markdown file under `memory/kb/md/`.
- DST must not already exist (the command will error if it does).
- Commit directly to `main` without feature branches.
