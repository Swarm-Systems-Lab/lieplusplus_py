# justfile - placed in your project root

# Setup the development environment (dev deps only by default)
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! command -v ssl-pydev >/dev/null 2>&1; then
        uv tool install ssl_pydev
    fi
    if ! command -v ssl-pydev >/dev/null 2>&1; then
        echo "error: ssl-pydev was installed but is not on PATH." >&2
        echo "check https://github.com/Swarm-Systems-Lab/ssl_pydev#install" >&2
        exit 1
    fi
    uv lock
    ssl-pydev setup-env --extras dev,lint,tests,type-checking,pre-commit

# Sync all dependency groups
sync:
    uv sync --frozen --all-extras

# Prune files not in template (run after copier update)
template-prune:
    python3 scripts/template_prune.py

# Build and install the package in development mode
build:
    uv build

# Build wheels (cibuildwheel) for release
build-release:
    ssl-pydev build-native

# Publish artifacts with uv (requires UV_PUBLISH_* env vars)
publish:
    ssl-pydev publish

# Publish artifacts with twine (CI-friendly; requires TWINE_* env vars)
publish-ci:
    ssl-pydev publish-ci

# Clean build artifacts
clean:
    rm -rf build dist src/lieplusplus.egg-info .pytest_cache .ruff_cache __pycache__ .venv site cov.xml .coverage .tox

# Run the basic usage example
example:
    uv run python examples/basic_usage.py

# Run pre-commit checks
pre-commit:
    uv run pre-commit run --all-files --show-diff-on-failure

# Run lint checks
lint:
    uv run ruff format .
    uv run ruff check . --fix

# Run type checks
typecheck:
    uv run ty check src/lieplusplus

# Run tests (fast, no coverage)
test:
    uv run tox -e tests

# Run tests in parallel, skip slow tests (fast)
test-fast:
    uv run tox -e tests-fast

# Run specific test
test-one TEST:
    uv run pytest tests/ -v -k

# Run tests across multiple Python versions
test-multi-py:
    uv run tox -e py312,py313,py314

# List all tox environments
list:
    uv run tox list

# Run security scans
security:
    uv run semgrep --config p/ci --config .semgrep.yml


# Start the documentation server (serves while watching for changes)
docs:
    uv run --with '.[docs]' mkdocs serve --livereload

# Build documentation
docs-build:
    uv run tox -e docs


# Full CI simulation (do this before pushing!)
check-all: lint security test
    uv run tox -e type-checking
    uv run tox -e pre-commit

# Clean documentation build artifacts
clean-docs:
    rm -rf site

# Validate built documentation
validate-docs:
    ssl-pydev validate-docs

# Regenerate pybind11 type stubs (run after changing src/bindings.cpp)
generate-stubs:
    ssl-pydev generate-stubs --module lieplusplus._core --output src/
