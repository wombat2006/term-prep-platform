from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from .providers import ProviderRegistry

_config_path = os.environ.get("GLOSSARY_KNOWLEDGE_CONFIG")
_registry = ProviderRegistry.from_config(
    Path(_config_path) if _config_path else None
)

mcp = FastMCP("glossary-knowledge", json_response=True)


@mcp.tool()
def classify_term(
    term: str,
    context: str | None = None,
    domain: str | None = None,
    provider: str | None = None,
) -> dict[str, Any]:
    """Classify a single term as general, domain, or unknown (stub: always unknown)."""
    result = _registry.classify(
        term.strip(),
        context=context,
        domain=domain,
        provider_id=provider,
    )
    return result.to_dict()


@mcp.tool()
def classify_batch(
    terms: list[str],
    context: str | None = None,
    domain: str | None = None,
    provider: str | None = None,
) -> dict[str, Any]:
    """Classify multiple terms. Returns { results: [...] }."""
    results = [
        _registry.classify(
            t.strip(),
            context=context,
            domain=domain,
            provider_id=provider,
        ).to_dict()
        for t in terms
        if t.strip()
    ]
    return {"results": results, "count": len(results)}


@mcp.tool()
def list_providers() -> dict[str, Any]:
    """List configured provider IDs in chain order."""
    return {"providers": _registry.list_providers()}


@mcp.tool()
def get_cache_stats() -> dict[str, Any]:
    """Cache statistics (stub — cache not implemented yet)."""
    return {"enabled": False, "hits": 0, "misses": 0, "note": "SQLite cache — Phase 2.5 T2.5-3"}
