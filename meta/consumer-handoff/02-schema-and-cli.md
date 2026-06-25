# Schema & CLI contract (consumer invoke surface)

**Read as:** Step 2 of [consumer-handoff index](./README.md)  
**Schema source of truth:** [meta/schemas/glossary-config.schema.json](../schemas/glossary-config.schema.json)

---

## Config file

| Role | Path (techdev-cursor) | Path (platform mirror) |
|------|----------------------|-------------------------|
| **Runtime** | `meta/glossary-config.json` | — |
| Reference / CI | — | `projects/techdev-cursor/glossary-config.json` |

`project_root` in consumer config points at consumer repo root. Platform mirror uses `../../../techdev-cursor` for local dev.

**Rule:** Schema changes land on platform first; consumer `meta/glossary-config.json` updated **same timing** (user / consumer PR).

---

## Required config sections (Phase 0+)

| Section | Purpose |
|---------|---------|
| `version` | Semver string (`1.0.0`) |
| `project_root` | Consumer repo root (relative to config file) |
| `morphology` | `fugashi` + dictionary (`unidic-lite` default) |
| `corpus.files` | Paths or **globs** relative to `project_root` |
| `scoring` | adopt/hold thresholds and weights |
| `output` | adopt / hold / registry / reject paths |
| `filter` | optional — `max_candidates_output`, `min_morph_freq`, etc. |
| `knowledge_filter` | optional — MCP batch filter (default `enabled: false`) |

---

## Phase 0.5 — `source` section (optional)

Present in schema; safe with `enabled: false` (default in platform mirror).

```json
{
  "source": {
    "enabled": false,
    "adapter": "googledrive",
    "local_mirror": "build/corpus/drive",
    "googledrive": {
      "folder_id": ""
    }
  }
}
```

| Field | When `enabled: true` |
|-------|----------------------|
| `adapter` | `"googledrive"` (S3 planned) |
| `local_mirror` | Staging dir under `project_root` (Git-ignored) |
| `googledrive.folder_id` | Drive folder ID, or env `GOOGLE_DRIVE_FOLDER_ID` |

**Corpus after sync:** point `corpus.files` at globs, e.g. `build/corpus/drive/**/*.md`.

---

## CLI commands (consumer npm → platform)

| Consumer npm | Platform command | Purpose |
|--------------|------------------|---------|
| `glossary:extract:check` | `glossary_extractor.py --check` | Morphology + schema |
| `glossary:extract` | `glossary_extractor.py` (no dry-run) | Full extract |
| `glossary:mcp-smoke` | MCP stub test | `glossary-knowledge` wiring |

**Phase 0.5 sync (not yet wired in consumer npm by default):**

```bash
python scripts/sync_corpus.py --config meta/glossary-config.json
python scripts/sync_corpus.py --check --config meta/glossary-config.json
```

Run from platform repo with `TERM_PREP_PLATFORM_ROOT` or sibling path; `--config` may be absolute path to consumer `meta/glossary-config.json`.

---

## Environment variables

### Glossary extract (platform venv)

Uses consumer `project_root` for corpus paths. Platform `.venv` required (`requirements-dev.txt`).

### Google Drive mirror (Phase 0.5)

| Variable | Required for live sync |
|----------|------------------------|
| `GOOGLE_CLIENT_ID` | yes |
| `GOOGLE_CLIENT_SECRET` | yes |
| `GOOGLE_REFRESH_TOKEN` | yes |
| `GOOGLE_REDIRECT_URI` | no |
| `GOOGLE_DRIVE_FOLDER_ID` | yes if not in config |

**Not used on platform:** `GSK_API_KEY`, Genspark, aidrive.

---

## Output artifacts (consumer repo)

| Path | Git | Description |
|------|-----|-------------|
| `meta/glossary-adopt.json` | yes | High-confidence candidates |
| `meta/glossary-hold.json` | yes | Review queue |
| `meta/glossary-registry.json` | yes (Phase 2 seed) | Registry — not populated yet |
| `build/glossary/reject.jsonl` | no | If `filter.emit_reject: true` |
| `build/corpus/drive/` | no | Mirror staging (Phase 0.5) |

---

## MCP: `glossary-knowledge`

**Registration (consumer `.cursor/mcp.json`):**

```json
"glossary-knowledge": {
  "command": "/path/to/term-prep-platform/.venv/bin/python",
  "args": ["-m", "glossary_knowledge_mcp"],
  "cwd": "/path/to/term-prep-platform/mcp/glossary-knowledge",
  "env": {
    "PYTHONPATH": "/path/to/term-prep-platform/mcp/glossary-knowledge"
  }
}
```

**Current behavior:** `knowledge_filter.enabled: false` → extractor skips MCP; smoke test classifies all terms as `unknown`.

**Do not modify** `techsapo-providers` — separate stdio server.

---

## Verification (no Drive credentials)

From platform root:

```bash
bash scripts/run_phase05_checks.sh
python scripts/glossary_extractor.py --check --config projects/techdev-cursor/glossary-config.json
```

From consumer (with sibling platform):

```bash
npm run glossary:extract:check
```

---

## Related

- [meta/schemas/README.md](../schemas/README.md)
- [connectors/googledrive/README.md](../../connectors/googledrive/README.md) § Testing
- [docs/MCP-CONTRACTS.md](../../docs/MCP-CONTRACTS.md)
