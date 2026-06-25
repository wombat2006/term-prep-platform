#!/usr/bin/env bash
# Consumer-side: open GitHub Issue on term-prep-platform requesting a platform change.
#
# Usage (from techdev-cursor root):
#   export GH_TOKEN=...   # or CROSS_REPO_GH_TOKEN
#   ./scripts/platform-handoff/request-platform-change.sh \
#     --title "cap max_candidates_output" \
#     --body-file /tmp/body.md
#
# Interactive:
#   ./scripts/platform-handoff/request-platform-change.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PLATFORM_ROOT="${TERM_PREP_PLATFORM_ROOT:-$REPO_ROOT/../term-prep-platform}"
PLATFORM_REPO="${PLATFORM_REPO:-wombat2006/term-prep-platform}"
CONSUMER_REPO="${CONSUMER_REPO:-wombat2006/techdev-cursor}"
LABEL="${PLATFORM_REQUEST_LABEL:-consumer-request}"

TITLE=""
BODY_FILE=""
BODY=""

usage() {
  echo "usage: $0 --title TITLE [--body TEXT | --body-file PATH]" >&2
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title)
      TITLE="${2:-}"
      shift 2
      ;;
    --body)
      BODY="${2:-}"
      shift 2
      ;;
    --body-file)
      BODY_FILE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "unknown arg: $1" >&2
      usage
      ;;
  esac
done

if [[ -z "$TITLE" ]]; then
  read -r -p "Issue title: " TITLE
fi

if [[ -n "$BODY_FILE" ]]; then
  BODY="$(cat "$BODY_FILE")"
elif [[ -z "$BODY" ]]; then
  echo "Enter body (end with Ctrl-D):"
  BODY="$(cat)"
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI required" >&2
  exit 1
fi

TOKEN="${CROSS_REPO_GH_TOKEN:-${GH_TOKEN:-${GITHUB_TOKEN:-}}}"
if [[ -z "$TOKEN" ]]; then
  echo "error: set CROSS_REPO_GH_TOKEN or GH_TOKEN" >&2
  exit 1
fi

HANDOFF_STATUS="${REPO_ROOT}/meta/TERM_PREP_PLATFORM_STATUS.md"
LATEST="unknown"
if [[ -f "${PLATFORM_ROOT}/meta/consumer-handoff/CHANGELOG.md" ]]; then
  LATEST="$(python3 "${PLATFORM_ROOT}/scripts/cross_repo/handoff_changelog.py" id 2>/dev/null || echo unknown)"
fi

FULL_BODY="$(cat <<EOF
## Consumer change request

**From consumer:** \`${CONSUMER_REPO}\`
**Platform handoff last entry:** ${LATEST}

### Request

${BODY}

### Consumer context

- Config: \`meta/glossary-config.json\`
- Boundary: \`meta/platform-integration/README.md\`
- Status shim: \`meta/TERM_PREP_PLATFORM_STATUS.md\` (if present)

### Expected platform response

1. Implement on term-prep-platform (not consumer)
2. Update \`meta/consumer-handoff/CHANGELOG.md\`
3. Bot opens new consumer notification issue (workflow C)

---
*Opened by \`scripts/platform-handoff/request-platform-change.sh\` on consumer.*
EOF
)"

export GH_TOKEN="$TOKEN"

URL="$(gh issue create \
  --repo "$PLATFORM_REPO" \
  --title "[consumer-request] ${TITLE}" \
  --body "$FULL_BODY" \
  --label "$LABEL" 2>/dev/null || gh issue create \
  --repo "$PLATFORM_REPO" \
  --title "[consumer-request] ${TITLE}" \
  --body "$FULL_BODY")"

echo "created: $URL"
