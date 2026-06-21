# pii-guard MCP (planned)

Phase 3 — PII detection before RAG ingest.

**Candidate adapter:** [Microsoft Presidio](https://github.com/microsoft/presidio)

Planned tools:

- `scan_text` — detect PII spans
- `mask_text` — replace or flag entities

Consumer: [techdev-cursor](https://github.com/wombat2006/techdev-cursor) Google Drive → Vector Store pipeline.
