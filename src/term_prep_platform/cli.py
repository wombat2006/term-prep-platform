from __future__ import annotations

import argparse
import importlib.metadata
import json
from pathlib import Path

from scripts.glossary_extractor import load_config, validate_config


def extract() -> int:
    from scripts.glossary_extractor import main as extractor_main

    raise SystemExit(extractor_main())


def sync() -> int:
    from scripts.sync_corpus import main as sync_main

    raise SystemExit(sync_main())


def glossary_knowledge_mcp() -> int:
    from glossary_knowledge_mcp.__main__ import main as mcp_main

    mcp_main()
    return 0


def contract_check(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate glossary config contract against installed term-prep-platform version."
    )
    parser.add_argument("--config", type=Path, required=True, help="Path to glossary-config.json")
    parser.add_argument(
        "--expect-major",
        type=int,
        default=1,
        help="Expected major version for term-prep-platform contract",
    )
    args = parser.parse_args(argv)

    if not args.config.is_file():
        print(f"error: config not found: {args.config}")
        return 1

    with args.config.open(encoding="utf-8") as fh:
        config = json.load(fh)

    try:
        validate_config(config)
    except Exception as exc:
        print(f"error: schema validation failed: {exc}")
        return 1

    version = importlib.metadata.version("term-prep-platform")
    major = int(version.split(".")[0])
    if major != args.expect_major:
        print(
            "error: major version mismatch: "
            f"installed={version} expected_major={args.expect_major}"
        )
        return 1

    print(
        "ok: contract check passed "
        f"(term-prep-platform {version}, expected major {args.expect_major})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(contract_check())
