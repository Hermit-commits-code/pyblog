from __future__ import annotations

import base64
import os
import time
from pathlib import Path
from typing import Optional

import requests
from fastapi import (Depends, FastAPI, File, Form, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import (HTMLResponse, JSONResponse, PlainTextResponse,
                               RedirectResponse)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

APP_DIR = Path(__file__).resolve().parents[0]
TEMPLATES = Jinja2Templates(directory=APP_DIR / "templates")

app = FastAPI(title="PyBlog Admin")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")

# Sessions for OAuth token storage
SESSION_SECRET = os.environ.get("ADMIN_SESSION_SECRET", "dev-secret-change-me")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# Config
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "Hermit-commits-code/pyblog")
GITHUB_BASE_BRANCH = os.environ.get("GITHUB_BASE_BRANCH", "main")
API_BASE = "https://api.github.com"
GITHUB_AUTOMERGE_LABEL = os.environ.get("ADMIN_AUTOMERGE_LABEL", "automerge-admin")

# Optional Basic auth
security = HTTPBasic()
ADMIN_BASIC_USER = os.environ.get("ADMIN_BASIC_USER")
ADMIN_BASIC_PASSWORD = os.environ.get("ADMIN_BASIC_PASSWORD")


def require_basic_auth(
    request: Request, credentials: HTTPBasicCredentials = Depends(security)
):
    if not (ADMIN_BASIC_USER and ADMIN_BASIC_PASSWORD):
        return None
    import secrets as _secrets

    user_ok = _secrets.compare_digest(credentials.username, ADMIN_BASIC_USER)
    pass_ok = _secrets.compare_digest(credentials.password, ADMIN_BASIC_PASSWORD)
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return None


def github_headers(token: Optional[str]) -> dict[str, str]:
    hdr = {"Accept": "application/vnd.github+json"}
    if token:
        hdr["Authorization"] = f"token {token}"
    return hdr


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = s.replace(" ", "-")
    s = "".join(ch for ch in s if ch.isalnum() or ch == "-")
    return s or f"post-{int(time.time())}"


def gh_create_branch(token: str, branch: str, source: Optional[str] = None) -> dict:
    owner, repo = GITHUB_REPO.split("/")
    source = source or GITHUB_BASE_BRANCH
    url_ref = f"{API_BASE}/repos/{owner}/{repo}/git/ref/heads/{source}"
    r = requests.get(url_ref, headers=github_headers(token))
    r.raise_for_status()
    sha = r.json()["object"]["sha"]
    payload = {"ref": f"refs/heads/{branch}", "sha": sha}
    r = requests.post(
        f"{API_BASE}/repos/{owner}/{repo}/git/refs",
        json=payload,
        headers=github_headers(token),
    )
    if r.status_code == 422:
        r2 = requests.get(
            f"{API_BASE}/repos/{owner}/{repo}/git/ref/heads/{branch}",
            headers=github_headers(token),
        )
        r2.raise_for_status()
        return r2.json()
    r.raise_for_status()
    return r.json()


def gh_create_or_update_file(
    token: str, path: str, content_bytes: bytes, branch: str, message: str
):
    owner, repo = GITHUB_REPO.split("/")
    url = f"{API_BASE}/repos/{owner}/{repo}/contents/{path}"
    b64 = base64.b64encode(content_bytes).decode("utf8")
    payload = {"message": message, "content": b64, "branch": branch}
    r = requests.put(url, json=payload, headers=github_headers(token))
    if r.status_code not in (200, 201):
        r.raise_for_status()
    return r.json()


def gh_open_pr(token: str, branch: str, title: str, body: str = "") -> dict:
    owner, repo = GITHUB_REPO.split("/")
    url = f"{API_BASE}/repos/{owner}/{repo}/pulls"
    payload = {"title": title, "head": branch, "base": GITHUB_BASE_BRANCH, "body": body}
    r = requests.post(url, json=payload, headers=github_headers(token))
    r.raise_for_status()
    pr = r.json()
    try:
        if GITHUB_AUTOMERGE_LABEL:
            lab_url = f"{API_BASE}/repos/{owner}/{repo}/issues/{pr['number']}/labels"
            requests.post(
                lab_url,
                json={"labels": [GITHUB_AUTOMERGE_LABEL]},
                headers=github_headers(token),
            )
    except Exception:
        pass
    return pr


def gh_post_comment(token: str, pr_number: int, comment: str) -> dict:
    owner, repo = GITHUB_REPO.split("/")
    url = f"{API_BASE}/repos/{owner}/{repo}/issues/{pr_number}/comments"
    r = requests.post(url, json={"body": comment}, headers=github_headers(token))
    if r.status_code not in (200, 201):
        return {"error": r.text}
    return r.json()


def gh_get_pr(token: str, pr_number: int) -> dict:
    owner, repo = GITHUB_REPO.split("/")
    r = requests.get(
        f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}",
        headers=github_headers(token),
    )
    r.raise_for_status()
    return r.json()


def gh_is_pr_merged(token: str, pr_number: int) -> bool:
    owner, repo = GITHUB_REPO.split("/")
    r = requests.get(
        f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}/merge",
        headers=github_headers(token),
    )
    return r.status_code == 204


def gh_get_combined_status(token: str, sha: str) -> dict:
    owner, repo = GITHUB_REPO.split("/")
    status = requests.get(
        f"{API_BASE}/repos/{owner}/{repo}/commits/{sha}/status",
        headers=github_headers(token),
    )
    status.raise_for_status()
    checks = requests.get(
        f"{API_BASE}/repos/{owner}/{repo}/commits/{sha}/check-runs",
        headers={**github_headers(token), "Accept": "application/vnd.github+json"},
    )
    checks_data = {}
    try:
        checks.raise_for_status()
        checks_data = checks.json()
    except Exception:
        checks_data = {"check_runs": []}
    return {"status": status.json(), "checks": checks_data}


@app.get("/", response_class=RedirectResponse)
def root_redirect():
    return RedirectResponse(url="/admin/new")


@app.get("/admin/new", response_class=HTMLResponse)
def new_post_form(request: Request, _auth=Depends(require_basic_auth)):
    token_present = bool(request.session.get("github_token") or GITHUB_TOKEN)
    return TEMPLATES.TemplateResponse(
        "new_post.html",
        {"request": request, "token": token_present, "repo": GITHUB_REPO},
    )


@app.post("/admin/new")
async def create_post(
    request: Request,
    title: str = Form(...),
    tags: str = Form(""),
    content: str = Form(""),
    image: UploadFile = File(None),
    _auth=Depends(require_basic_auth),
):
    token = request.session.get("github_token") or GITHUB_TOKEN
    if not token:
        return HTMLResponse(
            "<p>No GitHub credentials available. Login via OAuth or set `GITHUB_TOKEN`.</p>",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    slug = slugify(title)
    timestamp = int(time.time())
    branch = f"admin/{slug}-{timestamp}"
    try:
        gh_create_branch(token, branch)
    except requests.HTTPError:
        try:
            request.session.pop("github_token", None)
        except Exception:
            pass
        return RedirectResponse(url="/auth/login?next=/admin/new", status_code=303)
    fn = getattr(image, "filename", None)
    if image and (fn and fn.strip()):
        filename = Path(image.filename or "upload").name
        if not (image.content_type and image.content_type.startswith("image/")):
            return HTMLResponse(
                "<p>Uploaded file is not an image.</p>",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        img_bytes = await image.read()
        if len(img_bytes) > 2_000_000:
            return HTMLResponse(
                "<p>Image too large (max 2MB).</p>",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        img_path = f"docs/posts/{slug}_assets/{filename}"
        gh_create_or_update_file(
            token, img_path, img_bytes, branch, f"chore: add image for {slug}"
        )
        og_path = f"docs/posts/{slug}_assets/og.png"
        gh_create_or_update_file(
            token, og_path, img_bytes, branch, f"chore: add og for {slug}"
        )
    md_path = f"docs/posts/{slug}.md"
    front = [
        "---",
        f'title: "{title}"',
        f"date: {time.strftime('%Y-%m-%d')}",
        f"tags: [{tags}]",
        'excerpt: ""',
        "draft: false",
        f'images: "posts/{slug}_assets"',
        f'og_image: "posts/{slug}_assets/og.png"',
        "---",
        "",
    ]
    md = "\n".join(front) + content + "\n"
    gh_create_or_update_file(
        token, md_path, md.encode("utf8"), branch, f"chore: add post {slug}"
    )
    try:
        pr = gh_open_pr(
            token, branch, f"Add post: {title}", body=f"Auto-generated post {title}"
        )
        comment = (
            "This PR was created by the admin UI. It will be auto-merged when CI checks pass. "
            "If it doesn't merge automatically, check Actions → Automerge and the PR checks."
        )
        try:
            gh_post_comment(token, pr.get("number"), comment)
        except Exception:
            pass
    except Exception as exc:
        return PlainTextResponse(str(exc), status_code=500)
    return TEMPLATES.TemplateResponse(
        "pr_status.html",
        {
            "request": request,
            "pr_number": pr.get("number"),
            "pr_url": pr.get("html_url"),
            "pr_title": pr.get("title"),
        },
    )


@app.get("/admin/pr_status")
def pr_status(request: Request, pr_number: int, _auth=Depends(require_basic_auth)):
    token = request.session.get("github_token") or GITHUB_TOKEN
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No GitHub credentials available",
        )
    try:
        pr = gh_get_pr(token, pr_number)
    except Exception as exc:
        return JSONResponse({"error": str(exc)})
    merged = gh_is_pr_merged(token, pr_number)
    head_sha = pr.get("head", {}).get("sha")
    combined = None
    try:
        if head_sha:
            combined = gh_get_combined_status(token, head_sha)
    except Exception:
        combined = None
    resp = {"merged": merged, "state": pr.get("state"), "head_sha": head_sha}
    if combined:
        resp["combined_state"] = combined.get("status", {}).get("state")
        resp["checks"] = (
            combined.get("checks", {}).get("check_runs")
            if isinstance(combined.get("checks"), dict)
            else combined.get("checks")
        )
    return JSONResponse(resp)


@app.get("/auth/login")
def auth_login(request: Request):
    client_id = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    if not client_id:
        return HTMLResponse(
            "<p>OAuth not configured. Set GITHUB_OAUTH_CLIENT_ID and GITHUB_OAUTH_CLIENT_SECRET.</p>"
        )
    redirect = "http://127.0.0.1:8000/auth/callback"
    state = str(int(time.time()))
    request.session["oauth_state"] = state
    url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect}&scope=public_repo&state={state}"
    return RedirectResponse(url)


@app.get("/auth/callback")
def auth_callback(
    request: Request, code: Optional[str] = None, state: Optional[str] = None
):
    expected = request.session.get("oauth_state")
    if not code or state != expected:
        return HTMLResponse("<p>Invalid OAuth callback.</p>", status_code=400)
    client_id = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
    if not client_id or not client_secret:
        return HTMLResponse("<p>OAuth not fully configured.</p>", status_code=500)
    token_url = "https://github.com/login/oauth/access_token"
    r = requests.post(
        token_url,
        data={"client_id": client_id, "client_secret": client_secret, "code": code},
        headers={"Accept": "application/json"},
    )
    r.raise_for_status()
    data = r.json()
    access_token = data.get("access_token")
    if not access_token:
        return HTMLResponse("<p>Failed to obtain access token.</p>", status_code=500)
    request.session["github_token"] = access_token
    return RedirectResponse(url="/admin/new")


@app.get("/auth/logout")
def auth_logout(request: Request):
    request.session.pop("github_token", None)
    return RedirectResponse(url="/admin/new")
