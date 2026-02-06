#!/usr/bin/env python3
"""Create a new Markdown post in `docs/posts/` with a slugified filename.

Usage:
  python scripts/new_post.py "My New Post Title"

This creates `docs/posts/YYYY-MM-DD-my-new-post-title.md` with front matter.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    # replace non-alphanum with hyphens
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "post"


def new_post(title: str, outdir: Path) -> Path:
    today = date.today().isoformat()
    slug = slugify(title)
    fname = f"{today}-{slug}.md"
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / fname
    if path.exists():
        raise FileExistsError(f"Post already exists: {path}")
    content = f"""---
title: {title}
date: {today}
---

# {title}

Write your post here.

"""
    path.write_text(content, encoding="utf8")
    return path


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: new_post.py "Post Title"')
        return 2
    title = argv[1]
    outdir = Path(__file__).resolve().parents[1] / "docs" / "posts"
    try:
        path = new_post(title, outdir)
    except FileExistsError as exc:
        print(exc)
        return 1
    print(f"Created: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
