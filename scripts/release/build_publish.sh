#!/usr/bin/env bash
set -euo pipefail

# CI/publish build script — relies on the shared venv for tooling
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"
. .venv/bin/activate

echo "Preparing build output directory"
rm -rf dist
mkdir -p dist

echo "Building sdist"
python -m build --sdist --outdir dist

echo "Building wheels with cibuildwheel"
python -m cibuildwheel --output-dir dist

echo "Build artifacts placed in dist/"
