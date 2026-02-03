#!/usr/bin/env bash
set -euo pipefail

# Fast-fail test runner using uv-managed environment
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running tests (fast-fail)"
uv run pytest -v

echo "Tests finished"
