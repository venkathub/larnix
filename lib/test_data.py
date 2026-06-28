#!/usr/bin/env python3
"""Unit tests for the vendored-dataset loader (lib/data.py).

The stdlib path helpers are tested unconditionally; the pandas round-trip is
guarded by ``skipUnless`` so the pandas-less CI "grader" job stays green.

Run:  cd lib && python3 -m unittest test_data -v
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data  # noqa: E402

try:
    import pandas  # noqa: F401
    _HAS_PANDAS = True
except ImportError:
    _HAS_PANDAS = False


class DatasetPathTests(unittest.TestCase):
    def test_path_is_data_relative(self):
        self.assertEqual(data.dataset_path("penguins"), Path("data") / "penguins.csv")

    def test_rejects_separators_and_traversal(self):
        for bad in ["", "a/b", "..", "../secret", "x\\y"]:
            with self.assertRaises(ValueError):
                data.dataset_path(bad)


class LoadCsvTests(unittest.TestCase):
    def test_missing_file_raises_with_guidance(self):
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            try:
                os.chdir(d)
                with self.assertRaises(FileNotFoundError) as cm:
                    data.load_csv("nope")
                self.assertIn("resources:", str(cm.exception))
            finally:
                os.chdir(cwd)

    @unittest.skipUnless(_HAS_PANDAS, "pandas not installed")
    def test_round_trip_reads_vendored_csv(self):
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            try:
                os.chdir(d)
                (Path(d) / "data").mkdir()
                (Path(d) / "data" / "toy.csv").write_text(
                    "a,b\n1,x\n2,y\n", encoding="utf-8"
                )
                df = data.load_csv("toy")
                self.assertEqual(list(df.columns), ["a", "b"])
                self.assertEqual(df.shape, (2, 2))
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
