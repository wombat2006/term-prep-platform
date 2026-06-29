---
name: consumer-handoff
description: Update platform consumer-handoff docs and package contract guidance after platform work affecting techdev-cursor. Use when the user mentions consumer handoff, consumer PR, package pin, or schema/CLI contract updates.
disable-model-invocation: true
---

# Consumer handoff (term-prep-platform → techdev-cursor)

## Goal

After platform work that affects consumers, keep **canonical status on platform** and publish
package-contract guidance. **Do not edit techdev-cursor** from this repo.

## Non-negotiables

- **Do not** commit to `techdev-cursor` — consumer maintainer opens PR using [04-consumer-pr-guide-techdev-cursor.md](../../../meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md).
- **Do not** duplicate full handoff tree into consumer.
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
| 5 | `meta/consumer-handoff/06-cross-repo-workflow.md` (deprecated reference) |
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
3. **Update package contract guidance**:
   - `pyproject.toml` version / entrypoints
   - `02-schema-and-cli.md` command surface
   - `04-consumer-pr-guide-techdev-cursor.md` PR template
4. **Tell the user** to open consumer PR per `04` and bump package pin.

## Output format (when user asks for handoff summary)

Return:

1. **Ownership** — what platform did vs what consumer must do.
2. **Files updated** on platform (handoff paths).
3. **Consumer PR checklist** — bullet list from `04` (no full duplicate of 04).
4. **Verification commands** — package entrypoint checks (`term-prep-*`), `run_phase05_checks.sh`.

## Escalation (consumer → platform)

If user reports consumer breakage after pin bump, treat it as contract regression, fix platform, and update CHANGELOG + cutover guide.
