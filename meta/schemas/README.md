# glossary-config JSON Schema

Project:
term-prep-platform

Schema:
[glossary-config.schema.json](./glossary-config.schema.json)

Platform scope（本 repo が RAG 本体を提供しない理由含む）: [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md#scope--この-prj-が提供するもの)

---

## 役割

`scripts/glossary_extractor.py` が `--config` を読むたびに、このスキーマで **起動前検証** する。設定ミスを実行後ではなく CLI 入口で止める（TO-BE T1-4）。

---

## 依存

| 項目 | 内容 |
|---|---|
| Python パッケージ | `jsonschema>=4.23.0`（[requirements-dev.txt](../../requirements-dev.txt)） |
| 検証タイミング | `load_config()` — **`--check` でも本番実行でも同じ** |
| 失敗時 | stderr に `Config schema error: …`、**exit code `1`** |

---

## Phase 0 推奨 shape

新規・移植 config は [glossary-config.template.json](../glossary-pipeline/glossary-config.template.json) または [projects/_template/glossary-config.json](../../projects/_template/glossary-config.json) をコピーする。

| 節 | 必須 | 注意 |
|---|---|---|
| `version` | ✅ | semver 形式（例 `1.0.0`） |
| `project_root` | ✅ | **config ファイル位置からの相対パス**（CWD ではない） |
| `morphology` | ✅ | `backend: fugashi`、`dictionary: unidic-lite` 等 |
| `corpus.files` | ✅ | `project_root` からの相対パス。空配列はスキーマ上 OK だが抽出結果は空 |
| `scoring` | ✅ | `adopt_threshold` / `hold_threshold` / `weights` |
| `filter` | 推奨 | `emit_reject: false` デフォルト — reject は Git 外 |
| `output` | 推奨 | **オブジェクト** — `adopt` と `hold` が必須。文字列 1 本は legacy |
| `knowledge_filter` | 推奨 | Phase 2.5 用。`enabled: false` でも節ごと置く |

---

## スキーマの厳しさ

- **ルート** — 未知キーは許容（`$comment` 等）
- **`filter` / `output` / `knowledge_filter` / `morphology` / `scoring.weights`** — **未知キーは拒否**（ typo を早く見つける）
- **`output` がオブジェクト** — `adopt` と `hold` 必須。`registry` / `reject` / `legacy_candidates` は任意

config に新しい正式フィールドを足すときは **先にこの schema を更新** し、テンプレートと consumer config を揃える。

---

## 手動検証

```bash
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

python scripts/glossary_extractor.py --check \
  --config projects/dopagaki-transition/glossary-config.json
```

スキーマだけ試す例:

```bash
python -c "
import json
from pathlib import Path
import jsonschema
schema = json.loads(Path('meta/schemas/glossary-config.schema.json').read_text())
cfg = json.loads(Path('projects/techdev-cursor/glossary-config.json').read_text())
jsonschema.validate(cfg, schema)
print('OK')
"
```

---

## 移植時

glossary ツールごとコピーする場合:

```bash
cp -r meta/schemas /path/to/other-project/meta/
cp meta/glossary-pipeline/glossary-config.template.json /path/to/other-project/meta/glossary-config.json
```

`glossary_extractor.py` も同梱する。schema パスは repo ルート基準 `meta/schemas/` を想定。

---

## 関連

- [scripts/README.md](../../scripts/README.md) — CLI・exit code
- [meta/TO-BE-PLATFORM.md](../TO-BE-PLATFORM.md) — T1-4 完了条件
- [docs/integrations/](../integrations/) — consumer 別 config
