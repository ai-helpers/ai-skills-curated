#!/usr/bin/env python3
"""Rename/move a base markdown document and update all cross-references.

Usage:
    python3 scripts/rename_md.py <src-path> <dst-path>

The script:
1. Moves the source base MD file to the destination path.
2. Renames the corresponding raw wiki clone in memory/llm-wiki/raw/ (if present).
3. Updates all Markdown links in memory/bookmarks/md/ that reference the old filename.
4. Updates all snapshot header links in memory/bookmarks/snapshots/ that reference the old filename.
5. Prints a summary of every updated file.

After running this script the caller should run:
    make base-md-sync PATHS="<dst-path>"
    make snapshots-sync
to refresh the ToC, wiki index, and snapshot cross-links.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[1]
BASE_MD_DIR = ROOT / "memory" / "bookmarks" / "md"
SNAPSHOTS_DIR = ROOT / "memory" / "bookmarks" / "snapshots"
RAW_WIKI_DIR = ROOT / "memory" / "llm-wiki" / "raw"


def _replace_in_file(path: Path, old: str, new: str) -> bool:
    """Replace all occurrences of `old` with `new` in `path`. Return True if changed."""
    text = path.read_text(encoding="utf-8")
    new_text = text.replace(old, new)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def update_references(old_name: str, new_name: str) -> list[str]:
    """Scan all base-MD and snapshot files for references to old_name and replace them."""
    changed: list[str] = []
    old_encoded = quote(old_name)
    new_encoded = quote(new_name)

    # Also handle URL-decoded variants that may appear as plain text links
    variants = [
        (old_name, new_name),
        (old_encoded, new_encoded),
    ]
    # Deduplicate in case name has no special chars
    seen: set[tuple[str, str]] = set()
    unique_variants = []
    for pair in variants:
        if pair not in seen:
            seen.add(pair)
            unique_variants.append(pair)

    search_dirs = [BASE_MD_DIR, SNAPSHOTS_DIR]
    for directory in search_dirs:
        for md_file in sorted(directory.glob("*.md")):
            file_changed = False
            for old_v, new_v in unique_variants:
                if _replace_in_file(md_file, old_v, new_v):
                    file_changed = True
            if file_changed:
                changed.append(str(md_file.relative_to(ROOT)))

    return changed


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 rename_md.py <src-path> <dst-path>", file=sys.stderr)
        return 1

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    if not src.is_absolute():
        src = ROOT / src
    if not dst.is_absolute():
        dst = ROOT / dst

    if not src.exists():
        print(f"Error: source file not found: {src}", file=sys.stderr)
        return 1

    if dst.exists() and dst != src:
        print(f"Error: destination already exists: {dst}", file=sys.stderr)
        return 1

    old_name = src.name
    new_name = dst.name

    # 1. Move the base MD file
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)
    print(f"Moved: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")

    # 2. Rename raw wiki clone if present
    old_raw = RAW_WIKI_DIR / old_name
    new_raw = RAW_WIKI_DIR / new_name
    if old_raw.exists():
        old_raw.rename(new_raw)
        print(f"Moved: {old_raw.relative_to(ROOT)} -> {new_raw.relative_to(ROOT)}")

    # 3. Remove stale wiki source page if present (wiki-ingest will create a fresh one)
    wiki_sources_dir = ROOT / "memory" / "llm-wiki" / "wiki" / "sources"
    old_slug = re.sub(r"[^a-zA-Z0-9]+", "-", src.stem).strip("-").lower()
    old_wiki_source = wiki_sources_dir / f"{old_slug}.md"
    if old_wiki_source.exists():
        old_wiki_source.unlink()
        print(f"Removed stale wiki source: {old_wiki_source.relative_to(ROOT)}")

    # 4. Update cross-references in all markdown files
    changed_files = update_references(old_name, new_name)
    if changed_files:
        print(f"\nUpdated references in {len(changed_files)} file(s):")
        for f in changed_files:
            print(f"  {f}")
    else:
        print("\nNo cross-references needed updating.")

    print("\nNext steps (run automatically via Makefile):")
    print(f"  make base-md-sync PATHS=\"{dst.relative_to(ROOT)}\"")
    print("  make snapshots-sync")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
