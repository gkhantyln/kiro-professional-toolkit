---
name: setup-python-package
description: Production PyPI package with hatch, src layout, type stubs, semantic versioning, automated changelog, and CI/CD publish pipeline
---

# Setup Python Package

Production-ready PyPI paketi kurar:
- src layout + hatch build
- Full type annotations + py.typed
- Semantic versioning (commitizen)
- Automated changelog (git-cliff)
- GitHub Actions publish pipeline
- Pre-commit hooks
- Docs (mkdocs-material)

## Usage
```
#setup-python-package <package-name>
```

## pyproject.toml
```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "mypackage"
dynamic = ["version"]
description = "A production-ready Python package"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.11"
keywords = ["python", "library"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Typing :: Typed",
]
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov", "mypy>=1.10", "ruff>=0.4", "pre-commit"]
docs = ["mkdocs-material>=9", "mkdocstrings[python]>=0.25"]

[tool.hatch.version]
source = "vcs"

[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]

[tool.hatch.envs.default]
dependencies = ["pytest>=8", "pytest-cov", "mypy>=1.10", "ruff>=0.4"]

[tool.hatch.envs.default.scripts]
test = "pytest {args:tests} --cov=mypackage --cov-report=term-missing"
typecheck = "mypy src/mypackage"
lint = "ruff check src/ tests/ && ruff format --check src/ tests/"
fmt = "ruff format src/ tests/ && ruff check --fix src/ tests/"
all = ["lint", "typecheck", "test"]

[tool.hatch.envs.docs]
dependencies = ["mkdocs-material>=9", "mkdocstrings[python]>=0.25"]
[tool.hatch.envs.docs.scripts]
serve = "mkdocs serve"
build = "mkdocs build"

[tool.ruff]
line-length = 100
target-version = "py311"
[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "ANN", "S", "B", "A", "C4", "PT", "RUF"]
ignore = ["ANN101", "ANN102"]
[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "ANN"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--strict-markers", "--tb=short"]

[tool.commitizen]
name = "cz_conventional_commits"
version_provider = "scm"
tag_format = "v$version"
update_changelog_on_bump = true
```

## src/mypackage/__init__.py
```python
"""mypackage — A production-ready Python library."""
from __future__ import annotations

from mypackage._version import __version__
from mypackage.core import MyClass

__all__ = ["__version__", "MyClass"]
```

## src/mypackage/py.typed
```
# PEP 561 marker — this package ships type information
```

## src/mypackage/core.py
```python
from __future__ import annotations

from typing import Generic, TypeVar, overload
from collections.abc import Iterator

T = TypeVar("T")
S = TypeVar("S", bound="MyClass")

class MyClass(Generic[T]):
    """Core class with full type annotations.

    Example:
        >>> obj = MyClass(value=42)
        >>> obj.value
        42
    """

    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    @overload
    def transform(self: MyClass[int], factor: int) -> MyClass[int]: ...
    @overload
    def transform(self: MyClass[str], factor: int) -> MyClass[str]: ...

    def transform(self, factor: int) -> MyClass:
        if isinstance(self._value, int):
            return MyClass(self._value * factor)
        if isinstance(self._value, str):
            return MyClass(self._value * factor)
        raise TypeError(f"Cannot transform {type(self._value)}")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(value={self._value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MyClass):
            return NotImplemented
        return self._value == other._value
```

## .github/workflows/publish.yml
```yaml
name: Publish to PyPI

on:
  push:
    tags: ["v*"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install hatch
      - run: hatch build
      - uses: actions/upload-artifact@v4
        with: { name: dist, path: dist/ }

  test-matrix:
    needs: build
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python-version }}" }
      - run: pip install hatch && hatch run all

  publish:
    needs: [build, test-matrix]
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write  # OIDC trusted publishing
    steps:
      - uses: actions/download-artifact@v4
        with: { name: dist, path: dist/ }
      - uses: pypa/gh-action-pypi-publish@release/v1
        # No API token needed — uses OIDC trusted publishing
```

## .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.27.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```
