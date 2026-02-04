#!/usr/bin/env bash
set -euo pipefail

# Fast-fail type checking using `uv` environment
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running typing checks (fast-fail)"
if [ -f .venv/bin/activate ]; then
	. .venv/bin/activate
fi

if command -v uv >/dev/null 2>&1; then
	uv run ty check
else
	python -m ty check
fi

echo "Typing checks done"
