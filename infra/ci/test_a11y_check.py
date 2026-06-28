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


if __name__ == "__main__":
    unittest.main()
