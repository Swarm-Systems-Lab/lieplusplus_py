#!/usr/bin/env bash
set -euo pipefail

# Run pytest once the shared env is ready
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

. "${ROOT_DIR}/scripts/ci/_env.sh"
activate_venv

echo "Running tests"
uv run pytest -v
echo "Tests finished"
