---
name: tabs-sync
description: Capture open browser tabs and save to a dated markdown snapshot.
usage: /tabs-sync
trigger: user_message
---

# Tabs Sync Command

Use this command to capture your currently open Chrome browser tabs and save them as a dated markdown document in the repository's bookmark snapshots.

## Workflow

1. **Notebook Selection**: Prompt user to select a notebook basename from `notebooks/*.ipynb`.
2. **Filename Generation**:
   - Strip whitespace from the basename and convert to lowercase.
   - Append the current date in `YYYY-MM-DD` format.
   - Add `.md` file extension.
   - Result: `memory/bookmarks/snapshots/<basename-YYYY-MM-DD>.md`
3. **Tab Capture**:
   - **On macOS (`darwin`):** Run `make tabs-sync NOTEBOOK="<notebook_path>"`, which calls the AppleScript extraction method via `scripts/chrome_tabs_sync.py` to retrieve `title` and `URL` for all open tabs across all Chrome windows instantly with zero extra dependencies.
   - **On Windows/Linux:** Retrieve all open tabs from Chrome via `chrome-devtools-mcp` server tools.
4. **Markdown Generation**: Create a structured markdown document with:
   - Metadata header (date, profile, total tabs).
   - Table of Contents organized by category.
   - Categorized tab tables with title and URL.
5. **Commit**: Commit and push to `main` branch.

## Example

- **Selected notebook**: `50 - Personal and Work.ipynb`
- **Processed basename**: `50-personal-and-work`
- **Date**: `2026-06-27`
- **Result file**: `memory/bookmarks/snapshots/50-personal-and-work-2026-06-27.md`
- **Command**: `make tabs-sync NOTEBOOK="notebooks/50 - Personal and Work.ipynb"`

## Rules

- Ask the user for notebook selection if not provided.
- Preserve original URL and title text exactly as given by the browser.
- Organize tabs into logical categories (Google Services, AWS, GitHub, etc.).
- Include a table of contents for easy navigation.
- Commit directly to `main` without feature branches.
- The bookmark-manager skill handles the core functionality.
