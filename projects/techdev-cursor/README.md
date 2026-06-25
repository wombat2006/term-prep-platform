# techdev-cursor — consumer config

Consumer: [techdev-cursor](https://github.com/wombat2006/techdev-cursor)

**Consumer agents:** read platform progress at [meta/consumer-handoff/consumers/techdev-cursor.md](../../meta/consumer-handoff/consumers/techdev-cursor.md). **Open consumer PR using** [04-consumer-pr-guide-techdev-cursor.md](../../meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md) — platform does not edit techdev-cursor.

Phase 0: adopt/hold output split, `filter` / `output` / `knowledge_filter` schema aligned with dopagaki-transition. Config は起動時に platform schema で検証（[注意点](../../meta/schemas/README.md)）。

Fill `corpus.files` when Google Drive sync local path is defined — see Phase 0.5 mirror below.

Export target (planned): `config/fork/devassist-dictionary-v0.json`

| File | Role |
|------|------|
| [glossary-config.json](./glossary-config.json) | Platform mirror (`project_root` → consumer repo) |
| Consumer [meta/glossary-config.json](https://github.com/wombat2006/techdev-cursor/blob/master/meta/glossary-config.json) | Runtime config path for `--config` |
| Consumer `meta/glossary-adopt.json` / `hold.json` | Git-tracked outputs (stubs until first extract) |

Run:

```bash
python scripts/glossary_extractor.py --check --config projects/techdev-cursor/glossary-config.json
```

See [docs/integrations/techdev-cursor.md](../../docs/integrations/techdev-cursor.md) · [consumer TO-BE](https://github.com/wombat2006/techdev-cursor/blob/master/meta/TO-BE-GLOSSARY-PIPELINE.md).
