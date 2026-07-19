# infra/ci — Larnix CI gate scripts

Small, testable Python scripts that enforce the Larnix content contract in CI
(per `DECISIONS.md D0006`, P0-D10). Each has a unit test and is invoked by the
GitHub Actions workflows.

| Script | Gate | What it checks |
|--------|------|----------------|
| `frontmatter_lint.py` | Front-matter schema (P0 task 4) | The 10 required chapter fields, enum values, date format/non-future, types. |
| `quiz_lint.py` | Quiz schema (P0 task 7) | `quiz.yml` structure: questions, prompts, ≥2 options, in-range integer `answer`, unique ids. |
| `run_notebooks.py` | R10 — runs in CI (P0 task 8; extended P2-D9) | Executes `modules/**/*.ipynb` with `nbclient`; any cell error fails. **Generated Colab companions** (notebook metadata `larnix.generated_by`) execute **CPU-scaled**: `LARNIX_CI=1` exported to the kernel, exercise starters replaced by their `metadata.larnix.solution`, rubric cells dropped, and a wall-clock budget enforced (`LARNIX_NB_BUDGET_S`, default 90 s — over-budget fails with a "shrink your parameters cell" message). Hand-authored GPU/`colab` notebooks (front-matter `compute: colab\|gpu` or `larnix.compute`/`ci:false`, no `generated_by`) are still **skipped** — manually Colab-verified (D0012). `fixtures/` holds pass/fail test notebooks. |
| `a11y_check.py` | a11y — alt-text + contrast (P0 task 10, P0-D11) | Non-empty alt text on content images; WCAG AA contrast on declared theme colour pairs. Stdlib-only; deterministic (no browser). Full page-level axe/pa11y scanning is deferred. |
| `currency_check.py` | R1 (P0 task 11) | `status: frontier` chapters must have `last_reviewed` within 90 days; `stable` exempt. |
| `browser_import_lint.py` | R3 (P0 task 11; hardened P1-D7) | `compute: browser` chapters may import only Pyodide-safe packages (stdlib + curated allow-list incl. `lib`; known-unsafe denylist). Fail-closed: unknown imports fail. A pure-Python package installed at runtime must be declared with a `# micropip: <name>` annotation (which never overrides the known-unsafe denylist). |
| `free_fallback_check.py` | R6 (P0 task 11) | Chapters referencing a paid API must also show a free fallback (Ollama/Groq/free tier). |
| `review_cards_lint.py` | SR seeding (P0 task 13, P0-D3) | Validates the optional `review_cards:` front-matter block (Q/A pairs from Key Takeaways). |
| `make_twin.py` | Twin drift (P1-D10 / D0016) | **Generates** each browser chapter's CI twin `.ipynb` from its `.qmd` (worked-example cells + a grader bootstrap + per-exercise `<details>` solution + asserts) and, in `--check` mode, fails if a committed twin drifts from source. |
| `make_colab.py` | Companion drift (P2-D8 / D0020) | **Generates** each `compute: colab` chapter's learner-facing companion `<stem>-colab.ipynb` from its `.qmd` (header + badge, torch version-floor guard (P2-D11), `LARNIX_CI` parameters cell (P2-D9), grader bootstrap with inlined fallback, worked/exercise cells with `<details>` solutions and per-cell solution metadata) and, in `--check` mode, fails on drift. **Fail-closed:** missing/`LARNIX_CI`-less parameters cell, torch without `torch-floor:` front-matter, or a graded exercise without a solution are build errors. |

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
`infra/ci/requirements-notebooks.txt` (nbclient, ipykernel, the twin runtime
deps, and — for the P2-D9 companion tier — **exact-pinned CPU-only
torch/torchvision** from the official `download.pytorch.org/whl/cpu` index)
for R10.

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
- **Colab companions are generated too (P2-D8):** a `compute: colab` chapter is a
  rendered `.qmd` (prose + code with *recorded* outputs; nothing executes at
  render — the render gate installs no Jupyter) plus a generated companion
  `<stem>-colab.ipynb` that the `{{< colab >}}` button opens. Companion-bound
  code lives in **Pandoc-attribute fences**, which render highlighted with the
  attributes invisible to the learner:

  ````markdown
  ```{.python}                     → worked cell, copied in document order
  ```{.python setup="true"}        → dropped (the generated grader bootstrap replaces it)
  ```{.python companion="false"}   → display-only, never copied
  ```{.python parameters="true"}   → the LARNIX_CI parameters cell (exactly one; P2-D9)
  ```{.python exercise="ex_id"}    → exercise starter, paired with the next <details> solution
  ````

  Plain ```` ```python ```` fences (e.g. inside `<details>` solutions) are prose,
  never cells. Regenerate with `python infra/ci/make_colab.py --write
  <chapter.qmd>`; CI runs `--check`. The grader bootstrap fetches
  `lib/grader.py` from the repo raw URL (Colab is online) with an **inlined
  fallback embedded at generation time** — so a grader change drifts every
  companion and the gate forces regeneration; under `LARNIX_CI` the fetch is
  skipped entirely (offline-deterministic). Exercise cells carry
  `metadata.larnix.solution` (rubric exercises: `metadata.larnix.rubric`) — the
  contract the CPU-scaled CI runner (P2-D9) uses to substitute solutions.
  Repo/branch for badge + raw URLs come from `_quarto.yml`
  `larnix-colab-repo/-branch` (env `LARNIX_COLAB_REPO/BRANCH` fallback — never
  hardcoded). Note: the badge and raw URL point at the deploy branch, so they
  resolve **after merge** (same as the P0 shortcode, D0012); pre-merge
  verification is the recorded manual Colab run.
- **R10 for `compute: colab` chapters (P2-D9):** CI executes each *generated*
  companion **CPU-scaled** — `run_notebooks.py` exports `LARNIX_CI=1` (the
  parameters cell switches to tiny epochs/subsets), substitutes each exercise's
  `metadata.larnix.solution`, drops rubric cells, and fails if the notebook
  exceeds the wall-clock budget (`LARNIX_NB_BUDGET_S`, default 90 s). This keeps
  "everything runs" automated for the colab tier; the **recorded manual Colab
  run per chapter (D0012) is still required** for the real-GPU/full-scale path
  and calibrates the P2-D7 property thresholds.
