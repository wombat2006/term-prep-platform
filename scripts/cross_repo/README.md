# Cross-repo scripts (platform ↔ consumer)

**Workflow doc:** [meta/consumer-handoff/06-cross-repo-workflow.md](../meta/consumer-handoff/06-cross-repo-workflow.md)

## Platform bot (step C)

```bash
# Requires PAT with issues:write on consumer repo
export CROSS_REPO_GH_TOKEN=ghp_...
./scripts/cross_repo/notify_consumer_issue.sh
./scripts/cross_repo/notify_consumer_issue.sh --dry-run
```

Triggered automatically on push to `main` when `meta/consumer-handoff/**` changes (see `.github/workflows/consumer-handoff-notify.yml`).

## Prepare consumer PR branch (step A helper)

```bash
export CONSUMER_ROOT=../techdev-cursor
./scripts/cross_repo/install_consumer_scripts.sh
# Then in consumer: apply 04-consumer-pr-guide + commit scripts/platform-handoff/
```

## Consumer templates

Source: [consumer-templates/](./consumer-templates/) — installed to `techdev-cursor/scripts/platform-handoff/`.

| Script | Run from consumer |
|--------|-------------------|
| `check-handoff.sh` | Detect new platform handoff vs `meta/.platform-handoff-last-seen` |
| `request-platform-change.sh` | Open Issue on term-prep-platform |

## Env

| Variable | Default |
|----------|---------|
| `CONSUMER_REPO` | `wombat2006/techdev-cursor` |
| `PLATFORM_REPO` | `wombat2006/term-prep-platform` |
| `CONSUMER_ROOT` / `TECHDEV_CURSOR_ROOT` | sibling `../techdev-cursor` |
| `CROSS_REPO_GH_TOKEN` | PAT for cross-repo `gh issue create` |
