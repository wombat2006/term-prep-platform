# Glossary Knowledge Filter MCP

Status:
**Stub** — NullProvider only. Resume at Phase 2.5.

Repository:
[term-prep-platform](https://github.com/wombat2006/term-prep-platform)

Related:
[research-log/RL-20260621-knowledge-filter-mcp.md](../../research-log/RL-20260621-knowledge-filter-mcp.md)
[D-002](../../meta/glossary-pipeline/DECISIONS.md#d-002)
[meta/glossary-pipeline/mcp/README.md](../../meta/glossary-pipeline/mcp/README.md)

---

## Purpose

MCP server for **general / domain / unknown** term classification. Consumers (Cursor, batch CLI) call this server instead of embedding API clients in each repo.

**Current behavior:** all terms → `unknown` (NullProvider).

---

## Setup

**Requires Python >= 3.10**

```bash
cd /path/to/term-prep-platform
source .venv/bin/activate
python -m pip install -r requirements-mcp.txt
```

Provider logic smoke test (`classify_term` tool — no stdio MCP session):

```bash
cd mcp/glossary-knowledge
PYTHONPATH=. python -c "
from glossary_knowledge_mcp.server import classify_term, list_providers
print('providers:', list_providers())
r = classify_term('Wall-Bounce', context='multi-LLM', domain='devassist-platform')
assert r['label'] == 'unknown' and r['provider_id'] == 'null'
print('OK:', r)
"
```

Lower-level provider test (optional):

```bash
PYTHONPATH=. python -c "
from glossary_knowledge_mcp.providers import ProviderRegistry
print(ProviderRegistry.from_config().classify('探索').to_dict())
"
```

---

## Run (stdio)

```bash
cd mcp/glossary-knowledge
PYTHONPATH=. python -m glossary_knowledge_mcp
```

---

## Cursor MCP config

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

---

## Tools

| Tool | Description |
|---|---|
| `classify_term` | Single term classification |
| `classify_batch` | Batch classification |
| `list_providers` | Provider chain |
| `get_cache_stats` | Cache stub |

Labels: `canonical` | `domain` | `general` | `unknown`
