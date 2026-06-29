# Consumer actions required (platform cannot apply)

**Read as:** Step 3 of [consumer-handoff index](./README.md)  
**Rule:** Platform agents **document** consumer work here and in [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md). **Do not edit techdev-cursor.** User or consumer agent opens the PR using the guide.

---

## Consumer PR (techdev-cursor)

**Full spec (title, body, file contents):** [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md)

Summary of what the consumer PR wires (artifact boundary):

| Consumer change | Purpose |
|-----------------|---------|
| package pin (`term-prep-platform==X.Y.Z`) | 安定した契約利用 |
| `mcp.json` command | `term-prep-glossary-knowledge-mcp`（PATH 経由） |
| npm scripts | `term-prep-extract` / `term-prep-sync` を呼ぶ |
| `meta/glossary-config.json` | package schema に整合 |
| CI | contract check（schema + semver） |

Live OAuth sync remains **deferred** — see 04 § Follow-up PR.

---

## Always (one-time setup)

| # | Action | Repo | Status |
|---|--------|------|--------|
| A1 | package install source を決める（PyPI / private index） | consumer dev machine | user |
| A2 | `mcp.json` を PATH ベース command に更新 | techdev-cursor | PR |
| A3 | `meta/glossary-config.json` を package schema に整合 | techdev-cursor | ongoing |
| A4 | CI に contract check 追加 | techdev-cursor | PR |

Template: [templates/consumer-contract-ci.yml](./templates/consumer-contract-ci.yml)

---

## Phase 0 — complete

No open platform blockers for in-repo corpus extract.

---

## Plan B prep (contract-first, no migration yet)

| # | Action | When | Notes |
|---|--------|------|-------|
| PB1 | Review canonical contracts in `meta/contracts/` | Before remote service adoption | read order starts at `meta/contracts/README.md` |
| PB2 | Validate any custom wrappers against `ErrorEnvelope` and async job states | During adapter planning | avoid custom payload drift |
| PB3 | Keep CI on package contract guard (`term-prep-contract-check`) | Every release | remains mandatory in `1.x` |

No consumer code change is required yet for this draft contract set.

---

## Phase 0.5 — Google Drive mirror (open)

| # | Action | When | Notes |
|---|--------|------|-------|
| B1 | `term-prep-sync --check --config <consumer-config>` | Before first sync | package install 後 |
| B2 | Set OAuth env vars | Before live sync | See [02-schema-and-cli.md](./02-schema-and-cli.md) |
| B3 | `source.enabled: true` + real `folder_id` in `meta/glossary-config.json` | When Drive corpus ready | |
| B4 | Update `corpus.files` to mirror globs | After B3 | e.g. `build/corpus/drive/**/*.md` |
| B5 | Run sync before extract | Each corpus refresh | `npm run glossary:sync` |
| B6 | Optional: npm hook `glossary:sync` before extract | Convenience | Spec in [04](./04-consumer-pr-guide-techdev-cursor.md) |
| B7 | Live smoke: sync → extract | **Deferred** | Credentials not used in platform CI yet |
| B8 | Thin re-export platform googledrive connector | Later (O-P007-004 step 3) | Reduce duplicate TS in consumer |

---

## Phase 4.5 — Vector ingest (future)

| # | Action | When |
|---|--------|------|
| C1 | Stop extending consumer `googledrive-connector.ts` vector path | Now (policy) |
| C2 | Wire Phase 4 hook to platform vector connector | When platform ships 4.5 |
| C3 | Add `outputs.rag` (or successor) keys to consumer config | With schema PR |

---

## Escalation template (consumer → user)

When blocked on platform:

```text
Blocked: <goal>
Read: platform release note + 01-platform-status.md
Package version: <term-prep-platform X.Y.Z>
Request: bump package / add contract support
```

---

## Per-consumer checklists

- [techdev-cursor](./consumers/techdev-cursor.md)
- [Template for new consumers](./consumers/_TEMPLATE.md)
