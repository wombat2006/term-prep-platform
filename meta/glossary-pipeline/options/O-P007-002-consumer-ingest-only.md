# O-P007-002 — ingest は利用側のまま（現状維持）

Problem:
[P-007](../PROBLEMS.md#p-007)

Status:
proposed

---

## 概要

外部 fetch は **利用側リポジトリ**（例: techdev-cursor の `googledrive-connector.ts`）に置いたまま、platform はローカル `corpus.files` の prep のみを担う。

## メリット

- platform スコープが膨らまない
- 言語・認証・RAG 連携を consumer の TS スタックに任せられる
- Phase 0 の `glossary_extractor` を変更せずに済む

## デメリット

- S3 · Drive ごとに consumer 実装が増える
- 「fetch から registry まで platform 一本」というストーリーに弱い

## 採択条件

- consumer が 1–2 個で ingest 方式がバラバラ
- 共通化の運用コスト > 重複コスト

## 関連 Phase

現状 AS-IS のまま — Phase 0.5 は **見送り**
