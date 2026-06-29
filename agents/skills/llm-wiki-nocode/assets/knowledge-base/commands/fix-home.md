---
name: fix-home
description: Redirect a local KB base document to its canonical home repository.
usage: /fix-home "memory/kb/md/File.md" "owner/repo-or-repo-name"
trigger: user_message
---

# Fix Home Command

Use this command to mark a local base Markdown document as a redirect to its canonical home in another repository.

## Workflow

1. Parse source file path (`file-path-1.md`) and new home repo (`new-git-repo`) from user input.
2. Run:
   ```bash
   make fix-home SRC="<file-path-1.md>" HOME_REPO="<new-git-repo>"
   ```
   Optional export for home repo content (without Snapshots):
   ```bash
   make fix-home \
     SRC="<file-path-1.md>" \
     HOME_REPO="<new-git-repo>" \
     HOME_EXPORT="<home-repo-local-path>/<file-path-1.md>"
   ```
3. The command:
   - rewrites local source document to a canonical redirect stub,
   - keeps the same file path in the home repository (canonical path = local path),
   - runs `base-md-sync` and `snapshots-sync` so repo artifacts stay aligned.
4. Commit/push the exported canonical home file in the home repository, then keep this repo as redirect-only.

## Example

```bash
make fix-home \
  SRC="memory/kb/md/494 - DKT - Kill Legacy.md" \
  HOME_REPO="dktunited/ai-t2-data-staff"
```

## Rules

- Do not use `mv` for this operation.
- Source file must be under `memory/kb/md/`.
- Canonical home path remains exactly the same relative path as the source.
- Canonical home documents must not keep the `Snapshots` section (snapshots are personal/private).
- Commit directly to `main`.
