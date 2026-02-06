# PyBlog

Welcome to PyBlog — a lightweight developer blog. This site is built with MkDocs (Material theme) and automatically published to GitHub Pages.

## Recent posts

- [First Post](posts/first-post.md)

---

Subscribe and follow updates in the repository.

Quick post workflow
-------------------

Create new posts using the helper script which generates a date-prefixed slug filename and front matter:

```bash
python scripts/new_post.py "My New Post Title"
```

Or using `make`:

```bash
make new-post title="My New Post Title"
```

Files placed under `docs/posts/` will automatically publish to clean slugs (e.g. `/posts/my-new-post-title/`).
