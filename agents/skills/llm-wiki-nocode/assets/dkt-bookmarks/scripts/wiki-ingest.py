#!/usr/bin/env python3
"""Index raw Markdown documents into the repo-local wiki workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


RAW_ROOT = Path("memory/llm-wiki/raw")
WIKI_ROOT = Path("memory/llm-wiki/wiki")
README_PATH = Path("memory/llm-wiki/README.md")
SOURCES_ROOT = WIKI_ROOT / "sources"
ENTITIES_ROOT = WIKI_ROOT / "entities"
CONCEPTS_ROOT = WIKI_ROOT / "concepts"
SYNTHESIS_ROOT = WIKI_ROOT / "synthesis"
LOG_PATH = WIKI_ROOT / "log.md"
INDEX_PATH = WIKI_ROOT / "index.md"


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()


def relative_slug(path: Path, root: Path) -> str:
    parts = path.relative_to(root).with_suffix("").parts
    return "/".join(slugify(part) for part in parts)


def extract_title(markdown: str, fallback: str) -> str:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
        if index + 1 < len(lines):
            underline = lines[index + 1].strip()
            if underline and re.fullmatch(r"=+", underline):
                return stripped
            if underline and re.fullmatch(r"-+", underline):
                return stripped
        break
    return fallback


def strip_frontmatter(markdown: str) -> str:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return markdown.strip() + "\n"

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[index + 1 :]).lstrip("\n").rstrip() + "\n"

    return markdown.strip() + "\n"


def render_frontmatter(title: str, page_type: str, created: str, updated: str, sources: list[str]) -> str:
    return "\n".join(
        [
            "---",
            f"title: {json.dumps(title)}",
            f'type: {json.dumps(page_type)}',
            f'created: {json.dumps(created)}',
            f'updated: {json.dumps(updated)}',
            "sources: "
            + ("[]" if not sources else "[" + ", ".join(json.dumps(source) for source in sources) + "]"),
            "---",
        ]
    )


def read_existing_created(path: Path) -> str | None:
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("created:"):
            match = re.search(r'"([^"]+)"', stripped)
            if match:
                return match.group(1)
    return None


def collect_raw_files(raw_args: list[str]) -> list[Path]:
    if not raw_args or raw_args == ["scan"]:
        return sorted(RAW_ROOT.rglob("*.md"))

    paths: list[Path] = []
    for raw in raw_args:
        path = Path(raw)
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.md")))
        else:
            paths.append(path)
    return paths


def choose_latest_by_slug(raw_files: list[Path]) -> list[Path]:
    chosen: dict[str, Path] = {}
    chosen_mtime: dict[str, float] = {}
    for raw_path in raw_files:
        source_slug = relative_slug(raw_path, RAW_ROOT)
        mtime = raw_path.stat().st_mtime
        if source_slug not in chosen or mtime >= chosen_mtime[source_slug]:
            chosen[source_slug] = raw_path
            chosen_mtime[source_slug] = mtime
    return [chosen[key] for key in sorted(chosen)]


def ensure_directories() -> None:
    for path in [SOURCES_ROOT, ENTITIES_ROOT, CONCEPTS_ROOT, SYNTHESIS_ROOT]:
        path.mkdir(parents=True, exist_ok=True)


def write_source_page(raw_path: Path) -> tuple[Path, str]:
    raw_text = raw_path.read_text(encoding="utf-8")
    clean_text = strip_frontmatter(raw_text)
    source_slug = relative_slug(raw_path, RAW_ROOT)
    output_path = SOURCES_ROOT / f"{source_slug}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    created = read_existing_created(output_path)
    if created is None:
        created = dt.date.today().isoformat()
    updated = dt.date.today().isoformat()
    title = extract_title(clean_text, raw_path.stem)

    body = "\n".join(
        [
            render_frontmatter(title, "source", created, updated, []),
            "",
            clean_text.rstrip(),
            "",
        ]
    )
    output_path.write_text(body, encoding="utf-8")
    return output_path, title


def build_index(source_pages: list[tuple[str, Path, str]]) -> str:
    today = dt.date.today().isoformat()
    lines = [
        render_frontmatter("Wiki Index", "synthesis", today, today, []),
        "",
        "# Wiki Index",
        "",
        "## Sources",
    ]

    if source_pages:
        for slug, _, title in source_pages:
            lines.append(f"- [{title}](sources/{slug}.md)")
    else:
        lines.append("- _None yet_")

    lines.extend(
        [
            "",
            "## Entities",
            "- _None yet_",
            "",
            "## Concepts",
            "- _None yet_",
            "",
            "## Synthesis",
            "- _None yet_",
            "",
        ]
    )
    return "\n".join(lines)


def append_log(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")
    existing = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else "# Wiki Log\n\nChronological record of wiki operations.\n"
    entry = f"- {timestamp} — {message}\n"
    LOG_PATH.write_text(existing.rstrip() + "\n" + entry, encoding="utf-8")


def build_readme(source_pages: list[tuple[str, Path, str]]) -> str:
    lines = [
        "# LLM Wiki",
        "",
        "Repo-local nocode wiki workspace.",
        "",
        "## Layout",
        "",
        "```text",
        "memory/llm-wiki/",
        "  wiki/",
        "    index.md",
        "    log.md",
        "    sources/",
        "    entities/",
        "    concepts/",
        "    synthesis/",
        "  raw/",
        "  questions_pending/",
        "  questions_approved/",
        "  lint_pending/",
        "  lint_approved/",
        "```",
        "",
        "Use this tree for wiki ingestion, retrieval, and linting work. All generated wiki artifacts stay under `memory/llm-wiki/`.",
        "",
        "The `llm-wiki-nocode` skill documents the workflow for this tree.",
        "",
        "## Ingest",
        "",
        "Run `make wiki-ingest` to scan `memory/llm-wiki/raw/`, build source pages under `memory/llm-wiki/wiki/sources/`, refresh `memory/llm-wiki/wiki/index.md`, refresh this README, and append a log entry.",
        "",
        "## Sources",
    ]

    if source_pages:
        for slug, _, title in source_pages:
            lines.append(f"- [{title}](wiki/sources/{slug}.md)")
    else:
        lines.append("- _None yet_")

    lines.extend(["", "The `wiki/index.md` file is the primary catalog for navigation."])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Raw Markdown files, directories, or 'scan'")
    args = parser.parse_args()

    ensure_directories()

    raw_files = [path for path in collect_raw_files(args.paths) if path.exists() and path.suffix == ".md"]
    raw_files = choose_latest_by_slug(raw_files)
    source_pages: list[tuple[str, Path, str]] = []
    for raw_path in raw_files:
        output_path, title = write_source_page(raw_path)
        source_slug = output_path.relative_to(SOURCES_ROOT).with_suffix("").as_posix()
        source_pages.append((source_slug, output_path, title))
        print(f"{raw_path} -> {output_path}")

    source_pages.sort(key=lambda item: item[0])
    INDEX_PATH.write_text(build_index(source_pages), encoding="utf-8")
    README_PATH.write_text(build_readme(source_pages), encoding="utf-8")
    append_log(f"indexed {len(source_pages)} source page(s) from raw/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
