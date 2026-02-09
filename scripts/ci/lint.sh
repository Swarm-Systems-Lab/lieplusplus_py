#!/usr/bin/env bash
set -euo pipefail

# Run linting and formatting checks after venv bootstrap
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

. "${ROOT_DIR}/scripts/ci/_env.sh"
activate_venv

echo "Running ruff check"
uv run ruff check .

echo "Running ruff format"
uv run ruff format .

echo "Linting complete"
