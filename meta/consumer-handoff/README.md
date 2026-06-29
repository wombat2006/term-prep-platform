# Consumer handoff index — package contract migration

**Audience:** techdev-cursor / dopagaki maintainers  
**Start here:** [../CONSUMER_HANDOFF.md](../CONSUMER_HANDOFF.md) — top entry point with read order  
**Status:** Active migration guide (cross-repo A+C bot deprecated 2026-06-29)

---

## Migration summary

sibling path coupling (`../term-prep-platform`) と cross-repo issue bot を廃止し、
**versioned package contract** に移行しています。

| Surface | New contract |
|---|---|
| Extract CLI | `term-prep-extract` |
| Sync CLI | `term-prep-sync` |
| MCP server | `term-prep-glossary-knowledge-mcp` |
| Schema | `meta/schemas/glossary-config.schema.json` in package release |
| Versioning | Semver（MAJOR = contract break） |

Decision: [D-004](../glossary-pipeline/DECISIONS.md#d-004)

---

## Numbered read order（このフォルダの各ファイル）

| Step | File | 何が分かるか |
|---|---|---|
| 0 | **[../CONSUMER_HANDOFF.md](../CONSUMER_HANDOFF.md)** | 全体 TOP・read order・役割分担 |
| 1 | [01-platform-status.md](./01-platform-status.md) | 各 Phase の実装状況と consumer への影響 |
| 2 | [05-platform-implementation.md](./05-platform-implementation.md) | Platform が何を実装したかの詳細 |
| 3 | [02-schema-and-cli.md](./02-schema-and-cli.md) | 設定スキーマ・CLI・環境変数 |
| 4 | [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md) | consumer 側 PR テンプレート |
| 5 | [03-consumer-actions.md](./03-consumer-actions.md) | 自分でやること一覧 |
| 6 | [CHANGELOG.md](./CHANGELOG.md) | consumer 向け変更履歴 |
| 7 | [../contracts/README.md](../contracts/README.md) | Plan B service 契約 canon（将来参照用） |

---

## Plan B contract canon（将来参照）

Remote service（Plan B）実装前に契約を先に確定しています。
consumer の即時対応は不要ですが、将来の remote 採用時に参照します。

- [../contracts/README.md](../contracts/README.md)
- [../contracts/http/openapi.yaml](../contracts/http/openapi.yaml)
- [../contracts/sse/event-envelope.schema.json](../contracts/sse/event-envelope.schema.json)
- [../contracts/mcp-tool-contract.md](../contracts/mcp-tool-contract.md)
- [../contracts/connector-spi.md](../contracts/connector-spi.md)
- [../contracts/llm-provider-policy.md](../contracts/llm-provider-policy.md)

---

## Deprecated

- [06-cross-repo-workflow.md](./06-cross-repo-workflow.md) — A+C issue bot（廃止済み）
- `scripts/cross_repo/*` helpers（廃止済み）
- `projects/techdev-cursor/*` mirror config in this repo（廃止済み）

---

## Platform maintainer checklist

- [ ] [CHANGELOG.md](./CHANGELOG.md) に consumer-facing 変更を記録
- [ ] [02-schema-and-cli.md](./02-schema-and-cli.md) を package scripts と同期
- [ ] [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md) を最新状態に保つ
- [ ] schema / CLI 変更時は package Semver 更新 + publish

---

## Related

- [docs/integrations/techdev-cursor.md](../../docs/integrations/techdev-cursor.md)
- [meta/schemas/glossary-config.schema.json](../schemas/glossary-config.schema.json)
- [connectors/googledrive/README.md](../../connectors/googledrive/README.md)
