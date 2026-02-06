%20
%23%20pyblog

%5B%21%5BCI%5D%28https%3A%2F%2Fgithub.com%2FHermit-commits-code%2Fpyblog%2Factions%2Fworkflows%2Fci.yml%2Fbadge.svg%29%28https%3A%2F%2Fgithub.com%2FHermit-commits-code%2Fpyblog%2Factions%2Fworkflows%2Fci.yml%29
%5B%21%5BRelease%5D%28https%3A%2F%2Fimg.shields.io%2Fgithub%2Fv%2Frelease%2FHermit-commits-code%2Fpyblog%3Flabel%3Drelease%29%28https%3A%2F%2Fgithub.com%2FHermit-commits-code%2Fpyblog%2Freleases%29
%5B%21%5BPython%5D%28https%3A%2F%2Fimg.shields.io%2Fbadge%2Fpython-3.11%2520%257C%25203.12-blue.svg%29%28https%3A%2F%2Fwww.python.org%2F%29
%5B%21%5BLicense%5D%28https%3A%2F%2Fimg.shields.io%2Fbadge%2Flicense-Unspecified-lightgrey.svg%29%28https%3A%2F%2Fgithub.com%2FHermit-commits-code%2Fpyblog%29

%3E%20PyBlog%20%E2%80%94%20developer%20blog%20project.%20This%20repository%20bootstraps%20developer%20tooling%20%28Poetry%2C%20pre-commit%2C%20Commitizen%2C%20Towncrier%29%20and%20a%20minimal%20CI%2Frelease%20flow.

# pyblog

[![CI](https://github.com/Hermit-commits-code/pyblog/actions/workflows/ci.yml/badge.svg)](https://github.com/Hermit-commits-code/pyblog/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Hermit-commits-code/pyblog?label=release)](https://github.com/Hermit-commits-code/pyblog/releases)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Unspecified-lightgrey.svg)](https://github.com/Hermit-commits-code/pyblog)

> PyBlog — developer blog project. This repository bootstraps developer tooling (Poetry, pre-commit, Commitizen, Towncrier) and a minimal CI/release flow.

## Setup

```bash
python -m pip install --upgrade pip
python -m pip install poetry
poetry install
poetry run pre-commit install
```

## Run checks

```bash
poetry run pre-commit run --all-files
poetry run pytest
poetry run towncrier build --draft --version 0.0.0
```

## Testing

There is a tiny placeholder test at `tests/test_smoke.py` so CI doesn't fail when you don't yet have a test suite. Replace or remove this file when you add real tests.

To add tests, create files under `tests/` named `test_*.py` or `*_test.py` and run:

```bash
poetry run pytest -q
```

## Contributing

- Use `commitizen` for conventional commit messages (run `cz commit`).
- Open issues/PRs for features and fixes.

## Next steps

- Consider adding a `CONTRIBUTING.md` and a CI badge that points to coverage/quality checks.
