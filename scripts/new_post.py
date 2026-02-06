#!/usr/bin/env python3
"""Create a new Markdown post in `docs/posts/` with options for slug or UUID filenames.

Usage:
  python scripts/new_post.py "My New Post Title" [--uuid] [--images-dir IMGD]

This creates `docs/posts/YYYY-MM-DD-my-new-post-title.md` (default) or
`docs/posts/<uuid>.md` when `--uuid` is used. Image directory is created if requested.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from uuid import uuid4


def slugify(value: str) -> str:
    value = value.strip().lower()
    # replace non-alphanum with hyphens
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "post"


def new_post(
    title: str, outdir: Path, use_uuid: bool = False, images_dir: str | None = None
) -> Path:
    today = date.today().isoformat()
    if use_uuid:
        fname = f"{uuid4().hex}.md"
    else:
        slug = slugify(title)
        fname = f"{today}-{slug}.md"
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / fname
    if path.exists():
        raise FileExistsError(f"Post already exists: {path}")
    # Create a per-post assets/images folder by default (helps keep images private)
    if images_dir:
        assets_path = outdir / images_dir
    else:
        assets_path = outdir / (fname[:-3] + "_assets")
    assets_path.mkdir(parents=True, exist_ok=True)
    relative_assets = str(Path("posts") / assets_path.name)
    content = f"""---
title: "{title}"
date: {today}
tags: []
excerpt: ""
draft: false
images: "{relative_assets}"
---

# {title}

Write your post here.

You can add images into the `{relative_assets}` folder and reference them like:

![alt text]({{ site_url }}/{relative_assets}/image.png)

"""
    path.write_text(content, encoding="utf8")
    return path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Create a new blog post in docs/posts/"
    )
    parser.add_argument("title", help="Post title")
    parser.add_argument(
        "--uuid", action="store_true", help="Use a UUID filename instead of a date-slug"
    )
    parser.add_argument(
        "--images-dir",
        default=None,
        help="Create an images subdirectory under the post folder",
    )
    args = parser.parse_args(argv[1:])

    outdir = Path(__file__).resolve().parents[1] / "docs" / "posts"
    try:
        path = new_post(
            args.title, outdir, use_uuid=args.uuid, images_dir=args.images_dir
        )
    except FileExistsError as exc:
        print(exc)
        return 1
    print(f"Created: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
