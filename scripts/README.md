# Scripts

Project:
term-prep-platform

---

## Setup

```bash
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -r requirements-mcp.txt
```

**System:** MeCab (`libmecab`)

| OS | Command |
|---|---|
| AlmaLinux / RHEL 9 | `sudo dnf install mecab`（`mecab-devel` は **不要** — AppStream に無い） |
| Debian/Ubuntu | `sudo apt install mecab libmecab-dev` |
| macOS | `brew install mecab` |

---

## glossary_extractor.py

Extract glossary candidates from Markdown using **fugashi + unidic-lite**.

```bash
# Default config path: meta/glossary-config.json (legacy)
# Consumer configs live under projects/
python scripts/glossary_extractor.py --check \
  --config projects/dopagaki-transition/glossary-config.json

python scripts/glossary_extractor.py \
  --config projects/dopagaki-transition/glossary-config.json
```

**Governance:** [meta/glossary-pipeline/](../meta/glossary-pipeline/README.md)  
**Roadmap:** [meta/TO-BE-PLATFORM.md](../meta/TO-BE-PLATFORM.md)

Exit codes: `0` success · `1` config/IO · `2` morphology unavailable

---

## File roles

| File | Role |
|---|---|
| `scripts/glossary_extractor.py` | Shared extraction CLI |
| `projects/<consumer>/glossary-config.json` | Per-project corpus & scoring |
| `build/glossary/` | Generated adopt/hold/reject (Git ignored) |
