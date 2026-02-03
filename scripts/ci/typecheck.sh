#!/usr/bin/env bash
set -euo pipefail

# Fast-fail type checking using `uv` environment
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running typing checks (fast-fail)"
# repo declares `ty` in dev dependencies; use it
uv run ty check

echo "Typing checks done"
