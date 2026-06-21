# O-P001-001: reject を Git 外 JSONL へ

Status:
proposed

Problem:
[P-001](../PROBLEMS.md#p-001) — 出力 JSON の肥大化

---

## 概要

reject 候補を `build/glossary/reject.jsonl` に書き出し、`.gitignore` で Git 追跡から外す。

---

## 仕組み

- `glossary-config.json` → `filter.emit_reject: true`, `output.reject: build/glossary/reject.jsonl`
- `writers.py` が 1 行 1 candidate の JSONL を append または上書き
- CI artifact として保存可能

---

## メリット

- Git 履歴が clean
- reject はローカル調査用に残せる
- adopt/hold だけレビュー対象にできる

## デメリット

- `build/` ディレクトリ規約が要る
- clone 直後は reject ファイル無し

---

## 適用条件

- 向く PRJ: 全規模。特に corpus が大きい repo
- 向かない PRJ: reject も永久保存したい rare case

---

## 他案との関係

- 併用可: [O-P001-002](O-P001-002-adopt-hold-split.md)
- 排他: なし
