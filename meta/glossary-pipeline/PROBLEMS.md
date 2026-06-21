# Glossary Pipeline — 問題一覧

Status:
Living document

---

問題は **現象・制約** を記述する。解決手段は [OPTIONS.md](OPTIONS.md) / [options/](options/) へ。

---

## P-001

### 出力 JSON の肥大化

**現象:** 単一 `glossary-candidates.json` に adopt + hold + reject 全件。corpus 増加で MB 級。

**本 PRJ の観測（2026-06-21）:** Accepted 原稿 7 ファイル → ~255 KB、693 件（reject 93%）。

**影響:** Git  diff ノイズ、レビュー不能、CI 遅延。

**関連 Phase:** TO-BE Phase 0

---

## P-002

### 開世界抽出によるノイズ

**現象:** 名詞全量を先に抽出し、後から stop / スコア。一般名詞が大量に候補化。

**影響:** 採択判断コスト増。manual_adopt / stop リストの手メンテ。

**関連 Phase:** TO-BE Phase 2（registry seed-first）

---

## P-003

### 用途 A/B の混在

**現象:** 読者向け GLOSSARY（20–40 語）と RAG 索引（語↔span↔chunk）を同一出力に載せている。

**影響:** スキーマが両方に最適化できない。RAG 改修が Glossary 出力を壊す。

**関連 Phase:** TO-BE 用途分離、Phase 4

---

## P-004

### CLI とロジックの同居

**現象:** `glossary_extractor.py` 単一ファイルに morphology / extract / score / write 全部。

**影響:** 他 PRJ 移植時に diff が大きい。ユニットテスト困難。

**関連 Phase:** TO-BE Phase 1

---

## P-005

### RAG 前処理未対応

**現象:** 語 surface のみ。file / line / span / chunk ID なし。

**影響:** embedding 投入前の term-grounding ができない。

**関連 Phase:** TO-BE Phase 4

---

## P-006

### 複合語・英日ペア未統合

**現象:** 「注意」「経済」と「注意経済」が別候補。`Attention Scarcity` と日本語説明が別 entry。

**影響:** 用語集・索引の重複。読者混乱。

**関連 Phase:** TO-BE Phase 2（rank）

---

## P-007

### 外部 corpus の fetch が利用側に分散

**現象:** Google Drive · S3 等から Markdown を取る処理が consumer ごと（例: techdev-cursor の `googledrive-connector.ts`）にあり、platform は **ローカル `corpus.files` 前提** のみ。同じ sync ロジックを prep 利用側ごとに書きがち。

**本 PRJ の観測（2026-06-21）:** techdev-cursor は Drive → RAG 用 connector あり。glossary 用 corpus mirror パスは config 未固定。dopagaki は sibling 原稿 repo を手動参照。

**影響:** 複数 consumer で fetch 重複。prep 入口（mirror → PII → …）を platform 1 本で説明しにくい。一方で ingest を platform に寄せすぎると OAuth · 差分 sync でスコープ膨張。

**関連 Phase:** TO-BE **Phase 0.5**（Source connector — 提案）

**方針メモ（2026-06-21）:** Google Drive は techdev-cursor [`googledrive-connector.ts`](https://github.com/wombat2006/techdev-cursor/blob/master/src/services/googledrive-connector.ts) を platform へ移管・流用 — [O-P007-004](options/O-P007-004-googledrive-connector-reuse.md)

---

## P-008

### RAG Vector 投入が利用側に閉じている

**現象:** OpenAI Vector Store 等への chunk 投入は consumer（techdev-cursor `googledrive-connector.ts`）に実装があるが、platform 公式パスとして共通化されていない。prep 後の Vector 連携（Phase 4 hook）も未配線。

**影響:** 「Drive → prep → RAG」を複数 consumer で再実装しがち。mirror だけ platform 化しても Vector 側がバラける。

**関連 Phase:** TO-BE **Phase 4.5**（RAG Vector connector — 提案）— Drive 流用 connector の `vector` モードと一体

---

## 追加用テンプレート

```markdown
## P-0NN

### {タイトル}

**現象:**

**本 PRJ の観測:**

**影響:**

**関連 Phase:**
```
