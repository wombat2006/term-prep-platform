"""Phase 0.5 tests that do not require Google Drive credentials.

Live Drive sync (real OAuth tokens + folder_id) is intentionally out of scope here;
see connectors/googledrive/README.md § Testing.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.glossary_extractor import (  # noqa: E402
    load_config,
    resolve_corpus_files,
    validate_config,
)
from scripts.sync_corpus import main as sync_corpus_main  # noqa: E402


class CorpusGlobTests(unittest.TestCase):
    def test_resolve_glob_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "build" / "corpus" / "drive").mkdir(parents=True)
            (root / "build" / "corpus" / "drive" / "a.md").write_text("# A", encoding="utf-8")
            (root / "build" / "corpus" / "drive" / "b.txt").write_text("B", encoding="utf-8")

            files = resolve_corpus_files(root, ["build/corpus/drive/**/*.md"])
            self.assertEqual(len(files), 1)
            self.assertTrue(files[0].name.endswith("a.md"))

    def test_resolve_literal_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "README.md"
            doc.write_text("# readme", encoding="utf-8")
            files = resolve_corpus_files(root, ["README.md"])
            self.assertEqual(files, [doc.resolve()])


class GlossaryConfigSchemaTests(unittest.TestCase):
    def test_techdev_cursor_config_valid_with_source_disabled(self) -> None:
        config_path = _REPO_ROOT / "projects" / "techdev-cursor" / "glossary-config.json"
        config = load_config(config_path)
        self.assertFalse(config.get("source", {}).get("enabled"))


class SyncCorpusCheckTests(unittest.TestCase):
    def test_check_passes_when_source_disabled(self) -> None:
        config = _REPO_ROOT / "projects" / "techdev-cursor" / "glossary-config.json"
        code = sync_corpus_main(["--config", str(config), "--check"])
        self.assertEqual(code, 0)

    def test_enabled_without_folder_id_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "meta").mkdir()
            config_path = root / "meta" / "glossary-config.json"
            config = {
                "version": "1.0.0",
                "project_root": ".",
                "morphology": {"backend": "fugashi", "dictionary": "unidic-lite"},
                "corpus": {"files": ["README.md"]},
                "scoring": {
                    "adopt_threshold": 4,
                    "hold_threshold": 2,
                    "weights": {
                        "in_ts_or_adr": 2,
                        "multi_chapter": 2,
                        "emphasis": 2,
                        "english_pair": 2,
                        "already_in_glossary": -10,
                        "stop_noun": -5,
                    },
                },
                "source": {
                    "enabled": True,
                    "adapter": "googledrive",
                    "local_mirror": "build/corpus/drive",
                    "googledrive": {"folder_id": ""},
                },
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")
            (root / "README.md").write_text("# stub", encoding="utf-8")

            env = os.environ.copy()
            env.pop("GOOGLE_DRIVE_FOLDER_ID", None)
            proc = subprocess.run(
                [sys.executable, str(_REPO_ROOT / "scripts" / "sync_corpus.py"), "--config", str(config_path)],
                cwd=_REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("folder_id", proc.stderr.lower())


class DriveCliNoCredentialTests(unittest.TestCase):
    CLI = _REPO_ROOT / "connectors" / "googledrive" / "dist" / "cli.js"

    def test_cli_missing_folder_id(self) -> None:
        self.assertTrue(self.CLI.is_file(), "run: cd connectors/googledrive && npm run build")
        proc = subprocess.run(
            ["node", str(self.CLI), "mirror", "--output-dir", "/tmp/out"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("folder-id", proc.stderr.lower())

    def test_cli_missing_credentials(self) -> None:
        self.assertTrue(self.CLI.is_file())
        env = os.environ.copy()
        for key in (
            "GOOGLE_CLIENT_ID",
            "GOOGLE_CLIENT_SECRET",
            "GOOGLE_REFRESH_TOKEN",
            "GOOGLE_DRIVE_FOLDER_ID",
        ):
            env.pop(key, None)
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [
                    "node",
                    str(self.CLI),
                    "mirror",
                    "--folder-id",
                    "dummy-folder-for-test",
                    "--output-dir",
                    tmp,
                ],
                env=env,
                capture_output=True,
                text=True,
            )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("missing google drive credentials", proc.stderr.lower())


if __name__ == "__main__":
    unittest.main()
