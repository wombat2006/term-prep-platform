# O-P007-003 — rclone / 外部 CLI ラッパーのみ

Problem:
[P-007](../PROBLEMS.md#p-007)

Status:
proposed

---

## 概要

platform は **専用 adapter を書かず**、rclone 等の既存 sync CLI を `scripts/sync_corpus.py` から呼ぶ。config は `source.rclone_remote` と `local_mirror` のみ。

## メリット

- Drive · S3 · 多数 backend を一括でカバー
- 実装コスト最小 — Phase 0.5-1 だけで試せる

## デメリット

- 実行環境に rclone バイナリ依存
- 細かい OAuth フローを platform 内で制御しにくい
- MCP からの呼び出しは subprocess 前提

## 関連 Phase

TO-BE **Phase 0.5-1**（O-P007-001 の軽量版）
