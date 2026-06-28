#!/usr/bin/env python3
"""Tests for the R1/R3/R6 gates (stdlib unittest)."""
import os
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import browser_import_lint as r3  # noqa: E402
import currency_check as r1  # noqa: E402
import free_fallback_check as r6  # noqa: E402

TODAY = date(2026, 6, 28)


# ── R1 currency ──────────────────────────────────────────────────────────────
class CurrencyTests(unittest.TestCase):
    def test_stable_is_exempt(self):
        fm = {"status": "stable", "last_reviewed": "2020-01-01"}
        self.assertEqual(r1.check_currency(fm, today=TODAY), [])

    def test_frontier_fresh_ok(self):
        fm = {"status": "frontier", "last_reviewed": "2026-06-01"}
        self.assertEqual(r1.check_currency(fm, today=TODAY), [])

    def test_frontier_overdue_fails(self):
        fm = {"status": "frontier", "last_reviewed": "2026-01-01"}  # ~178 days
        self.assertTrue(r1.check_currency(fm, today=TODAY))

    def test_frontier_bad_date_fails(self):
        fm = {"status": "frontier", "last_reviewed": "nope"}
        self.assertTrue(r1.check_currency(fm, today=TODAY))


# ── R3 browser imports ───────────────────────────────────────────────────────
class BrowserImportTests(unittest.TestCase):
    def test_extract_code_pyodide_and_python(self):
        text = "```{pyodide}\nimport numpy\n```\n\n```python\nimport os\n```\n```bash\nls\n```"
        code = r3.extract_code(text)
        self.assertIn("import numpy", code)
        self.assertIn("import os", code)
        self.assertNotIn("ls", code)

    def test_imported_modules_variants(self):
        code = "import numpy as np\nfrom sklearn.linear_model import X\nimport os, sys"
        mods = r3.imported_modules(code)
        self.assertEqual(mods, {"numpy", "sklearn", "os", "sys"})

    def test_safe_imports_pass(self):
        self.assertEqual(r3.check_imports({"numpy", "sklearn", "os", "math"}), [])

    def test_known_unsafe_flagged(self):
        problems = r3.check_imports({"torch"})
        self.assertTrue(problems and "torch" in problems[0])

    def test_unknown_flagged(self):
        problems = r3.check_imports({"some_random_pkg"})
        self.assertTrue(problems and "allow-list" in problems[0])

    def test_only_browser_chapters_checked(self):
        with tempfile.TemporaryDirectory() as d:
            colab = os.path.join(d, "c.qmd")
            with open(colab, "w") as fh:
                fh.write('---\ncompute: "colab"\n---\n```python\nimport torch\n```\n')
            self.assertEqual(r3.check_file(colab), [])  # not browser → skipped

    def test_browser_chapter_with_torch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "b.qmd")
            with open(p, "w") as fh:
                fh.write('---\ncompute: "browser"\n---\n```{pyodide}\nimport torch\n```\n')
            self.assertTrue(r3.check_file(p))


# ── R6 free fallback ─────────────────────────────────────────────────────────
class FreeFallbackTests(unittest.TestCase):
    def test_no_paid_marker_ok(self):
        self.assertEqual(r6.check_text("Just scikit-learn here."), [])

    def test_paid_without_fallback_fails(self):
        self.assertTrue(r6.check_text("Set OPENAI_API_KEY and call openai.chat()."))

    def test_paid_with_ollama_fallback_ok(self):
        self.assertEqual(
            r6.check_text("Use openai with OPENAI_API_KEY. Free fallback: run Ollama locally."),
            [],
        )


if __name__ == "__main__":
    unittest.main()
