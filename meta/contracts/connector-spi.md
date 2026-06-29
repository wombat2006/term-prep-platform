# Connector SPI Contract

Status:
Draft v1 (2026-06-29)

---

## Goal

Standardize connector behavior so new integrations (Drive, S3, future APIs) can be
implemented quickly without rewriting orchestration logic.

---

## SPI lifecycle

1. `validate_config` (no network side effects)
2. `check_readiness` (credentials and minimal access checks)
3. `list_items` (discover remote items)
4. `sync_items` (mirror to local root, idempotent)
5. `emit_summary` (files changed, skipped, failed)

---

## Required capabilities metadata

Each connector declares:

- `connector_id` (stable identifier)
- `supported_modes` (`check`, `mirror`, future `vector`)
- `auth_type` (`oauth`, `api_key`, `iam_role`, `none`)
- `supports_incremental_sync` (boolean)

---

## Behavioral requirements

- **Idempotency:** running mirror twice without upstream changes should produce no diffs
- **Deterministic local paths:** same remote item maps to same local path
- **Error normalization:** connector-native errors map to `CONNECTOR_*` or `AUTH_*`
- **Partial failure reporting:** failed items must be listed explicitly

---

## Cost-reduction scaffold (B0 requirement)

New connector template should include:

1. config schema fragment
2. readiness check implementation
3. sync loop with normalized event emission
4. conformance tests with golden summaries
5. docs snippet for `meta/consumer-handoff/02-schema-and-cli.md`

---

## Conformance test matrix

Minimum tests for each connector:

1. no-credential check mode failure shape (`AUTH_*`)
2. invalid config failure shape (`CONFIG_*`)
3. deterministic local path mapping
4. idempotent mirror behavior
5. summary counters consistency (`total = synced + skipped + failed`)

Conformance tests must pass before connector is considered contract-compliant.

---

## Python ABC stub (copy-paste template)

New connectors must subclass `SourceConnector`. Copy the stub below into
`scripts/connectors/<connector_id>.py` and implement all abstract methods.

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator


@dataclass
class ConnectorMeta:
    connector_id: str
    supported_modes: list[str]          # subset of ["check", "mirror"]
    auth_type: str                      # "oauth" | "api_key" | "iam_role" | "none"
    supports_incremental_sync: bool


@dataclass
class SyncSummary:
    total: int
    synced: int
    skipped: int
    failed: int
    failed_items: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        assert self.total == self.synced + self.skipped + self.failed, (
            "SyncSummary: total must equal synced + skipped + failed"
        )


class ConnectorError(Exception):
    """Base for all connector errors.

    code must be a string from the families:
        AUTH_*       missing/invalid credentials
        CONFIG_*     invalid config field or missing required value
        CONNECTOR_*  upstream API or network failure
    """

    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


class SourceConnector(ABC):
    """Contract: one subclass per connector_id.

    Lifecycle (called in order by the orchestrator):
        validate_config → check_readiness → list_items → sync_items → emit_summary
    """

    @abstractmethod
    def meta(self) -> ConnectorMeta:
        """Return static metadata about this connector."""
        ...

    @abstractmethod
    def validate_config(self, config: dict) -> None:
        """Validate connector-specific config section.

        Must not make any network calls.
        Raise ConnectorError with code CONFIG_* on failure.
        """
        ...

    @abstractmethod
    def check_readiness(self) -> None:
        """Verify credentials and minimal access (e.g. list root folder).

        Raise ConnectorError with code AUTH_* if credentials are missing or invalid.
        Raise ConnectorError with code CONNECTOR_* on upstream errors.
        """
        ...

    @abstractmethod
    def list_items(self) -> Iterator[str]:
        """Yield stable remote item IDs in deterministic order.

        The same remote item must always yield the same ID across runs.
        """
        ...

    @abstractmethod
    def sync_items(self, local_root: Path) -> SyncSummary:
        """Mirror remote items to local_root.

        Must be idempotent: running twice without upstream changes produces
        no diffs (skipped == total on second run).
        Local paths must be deterministic: same item_id always maps to the
        same relative path under local_root.
        Partial failures are allowed; list failed items in SyncSummary.
        """
        ...
```

### Error mapping example

```python
# Translate connector-native exceptions to ConnectorError
try:
    client.list_files(folder_id)
except PermissionDeniedError as exc:
    raise ConnectorError("AUTH_INSUFFICIENT_SCOPE", str(exc)) from exc
except NetworkTimeoutError as exc:
    raise ConnectorError("CONNECTOR_TIMEOUT", str(exc), retryable=True) from exc
```
