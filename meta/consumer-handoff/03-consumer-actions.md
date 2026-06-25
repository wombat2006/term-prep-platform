# Consumer actions required (platform cannot apply)

**Read as:** Step 3 of [consumer-handoff index](./README.md)  
**Rule:** Platform agents **document** consumer work here and in [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md). **Do not edit techdev-cursor.** User or consumer agent opens the PR using the guide.

---

## Consumer PR (techdev-cursor)

**Full spec (title, body, file contents):** [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md)

Summary of what the consumer PR wires (platform already implemented the runtime):

| Consumer change | Purpose |
|-----------------|---------|
| `meta/TERM_PREP_PLATFORM_STATUS.md` | Shim → read this handoff pack |
| `docs/DOCUMENTATION_INDEX.md` | Integration pointer |
| `meta/glossary-config.json` | `source` block (`enabled: false`) |
| `scripts/run-glossary-sync.sh` + npm `glossary:sync*` | Delegate to platform `sync_corpus.py` |
| `meta/TO-BE-GLOSSARY-PIPELINE.md` | Phase 0.5 section |

Live OAuth sync remains **deferred** — see 04 § Follow-up PR.

---

## Always (one-time setup)

| # | Action | Repo | Status |
|---|--------|------|--------|
| A1 | Sibling clone or set `TERM_PREP_PLATFORM_ROOT` | consumer dev machine | user |
| A2 | Register `glossary-knowledge` in `.cursor/mcp.json` | techdev-cursor | [docs/integrations/techdev-cursor.md](../../docs/integrations/techdev-cursor.md) |
| A3 | Keep `meta/glossary-config.json` aligned with platform schema | techdev-cursor | ongoing |
| A4 | Add pointers per [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md) | techdev-cursor PR | **use PR guide** |

### A4 — covered by consumer PR guide

See [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md) § Files to add or change — includes `DOCUMENTATION_INDEX`, shim, npm scripts.

---

## Phase 0 — complete

No open platform blockers for in-repo corpus extract.

---

## Phase 0.5 — Google Drive mirror (open)

| # | Action | When | Notes |
|---|--------|------|-------|
| B1 | `cd ../term-prep-platform/connectors/googledrive && npm install && npm run build` | Before first sync | One-time per machine |
| B2 | Set OAuth env vars | Before live sync | See [02-schema-and-cli.md](./02-schema-and-cli.md) |
| B3 | `source.enabled: true` + real `folder_id` in `meta/glossary-config.json` | When Drive corpus ready | |
| B4 | Update `corpus.files` to mirror globs | After B3 | e.g. `build/corpus/drive/**/*.md` |
| B5 | Run sync before extract | Each corpus refresh | `npm run glossary:sync` after consumer PR |
| B6 | Optional: npm hook `glossary:sync` before extract | Convenience | Spec in [04](./04-consumer-pr-guide-techdev-cursor.md) |
| B7 | Live smoke: sync → extract | **Deferred** | Credentials not used in platform CI yet |
| B8 | Thin re-export platform googledrive connector | Later (O-P007-004 step 3) | Reduce duplicate TS in consumer |

**Platform mirror config** (reference only): [projects/techdev-cursor/glossary-config.json](../../projects/techdev-cursor/glossary-config.json) — `source.enabled: false` until user enables.

---

## Phase 4.5 — Vector ingest (future)

| # | Action | When |
|---|--------|------|
| C1 | Stop extending consumer `googledrive-connector.ts` vector path | Now (policy) |
| C2 | Wire Phase 4 hook to platform vector connector | When platform ships 4.5 |
| C3 | Add `outputs.rag` (or successor) keys to consumer config | With schema PR |

---

## Escalation template (consumer → user)

When blocked on platform:

```text
Blocked: <goal>
Read: ../term-prep-platform/meta/consumer-handoff/01-platform-status.md
Platform status: <phase / item not done>
Request: assign platform task or confirm workaround
```

---

## Per-consumer checklists

- [techdev-cursor](./consumers/techdev-cursor.md)
- [Template for new consumers](./consumers/_TEMPLATE.md)
