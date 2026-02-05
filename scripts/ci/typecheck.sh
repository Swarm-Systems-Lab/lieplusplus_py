#!/usr/bin/env bash
set -euo pipefail

# Run typing checks sequentially after venv bootstrap
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running typing checks"
. .venv/bin/activate
uv run ty check
echo "Typing checks done"
