# justfile - placed in your project root

# Setup the development environment
setup:
    ./scripts/ci/setup-env.sh

# Sync dependencies
sync:
    uv sync --all-groups

# Build and install the package in development mode
build:
    uv build

# Clean build artifacts
clean:
    rm -rf build dist src/lieplusplus.egg-info .pytest_cache .ruff_cache __pycache__

# Run the basic usage example
example:
    uv run python examples/basic_usage.py

# Run pre-commit checks
pre-commit:
    ./scripts/ci/pre-commit.sh

# Run type checks
typecheck:
    ./scripts/ci/typecheck.sh

# Run the full local CI pipeline
ci-local:
    ./scripts/ci/run_locally.sh

# Run the full linting suite
lint:
    uv run ruff check --fix .
    uv run ruff format .

# Run tests with coverage
test:
    uv run pytest --cov=src

# Start the documentation server
docs:
    uv run mkdocs serve

# Full CI simulation (do this before pushing!)
check-all: lint test
    uv run ty check
