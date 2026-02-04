#!/usr/bin/env bash
set -euo pipefail

# Development build script — use `uv` for local builds
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Preparing build output directory"
rm -rf dist
mkdir -p dist

echo "Building sdist and wheel (local)"
uv build

echo "Build artifacts placed in dist/"
