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
