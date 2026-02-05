#!/usr/bin/env bash
set -euo pipefail

# Shared environment bootstrap using uv for venv management.
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

# Install uv if not available
if ! command -v uv >/dev/null 2>&1; then
	curl -LsSf https://astral.sh/uv/install.sh | sh
	export PATH="$HOME/.local/bin:$PATH"
fi

# Create uv-managed venv if it doesn't exist
if [ ! -d .venv ]; then
	uv venv .venv
fi

# Activate and sync dependencies
. .venv/bin/activate
uv sync --frozen --only-group dev

if [ "$#" -gt 0 ]; then
	uv add "$@"
fi
