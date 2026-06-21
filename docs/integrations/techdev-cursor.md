# Integration: techdev-cursor

Consumer: [wombat2006/techdev-cursor](https://github.com/wombat2006/techdev-cursor)

---

## Use case

Google Drive → document fetch → **prep** → OpenAI Vector Store (existing `googledrive-connector.ts`).

Also: expand [devassist-dictionary-v0.json](https://github.com/wombat2006/techdev-cursor/blob/master/config/fork/devassist-dictionary-v0.json) from extracted terms.

---

## Config

[projects/techdev-cursor/glossary-config.json](../projects/techdev-cursor/glossary-config.json)

Set `corpus.files` when Drive sync local mirror path is fixed.

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

---

## Insertion point (target)

```text
GoogleDriveRAGConnector.download/process
    → [term-prep MCP batch]   … Phase 2+
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
