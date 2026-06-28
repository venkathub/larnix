#!/usr/bin/env python3
"""Unit tests for the Varsity-contract structure gate.

Run:  cd infra/ci && python3 -m unittest test_chapter_structure_lint -v
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import chapter_structure_lint as cs  # noqa: E402

GOOD = """\
---
compute: "browser"
---

## Build it

```{pyodide}
print("hi")
```

::: {.key-takeaways}
### Key Takeaways
1. A point.
:::

## Practice

```{pyodide}
#| exercise: ex1
run_tests([("ok", 1, 1)])
```

<details><summary>Show solution</summary>

```python
1
```
</details>
"""


class CheckTextTests(unittest.TestCase):
    def test_complete_chapter_passes(self):
        self.assertEqual(cs.check_text(GOOD), [])

    def test_missing_key_takeaways(self):
        text = GOOD.replace("::: {.key-takeaways}", "::: {.note}")
        self.assertTrue(any("Key Takeaways" in p for p in cs.check_text(text)))

    def test_missing_pyodide_cell(self):
        text = GOOD.replace("{pyodide}", "{python}")
        self.assertTrue(any("runnable" in p for p in cs.check_text(text)))

    def test_missing_hidden_solution(self):
        text = GOOD.replace("<details>", "<div>")
        self.assertTrue(any("hidden-solution" in p for p in cs.check_text(text)))


class ChapterDetectionTests(unittest.TestCase):
    def _write(self, d, name, body):
        p = Path(d) / name
        p.write_text(body, encoding="utf-8")
        return str(p)

    def test_non_chapter_qmd_skipped(self):
        # A landing page without `compute:` is not a chapter → not checked.
        with tempfile.TemporaryDirectory() as d:
            p = self._write(d, "index.qmd", "---\ntitle: \"M0\"\n---\n# Landing\n")
            self.assertFalse(cs.is_chapter(p))
            self.assertEqual(cs.check_file(p), [])

    def test_ipynb_twin_not_a_chapter(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write(d, "ch.ipynb", "{}")
            self.assertFalse(cs.is_chapter(p))

    def test_chapter_with_compute_is_checked(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write(d, "ch.qmd", "---\ncompute: \"browser\"\n---\n# bare\n")
            self.assertTrue(cs.is_chapter(p))
            self.assertTrue(cs.check_file(p))  # bare chapter fails all pillars

    def test_main_passes_on_good_chapter(self):
        with tempfile.TemporaryDirectory() as d:
            self._write(d, "ch.qmd", GOOD)
            self.assertEqual(cs.main([os.path.join(d, "ch.qmd")]), 0)

    def test_main_fails_on_bad_chapter(self):
        with tempfile.TemporaryDirectory() as d:
            self._write(d, "ch.qmd", "---\ncompute: \"browser\"\n---\n# bare\n")
            self.assertEqual(cs.main([os.path.join(d, "ch.qmd")]), 1)


if __name__ == "__main__":
    unittest.main()
