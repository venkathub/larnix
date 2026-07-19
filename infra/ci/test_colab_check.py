#!/usr/bin/env python3
"""Unit tests for the colab-policy gate (infra/ci/colab_check.py, P2 §5.3).

Run:  cd infra/ci && python3 -m unittest test_colab_check -v
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import colab_check  # noqa: E402
import make_colab  # noqa: E402
from test_make_colab import SAMPLE_QMD  # noqa: E402  (the shared colab fixture)


def chapter_with_button(qmd_rel: str) -> str:
    """SAMPLE_QMD plus a correctly-pointed colab button."""
    rel = make_colab.companion_relpath(qmd_rel)
    return SAMPLE_QMD + f"\n{{{{< colab {rel} >}}}}\n"


class ColabCheckTests(unittest.TestCase):
    """All tests run with cwd = a temp 'repo root' so repo-relative paths hold."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.prev_cwd = os.getcwd()
        os.chdir(self.tmp.name)
        os.makedirs("modules/09-test")
        self.qmd = "modules/09-test/ch12-sample.qmd"

    def tearDown(self):
        os.chdir(self.prev_cwd)
        self.tmp.cleanup()

    def write_valid_pair(self):
        Path(self.qmd).write_text(chapter_with_button(self.qmd), encoding="utf-8")
        assert make_colab.cmd_write([self.qmd]) == 0

    def test_valid_chapter_passes(self):
        self.write_valid_pair()
        self.assertEqual(colab_check.check_chapter(self.qmd), [])
        self.assertEqual(colab_check.main([self.qmd]), 0)

    def test_missing_button_fails(self):
        Path(self.qmd).write_text(SAMPLE_QMD, encoding="utf-8")
        make_colab.cmd_write([self.qmd])
        errs = colab_check.check_chapter(self.qmd)
        self.assertTrue(any("exactly one" in e for e in errs))

    def test_wrong_button_path_fails(self):
        text = SAMPLE_QMD + "\n{{< colab modules/09-test/wrong.ipynb >}}\n"
        Path(self.qmd).write_text(text, encoding="utf-8")
        make_colab.cmd_write([self.qmd])
        errs = colab_check.check_chapter(self.qmd)
        self.assertTrue(any("expected the generated companion" in e for e in errs))

    def test_missing_companion_fails(self):
        Path(self.qmd).write_text(chapter_with_button(self.qmd), encoding="utf-8")
        errs = colab_check.check_chapter(self.qmd)
        self.assertTrue(any("missing" in e for e in errs))

    def test_drifted_companion_fails(self):
        self.write_valid_pair()
        # Edit the chapter after generation → companion no longer matches.
        Path(self.qmd).write_text(
            chapter_with_button(self.qmd).replace("x = torch.ones(3)",
                                                  "x = torch.ones(4)"),
            encoding="utf-8",
        )
        errs = colab_check.check_chapter(self.qmd)
        self.assertTrue(any("drifted" in e for e in errs))

    def test_hand_stripped_parameters_cell_fails(self):
        self.write_valid_pair()
        companion = make_colab.companion_path(self.qmd)
        nb = json.loads(companion.read_text(encoding="utf-8"))
        nb["cells"] = [c for c in nb["cells"] if c.get("id") != "parameters"]
        companion.write_text(json.dumps(nb), encoding="utf-8")
        errs = colab_check.check_chapter(self.qmd)
        self.assertTrue(any("LARNIX_CI parameters cell" in e for e in errs))

    def test_hand_stripped_torch_guard_fails(self):
        self.write_valid_pair()
        companion = make_colab.companion_path(self.qmd)
        nb = json.loads(companion.read_text(encoding="utf-8"))
        nb["cells"] = [c for c in nb["cells"] if c.get("id") != "torch-guard"]
        companion.write_text(json.dumps(nb), encoding="utf-8")
        errs = colab_check.check_chapter(self.qmd)
        self.assertTrue(any("version-floor guard" in e for e in errs))

    def test_browser_chapter_with_button_fails(self):
        text = chapter_with_button(self.qmd).replace(
            'compute: "colab"', 'compute: "browser"'
        )
        Path(self.qmd).write_text(text, encoding="utf-8")
        errs = colab_check.check_chapter(self.qmd)
        self.assertTrue(any("non-colab" in e for e in errs))

    def test_browser_chapter_without_button_passes(self):
        text = SAMPLE_QMD.replace('compute: "colab"', 'compute: "browser"')
        Path(self.qmd).write_text(text, encoding="utf-8")
        self.assertEqual(colab_check.check_chapter(self.qmd), [])

    def test_main_aggregates_multiple_chapters(self):
        self.write_valid_pair()
        bad = "modules/09-test/ch13-bad.qmd"
        Path(bad).write_text(SAMPLE_QMD, encoding="utf-8")  # colab, no button
        make_colab.cmd_write([bad])
        import contextlib
        import io

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = colab_check.main([self.qmd, bad])
        self.assertEqual(rc, 1)
        self.assertIn("OK   " + self.qmd, buf.getvalue())
        self.assertIn("violation", buf.getvalue())

    def test_no_chapters_is_green(self):
        rc = colab_check.main(["modules/__missing__/**/*.qmd"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
