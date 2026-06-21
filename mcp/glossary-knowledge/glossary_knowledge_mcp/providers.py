from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .models import ClassifyResult, Label


class Provider(ABC):
    id: str

    @abstractmethod
    def classify(
        self,
        term: str,
        *,
        context: str | None = None,
        domain: str | None = None,
    ) -> ClassifyResult:
        ...


class NullProvider(Provider):
    """Stub provider — always unknown. Real adapters (wikipedia, llm, …) go here later."""

    def __init__(self, provider_id: str = "null") -> None:
        self.id = provider_id

    def classify(
        self,
        term: str,
        *,
        context: str | None = None,
        domain: str | None = None,
    ) -> ClassifyResult:
        _ = context, domain
        return ClassifyResult(
            term=term,
            label="unknown",
            confidence=0.0,
            reason="NullProvider stub — no external API configured",
            provider_id=self.id,
            cached=False,
        )


def load_providers_config(path: Path | None = None) -> dict[str, Any]:
    if path is None:
        path = Path(__file__).resolve().parent.parent / "providers.json"
    if not path.is_file():
        example = path.with_suffix(".json.example")
        if example.is_file():
            path = example
        else:
            return {"default_chain": ["null"], "providers": [{"id": "null", "type": "null"}]}
    return json.loads(path.read_text(encoding="utf-8"))


def build_provider_chain(config: dict[str, Any]) -> list[Provider]:
    by_id: dict[str, Provider] = {}
    for entry in config.get("providers", []):
        provider_id = entry["id"]
        provider_type = entry.get("type", "null")
        if provider_type == "null":
            by_id[provider_id] = NullProvider(provider_id)
        # Future: wikipedia, llm, stats, custom

    chain: list[Provider] = []
    for provider_id in config.get("default_chain", ["null"]):
        if provider_id in by_id:
            chain.append(by_id[provider_id])
    if not chain:
        chain.append(NullProvider())
    return chain


class ProviderRegistry:
    def __init__(self, providers: list[Provider]) -> None:
        self._chain = providers

    @classmethod
    def from_config(cls, config_path: Path | None = None) -> ProviderRegistry:
        return cls(build_provider_chain(load_providers_config(config_path)))

    def list_providers(self) -> list[str]:
        return [p.id for p in self._chain]

    def classify(
        self,
        term: str,
        *,
        context: str | None = None,
        domain: str | None = None,
        provider_id: str | None = None,
    ) -> ClassifyResult:
        if provider_id:
            for provider in self._chain:
                if provider.id == provider_id:
                    return provider.classify(term, context=context, domain=domain)
            return NullProvider(provider_id).classify(term, context=context, domain=domain)

        for provider in self._chain:
            result = provider.classify(term, context=context, domain=domain)
            if result.label != "unknown":
                return result
        return self._chain[-1].classify(term, context=context, domain=domain)
