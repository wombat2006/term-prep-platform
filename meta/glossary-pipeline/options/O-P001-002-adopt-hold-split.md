# O-P001-002: adopt / hold のみ JSON（正典側）

Status:
proposed

Problem:
[P-001](../PROBLEMS.md#p-001) — 出力 JSON の肥大化

---

## 概要

Git 追跡するのは `meta/glossary-adopt.json` と `meta/glossary-hold.json` のみ。単一 `glossary-candidates.json` を廃止。

---

## 仕組み

```json
"output": {
  "adopt": "meta/glossary-adopt.json",
  "hold": "meta/glossary-hold.json",
  "reject": "build/glossary/reject.jsonl"
}
```

- adopt: 数十件想定
- hold: レビュー待ち（任意で Git 追跡）

---

## メリット

- PR レビューが現実的なサイズ
- GLOSSARY 更新の入力が明確

## デメリット

- ファイルが 2–3 に増える
- 既存 `glossary-candidates.json` からの移行が要る

---

## 適用条件

- 向く PRJ: 人間採択型 Glossary がある全 repo
- 向かない PRJ: 機械出力のみで全件 API 投入する pipeline

---

## 他案との関係

- 併用可: [O-P001-001](O-P001-001-reject-jsonl.md)
- 排他: 単一 candidates.json 継続
