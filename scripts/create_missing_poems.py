#!/usr/bin/env python3
"""Create placeholder poem files in target languages for Greek poem slugs.

The generated files follow EN/RU poem placeholder format (title only), and the
title value is the markdown filename without extension (slug), e.g.:

---
title: "anoiksi"
---
"""

from __future__ import annotations

import argparse
from pathlib import Path


def write_placeholder(path: Path, title: str, dry_run: bool) -> None:
    body = f"---\ntitle: \"{title}\"\n---\n"

    if dry_run:
        print(f"[DRY RUN] Would create: {path}")
        return

    path.write_text(body, encoding="utf-8")
    print(f"Created: {path}")


def create_missing_files(content_dir: Path, target_langs: list[str], dry_run: bool) -> int:
    greek_poems_dir = content_dir / "el" / "poems"
    greek_files = sorted(
        p for p in greek_poems_dir.glob("*.md") if p.name != "_index.md"
    )

    created = 0

    for lang in target_langs:
        lang_poems_dir = content_dir / lang / "poems"
        if not lang_poems_dir.exists():
            print(f"Skipping language '{lang}' (missing directory: {lang_poems_dir})")
            continue

        existing = {p.name for p in lang_poems_dir.glob("*.md")}

        for greek_file in greek_files:
            filename = greek_file.name
            if filename in existing:
                continue

            title = greek_file.stem
            target_file = lang_poems_dir / filename
            write_placeholder(target_file, title, dry_run=dry_run)
            created += 1

    return created


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create missing poem files for target languages based on Greek poem "
            "filenames, using title-only front matter."
        )
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=Path("content"),
        help="Root content directory (default: content)",
    )
    parser.add_argument(
        "--langs",
        nargs="+",
        default=["en", "ru"],
        help="Target language codes to process (default: en ru)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    created = create_missing_files(
        content_dir=args.content_dir,
        target_langs=args.langs,
        dry_run=args.dry_run,
    )
    mode = "would be created" if args.dry_run else "created"
    print(f"\nDone. {created} file(s) {mode}.")


if __name__ == "__main__":
    main()
