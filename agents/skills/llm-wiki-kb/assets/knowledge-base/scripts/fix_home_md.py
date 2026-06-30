#!/usr/bin/env python3
"""Redirect a local KB base document to its canonical home repository.

Usage:
    python3 scripts/fix_home_md.py <src-path> <home-repo> [--export-home <path>]

Arguments:
    src-path   Path to the local base markdown document (for example:
               memory/kb/md/494 - DKT - Kill Legacy.md).
    home-repo  Canonical repository in "owner/repo" form. If only a repo name
               is provided, "dktunited/<repo>" is assumed.

Behavior:
1. Keeps the same document path inside the canonical repository.
2. Optionally exports canonical-home content with the "Snapshots" section removed.
3. Rewrites the local document into a machine-readable redirect stub.
4. Prints the canonical path/url for follow-up actions.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE_MD_DIR = ROOT / "memory" / "kb" / "md"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def normalize_home_repo(raw: str) -> str:
    value = raw.strip()
    if not value:
        raise ValueError("home-repo cannot be empty")
    if "/" in value:
        return value
    return f"dktunited/{value}"


def canonical_url(home_repo: str, rel_path: Path) -> str:
    encoded_path = quote(rel_path.as_posix(), safe="/")
    return f"https://github.com/{home_repo}/blob/main/{encoded_path}"


def rewrite_as_redirect_stub(src_path: Path, home_repo: str, rel_src: Path) -> None:
    home_url = canonical_url(home_repo, rel_src)
    body = "\n".join(
        [
            "---",
            'canonical_entity: "kb-document"',
            f'home_repo: "{home_repo}"',
            f'home_path: "{rel_src.as_posix()}"',
            f'home_url: "{home_url}"',
            "---",
            "",
            "This document is redirected to its canonical home.",
            "",
            f"- Home repository: `{home_repo}`",
            f"- Home path: `{rel_src.as_posix()}`",
            f"- Canonical document: [{rel_src.name}]({home_url})",
            "",
        ]
    )
    src_path.write_text(body, encoding="utf-8")


def strip_snapshots_section(markdown: str) -> str:
    """Remove a section titled 'Snapshots' (any heading level), if present."""
    lines = markdown.splitlines()
    start_idx = None
    start_level = None
    for i, line in enumerate(lines):
        match = HEADING_RE.match(line.strip())
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip().lower()
        if title == "snapshots":
            start_idx = i
            start_level = level
            break

    if start_idx is None or start_level is None:
        return markdown

    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        match = HEADING_RE.match(lines[i].strip())
        if not match:
            continue
        level = len(match.group(1))
        if level <= start_level:
            end_idx = i
            break

    while start_idx > 0 and lines[start_idx - 1].strip() == "":
        start_idx -= 1

    kept = lines[:start_idx] + lines[end_idx:]
    return "\n".join(kept).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src_path", help="Local source path under memory/kb/md/")
    parser.add_argument("home_repo", help='Canonical home repo (owner/repo or just "repo")')
    parser.add_argument(
        "--export-home",
        dest="export_home",
        help="Optional output path for canonical-home content with Snapshots section removed",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    src = Path(args.src_path)
    if not src.is_absolute():
        src = ROOT / src
    src = src.resolve()

    if not src.exists():
        print(f"Error: source file not found: {src}", file=sys.stderr)
        return 1

    try:
        rel_src = src.relative_to(ROOT)
    except ValueError:
        print(f"Error: source file must be inside repository root: {src}", file=sys.stderr)
        return 1

    if not str(rel_src.as_posix()).startswith("memory/kb/md/"):
        print(f"Error: source file must be under memory/kb/md/: {rel_src}", file=sys.stderr)
        return 1

    try:
        home_repo = normalize_home_repo(args.home_repo)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    original = src.read_text(encoding="utf-8")
    canonical_home = strip_snapshots_section(original)
    if args.export_home:
        export_path = Path(args.export_home)
        if not export_path.is_absolute():
            export_path = ROOT / export_path
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_path.write_text(canonical_home, encoding="utf-8")
        print(f"Exported canonical-home content (without Snapshots): {export_path.relative_to(ROOT)}")

    rewrite_as_redirect_stub(src, home_repo, rel_src)
    print(f"Redirected local document: {rel_src}")
    print(f"Canonical repository: {home_repo}")
    print(f"Canonical path: {rel_src.as_posix()}")
    print(f"Canonical URL: {canonical_url(home_repo, rel_src)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
