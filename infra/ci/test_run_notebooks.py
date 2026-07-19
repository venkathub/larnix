#!/usr/bin/env python3
"""Tests for the R10 notebook-execution gate.

Requires a Jupyter `python3` kernel (nbclient + ipykernel). Kept OUT of the
schema job's discovery; run explicitly in the notebooks CI job:

    cd infra/ci && python -m unittest test_run_notebooks
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import run_notebooks as rn  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _code_cell(cell_id, source, larnix=None):
    meta = {"larnix": larnix} if larnix else {}
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": meta,
        "outputs": [],
        "source": source,
    }


def make_companion(tmpdir, cells, generated=True):
    """Write a minimal generated-companion notebook (the make_colab metadata
    contract) and return its path."""
    meta = {"kernelspec": {"display_name": "Python 3", "language": "python",
                           "name": "python3"}}
    if generated:
        meta["larnix"] = {"compute": "colab", "generated_by": "infra/ci/make_colab.py"}
    else:
        meta["larnix"] = {"compute": "colab"}
    nb = {"cells": cells, "metadata": meta, "nbformat": 4, "nbformat_minor": 5}
    path = os.path.join(tmpdir, "ch-colab.ipynb")
    Path(path).write_text(json.dumps(nb), encoding="utf-8")
    return path


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

    def test_gpu_colab_notebook_is_skipped(self):
        # infra/ci/ -> infra/ -> infra/fixtures/colab-fixture.ipynb
        infra_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(infra_dir, "fixtures", "colab-fixture.ipynb")
        self.assertTrue(os.path.exists(path), msg=f"missing fixture: {path}")
        self.assertFalse(rn.should_run(path))
        self.assertEqual(rn.classify(path), "skip")

    def test_plain_notebook_is_run(self):
        self.assertTrue(rn.should_run(os.path.join(FIXTURES, "pass.ipynb")))
        self.assertEqual(rn.classify(os.path.join(FIXTURES, "pass.ipynb")), "run")


class CompanionTests(unittest.TestCase):
    """The P2-D9 CPU-scaled execution contract for generated companions."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_generated_companion_classified_run_scaled(self):
        path = make_companion(self.tmp.name, [_code_cell("c1", "x = 1")])
        self.assertEqual(rn.classify(path), "run-scaled")
        self.assertTrue(rn.should_run(path))

    def test_hand_authored_colab_notebook_still_skipped(self):
        path = make_companion(
            self.tmp.name, [_code_cell("c1", "x = 1")], generated=False
        )
        self.assertEqual(rn.classify(path), "skip")

    def test_solution_substituted_and_rubric_dropped(self):
        # The starter raises; only the substituted solution passes. The rubric
        # cell raises unconditionally; only dropping it passes.
        cells = [
            _code_cell("params", "import os\nassert os.environ.get('LARNIX_CI') == '1'"),
            _code_cell(
                "ex-a",
                "raise RuntimeError('starter must not run')",
                larnix={"exercise": "a", "solution": "answer = 42\nassert answer == 42"},
            ),
            _code_cell(
                "ex-b",
                "raise RuntimeError('rubric must not run')",
                larnix={"exercise": "b", "rubric": True},
            ),
        ]
        path = make_companion(self.tmp.name, cells)
        ok, err = rn.run_ipynb(path, scaled=True)
        self.assertTrue(ok, msg=f"unexpected error: {err}")

    def test_larnix_ci_visible_in_kernel_and_restored_after(self):
        before = os.environ.get("LARNIX_CI")
        path = make_companion(
            self.tmp.name,
            [_code_cell("c1", "import os\nassert os.environ['LARNIX_CI'] == '1'")],
        )
        ok, err = rn.run_ipynb(path, scaled=True)
        self.assertTrue(ok, msg=f"unexpected error: {err}")
        self.assertEqual(os.environ.get("LARNIX_CI"), before)

    def test_unscaled_run_does_not_substitute(self):
        # Without scaled=True the starter source runs as-is (and here, fails) —
        # substitution is strictly a companion-execution behaviour.
        cells = [_code_cell("ex-a", "raise RuntimeError('starter ran')",
                            larnix={"exercise": "a", "solution": "pass"})]
        path = make_companion(self.tmp.name, cells)
        ok, err = rn.run_ipynb(path, scaled=False)
        self.assertFalse(ok)
        self.assertIn("starter ran", err)

    def test_budget_exceeded_fails_with_scale_down_message(self):
        os.environ["LARNIX_NB_BUDGET_S"] = "0.0"
        try:
            path = make_companion(self.tmp.name, [_code_cell("c1", "x = 1")])
            ok, err = rn.run_ipynb(path, scaled=True)
            self.assertFalse(ok)
            self.assertIn("budget", err)
            self.assertIn("parameters cell", err)
        finally:
            del os.environ["LARNIX_NB_BUDGET_S"]

    def test_budget_env_override_and_default(self):
        self.assertEqual(rn.budget_s(), 90.0)
        os.environ["LARNIX_NB_BUDGET_S"] = "120"
        try:
            self.assertEqual(rn.budget_s(), 120.0)
        finally:
            del os.environ["LARNIX_NB_BUDGET_S"]

    def test_main_reports_companion_scaled(self):
        import contextlib
        import io

        path = make_companion(self.tmp.name, [_code_cell("c1", "x = 1")])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = rn.main([path])
        self.assertEqual(rc, 0)
        self.assertIn("companion, CPU-scaled", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
