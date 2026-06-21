# RL-20260621: Knowledge Filter — API 比較と MCP 実装方針

Status:
Closed（2026-06-21）— stub 作成まで。再開条件: Phase 2.5 着手時

Closed:
2026-06-21

Related:
[P-002](../meta/glossary-pipeline/PROBLEMS.md#p-002)
[O-P002-004](../meta/glossary-pipeline/options/O-P002-004-external-knowledge-filter.md)
[TO-BE-PLATFORM](../meta/TO-BE-PLATFORM.md)
[D-002](../meta/glossary-pipeline/DECISIONS.md#d-002)
[mcp/glossary-knowledge/](../mcp/glossary-knowledge/README.md)

Repository:
https://github.com/wombat2006/term-prep-platform

Opened:
2026-06-21

---

## 要約

形態素解析後の **ノイズ除去フィルタ** を、パイプライン本体から分離し **MCP サーバ** として実装する。MCP は **任意のバックエンド API**（LLM / 百科 / クラウド NLP / 自前辞典）へ接続する **adapter 層** を担う。具体的な API 選定は本 Research Log の比較表を参照し、別途 DECISIONS で確定する。

**採択:** Research Log B（API 候補比較）+ **実装形態として MCP**

**未決:** 第一プロバイダ、MCP 配置 repo、認証・キャッシュの正典

---

## 背景

| 現象 | 観測 |
|---|---|
| 開世界名詞抽出 | Accepted 原稿 7 章 → 693 候補、reject 93% |
| 形態素解析の限界 | POS まで。一般語 vs 専門語 vs 再定義語は区別不可 |
| stop リスト | 手メンテ限界。corpus 拡大で破綻見込み |

registry seed-first（O-P002-001）が土台。**その後段** に語彙知識フィルタが要る（O-P002-004）。

---

## 実装形態の素案比較

| 案 | 概要 | 棄却 / 採択 |
|---|---|---|
| **A** | `scripts/glossary/` 内に Python `KnowledgeFilter` プロトコル + provider 直結 | **棄却（単体）** |
| **B** | 外部 HTTP マイクロサービス（REST）を glossary CLI が呼ぶ | **棄却** |
| **C** | **MCP サーバ** — glossary / Cursor / 他 PRJ が MCP 経由で `classify_term` | **採択** |

### 案A を主形態にしない理由

- provider 追加のたび **glossary Core に依存が増える**
- LLM / 百科 / 自前辞典で **認証・レート制限・プロンプト** がバラバラ
- Cursor エージェントが **同じ判定を対話中に再利用** できない

### 案B を棄却した理由

- REST サービスはデプロイ・バージョン管理が別 Epic
- MCP は Cursor / CLI / CI から **同一ツール契約** で呼べる
- 専門用語辞典 PRJ へ **MCP として export** しやすい

### 案C（MCP）を採択した理由

- **関心分離:** fugashi / registry / filter ルールは repo 内、語彙知識は MCP 外
- **プロバイダ差し替え:** MCP 内部の adapter のみ変更。glossary CLI は MCP クライアント固定
- **任意 API 接続:** adapter 層で OpenAI / Wikidata / 自前 API を config 指定
- **Traceability:** MCP tool 呼び出し + 応答を build/ にログ可能（C-0003）
- **エージェント連携:** 用語採択レビュー時、Cursor が同一 MCP で再判定可能

---

## API プロバイダ候補 — 比較表

判定問い: **「この surface 形は、指定ドメイン文脈で Glossary 候補として残す価値があるか？」**

出力ラベル（全 provider 共通）:

| ラベル | 意味 | パイプライン扱い |
|---|---|---|
| `canonical` | registry 命中（MCP 前段） | adopt 候補 |
| `domain` | 専門語・ドメイン語 | hold / adopt 候補 |
| `general` | 一般語 | reject |
| `unknown` | 判定不能・新語 | **hold**（誤 reject 防止） |

### 一覧

| ID | 種別 | 代表例 | 入力 | 判定の強み | 弱み | コスト | 決定論 | 日本語 | オフライン | 第一候補 |
|---|---|---|---|---|---|---|---|---|---|---|
| **K-001** | LLM チャット | OpenAI, Anthropic, Gemini | term + context + domain hint | 再定義語、neologism、文脈付き | 非決定論、プロンプト設計、規約 | 中〜高 | 低 | ◎ | ✗ | △ |
| **K-002** | ローカル LLM | Ollama, llama.cpp | 同上 | データ不出域、コスト固定 | GPU、品質ばらつき | 低（固定） | 低 | ○ | ◎ | △ |
| **K-003** | 百科 API | Wikidata, Wikipedia REST | term | 「世間一般に既知か」 | 専門再定義語は general 寄り | 無〜低 | 高 | ○ | △（cache） | ○ |
| **K-004** | 国語辞書 | 三省堂・goo 等（要契約） | term | 一般語判定が明確 | 契約、API 不安定、ドメイン不可 | 要調査 | 高 | ◎ | △ | △ |
| **K-005** | クラウド NLP | Google NL, AWS Comprehend, Azure Text | term or sentence | 固有名詞・組織 | ドメイン再定義語に弱い | 中 | 高 | ○ | ✗ | △ |
| **K-006** | 統計コーパス | BCCWJ / 内蔵一般語頻度表 | term | 決定的、オフライン可 | コーパス構築、ドメイン不可 | 低 | ◎ | ◎ | ◎ | ○ |
| **K-007** | 自前辞典 API | 専門用語辞典 PRJ 将来 MCP | term_id or surface | 閉世界と一致、最正確 | **未構築** | — | ◎ | ◎ | ◎ | **長期** |
| **K-008** | ハイブリッド | K-003 + K-001 fallback | term + context | コスト抑制 + 境界ケース | 実装複雑 | 低〜中 | 中 | ◎ | △ | **推奨（中期）** |

### プロバイダ別メモ

**K-001 LLM**

- プロンプト例: 「ドメイン={domain}。用語={term}。周辺文={context}。general/domain/unknown と理由を JSON で」
- C-0003: `build/glossary/knowledge-log.jsonl` に prompt hash + response を保存
- 第一 provider にする場合: **K-002 ローカル** または **K-008** を推奨（出域・コスト）

**K-003 百科**

- 手順: ja Wikipedia 記事有無 → Wikidata label/descriptions → `general` if 一般概念記事
- 「注意」「探索」は記事あり → **general 誤判定**。registry 優先必須
- 無料・レート制限あり → MCP 内 cache 必須

**K-006 統計**

- O-P002-003（TF-IDF）と近いが **MCP adapter として提供** すれば glossary から同一 IF で呼べる
- オフライン CI 用 **NullProvider / StatsProvider** として有用

**K-007 自前**

- 専門用語辞典 PRJ の MCP が **provider registry** に載る想定
- dopagaki の `glossary-registry.json` を seed として K-007 に問い合わせる流れ

**K-008 ハイブリッド（推奨構成案）**

```text
1. registry 命中 → canonical（MCP を呼ばない）
2. K-006 or K-003 → general なら reject
3. general 以外 / unknown → K-001 or K-002 で domain 確認（オプション）
4. それでも unknown → hold
```

---

## MCP アーキテクチャ（採択方向）

### 配置

| 候補 | メリット | デメリット |
|---|---|---|
| **本 repo `mcp/glossary-knowledge/`** | dopagaki と同 lifecycle | 他 PRJ 移植時 copy |
| **専門用語辞典 PRJ 独立 repo** | 辞典 + filter 一体 | dopagaki 単体で完結しない |
| **portable bundle `meta/glossary-pipeline/mcp/`** | glossary-pipeline と同梱 | 実装は stub から |

**当面:** portable bundle に **仕様 + stub**、実装は `mcp/glossary-knowledge/`（本 repo）で PoC。

### コンポーネント

```text
┌─────────────────────────────────────────────────────────┐
│  glossary_extractor.py  /  Cursor Agent               │
│         │ MCP client (stdio or HTTP)                    │
└─────────┼───────────────────────────────────────────────┘
          ▼
┌─────────────────────────────────────────────────────────┐
│  MCP Server: glossary-knowledge                         │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │ tools       │  │ cache layer  │  │ provider        │ │
│  │ classify_*  │→ │ SQLite/JSONL │→ │ registry        │ │
│  │ batch_*     │  │              │  │ (config-driven) │ │
│  └─────────────┘  └──────────────┘  └────────┬────────┘ │
└────────────────────────────────────────────────┼────────┘
                                                 ▼
                    ┌────────────────────────────────────────┐
                    │ Adapters (任意 API)                    │
                    │  wikipedia │ llm │ stats │ custom │ …  │
                    └────────────────────────────────────────┘
```

### MCP Tools（案）

| Tool | 入力 | 出力 |
|---|---|---|
| `classify_term` | `term`, `context?`, `domain?`, `provider?` | `{ label, confidence, reason, provider_id, cached }` |
| `classify_batch` | `terms[]`, 同上 | `{ results[] }` |
| `list_providers` | — | 有効 adapter 一覧 |
| `get_cache_stats` | — | ヒット率（デバッグ） |

### Provider 設定（案）

```json
{
  "providers": [
    { "id": "wikipedia-ja", "type": "wikipedia", "lang": "ja", "priority": 10 },
    { "id": "ollama-local", "type": "llm", "base_url": "http://127.0.0.1:11434", "model": "...", "priority": 20 },
    { "id": "null", "type": "null", "priority": 999 }
  ],
  "default_chain": ["wikipedia-ja", "ollama-local"],
  "cache": "build/glossary/knowledge-cache.sqlite",
  "fail_mode": "unknown"
}
```

`fail_mode`: API 失敗時は `unknown`（hold）— **fail-open**。誤 reject を避ける。

### glossary パイプライン統合

```text
extract → registry match → rule filter
    ↓
[MCP classify_batch]  … enabled 時のみ。未起動時はスキップ（Phase 2 後）
    ↓
rank → writers
```

CLI config:

```json
"knowledge_filter": {
  "enabled": false,
  "mcp_server": "mcp/glossary-knowledge",
  "transport": "stdio",
  "domain": "attention-economics",
  "batch_size": 50
}
```

---

## 棄却した API 単独戦略

| 戦略 | 棄却理由 |
|---|---|
| LLM のみ | コスト・非決定論。百科/統計で general を先に落とすべき |
| 百科のみ | 再定義語・新語で false general |
| API 選定前に Core に直結実装 | provider 差し替えコスト。MCP で固定 IF を先に |

---

## 決定

| 項目 | 内容 |
|---|---|
| Research Log | 本ファイル（API 比較 + MCP 方針） |
| 実装形態 | **MCP サーバ** + provider adapter  registry |
| 必須併用 | O-P002-001 registry seed-first |
| 第一プロバイダ | **未選定** — K-008（ハイブリッド）を中期推奨として記録 |
| Phase | TO-BE **Phase 2.5**（registry 後、rank 前）。Phase 0–1 完了後 |

---

## Close サマリ（2026-06-21）

| 項目 | 結果 |
|---|---|
| 方針 | MCP + provider adapter registry（D-002 採択） |
| 成果物 | [mcp/glossary-knowledge/](../mcp/glossary-knowledge/) — NullProvider stub、4 tools |
| 未実装（defer） | cache、第一 provider、glossary CLI 連携 |
| 再開条件 | Phase 0–1 完了後、Phase 2.5 着手時 |
| 先行作業 | Phase 0 出力分割 — **done** (2026-06-21); registry seed-first — pending |

**棄却せず保留:** K-003 / K-006 / K-008 の第一プロバイダ選定 — 別 RL または D-003 で再開。

---

## 次のアクション

| # | アクション | 状態 |
|---|---|---|
| 1 | D-002 採択ログ | done |
| 2 | O-P002-004 MCP 方針 | done |
| 3 | `mcp/glossary-knowledge/` stub | **done** |
| 4 | 第一 provider 選定 | **deferred** |
| 5 | `glossary-config.json` knowledge_filter 節 | deferred（Phase 2.5） |
| 6 | Phase 0（出力分割） | **done** (dopagaki + techdev-cursor consumers) |

---

## Open Questions（close 時点 — 再開時に扱う）

1. MCP transport — stdio vs HTTP（CI batch）
2. 認証 — API key を MCP server env のみ
3. キャッシュ正典 — build/ vs corpus hash artifact
4. 専門用語辞典 PRJ — 同一 MCP repo vs fork
5. 第一プロバイダ — K-003 / K-006 / K-008
