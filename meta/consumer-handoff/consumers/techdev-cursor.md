# techdev-cursor — consumer checklist

**Consumer repo:** [wombat2006/techdev-cursor](https://github.com/wombat2006/techdev-cursor)  
**Platform mirror:** [projects/techdev-cursor/glossary-config.json](../../../projects/techdev-cursor/glossary-config.json)  
**Open a consumer PR using:** [04-consumer-pr-guide-techdev-cursor.md](../04-consumer-pr-guide-techdev-cursor.md)  
**Platform implementation detail:** [05-platform-implementation.md](../05-platform-implementation.md)

---

## Read order (from consumer workspace)

1. `../term-prep-platform/meta/consumer-handoff/README.md`
2. `05-platform-implementation.md` — **what platform built**
3. `01-platform-status.md` → `02-schema-and-cli.md`
4. `04-consumer-pr-guide-techdev-cursor.md` — **consumer PR to open**
5. Consumer boundary: `meta/platform-integration/README.md` (in techdev-cursor)

**Platform agents do not edit techdev-cursor.** All wiring goes through consumer PR per step 4.

---

## Current integration state

| Area | Platform | Consumer (today) | Gap → fix in consumer PR |
|------|----------|------------------|---------------------------|
| Glossary extract | ✅ | ✅ `npm run glossary:extract` | — |
| Config schema + `source` | ✅ schema | ⏸ no `source` in config yet | [04 § glossary-config](./04-consumer-pr-guide-techdev-cursor.md) |
| Drive mirror runtime | ✅ `sync_corpus.py` | ⏸ no `glossary:sync` npm | [04 § run-glossary-sync](./04-consumer-pr-guide-techdev-cursor.md) |
| Docs pointer | ✅ handoff pack | ⏸ no shim | [04 § TERM_PREP_PLATFORM_STATUS](./04-consumer-pr-guide-techdev-cursor.md) |
| MCP glossary-knowledge | stub | registered | Real provider Phase 2+ |
| Vector RAG ingest | planned 4.5 | legacy TS connector | Do not extend legacy |
| Genspark / aidrive | **out of scope** | TS-30 idea | consumer `platform-integration/02` |

---

## Corpus strategy

| Mode | `corpus.files` | When |
|------|----------------|------|
| **Interim (now)** | In-repo markdown paths | `source.enabled: false` |
| **Target (0.5)** | `build/corpus/drive/**/*.md` (+ txt/csv) | After `glossary:sync` with OAuth |

Reference config shape: [projects/techdev-cursor/glossary-config.json](../../../projects/techdev-cursor/glossary-config.json)

---

## Commands cheat sheet

```bash
# Consumer (after PR merges glossary:sync*)
npm run glossary:extract:check
npm run glossary:sync:check          # no OAuth
npm run glossary:extract

# Platform sibling — verification
cd ../term-prep-platform
bash scripts/run_phase05_checks.sh
python scripts/sync_corpus.py --check \
  --config ../techdev-cursor/meta/glossary-config.json

# Live sync (deferred until OAuth):
# npm run glossary:sync
```

---

## Open items (consumer PR + follow-up)

- [ ] Open PR per [04-consumer-pr-guide-techdev-cursor.md](../04-consumer-pr-guide-techdev-cursor.md)
- [ ] B3–B4 — enable `source` + corpus globs when Drive folder ready (follow-up)
- [ ] B7 — live Drive smoke (credentials)
- [ ] B8 — connector re-export (optional, later)
