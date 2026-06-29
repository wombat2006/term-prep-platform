# MCP Tool Contract

Status:
Draft v1 (2026-06-29)

---

## Scope

This document defines the stable MCP tool surface that must be preserved across
transport styles:

- local stdio (`term-prep-glossary-knowledge-mcp`)
- future remote MCP adapter

---

## Tool set

| Tool | Required | Notes |
|---|---|---|
| `classify_term` | yes | one candidate/term classification |
| `classify_batch` | yes | batch classification |
| `list_providers` | yes | debugging and ops visibility |
| `get_cache_stats` | optional | available when cache is enabled |

---

## `classify_term`

Input contract:

```json
{
  "term": "Wall-Bounce",
  "context": "Used in RAG retrieval ranking docs",
  "domain": "devassist-platform"
}
```

Output contract:

```json
{
  "label": "unknown",
  "provider_id": "null",
  "confidence": 0.0,
  "reason": "no provider configured"
}
```

Rules:

- `label` enum must remain `canonical|domain|general|unknown`
- unknown fields in input must not fail tool execution
- failures must return `ErrorEnvelope`-compatible fields where possible

---

## `classify_batch`

Input contract:

```json
{
  "items": [
    {"term": "Wall-Bounce", "domain": "devassist-platform"},
    {"term": "探索", "domain": "attention-economics"}
  ]
}
```

Output contract:

```json
{
  "results": [
    {"label": "unknown", "provider_id": "null", "confidence": 0.0},
    {"label": "unknown", "provider_id": "null", "confidence": 0.0}
  ]
}
```

---

## Compatibility rules

- Additive fields are allowed in both input and output
- Tool names and required fields are major-version locked
- Any rename/removal of tools is a breaking change

---

## Conformance tests (minimum)

1. `classify_term` unknown fallback behavior
2. `classify_batch` preserves item order
3. `list_providers` returns active chain in priority order
4. error behavior is stable when provider config is invalid

---

## LLM provider abstraction

The `provider_id` in tool output identifies which adapter ran. This value is
**informational only** and changes as the platform operator configures the
provider chain. Consumer code must not branch on `provider_id`.

For details on how Anthropic/Google/Ollama are isolated from consumers:

- [llm-provider-policy.md](./llm-provider-policy.md)
