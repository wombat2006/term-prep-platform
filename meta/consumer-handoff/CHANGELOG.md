# Consumer-facing changelog (platform)

Dated entries for changes that affect **techdev-cursor** (and other consumers).  
Platform-internal refactors omitted unless they break invoke contract.

Format: `YYYY-MM-DD` — summary — consumer action if any

---

## 2026-06-29 — LLM provider policy added (contracts)

**Changed**

- Added `meta/contracts/llm-provider-policy.md`: SDK interface design, error normalization table,
  and `providers.json` format for Anthropic / Google Gen AI / Ollama
- `mcp-tool-contract.md`: clarified that `provider_id` is informational; added link to new policy
- `02-schema-and-cli.md`: added one-liner explaining provider abstraction when `knowledge_filter.enabled: true`

**Consumer action**

None. Provider chain is platform-controlled. No consumer config changes.

---

## 2026-06-29 — Decoupling pivot: package contract (D-004)

**Changed**

- Adopted artifact boundary (`term-prep-platform` package + Semver pin)
- Deprecated A+C cross-repo issue bot flow
- Rewrote consumer PR guide for package cutover
- Added consumer CI template: `templates/consumer-contract-ci.yml`

**Consumer action**

- Open cutover PR based on [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md)
- Replace sibling path launch with package entrypoints
- Add contract CI check (`term-prep-contract-check`)

---

## 2026-06-29 — Plan B contract-first canon (D-005, draft)

**Added**

- `meta/contracts/` as canonical spec directory for future remote service surfaces
- Domain contract definitions: `TermCandidate`, `KnowledgeClassification`, `SyncJob`, `AsyncJobStatus`, `ErrorEnvelope`
- Surface contract drafts: HTTP OpenAPI, SSE event envelope schema, MCP tool contract, CLI contract
- Connector SPI contract for lower-cost adapter onboarding

**Consumer action**

- No immediate migration required; keep using package CLI contract (`1.x`)
- Track `meta/contracts/` before adopting remote service integration

---

## 2026-06-21 — A+C cross-repo workflow (bot + consumer scripts)

**Added**

- `06-cross-repo-workflow.md` — Issue bot (C) + consumer PR (A) coordination
- `scripts/cross_repo/notify_consumer_issue.sh` — opens consumer Issue on handoff CHANGELOG
- `scripts/cross_repo/consumer-templates/` — `check-handoff.sh`, `request-platform-change.sh`
- `.github/workflows/consumer-handoff-notify.yml` — Action on `meta/consumer-handoff/**` push

**Consumer action**

- Install `scripts/platform-handoff/` via consumer PR ([04](./04-consumer-pr-guide-techdev-cursor.md) §5)
- On Issue: read handoff → `check-handoff.sh` → consumer PR or `request-platform-change.sh`
- Configure platform secret `CROSS_REPO_GH_TOKEN` for bot

---

## 2026-06-21 — Consumer PR guide + implementation reference

**Added**

- `05-platform-implementation.md` — full Phase 0 · 0.5 artifact map and flows
- `04-consumer-pr-guide-techdev-cursor.md` — **consumer PR spec** (copy-paste files; platform does not edit techdev-cursor)

**Consumer action**

- Open techdev-cursor PR using **04** (pointers, `source` config, `glossary:sync*` scripts)
- OAuth live sync still **deferred**

---

## 2026-06-21 — Phase 0.5 Drive mirror (platform)

**Shipped**

- `connectors/googledrive/` — mirror mode (TypeScript, no Genspark/aidrive)
- `scripts/sync_corpus.py` — reads `source` from glossary-config
- Schema: optional `source` block (`googledrive`, `local_mirror`, `folder_id`)
- `corpus.files` glob support in `glossary_extractor`
- No-credential test suite: `scripts/run_phase05_checks.sh`

**Consumer action**

- B1–B5 in [03-consumer-actions.md](./03-consumer-actions.md) when enabling Drive mirror
- B7 (live OAuth smoke) **deferred**
- A4: add documentation pointer in consumer repo (user)

**Not changed**

- adopt/hold JSON output shape
- `glossary:extract` npm script contract
- MCP tool surface (`classify_term` stub)

---

## 2026-06-21 — Consumer handoff pack created

- New directory `meta/consumer-handoff/` for platform → consumer status
- Complements techdev-cursor `meta/platform-integration/`

**Consumer action:** Read [README.md](./README.md); add index pointer (A4)

---

## 2026-06-21 — Phase 0 baseline (reference)

- adopt/hold output split, JSON Schema validation, `glossary-knowledge` MCP stub
- Consumer Phase 0 aligned

**Consumer action:** None (already live)
