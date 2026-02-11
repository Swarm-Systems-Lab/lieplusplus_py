#!/usr/bin/env bash
set -euo pipefail

# CI/publish build script — relies on the shared venv for tooling
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
	./scripts/ci/setup-env.sh --extras dev,release
fi

. .venv/bin/activate

echo "Preparing build output directory"
rm -rf dist
mkdir -p dist

echo "Running tox build + cibuildwheel"
uv run tox -e build
uv run tox -e cibuildwheel

echo "Build artifacts placed in dist/"
