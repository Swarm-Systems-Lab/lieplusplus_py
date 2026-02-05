#!/usr/bin/env bash
set -euo pipefail

# Run pytest once the shared env is ready
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running tests"
. .venv/bin/activate
uv run pytest -v
echo "Tests finished"
