# O-P009-001 — Artifact boundary / Semver contract

Status:
accepted (D-004, 2026-06-29)

Problem:
P-009（repo 間の sibling 追従・cross-repo handoff による連鎖破綻リスク）

---

## 要旨

term-prep-platform を **配布 artifact（pip package）** として扱い、consumer は
filesystem sibling (`../term-prep-platform`) ではなく **version pin** で利用する。

契約の正本:

- `glossary-config.schema.json`（package 同梱）
- CLI entry points（`term-prep-extract`, `term-prep-sync`）
- MCP entry point（`term-prep-glossary-knowledge-mcp`）

---

## 採択理由

1. runtime coupling（sibling path, local venv）を除去できる
2. docs/bot handoff ドリフトを release note 中心に置き換えられる
3. 既存の Phase 0.5 資産（extract/sync/connectors）を活かせる
4. Remote service 案より低コストで導入可能

---

## 非採択案

### O-P009-002 — Remote service / streamable-http

- 長所: repo 完全分離
- 棄却理由: SPOF, infra 運用負債, 初期コスト

### O-P009-003 — 完全独立（consumer 内製 or vendoring）

- 長所: 組織境界の明確化
- 棄却理由: 重複実装 / ドリフト / Phase 0.5 投資の棄損

---

## 移行ステップ（概要）

1. package entrypoint 提供（extract/sync/mcp）
2. consumer cutover guide を package 前提へ更新
3. sibling 前提 assets（mirror config / cross_repo scripts）を撤去
4. contract CI（schema + semver）を導入
