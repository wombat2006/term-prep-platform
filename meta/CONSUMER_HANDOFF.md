# Consumer entry point — term-prep-platform

**対象:** techdev-cursor / dopagaki / 新規 consumer の maintainer / AI agent  
**このファイルを先に読んでください。** 他の consumer-handoff ドキュメントへのリンクはここから辿れます。

---

## 概要

`term-prep-platform` は用語抽出・ノイズ除去・コーパス同期の共通前処理を提供するプラットフォームです。

consumer は **package entrypoint を呼び出すだけ**で利用できます。
このリポジトリのコードを直接編集したり、sibling path で参照したりする必要はありません。

```
Consumer side                    Platform side
─────────────────────            ─────────────────────────────────
meta/glossary-config.json   →    term-prep-extract (CLI)
npm run glossary:extract    →    term-prep-sync    (CLI)
.cursor/mcp.json            →    term-prep-glossary-knowledge-mcp (MCP)
CI: term-prep-contract-check
```

---

## Consumer read order（全員必読）

| # | ファイル | 何が分かるか |
|---|----------|------------|
| **1** | [consumer-handoff/01-platform-status.md](./consumer-handoff/01-platform-status.md) | 各 Phase の実装状況・consumer への影響 |
| **2** | [consumer-handoff/02-schema-and-cli.md](./consumer-handoff/02-schema-and-cli.md) | 設定スキーマ・呼び出し CLI・環境変数 |
| **3** | [consumer-handoff/05-platform-implementation.md](./consumer-handoff/05-platform-implementation.md) | Platform が何を実装したかの詳細 |
| **4** | [consumer-handoff/04-consumer-pr-guide-techdev-cursor.md](./consumer-handoff/04-consumer-pr-guide-techdev-cursor.md) | consumer 側 PR テンプレート（sibling → package 切り替え） |
| **5** | [consumer-handoff/03-consumer-actions.md](./consumer-handoff/03-consumer-actions.md) | 自分でやること一覧（Phase 0 / 0.5 / Plan B） |
| **6** | [consumer-handoff/CHANGELOG.md](./consumer-handoff/CHANGELOG.md) | consumer 向け変更履歴（日付順） |
| **7** | [contracts/README.md](./contracts/README.md) | Plan B service 契約 canon（将来参照用） |

---

## 現在の production 契約（1.x パッケージ）

```bash
# インストール
pip install term-prep-platform==1.0.0

# 設定確認
term-prep-contract-check --config meta/glossary-config.json --expect-major 1
term-prep-extract --check --config meta/glossary-config.json

# 抽出実行
term-prep-extract --config meta/glossary-config.json
# → meta/glossary-adopt.json, meta/glossary-hold.json

# ミラー同期（Phase 0.5 / Drive 認証後）
term-prep-sync --config meta/glossary-config.json

# MCP 登録（.cursor/mcp.json）
"glossary-knowledge": { "command": "term-prep-glossary-knowledge-mcp" }
```

---

## 変更ルール（consumer が知っておくべきこと）

| ルール | 詳細 |
|--------|------|
| **Semver MAJOR = 契約変更** | MAJOR が変わるまで CLI / schema / MCP は後方互換を保証 |
| **CI ゲート** | `term-prep-contract-check --expect-major 1` を必ず CI に入れる |
| **プロバイダ透過** | Anthropic / Google / Ollama の追加・変更は consumer コード変更不要 |
| **エラーコードは安定** | `ErrorEnvelope.error.code` は 1.x 内で変わらない（message は変わりうる） |

---

## 参照リンク（目的別）

| 目的 | リンク |
|------|--------|
| 最新の変更を確認 | [consumer-handoff/CHANGELOG.md](./consumer-handoff/CHANGELOG.md) |
| techdev-cursor の移行状況 | [consumer-handoff/consumers/techdev-cursor.md](./consumer-handoff/consumers/techdev-cursor.md) |
| 新規 consumer チェックリスト | [consumer-handoff/consumers/_TEMPLATE.md](./consumer-handoff/consumers/_TEMPLATE.md) |
| CI テンプレート | [consumer-handoff/templates/consumer-contract-ci.yml](./consumer-handoff/templates/consumer-contract-ci.yml) |
| LLM プロバイダ透過ポリシー | [contracts/llm-provider-policy.md](./contracts/llm-provider-policy.md) |
| Plan B 契約詳細 (HTTP / SSE / MCP) | [contracts/README.md](./contracts/README.md) |
| 廃止: A+C cross-repo bot ワークフロー | [consumer-handoff/06-cross-repo-workflow.md](./consumer-handoff/06-cross-repo-workflow.md) (legacy) |

---

## 役割分担（絶対ルール）

> **Platform は consumer repo を直接編集しない。Consumer は platform repo を直接編集しない。**

- platform 側の変更は consumer-handoff docs + CHANGELOG に記録
- consumer は [04-consumer-pr-guide-techdev-cursor.md](./consumer-handoff/04-consumer-pr-guide-techdev-cursor.md) を参照して自分で PR を開く
- ブロックが発生した場合は [03-consumer-actions.md § Escalation](./consumer-handoff/03-consumer-actions.md#escalation-template-consumer--user) のテンプレートを使う

---

## Platform maintainer checklist（更新時）

- [ ] [consumer-handoff/CHANGELOG.md](./consumer-handoff/CHANGELOG.md) に日付エントリを追加
- [ ] [consumer-handoff/01-platform-status.md](./consumer-handoff/01-platform-status.md) の Phase 表を更新
- [ ] [consumer-handoff/02-schema-and-cli.md](./consumer-handoff/02-schema-and-cli.md) と package entrypoint を同期
- [ ] schema / CLI 変更があれば package Semver を更新して publish
