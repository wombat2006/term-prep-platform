# Consumer PR guide — techdev-cursor (package contract cutover)

**Read as:** Step 4 of [consumer-handoff index](./README.md) · [top entry: ../CONSUMER_HANDOFF.md](../CONSUMER_HANDOFF.md)  
**Purpose:** techdev-cursor が sibling 追従をやめるための PR テンプレート。  
**Rule:** term-prep-platform 側から consumer repo を直接編集しない。

---

## Goal

techdev-cursor が `../term-prep-platform` 依存を廃止し、`term-prep-platform` package の
entrypoint を使って glossary extract / sync / MCP を実行できる状態にする。

---

## Suggested PR title

```text
chore: cut over glossary integration to term-prep package contract
```

---

## Suggested PR body

```markdown
## Summary

- Remove sibling-path dependency on `../term-prep-platform`.
- Pin `term-prep-platform` package version and call package entrypoints.
- Update MCP config to command-based launch (`term-prep-glossary-knowledge-mcp`).
- Add contract CI check for schema + package version.

## Contract

- Package: `term-prep-platform==<PIN>`
- Extract: `term-prep-extract`
- Sync: `term-prep-sync`
- MCP server: `term-prep-glossary-knowledge-mcp`
- Schema source: package release (`meta/schemas/glossary-config.schema.json`)

## Test plan

- [ ] `npm run glossary:extract:check`
- [ ] `npm run glossary:sync:check` (source disabled path)
- [ ] contract CI check (schema + version)
- [ ] Live OAuth smoke is deferred (follow-up)
```

---

## Files to change in techdev-cursor

### 1) package pin

- `requirements` or lock file where Python CLI dependencies are managed
- Pin `term-prep-platform==X.Y.Z`

### 2) npm scripts

Replace sibling script wrappers with direct command wrappers:

```json
"glossary:extract": "term-prep-extract --config meta/glossary-config.json",
"glossary:extract:check": "term-prep-extract --check --config meta/glossary-config.json",
"glossary:sync": "term-prep-sync --config meta/glossary-config.json",
"glossary:sync:check": "term-prep-sync --check --config meta/glossary-config.json"
```

### 3) Cursor MCP config

Switch from sibling Python path to command-based launch:

```json
"glossary-knowledge": {
  "command": "term-prep-glossary-knowledge-mcp"
}
```

### 4) config notes

- Keep `source.enabled: false` until OAuth credentials are ready
- Enable with real `folder_id` and mirror globs only when doing live sync

### 5) CI contract check

Add a CI step that runs:

```bash
term-prep-contract-check --config meta/glossary-config.json --expect-major 1
```

---

## Follow-up PR (OAuth live sync)

1. Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`
2. Set `source.enabled: true` and real `folder_id`
3. Update `corpus.files` to mirror globs (`build/corpus/drive/**/*.md` etc.)
4. Run `npm run glossary:sync && npm run glossary:extract`

---

## Do not

- Do not restore sibling path scripts (`../term-prep-platform/...`)
- Do not point `corpus.files` to Genspark aidrive
- Do not duplicate platform implementation code in consumer
