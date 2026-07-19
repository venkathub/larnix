#!/usr/bin/env python3
"""Tests for the deterministic a11y gate (stdlib unittest)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a11y_check as a  # noqa: E402


class ContrastMathTests(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertAlmostEqual(a.contrast_ratio("#000000", "#ffffff"), 21.0, places=1)

    def test_same_colour_is_1(self):
        self.assertAlmostEqual(a.contrast_ratio("#777777", "#777777"), 1.0, places=3)

    def test_symmetric(self):
        self.assertAlmostEqual(
            a.contrast_ratio("#0b6e6e", "#ffffff"),
            a.contrast_ratio("#ffffff", "#0b6e6e"),
            places=6,
        )

    def test_blend_extremes(self):
        self.assertEqual(a.blend((255, 255, 255, 1.0), "#000000"), "#ffffff")
        self.assertEqual(a.blend((255, 255, 255, 0.0), "#000000"), "#000000")


class ThemeContrastTests(unittest.TestCase):
    def test_all_declared_pairs_pass_AA(self):
        failures = a.check_contrast()
        self.assertEqual(failures, [], msg=f"theme pairs below AA: {failures}")

    def test_detects_a_failing_pair(self):
        # A near-white-on-white pair must be flagged at AA.
        original = a.THEME_PAIRS
        try:
            a.THEME_PAIRS = [("bad pair", "#fefefe", "#ffffff")]
            self.assertTrue(a.check_contrast())
        finally:
            a.THEME_PAIRS = original


class AltTextTests(unittest.TestCase):
    def test_markdown_empty_alt_flagged(self):
        self.assertEqual(a.check_alt_text_in_text("![](chart.png)"), ["chart.png"])

    def test_markdown_with_alt_ok(self):
        self.assertEqual(a.check_alt_text_in_text("![A bar chart](chart.png)"), [])

    def test_html_img_no_alt_flagged(self):
        probs = a.check_alt_text_in_text('<img src="x.png">')
        self.assertEqual(probs, ["x.png"])

    def test_html_img_empty_alt_flagged(self):
        probs = a.check_alt_text_in_text('<img src="x.png" alt="">')
        self.assertEqual(probs, ["x.png"])

    def test_html_img_with_alt_ok(self):
        self.assertEqual(a.check_alt_text_in_text('<img src="x.png" alt="A diagram">'), [])

    def test_check_alt_text_on_file(self):
        with tempfile.TemporaryDirectory() as d:
            good = os.path.join(d, "good.qmd")
            bad = os.path.join(d, "bad.qmd")
            with open(good, "w") as fh:
                fh.write("![A labelled diagram](d.png)\n")
            with open(bad, "w") as fh:
                fh.write("![](d.png)\n")
            self.assertEqual(a.check_alt_text([good]), [])
            self.assertEqual(len(a.check_alt_text([bad])), 1)


class ScssSyncTests(unittest.TestCase):
    """SCSS ↔ THEME_PAIRS drift detection (review 2026-07-19 / D0017)."""

    PAIRS_SRC = 'THEME_PAIRS = [\n    ("x", "#0c5f57", "#d4f3ee"),\n]\n'

    def test_current_repo_state_is_in_sync(self):
        repo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
        files = [os.path.join(repo, p) for p in a.THEME_SCSS_FILES]
        self.assertEqual(a.run_scss_sync(files), [])

    def test_orphaned_pair_colour_fails(self):
        scss = ":root { --clay-teal-bg: #d4f3ee; --clay-teal-tx: #0c5f57; }"
        src = 'THEME_PAIRS = [\n    ("x", "#0c5f57", "#d4f3ee"),\n    ("gone", "#123456", "#d4f3ee"),\n]\n'
        fails = a.check_scss_sync(scss, src)
        self.assertTrue(any("#123456" in f and "stale pair" in f for f in fails), fails)

    def test_ungated_clay_pair_fails(self):
        scss = (":root { --clay-teal-bg: #d4f3ee; --clay-teal-tx: #0c5f57;"
                " --clay-new-bg: #eeeeee; --clay-new-tx: #111111; }")
        # 'new' is declared in SCSS but the pairs block doesn't gate it. Its
        # hexes must not trip the orphan check, so include them as literals.
        src = ('THEME_PAIRS = [\n    ("x", "#0c5f57", "#d4f3ee"),\n'
               '    # seen: #eeeeee #111111\n]\n')
        fails = a.check_scss_sync(scss, src)
        self.assertTrue(any("clay pair 'new'" in f for f in fails), fails)

    def test_ungated_badge_fails(self):
        # NB: colours chosen to NOT match any real THEME_PAIRS combo.
        scss = ".badge-shiny { background: #e7f4eb; color: #145232; border-color: #bfe3c9; }"
        src = 'THEME_PAIRS = [\n    ("x", "#0c5f57", "#d4f3ee"),\n    # #e7f4eb #145232 #bfe3c9\n]\n'
        fails = a.check_scss_sync(scss, src)
        self.assertTrue(any("badge 'shiny'" in f for f in fails), fails)

    def test_gated_state_passes(self):
        scss = (":root { --clay-teal-bg: #d4f3ee; --clay-teal-tx: #0c5f57; }\n"
                ".badge-b { background: #d4f3ee; color: #0c5f57; }")
        fails = a.check_scss_sync(scss, self.PAIRS_SRC)
        self.assertEqual(fails, [])


if __name__ == "__main__":
    unittest.main()
