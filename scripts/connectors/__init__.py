"""Source connector contracts for corpus mirror sync (Phase 0.5)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class SyncResult:
    adapter: str
    local_mirror: Path
    mirrored_count: int
    failed_count: int
    manifest_path: Path | None = None


class SourceConnector(Protocol):
    """Thin mirror contract: external storage → local paths for glossary_extractor."""

    adapter: str

    def sync_to_local(self, project_root: Path, source_config: dict) -> SyncResult:
        """Fetch remote corpus into local_mirror under project_root."""
