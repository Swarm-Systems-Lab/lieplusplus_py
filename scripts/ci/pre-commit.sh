#!/usr/bin/env bash
set -euo pipefail

# Run pre-commit after the shared env bootstrap step
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running pre-commit"
. .venv/bin/activate
uv run pre-commit run --all-files --show-diff-on-failure
echo "pre-commit checks passed"
