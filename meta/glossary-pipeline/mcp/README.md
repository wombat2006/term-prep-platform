# Glossary Knowledge Filter — MCP（portable 仕様）

Status:
Specification — implementation at [mcp/glossary-knowledge/](../../../mcp/glossary-knowledge/)

Related:
[O-P002-004](../options/O-P002-004-external-knowledge-filter.md)
[RL-20260621-knowledge-filter-mcp](../../research-log/RL-20260621-knowledge-filter-mcp.md)

---

## 目的

用語候補の **一般語 / 専門語 / 未知** 判定を MCP ツールとして提供する。バックエンド API は MCP 内部の **provider adapter** で任意に差し替える。

## クライアント

- `scripts/glossary_extractor.py`（batch classify）
- Cursor Agent（レビュー時の再判定）
- 専門用語辞典 PRJ（同一 MCP を import）

## Tools

| Name | Description |
|---|---|
| `classify_term` | 単語 +  optional context/domain → label |
| `classify_batch` | 複数 term を一括 |
| `list_providers` | 有効 adapter 一覧 |
| `get_cache_stats` | キャッシュ統計 |

## Labels

`canonical` | `domain` | `general` | `unknown`

（`canonical` は通常 MCP 前段の registry で処理。MCP は主に general/domain/unknown）

## Provider types

| type | 例 |
|---|---|
| `null` | 常に unknown（オフライン / 無効） |
| `wikipedia` | ja/en 百科 |
| `llm` | OpenAI-compatible / Ollama |
| `stats` | 内蔵一般語頻度表 |
| `custom` | 自前辞典 HTTP |

## Config

`providers.json` — priority 順 chain。詳細は Research Log § Provider 設定。

## 移植

本ディレクトリは **契約のみ**。他 PRJ では README + options/O-P002-004 をコピーし、実装 repo パスは各自の `mcp/` に置く。
