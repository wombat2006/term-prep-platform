# Google Drive connector — corpus mirror (Phase 0.5)

Status: **Phase 0.5** — `mirror` mode only. Vector ingest is Phase 4.5.

Patterns adapted from techdev-cursor `src/services/googledrive-connector/` (reference only).  
**No Genspark / aidrive.** Canonical ingest is Google Drive API → local mirror → `glossary_extractor`.

## Mirror flow

```text
Google Drive folder
  → connectors/googledrive (mirror)
  → {project_root}/build/corpus/drive/
  → glossary_extractor (corpus.files globs)
```

## Setup

```bash
cd connectors/googledrive
npm install
npm run build
```

## Credentials (env)

| Variable | Required |
|----------|----------|
| `GOOGLE_CLIENT_ID` | yes |
| `GOOGLE_CLIENT_SECRET` | yes |
| `GOOGLE_REFRESH_TOKEN` | yes |
| `GOOGLE_REDIRECT_URI` | no (default `urn:ietf:wg:oauth:2.0:oob`) |
| `GOOGLE_DRIVE_FOLDER_ID` | yes for CLI (or `--folder-id`) |

## CLI

```bash
npm run drive:mirror -- \
  --folder-id "$GOOGLE_DRIVE_FOLDER_ID" \
  --output-dir /path/to/techdev-cursor/build/corpus/drive
```

Or from platform root via `scripts/sync_corpus.py` (reads `glossary-config.json` `source` section).

## Consumer config

After mirror, consumer `meta/glossary-config.json` should use globs under `build/corpus/drive/`:

```json
{
  "source": {
    "enabled": true,
    "adapter": "googledrive",
    "local_mirror": "build/corpus/drive",
    "googledrive": {
      "folder_id": "YOUR_FOLDER_ID"
    }
  },
  "corpus": {
    "files": [
      "build/corpus/drive/**/*.md",
      "build/corpus/drive/**/*.txt",
      "build/corpus/drive/**/*.csv"
    ]
  }
}
```

Then in techdev-cursor: `npm run glossary:extract`

## Testing

### Without credentials (run now)

These validate build, config schema, corpus globs, and credential guards — **no Google OAuth or live Drive API**.

```bash
# All Phase 0.5 no-credential checks
bash scripts/run_phase05_checks.sh

# Or individually:
cd connectors/googledrive && npm run test
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/sync_corpus.py --check --config projects/techdev-cursor/glossary-config.json
```

### With credentials (deferred)

**Not run in CI or local dev until you provide OAuth env vars.** Schedule separately when ready:

| Step | Command |
|------|---------|
| Set env | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `GOOGLE_DRIVE_FOLDER_ID` |
| Enable config | consumer `meta/glossary-config.json`: `source.enabled: true`, real `folder_id` |
| Sync | `python scripts/sync_corpus.py --config <glossary-config.json>` |
| Extract | `npm run glossary:extract` (consumer) or `glossary_extractor.py` |

Expected: `build/corpus/drive/` populated, `mirror-manifest.json` present, extract reads `corpus.files` globs.

## Related

- [O-P007-004](../../meta/glossary-pipeline/options/O-P007-004-googledrive-connector-reuse.md)
- [docs/integrations/techdev-cursor.md](../../docs/integrations/techdev-cursor.md)
- Consumer boundary: `techdev-cursor/meta/platform-integration/`
