Branch protection guidance
=========================

Apply these settings in the GitHub repository Settings → Branches → Branch protection rules for `feat/bootstrap-ci` (or your deploy branch):

- Require pull request reviews before merging (1 or 2 reviews).
- Require status checks to pass before merging: add your CI job names (e.g., `ci`, `lint`, `test`).
- Require branches to be up to date before merging.
- Restrict who can push to matching branches (add a BOT account + admins only).
- Require signed commits (optional).
- Enable include administrators as needed.

You can apply protections via the REST API (requires `repo` scope and admin rights). Example curl:

```bash
curl -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/branches/feat/bootstrap-ci/protection \
  -d '{
    "required_status_checks": {"strict": true, "contexts": ["ci"]},
    "enforce_admins": true,
    "required_pull_request_reviews": {"required_approving_review_count": 1},
    "restrictions": null
  }'
```

If you want, I can attempt to apply this via a workflow run, but it requires an admin-scoped token stored in Secrets and is irreversible without credentials.
