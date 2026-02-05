#!/usr/bin/env bash
set -euo pipefail

# Development build script — assumes the shared venv is active
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"
. .venv/bin/activate

echo "Preparing build output directory"
rm -rf dist
mkdir -p dist

echo "Building sdist and wheel (local)"
uv build

echo "Build artifacts placed in dist/"
