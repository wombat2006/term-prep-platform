# Handoff: platform status for consumers

**From:** term-prep-platform  
**To:** techdev-cursor (and other consumer) maintainers / agents  
**Status:** Active (2026-06-21) — not an ADR

---

## Start here (consumer agents)

**Canonical pack:** [meta/consumer-handoff/README.md](./consumer-handoff/README.md)

| Step | File |
|------|------|
| Index + read order | [consumer-handoff/README.md](./consumer-handoff/README.md) |
| **Platform implementation** | [05-platform-implementation.md](./consumer-handoff/05-platform-implementation.md) |
| Phase progress | [01-platform-status.md](./consumer-handoff/01-platform-status.md) |
| Schema & CLI | [02-schema-and-cli.md](./consumer-handoff/02-schema-and-cli.md) |
| **Consumer PR spec (techdev-cursor)** | [04-consumer-pr-guide-techdev-cursor.md](./consumer-handoff/04-consumer-pr-guide-techdev-cursor.md) |
| Actions checklist | [03-consumer-actions.md](./consumer-handoff/03-consumer-actions.md) |
| Dated changes | [CHANGELOG.md](./consumer-handoff/CHANGELOG.md) |
| Cross-repo A+C bot workflow | [06-cross-repo-workflow.md](./consumer-handoff/06-cross-repo-workflow.md) |
| techdev-cursor summary | [consumers/techdev-cursor.md](./consumer-handoff/consumers/techdev-cursor.md) |

Consumer agents **read** term-prep-platform (sibling `../term-prep-platform` or `$TERM_PREP_PLATFORM_ROOT`). Platform agents **do not edit techdev-cursor** — consumer wiring is specified in **04** for a consumer-side PR.

**Opposite direction (platform agents):** techdev-cursor [meta/platform-integration/README.md](https://github.com/wombat2006/techdev-cursor/blob/master/meta/platform-integration/README.md)

**Cross-repo policy:** Consumer edits consumer only. Platform edits platform only. **No direct cross-repo file edits** — use [04-consumer-pr-guide-techdev-cursor.md](./consumer-handoff/04-consumer-pr-guide-techdev-cursor.md).

---

## Consumer PR (techdev-cursor)

Platform does **not** open PRs on techdev-cursor. Copy the spec from:

**[meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md](./consumer-handoff/04-consumer-pr-guide-techdev-cursor.md)**

---

## Suggested consumer pointer (after consumer PR merges)

In techdev-cursor, add to `docs/DOCUMENTATION_INDEX.md`:

```markdown
| **../term-prep-platform/meta/consumer-handoff/README.md** | Platform progress · schema/CLI · pending consumer actions |
```

Optional shim: `meta/TERM_PREP_PLATFORM_STATUS.md` → link to sibling handoff README.
