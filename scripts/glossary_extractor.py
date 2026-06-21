#!/usr/bin/env python3
"""
glossary_extractor.py — Reusable glossary candidate extraction from Markdown corpora.

Requires fugashi + an external MeCab dictionary (default: unidic-lite).
Designed for reuse across research repos and specialized terminology projects.

Usage:
    python scripts/glossary_extractor.py
    python scripts/glossary_extractor.py --config meta/glossary-config.json
    python scripts/glossary_extractor.py --check   # verify morphology backend only

Exit codes:
    0 success
    1 configuration / IO error
    2 morphology backend unavailable (fugashi or dictionary missing)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Morphology backend (fugashi + external dictionary) — mandatory by default
# ---------------------------------------------------------------------------

MORPHOLOGY_ERROR = """
glossary_extractor requires fugashi and an external MeCab dictionary.

Install:
  python3 -m pip install -r requirements-dev.txt

System (if fugashi fails to load MeCab):
  Debian/Ubuntu: sudo apt install mecab libmecab-dev
  macOS:         brew install mecab

Verify:
  python scripts/glossary_extractor.py --check
""".strip()


@dataclass
class MorphologyBackend:
    name: str
    dictionary: str
    dicdir: str
    tagger: Any

    def nouns(self, text: str, *, min_len: int = 2) -> list[str]:
        out: list[str] = []
        for word in self.tagger(text):
            pos1 = word.feature.pos1
            pos2 = getattr(word.feature, "pos2", "") or ""
            if pos1 != "名詞":
                continue
            if pos2 in ("非自立", "代名詞", "副詞可能", "数"):
                continue
            surface = word.surface.strip()
            if len(surface) >= min_len:
                out.append(surface)
        return out


def _resolve_dictionary(dict_name: str) -> tuple[str, str]:
    """Return (dictionary_id, dicdir_path). Raises RuntimeError if unavailable."""
    if dict_name in ("unidic-lite", "unidic_lite"):
        try:
            import unidic_lite
        except ImportError as exc:
            raise RuntimeError("unidic-lite is not installed") from exc
        return "unidic-lite", unidic_lite.DICDIR

    if dict_name == "unidic":
        try:
            import unidic
        except ImportError as exc:
            raise RuntimeError("unidic is not installed (pip install unidic)") from exc
        dicdir = unidic.DICDIR
        if not Path(dicdir).exists():
            raise RuntimeError("UniDic files missing; run: python -m unidic download")
        return "unidic", dicdir

    if dict_name in ("ipadic", "ipadic-utf8"):
        for candidate in (
            "/var/lib/mecab/dic/ipadic-utf8",
            "/usr/lib/mecab/dic/ipadic-utf8",
            "/opt/homebrew/lib/mecab/dic/ipadic-utf8",
        ):
            if Path(candidate).exists():
                return "ipadic-utf8", candidate
        raise RuntimeError(f"IPAdic dictionary not found on system paths for {dict_name!r}")

    raise RuntimeError(f"Unknown dictionary: {dict_name!r}")


def create_morphology_backend(config: dict) -> MorphologyBackend:
    morph = config.get("morphology", {})
    if morph.get("backend", "fugashi") != "fugashi":
        raise RuntimeError(f"Unsupported morphology backend: {morph.get('backend')!r}")

    dict_name = morph.get("dictionary", "unidic-lite")
    try:
        from fugashi import Tagger
    except ImportError as exc:
        raise RuntimeError("fugashi is not installed") from exc

    dictionary, dicdir = _resolve_dictionary(dict_name)
    try:
        tagger = Tagger(f"-d {dicdir}")
    except Exception as exc:
        raise RuntimeError(f"Failed to initialize MeCab tagger with {dictionary}: {exc}") from exc

    # smoke test
    _ = list(tagger("テスト"))

    return MorphologyBackend(
        name="fugashi",
        dictionary=dictionary,
        dicdir=dicdir,
        tagger=tagger,
    )


# ---------------------------------------------------------------------------
# Markdown / corpus processing
# ---------------------------------------------------------------------------

CODE_FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\([^\)]+\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ENGLISH_PHRASE = re.compile(
    r"(?:^|[\s（(「])([A-Z][A-Za-z0-9][A-Za-z0-9 \-/=∞.+']{0,48})(?=[\s、。，,.）)」]|$)"
)
KATAKANA = re.compile(r"[\u30A0-\u30FFー]{2,}")


def strip_markdown(text: str) -> str:
    text = CODE_FENCE.sub(" ", text)
    text = INLINE_CODE.sub(r" \1 ", text)
    text = LINK.sub(r" \1 ", text)
    text = BOLD.sub(r" \1 ", text)
    text = re.sub(r"^#+\s*", " ", text, flags=re.M)
    text = re.sub(r"^[-|>].*$", " ", text, flags=re.M)
    return text


@dataclass
class TermRecord:
    term: str
    lang: str  # ja | en | mixed
    morph_freq: int = 0
    emphasis_freq: int = 0
    code_freq: int = 0
    chapters: set[str] = field(default_factory=set)
    signals: set[str] = field(default_factory=set)

    @property
    def frequency(self) -> int:
        return self.morph_freq + self.emphasis_freq + self.code_freq


def detect_lang(term: str) -> str:
    if re.search(r"[A-Za-z]", term) and re.search(r"[\u3040-\u9FFF]", term):
        return "mixed"
    if re.search(r"[A-Za-z]", term):
        return "en"
    return "ja"


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def project_root_from_config(config_path: Path, config: dict) -> Path:
    rel = config.get("project_root", "..")
    return (config_path.parent / rel).resolve()


def load_glossary_terms(glossary_path: Path) -> set[str]:
    if not glossary_path.exists():
        return set()
    text = glossary_path.read_text(encoding="utf-8")
    terms: set[str] = set()
    for m in re.finditer(r"^###\s+(.+)$", text, re.M):
        title = m.group(1).strip()
        title = re.sub(r"（[^）]+）", "", title).strip()
        terms.add(title)
    return terms


def load_catalog_terms(paths: list[Path]) -> set[str]:
    terms: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"(?:^#+\s+|[-*]\s+)(TS-\d+|ADR-\d+)[^\n]*", text, re.M):
            terms.add(m.group(0))
        for m in re.finditer(r"\*\*([A-Za-z][A-Za-z0-9 /=∞.+'-]{2,})\*\*", text):
            terms.add(m.group(1).strip())
        for m in re.finditer(r"(Attention [A-Za-z]+|Platform Capital|Participation Capital|"
                             r"Effective Population|Variable Reward|Evolutionary Mismatch|"
                             r"Skinner Box|Prediction Market|Meaning Allocation)", text):
            terms.add(m.group(1))
    return terms


def chapter_id(path: Path) -> str:
    return path.stem


def extract_from_corpus(
    backend: MorphologyBackend,
    corpus_files: list[Path],
) -> dict[str, TermRecord]:
    records: dict[str, TermRecord] = {}

    def touch(term: str) -> TermRecord:
        key = term.strip()
        if key not in records:
            records[key] = TermRecord(term=key, lang=detect_lang(key))
        return records[key]

    for path in corpus_files:
        raw = path.read_text(encoding="utf-8")
        ch = chapter_id(path)
        plain = strip_markdown(raw)

        for noun in backend.nouns(plain):
            rec = touch(noun)
            rec.morph_freq += 1
            rec.chapters.add(ch)
            rec.signals.add("morph")

        for m in BOLD.finditer(raw):
            t = m.group(1).strip()
            if len(t) >= 2:
                rec = touch(t)
                rec.emphasis_freq += 1
                rec.chapters.add(ch)
                rec.signals.add("emphasis")

        for m in INLINE_CODE.finditer(raw):
            t = m.group(1).strip()
            if len(t) >= 2 and not t.startswith("http"):
                rec = touch(t)
                rec.code_freq += 1
                rec.chapters.add(ch)
                rec.signals.add("code")

        for m in ENGLISH_PHRASE.finditer(raw):
            t = m.group(1).strip()
            rec = touch(t)
            rec.emphasis_freq += 1
            rec.chapters.add(ch)
            rec.signals.add("english")

        for m in KATAKANA.finditer(raw):
            t = m.group(0)
            rec = touch(t)
            rec.morph_freq += 1
            rec.chapters.add(ch)
            rec.signals.add("katakana")

    return records


def is_valid_term(term: str) -> bool:
    t = term.strip()
    if not t or len(t) > 64:
        return False
    if any(x in t for x in ("\n", "↓", "```", "http://", "https://")):
        return False
    if t.startswith(("text\n", "ADR-", "TS-", "#")):
        return False
    if re.fullmatch(r"[a-zA-Z]{1,2}", t):
        return False
    if re.fullmatch(r"(as|an|in|on|is|not|or|the|fi|iv|model|text|ratio|reward|variable|prediction)", t, re.I):
        return False
    if re.fullmatch(r"\d+", t):
        return False
    return True


def normalize_for_match(term: str) -> str:
    return re.sub(r"\s+", " ", term.strip().lower())


def term_in_catalog(term: str, catalog_terms: set[str]) -> bool:
    if len(term) < 3:
        return False
    nt = normalize_for_match(term)
    for c in catalog_terms:
        nc = normalize_for_match(c)
        if len(nc) < 4:
            continue
        if nt == nc or (len(nt) >= 5 and nt in nc):
            return True
    return False


def score_record(
    rec: TermRecord,
    *,
    config: dict,
    glossary_terms: set[str],
    catalog_terms: set[str],
    manual_adopt: set[str],
    manual_reject: set[str],
    stop_nouns: set[str],
    stop_english: set[str],
) -> tuple[int, list[str], str]:
    w = config["scoring"]["weights"]
    adopt_t = config["scoring"]["adopt_threshold"]
    hold_t = config["scoring"]["hold_threshold"]
    reasons: list[str] = []
    score = 0

    if rec.term in manual_reject or any(r.lower() in rec.term.lower() for r in manual_reject):
        return -99, ["manual_reject"], "reject"

    if rec.term in manual_adopt:
        return 99, ["manual_adopt"], "adopt"

    for g in glossary_terms:
        if g in rec.term or rec.term in g:
            score += w["already_in_glossary"]
            reasons.append("already_in_glossary")
            break

    if rec.term in stop_nouns or rec.term in stop_english:
        score += w["stop_noun"]
        reasons.append("stop_noun")

    if term_in_catalog(rec.term, catalog_terms):
        score += w["in_ts_or_adr"]
        reasons.append("in_ts_or_adr")

    if len(rec.chapters) >= 2:
        score += w["multi_chapter"]
        reasons.append("multi_chapter")

    if "emphasis" in rec.signals or "code" in rec.signals:
        score += w["emphasis"]
        reasons.append("emphasis")

    if rec.lang in ("en", "mixed") or "english" in rec.signals:
        score += w["english_pair"]
        reasons.append("english_pair")

    if score >= adopt_t:
        status = "adopt"
    elif score >= hold_t:
        status = "hold"
    else:
        status = "reject"

    return score, reasons, status


def build_output(
    config: dict,
    backend: MorphologyBackend,
    records: dict[str, TermRecord],
    corpus_files: list[Path],
    glossary_terms: set[str],
    catalog_terms: set[str],
) -> dict:
    manual_adopt = set(config.get("manual_adopt", []))
    manual_reject = set(config.get("manual_reject", []))
    stop_nouns = set(config.get("stop_nouns", []))
    stop_english = set(config.get("stop_english", []))

    candidates = []
    for rec in records.values():
        if rec.frequency == 0 or not is_valid_term(rec.term):
            continue
        score, reasons, status = score_record(
            rec,
            config=config,
            glossary_terms=glossary_terms,
            catalog_terms=catalog_terms,
            manual_adopt=manual_adopt,
            manual_reject=manual_reject,
            stop_nouns=stop_nouns,
            stop_english=stop_english,
        )
        candidates.append(
            {
                "term": rec.term,
                "lang": rec.lang,
                "score": score,
                "status": status,
                "frequency": rec.frequency,
                "morph_freq": rec.morph_freq,
                "emphasis_freq": rec.emphasis_freq,
                "code_freq": rec.code_freq,
                "chapters": sorted(rec.chapters),
                "signals": sorted(rec.signals),
                "reasons": reasons,
            }
        )

    candidates.sort(key=lambda x: (-x["score"], -x["frequency"], x["term"]))
    summary = Counter(c["status"] for c in candidates)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "morphology": {
            "backend": backend.name,
            "dictionary": backend.dictionary,
            "dicdir": backend.dicdir,
            "required": config.get("morphology", {}).get("required", True),
        },
        "corpus_files": [str(p) for p in corpus_files],
        "summary": dict(summary),
        "candidates": candidates,
    }


def _resolve_output_path(root: Path, rel: str) -> Path:
    path = Path(rel)
    return path.resolve() if path.is_absolute() else (root / rel).resolve()


def write_outputs(root: Path, config: dict, payload: dict) -> dict[str, Path]:
    """Write adopt/hold/reject per config. Legacy single-file output supported."""
    out_cfg = config.get("output", "meta/glossary-candidates.json")
    filter_cfg = config.get("filter", {})
    emit_reject = filter_cfg.get("emit_reject", False)

    if isinstance(out_cfg, str):
        path = _resolve_output_path(root, out_cfg)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        return {"legacy": path}

    candidates = payload["candidates"]
    by_status = {
        "adopt": [c for c in candidates if c["status"] == "adopt"],
        "hold": [c for c in candidates if c["status"] == "hold"],
        "reject": [c for c in candidates if c["status"] == "reject"],
    }
    written: dict[str, Path] = {}

    for status in ("adopt", "hold"):
        rel = out_cfg.get(status)
        if not rel:
            continue
        path = _resolve_output_path(root, rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        doc = {
            "generated_at": payload["generated_at"],
            "status": status,
            "morphology": payload["morphology"],
            "corpus_files": payload["corpus_files"],
            "count": len(by_status[status]),
            "candidates": by_status[status],
        }
        with path.open("w", encoding="utf-8") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        written[status] = path

    if emit_reject:
        rel = out_cfg.get("reject", "build/glossary/reject.jsonl")
        path = _resolve_output_path(root, rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            for row in by_status["reject"]:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        written["reject"] = path

    return written


def run(config_path: Path) -> dict:
    config = load_config(config_path)
    root = project_root_from_config(config_path, config)

    morph_cfg = config.setdefault("morphology", {})
    morph_cfg.setdefault("backend", "fugashi")
    morph_cfg.setdefault("dictionary", "unidic-lite")
    morph_cfg.setdefault("required", True)

    backend = create_morphology_backend(config)

    corpus_files = [(root / f).resolve() for f in config["corpus"]["files"]]
    for p in corpus_files:
        if not p.exists():
            raise FileNotFoundError(f"Corpus file not found: {p}")

    catalog_paths = [(root / p).resolve() for p in config.get("reference_catalogs", [])]
    glossary_path = root / "GLOSSARY.md"
    glossary_terms = load_glossary_terms(glossary_path)
    catalog_terms = load_catalog_terms(catalog_paths)

    records = extract_from_corpus(backend, corpus_files)
    payload = build_output(config, backend, records, corpus_files, glossary_terms, catalog_terms)

    written = write_outputs(root, config, payload)
    payload["_written"] = {k: str(v) for k, v in written.items()}
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_config = Path(__file__).resolve().parents[1] / "meta" / "glossary-config.json"
    parser.add_argument("--config", type=Path, default=default_config)
    parser.add_argument("--check", action="store_true", help="Verify fugashi + dictionary only")
    args = parser.parse_args(argv)

    if args.check:
        try:
            config = load_config(args.config)
            backend = create_morphology_backend(config)
            print(f"OK: fugashi + {backend.dictionary}")
            print(f"DICDIR: {backend.dicdir}")
            sample = backend.nouns("注意経済における探索行動の Capacity と Capture")
            print(f"Sample nouns: {sample}")
            return 0
        except RuntimeError as exc:
            print(f"FAIL: {exc}", file=sys.stderr)
            print(MORPHOLOGY_ERROR, file=sys.stderr)
            return 2

    try:
        result = run(args.config)
    except RuntimeError as exc:
        print(f"Morphology error: {exc}", file=sys.stderr)
        print(MORPHOLOGY_ERROR, file=sys.stderr)
        return 2
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    summary = result["summary"]
    written = result.get("_written", {})
    if "legacy" in written:
        print(f"Wrote {written['legacy']}")
    else:
        for kind, path in written.items():
            print(f"Wrote {kind}: {path}")
    print(
        f"Candidates: adopt={summary.get('adopt', 0)} "
        f"hold={summary.get('hold', 0)} reject={summary.get('reject', 0)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
