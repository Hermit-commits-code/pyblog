# pyblog

Minimal bootstrap and developer instructions.

Setup:

```bash
python -m pip install --upgrade pip
python -m pip install poetry
poetry install
poetry run pre-commit install
```

Run checks:

```bash
poetry run pre-commit run --all-files
poetry run pytest
poetry run towncrier build --draft --version 0.0.0
```

Testing
-------

This repository includes a tiny placeholder test at `tests/test_smoke.py` to ensure CI runs without failing when you don't yet have a test suite. Remove or replace this file when you add real tests. The CI workflow also skips `pytest` automatically if no test files are present.

To add tests, create files under `tests/` named `test_*.py` or `*_test.py` and run:

```bash
poetry run pytest -q
```
