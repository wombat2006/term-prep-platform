# Scripts

Project:
term-prep-platform

---

## Position in target flow

`glossary_extractor.py` は Prep Platform パイプラインの **extract → noise filter → term registry** 区間を担う CLI 入口（PII / sanitize は upstream MCP、registry 以降の RAG / 辞書 / query expander は consumer）。

```text
社内データ → [PII MCP] → [sanitize MCP] → glossary_extractor → term registry → RAG / glossary / query expander
```

図解: [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)

---

## Setup

```bash
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -r requirements-mcp.txt
```

**System:** MeCab (`libmecab`)

| OS | Command |
|---|---|
| AlmaLinux / RHEL 9 | `sudo dnf install mecab`（`mecab-devel` は **不要** — AppStream に無い） |
| Debian/Ubuntu | `sudo apt install mecab libmecab-dev` |
| macOS | `brew install mecab` |

**Python:** 必ず repo ルートの `.venv` を activate してから CLI を実行する。システム Python にだけ `jsonschema` 等を入れても、`.venv/bin/python` 実行時には効かない。

---

## glossary_extractor.py

Extract glossary candidates from Markdown using **fugashi + unidic-lite**.

```bash
# Default config path: meta/glossary-config.json (legacy)
# Consumer configs live under projects/
python scripts/glossary_extractor.py --check \
  --config projects/dopagaki-transition/glossary-config.json

python scripts/glossary_extractor.py \
  --config projects/dopagaki-transition/glossary-config.json
```

**Governance:** [meta/glossary-pipeline/](../meta/glossary-pipeline/README.md)  
**Roadmap:** [meta/TO-BE-PLATFORM.md](../meta/TO-BE-PLATFORM.md)  
**Config schema:** [meta/schemas/README.md](../meta/schemas/README.md)

Exit codes: `0` success · `1` config / IO / **JSON Schema 不一致** · `2` morphology unavailable

### Config 検証（注意）

- `load_config()` が [meta/schemas/glossary-config.schema.json](../meta/schemas/glossary-config.schema.json) で検証する。**`--check` も本番も同じ**
- 依存: `jsonschema>=4.23.0`（`requirements-dev.txt`）
- スキーマエラー例: `output` をオブジェクトにしたが `adopt` 欠落、`filter` に typo キー、semver 以外の `version`
- **legacy:** `output` を文字列 1 本にした旧形式もスキーマ上は許容（Phase 0 移行済み PRJ ではオブジェクト推奨）
- **`project_root`:** `--config` パスの親から解決。実行時 CWD は repo ルート想定だが、パス解決の基準は config ファイル側
- **`filter.emit_reject`:** デフォルト `false` — `true` にしない限り reject JSONL は書かない（Git 衛生）

---

## File roles

| File | Role |
|---|---|
| `scripts/glossary_extractor.py` | Shared extraction CLI |
| `meta/schemas/glossary-config.schema.json` | Config JSON Schema (validated on load) |
| `projects/<consumer>/glossary-config.json` | Per-project corpus & scoring |
| `build/glossary/` | Generated adopt/hold/reject (Git ignored) |
