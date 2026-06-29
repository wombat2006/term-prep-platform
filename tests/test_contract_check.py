from __future__ import annotations

import unittest
from pathlib import Path

from term_prep_platform.cli import contract_check


class ContractCheckTests(unittest.TestCase):
    def test_contract_check_passes_for_template(self) -> None:
        config = Path(__file__).resolve().parents[1] / "projects" / "_template" / "glossary-config.json"
        code = contract_check(["--config", str(config), "--expect-major", "1"])
        self.assertEqual(code, 0)

    def test_contract_check_fails_on_wrong_major(self) -> None:
        config = Path(__file__).resolve().parents[1] / "projects" / "_template" / "glossary-config.json"
        code = contract_check(["--config", str(config), "--expect-major", "99"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
