# PyBlog Admin (archived)

This folder is an archive of a previously used FastAPI admin UI that created posts and opened PRs.

Why archived

- The project is being simplified to an offline-first authoring workflow (create Markdown locally under `docs/posts/` and build with `mkdocs`).
- The admin UI and its automerge workflows increased complexity and attack surface.

If you need this code later, it is preserved here for reference. To restore the admin UI, move files back to `admin/` and re-enable any workflows.

Security reminder: rotate any credentials that may have been exposed and verify GitHub Actions secrets after history rewrites.
