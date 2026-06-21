# term-prep-platform

> **社内データを RAG に載せる前の前処理 — 用語抽出・ノイズ除去・PII/サニタイズを MCP で共通化**

**English:** MCP-based data prep for RAG — terminology extraction, noise filtering, and document cleanup, shared across repos.

Repository:
https://github.com/wombat2006/term-prep-platform

Status:
Initial extract from [dopagaki-transition](https://github.com/wombat2006/dopagaki-transition) (2026-06-21)

---

## 何をする repo か

| 層 | 本 repo | 各 consumer PRJ |
|---|---|---|
| MCP servers（Python, stdio） | ✅ | `.cursor/mcp.json` で参照 |
| 抽出 CLI・governance テンプレ | ✅ | — |
| corpus・正典・GLOSSARY | — | ✅ |

**第 1 consumer:** [techdev-cursor](https://github.com/wombat2006/techdev-cursor) — Google Drive → RAG 前処理  
**参考 consumer:** [dopagaki-transition](https://github.com/wombat2006/dopagaki-transition) — 研究原稿用語集

---

## クイックスタート

```bash
git clone https://github.com/wombat2006/term-prep-platform.git
cd term-prep-platform
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -r mcp/glossary-knowledge/requirements.txt

# 形態素バックエンド確認
python scripts/glossary_extractor.py --check --config projects/dopagaki-transition/glossary-config.json

# MCP provider stub（pip 不要の部分）
cd mcp/glossary-knowledge && PYTHONPATH=. python -c "
from glossary_knowledge_mcp.providers import ProviderRegistry
print(ProviderRegistry.from_config().classify('探索').to_dict())
"
```

**System:** MeCab (`libmecab`) — AlmaLinux: `sudo dnf install mecab mecab-devel`

---

## ディレクトリ

```text
term-prep-platform/
  mcp/                    … MCP servers（1 tool = 1 package）
  scripts/                … glossary_extractor.py
  meta/glossary-pipeline/ … 問題・手段案・採択（portable）
  meta/TO-BE-PLATFORM.md  … ロードマップ
  projects/               … consumer 別 config サンプル
  docs/                   … アーキテクチャ・連携
```

---

## MCP（現状）

| Server | Status | Tools |
|---|---|---|
| [glossary-knowledge](mcp/glossary-knowledge/) | **stub** (NullProvider) | `classify_term`, `classify_batch`, … |
| term-extract | planned | — |
| pii-guard | planned | — |
| sanitize | planned | — |

---

## Consumer 設定

| PRJ | Config |
|---|---|
| dopagaki-transition | [projects/dopagaki-transition/](projects/dopagaki-transition/) |
| techdev-cursor | [projects/techdev-cursor/](projects/techdev-cursor/) |

詳細: [docs/integrations/](docs/integrations/)

---

## 関連

- [meta/glossary-pipeline/README.md](meta/glossary-pipeline/README.md) — 移植・ governance
- [research-log/RL-20260621-knowledge-filter-mcp.md](research-log/RL-20260621-knowledge-filter-mcp.md) — MCP 方針（closed）
- Origin: dopagaki-transition @ `5306a8b`

---

## Topics

`mcp` · `rag` · `terminology` · `glossary` · `data-prep` · `python` · `cursor`
