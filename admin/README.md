PyBlog Admin
=================

This directory contains a minimal FastAPI admin used to create posts and open PRs against the repository.

Setup (local)
- install dependencies: `pip install fastapi jinja2 requests uvicorn`
- set env:
  - `GITHUB_REPO=owner/repo`
  - `GITHUB_BASE_BRANCH=feat/bootstrap-ci` (or your branch)
  - `GITHUB_TOKEN` (optional fallback)
  - `GITHUB_OAUTH_CLIENT_ID` and `GITHUB_OAUTH_CLIENT_SECRET` for OAuth
  - `ADMIN_BASIC_USER`/`ADMIN_BASIC_PASSWORD` to enable Basic Auth
  - `ADMIN_SESSION_SECRET` set to a secure random value

Run:
- `uvicorn admin.app:app --reload --port 8000`

Security notes
- Never store real secrets in repo. Use GitHub Secrets and rotate any exposed tokens.
- Use a short-lived OAuth App or GitHub App for production.
- Protect `GITHUB_TOKEN` and restrict automerge label acceptance in Actions.
