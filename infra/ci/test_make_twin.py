#!/usr/bin/env python3
"""Unit tests for the twin generator (infra/ci/make_twin.py, P1-D10).

Run:  cd infra/ci && python3 -m unittest test_make_twin -v
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import make_twin  # noqa: E402

# A minimal chapter exercising every extraction rule: a worked cell, a setup cell
# (skipped), an auto-graded exercise (+ solution), and a rubric exercise (skipped).
SAMPLE_QMD = '''---
title: "Sample"
module: "M9 — Test"
chapter: 3
difficulty: "beginner"
prereqs: []
learning_objectives:
  - "Do a thing"
compute: "browser"
status: "stable"
last_reviewed: "2026-06-28"
est_minutes: 10
resources:
  - ../../lib/grader.py
---

## Worked

```{pyodide}
#| caption: "step"
x = 2 + 2
print(x)
```

## Practice

```{pyodide}
#| setup: true
#| exercise: ex_one
from lib.grader import run_tests
```

```{pyodide}
#| exercise: ex_one
def double(n):
    return ____  # TODO

run_tests([
    ("doubles", double(3), 6),
])
```

<details><summary>Show solution</summary>

```python
def double(n):
    return n * 2
```

Because two times.
</details>

### Stretch

<details><summary>Show one possible solution</summary>

```python
print("open ended")
```

</details>
'''


class ParseTests(unittest.TestCase):
    def setUp(self):
        self.cells = make_twin.parse_chapter(SAMPLE_QMD)
        self.by_id = {c["id"]: c["code"] for c in self.cells}

    def test_worked_cell_included_without_options(self):
        self.assertIn("worked-1", self.by_id)
        self.assertEqual(self.by_id["worked-1"], "x = 2 + 2\nprint(x)")
        self.assertNotIn("#|", self.by_id["worked-1"])

    def test_setup_cell_skipped(self):
        # No twin cell should be the bare grader import (that's the bootstrap's job).
        self.assertNotIn("from lib.grader import run_tests", "\n".join(self.by_id.values()))

    def test_autograded_exercise_paired_with_solution_then_asserts(self):
        self.assertIn("ex-ex_one", self.by_id)
        code = self.by_id["ex-ex_one"]
        # Solution body comes first…
        self.assertIn("return n * 2", code)
        self.assertNotIn("____", code)
        # …then the run_tests block lifted from the exercise cell.
        self.assertIn('run_tests([', code)
        self.assertLess(code.index("return n * 2"), code.index("run_tests(["))

    def test_rubric_exercise_skipped(self):
        joined = "\n".join(self.by_id.values())
        self.assertNotIn("open ended", joined)

    def test_cell_order_worked_before_exercise(self):
        ids = [c["id"] for c in self.cells]
        self.assertLess(ids.index("worked-1"), ids.index("ex-ex_one"))


class NotebookTests(unittest.TestCase):
    def _write(self, tmp, text=SAMPLE_QMD):
        qmd = Path(tmp) / "ch.qmd"
        qmd.write_text(text, encoding="utf-8")
        return str(qmd)

    def test_frontmatter_has_ten_fields_and_twin_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            nb = make_twin.build_notebook(self._write(tmp))
        fm_src = "".join(nb["cells"][0]["source"])
        for field in make_twin.TWIN_FIELDS:
            self.assertIn(f"{field}:", fm_src)
        self.assertIn('title: "Sample (CI twin)"', fm_src)
        self.assertNotIn("resources:", fm_src)  # live-only key dropped

    def test_bootstrap_cell_present_and_single_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            nb = make_twin.build_notebook(self._write(tmp))
        boot = next(c for c in nb["cells"] if c.get("id") == "grader-bootstrap")
        src = "".join(boot["source"])
        self.assertIn("from lib.grader import run_tests", src)
        self.assertNotIn("def run_tests", src)  # imported, never pasted

    def test_generation_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            qmd = self._write(tmp)
            self.assertEqual(make_twin.notebook_text(qmd), make_twin.notebook_text(qmd))


class CheckTests(unittest.TestCase):
    def _setup(self, tmp):
        qmd = Path(tmp) / "ch.qmd"
        qmd.write_text(SAMPLE_QMD, encoding="utf-8")
        return str(qmd), Path(tmp) / "ch.ipynb"

    def test_check_passes_after_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            qmd, _ = self._setup(tmp)
            self.assertEqual(make_twin.cmd_write([qmd]), 0)
            self.assertEqual(make_twin.cmd_check([qmd]), 0)

    def test_check_detects_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            qmd, twin = self._setup(tmp)
            make_twin.cmd_write([qmd])
            twin.write_text(twin.read_text(encoding="utf-8") + "\n# tampered\n", encoding="utf-8")
            self.assertEqual(make_twin.cmd_check([qmd]), 1)

    def test_check_detects_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            qmd, twin = self._setup(tmp)
            self.assertFalse(twin.exists())
            self.assertEqual(make_twin.cmd_check([qmd]), 1)


if __name__ == "__main__":
    unittest.main()
