# dopagaki-transition — consumer config

Run extractor from platform repo root (**`.venv` activate + `requirements-dev.txt` 済み**):

```bash
python scripts/glossary_extractor.py --check --config projects/dopagaki-transition/glossary-config.json
python scripts/glossary_extractor.py --config projects/dopagaki-transition/glossary-config.json
```

Clone dopagaki as sibling or set `project_root` in config to absolute path.

**Phase 0 done:** outputs `meta/glossary-adopt.json` and `meta/glossary-hold.json` in consumer repo; `filter.emit_reject: false` (reject not in Git).

Config は [JSON Schema](../../meta/schemas/glossary-config.schema.json) で起動時検証。注意点: [meta/schemas/README.md](../../meta/schemas/README.md).

See [docs/integrations/dopagaki-transition.md](../../docs/integrations/dopagaki-transition.md).
