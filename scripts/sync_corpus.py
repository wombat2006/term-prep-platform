#!/usr/bin/env python3
"""
sync_corpus.py — Sync external corpus into local mirror before glossary prep.

Phase 0.5: Google Drive via connectors/googledrive (mirror mode).

Usage:
    python scripts/sync_corpus.py --config meta/glossary-config.json
    python scripts/sync_corpus.py --config projects/techdev-cursor/glossary-config.json

Requires glossary-config `source` section with enabled=true.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.connectors.googledrive import sync_googledrive_mirror  # noqa: E402
from scripts.glossary_extractor import (  # noqa: E402
    load_config,
    project_root_from_config,
    validate_config,
)


def sync_from_config(config_path: Path) -> dict:
    config = load_config(config_path)
    source = config.get("source") or {}
    if not source.get("enabled"):
        raise ValueError("source.enabled is false — nothing to sync")

    adapter = source.get("adapter")
    project_root = project_root_from_config(config_path, config)

    if adapter == "googledrive":
        result = sync_googledrive_mirror(project_root, source)
    else:
        raise ValueError(f"Unsupported source.adapter: {adapter!r}")

    return {
        "adapter": result.adapter,
        "local_mirror": str(result.local_mirror),
        "mirrored_count": result.mirrored_count,
        "failed_count": result.failed_count,
        "manifest": str(result.manifest_path) if result.manifest_path else None,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to glossary-config.json",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate config and connector build only (no sync)",
    )
    args = parser.parse_args(argv)

    config_path = args.config.resolve()
    if not config_path.is_file():
        print(f"error: config not found: {config_path}", file=sys.stderr)
        return 1

    try:
        with config_path.open(encoding="utf-8") as fh:
            config = json.load(fh)
        validate_config(config)
    except Exception as exc:
        print(f"error: invalid config: {exc}", file=sys.stderr)
        return 1

    if args.check:
        source = config.get("source") or {}
        if not source.get("enabled"):
            print("ok: source disabled (check only)")
            return 0
        if source.get("adapter") == "googledrive":
            cli = _REPO_ROOT / "connectors" / "googledrive" / "dist" / "cli.js"
            if not cli.is_file():
                print(f"error: build connector first: {cli}", file=sys.stderr)
                return 1
        print("ok: config and connector ready")
        return 0

    try:
        payload = sync_from_config(config_path)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if payload.get("failed_count", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
