# O-P002-004: 外部 Knowledge Filter — MCP + 任意 API

Status:
closed — stub shipped; resume Phase 2.5

Problem:
[P-002](../PROBLEMS.md#p-002) — 開世界抽出によるノイズ

Research Log:
[RL-20260621-knowledge-filter-mcp](../../research-log/RL-20260621-knowledge-filter-mcp.md)

Decision:
[D-002](../DECISIONS.md#d-002)

---

## 概要

形態素解析 **の後**、**MCP サーバ** 経由で「一般語か / ドメイン専門語か」を判定する。MCP 内部に **provider adapter registry** を持ち、LLM / 百科 / 統計 / 自前辞典など **任意の API** へ接続する。glossary CLI は MCP クライアントのみ — provider 直結はしない。

---

## 考え方（妥当性）

| 観点 | 評価 |
|---|---|
| 問題との対応 | ✅ 形態素解析は POS まで。一般語 vs 専門語は **語彙知識** の問題 |
| アーキテクチャ | ✅ 「ノイズ除去フィルタを別実装」は TO-BE の `filter.py` / 別立て方針と一致 |
| 単独依存 | ⚠️ API だけでは不十分。**registry seed-first** と併用すべき |
| 他 PRJ 移植 | ✅ インタフェース固定 + 実装差し替えで辞典 PRJ でも再利用可 |

---

## パイプライン上の位置

```text
extract (fugashi)
    ↓
registry match     … 閉世界：TS/ADR/GLOSSARY にあれば即 adopt 候補
    ↓
rule filter        … stop, min_freq, valid_term
    ↓
knowledge filter   … ★ MCP classify_batch（general / domain / unknown）
    ↓
rank → writers
```

**判定ラベル（案）:**

| ラベル | 扱い |
|---|---|
| `canonical` | registry 命中 → そのまま adopt 候補 |
| `domain` | API が専門語と判断 → hold / adopt 候補 |
| `general` | 一般語 → reject（または JSONL のみ） |
| `unknown` | API 不明・新語 → **hold**（ドパガキ等。誤除外を防ぐ） |

---

## API プロバイダ候補

詳細比較表は [RL-20260621](../../research-log/RL-20260621-knowledge-filter-mcp.md#api-プロバイダ候補--比較表)。

| ID | 種別 | 第一候補 |
|---|---|---|
| K-001 | LLM クラウド | △ |
| K-002 | ローカル LLM | △ |
| K-003 | 百科 API | ○ |
| K-006 | 統計コーパス | ○ |
| K-007 | 自前辞典 | 長期 |
| **K-008** | **ハイブリッド** | **中期推奨** |

---

## MCP 実装（採択）

```text
glossary CLI / Cursor
    → MCP (classify_term | classify_batch)
        → cache (SQLite)
        → provider chain (config)
            → wikipedia | llm | stats | custom | null
```

仕様 stub: [mcp/README.md](../mcp/README.md)

PoC 着手条件:** Phase 0–1 完了後。stub は [mcp/glossary-knowledge/](../../mcp/glossary-knowledge/)。

---

## 実装スケッチ（glossary 側 — MCP クライアントのみ）

```python
# scripts/glossary/knowledge_filter.py（将来）

class McpKnowledgeFilter:
    """MCP classify_batch — provider 詳細は MCP server 側"""

    def classify_batch(
        self, terms: list[str], domain: str | None, context: dict[str, str] | None
    ) -> dict[str, Literal["general", "domain", "unknown"]]:
        ...
```

config 例:

```json
"knowledge_filter": {
  "enabled": false,
  "mcp_server": "mcp/glossary-knowledge",
  "transport": "stdio",
  "domain": "attention-economics",
  "batch_size": 50
}
```

Provider 設定は **MCP server 側** `providers.json`。API key は MCP env のみ。

---

## 旧スケッチ（参考 — Core 直結は不採択）

~~`KnowledgeFilter` Protocol + `ConfigurableApiFilter`~~ → MCP adapter に移行。Null は MCP `null` provider。

## メリット

- 形態素解析と **関心分離** — fugashi は変えない
- stop リストの手メンテ削減見込み
- 専門用語辞典 PRJ では **自前 API を provider に** できる
- キャッシュで corpus 再実行時の再現性・コスト削減

## デメリット

- 外部依存（可用性、料金、規約）
- LLM 利用時は **C-0003 Traceability** — 判定理由のログが要る
- 「一般語」≠「GLOSSARY に載せない」— 文脈で再定義される語（注意、探索）を API が general と誤判定しうる → **registry 優先必須**
- オフライン開発は cache または `provider: null` が必要

---

## 適用条件

- 向く PRJ: corpus が大きい、stop リストが破綻している、辞典/RAG 両方
- 向かない PRJ: 小 corpus + registry だけで足りる段階（**今の dopagaki は registry 先行の方が先**）

---

## 他案との関係

- **必須併用:** O-P002-001（seed-first / registry）
- 併用可: O-P002-002（閾値）、O-P002-003（TF-IDF）
- 排他: API のみで registry なし（非推奨）

---

## Open（API 選定時に決める）

1. 判定単位 — 単語 / 複合語 / 文脈付き（chunk 1 段落）
2. ドメイン hint — config に `domain: "neuroeconomics"` を渡すか
3. 正典 — API 応答を Research Log / build/ に残すか
4. 失敗時 — fail-open（全部 hold）vs fail-closed（API 無しは filter スキップ）

---

## 採択時メモ

- **2026-06-21:** 実装形態 MCP 採択（D-002）。API 比較 RL 作成。
- **2026-06-21 close:** [mcp/glossary-knowledge/](../../mcp/glossary-knowledge/) stub 作成。第一 provider・CLI 連携は Phase 2.5 まで defer。
