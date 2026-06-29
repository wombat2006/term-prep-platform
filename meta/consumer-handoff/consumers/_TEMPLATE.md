# Consumer checklist template

Copy to `consumers/<project-id>.md` when onboarding a new consumer.

---

## Metadata

| Field | Value |
|-------|-------|
| Consumer repo | `<org>/<repo>` |
| Package pin | `term-prep-platform==X.Y.Z` |
| Integration doc | `docs/integrations/<project-id>.md` |

---

## Read order

1. [../../CONSUMER_HANDOFF.md](../../CONSUMER_HANDOFF.md) — top entry point (start here)
2. [../01-platform-status.md](../01-platform-status.md) — phase status
3. [../02-schema-and-cli.md](../02-schema-and-cli.md) — schema + CLI
4. [../04-consumer-pr-guide-techdev-cursor.md](../04-consumer-pr-guide-techdev-cursor.md) — PR template
5. [../03-consumer-actions.md](../03-consumer-actions.md) — checklist
6. [../../contracts/README.md](../../contracts/README.md) — Plan B contracts (future reference)

---

## Integration state

| Area | Platform | Consumer | Gap |
|------|----------|----------|-----|
| Glossary extract | | | |
| Config schema | | | |
| Source connector | | | |
| MCP | | | |
| Plan B contract tracking (`meta/contracts/*`) | | | |

---

## Open items

- [ ] Register MCP command (`term-prep-glossary-knowledge-mcp`)
- [ ] Align `meta/glossary-config.json`
- [ ] Add contract CI check
