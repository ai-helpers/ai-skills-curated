#!/usr/bin/env python3
"""Synchronize bookmark snapshots and base markdown documents."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS_DIR = ROOT / "memory" / "bookmarks" / "snapshots"
BASE_MD_DIR = ROOT / "memory" / "bookmarks" / "md"
SNAPSHOT_DATE_RE = re.compile(r"^(?P<slug>.+)-(?P<date>\d{4}-\d{2}-\d{2})$")


def normalize_stem(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-{2,}", "-", normalized)


def find_base_md_by_slug(base_slug: str) -> Path | None:
    for candidate in BASE_MD_DIR.glob("*.md"):
        if normalize_stem(candidate.stem) == base_slug:
            return candidate
    return None


def upsert_snapshot_header(snapshot_path: Path, base_md_path: Path) -> bool:
    text = snapshot_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return False

    base_link = f"../md/{base_md_path.name}"
    header_line = f"**Base document:** [{base_md_path.stem}]({base_link})"

    changed = False
    insert_idx = 1

    date_line_idx = next((i for i, line in enumerate(lines) if line.startswith("**Date:**")), -1)
    if date_line_idx != -1:
        existing_idx = date_line_idx - 1
        if existing_idx >= 0 and lines[existing_idx].startswith("**Base document:**"):
            if lines[existing_idx] != header_line:
                lines[existing_idx] = header_line
                changed = True
        else:
            lines.insert(date_line_idx, header_line)
            changed = True
    else:
        if len(lines) > 1 and lines[1].startswith("**Base document:**"):
            if lines[1] != header_line:
                lines[1] = header_line
                changed = True
        else:
            lines.insert(insert_idx, header_line)
            changed = True

    if changed:
        snapshot_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    return changed


def upsert_base_snapshot_table(base_md_path: Path, snapshot_path: Path, date_str: str) -> bool:
    text = base_md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    section_header = "## Snapshots"
    table_header = "| Date | Snapshot |"
    table_separator = "|---|---|"
    row = f"| {date_str} | [{snapshot_path.name}](../snapshots/{snapshot_path.name}) |"

    changed = False
    section_idx = next((i for i, line in enumerate(lines) if line.strip() == section_header), -1)

    if section_idx == -1:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend([section_header, "", table_header, table_separator, row])
        changed = True
    else:
        next_section_idx = len(lines)
        for i in range(section_idx + 1, len(lines)):
            if lines[i].startswith("## "):
                next_section_idx = i
                break

        header_idx = -1
        for i in range(section_idx + 1, next_section_idx):
            if lines[i].strip() == table_header:
                header_idx = i
                break

        if header_idx == -1:
            insertion = [""]
            if section_idx + 1 < len(lines) and lines[section_idx + 1].strip() == "":
                insertion = []
            insertion.extend([table_header, table_separator, row])
            lines[section_idx + 1 : section_idx + 1] = insertion
            changed = True
        else:
            separator_idx = header_idx + 1
            if separator_idx >= len(lines) or lines[separator_idx].strip() != table_separator:
                lines.insert(separator_idx, table_separator)
                changed = True

            next_section_idx = len(lines)
            for i in range(header_idx + 1, len(lines)):
                if lines[i].startswith("## "):
                    next_section_idx = i
                    break

            existing_rows = {
                lines[i].strip()
                for i in range(header_idx + 2, next_section_idx)
                if lines[i].strip().startswith("|")
            }
            if row not in existing_rows:
                insert_idx = next_section_idx
                while insert_idx > header_idx + 2 and lines[insert_idx - 1].strip() == "":
                    insert_idx -= 1
                lines.insert(insert_idx, row)
                changed = True

    if changed:
        base_md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    return changed


def main() -> None:
    if not SNAPSHOTS_DIR.exists() or not BASE_MD_DIR.exists():
        raise SystemExit("Required directories are missing.")

    snapshot_files = sorted(
        p for p in SNAPSHOTS_DIR.glob("*.md") if p.name.lower() != "readme.md"
    )

    snapshot_updates = 0
    base_updates = 0
    unmatched = []

    for snapshot_path in snapshot_files:
        match = SNAPSHOT_DATE_RE.match(snapshot_path.stem)
        if not match:
            continue

        base_slug = normalize_stem(match.group("slug"))
        date_str = match.group("date")
        base_md_path = find_base_md_by_slug(base_slug)

        if base_md_path is None:
            unmatched.append(snapshot_path.name)
            continue

        if upsert_snapshot_header(snapshot_path, base_md_path):
            snapshot_updates += 1
        if upsert_base_snapshot_table(base_md_path, snapshot_path, date_str):
            base_updates += 1

    print(f"Updated snapshot files: {snapshot_updates}")
    print(f"Updated base markdown files: {base_updates}")
    if unmatched:
        print("Unmatched snapshots:")
        for name in unmatched:
            print(f"- {name}")


if __name__ == "__main__":
    main()
