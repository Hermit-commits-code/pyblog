# pyblog

Lightweight, offline-first developer blog scaffold.

This repository is optimized for local authoring of Markdown posts and publishing a built site to GitHub Pages.

Key ideas
- Author posts locally under `docs/posts/` as Markdown.
- Build the site with `mkdocs build` or let GitHub Actions publish on push to the deploy branch.
- Keep the workflow simple: no remote admin UI, no automerge; posts are regular commits.

Quick start (dev)

```bash
python -m pip install --upgrade pip
python -m pip install poetry
poetry install
poetry run pre-commit install
```

Create a new post (helper)

```bash
python scripts/new_post.py "My Title" --open
# or just run the script without args to be prompted interactively
```

Build site locally

```bash
poetry run mkdocs build
```

Preview locally

```bash
poetry run mkdocs serve
```

Deploy

- This repo contains a GitHub Actions workflow to publish the built `site/` to `gh-pages`. Push to your deploy branch (e.g. `feat/bootstrap-ci`) or configure the workflow as desired.

Security and cleanup notes
- The `admin/` folder has been archived to `admin-archive/` to simplify the project. If you want the UI back, restore those files.
- Rotate any credentials that were exposed and advise collaborators to re-clone if history was rewritten.

Contributing

- Use `commitizen` for conventional commits and open PRs for changes.
