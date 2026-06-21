# Platform TODO

Project:
term-prep-platform

Status:
Living checklist — [TO-BE-PLATFORM.md](TO-BE-PLATFORM.md) の実行用サマリ

**最終更新:** 2026-06-21

---

## 凡例

| 記号 | 意味 |
|---|---|
| `[x]` | 完了 |
| `[ ]` | 未着手 |
| `[~]` | 一部 / stub |

---

## Phase 0 — 出力・schema（**完了**）

- [x] adopt / hold / reject 出力分割（`write_outputs`）
- [x] `glossary-config` JSON Schema + CLI 起動時検証
- [x] consumer config サンプル（dopagaki · techdev-cursor）
- [x] ドキュメント（README · ARCHITECTURE · integrations）

---

## Phase 0.5 — Source connector（**提案 · 次の Epic**）

**目的:** 外部ストレージ → ローカル corpus mirror → 既存 prep。

**Google Drive 方針:** techdev-cursor [`googledrive-connector.ts`](https://github.com/wombat2006/techdev-cursor/blob/master/src/services/googledrive-connector.ts) を platform へ **移管・流用**（Python 新規実装しない）— [O-P007-004](glossary-pipeline/options/O-P007-004-googledrive-connector-reuse.md)

Governance: [P-007](glossary-pipeline/PROBLEMS.md#p-007) · [OPTIONS § P-007](glossary-pipeline/OPTIONS.md#p-007)

### 0.5-0 — 設計・governance

- [ ] `SourceConnector` 最小 contract（list · sync · local_root）— S3 / 汎用は Python
- [ ] `glossary-config` に `source` 節の schema 案
- [ ] googledrive 流用の移管計画（platform `connectors/googledrive/` · consumer re-export）

### 0.5-1 — ローカル mirror contract

- [ ] `build/corpus/` を Git 外 staging として docs に定義
- [ ] `corpus.files` が mirror 相対パスを指す例を `_template` に追加

### 0.5-2 — S3 / 互換ストレージ adapter

- [ ] `scripts/connectors/s3.py` skeleton（Drive 以外）
- [ ] 認証: env / IAM role のみ

### 0.5-3 — Google Drive（googledrive-connector 流用）

- [ ] platform `connectors/googledrive/` に techdev-cursor から移管
- [ ] **`mirror` モード** — Vector 非経由で `build/corpus/` へ sync
- [ ] techdev-cursor が platform パッケージを参照するよう更新（利用側 PR）
- [ ] prep 連携 smoke: mirror → `glossary_extractor`

---

## Phase 4.5 — RAG Vector connector（**提案**）

**目的:** prep 後の **Vector Store 投入**も platform が共通化。Drive 接続は 0.5-3 と **同一 TS モジュール**の `vector` モード。

Governance: [P-008](glossary-pipeline/PROBLEMS.md#p-008) · [O-P008-001](glossary-pipeline/options/O-P008-001-rag-vector-connector.md)

- [ ] `vector` モード contract（prep 完了 hook · vector_store_id）
- [ ] techdev-cursor Phase 4 hook を platform 公式パスに接続
- [ ] config `outputs.rag` schema 案
- [ ] dopagaki 等 Drive 非利用 consumer では optional のまま維持

---

## Phase 1 — Core 分離

- [ ] `scripts/glossary/` パッケージ化（T1-1）
- [ ] `morphology.py` · `writers.py` 分離
- [ ] `registry.py` seed 生成（T2-1）

---

## Phase 2 / 2.5 — filter · MCP

- [ ] seed-first · rank 強化
- [ ] `glossary-knowledge` MCP を stub から実 provider へ（D-002 以降）

---

## Phase 3–4 — GLOSSARY 提案 · RAG subpackage

- [ ] `--diff-glossary`
- [ ] `build/rag/` · `--rag-index`（Python 側 term index — Vector とは別）

---

## 参照

- [TO-BE-PLATFORM.md](TO-BE-PLATFORM.md) — AS-IS / To-Be · ロードマップ図
- [glossary-pipeline/](glossary-pipeline/README.md) — PROBLEMS / OPTIONS / DECISIONS
