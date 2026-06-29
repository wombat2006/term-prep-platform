# Integration: techdev-cursor

Consumer: [wombat2006/techdev-cursor](https://github.com/wombat2006/techdev-cursor)

---

## Ownership boundary

| Area | Owner |
|---|---|
| `glossary_extractor`, `sync_corpus`, `glossary-knowledge` MCP | term-prep-platform |
| `meta/glossary-config.json`, npm wiring, RAG consumer logic | techdev-cursor |
| Genspark / aidrive | techdev-cursor only |

Platform does not edit consumer repo; consumer applies its own PR.

---

## Contract (package entrypoints)

| Command | Purpose |
|---|---|
| `term-prep-extract --check --config <config>` | morphology + schema check |
| `term-prep-extract --config <config>` | extract adopt/hold |
| `term-prep-sync --check --config <config>` | sync preflight |
| `term-prep-sync --config <config>` | mirror sync |
| `term-prep-glossary-knowledge-mcp` | MCP stdio server |
| `term-prep-contract-check --config <config> --expect-major 1` | contract guard |

---

## Phase 0.5 (Drive mirror)

```text
Google Drive API
  -> connectors/googledrive (platform)
  -> build/corpus/drive/ (consumer workspace)
  -> term-prep-extract
```

Required env for live sync:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`
- optional `GOOGLE_DRIVE_FOLDER_ID`

Credential-free verification remains available:

```bash
bash scripts/run_phase05_checks.sh
```

---

## Consumer migration docs

- [meta/consumer-handoff/README.md](../../meta/consumer-handoff/README.md)
- [meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md](../../meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md)
- [meta/consumer-handoff/02-schema-and-cli.md](../../meta/consumer-handoff/02-schema-and-cli.md)
- [meta/contracts/README.md](../../meta/contracts/README.md) (Plan B contract-first draft)
