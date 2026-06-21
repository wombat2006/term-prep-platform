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

## 追加用テンプレート

```markdown
## P-0NN

### {タイトル}

**現象:**

**本 PRJ の観測:**

**影響:**

**関連 Phase:**
```
