# Release process (short)

1. Prepare a feature branch and ensure PR passes CI (pre-commit, tests, towncrier draft).
2. Merge to `main` (squash preferred).
3. Run the release workflow (Actions → Release → Run workflow) and enter the version (e.g. `0.1.0`).
4. The workflow will build the changelog, commit `CHANGELOG.md`, tag the release and create a GitHub Release.

Local alternative:

```bash
poetry run towncrier build --yes --version 0.1.0
git add CHANGELOG.md
git commit -m "chore(release): v0.1.0"
git tag -a v0.1.0 -m "v0.1.0"
git push origin HEAD
git push origin --tags
```
