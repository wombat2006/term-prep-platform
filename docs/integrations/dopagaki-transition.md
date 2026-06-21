# Integration: dopagaki-transition

Consumer: [wombat2006/dopagaki-transition](https://github.com/wombat2006/dopagaki-transition)

---

## Role in platform flow

dopagaki-transition は **Outputs: glossary** 側 — 原稿 MD を ingest し、prep 後の adopt/hold を人間が `GLOSSARY.md` に反映する。

```text
原稿 MD（社内データ）→ [prep: term-prep-platform] → term registry → GLOSSARY.md
```

図解: [ARCHITECTURE.md](../ARCHITECTURE.md)

---

## Use case

Research manuscript glossary — extract terms from Accepted chapters → human curation → `GLOSSARY.md` with TS/ADR links.

---

## Config

[projects/dopagaki-transition/glossary-config.json](../projects/dopagaki-transition/glossary-config.json)

**Note:** `project_root` points at dopagaki repo when running extractor:

```bash
cd /path/to/term-prep-platform
python scripts/glossary_extractor.py \
  --config projects/dopagaki-transition/glossary-config.json
```

Adjust `project_root` in config if layout differs.

---

## Relationship

Platform extracted from dopagaki @ `5306a8b`. dopagaki keeps consumer copy of config and `GLOSSARY.md`; platform holds shared MCP + governance.
