#!/usr/bin/env python3
"""Unit tests for the Colab companion generator (infra/ci/make_colab.py, P2-D8).

Run:  cd infra/ci && python3 -m unittest test_make_colab -v
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import make_colab  # noqa: E402

# A minimal colab chapter exercising every extraction rule: a worked cell, a
# setup cell (dropped), a display-only cell (skipped), the parameters cell, an
# auto-graded exercise (+ hint + solution), and a rubric exercise.
SAMPLE_QMD = '''---
title: "Sample colab chapter"
module: "M9 — Test"
chapter: 12
difficulty: "intermediate"
prereqs: []
learning_objectives:
  - "Train a thing"
compute: "colab"
status: "stable"
last_reviewed: "2026-07-19"
est_minutes: 30
torch-floor: "2.4"
---

## Setup

```{.python setup="true"}
from lib.grader import run_tests
```

## Parameters

```{.python parameters="true"}
import os
CI = bool(os.environ.get("LARNIX_CI"))
EPOCHS = 1 if CI else 5
N_SAMPLES = 2000 if CI else None
```

## Worked

::: {.companion-prose}
### Warm up the tensors

One line of narration that should travel into the notebook.
:::

```{.python}
import torch
x = torch.ones(3)
print(x.sum())
```

Display only (a shell command the learner types, not a cell):

```{.python companion="false"}
nvidia-smi
```

## Practice

```{.python exercise="ex_train"}
def train_step(w, lr):
    return ____  # TODO

w_after = train_step(1.0, 0.1)
run_tests([
    ("moved", w_after != 1.0, True),
])
```

<details><summary>If you're stuck</summary>

Think about gradients.
</details>

<details><summary>Show solution</summary>

```python
def train_step(w, lr):
    return w - lr * 2 * w

w_after = train_step(1.0, 0.1)
run_tests([
    ("moved", w_after != 1.0, True),
])
```

</details>

### Stretch

```{.python exercise="ex_stretch"}
# Tune the LR to beat the target (rubric-graded).
lr = 0.1
```

<details><summary>Show one possible solution</summary>

```python
lr = 0.03
```

</details>
'''


def write_chapter(tmp, text=SAMPLE_QMD, name="ch12-sample.qmd"):
    p = Path(tmp) / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def nb_cells(qmd_path):
    nb = make_colab.build_notebook(qmd_path)
    return nb, {c["id"]: c for c in nb["cells"]}


class ParseTests(unittest.TestCase):
    def setUp(self):
        self.parsed = make_colab.parse_chapter(SAMPLE_QMD)
        self.by_id = {c["id"]: c for c in self.parsed["cells"]}

    def test_parameters_cell_extracted(self):
        self.assertIn("LARNIX_CI", self.parsed["parameters"])
        self.assertIn("EPOCHS = 1 if CI else 5", self.parsed["parameters"])

    def test_worked_cell_included_setup_and_display_skipped(self):
        self.assertIn("worked-1", self.by_id)
        joined = "\n".join(c.get("code", "") for c in self.parsed["cells"])
        self.assertNotIn("from lib.grader import run_tests", joined)
        self.assertNotIn("nvidia-smi", joined)

    def test_graded_exercise_paired_with_solution_not_hint(self):
        ex = self.by_id["ex-ex_train"]
        self.assertTrue(ex["graded"])
        self.assertIn("____", ex["code"])  # learner-facing starter keeps the TODO
        self.assertIn("return w - lr * 2 * w", ex["solution"])
        self.assertNotIn("Think about gradients", ex["solution"])

    def test_solution_markdown_cell_follows_exercise(self):
        ids = [c["id"] for c in self.parsed["cells"]]
        self.assertLess(ids.index("ex-ex_train"), ids.index("sol-ex_train"))

    def test_rubric_exercise_marked_ungraded(self):
        self.assertFalse(self.by_id["ex-ex_stretch"]["graded"])

    def test_missing_parameters_cell_fails_closed(self):
        qmd = SAMPLE_QMD.replace('parameters="true"', 'companion="false"')
        with self.assertRaises(ValueError) as cm:
            make_colab.parse_chapter(qmd)
        self.assertIn("parameters", str(cm.exception))

    def test_parameters_without_larnix_ci_fails_closed(self):
        qmd = SAMPLE_QMD.replace("LARNIX_CI", "SOME_OTHER_VAR")
        with self.assertRaises(ValueError) as cm:
            make_colab.parse_chapter(qmd)
        self.assertIn("LARNIX_CI", str(cm.exception))

    def test_graded_exercise_without_solution_fails_closed(self):
        qmd = SAMPLE_QMD.replace("<details><summary>Show solution</summary>", "<div>")
        qmd = qmd.replace("</details>\n\n### Stretch", "</div>\n\n### Stretch")
        with self.assertRaises(ValueError) as cm:
            make_colab.parse_chapter(qmd)
        self.assertIn("ex_train", str(cm.exception))


class NotebookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.qmd = write_chapter(self.tmp.name)
        self.nb, self.by_id = nb_cells(self.qmd)

    def tearDown(self):
        self.tmp.cleanup()

    def _src(self, cell_id):
        return "".join(self.by_id[cell_id]["source"])

    def test_frontmatter_travels_in_notebook_metadata_not_a_raw_cell(self):
        # Colab renders raw cells as "Unsupported Cell Type" above the title
        # (learner feedback 2026-07-28) — companions carry no raw cell at all.
        self.assertNotIn("frontmatter", self.by_id)
        self.assertFalse([c for c in self.nb["cells"]
                          if c["cell_type"] == "raw"])
        fm_text = self.nb["metadata"]["larnix"]["frontmatter"]
        self.assertIn('compute: "colab"', fm_text)
        self.assertIn("(Colab companion)", fm_text)

    def test_companion_prose_div_becomes_markdown_cell_in_position(self):
        cell = self.by_id["prose-1"]
        self.assertEqual(cell["cell_type"], "markdown")
        src = self._src("prose-1")
        self.assertIn("### Warm up the tensors", src)
        self.assertIn("travel into the notebook", src)
        ids = [c["id"] for c in self.nb["cells"]]
        # Document position: after the generated preamble, before the worked cell.
        self.assertLess(ids.index("grader-bootstrap"), ids.index("prose-1"))
        self.assertLess(ids.index("prose-1"), ids.index("worked-1"))

    def test_companion_prose_may_not_contain_details(self):
        text = SAMPLE_QMD.replace(
            "### Warm up the tensors",
            "<details><summary>hidden</summary>x</details>\n### Warm up the tensors",
        )
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError) as cm:
                make_colab.build_notebook(write_chapter(td, text))
        self.assertIn("companion-prose", str(cm.exception))

    def test_notebook_metadata_marks_larnix_colab(self):
        self.assertEqual(self.nb["metadata"]["larnix"]["compute"], "colab")

    def test_header_has_badge_and_do_not_edit_note(self):
        src = self._src("colab-header")
        self.assertIn("colab.research.google.com/github/", src)
        self.assertIn("ch12-sample-colab.ipynb", src)
        self.assertIn("do not edit by hand", src)

    def test_torch_guard_uses_frontmatter_floor(self):
        src = self._src("torch-guard")
        self.assertIn('_FLOOR = "2.4"', src)
        self.assertIn("torch.__version__", src)
        # The generated guard must itself be valid Python.
        compile(src, "guard", "exec")

    def test_parameters_cell_present_before_worked_cells(self):
        ids = [c["id"] for c in self.nb["cells"]]
        self.assertLess(ids.index("parameters"), ids.index("worked-1"))
        self.assertIn("LARNIX_CI", self._src("parameters"))

    def test_bootstrap_has_raw_url_and_inlined_fallback(self):
        src = self._src("grader-bootstrap")
        self.assertIn("raw.githubusercontent.com/", src)
        self.assertIn("/lib/grader.py", src)
        self.assertIn("_LARNIX_GRADER_FALLBACK = r'''", src)
        self.assertIn("def run_tests", src)      # the fallback really is the grader
        self.assertIn("def grad_check", src)     # incl. the P2-D7 property helpers
        compile(src, "bootstrap", "exec")

    def test_bootstrap_falls_back_when_fetched_grader_is_stale(self):
        """Regression (found live on Colab, 2026-07-28): the raw-URL fetch can
        SUCCEED yet return a grader too old to serve the companion's imports
        (branch skew — main's grader predated the property builders). The
        bootstrap must validate capability, not fetch success, and fall back
        to the inlined copy."""
        from unittest import mock

        src = self._src("grader-bootstrap")
        stale = b"def run_tests(*a, **k):\n    pass\n"   # no between/decreased/…

        class _Resp:
            def __enter__(self):
                return self
            def __exit__(self, *exc):
                return False
            def read(self):
                return stale

        cwd, argv_path = os.getcwd(), list(sys.path)
        saved_mods = {k: sys.modules.pop(k) for k in ("lib", "lib.grader")
                      if k in sys.modules}
        with tempfile.TemporaryDirectory() as td:
            try:
                os.chdir(td)
                sys.path.insert(0, td)
                env = {k: v for k, v in os.environ.items() if k != "LARNIX_CI"}
                with mock.patch.dict(os.environ, env, clear=True), \
                        mock.patch("urllib.request.urlopen",
                                   return_value=_Resp()):
                    import contextlib
                    import io
                    ns: dict = {}
                    with contextlib.redirect_stdout(io.StringIO()) as out:
                        exec(src, ns)                 # must not raise
                self.assertIn("inlined copy", out.getvalue())
                self.assertFalse(ns["_fetched"])       # stale copy rejected
                written = Path(td, "lib", "grader.py").read_text()
                self.assertIn("def between", written)  # fallback won
            finally:
                os.chdir(cwd)
                sys.path[:] = argv_path
                for k in ("lib", "lib.grader"):
                    sys.modules.pop(k, None)
                sys.modules.update(saved_mods)

    def test_exercise_cell_carries_solution_metadata(self):
        meta = self.by_id["ex-ex_train"]["metadata"]["larnix"]
        self.assertEqual(meta["exercise"], "ex_train")
        self.assertIn("return w - lr * 2 * w", meta["solution"])
        self.assertNotIn("rubric", meta)

    def test_rubric_exercise_flagged_for_ci_skip(self):
        meta = self.by_id["ex-ex_stretch"]["metadata"]["larnix"]
        self.assertTrue(meta["rubric"])

    def test_solution_markdown_hidden_in_details(self):
        src = self._src("sol-ex_train")
        self.assertTrue(src.startswith("<details>"))
        self.assertEqual(self.by_id["sol-ex_train"]["cell_type"], "markdown")

    def test_notebook_is_valid_json_and_deterministic(self):
        a = make_colab.notebook_text(self.qmd)
        b = make_colab.notebook_text(self.qmd)
        self.assertEqual(a, b)
        json.loads(a)

    def test_torch_chapter_without_floor_fails_closed(self):
        text = SAMPLE_QMD.replace('torch-floor: "2.4"\n', "")
        qmd = write_chapter(self.tmp.name, text, "ch13-nofloor.qmd")
        with self.assertRaises(ValueError) as cm:
            make_colab.build_notebook(qmd)
        self.assertIn("torch-floor", str(cm.exception))

    def test_no_guard_cell_for_torchless_chapter(self):
        text = SAMPLE_QMD.replace('torch-floor: "2.4"\n', "")
        text = text.replace("import torch\nx = torch.ones(3)\nprint(x.sum())",
                            "x = [1, 1, 1]\nprint(sum(x))")
        qmd = write_chapter(self.tmp.name, text, "ch14-notorch.qmd")
        _, by_id = nb_cells(qmd)
        self.assertNotIn("torch-guard", by_id)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.qmd = write_chapter(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_write_then_check_ok(self):
        self.assertEqual(make_colab.cmd_write([self.qmd]), 0)
        out = make_colab.companion_path(self.qmd)
        self.assertTrue(out.exists())
        self.assertTrue(str(out).endswith("ch12-sample-colab.ipynb"))
        self.assertEqual(make_colab.cmd_check([self.qmd]), 0)

    def test_check_fails_on_missing_companion(self):
        self.assertEqual(make_colab.cmd_check([self.qmd]), 1)

    def test_check_fails_on_drift(self):
        make_colab.cmd_write([self.qmd])
        Path(self.qmd).write_text(
            SAMPLE_QMD.replace("x = torch.ones(3)", "x = torch.ones(4)"),
            encoding="utf-8",
        )
        self.assertEqual(make_colab.cmd_check([self.qmd]), 1)

    def test_browser_chapters_ignored(self):
        text = SAMPLE_QMD.replace('compute: "colab"', 'compute: "browser"')
        qmd = write_chapter(self.tmp.name, text, "ch01-browser.qmd")
        self.assertEqual(make_colab.cmd_write([qmd]), 0)
        self.assertFalse(make_colab.companion_path(qmd).exists())

    def test_write_reports_fail_closed_errors(self):
        text = SAMPLE_QMD.replace("LARNIX_CI", "NOPE")
        qmd = write_chapter(self.tmp.name, text, "ch15-bad.qmd")
        self.assertEqual(make_colab.cmd_write([qmd]), 1)

    def test_companion_relpath_is_repo_relative_for_badge(self):
        # Badge deep-links must be repo-relative (colab.research.google.com/github/
        # OWNER/REPO/blob/BRANCH/<this>). cwd is the repo root in CI.
        rel = make_colab.companion_relpath("modules/05-deep-learning/ch12-tensors.qmd")
        self.assertEqual(rel, "modules/05-deep-learning/ch12-tensors-colab.ipynb")


if __name__ == "__main__":
    unittest.main()
