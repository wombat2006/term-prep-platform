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

（予約 — Phase 0 採択時に記入）

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
