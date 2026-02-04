#!/usr/bin/env bash
set -euo pipefail

# CI/publish build script — use cibuildwheel for multi-version compatibility
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Preparing build output directory"
rm -rf dist
mkdir -p dist

echo "Building sdist"
python -m build --sdist --outdir dist

echo "Building wheels with cibuildwheel"
python -m cibuildwheel --output-dir dist

echo "Build artifacts placed in dist/"
