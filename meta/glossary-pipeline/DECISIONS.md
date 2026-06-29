# Glossary Pipeline — 採択ログ

Status:
Living document

---

採択された手段案を記録する。不採択案は [options/](options/) に残す（C-0003 Traceability 準拠）。

---

## 索引

| ID | 日付 | Problem | 採択案 | 実装 |
|---|---|---|---|---|
| D-002 | 2026-06-21 | P-002 | O-P002-004（MCP stub） | closed — [mcp/glossary-knowledge/](../../mcp/glossary-knowledge/) |
| D-003 | 2026-06-21 | （ops） | Terraform（AWS 第一） | planned — [docs/IAC.md](../../docs/IAC.md) |
| D-004 | 2026-06-29 | P-009（repo 間追従による連鎖破綻リスク） | O-P009-001（artifact boundary / Semver 契約） | in progress — package cutover |
| D-005 | 2026-06-29 | P-009-B（Remote service 検討） | Contract-first canon（Domain/Surface/SPI 先行固定） | in progress — [meta/contracts/](../contracts/README.md) |

---

## テンプレート

```markdown
## D-0NN

**日付:** YYYY-MM-DD

**Problem:** P-0NN

**採択:** O-P0NN-0NN

**棄却:** O-P0NN-0MM, …

**理由:**

**実装:** Phase / PR / commit

**影響:** config, TO-BE, scripts/…
```

---

## D-001

（予約 — Phase 0 採択済み 2026-06-21: O-P001-002 adopt/hold split, emit_reject false）

**候補:**

- P-001 → O-P001-001 + O-P001-002
- P-004 → O-P004-001

**Status:** pending decision

---

## D-002 {#d-002}

**日付:** 2026-06-21

**Problem:** P-002（開世界抽出によるノイズ）

**採択:** O-P002-004 — Knowledge Filter を **MCP サーバ** として実装。任意 API は MCP 内 provider adapter で接続。

**棄却:**

- O-P002-004 案A — glossary Core 内 Python provider 直結（主形態）
- REST マイクロサービス単体

**理由:**

- provider 差し替えを glossary Core から分離
- Cursor / CLI / 他 PRJ が同一 MCP 契約で再利用
- API 未選定でも MCP stub + NullProvider で差し口確保

**未決（別 DECISION 待ち）:** 第一プロバイダ（K-003 / K-006 / K-008）。Research Log [RL-20260621](../../research-log/RL-20260621-knowledge-filter-mcp.md) 参照。

**実装:** **stub 完了** — `mcp/glossary-knowledge/`（NullProvider、4 tools）。Research Log [RL-20260621](../../research-log/RL-20260621-knowledge-filter-mcp.md) **closed** 2026-06-21。

**deferred（Phase 2.5 再開時）:** cache、第一 provider、glossary CLI MCP client。

**影響:** `mcp/glossary-knowledge/`, TO-BE Phase 2.5

**必須併用:** O-P002-001 registry seed-first

---

## D-003 {#d-003}

**日付:** 2026-06-21

**Problem:** batch prep 用 infra（S3 mirror · IAM · EC2/ECS）の再現性とレビュー可能性

**採択:** **Terraform**（HCL）を IaC の正とする。配置は `infra/terraform/`。AWS 第一 · Cloudflare は Phase 3+ ops で optional。

**棄却:**

- **AWS CloudFormation** — AWS 単体 · 本 PRJ は CF 代替経路あり · [検証](IAC.md#terraform-vs-cloudformation-検証)
- AWS CDK · Pulumi（当面）
- 手動コンソールのみ運用（本番 S3/IAM）

**理由:**

- S3 + IAM + batch compute の provider・事例が豊富
- plan/apply で infra diff を PR レビュー可能
- consumer 増加時にモジュール変数でプレフィックス分離しやすい
- **Cloudflare（R2 / Containers）を同一 IaC で扱える** — CFN は非対応

**段階投入:**

1. Phase 0.5 — S3 バケット + IAM + KMS/Secrets（prep batch 最小権限 · 外部 API key 基盤）
2. Phase 3+ ops — EC2 launch template または ECS（定期 ingest 定常化後）
3. Phase 3+（任意）— API Gateway（HTTP で prep トリガーする要件が出たら）
4. Phase 3+ — **LINE Webhook**（既存 line-notification 基盤 · prep SUCCESS/WARNING/FAILED）
5. Phase 3+（任意）— SES · API Gateway

**通知方針:** 運用アラートは **LINE 第一**（サーバ監視と同型メッセージ）· SES はメール必須時のみ — [IAC.md §5](../../docs/IAC.md#line-webhook--運用通知phase-3--第一候補)

**棄却の補足:** CloudFormation — [IAC.md §7](../../docs/IAC.md#7-terraform-vs-cloudformation-検証) · KMS/LINE/SES — [IAC.md §5](../../docs/IAC.md#5-aws-サービス選定--kms--通知--api-gateway--cloudformation)

**実装:** planned — [docs/IAC.md](../../docs/IAC.md) · [infra/terraform/README.md](../../infra/terraform/README.md)

**影響:** `infra/terraform/` · ROADMAP-AND-COSTS · IMPLEMENTATION-COMPARISON · Phase 0.5 TODO

---

## D-004 {#d-004}

**日付:** 2026-06-29

**Problem:** P-009（techdev-cursor ↔ term-prep-platform の sibling 追従・双方向 handoff により、runtime / docs / CI の連鎖破綻が発生しうる）

**採択:** O-P009-001 — **Artifact boundary**（pip package + Semver 契約）を採用。consumer は sibling path ではなく version pin で接続。

**棄却:**

- O-P009-002 — Remote MCP / 常時サービス化（SPOF と運用負債が先行）
- O-P009-003 — 完全独立（consumer 内製または vendoring、重複実装ドリフト増大）

**理由:**

- sibling パス依存（`../term-prep-platform`）を廃し、再現性を version pin に移せる
- Phase 0.5 の実装資産（extractor / sync / schema）を捨てずに脱耦できる
- multi-consumer（techdev-cursor / dopagaki）へ拡張しやすい
- Remote service 案よりも初期コストと可用性リスクを抑えられる

**実装:** in progress — `term-prep` package entry points（extract/sync/mcp）と consumer cutover guide。

**影響:** `pyproject.toml`, package entrypoint, `meta/consumer-handoff/` migration guide, `projects/techdev-cursor/` mirror 廃止

---

## D-005 {#d-005}

**日付:** 2026-06-29

**Problem:** P-009-B（将来の enterprise 運用で Remote service / Remote MCP を採択する前に、
I/F 仕様が未固定だと connector 実装コストと consumer 追従コストが増える）

**採択:** O-P009-002 — Contract-first 方式で canonical spec を先に固定する（実装前に Domain/Surface/SPI を定義）。

**棄却:**

- サービス実装先行（仕様は実装後追い）
- transport ごとに独立 payload を許容（HTTP/SSE/MCP/CLI で別契約）

**理由:**

- enterprise では API 契約と変更管理がコードより長寿命
- connector 実装を SPI + conformance test で共通化できる
- consumer 側 CI で互換性を早期検知できる

**実装:** in progress — `meta/contracts/`（domain, version policy, OpenAPI, SSE schema, MCP/CLI/SPI contract）。

**影響:** `meta/contracts/` を Plan B 実装の唯一の契約正本とする。
