#!/usr/bin/env python3
"""Fail when a Markdown or HTML reference points to a missing local file."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:")


def local_target(raw_target: str, source: Path) -> Path | None:
    target = raw_target.strip().strip("<>").split(maxsplit=1)[0]
    if not target or target.startswith("#") or target.startswith(SKIP_PREFIXES):
        return None

    target = unquote(target.split("?", 1)[0].split("#", 1)[0])
    if not target:
        return None

    return (source.parent / target).resolve()


def main() -> int:
    failures: list[str] = []
    markdown_files = sorted(
        path for path in ROOT.rglob("*.md") if ".git" not in path.parts
    )

    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        targets = MARKDOWN_LINK.findall(text) + HTML_LINK.findall(text)
        for raw_target in targets:
            target = local_target(raw_target, source)
            if target is not None and not target.exists():
                failures.append(
                    f"{source.relative_to(ROOT)} -> {raw_target} (missing {target.relative_to(ROOT)})"
                )

    if failures:
        print("Broken local documentation links:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Checked {len(markdown_files)} Markdown files: all local links exist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
