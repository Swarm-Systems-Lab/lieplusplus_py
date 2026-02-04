#!/usr/bin/env bash
set -euo pipefail

# Fast-fail test runner using uv-managed environment
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running tests (fast-fail)"
if [ -f .venv/bin/activate ]; then
	. .venv/bin/activate
fi

if command -v uv >/dev/null 2>&1; then
	uv run pytest -v
else
	# fallback to direct pytest if uv is not available
	python -m pytest -v
fi

echo "Tests finished"
