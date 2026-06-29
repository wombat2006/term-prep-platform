# CLI Surface Contract

Status:
Draft v1 (2026-06-29)

---

## Stable commands

| Command | Role |
|---|---|
| `term-prep-extract` | extraction/check execution |
| `term-prep-sync` | connector sync/check execution |
| `term-prep-glossary-knowledge-mcp` | MCP stdio server entrypoint |
| `term-prep-contract-check` | config + package major compatibility gate |

---

## Required flags

| Command | Required flags | Optional flags |
|---|---|---|
| `term-prep-extract` | `--config <path>` | `--check` |
| `term-prep-sync` | `--config <path>` | `--check` |
| `term-prep-contract-check` | `--config <path>` | `--expect-major <n>` |

Command names and required flags are major-version locked.

---

## Exit code contract

- `0`: success
- `1`: contract/config/validation failure
- `2`: dependency or runtime precondition failure (for extractor/sync)

All tools should emit concise machine-parsable error prefixes:

- `error:`
- `ok:`

---

## Output contract

Human-readable output remains default, but fields in `error:` lines must keep stable
keywords for CI parsing:

- `schema validation failed`
- `major version mismatch`
- `config not found`

---

## Forward compatibility

New subcommands/flags may be added if:

1. Existing command behavior is unchanged
2. Existing required arguments remain valid
3. Consumer docs and changelog are updated in same release
