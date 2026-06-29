# techdev-cursor — cutover checklist (package contract)

Consumer repo: [wombat2006/techdev-cursor](https://github.com/wombat2006/techdev-cursor)

---

## Read order

1. [README.md](../README.md)
2. [02-schema-and-cli.md](../02-schema-and-cli.md)
3. [04-consumer-pr-guide-techdev-cursor.md](../04-consumer-pr-guide-techdev-cursor.md)
4. [03-consumer-actions.md](../03-consumer-actions.md)
5. [../../contracts/README.md](../../contracts/README.md) (Plan B draft, no immediate migration)

---

## Current migration status

| Area | Target | Status |
|---|---|---|
| Extract / Sync | `term-prep-extract`, `term-prep-sync` | pending consumer PR |
| MCP launch | `term-prep-glossary-knowledge-mcp` command | pending consumer PR |
| Contract CI | `term-prep-contract-check` | pending consumer PR |
| Plan B draft tracking | `meta/contracts/*` | monitor only |
| OAuth live sync smoke | deferred | pending |

---

## Commands after cutover

```bash
npm run glossary:extract:check
npm run glossary:sync:check
term-prep-contract-check --config meta/glossary-config.json --expect-major 1
```

---

## Open items

- [ ] consumer PR based on [04](../04-consumer-pr-guide-techdev-cursor.md)
- [ ] package pin update policy agreed (who bumps Semver)
- [ ] live OAuth smoke scheduled
