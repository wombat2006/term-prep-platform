# Integration: techdev-cursor

Consumer: [wombat2006/techdev-cursor](https://github.com/wombat2006/techdev-cursor)

---

## Role in platform flow

techdev-cursor は **Outputs** 側 — ingest（Google Drive）と RAG index / bot dict / query expander を保持し、prep は本 repo の MCP + CLI を参照する。

```text
Drive（社内データ）→ [prep: term-prep-platform] → term registry → RAG index · devassist-dictionary · query expander
```

図解: [ARCHITECTURE.md](../ARCHITECTURE.md)

---

## Use case

Google Drive → document fetch → **prep** → OpenAI Vector Store (existing `googledrive-connector.ts`).

Also: expand [devassist-dictionary-v0.json](https://github.com/wombat2006/techdev-cursor/blob/master/config/fork/devassist-dictionary-v0.json) from extracted terms.

---

## Config

[projects/techdev-cursor/glossary-config.json](../projects/techdev-cursor/glossary-config.json) — **Phase 0** schema (`filter` / `output` / `knowledge_filter`; adopt/hold split).

Consumer copy in repo: [techdev-cursor/meta/glossary-config.json](https://github.com/wombat2006/techdev-cursor/blob/master/meta/glossary-config.json)

Set `corpus.files` when Drive sync local mirror path is fixed.

### Output layout (consumer repo)

| Path | Git | Content |
|------|-----|---------|
| `meta/glossary-adopt.json` | ✅ | Adopt candidates |
| `meta/glossary-hold.json` | ✅ | Hold candidates |
| `meta/glossary-registry.json` | ✅ (Phase 2) | Registry seed — not yet |
| `meta/glossary-candidates.json` | ❌ | Legacy — gitignored in consumer |
| `build/glossary/reject.jsonl` | ❌ | Only if `emit_reject: true` |

---

## MCP registration

Add to techdev-cursor `.cursor/mcp.json` alongside `techsapo-providers`:

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

**Do not modify `techsapo-providers`.** `glossary-knowledge` is a separate stdio server for term classification (RAG prep).

---

## Verification

### Morphology check

```bash
python scripts/glossary_extractor.py --check \
  --config projects/techdev-cursor/glossary-config.json
```

### MCP stub — `classify_term` (NullProvider → unknown)

```bash
cd mcp/glossary-knowledge
PYTHONPATH=. python -c "
from glossary_knowledge_mcp.server import classify_term, list_providers
print(list_providers())
r = classify_term('Wall-Bounce', domain='devassist-platform')
assert r['label'] == 'unknown' and r['provider_id'] == 'null'
print('OK:', r)
"
```

Expected while `knowledge_filter.enabled: false`: all terms classified as `unknown` (stub).

### Legacy ignore (consumer)

```bash
cd /path/to/techdev-cursor
touch meta/glossary-candidates.json
git check-ignore -v meta/glossary-candidates.json
rm meta/glossary-candidates.json
```

---

## Insertion point (target)

```text
GoogleDriveRAGConnector.download/process
    → [term-prep MCP batch]   … Phase 2.5+
    → openai vector store upload
```

Dictionary export (planned):

```text
platform registry → devassist-dictionary-v0.json
  { term_id, surface } → { key, expansion, domain }
```

---

## forkProfile.yaml

Existing swappable `dictionary` path can point at exported JSON from this platform.
