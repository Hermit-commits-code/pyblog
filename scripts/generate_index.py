#!/usr/bin/env python3
"""Generate blog index and tag pages from `docs/posts/*.md` front-matter.

Writes:
 - `docs/blog/index.md`
 - `docs/tags/<tag>.md` for each tag

Usage:
  python scripts/generate_index.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - runtime availability
    print("PyYAML is required to run this script. Install project dev deps.")
    raise


POSTS_DIR = Path(__file__).resolve().parents[1] / "docs" / "posts"
OUT_BLOG = Path(__file__).resolve().parents[1] / "docs" / "blog"
OUT_TAGS = Path(__file__).resolve().parents[1] / "docs" / "tags"


def read_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    raw = parts[1]
    return yaml.safe_load(raw) or {}


def find_posts() -> list[dict[str, Any]]:
    posts: list[dict[str, Any]] = []
    for md in sorted(POSTS_DIR.glob("*.md")):
        meta = read_front_matter(md)
        if not meta:
            continue
        # Skip drafts
        if meta.get("draft"):
            continue
        # Normalize
        date = meta.get("date")
        try:
            date_obj = datetime.fromisoformat(str(date)) if date else None
        except Exception:
            date_obj = None
        posts.append(
            {
                "path": md.relative_to(Path(__file__).resolve().parents[1] / "docs"),
                "title": meta.get("title") or md.stem,
                "date": date_obj,
                "date_str": str(date) if date else "",
                "excerpt": meta.get("excerpt", ""),
                "tags": meta.get("tags", []),
            }
        )
    # sort by date desc, fallback to filename
    posts.sort(key=lambda p: p["date"] or datetime.min, reverse=True)
    return posts


def render_index(posts: list[dict[str, Any]]) -> str:
    lines = ["---", "title: Blog", "---", "", "# Blog", ""]
    for p in posts:
        # link from docs/blog/index.md -> posts/* : step up one level
        link = "../" + str(p["path"]).replace("\\", "/")
        title = p["title"]
        date = p["date_str"]
        excerpt = p["excerpt"]
        lines.append(f"- **[{title}]({link})** — {date}")
        if excerpt:
            lines.append(f"  \n  {excerpt}")
    lines.append("")
    return "\n".join(lines)


def render_tag(tag: str, posts: list[dict[str, Any]]) -> str:
    lines = ["---", f"title: Tags: {tag}", "---", "", f"# Tag: {tag}", ""]
    for p in posts:
        # tag pages are in docs/tags/ so step up one level to reach posts
        link = "../" + str(p["path"]).replace("\\", "/")
        title = p["title"]
        date = p["date_str"]
        lines.append(f"- **[{title}]({link})** — {date}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    posts = find_posts()
    OUT_BLOG.mkdir(parents=True, exist_ok=True)
    OUT_TAGS.mkdir(parents=True, exist_ok=True)
    index_md = OUT_BLOG / "index.md"
    index_md.write_text(render_index(posts), encoding="utf8")

    # collect tags
    tag_map: dict[str, list[dict[str, Any]]] = {}
    for p in posts:
        for t in p["tags"] or []:
            tag_map.setdefault(str(t), []).append(p)

    # write tag pages
    for tag, items in tag_map.items():
        safe = "-".join(tag.split())
        path = OUT_TAGS / f"{safe}.md"
        path.write_text(render_tag(tag, items), encoding="utf8")

    print(f"Wrote {index_md} and {len(tag_map)} tag pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
