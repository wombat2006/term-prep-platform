from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

Label = Literal["canonical", "domain", "general", "unknown"]


@dataclass(frozen=True)
class ClassifyResult:
    term: str
    label: Label
    confidence: float
    reason: str
    provider_id: str
    cached: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
