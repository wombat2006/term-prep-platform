---
name: consumer-handoff
description: Update platform consumer-handoff docs, CHANGELOG, and cross-repo bot notify after platform work affecting techdev-cursor. Use when the user mentions consumer handoff, consumer PR, notify_consumer_issue, or A+C cross-repo workflow.
disable-model-invocation: true
---

# Consumer handoff (term-prep-platform → techdev-cursor)

## Goal

After platform work that affects consumers, keep **canonical status on platform** and trigger the **A+C hybrid** workflow (bot Issue + consumer PR spec). **Do not edit techdev-cursor** from this repo.

## Non-negotiables

- **Do not** commit to `techdev-cursor` — consumer maintainer opens PR using [04-consumer-pr-guide-techdev-cursor.md](../../../meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md).
- **Do not** duplicate full handoff tree into consumer — pointers + `scripts/platform-handoff/` templates only (via consumer PR).
- **Never** implement Genspark / aidrive on platform unless user explicitly requests a new ADR.
- Read consumer boundary (sibling): `../techdev-cursor/meta/platform-integration/` when scope is unclear.

## Canonical docs (this repo)

| Step | File |
|------|------|
| 0 | `meta/consumer-handoff/README.md` |
| 1 | `meta/consumer-handoff/05-platform-implementation.md` |
| 2 | `meta/consumer-handoff/01-platform-status.md` |
| 3 | `meta/consumer-handoff/02-schema-and-cli.md` |
| 4 | `meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md` |
| 5 | `meta/consumer-handoff/06-cross-repo-workflow.md` |
| 6 | `meta/consumer-handoff/CHANGELOG.md` — **new entry at top** on every consumer-affecting change |

## Workflow

1. **Confirm what changed** on platform (code, schema, CLI, connectors).
2. **Update handoff pack** in one logical commit:
   - `CHANGELOG.md` — `## YYYY-MM-DD — title` at top
   - `01-platform-status.md` if phase status moved
   - `02-schema-and-cli.md` if contract changed
   - `04` if consumer PR file list changed
   - `05` if artifacts / flows changed
   - `meta/TODO.md` checkboxes
3. **Notify consumer (step C)** after push:
   ```bash
   export CROSS_REPO_GH_TOKEN=...
   ./scripts/cross_repo/notify_consumer_issue.sh --dry-run   # verify
   ./scripts/cross_repo/notify_consumer_issue.sh             # opens Issue on consumer
   ```
   Or rely on `.github/workflows/consumer-handoff-notify.yml` when `CROSS_REPO_GH_TOKEN` secret is set.
4. **Tell the user** to open consumer PR per `04` (or run `install_consumer_scripts.sh` to stage `scripts/platform-handoff/` into consumer clone).

## Output format (when user asks for handoff summary)

Return:

1. **Ownership** — what platform did vs what consumer must do.
2. **Files updated** on platform (handoff paths).
3. **Consumer PR checklist** — bullet list from `04` (no full duplicate of 04).
4. **Bot / verify commands** — dry-run notify, `run_phase05_checks.sh` if relevant.

## Escalation (consumer → platform)

If user pastes a consumer Issue from `request-platform-change.sh`, implement on platform, then repeat workflow above (CHANGELOG + notify).
