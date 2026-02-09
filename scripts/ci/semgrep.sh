#!/usr/bin/env bash
set -euo pipefail

# CI helper to run semgrep with curated rulesets and fail on findings.
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

. "${ROOT_DIR}/scripts/ci/_env.sh"
activate_venv

echo "Running semgrep..."
uv run semgrep --config p/ci --json --output semgrep-results.json || true

if [ -s semgrep-results.json ]; then
  len=$(jq '.results | length' semgrep-results.json)
  if [ "$len" -gt 0 ]; then
    echo "Semgrep found $len issue(s):" >&2
    jq '.results[] | {check_id: .check_id, path: .path, start: .start, end: .end, extra: .extra}' semgrep-results.json >&2
    exit 1
  fi
fi

echo "Semgrep scan complete, no issues found."
