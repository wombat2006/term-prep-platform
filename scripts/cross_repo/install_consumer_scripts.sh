#!/usr/bin/env bash
# Copy consumer-side handoff scripts into a local techdev-cursor clone (for consumer PR branch).
#
# Does NOT commit or push — run from consumer repo after copy:
#   git add scripts/platform-handoff && git commit ...
#
# Usage:
#   CONSUMER_ROOT=../techdev-cursor ./scripts/cross_repo/install_consumer_scripts.sh
#   ./scripts/cross_repo/install_consumer_scripts.sh --dry-run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

PLATFORM_ROOT="$(cross_repo_platform_root)"
if ! CONSUMER_ROOT="$(cross_repo_consumer_root)"; then
  echo "error: set CONSUMER_ROOT or TECHDEV_CURSOR_ROOT (sibling ../techdev-cursor)" >&2
  exit 1
fi

SRC="${PLATFORM_ROOT}/scripts/cross_repo/consumer-templates"
DEST="${CONSUMER_ROOT}/scripts/platform-handoff"

if [[ ! -d "$SRC" ]]; then
  echo "error: templates not found: $SRC" >&2
  exit 1
fi

echo "install: $SRC -> $DEST"

if [[ "$DRY_RUN" -eq 1 ]]; then
  find "$SRC" -type f | while read -r f; do
    rel="${f#"$SRC"/}"
    echo "  would copy: $rel"
  done
  exit 0
fi

mkdir -p "$DEST"
cp -a "$SRC/." "$DEST/"
chmod +x "$DEST"/*.sh 2>/dev/null || true

echo "ok: consumer scripts at $DEST"
echo "next: in techdev-cursor, include in PR per meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md"
