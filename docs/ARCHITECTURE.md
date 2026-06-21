# Architecture

## Model

```text
Consumer repos (dopagaki, techdev-cursor, …)
    │  projects/<name>/glossary-config.json
    │  .cursor/mcp.json → term-prep-platform MCPs
    ▼
term-prep-platform
    mcp/           … stdio servers (Python)
    scripts/       … batch CLI
    meta/          … governance + TO-BE
```

**Polyglot:** TypeScript consumers (techdev-cursor) keep Drive/RAG code; prep runs via MCP stdio — same pattern as `techsapo-providers`.

---

## Pipeline (target)

```text
ingest → pii-guard → sanitize → term-extract → glossary-knowledge → registry → RAG / bot dict
```

Phase 0 (now): `glossary-knowledge` stub + `glossary_extractor` CLI.

---

## Reuse rules

| Share in platform | Keep in consumer |
|---|---|
| MCP tools & adapters | corpus paths |
| extractor CLI | human glossary / dictionary JSON |
| PROBLEMS/OPTIONS/DECISIONS template | ADR/TS/manuscript |

---

## References

- [techdev-cursor integration](integrations/techdev-cursor.md)
- [dopagaki-transition integration](integrations/dopagaki-transition.md)
- [TO-BE-PLATFORM.md](../meta/TO-BE-PLATFORM.md)
