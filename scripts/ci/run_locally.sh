#!/usr/bin/env bash
set -euo pipefail

# Helper to run the CI job steps locally. Assumes `uv` and Docker (for wheels) are available.
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Syncing dependencies (frozen)"
uv sync --all-groups --frozen

echo "Running pre-commit checks"
./scripts/ci/pre-commit.sh

echo "Running tests"
./scripts/ci/test.sh

echo "Running type checks"
./scripts/ci/typecheck.sh

echo "Local CI run complete"

echo "If you want to simulate the GitHub Actions job runner use 'act' (https://github.com/nektos/act)"
echo "Example: install act and run: act -j fast-checks -P ubuntu-latest=nektos/act-environments-ubuntu:18.04"
