# dopagaki-transition — consumer config

Run extractor from platform repo root:

```bash
python scripts/glossary_extractor.py --config projects/dopagaki-transition/glossary-config.json
```

Clone dopagaki as sibling or set `project_root` in config to absolute path.

Output: `build/glossary/` (when Phase 0 writers land) or legacy path in config.

See [docs/integrations/dopagaki-transition.md](../../docs/integrations/dopagaki-transition.md).
