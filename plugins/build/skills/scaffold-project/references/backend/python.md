# Python Backend Scaffold

## Package Manager: uv

Initialize with `uv init --lib <project-name>` then customize the generated `pyproject.toml`.

## pyproject.toml

```toml
[project]
name = "<project-name>"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.34",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=6.0",
    "ruff>=0.8",
    "pre-commit>=4.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "SIM"]

[tool.ruff.lint.isort]
known-first-party = ["<project_name>"]
```

## Project Structure

```
<project-name>/
├── src/<project_name>/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml
├── Makefile
├── .gitignore
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
└── CLAUDE.md
```

## Makefile

```makefile
.PHONY: install dev format lint test check

install:
	uv sync

dev:
	uv run uvicorn <project_name>.main:app --reload --port 8000

format:
	uv run ruff format src tests

lint:
	uv run ruff check src tests

test:
	uv run pytest -v

check: lint test
```

## .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: detect-private-key
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## .gitignore

```
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.venv/
.env
.pytest_cache/
.ruff_cache/
htmlcov/
.coverage
```

## .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run ruff check src tests
      - run: uv run ruff format --check src tests
      - run: uv run pytest -v
```

## src/<project_name>/main.py

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}
```

## tests/test_main.py

```python
from fastapi.testclient import TestClient

from <project_name>.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

## CLAUDE.md

```markdown
# CLAUDE.md

## Commands

\```bash
make install    # Install dependencies
make dev        # Start dev server (port 8000, auto-reload)
make format     # Format code with ruff
make lint       # Lint code with ruff
make test       # Run tests with pytest
make check      # Run lint + test
\```

## Architecture

FastAPI backend using uv for package management, ruff for linting/formatting, pytest for testing.

\```
src/<project_name>/
  main.py       # FastAPI app entry point
tests/
  test_main.py  # Tests
\```
```
