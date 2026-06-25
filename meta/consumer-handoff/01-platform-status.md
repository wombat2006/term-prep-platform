# Platform status snapshot

**Read as:** Step 1 of [consumer-handoff index](./README.md)  
**Last updated:** 2026-06-21  
**Detail checklist:** [meta/TODO.md](../TODO.md)

---

## Summary

| Phase | Theme | Status | Consumer impact |
|-------|-------|--------|-----------------|
| **0** | adopt/hold split, schema, extractor | **Done** | Use `npm run glossary:extract`; outputs under `meta/glossary-*.json` |
| **0.5** | Source connector — Google Drive mirror | **In progress** | Mirror code on platform; consumer enables `source` + corpus globs when ready |
| **1** | Core package split (`scripts/glossary/`) | Not started | None yet |
| **2 / 2.5** | seed-first, real `glossary-knowledge` provider | Stub only | MCP returns `unknown` for all terms |
| **3–4** | GLOSSARY diff, Python RAG subpackage | Not started | None yet |
| **4.5** | RAG Vector Store ingest connector | Proposed | Replaces consumer `googledrive-connector` vector path when ready |
| **IaC** | Terraform (S3 mirror, batch IAM) | Proposed / docs only | Optional S3 path for corpus mirror |

---

## Phase 0 — shipped

- `scripts/glossary_extractor.py` — fugashi + unidic-lite, adopt/hold/reject outputs
- `meta/schemas/glossary-config.schema.json` — validated on every CLI run
- `mcp/glossary-knowledge` — stdio MCP stub (`classify_term` → `unknown`)
- Consumer invoke: `npm run glossary:extract` / `glossary:extract:check` (delegates to platform)

**Consumer:** Phase 0 complete on both sides. No platform blocker for in-repo corpus paths.

---

## Phase 0.5 — Google Drive mirror (current focus)

### Done on platform

| Item | Location |
|------|----------|
| TS mirror connector (no Genspark / aidrive) | `connectors/googledrive/` |
| Python sync entry | `scripts/sync_corpus.py` |
| Config `source` section in schema | `meta/schemas/glossary-config.schema.json` |
| Corpus glob patterns | `glossary_extractor.resolve_corpus_files` |
| No-credential tests | `scripts/run_phase05_checks.sh`, `tests/`, `npm test` in connector |
| Integration docs | `docs/integrations/techdev-cursor.md`, `connectors/googledrive/README.md` |

### Not done / deferred

| Item | Notes |
|------|-------|
| Live Drive sync smoke | Requires OAuth env — **scheduled later** |
| S3 adapter + Terraform modules | `0.5-2` in [TODO.md](../TODO.md) |
| Consumer re-export of TS connector | User applies on techdev-cursor |
| Consumer `source.enabled: true` | User applies when folder_id + credentials ready |

### Target flow (when consumer enables source)

```text
sync_corpus.py  →  build/corpus/drive/
glossary:extract  →  meta/glossary-adopt.json · hold.json
```

---

## Phase 4.5 — RAG Vector (planned)

- Design option: [O-P008-001](../glossary-pipeline/options/O-P008-001-rag-vector-connector.md)
- **Not implemented.** Consumer AS-IS: `googledrive-connector.ts` vector mode remains legacy until delegation.

---

## MCP servers

| Server | Status | Consumer registration |
|--------|--------|----------------------|
| `glossary-knowledge` | Stub (`NullProvider`) | `.cursor/mcp.json` → platform venv |
| `pii-guard`, `sanitize`, `noise-filter` | Planned | — |

---

## How to refresh this snapshot

Platform maintainers: after meaningful progress, update this file + [CHANGELOG.md](./CHANGELOG.md) + [03-consumer-actions.md](./03-consumer-actions.md).  
Consumers: prefer reading **git date** on these files over stale chat summaries.
