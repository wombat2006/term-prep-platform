# Schema & CLI contract (consumer invoke surface)

**Read as:** Step 2 of [consumer-handoff index](./README.md)  
**Schema source of truth:** [meta/schemas/glossary-config.schema.json](../schemas/glossary-config.schema.json)

---

## Config file

| Role | Path |
|------|------|
| **Runtime** | consumer `meta/glossary-config.json` |
| **Schema source** | package release `meta/schemas/glossary-config.schema.json` |

**Rule:** Schema and CLI contract are versioned by package Semver.

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

## Package entrypoints (consumer invokes)

| Command | Purpose |
|--------------|---------|
| `term-prep-extract --check --config <config>` | Morphology + schema |
| `term-prep-extract --config <config>` | Full extract |
| `term-prep-sync --check --config <config>` | Connector readiness / config check |
| `term-prep-sync --config <config>` | Sync mirror |
| `term-prep-contract-check --config <config> --expect-major 1` | Contract guard in CI |

These commands are the current production invoke surface (D-004 package contract).

---

## Upcoming Plan B service surfaces (contract-first draft)

Before remote service implementation, canonical interface specs are fixed at:

- [../contracts/http/openapi.yaml](../contracts/http/openapi.yaml)
- [../contracts/sse/event-envelope.schema.json](../contracts/sse/event-envelope.schema.json)
- [../contracts/mcp-tool-contract.md](../contracts/mcp-tool-contract.md)
- [../contracts/cli-contract.md](../contracts/cli-contract.md)

Consumer impact policy:

- package CLI remains supported in major version `1.x`
- remote HTTP/SSE/MCP surfaces are introduced additively
- any incompatible change is major-version gated and announced in changelog

### Consumer npm mapping (example)

```bash
term-prep-extract --check --config meta/glossary-config.json
term-prep-extract --config meta/glossary-config.json
term-prep-sync --check --config meta/glossary-config.json
```

---

## Environment variables

### Extract / sync runtime

Install package in consumer runtime environment. No sibling repo path required.

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
  "command": "term-prep-glossary-knowledge-mcp"
}
```

**Current behavior:** `knowledge_filter.enabled: false` → extractor skips MCP; smoke test classifies all terms as `unknown`.

**When `enabled: true`:** The platform routes each term through the configured LLM provider chain
(Anthropic / Google / Ollama / fallback). Consumer code does not change when the platform
adds or switches providers. Only `label` and `candidate_id` matter to consumer logic.

**Provider abstraction policy:** [meta/contracts/llm-provider-policy.md](../../meta/contracts/llm-provider-policy.md)

**Do not modify** `techsapo-providers` — separate stdio server.

---

## Verification (no Drive credentials)

From any environment with package installed:

```bash
term-prep-extract --check --config meta/glossary-config.json
term-prep-sync --check --config meta/glossary-config.json
term-prep-contract-check --config meta/glossary-config.json --expect-major 1
```

---

## Related

- [meta/schemas/README.md](../schemas/README.md)
- [connectors/googledrive/README.md](../../connectors/googledrive/README.md) § Testing
- [docs/MCP-CONTRACTS.md](../../docs/MCP-CONTRACTS.md)
- [templates/consumer-contract-ci.yml](./templates/consumer-contract-ci.yml)
