# Platform TODO

Project:
term-prep-platform

Status:
Living checklist — [TO-BE-PLATFORM.md](TO-BE-PLATFORM.md) の実行用サマリ

**最終更新:** 2026-06-29

**Consumer handoff:** 進捗・schema・consumer 側作業は [meta/consumer-handoff/](../consumer-handoff/README.md) を更新すること。

**Decoupling:** D-004（artifact boundary / package contract）を正とする。sibling 追従と cross-repo bot は deprecated。

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

- [x] `SourceConnector` 最小 contract（list · sync · local_root）— S3 / 汎用は Python
- [x] `glossary-config` に `source` 節の schema 案
- [~] googledrive 流用の移管計画（platform `connectors/googledrive/` · consumer re-export）

### 0.5-1 — ローカル mirror contract

- [x] `build/corpus/` を Git 外 staging として docs に定義
- [x] `corpus.files` が mirror 相対パスを指す例を `_template` に追加
- [x] `corpus.files` glob 対応（`glossary_extractor`）

### 0.5-2 — S3 / 互換ストレージ adapter

- [ ] `scripts/connectors/s3.py` skeleton（Drive 以外）
- [ ] 認証: env / IAM role のみ
- [ ] **Terraform** `modules/s3-mirror` · `iam-prep-batch` · `kms-secrets`（[D-003](glossary-pipeline/DECISIONS.md#d-003) · [docs/IAC.md](../docs/IAC.md)）

### 0.5-3 — Google Drive（googledrive-connector 流用）

- [x] platform `connectors/googledrive/` に mirror モード実装（TS · consumer パターン流用）
- [x] **`mirror` モード** — Vector 非経由で `build/corpus/drive/` へ sync
- [x] `scripts/sync_corpus.py` — config `source` から mirror 起動
- [ ] techdev-cursor が platform パッケージを参照するよう更新（利用側 PR — **ユーザー適用**）
- [ ] prep 連携 smoke: mirror → `glossary_extractor`（**要 Drive 認証 — 後日実施**）
- [x] credential なしテスト — `scripts/run_phase05_checks.sh` · `tests/test_phase05_no_credentials.py` · `connectors/googledrive` `npm test`

---

## Phase 4.5 — RAG Vector connector（**提案**）

**目的:** prep 後の **Vector Store 投入**も platform が共通化。Drive 接続は 0.5-3 と **同一 TS モジュール**の `vector` モード。

Governance: [P-008](glossary-pipeline/PROBLEMS.md#p-008) · [O-P008-001](glossary-pipeline/options/O-P008-001-rag-vector-connector.md)

- [ ] `vector` モード contract（prep 完了 hook · vector_store_id）
- [ ] techdev-cursor Phase 4 hook を platform 公式パスに接続
- [ ] config `outputs.rag` schema 案
- [ ] dopagaki 等 Drive 非利用 consumer では optional のまま維持

---

## Decoupling migration（D-004）

- [x] 採択ログ（D-004）と option 文書（O-P009-001）を追加
- [x] package entrypoint（`term-prep-extract`, `term-prep-sync`, `term-prep-glossary-knowledge-mcp`）を実装
- [x] cross-repo bot / sibling mirror assets を削除
- [x] consumer cutover PR ガイドを package 契約へ更新
- [x] contract check CLI + consumer CI template を追加
- [ ] techdev-cursor 側 PR で package pin へ切替（ユーザー適用）

---

## Plan B prep（D-005, contract-first）

- [x] `b0-contract-canon` 実装契約（domain / error / version policy）を canonical spec に固定
- [x] `b0-surface-spec` MCP / HTTP / SSE / CLI の surface contract と互換性ルールを定義
- [x] `b0-connector-sdk` Connector SPI / conformance 要件を定義
- [ ] `b1-service-skeleton` 契約準拠 service skeleton（HTTP + SSE + MCP adapter）最小実装
- [ ] `b1-consumer-adapter` techdev-cursor adapter を契約準拠で置換（feature flag）
- [ ] `b1-contract-ci` compatibility matrix / backward-compat CI を導入
- [ ] `b2-consumer-handoff` 方針・計画・影響を consumer へ継続伝達

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
- [consumer-handoff/](consumer-handoff/README.md) — consumer 向け進捗・作業リスト
- [docs/ROADMAP-AND-COSTS.md](../docs/ROADMAP-AND-COSTS.md) — 課題→ツール · 開発/運用コスト概算 · Confluence 10k ページ例
- [glossary-pipeline/](glossary-pipeline/README.md) — PROBLEMS / OPTIONS / DECISIONS
- [contracts/](contracts/README.md) — Plan B contract canon（domain/surface/SPI）
