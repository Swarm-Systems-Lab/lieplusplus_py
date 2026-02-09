#!/usr/bin/env bash
set -euo pipefail

# Shared environment bootstrap using uv for venv management.
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

GROUP_LIST=("dev")
FROZEN=1
EXTRA_PACKAGES=()

usage() {
	echo "Usage: $0 [--groups <comma-separated>] [--all-groups] [--no-frozen] [--with <pkg> ...]" >&2
	exit 1
}

while [[ $# -gt 0 ]]; do
	case "$1" in
		--groups)
			[[ $# -ge 2 ]] || usage
			IFS=',' read -r -a GROUP_LIST <<< "$2"
			shift 2
			;;
		--all-groups)
			GROUP_LIST=()
			shift
			;;
		--no-frozen)
			FROZEN=0
			shift
			;;
		--with)
			[[ $# -ge 2 ]] || usage
			EXTRA_PACKAGES+=("$2")
			shift 2
			;;
		*)
			usage
			;;
	esac
done

# Install uv if not available
if ! command -v uv >/dev/null 2>&1; then
	curl -LsSf https://astral.sh/uv/install.sh | sh
	export PATH="$HOME/.local/bin:$PATH"
fi

# Create uv-managed venv if it doesn't exist
if [ ! -d .venv ]; then
	uv venv .venv
fi

# Activate and sync dependencies
. .venv/bin/activate

SYNC_ARGS=(sync)
((FROZEN)) && SYNC_ARGS+=("--frozen")

if [ ${#GROUP_LIST[@]} -eq 0 ]; then
	SYNC_ARGS+=("--all-groups")
else
	for group in "${GROUP_LIST[@]}"; do
		SYNC_ARGS+=("--group" "$group")
	done
fi

uv "${SYNC_ARGS[@]}"

if [ ${#EXTRA_PACKAGES[@]} -gt 0 ]; then
	uv add "${EXTRA_PACKAGES[@]}"
fi
