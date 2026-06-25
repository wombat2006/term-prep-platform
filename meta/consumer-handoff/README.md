# Consumer handoff — platform progress & obligations

**Audience:** Agents and maintainers working in **techdev-cursor** (and other consumers)  
**Canonical location:** term-prep-platform only — consumer adds **pointers** here; do not mirror this tree into consumer unless the user requests it  
**Status:** Active (2026-06-21) — living status pack, not an ADR

---

## Purpose

techdev-cursor is the **consumer**; term-prep-platform is the **platform** (glossary extract, connectors, MCP).  
Consumer agents need a **read-only** view of platform progress, schema/CLI contract, and **pending consumer-side actions** — without editing this repo.

This directory is the **single entry** for that view. It complements consumer-owned [platform-integration](https://github.com/wombat2006/techdev-cursor/blob/master/meta/platform-integration/README.md) (boundary **into** platform work).

| Direction | Canonical pack | Who edits |
|-----------|----------------|-----------|
| Platform → consumer (status, schema, actions) | **This tree** (`meta/consumer-handoff/`) | term-prep-platform |
| Consumer → platform (boundary, Genspark, scope) | techdev-cursor `meta/platform-integration/` | techdev-cursor |

**Cross-repo policy:** Consumer agents **read** term-prep-platform (sibling clone). Platform agents **read** techdev-cursor. **Neither repo's agents edit the other repo** — consumer changes go through a **consumer PR** spec'd in [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md).

---

## Resolve term-prep-platform path (consumer side)

Use the first path that exists on your machine:

| Priority | Path | When |
|----------|------|------|
| 1 | `$TERM_PREP_PLATFORM_ROOT` | Env override (recommended in CI) |
| 2 | `../term-prep-platform` | Default sibling layout next to techdev-cursor |
| 3 | Clone | `https://github.com/wombat2006/term-prep-platform` |

All paths below are **relative to term-prep-platform repo root**.

---

## Mandatory read order (consumer work touching platform)

Read **in order** before changing `meta/glossary-config.json`, npm glossary scripts, MCP registration, or corpus paths.

| Step | File | Covers |
|------|------|--------|
| **0** | This file | Index, paths, policy |
| **1** | [05-platform-implementation.md](./05-platform-implementation.md) | **What platform built** — artifacts, flows, tests |
| **2** | [01-platform-status.md](./01-platform-status.md) | Phase progress · shipped vs planned |
| **3** | [02-schema-and-cli.md](./02-schema-and-cli.md) | Config schema, CLI/MCP surface |
| **4** | [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md) | **Consumer PR spec** (copy-paste; platform does not open PR) |
| **5** | [03-consumer-actions.md](./03-consumer-actions.md) | Obligations checklist |
| **6** | [CHANGELOG.md](./CHANGELOG.md) | Dated platform changes |
| **7** | [06-cross-repo-workflow.md](./06-cross-repo-workflow.md) | **A+C bot** Issue / PR coordination |

**Per-consumer summary:** [consumers/techdev-cursor.md](./consumers/techdev-cursor.md)

---

## Task-specific shortcuts

| Your task | Minimum read set |
|-----------|------------------|
| Run / fix `glossary:extract` | 01 (Phase 0) + 02 |
| Enable Google Drive mirror (Phase 0.5) | 05 + 01 + 02 + **04** + [consumers/techdev-cursor.md](./consumers/techdev-cursor.md) |
| Open consumer PR for handoff wiring | **04** + install [consumer-templates](../../scripts/cross_repo/consumer-templates/) |
| Cross-repo bot / Issue flow | **06** + [scripts/cross_repo](../../scripts/cross_repo/README.md) |
| MCP `glossary-knowledge` | 02 § MCP |
| Check if platform blocked you | 03 + CHANGELOG |
| Genspark / aidrive scope | techdev-cursor `meta/platform-integration/02-genspark-aidrive-boundary.md` (not duplicated here) |

---

## When to stop and notify the user

1. Platform change is required but not listed as **done** in 01 — escalate; do not edit term-prep-platform from consumer workspace.
2. Schema or output shape in 02 does not match what extract produced — report mismatch with config path and platform commit/date.
3. Action in 03 is blocked (missing credentials, path, MCP) — user must unblock; agent does not commit cross-repo.

---

## Platform maintainer sync checklist

When platform work affects consumers, update **term-prep-platform in one commit:**

- [ ] [01-platform-status.md](./01-platform-status.md) — phase checkboxes / status line
- [ ] [02-schema-and-cli.md](./02-schema-and-cli.md) — if schema or CLI contract changed
- [ ] [03-consumer-actions.md](./03-consumer-actions.md) — new or completed consumer obligations
- [ ] [CHANGELOG.md](./CHANGELOG.md) — dated entry
- [ ] [consumers/techdev-cursor.md](./consumers/techdev-cursor.md) — if techdev-cursor-specific
- [ ] [meta/TODO.md](../TODO.md) — execution checklist (platform-internal)
- [ ] [05-platform-implementation.md](./05-platform-implementation.md) — if artifacts or flows changed
- [ ] [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md) — if consumer PR spec changes
- [ ] Notify user to open **consumer PR** using 04 (platform does not edit techdev-cursor)

---

## Related (platform)

| Topic | Path |
|-------|------|
| Integration detail (platform view) | [docs/integrations/techdev-cursor.md](../../docs/integrations/techdev-cursor.md) |
| Config schema | [meta/schemas/glossary-config.schema.json](../schemas/glossary-config.schema.json) |
| Consumer config mirror | [projects/techdev-cursor/glossary-config.json](../../projects/techdev-cursor/glossary-config.json) |
| Phase 0.5 Drive connector | [connectors/googledrive/README.md](../../connectors/googledrive/README.md) |
| Execution TODO | [meta/TODO.md](../TODO.md) |
