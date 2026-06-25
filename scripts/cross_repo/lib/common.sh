# shellcheck shell=bash
# Shared helpers for platform ↔ consumer cross-repo scripts.

cross_repo_platform_root() {
  local root
  root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
  printf '%s' "$root"
}

cross_repo_consumer_repo() {
  printf '%s' "${CONSUMER_REPO:-wombat2006/techdev-cursor}"
}

cross_repo_platform_repo() {
  printf '%s' "${PLATFORM_REPO:-wombat2006/term-prep-platform}"
}

cross_repo_consumer_root() {
  if [[ -n "${CONSUMER_ROOT:-}" ]]; then
    printf '%s' "$CONSUMER_ROOT"
    return 0
  fi
  if [[ -n "${TECHDEV_CURSOR_ROOT:-}" ]]; then
    printf '%s' "$TECHDEV_CURSOR_ROOT"
    return 0
  fi
  local sibling
  sibling="$(cross_repo_platform_root)/../techdev-cursor"
  if [[ -d "$sibling/.git" ]]; then
    printf '%s' "$(cd "$sibling" && pwd)"
    return 0
  fi
  return 1
}

cross_repo_gh_token() {
  if [[ -n "${CROSS_REPO_GH_TOKEN:-}" ]]; then
    printf '%s' "$CROSS_REPO_GH_TOKEN"
    return 0
  fi
  if [[ -n "${GH_TOKEN:-}" ]]; then
    printf '%s' "$GH_TOKEN"
    return 0
  fi
  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    printf '%s' "$GITHUB_TOKEN"
    return 0
  fi
  return 1
}

cross_repo_require_gh() {
  if ! command -v gh >/dev/null 2>&1; then
    echo "error: gh CLI not found — install https://cli.github.com/" >&2
    return 1
  fi
  if ! cross_repo_gh_token >/dev/null; then
    echo "error: set CROSS_REPO_GH_TOKEN (or GH_TOKEN) with issues:write on target repo" >&2
    return 1
  fi
  return 0
}

cross_repo_handoff_changelog() {
  printf '%s/meta/consumer-handoff/CHANGELOG.md' "$(cross_repo_platform_root)"
}

cross_repo_latest_handoff_id() {
  python3 "$(cross_repo_platform_root)/scripts/cross_repo/handoff_changelog.py" id
}

cross_repo_latest_handoff_summary() {
  python3 "$(cross_repo_platform_root)/scripts/cross_repo/handoff_changelog.py" summary
}

cross_repo_latest_handoff_body() {
  python3 "$(cross_repo_platform_root)/scripts/cross_repo/handoff_changelog.py" body
}
