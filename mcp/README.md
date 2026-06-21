# MCP Servers

Shared stdio MCP tools for data prep before RAG ingest.

Register in consumer `.cursor/mcp.json` alongside project-specific MCPs (e.g. techsapo-providers).

---

## Servers

| Directory | Purpose | Status |
|---|---|---|
| [glossary-knowledge/](glossary-knowledge/) | general / domain / unknown classification | stub |
| [term-extract/](term-extract/) | fugashi candidate extraction as MCP | planned |
| [pii-guard/](pii-guard/) | PII detect / mask / flag | planned |
| [sanitize/](sanitize/) | policy-based redaction | planned |

---

## Cursor registration (example)

```json
{
  "mcpServers": {
    "glossary-knowledge": {
      "command": "/path/to/term-prep-platform/.venv/bin/python",
      "args": ["-m", "glossary_knowledge_mcp"],
      "cwd": "/path/to/term-prep-platform/mcp/glossary-knowledge",
      "env": {
        "PYTHONPATH": "/path/to/term-prep-platform/mcp/glossary-knowledge"
      }
    }
  }
}
```

Requires Python >= 3.10 and `pip install -r requirements-mcp.txt`.

---

## Contracts

See [docs/MCP-CONTRACTS.md](../docs/MCP-CONTRACTS.md).
