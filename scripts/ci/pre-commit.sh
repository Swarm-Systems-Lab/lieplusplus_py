#!/usr/bin/env bash
set -euo pipefail

# Minimal fast-fail pre-commit runner: assume `uv` and tools are available.
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running pre-commit (fast-fail)"
uv run pre-commit run --all-files --show-diff-on-failure

echo "pre-commit checks passed"
