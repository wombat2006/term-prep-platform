# Consumer PR guide — techdev-cursor (copy from platform only)

**Read as:** Step 4 when preparing a **techdev-cursor** PR.  
**Rule:** term-prep-platform agents **do not** edit techdev-cursor. A human or consumer agent opens the PR using this spec.

**Prerequisite reads:** [05-platform-implementation.md](./05-platform-implementation.md) · [01-platform-status.md](./01-platform-status.md) · [02-schema-and-cli.md](./02-schema-and-cli.md)

---

## What this PR achieves

After merge, anyone working in **techdev-cursor** can:

1. Find platform progress without chat history (pointer → sibling or GitHub).
2. Run Phase 0.5 **check** paths (`glossary:sync:check`) without OAuth.
3. Enable Drive mirror later by flipping `source.enabled` + `corpus.files` (credentials still **deferred**).

This PR does **not** require Google OAuth. Live `glossary:sync` smoke remains a follow-up task.

---

## Suggested PR title

```text
docs: Phase 0.5 glossary handoff — read term-prep-platform consumer-handoff
```

---

## Suggested PR body (paste into GitHub)

```markdown
## Summary

- Add read-only pointer to term-prep-platform `meta/consumer-handoff/` (platform progress + schema + obligations).
- Add `source` block to `meta/glossary-config.json` (disabled until Drive OAuth ready).
- Add `glossary:sync` / `glossary:sync:check` npm scripts delegating to platform `sync_corpus.py`.
- Document Phase 0.5 in glossary pipeline TO-BE.

Platform Phase 0.5 implementation is **complete without credentials** (mirror code + tests). Live Drive sync is **deferred**.

## Read on platform (canonical)

Sibling or clone `term-prep-platform`, then:

1. `meta/consumer-handoff/README.md`
2. `meta/consumer-handoff/05-platform-implementation.md`
3. `meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md` (this PR spec)

## Test plan

- [ ] Platform bot Issue received (label `platform-handoff`) or run `check-handoff.sh`
- [ ] `npm run glossary:extract:check` — unchanged
- [ ] `npm run glossary:sync:check` — ok when `source.enabled: false`
- [ ] `./scripts/platform-handoff/check-handoff.sh` then `--mark-seen`
- [ ] Platform: `bash ../term-prep-platform/scripts/run_phase05_checks.sh`
- [ ] **Not in this PR:** live Drive OAuth sync (scheduled later)

## Out of scope

- No changes to `googledrive-connector.ts`
- No Genspark / aidrive
- No commits to term-prep-platform from this PR
```

---

## Files to add or change (techdev-cursor)

Apply in **techdev-cursor** only. Paths below are relative to **techdev-cursor repo root**.

### 1. NEW — `meta/TERM_PREP_PLATFORM_STATUS.md`

Shim — **no duplicate** of platform docs; links only.

```markdown
# term-prep-platform — progress & consumer obligations (read-only)

**Canonical pack lives on platform.** Do not copy `meta/consumer-handoff/` into this repo unless explicitly requested.

## Resolve platform path

| Priority | Path |
|----------|------|
| 1 | `$TERM_PREP_PLATFORM_ROOT/meta/consumer-handoff/README.md` |
| 2 | `../term-prep-platform/meta/consumer-handoff/README.md` |
| 3 | [GitHub — meta/consumer-handoff](https://github.com/wombat2006/term-prep-platform/tree/main/meta/consumer-handoff) |

## Read order (consumer agents)

| Step | Platform file | Purpose |
|------|---------------|---------|
| 0 | `README.md` | Index |
| 1 | `05-platform-implementation.md` | What platform built (Phase 0 · 0.5) |
| 2 | `01-platform-status.md` | Phase progress |
| 3 | `02-schema-and-cli.md` | Schema · CLI · MCP contract |
| 4 | `04-consumer-pr-guide-techdev-cursor.md` | Consumer PR / wiring spec |
| 5 | `03-consumer-actions.md` | Open obligations checklist |
| 6 | `CHANGELOG.md` | Dated platform changes |

**Boundary (consumer → platform):** [meta/platform-integration/README.md](./platform-integration/README.md)

**Glossary consumer doc:** [meta/TO-BE-GLOSSARY-PIPELINE.md](./TO-BE-GLOSSARY-PIPELINE.md)
```

---

### 2. EDIT — `docs/DOCUMENTATION_INDEX.md`

Under **### Integration**, add after item 5 (platform-integration):

```markdown
6. **[../term-prep-platform/meta/consumer-handoff/README.md](../term-prep-platform/meta/consumer-handoff/README.md)** — **platform progress** (implementation · schema · consumer obligations · [shim](../meta/TERM_PREP_PLATFORM_STATUS.md))
```

Renumber following items if your index uses strict numbering.

---

### 3. EDIT — `meta/glossary-config.json`

Add **`source`** block (keep existing `corpus.files` until Drive enabled):

```json
  "source": {
    "enabled": false,
    "adapter": "googledrive",
    "local_mirror": "build/corpus/drive",
    "googledrive": {
      "folder_id": ""
    }
  },
```

Insert after the `corpus` object (comma placement per JSON).  
Update `corpus.description` to note interim vs mirror:

```json
"description": "Interim in-repo paths. When source.enabled=true, use build/corpus/drive/**/*.md after glossary:sync."
```

**When enabling Drive (later, separate PR or same repo follow-up):**

```json
"source": { "enabled": true, "googledrive": { "folder_id": "YOUR_FOLDER_ID" } },
"corpus": {
  "files": [
    "build/corpus/drive/**/*.md",
    "build/corpus/drive/**/*.txt",
    "build/corpus/drive/**/*.csv"
  ]
}
```

Schema reference: platform `meta/schemas/glossary-config.schema.json`.

---

### 4. NEW — `scripts/run-glossary-sync.sh`

```bash
#!/usr/bin/env bash
# Invoke term-prep-platform sync_corpus against THIS repo's consumer config only.
# Read-only on the platform clone — do not edit or commit term-prep-platform from here.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLATFORM_ROOT="${TERM_PREP_PLATFORM_ROOT:-$REPO_ROOT/../term-prep-platform}"
PYTHON="${PLATFORM_ROOT}/.venv/bin/python"
SYNC="${PLATFORM_ROOT}/scripts/sync_corpus.py"
CONFIG="${REPO_ROOT}/meta/glossary-config.json"

if [[ ! -f "$CONFIG" ]]; then
  echo "error: consumer config not found: $CONFIG" >&2
  exit 1
fi

if [[ ! -x "$PYTHON" ]]; then
  echo "error: platform venv not found: $PYTHON" >&2
  echo "Clone term-prep-platform as sibling and install requirements-dev.txt" >&2
  exit 1
fi

if [[ ! -f "$SYNC" ]]; then
  echo "error: sync_corpus.py not found: $SYNC" >&2
  echo "Platform Phase 0.5 required — read ../term-prep-platform/meta/consumer-handoff/05-platform-implementation.md" >&2
  exit 1
fi

CONNECTOR_CLI="${PLATFORM_ROOT}/connectors/googledrive/dist/cli.js"
if [[ ! -f "$CONNECTOR_CLI" ]]; then
  echo "error: Drive connector not built: $CONNECTOR_CLI" >&2
  echo "Run: cd \"\$TERM_PREP_PLATFORM_ROOT/connectors/googledrive\" && npm install && npm run build" >&2
  exit 1
fi

if [[ "${1:-}" == "--check" ]]; then
  exec "$PYTHON" "$SYNC" --config "$CONFIG" --check
fi

exec "$PYTHON" "$SYNC" --config "$CONFIG"
```

`chmod +x scripts/run-glossary-sync.sh`

---

### 5. NEW — `scripts/platform-handoff/` (A+C hybrid)

Install from platform clone into consumer before commit:

```bash
cd /path/to/term-prep-platform
./scripts/cross_repo/install_consumer_scripts.sh
# → copies to ../techdev-cursor/scripts/platform-handoff/
```

Adds:

| File | Role |
|------|------|
| `check-handoff.sh` | Compare platform CHANGELOG vs `meta/.platform-handoff-last-seen` |
| `request-platform-change.sh` | Open Issue on term-prep-platform |
| `README.md` | Consumer-side workflow |

Optional `.gitignore` line:

```gitignore
meta/.platform-handoff-last-seen
```

Workflow: [06-cross-repo-workflow.md](./06-cross-repo-workflow.md)

---

### 6. EDIT — `package.json` scripts

Add next to existing glossary scripts:

```json
    "glossary:sync": "bash scripts/run-glossary-sync.sh",
    "glossary:sync:check": "bash scripts/run-glossary-sync.sh --check",
```

---

### 7. EDIT — `meta/TO-BE-GLOSSARY-PIPELINE.md`

Add section after **Phase 0 (done)**:

```markdown
## Phase 0.5 — Google Drive mirror (platform ready · consumer wiring)

**Platform (read-only):** mirror connector + `sync_corpus.py` — see sibling `../term-prep-platform/meta/consumer-handoff/05-platform-implementation.md`.

| Step | Command | OAuth required |
|------|---------|----------------|
| Check wiring | `npm run glossary:sync:check` | No |
| Sync Drive → `build/corpus/drive/` | `npm run glossary:sync` | Yes |
| Extract | `npm run glossary:extract` | No (uses local mirror) |

Config: `source` block in `meta/glossary-config.json` (`enabled: false` until folder_id + env ready).

**Deferred:** live Drive sync smoke — credentials not used in platform default tests.

**Do not** point `corpus.files` at Genspark aidrive. **Do not** extend `googledrive-connector.ts` for new prep — escalate platform work to user.
```

Update **Next (not in scope yet)** — remove “Google Drive local mirror” if present; add pointer to Phase 0.5 section above.

---

### 8. EDIT — `README.md` and `README_en.md` (optional but recommended)

In **実装分担** / **Implementation ownership** section, add row or footnote:

```markdown
**Platform progress (read-only):** [meta/TERM_PREP_PLATFORM_STATUS.md](./meta/TERM_PREP_PLATFORM_STATUS.md) → sibling `term-prep-platform/meta/consumer-handoff/`
```

Under **次に読むもの** / **Next reads**:

```markdown
| **Platform progress · Phase 0.5** | [TERM_PREP_PLATFORM_STATUS.md](./meta/TERM_PREP_PLATFORM_STATUS.md) |
```

---

## Post-merge verification (no OAuth)

From **techdev-cursor** root (sibling platform with `.venv` + built connector):

```bash
npm run glossary:extract:check
npm run glossary:sync:check
./scripts/platform-handoff/check-handoff.sh
./scripts/platform-handoff/check-handoff.sh --mark-seen
```

From **term-prep-platform**:

```bash
bash scripts/run_phase05_checks.sh
python scripts/sync_corpus.py --check \
  --config ../techdev-cursor/meta/glossary-config.json
```

Expected: `ok: source disabled (check only)` until `source.enabled: true`.

---

## Follow-up PR (when OAuth ready — not this PR)

| Step | Action |
|------|--------|
| 1 | Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `GOOGLE_DRIVE_FOLDER_ID` |
| 2 | `source.enabled: true` + real `folder_id` |
| 3 | `corpus.files` → `build/corpus/drive/**/*.md` (etc.) |
| 4 | `npm run glossary:sync && npm run glossary:extract` |
| 5 | Document smoke result in consumer PR or issue |

---

## What consumer must **not** do

| Forbidden | Reason |
|-----------|--------|
| Copy entire `meta/consumer-handoff/` into techdev-cursor | Single canonical copy on platform |
| Implement mirror in `googledrive-connector.ts` | Platform owns Phase 0.5 |
| Use aidrive / Genspark paths in `corpus.files` | [platform-integration/02](https://github.com/wombat2006/techdev-cursor/blob/master/meta/platform-integration/02-genspark-aidrive-boundary.md) |
| Commit changes to term-prep-platform from consumer task | Cross-repo policy |

---

## Related

- [consumers/techdev-cursor.md](./consumers/techdev-cursor.md)
- [03-consumer-actions.md](./03-consumer-actions.md)
- Platform integration view: [docs/integrations/techdev-cursor.md](../../docs/integrations/techdev-cursor.md)
