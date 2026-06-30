#!/usr/bin/env python3
"""Convert iPython notebooks to Markdown documents via uv + jupyter nbconvert."""

from __future__ import annotations

import argparse
import re
import subprocess
import shutil
from pathlib import Path
from typing import Iterable


def resolve_inputs(paths: Iterable[str]) -> list[Path]:
    resolved: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            resolved.extend(sorted(path.rglob("*.ipynb")))
        else:
            resolved.append(path)
    return resolved


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-")
    return slug.lower()


def output_name_for(input_path: Path, mode: str) -> str:
    if mode == "exact":
        return input_path.stem
    return slugify(input_path.stem)


def run_nbconvert(input_path: Path, output_dir: Path, output_name: str) -> Path:
    command = [
        "uv",
        "run",
        "jupyter",
        "nbconvert",
        "--to",
        "markdown",
        "--output",
        output_name,
        "--output-dir",
        str(output_dir),
        str(input_path),
    ]
    subprocess.run(command, check=True)
    return output_dir / f"{output_name}.md"


def clone_output(output_path: Path, clone_dirs: list[Path]) -> None:
    for clone_dir in clone_dirs:
        clone_dir.mkdir(parents=True, exist_ok=True)
        clone_path = clone_dir / output_path.name
        shutil.copy2(output_path, clone_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Notebook files or directories")
    parser.add_argument(
        "--output-dir",
        default="memory/kb/md",
        help="Directory where Markdown files will be written",
    )
    parser.add_argument(
        "--name-mode",
        choices=["slug", "exact"],
        default="slug",
        help="Whether to slugify the output filename or preserve the notebook stem",
    )
    parser.add_argument(
        "--clone-to",
        action="append",
        default=[],
        help="Additional directories that receive a copy of the generated Markdown",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    clone_dirs = [Path(path) for path in args.clone_to]

    converted = 0
    for input_path in resolve_inputs(args.paths):
        if input_path.suffix != ".ipynb":
            continue
        output_name = output_name_for(input_path, args.name_mode)
        output_path = run_nbconvert(input_path, output_dir, output_name)
        if clone_dirs:
            clone_output(output_path, clone_dirs)
        print(f"{input_path} -> {output_path}")
        converted += 1

    if converted == 0:
        raise SystemExit("No .ipynb files were converted.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
