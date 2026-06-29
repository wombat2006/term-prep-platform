# O-P009-002 — Contract-first canon for Plan B service

Status:
accepted (D-005, 2026-06-29)

Problem:
P-009-B（Remote service 実装時に interface 契約が先にないと、connector 実装と consumer 追従のコストが増える）

---

## 要旨

Plan B（Remote MCP / HTTP service）実装前に、契約正本を固定する。

Canonical files:

- `meta/contracts/domain-model.md`
- `meta/contracts/versioning-policy.md`
- `meta/contracts/http/openapi.yaml`
- `meta/contracts/sse/event-envelope.schema.json`
- `meta/contracts/mcp-tool-contract.md`
- `meta/contracts/cli-contract.md`
- `meta/contracts/connector-spi.md`

---

## 採択理由

1. transport 別 payload drift（HTTP/SSE/MCP/CLI）を防ぐ
2. Semver による互換性管理を実装前から適用できる
3. connector 実装コストを SPI + conformance tests で圧縮できる
4. enterprise の監査・障害対応で必要な traceable error model を統一できる

---

## 非採択案

### 実装先行（仕様は後追い）

- 長所: 着手が速い
- 棄却理由: 後で non-compatible fix が発生しやすい

### surface ごとの独立仕様

- 長所: 実装の自由度が高い
- 棄却理由: consumer ごとに adapter が増殖し運用負債化する

---

## 完了条件（B0）

1. Domain / Error / Version policy の文書化
2. HTTP OpenAPI draft、SSE schema、MCP/CLI contract の配置
3. Connector SPI と conformance 要件の文書化
4. consumer-handoff から参照可能であること
