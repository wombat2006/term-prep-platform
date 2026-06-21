# MCP Contracts

## glossary-knowledge

| Tool | Input | Output |
|---|---|---|
| `classify_term` | `term`, `context?`, `domain?`, `provider?` | `{ term, label, confidence, reason, provider_id, cached }` |
| `classify_batch` | `terms[]`, … | `{ results[], count }` |
| `list_providers` | — | `{ providers[] }` |
| `get_cache_stats` | — | stub |

**Labels:** `canonical` | `domain` | `general` | `unknown`

Spec: [meta/glossary-pipeline/mcp/README.md](../meta/glossary-pipeline/mcp/README.md)

---

## Future servers

Document here when implemented: `term-extract`, `pii-guard`, `sanitize`, `query-ground`.
