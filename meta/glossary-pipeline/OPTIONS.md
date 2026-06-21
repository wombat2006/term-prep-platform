# Glossary Pipeline — 手段案インデックス

Status:
Living document

---

各問題に対し **複数案を並記** し、採択前に比較する。詳細は [options/](options/) の個別ファイル。採択後は [DECISIONS.md](DECISIONS.md) へ。

**ステータス:** `proposed` | `adopted` | `rejected` | `superseded`

---

## 一覧

| ID | Problem | 案 | Status | 概要 |
|---|---|---|---|---|
| O-P001-001 | P-001 | reject を Git 外へ | proposed | JSONL + .gitignore |
| O-P001-002 | P-001 | adopt/hold のみ JSON | proposed | 出力 2 ファイル |
| O-P001-003 | P-001 | SQLite 単一 DB | proposed | 大 scale 向け |
| O-P002-001 | P-002 | seed-first（registry 先行） | proposed | 閉世界優先 |
| O-P002-002 | P-002 | min_freq / min_doc 閾値強化 | proposed | 事後 filter 強化 |
| O-P002-003 | P-002 | TF-IDF / 一般語コーパス差分 | proposed | 統計 filter |
| O-P002-004 | P-002 | MCP — 既知/専門語判別 | closed (stub) | Knowledge filter（MCP + provider） |
| O-P003-001 | P-003 | writer 分離（glossary / rag） | proposed | 用途別出力 |
| O-P003-002 | P-003 | repo 分離（辞典 PRJ 専用） | proposed | RAG は別 repo |
| O-P004-001 | P-004 | scripts/glossary/ パッケージ化 | proposed | 薄い CLI 維持 |
| O-P004-002 | P-004 | pip package 化 | proposed | 長期・複数 repo |
| O-P005-001 | P-005 | span + chunk index | proposed | Phase 4 基本 |
| O-P005-002 | P-005 | 章単位 chunk のみ（簡易） | proposed | 最小 RAG 準備 |
| O-P006-001 | P-006 | seed 最長一致マージ | proposed | registry ベース |
| O-P006-002 | P-006 | 英日 alias テーブル | proposed | 手動 + 半自動 |

---

## P-001 {#p-001}

出力 JSON の肥大化

| 案 | メリット | デメリット | Status |
|---|---|---|---|
| [O-P001-001](options/O-P001-001-reject-jsonl.md) | Git  clean、reject 調査可能 | build/ 管理が要る | proposed |
| [O-P001-002](options/O-P001-002-adopt-hold-split.md) | レビュー容易、小さい正典 | reject 見えない | proposed |
| O-P001-003 | クエリ・索引向き | 依存増、初期コスト | proposed |

**メモ:** O-P001-001 + O-P001-002 の併用が TO-BE Phase 0 の想定。

---

## P-002 {#p-002}

開世界抽出によるノイズ

| 案 | メリット | デメリット | Status |
|---|---|---|---|
| O-P002-001 | ノイズ根本削減 | registry 整備が先決 | proposed |
| O-P002-002 | 実装簡単 | 根本解決にならない | proposed |
| O-P002-003 | 一般語除去に強い | コーパス・計算コスト | proposed |
| [O-P002-004](options/O-P002-004-external-knowledge-filter.md) | 一般語除去、PRJ 横断、Cursor 連携 | MCP 運用・API コスト | closed (stub) |

**メモ:** O-P002-001（閉世界）を土台に、O-P002-004 は **第2段フィルタ** として併用が自然。API 単独では neologism（ドパガキ）を誤除外しうる。

## P-003 {#p-003}

用途 A/B の混在

| 案 | メリット | デメリット | Status |
|---|---|---|---|
| O-P003-001 | 同一 repo 内で分離 | writer 実装が要る | proposed |
| O-P003-002 | 関心完全分離 | 二重メンテ | proposed |

---

## P-004 {#p-004}

CLI とロジックの同居

| 案 | メリット | デメリット | Status |
|---|---|---|---|
| O-P004-001 | 段階的移行、CLI 安定 | 一時的に二重構造 | proposed |
| O-P004-002 | バージョン管理明確 | 公開・配布コスト | proposed |

**メモ:** 当面 O-P004-001。O-P004-002 は複数 PRJ 安定後。

---

## P-005 {#p-005}

RAG 前処理未対応

| 案 | メリット | デメリット | Status |
|---|---|---|---|
| O-P005-001 | RAG 完全対応 | 工数大 | proposed |
| O-P005-002 | 早い着手 | 精度・粒度限定 | proposed |

---

## P-006 {#p-006}

複合語・英日ペア未統合

| 案 | メリット | デメリット | Status |
|---|---|---|---|
| O-P006-001 | 追加データ少 | registry 依存 | proposed |
| O-P006-002 | 明示的 | 手メンテ | proposed |

---

## 新規案の追加

1. [options/_TEMPLATE.md](options/_TEMPLATE.md) をコピー
2. `options/O-P{ppp}-{nnn}-{slug}.md` として記述
3. 本ファイルの一覧表に 1 行追加
4. 採択時は [DECISIONS.md](DECISIONS.md) に D-xxx を起票
