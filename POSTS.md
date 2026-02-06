# Authoring Posts

Use the `scripts/new_post.py` helper to create new posts. Examples:

Create a date-slugged post:

```bash
python scripts/new_post.py "My New Post Title"
```

Create a UUID-named post (recommended for reduced timing correlation):

```bash
python scripts/new_post.py "My Secret Post" --uuid
```

By default the script creates a per-post assets directory next to the post file (e.g. `2026-02-06-my-post_assets`) and adds an `images` front-matter field pointing to that folder. Place images there and reference them from Markdown using a relative path.

Open Graph preview
- To supply a social preview image for a post, add `og.png` to the assets folder created by `scripts/new_post.py` and the `og_image` front-matter will point to it automatically.
Template: see `docs/posts/_post-template.md` for a sample front-matter layout.
