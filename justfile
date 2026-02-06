# justfile - placed in your project root

# Setup the development environment (dev deps only by default)
setup:
    ./scripts/ci/setup-env.sh

# Sync all dependency groups
sync:
    ./scripts/ci/setup-env.sh --all-groups

# Build and install the package in development mode
build:
    uv build

# Clean build artifacts
clean:
    rm -rf build dist src/lieplusplus.egg-info .pytest_cache .ruff_cache __pycache__ .venv
    uv clean

# Run the basic usage example
example:
    uv run python examples/basic_usage.py

# Run pre-commit checks
pre-commit:
    ./scripts/ci/pre-commit.sh

# Run lint checks
lint:
    ./scripts/ci/lint.sh

# Run type checks
typecheck:
    ./scripts/ci/typecheck.sh

# Run the full local CI pipeline
ci-local:
    ./scripts/ci/run_locally.sh

# Test CI workflow locally with act
act:
    ./scripts/ci/test_workflows.sh

# Run tests (fast, no coverage)
test:
    ./scripts/ci/test.sh

# Run security scans
security:
    ./scripts/ci/semgrep.sh
    ./scripts/ci/trufflehog.sh

# Start the documentation server (installs docs deps on demand)
docs:
    ./scripts/ci/setup-env.sh --groups dev,docs
    uv run mkdocs serve

# Build documentation
docs-build:
    ./scripts/ci/setup-env.sh --groups dev,docs
    uv run mkdocs build

# Full CI simulation (do this before pushing!)
check-all: lint test
    uv run ty check
