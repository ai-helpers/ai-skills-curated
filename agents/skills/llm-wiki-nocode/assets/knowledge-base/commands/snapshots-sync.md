---
name: snapshots-sync
description: Sync snapshot markdown files with their base bookmark markdown documents.
usage: /snapshots-sync
trigger: user_message
---

# Snapshots Sync Command

Use this command to synchronize browser snapshot documents under `memory/kb/snapshots/` with curated base documents under `memory/kb/md/`.

## Workflow

1. Scan all snapshot files matching `memory/kb/snapshots/*-YYYY-MM-DD.md`.
2. Match each snapshot to its base markdown document in `memory/kb/md/` using shared normalized basename.
3. Update the snapshot document with a header link to its base markdown document.
4. Update the base markdown document with a `## Snapshots` section and `Timestamp | Snapshot` table.
5. Add one table row per snapshot if missing.

## Command

```bash
make snapshots-sync
```

## Rules

- Keep all links as standard Markdown links.
- Do not remove existing content from base or snapshot documents.
- Add missing snapshot sections/tables only when absent.
- Do not duplicate snapshot rows.
