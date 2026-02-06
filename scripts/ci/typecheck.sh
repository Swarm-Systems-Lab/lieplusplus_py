#!/usr/bin/env bash
set -euo pipefail

# Run typing checks sequentially after venv bootstrap
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

. "${ROOT_DIR}/scripts/ci/_env.sh"
activate_venv

echo "Running typing checks"
uv run ty check
echo "Typing checks done"
