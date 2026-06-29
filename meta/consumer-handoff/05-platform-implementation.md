# Platform implementation reference (Phase 0 · 0.5)

**Read as:** Step 3 of [consumer-handoff index](./README.md) · [top entry: ../CONSUMER_HANDOFF.md](../CONSUMER_HANDOFF.md)  
**Purpose:** Platform が何を実装したかを理解してから consumer PR を開く。  
**Audience:** techdev-cursor maintainers (read-only on this repo).  
**Last updated:** 2026-06-29

---

## Scope boundary (do not confuse)

| Owns | Repo | Does **not** own |
|------|------|------------------|
| **Platform** | term-prep-platform | Wall-Bounce, Genspark, aidrive, consumer `meta/glossary-*` edits |
| **Consumer** | techdev-cursor | `glossary_extractor` body, Drive mirror TS, platform MCP source |

Consumer invokes platform via **versioned package entrypoints**. Platform never commits to techdev-cursor.

Plan B pre-implementation contracts (remote service draft) are tracked separately in
[meta/contracts/](../contracts/README.md) and do not replace current package invoke flow yet.

---

## End-to-end flows

### Phase 0 — in-repo corpus (live today)

```text
techdev-cursor/meta/glossary-config.json
  corpus.files → paths under consumer repo
       ↓
npm run glossary:extract
       ↓
term-prep-extract --config meta/glossary-config.json
       ↓
meta/glossary-adopt.json · meta/glossary-hold.json
```

### Phase 0.5 — Google Drive mirror (platform shipped · consumer wiring optional)

```text
Google Drive API (OAuth env)
       ↓
connectors/googledrive/  [mirror mode only — no Vector, no Genspark]
       ↓
scripts/sync_corpus.py  ← reads glossary-config `source`
       ↓
{consumer}/build/corpus/drive/   (Git-ignored via consumer build/)
       ↓
glossary_extractor  ← corpus.files globs e.g. build/corpus/drive/**/*.md
       ↓
meta/glossary-adopt.json · hold.json
```

**Not in scope:** Genspark `aidrive`, `GSK_API_KEY`, Genspark `google_drive` tool as corpus source.

---

## Platform artifact map

```text
term-prep-platform/
├── scripts/
│   ├── glossary_extractor.py      # Phase 0 extract CLI (+ corpus glob)
│   ├── sync_corpus.py               # Phase 0.5 sync entry
│   ├── run_phase05_checks.sh        # Tests without OAuth
│   └── connectors/googledrive.py    # subprocess → Node CLI
├── connectors/googledrive/          # TypeScript mirror connector
│   ├── src/cli.ts                   # mirror --folder-id --output-dir
│   ├── src/mirror-sync.ts
│   ├── src/drive-client.ts          # OAuth from env
│   └── README.md
├── meta/schemas/
│   └── glossary-config.schema.json  # includes optional `source` block
├── mcp/glossary-knowledge/          # stub MCP (NullProvider)
├── tests/test_phase05_no_credentials.py
└── meta/consumer-handoff/           # ← you are here (consumer read pack)
```

---

## Phase 0 — implementation detail

| Component | Behavior |
|-----------|----------|
| `glossary_extractor.py` | Loads config → JSON Schema validate → fugashi morph → scoring → adopt/hold/reject |
| `resolve_corpus_files()` | Literal paths + `**` globs relative to `project_root` |
| `glossary-knowledge` MCP | `classify_term` returns `unknown` until Phase 2.5 |
| Schema | Required: `version`, `project_root`, `morphology`, `corpus`, `scoring`; optional: `filter`, `output`, `knowledge_filter`, `source` |

**Known gap (platform backlog):** `filter.max_candidates_output` may not cap output yet — see [meta/TODO.md](../TODO.md).

---

## Phase 0.5 — implementation detail

| Component | Behavior |
|-----------|----------|
| `connectors/googledrive` | Lists Drive folder, exports Google Docs → `.md`, spreadsheets → `.csv`, writes `mirror-manifest.json` |
| `sync_corpus.py` | If `source.enabled: false` → check-only OK; if true → calls Node CLI with `folder_id` + `local_mirror` under `project_root` |
| Credentials | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`; optional `GOOGLE_DRIVE_FOLDER_ID` |
| Tests (no OAuth) | `npm test` in connector; `bash scripts/run_phase05_checks.sh`; CLI fails fast without credentials |

**Deferred on purpose:** Live Drive sync smoke — requires real OAuth (not run in default CI).

---

## Config contract (`source` block)

Schema source: [glossary-config.schema.json](../schemas/glossary-config.schema.json)

| Field | Notes |
|-------|-------|
| `source.enabled` | `false` = interim in-repo `corpus.files` (current) |
| `source.adapter` | `"googledrive"` today; `"s3"` planned |
| `source.local_mirror` | Default `build/corpus/drive` under consumer root |
| `source.googledrive.folder_id` | Empty allowed when disabled; required when enabled (or env) |

When enabling Drive mirror, consumer **must** switch `corpus.files` to globs under `local_mirror`.

---

## Verification matrix

| Check | Where | Credentials |
|-------|-------|-------------|
| `bash scripts/run_phase05_checks.sh` | platform package env | No |
| `npm run test` in `connectors/googledrive` | platform | No |
| `term-prep-sync --check --config <consumer-config>` | consumer runtime | No |
| `term-prep-extract --check --config <consumer-config>` | consumer runtime | No |
| `term-prep-sync --config <consumer-config>` | consumer runtime | **Yes** — deferred |
| sync → extract E2E | consumer + platform | **Yes** — deferred |

---

## Phase 4.5 (not built)

RAG Vector ingest connector — design only ([O-P008-001](../glossary-pipeline/options/O-P008-001-rag-vector-connector.md)).  
Consumer legacy: `src/services/googledrive-connector.ts` — **do not extend** for new prep work.

---

## Related

- [01-platform-status.md](./01-platform-status.md) — phase checklist
- [02-schema-and-cli.md](./02-schema-and-cli.md) — invoke surface
- [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md) — **consumer PR spec (copy from here)**
- [docs/integrations/techdev-cursor.md](../../docs/integrations/techdev-cursor.md)
