#!/usr/bin/env bash
set -euo pipefail

# CI helper to run TruffleHog in repo/PR scan mode and fail on findings.
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

. "${ROOT_DIR}/scripts/ci/_env.sh"
activate_venv

echo "Running trufflehog scan (git mode, limited depth)..."

EXCLUDES_FILE="${ROOT_DIR}/scripts/ci/trufflehog_excludes.txt"

# Run a fast scan over recent commits / current working tree. Limit depth to avoid long CI times.
if [ -f "$EXCLUDES_FILE" ]; then
  echo "Using trufflehog excludes: $EXCLUDES_FILE"
  uv run trufflehog --json --max_depth 50 -x "$EXCLUDES_FILE" . > trufflehog-results.json || true
else
  uv run trufflehog --json --max_depth 50 . > trufflehog-results.json || true
fi

if [ -s trufflehog-results.json ]; then
  # Detect likely findings (non-empty JSON with results)
  if jq '. | length > 0' trufflehog-results.json >/dev/null 2>&1; then
    echo "TruffleHog found potential secrets (first 200 lines):" >&2
    head -n 200 trufflehog-results.json >&2
    exit 1
  fi
fi

echo "TruffleHog scan complete, no high-confidence secrets found."
