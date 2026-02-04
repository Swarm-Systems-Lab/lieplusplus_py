#!/usr/bin/env bash
set -euo pipefail

# Minimal fast-fail pre-commit runner: assume `uv` and tools are available.
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running pre-commit (fast-fail)"
if [ -f .venv/bin/activate ]; then
	. .venv/bin/activate
fi

if command -v uv >/dev/null 2>&1; then
	uv run pre-commit run --all-files --show-diff-on-failure
else
	# try running pre-commit if installed in current env
	pre-commit run --all-files --show-diff-on-failure
fi

echo "pre-commit checks passed"
