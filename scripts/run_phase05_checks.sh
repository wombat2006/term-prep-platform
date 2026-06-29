#!/usr/bin/env bash
# Phase 0.5 checks that do NOT use Google Drive credentials.
# Live Drive sync smoke is deferred — see connectors/googledrive/README.md § Testing.

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== connectors/googledrive: build + unit tests (no credentials) =="
(cd connectors/googledrive && npm run test)

echo "== Python: glossary_extractor --check =="
source .venv/bin/activate
python scripts/glossary_extractor.py --check --config projects/_template/glossary-config.json

echo "== Python: sync_corpus --check =="
python scripts/sync_corpus.py --check --config projects/_template/glossary-config.json

echo "== Package contract check =="
term-prep-contract-check --config projects/_template/glossary-config.json --expect-major 1

echo "== Python: unittest (Phase 0.5, no credentials) =="
python -m unittest discover -s tests -p 'test_*.py' -v

echo ""
echo "OK: Phase 0.5 no-credential checks passed."
echo "NOTE: Google Drive live mirror (OAuth + folder_id) is NOT run here — schedule separately."
