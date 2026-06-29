# infra/ci — Larnix CI gate scripts

Small, testable Python scripts that enforce the Larnix content contract in CI
(per `DECISIONS.md D0006`, P0-D10). Each has a unit test and is invoked by the
GitHub Actions workflows.

| Script | Gate | What it checks |
|--------|------|----------------|
| `frontmatter_lint.py` | Front-matter schema (P0 task 4) | The 10 required chapter fields, enum values, date format/non-future, types. |
| `quiz_lint.py` | Quiz schema (P0 task 7) | `quiz.yml` structure: questions, prompts, ≥2 options, in-range integer `answer`, unique ids. |
| `run_notebooks.py` | R10 — runs in CI (P0 task 8) | Executes `modules/**/*.ipynb` with `nbclient`; any cell error fails. **Skips** GPU/`colab` notebooks (front-matter `compute: colab\|gpu` or notebook metadata `larnix.compute`/`ci:false`) — those are manually Colab-verified (D0012). `fixtures/` holds pass/fail test notebooks. |
| `a11y_check.py` | a11y — alt-text + contrast (P0 task 10, P0-D11) | Non-empty alt text on content images; WCAG AA contrast on declared theme colour pairs. Stdlib-only; deterministic (no browser). Full page-level axe/pa11y scanning is deferred. |
| `currency_check.py` | R1 (P0 task 11) | `status: frontier` chapters must have `last_reviewed` within 90 days; `stable` exempt. |
| `browser_import_lint.py` | R3 (P0 task 11; hardened P1-D7) | `compute: browser` chapters may import only Pyodide-safe packages (stdlib + curated allow-list incl. `lib`; known-unsafe denylist). Fail-closed: unknown imports fail. A pure-Python package installed at runtime must be declared with a `# micropip: <name>` annotation (which never overrides the known-unsafe denylist). |
| `free_fallback_check.py` | R6 (P0 task 11) | Chapters referencing a paid API must also show a free fallback (Ollama/Groq/free tier). |
| `review_cards_lint.py` | SR seeding (P0 task 13, P0-D3) | Validates the optional `review_cards:` front-matter block (Q/A pairs from Key Takeaways). |
| `make_twin.py` | Twin drift (P1-D10 / D0016) | **Generates** each browser chapter's CI twin `.ipynb` from its `.qmd` (worked-example cells + a grader bootstrap + per-exercise `<details>` solution + asserts) and, in `--check` mode, fails if a committed twin drifts from source. |

## Run locally

```bash
# Lint chapter front-matter (defaults to modules/**/*.qmd|ipynb; or pass paths)
python3 infra/ci/frontmatter_lint.py
python3 infra/ci/frontmatter_lint.py path/to/chapter.qmd

# Schema-linter unit tests (stdlib unittest; PyYAML only)
cd infra/ci && python3 -m unittest test_frontmatter_lint test_quiz_lint -v
```

The **R10 notebook gate** needs a Jupyter kernel, so it runs in its own venv/CI
job:

```bash
python3 -m venv .nbenv && . .nbenv/bin/activate
pip install -r infra/ci/requirements-notebooks.txt
python -m ipykernel install --user --name python3
cd infra/ci && python -m unittest test_run_notebooks -v   # gate self-tests
python infra/ci/run_notebooks.py                          # execute modules/**/*.ipynb
```

Dependencies: `infra/ci/requirements.txt` (PyYAML) for the schema linters;
`infra/ci/requirements-notebooks.txt` (nbclient, ipykernel) for R10.

## Conventions

- Each script exposes a pure `validate_*`/`check_*` function (no I/O) plus a thin
  CLI `main(argv) -> int`. Exit `0` = pass (or nothing to check), `1` = failure.
- "Nothing to check" (no matching files) exits `0` so the gate is green before
  content exists, and automatically covers chapters once they land.
- Unknown extra front-matter keys are allowed (forward-compatible with
  `review_cards:` etc.).
- **R10 for `compute: browser` chapters (D0010):** their `{pyodide}` cells run
  client-side and are not executed by a headless render, so each browser chapter
  ships a companion **executable twin** `.ipynb` under `modules/` (the worked
  example + exercise solutions + grader asserts). `run_notebooks.py` executes it,
  giving R10 real teeth; the `.qmd` provides the interactive in-browser UX.
- **Twins are generated, not hand-written (P1-D10):** derive/refresh a twin with
  `python infra/ci/make_twin.py --write <chapter.qmd>` (omit the path to do all
  browser chapters) and commit it. CI runs `make_twin.py --check` to fail on drift,
  so a chapter edit that isn't reflected in its twin is caught at PR time.
