#!/usr/bin/env python3
"""Refresh base Markdown ToCs, clone curated docs to raw/, and leave wiki ingest to Make."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DOCS_ROOT = Path("memory/kb/md")
RAW_ROOT = Path("memory/llm-wiki/raw")
TOC_START = "<!-- llm-wiki-nocode-toc:start -->"
TOC_END = "<!-- llm-wiki-nocode-toc:end -->"
TOC_PATTERN = re.compile(
    rf"\n?{re.escape(TOC_START)}.*?{re.escape(TOC_END)}\n?",
    re.DOTALL,
)


def read_paths_file(paths_file: Path) -> list[str]:
    return [line.strip() for line in paths_file.read_text(encoding="utf-8").splitlines() if line.strip()]


def resolve_inputs(raw_inputs: list[str]) -> list[Path]:
    if not raw_inputs:
        return sorted(path for path in DOCS_ROOT.rglob("*.md") if path.name != "README.md")

    resolved: list[Path] = []
    for raw in raw_inputs:
        path = Path(raw)
        if path.is_dir():
            resolved.extend(sorted(candidate for candidate in path.rglob("*.md") if candidate.name != "README.md"))
        else:
            resolved.append(path)
    return dedupe_paths(resolved)


def dedupe_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        normalized = path.resolve() if path.exists() else path
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(path)
    return unique


def ensure_doc_path(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Base Markdown document not found: {path}")
    if path.suffix != ".md" or path.name == "README.md":
        raise ValueError(f"Unsupported base Markdown path: {path}")
    resolved_path = path.resolve()
    resolved_docs_root = DOCS_ROOT.resolve()
    try:
        resolved_path.relative_to(resolved_docs_root)
    except ValueError as exc:
        raise ValueError(f"Base Markdown path must stay under {DOCS_ROOT}: {path}") from exc
    return resolved_path


def strip_existing_toc(markdown: str) -> str:
    stripped = TOC_PATTERN.sub("\n", markdown)
    return stripped.strip() + "\n"


def collect_headings(markdown: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    seen_anchors: dict[str, int] = {}
    in_fence = False
    fence_marker = ""

    for line in markdown.splitlines():
        stripped = line.lstrip()
        fence_match = re.match(r"^(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                in_fence = False
                fence_marker = ""
            continue
        if in_fence:
            continue

        match = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if not match:
            continue

        level = len(match.group(1))
        title = normalize_heading_title(match.group(2))
        if not title or title.lower() == "table of contents":
            continue

        anchor = github_anchor(title)
        duplicate_count = seen_anchors.get(anchor, 0)
        seen_anchors[anchor] = duplicate_count + 1
        if duplicate_count:
            anchor = f"{anchor}-{duplicate_count}"
        headings.append((level, title, anchor))

    return [(level, f"[{title}](#{anchor})") for level, title, anchor in headings]


def normalize_heading_title(title: str) -> str:
    text = title.strip()
    text = re.sub(r"\s+#+$", "", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_~]", "", text)
    return " ".join(text.split())


def github_anchor(title: str) -> str:
    anchor = title.strip().lower()
    anchor = re.sub(r"[^\w\- ]", "", anchor)
    anchor = anchor.replace(" ", "-")
    anchor = re.sub(r"-{2,}", "-", anchor)
    return anchor.strip("-")


def render_toc(headings: list[tuple[int, str]]) -> str:
    if not headings:
        return ""

    base_level = min(level for level, _ in headings)
    toc_heading = "#" * base_level
    lines = [TOC_START, f"{toc_heading} Table of contents", ""]
    for level, link in headings:
        indent = "  " * (level - base_level)
        lines.append(f"{indent}- {link}")
    lines.extend(["", TOC_END])
    return "\n".join(lines)


def intro_block_end(markdown: str) -> int:
    lines = markdown.splitlines()
    if not lines:
        return 0

    end = 0
    # Keep YAML frontmatter at the top when present.
    if lines[0].strip() == "---":
        frontmatter_end = 1
        while frontmatter_end < len(lines) and lines[frontmatter_end].strip() != "---":
            frontmatter_end += 1
        if frontmatter_end < len(lines):
            end = frontmatter_end + 1
        else:
            end = len(lines)

    while end < len(lines) and not lines[end].strip():
        end += 1
    return end


def rewrite_markdown(markdown: str) -> str:
    clean = strip_existing_toc(markdown)
    headings = collect_headings(clean)
    toc = render_toc(headings)
    if not toc:
        return clean

    lines = clean.splitlines()
    split_index = intro_block_end(clean)
    prefix = "\n".join(lines[:split_index]).rstrip()
    suffix = "\n".join(lines[split_index:]).strip()

    parts = [part for part in [prefix, toc, suffix] if part]
    return "\n\n".join(parts) + "\n"


def sync_one(path: Path) -> tuple[bool, bool]:
    source_path = ensure_doc_path(path)
    original = source_path.read_text(encoding="utf-8")
    rewritten = rewrite_markdown(original)

    doc_changed = False
    if original != rewritten:
        source_path.write_text(rewritten, encoding="utf-8")
        doc_changed = True

    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_ROOT / source_path.name
    raw_changed = not raw_path.exists() or raw_path.read_text(encoding="utf-8") != rewritten
    if raw_changed:
        raw_path.write_text(rewritten, encoding="utf-8")

    return doc_changed, raw_changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Base Markdown files or directories under memory/kb/md/")
    parser.add_argument(
        "--paths-file",
        help="Text file listing one base Markdown path per line. Useful when paths contain spaces.",
    )
    args = parser.parse_args()

    raw_inputs = list(args.paths)
    if args.paths_file:
        raw_inputs.extend(read_paths_file(Path(args.paths_file)))

    docs = [ensure_doc_path(path) for path in resolve_inputs(raw_inputs)]
    updated_docs = 0
    updated_raw = 0
    for path in docs:
        doc_changed, raw_changed = sync_one(path)
        if doc_changed:
            updated_docs += 1
        if raw_changed:
            updated_raw += 1

    print(f"Processed base markdown files: {len(docs)}")
    print(f"Updated base markdown files: {updated_docs}")
    print(f"Updated raw wiki source files: {updated_raw}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
