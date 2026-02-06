# Contributing to pyblog

Thank you for contributing! This file describes the preferred workflow and tools for contributions.

Guidelines
- Use `commitizen` for conventional commits. Run `cz commit` to craft commit messages.
- Keep changes small and focused. One logical change per PR.
- Add tests for new features or bug fixes.
- Ensure `pre-commit` hooks pass locally before opening a PR.

Local setup
```
python -m pip install --upgrade pip
python -m pip install poetry
poetry install
poetry run pre-commit install
```

Running checks locally
```
poetry run pre-commit run --all-files
poetry run pytest -q
```

Pull requests
- Branch from `main` and name branches meaningfully (e.g., `feat/login`, `fix/typo`).
- Open a PR against `main`. Describe the change, tests added, and any migration notes.
- Set reviewers and address feedback iteratively.

Code style
- Formatting: `black` (automatic via pre-commit).
- Linting: `ruff` (enforced via pre-commit).

Security & dependencies
- We run `pip-audit` in CI as a non-blocking scan. If it reports critical issues, open an issue and assign an owner.

Thanks for helping improve pyblog!
