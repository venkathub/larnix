# infra/ci — Larnix CI gate scripts

Small, testable Python scripts that enforce the Larnix content contract in CI
(per `DECISIONS.md D0006`, P0-D10). Each has a unit test and is invoked by the
GitHub Actions workflows.

| Script | Gate | What it checks |
|--------|------|----------------|
| `frontmatter_lint.py` | Front-matter schema (P0 task 4) | The 10 required chapter fields, enum values, date format/non-future, types. |
| `quiz_lint.py` | Quiz schema (P0 task 7) | `quiz.yml` structure: questions, prompts, ≥2 options, in-range integer `answer`, unique ids. |
| _(later)_ `currency_check.py` | R1 (task 11) | `status: frontier` chapters reviewed within 90 days. |
| _(later)_ `browser_import_lint.py` | R3 (task 11) | `compute: browser` chapters import only Pyodide-safe packages. |
| _(later)_ `free_fallback_check.py` | R6 (task 11) | Paid-API lessons ship a free fallback. |

## Run locally

```bash
# Lint chapter front-matter (defaults to modules/**/*.qmd|ipynb; or pass paths)
python3 infra/ci/frontmatter_lint.py
python3 infra/ci/frontmatter_lint.py path/to/chapter.qmd

# Unit tests (stdlib unittest; also pytest-discoverable)
cd infra/ci && python3 -m unittest -v
```

Dependencies: `pip install -r infra/ci/requirements.txt` (PyYAML only).

## Conventions

- Each script exposes a pure `validate_*`/`check_*` function (no I/O) plus a thin
  CLI `main(argv) -> int`. Exit `0` = pass (or nothing to check), `1` = failure.
- "Nothing to check" (no matching files) exits `0` so the gate is green before
  content exists, and automatically covers chapters once they land.
- Unknown extra front-matter keys are allowed (forward-compatible with
  `review_cards:` etc.).
