#!/usr/bin/env bash
# Open (or skip duplicate) GitHub Issue on consumer repo — workflow step C of A+C hybrid.
#
# Usage:
#   export CROSS_REPO_GH_TOKEN=ghp_...   # issues:write on consumer repo
#   ./scripts/cross_repo/notify_consumer_issue.sh
#   ./scripts/cross_repo/notify_consumer_issue.sh --dry-run
#
# Env:
#   CONSUMER_REPO     default wombat2006/techdev-cursor
#   PLATFORM_REPO     default wombat2006/term-prep-platform
#   CONSUMER_ISSUE_LABEL  default platform-handoff
#   PLATFORM_REF      git ref for links (default: HEAD short sha)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

if [[ "$DRY_RUN" -ne 1 ]]; then
  cross_repo_require_gh
fi

PLATFORM_ROOT="$(cross_repo_platform_root)"
CONSUMER_SLUG="$(cross_repo_consumer_repo)"
PLATFORM_SLUG="$(cross_repo_platform_repo)"
LABEL="${CONSUMER_ISSUE_LABEL:-platform-handoff}"
ENTRY_ID="$(cross_repo_latest_handoff_id)"
ENTRY_BODY="$(cross_repo_latest_handoff_body)"

PLATFORM_REF="${PLATFORM_REF:-$(git -C "$PLATFORM_ROOT" rev-parse --short HEAD 2>/dev/null || echo main)}"
HANDOFF_URL="https://github.com/${PLATFORM_SLUG}/blob/${PLATFORM_REF}/meta/consumer-handoff/README.md"
CHANGELOG_URL="https://github.com/${PLATFORM_SLUG}/blob/${PLATFORM_REF}/meta/consumer-handoff/CHANGELOG.md"
PR_GUIDE_URL="https://github.com/${PLATFORM_SLUG}/blob/${PLATFORM_REF}/meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md"
WORKFLOW_URL="https://github.com/${PLATFORM_SLUG}/blob/${PLATFORM_REF}/meta/consumer-handoff/06-cross-repo-workflow.md"

TITLE="[platform-handoff] ${ENTRY_ID}"

ISSUE_BODY="$(cat <<EOF
## Platform handoff notification (read-only)

term-prep-platform pushed an update that may affect **${CONSUMER_SLUG}**.

**Do not implement platform code in the consumer repo.** Review, then open a consumer PR if wiring is needed.

### Read first (platform — canonical)

| Step | Doc |
|------|-----|
| 0 | [consumer-handoff README](${HANDOFF_URL}) |
| 1 | [05-platform-implementation](https://github.com/${PLATFORM_SLUG}/blob/${PLATFORM_REF}/meta/consumer-handoff/05-platform-implementation.md) |
| 2 | [04-consumer-pr-guide](${PR_GUIDE_URL}) |
| 3 | [CHANGELOG entry](${CHANGELOG_URL}) |

### Latest CHANGELOG entry

${ENTRY_BODY}

### Consumer checklist

- [ ] Read platform docs above (steps 0–2)
- [ ] Decide: **no consumer change** / **consumer PR needed** / **platform change request**
- [ ] If consumer PR: follow [04-consumer-pr-guide](${PR_GUIDE_URL}) and run \`scripts/platform-handoff/check-handoff.sh\` after merge
- [ ] If platform change needed: \`scripts/platform-handoff/request-platform-change.sh\` (opens issue on platform)
- [ ] Close this issue when done or comment with links to consumer/platform PRs

### Workflow

[A+C hybrid (bot + manual PR)](${WORKFLOW_URL}) · platform ref \`${PLATFORM_REF}\`

---
*Opened by \`scripts/cross_repo/notify_consumer_issue.sh\` on term-prep-platform.*
EOF
)"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "dry-run: would create issue on $CONSUMER_SLUG"
  echo "title: $TITLE"
  echo "---"
  echo "$ISSUE_BODY"
  exit 0
fi

export GH_TOKEN
GH_TOKEN="$(cross_repo_gh_token)"

if gh issue list --repo "$CONSUMER_SLUG" --label "$LABEL" --state open --search "$ENTRY_ID" --limit 5 \
  | grep -q .; then
  echo "skip: open issue already exists for: $ENTRY_ID"
  exit 0
fi

URL="$(gh issue create \
  --repo "$CONSUMER_SLUG" \
  --title "$TITLE" \
  --body "$ISSUE_BODY" \
  --label "$LABEL" 2>/dev/null || gh issue create \
  --repo "$CONSUMER_SLUG" \
  --title "$TITLE" \
  --body "$ISSUE_BODY")"

echo "created: $URL"
