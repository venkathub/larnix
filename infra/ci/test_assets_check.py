#!/usr/bin/env python3
"""Unit tests for the dataset license-ledger gate (infra/ci/assets_check.py).

Run:  cd infra/ci && python3 -m unittest test_assets_check -v
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import assets_check as ac  # noqa: E402


class UnledgeredTests(unittest.TestCase):
    def test_path_match_passes(self):
        files = ["modules/03-data/data/penguins.csv"]
        ledger = "see `modules/03-data/data/penguins.csv` — CC0-1.0"
        self.assertEqual(ac.unledgered(files, ledger), [])

    def test_basename_match_passes(self):
        files = ["modules/03-data/data/penguins.csv"]
        ledger = "penguins.csv | CC0-1.0"
        self.assertEqual(ac.unledgered(files, ledger), [])

    def test_unledgered_flagged(self):
        files = ["modules/03-data/data/penguins.csv", "modules/01-python/data/habits.csv"]
        ledger = "penguins.csv | CC0-1.0"  # habits.csv missing
        self.assertEqual(ac.unledgered(files, ledger), ["modules/01-python/data/habits.csv"])


class MainTests(unittest.TestCase):
    def _run_in(self, files: dict, ledger_text):
        """Build a temp repo with given data files (+ optional ledger), run main()."""
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            try:
                os.chdir(d)
                for rel, content in files.items():
                    p = Path(d) / rel
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(content, encoding="utf-8")
                args = []
                if ledger_text is not None:
                    led = Path(d) / "docs" / "ASSETS.md"
                    led.parent.mkdir(parents=True, exist_ok=True)
                    led.write_text(ledger_text, encoding="utf-8")
                return ac.main(args)
            finally:
                os.chdir(cwd)

    def test_no_data_files_passes(self):
        self.assertEqual(self._run_in({}, "ledger"), 0)

    def test_ledgered_passes(self):
        rc = self._run_in(
            {"modules/03-data/data/penguins.csv": "a,b\n1,2\n"},
            "penguins.csv — CC0-1.0",
        )
        self.assertEqual(rc, 0)

    def test_unledgered_fails(self):
        rc = self._run_in(
            {"modules/03-data/data/penguins.csv": "a,b\n1,2\n"},
            "nothing relevant here",
        )
        self.assertEqual(rc, 1)

    def test_missing_ledger_fails(self):
        rc = self._run_in(
            {"modules/03-data/data/penguins.csv": "a,b\n1,2\n"},
            None,  # no ledger file
        )
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
