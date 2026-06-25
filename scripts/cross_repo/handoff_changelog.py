#!/usr/bin/env python3
"""Parse latest entry from meta/consumer-handoff/CHANGELOG.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
CHANGELOG = _REPO / "meta" / "consumer-handoff" / "CHANGELOG.md"
HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — (.+)$")


def latest_entry(text: str) -> tuple[str, str, str]:
    lines = text.splitlines()
    start = None
    date = ""
    title = ""
    for i, line in enumerate(lines):
        match = HEADING.match(line)
        if match:
            start = i
            date, title = match.group(1), match.group(2)
            break
    if start is None:
        raise SystemExit("no changelog entries found")

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if HEADING.match(lines[j]):
            end = j
            break

    body = "\n".join(lines[start + 1 : end]).strip()
    entry_id = f"{date} — {title}"
    return entry_id, title, body


def main() -> int:
    if not CHANGELOG.is_file():
        print(f"error: missing {CHANGELOG}", file=sys.stderr)
        return 1

    text = CHANGELOG.read_text(encoding="utf-8")
    entry_id, title, body = latest_entry(text)
    mode = sys.argv[1] if len(sys.argv) > 1 else "id"

    if mode == "id":
        print(entry_id)
    elif mode == "title":
        print(title)
    elif mode == "summary":
        print(entry_id)
        if body:
            print()
            print(body.splitlines()[0] if body else "")
    elif mode == "body":
        print(f"## {entry_id}")
        print()
        print(body)
    else:
        print(f"usage: {sys.argv[0]} [id|title|summary|body]", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
