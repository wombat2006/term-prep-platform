# Consumer-facing changelog (platform)

Dated entries for changes that affect **techdev-cursor** (and other consumers).  
Platform-internal refactors omitted unless they break invoke contract.

Format: `YYYY-MM-DD` — summary — consumer action if any

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
