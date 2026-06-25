#!/usr/bin/env bash
# Consumer-side: verify platform handoff was read; compare CHANGELOG to last-seen marker.
#
# Install via term-prep-platform:
#   ../term-prep-platform/scripts/cross_repo/install_consumer_scripts.sh
#
# Usage (from techdev-cursor root):
#   ./scripts/platform-handoff/check-handoff.sh
#   ./scripts/platform-handoff/check-handoff.sh --mark-seen

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PLATFORM_ROOT="${TERM_PREP_PLATFORM_ROOT:-$REPO_ROOT/../term-prep-platform}"
CHANGELOG="${PLATFORM_ROOT}/meta/consumer-handoff/CHANGELOG.md"
SEEN_FILE="${REPO_ROOT}/meta/.platform-handoff-last-seen"
WORKFLOW="${PLATFORM_ROOT}/meta/consumer-handoff/06-cross-repo-workflow.md"

MARK_SEEN=0
if [[ "${1:-}" == "--mark-seen" ]]; then
  MARK_SEEN=1
fi

if [[ ! -f "$CHANGELOG" ]]; then
  echo "error: platform CHANGELOG not found: $CHANGELOG" >&2
  echo "Set TERM_PREP_PLATFORM_ROOT or clone sibling term-prep-platform" >&2
  exit 1
fi

LATEST="$(python3 "${PLATFORM_ROOT}/scripts/cross_repo/handoff_changelog.py" id)"

if [[ "$MARK_SEEN" -eq 1 ]]; then
  mkdir -p "$(dirname "$SEEN_FILE")"
  printf '%s\n' "$LATEST" > "$SEEN_FILE"
  echo "marked seen: $LATEST"
  exit 0
fi

echo "platform handoff latest: $LATEST"
echo "read pack: ${PLATFORM_ROOT}/meta/consumer-handoff/README.md"

if [[ -f "$WORKFLOW" ]]; then
  echo "workflow:  ${WORKFLOW}"
fi

if [[ ! -f "$SEEN_FILE" ]]; then
  echo ""
  echo "status: NEW — no meta/.platform-handoff-last-seen yet"
  echo "action: read consumer-handoff README → 05 → 04; open consumer PR if needed"
  echo "        then: $0 --mark-seen"
  exit 2
fi

SEEN="$(tr -d '\n' < "$SEEN_FILE")"
if [[ "$SEEN" == "$LATEST" ]]; then
  echo "status: OK — consumer marked seen through: $SEEN"
  exit 0
fi

echo ""
echo "status: STALE — last seen: $SEEN"
echo "action: read CHANGELOG + 04-consumer-pr-guide; update consumer PR or request-platform-change.sh"
exit 1
