# term-extract MCP (planned)

Phase 2 — expose `scripts/glossary_extractor.py` logic as MCP tools:

- `extract_terms` — corpus path + config → candidates
- `extract_from_text` — ad-hoc string

Until implemented, use the CLI:

```bash
python scripts/glossary_extractor.py --config projects/<consumer>/glossary-config.json
```
