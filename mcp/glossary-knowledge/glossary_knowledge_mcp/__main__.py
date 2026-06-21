from __future__ import annotations

import sys


def main() -> None:
    try:
        from .server import mcp
    except ImportError as exc:
        print(
            "glossary-knowledge-mcp requires Python >= 3.10 and: pip install mcp",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
