#!/usr/bin/env python3
"""Redirect a local KB base document to its canonical home repository.

Usage:
    python3 scripts/fix_home_md.py <src-path> <home-repo>

Arguments:
    src-path   Path to the local base markdown document (for example:
               memory/kb/md/494 - DKT - Kill Legacy.md).
    home-repo  Canonical repository in "owner/repo" form. If only a repo name
               is provided, "dktunited/<repo>" is assumed.

Behavior:
1. Keeps the same document path inside the canonical repository.
2. Rewrites the local document into a machine-readable redirect stub.
3. Prints the canonical path/url for follow-up actions.
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE_MD_DIR = ROOT / "memory" / "kb" / "md"


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


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/fix_home_md.py <src-path> <home-repo>", file=sys.stderr)
        return 1

    src = Path(sys.argv[1])
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
        home_repo = normalize_home_repo(sys.argv[2])
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    rewrite_as_redirect_stub(src, home_repo, rel_src)
    print(f"Redirected local document: {rel_src}")
    print(f"Canonical repository: {home_repo}")
    print(f"Canonical path: {rel_src.as_posix()}")
    print(f"Canonical URL: {canonical_url(home_repo, rel_src)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

