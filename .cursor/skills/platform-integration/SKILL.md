---
name: platform-integration
description: Start term-prep-platform work with correct consumer boundary reads. Use when the user pastes an integration task, mentions techdev-cursor, Phase 0.5 Drive mirror, glossary extractor, or platform-integration read pack.
disable-model-invocation: true
---

# Platform integration (read consumer boundary first)

## Goal

Scope **term-prep-platform** work correctly before coding. Consumer docs are **read-only** from this workspace.

## Resolve consumer path

| Priority | Path |
|----------|------|
| 1 | `$TECHDEV_CURSOR_ROOT` |
| 2 | `../techdev-cursor` |
| 3 | Stop and ask user for path |

## Mandatory read order (consumer repo)

| Step | File |
|------|------|
| 0 | `meta/platform-integration/README.md` |
| 1 | `01-repo-split.md` |
| 2 | `02-genspark-aidrive-boundary.md` |
| 3 | `03-glossary-consumer-contract.md` |

## Platform handoff (this repo — write here)

After reading consumer boundary:

| Step | File |
|------|------|
| 1 | `meta/consumer-handoff/05-platform-implementation.md` |
| 2 | `meta/consumer-handoff/01-platform-status.md` |

## Workflow

1. Confirm read of consumer steps 0–3.
2. State **will implement** vs **will not touch** (consumer repo, Genspark, aidrive).
3. Plan scoped to **term-prep-platform** only.
4. List **consumer-side** changes → user applies via consumer PR ([04](../../../meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md)).
5. If boundary unclear → stop and ask before coding.

## Task shortcuts

| Task | Minimum consumer reads |
|------|------------------------|
| Glossary extract only | 01 + 03 |
| Drive mirror (0.5) | 01 + 02 + 03 |
| Vector ingest (4.5) | 01 + 02 + 03 |
| Genspark scope check | 02 full |

## Output format (when preparing work)

```markdown
## Ownership
- Platform: ...
- Not touching: ...

## Plan (term-prep-platform only)
...

## Consumer obligations (user / consumer PR)
...

## Handoff updates after merge
- CHANGELOG · 01 · 04 as needed
```
