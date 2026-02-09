#!/usr/bin/env bash
set -euo pipefail

# Run pre-commit after the shared env bootstrap step
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

. "${ROOT_DIR}/scripts/ci/_env.sh"
activate_venv

echo "Running pre-commit"
uv run pre-commit run --all-files --show-diff-on-failure
echo "pre-commit checks passed"
