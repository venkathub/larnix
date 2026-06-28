#!/usr/bin/env python3
"""Tests for the R10 notebook-execution gate.

Requires a Jupyter `python3` kernel (nbclient + ipykernel). Kept OUT of the
schema job's discovery; run explicitly in the notebooks CI job:

    cd infra/ci && python -m unittest test_run_notebooks
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import run_notebooks as rn  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


class RunNotebookTests(unittest.TestCase):
    def test_passing_notebook_executes(self):
        ok, err = rn.run_ipynb(os.path.join(FIXTURES, "pass.ipynb"))
        self.assertTrue(ok, msg=f"expected pass, got error: {err}")
        self.assertIsNone(err)

    def test_failing_notebook_reports_error(self):
        ok, err = rn.run_ipynb(os.path.join(FIXTURES, "fail.ipynb"))
        self.assertFalse(ok)
        self.assertIn("boom", err)

    def test_collect_skips_checkpoints(self):
        targets = rn.collect_targets(
            ["x/.ipynb_checkpoints/foo.ipynb", os.path.join(FIXTURES, "pass.ipynb")]
        )
        self.assertNotIn("x/.ipynb_checkpoints/foo.ipynb", targets)
        self.assertEqual(len(targets), 1)

    def test_main_nothing_to_run_is_green(self):
        # An empty glob target → exit 0 ("nothing to execute").
        rc = rn.main(["modules/__definitely_missing__/**/*.ipynb"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
