# Decisions

> Dated log of pedagogical & technical choices (options considered + rationale).
> Newest entries first. Each entry: context, options considered, decision, rationale, consequences.

---

## D0016 — P1 technical decisions (env-chapter proxy, plotting, datasets, grader, twins, quizzes)

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** Grooming Phase **P1 — Foundations track (M0–M3)** (`docs/phases/P1_SPEC.md §3`). The
  technical choices needed to author ~50 in-browser chapters at scale without regressing the P0
  gates. Every load-bearing claim was web-validated 2026-06-28 (`P1_SPEC.md §9`).
- **Decisions (P1-Dn → chosen option).**
  1. **P1-D6 = A — environment/tooling chapters stay `browser`-conceptual.** Pyodide cannot run
     `pip`/`venv`/a real IDE, yet the Varsity contract requires a runnable example. M1 Ch13–14
     (venv/pip, IDE/Colab) and M3 Ch11–12 (notebooks, environments) ship a **runnable in-scope
     proxy** (e.g. `micropip` as the Pyodide analogue of pip; inspect `sys.path`) plus a **recorded,
     copy-paste shell transcript** for the real local commands. Keeps P1 **Colab-free** (a phase
     non-goal). *Rejected:* tagging them `colab` (introduces Colab into P1); pure prose with a lint
     exception (special-cases the "every chapter runs" gate).
  2. **P1-D7 = A — Matplotlib-only for M3 plotting.** Matplotlib is **built into Pyodide**
     (zero-install, offline, ₹0). Seaborn is shown as an optional `🔬` "install it yourself" note.
     Web search (§9) **retired** the earlier "Seaborn may have no Pyodide wheel" risk — Seaborn is
     pure-Python and `micropip`-installable; the recommendation now rests on **offline/zero-install**,
     not capability. *Rejected:* Matplotlib+Seaborn by default (adds a first-use network download,
     breaks the offline promise); Plotly (different mental model, not what M4+ assumes).
  3. **P1-D8 = A — vendor small CSVs in-repo + a `lib/data.py` loader.** Each ≤~50 KB; Palmer
     Penguins shipped as a vendored CSV (CC0 1.0, verified §9); sklearn `load_*` built-ins used where
     they exist (Iris). Deterministic + offline-friendly + CI-twin-safe; licenses logged in
     `docs/ASSETS.md` (R11). *Rejected:* runtime URL fetch (needs internet, flaky in CI, R13);
     all-synthetic (M3 EDA must use real data to be honest).
  4. **P1-D9 = A — single-source the grader via quarto-live `resources:`.** Load `lib/grader.py`
     into the Pyodide VFS once (the `resources:` front-matter key, confirmed in §9) instead of
     pasting the helper into ~50 chapters; CPython `lib/test_grader.py` stays the off-browser
     evidence (D0009). *Rejected:* per-chapter paste (50× duplication; bug = 50 edits); pip/micropip
     package (over-engineered for one file).
  5. **P1-D10 = A — generate the CI twin notebooks.** `infra/ci/make_twin.py` extracts tagged
     `{pyodide}` cells + exercise solutions from each `.qmd` into its CPython twin (R10), with a CI
     check that the committed twin matches source (no silent drift). *Rejected:* hand-authoring 49
     twins (drift risk — the exact future improvement D0010 flagged); headless-browser smoke test
     (slow/flaky, rejected for P0 too).
  6. **P1-D11 = A — per-chapter quick check + cumulative module quiz.** Each chapter gets a 2–3-MCQ
     quick check (`quiz.yml`); each module gets a `module-quiz.yml` (~8–12 MCQ) on the README,
     rendered/scored by the P0 JS engine. *Rejected:* single end-of-module quiz only (loses recall
     checks, R12); per-chapter only (breaks the Varsity end-of-module-quiz → cert model + per-module
     DoD).
- **Rationale.** Each choice keeps P1 **₹0/offline/browser**, correct-in-CI, and maintainable across
  ~50 chapters (R9), reusing the proven P0 platform rather than adding subsystems.
- **Consequences.** New shared tooling lands before content scale (`P1_SPEC.md §6.A`): grader VFS
  loading, `make_twin.py`, module-quiz support, an extended `browser_import_lint.py` Pyodide-safe
  allow-list (with a `# micropip:` annotation for runtime-installed packages), `lib/data.py` +
  vendored CSVs, and `docs/ASSETS.md` + `assets_check.py` (R11). Seaborn-by-default and runtime
  dataset fetching are explicitly **not** adopted in P1.
- **Implementation note — P1-D9 grader single-source (Task 1, 2026-06-28; verified in-browser).**
  The mechanism is confirmed end-to-end on M0 Ch1 (Docker-rendered `live-html`, driven with
  Playwright on a real Pyodide runtime):
  - Add the helper to the page front-matter: `resources: [ ../../lib/grader.py ]` (path relative to
    the chapter). Quarto copies it to `_site/lib/grader.py`; quarto-live fetches it and writes it to
    the Pyodide VFS. `collapsePath` normalises `../../lib/grader.py` → it lands at
    `/home/pyodide/lib/grader.py`. `''` (cwd) is on `sys.path`, so the import is
    **`from lib.grader import run_tests`** (namespace package; no `__init__.py` needed).
  - **Each `#| exercise:` widget runs in its own isolated environment** (`exercise-env-<id>`), which
    a global/`autorun` cell does **not** reach. So the grader is injected per exercise with a
    `#| setup: true` + `#| exercise: <id>` cell containing the one-line import. Logic stays
    single-sourced in `lib/grader.py`; only the import line repeats (one per exercise).
  - R3 (`browser_import_lint.py`) now allow-lists `lib` so `from lib.grader …` passes; the broader
    fail-closed R3 hardening remains Task 4. CPython `lib/test_grader.py` (6 tests) stays the
    off-browser evidence.
- **Implementation note — P1-D10 twin generator (Task 2, 2026-06-28).** `infra/ci/make_twin.py`
  derives each browser chapter's CI twin from its `.qmd`: worked-example `{pyodide}` cells verbatim,
  a grader-bootstrap cell (locates `lib/grader.py`, imports `run_tests` — single-sourced off-browser
  too), then, per auto-graded exercise, the hidden `<details>` solution + the `run_tests(...)` block
  lifted from the exercise cell. `setup:` cells and rubric/stretch exercises (no `run_tests`) are
  skipped. `--write` regenerates twins; `--check` (wired into CI before R10 execution) fails on drift.
  Output is byte-deterministic so the check is stable. Authoring rule this imposes: a hidden solution
  must be a runnable cell given the cells above it. The M0 Ch1 twin was migrated to the generated
  form (its pasted grader removed) and executes clean under `run_notebooks.py`.
- **Implementation note — P1-D11 module quizzes (Task 3, 2026-06-28; verified in-browser).** The P0
  quiz engine needs no changes: the `{{< quiz FILE >}}` shortcode is path-agnostic, so a module quiz
  mounts with `{{< quiz module-quiz.yml >}}`. Two artifacts share the schema — per-chapter `quiz.yml`
  (2–3 MCQ) and a cumulative `modules/<NN>/module-quiz.yml` (~8–12 MCQ). `quiz_lint.py` now globs
  `module-quiz.yml` and emits an advisory (non-fatal) NOTE when a module quiz is outside the band.
  **Mount location = a rendered module landing `modules/<NN>/index.qmd`** (chosen over rendering the
  GitHub-facing `README.md`); the page is added to render globs + nav in Task 64, and each module's
  real `index.qmd` + `module-quiz.yml` ships with its assessment task. Proven on a staging M0 landing:
  rendered 8 questions, scored 8/8, persisted `localStorage["larnix-quiz:m0-module-quiz"]`.
- **Implementation note — R3 hardening (Task 4, 2026-06-28).** `browser_import_lint.py` is the
  load-bearing P1 gate and was already fail-closed (strict allow-list incl. `lib`; unknown imports
  fail; `KNOWN_UNSAFE` denylist for heavyweights). Added the P1-D7 guard: a pure-Python package
  installed at runtime must be declared with a `# micropip: <name>` annotation, which exempts only
  the named module and **never** rescues a `KNOWN_UNSAFE` package (e.g. an annotated `torch` still
  fails — no pure-Python wheel exists). So a bare `import seaborn`/`import torch` fails, while a
  deliberate `micropip.install("seaborn")` + `# micropip: seaborn` passes. +6 tests in `test_r_gates`.
- **Implementation note — P1-D8 datasets + R11 ledger (Task 5, 2026-06-28; verified in-browser).**
  `lib/data.py` loads `data/<name>.csv` **relative to cwd**, which resolves identically in the Pyodide
  VFS (chapter declares the CSV in `resources:`) and the CPython twin (cwd = module dir). Vendored:
  `modules/03-data/data/penguins.csv` (Palmer Penguins, **CC0-1.0 confirmed via GitHub API**, 344 rows)
  and a synthetic `modules/01-python/data/habits.csv` (CC0-by-us, 35 rows, deliberately messy for M1).
  `docs/ASSETS.md` is the license ledger; `infra/ci/assets_check.py` (R11) fails on any un-ledgered
  `data/` file. Proven in-browser: `load_csv("penguins")` returned 344×8 offline. **Authoring rule:**
  because quarto-live auto-loads only packages imported *in a cell* (not inside `lib/data.py`), a chapter
  using `load_csv` must declare `pyodide: packages: [pandas]`. `requirements-notebooks.txt` now pins
  `pandas==3.0.4` so data-chapter twins execute under R10.

---

## D0015 — P1 pedagogical decisions (M0 ordering, running examples, GenAI taste, scaffolding, granularity)

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** Grooming Phase **P1 — Foundations track (M0–M3)** (`docs/phases/P1_SPEC.md`). P1 is
  the first content-at-scale phase (~50 chapters, all 🟢→🟡, all `browser`/₹0). These are the
  pedagogical choices that shape the on-ramp; confirmed via the grooming Q&A (2026-06-28).
- **Decisions (P1-Dn → chosen option).**
  1. **P1-D1 = A — M0 is wow-first:** `1 Run a model → 2 What it costs → 3 What is AI → 4 Family tree
     (+ GenAI taste) → 5 History → 6 How this school works`. Honours "taste before theory"
     (`STYLE_GUIDE §2`), keeps the P0 sample chapter as Ch1, and still ships the ₹0 cost chapter up
     front (Ch2). *Rejected:* concept-first (demotes the strongest hook); cost-chapter-first (opens
     with logistics, not a win).
  2. **P1-D2 = A — per-module running examples:** M0 = the Iris "tell species apart" demo + the
     "Asha" persona; **M1 = a synthetic, license-free messy `habits.csv`** (we author it → full
     control of the mess for teaching cleaning); **M2 = the "assemble one neuron" thread**
     (movie-taste vectors + tip-vs-bill line); **M3 = Palmer Penguins (CC0)**, with the capstone on a
     *different* public dataset. *Rejected:* one real dataset across all of M1–M3 (can't serve both
     messy-CSV teaching and clean EDA); per-chapter ad-hoc examples (breaks `STYLE_GUIDE §4`; worse
     retention, R12).
  3. **P1-D3 = A — M0 GenAI taste via a client-side `transformers.js` widget** (sentiment/
     image-caption) in M0 Ch4: runs in-browser, no Python, no key, no Colab, ₹0 (feasibility
     confirmed §9). It is a *demo*, not a graded exercise (outside the Pyodide grader path).
     *Rejected:* classical-only M0 (under-sells "what is AI today" for a 2026 beginner); an
     Open-in-Colab HF demo (introduces Colab into P1, a non-goal).
  4. **P1-D4 = A — a small fixed scaffolding kit across all ~50 chapters:** a one-line "You'll need
     from before" recap; exercises always run guided → implement → stretch; `🧱 For Java developers`
     collapsible asides in M1; an "If you're stuck" hint before each hidden solution. Consistency aids
     retention (R12) and is partly lintable. *Rejected:* free-form scaffolding (inconsistent across
     50 chapters); heavy per-exercise sub-steps (slows confident learners; more to maintain).
  5. **P1-D5 = A — hold PLAN's chapter counts (6/14/16/14 ≈ 50) but allow ≤3 documented merges**
     where two chapters are thin (candidate pairs: M1 errors+tracebacks; M2 distributions +
     mean/variance; M3 notebooks + environments), each logged. Protects pace while keeping
     single-idea chapters. *Rejected:* hold counts exactly (some chapters pad/split awkwardly);
     aggressive consolidation to ~35 (breaks "one concept per chapter"; diverges from PLAN).
- **Rationale.** Beginner-first, analogy-before-symbol, a satisfying early win, and one running
  example per module — the Varsity pedagogy ported to a code-heavy on-ramp, tuned against drop-off
  (R12) and re-authoring cost (R9).
- **Consequences.** Drives the M0–M3 chapter design in `P1_SPEC.md §2`; the `habits.csv` and Penguins
  datasets feed P1-D8/D0016; the transformers.js widget is the only non-Pyodide runnable in P1 and is
  browser-preview-verified (not in the notebook-execution path). Any chapter merge is recorded so the
  count can drift from PLAN by a few with an audit trail.

---

## D0014 — GUI: playful claymorphism design system (Fredoka + Nunito); sepia shipped

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** A scoped pre-P1 design pass was requested to make the platform feel premium. A first
  clean Inter-based polish was not distinctive enough; the user asked for a more creative, playful
  educational look (referencing modern UI galleries). Guided by the `frontend-design` skill, the
  brief became: claymorphism cards, a course catalog, a progress demo, testimonials, an enrollment
  CTA, and vibrant colours.
- **Decisions.**
  1. **Aesthetic = playful claymorphism.** Soft "puffy" 3-D cards (large radii + layered inset/outer
     shadows), a warm cream canvas with floating colour blobs, vibrant pastel-fill clay cards, and a
     choreographed staggered page-load reveal. Distinctive type: **Fredoka** (rounded display) +
     **Nunito** (friendly body), self-hosted (OFL, ~140KB) — replacing Inter.
  2. **A real marketing landing** (`index.qmd`): hero (gradient-text headline + clay CTAs), a course
     catalog (M0 live + later modules "soon"), an honest browser-progress demo (ties to the real
     `localStorage` quiz scores — no accounts), persona-framed "made for learners like you" cards
     (honest, not fabricated named reviews), and an enrollment CTA band.
  3. **Scope:** the playful clay treatment is for the **landing**; chapter reading stays calm
     (same fonts + clay-lite Key Takeaways/badges, but no blob background) so long-form stays legible.
  4. **Accessibility kept:** vibrant comes from pastel fills + colour accents, with dark text for AA;
     the a11y gate's `THEME_PAIRS` was extended to the full palette and now supports a **3:1
     large-text threshold** (WCAG) for the big hero gradient word. All pairs pass.
  5. **Sepia reading mode — shipped** (was the deferred D0008 item; this closes it).
     Quarto's native theme toggle is light/dark only, so the third reading theme is
     delivered as a **token + Bootstrap-var override layered on the light stylesheet**
     (`html[data-lx-mode="sepia"]` in `theme/_larnix-components.scss` — warm "paper"
     `#f3e9d2` ground, brown ink, warmed nav/code/Key-Takeaways surfaces; clay cards
     reused from light), switched on by a **custom 3-way control** in
     `theme/_after-body.html`: it repurposes Quarto's existing navbar toggle to cycle
     **Light → Sepia → Dark** (current-mode glyph ☀️/📖/🌙 via CSS, descriptive
     `title`/`aria-label`). Light/dark **reuse Quarto's own `quartoToggleColorScheme`**
     stylesheet switching (never reimplemented); only the dark base needs the alternate
     sheet, so sepia rides on light. Choice persists in `localStorage["larnix-mode"]`,
     and the code keeps Quarto's own `quarto-color-scheme` sentinel in sync so the dark
     base loads on reload without a flash (the light→sepia warm-on-warm transition is
     applied after body parse and is visually negligible). All sepia colour pairs meet
     WCAG AA and are enforced by `infra/ci/a11y_check.py`.
  6. **Live-cell status: "Setting up…" while downloading packages, not "Running…"** (follow-up fix).
     quarto-live drives one per-cell indicator (`.exercise-editor-eval-indicator`) for the whole
     `evaluate()` call, which the theme renders as the in-place Run-button status **"Running…"**. But
     a cell run involves two distinct download phases that both read as "Running…" yet are really a
     one-time, multi-second **download**, not code execution: **(a)** the first-load Pyodide runtime +
     base-package **bootstrap** (the `Downloading Pyodide` / `Downloading package: …` phase), and
     **(b)** on-demand package installs when a cell first imports something (e.g. the first
     `import sklearn`). Considered: editing the vendored, minified `live-runtime.js` — rejected
     (third-party, overwritten on extension upgrade, non-diffable). **Chosen:** a two-part theme-layer
     fix that swaps the label to a violet **"Setting up…"** for both phases:
     - **Bootstrap (a) — CSS only.** quarto-live shows its own global `#exercise-loading-indicator`
       (created `d-none` by `live.lua`, un-hidden during boot, removed when ready) for exactly this
       window. A `body:has(#exercise-loading-indicator:not(.d-none)) .exercise-editor:has(.exercise-editor-eval-indicator:not(.d-none))`
       selector retargets the running cell's button to "Setting up…" — no JS, no runtime internals.
     - **On-demand (b) — JS seam.** Wrap `PyodideEvaluator.prototype.evaluate` (exposed on
       `window._exercise_ojs_runtime`) to pre-load the cell's imports first, tagging the active editor
       `.lx-loading-pkg` (CSS swaps the label), then delegate to the original `evaluate()` (its load
       step now a no-op, so "Running…" shows only for real execution). A 150 ms delay before tagging
       means already-cached packages never flash the setup state; the **first** eval of the page uses
       no delay so it hands straight off from the bootstrap state without a "Running…" flash.

     Scoped to Pyodide (Python) cells; the wrapper self-heals (no-ops) if runtime internals change.
- **Rationale.** A memorable, friendly identity that fits a beginner-first learning platform; CSS-only
  motion, self-hosted fonts, ₹0, accessible.
- **Consequences.** Replaces the earlier Inter polish. New tokens/components in
  `theme/_larnix-components.scss`; `a11y_check.py` gained per-pair contrast thresholds. Honest content
  choices: testimonials are persona-based with a "Larnix is new" framing; "enrollment" is "start free,
  no signup" (no accounts exist in P0). The live-cell loading fix (decision 6) adds the `.lx-loading-pkg`
  / `#exercise-loading-indicator` "Setting up…" states in `theme/_larnix-components.scss` and a second
  `<script>` in `theme/_after-body.html`. Verified end-to-end in a real browser on a cold cache: the
  full ~4.4 s runtime bootstrap and the on-demand scikit-learn download both read "Setting up…", with
  "Running…" only during actual code execution. The sepia mode (decision 5) adds the
  `html[data-lx-mode="sepia"]` token block + 3-state toggle glyphs in `theme/_larnix-components.scss`,
  the 3-way switcher in `theme/_after-body.html`, and 14 sepia pairs in `infra/ci/a11y_check.py`
  (gate now checks 74 pairs, all pass). Verified in-browser: Light↔Sepia↔Dark cycle, reload
  persistence, and Quarto-sentinel sync, with zero console errors. This **closes the last open item**
  in this ADR; D0008's deferred sepia task is done.

---

## D0013 — Single Quarto project at the repo root (content layout)

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** `CLAUDE.md` placed `_quarto.yml` under `/site` and chapters under `/modules` at the
  repo root. A Quarto website only renders content inside its project directory, so a chapter in
  `/modules` could not use the site theme, the badge/quiz/colab shortcodes (`_extensions`), or nav.
  Authoring the first sample chapter (P0 task 14) forced the choice.
- **Options considered.** (A) single Quarto project at the repo root, chapters in `/modules`;
  (B) keep the project in `/site`, chapters in `site/modules/` (changes gate globs, diverges from
  CLAUDE.md); (C) repo-root `/modules` plus a `site/modules` symlink (fragile in copy-based renders).
- **Decision.** **(A)** — relocate `_quarto.yml`, `_extensions/`, `theme/`, and the landing/sandbox
  `.qmd` from `site/` to the repo root; render list = `["*.qmd", "modules/**/*.qmd"]`; output `_site/`.
  Chapters live in `/modules/<NN>-slug/` per CLAUDE.md; CI content-gate globs (`modules/**`) are
  unchanged.
- **Rationale.** The most natural Quarto layout, scales to 240+ chapters in one project, keeps the
  repo-root `/modules` convention and the existing gate globs, and avoids symlink fragility.
- **Consequences.** Updated all `site/`-relative paths (workflows render `path: "."`, deploy `_site`;
  docker-compose `working_dir: /work`; a11y/quiz gate globs; Vale/lychee/markdownlint/codespell
  configs; docs). `site/README.md` moved to `docs/SITE.md`. CLAUDE.md repo-conventions updated.

---

## D0012 — GPU/colab notebooks: skipped in CI, manually Colab-verified

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** P0 builds the "Open in Colab" pattern + GPU-notebook CI policy on a minimal fixture
  (P0_SPEC §1.1, §5.1) without authoring a real GPU lesson. CI has no GPU runner, so `colab`/`gpu`
  notebooks cannot (and must not) be executed by the R10 gate.
- **Decision.**
  1. **Colab button = a `colab` shortcode** (`site/_extensions/larnix/colab`) emitting the standard
     "Open in Colab" badge linking to `colab.research.google.com/github/<repo>/blob/<branch>/<path>`.
     The repo + branch are **not hardcoded** — they come from `_quarto.yml`
     (`larnix-colab-repo`/`larnix-colab-branch`) or `LARNIX_COLAB_REPO`/`LARNIX_COLAB_BRANCH` env
     (CLAUDE.md "never hardcode endpoints"). Badge `alt` text is set for a11y.
  2. **R10 skips GPU/colab notebooks.** `run_notebooks.py` does not execute a notebook whose Quarto
     front-matter is `compute: colab|gpu` or whose notebook metadata is `larnix.compute=colab` /
     `larnix.ci=false`. Only browser-twin + CPU notebooks run in CI.
  3. **Manual Colab-run record** is required in the PR for every changed `colab`/`gpu` notebook
     (link, runtime type + cost, top-to-bottom confirmation + final output + date) — see `RUNBOOK.md`.
  4. **Fixtures live outside `modules/`** (`infra/fixtures/colab-fixture.ipynb`) so the content gates
     (front-matter lint, R-gates) do not treat them as chapters.
- **Rationale.** Honours the free-tier-first principle (GPU on free Colab/Kaggle), keeps CI correct
  (never pretends to run GPU), and proves the pattern on a fixture per "evals before features".
- **Consequences.** `run_notebooks.py` gains a `should_run()` skip + tests; the M11 rented-GPU
  specifics (provider, model size) remain deferred to P4. The placeholder `OWNER/REPO` in
  `_quarto.yml` must be set when the repo is published.

---

## D0011 — a11y gate (P0-D11): deterministic alt-text + contrast; defer page-level axe

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** D0006 adopted P0-D11: a minimal a11y CI gate (alt-text presence + theme
  colour-contrast, WCAG AA). The implementation needed a path that runs in CI and on the builder's
  low-spec laptop. Full axe/pa11y page scanning needs a headless Chromium.
- **Options considered.**
  1. *axe/pa11y against the built pages in CI* — most faithful (scans the rendered DOM, generated
     images, runtime contrast), but needs a headless browser; can't run on the builder laptop or in
     the current sandbox, and is heavier/slower.
  2. **Deterministic, browser-free checks (chosen).** `infra/ci/a11y_check.py`: (a) non-empty
     alt-text on content images (Markdown `![alt]()` + inline `<img>`); (b) WCAG AA contrast on the
     theme's declared colour pairs (badges, Key Takeaways, links — light + dark, dark fills flattened
     over the `darkly` body). Stdlib-only, unit-tested, locally provable.
- **Decision.** Ship the deterministic checker now (alt-text + contrast). Defer full page-level
  axe/pa11y scanning of the rendered site to a later phase, when real content and images exist.
- **Rationale.** Deterministic + ₹0 + locally runnable beats a browser-dependent gate for P0, and it
  enforces the two things we control today (authoring alt-text, and the design system's contrast).
- **Consequences.** `a11y_check.py` (+ 12 tests) runs in the `schema` CI job (no extra deps). The
  `THEME_PAIRS` list must be kept in sync with `theme/_larnix-components.scss` / `larnix-dark.scss`
  (noted in-file). Page-level axe scanning is tracked for a later phase.

---

## D0010 — R10 for browser chapters: a CI-executed companion notebook ("twin")

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** The R10 gate (`RISKS.md §5`, P0_SPEC §5.1) requires every chapter's code to execute
  in CI. But a `compute: browser` chapter runs its `{pyodide}` cells **client-side** via quarto-live;
  they are not executed during a headless `quarto render` (we set `execute.enabled: false` so the
  build needs no kernel — D0005/task 5). So a render alone gives R10 no teeth for browser chapters.
- **Options considered.**
  1. **Companion executable "twin" notebook per browser chapter (chosen).** Each browser chapter
     ships a `.ipynb` under `modules/` containing the worked-example code + exercise *solutions* +
     grader asserts; `infra/ci/run_notebooks.py` executes it with `nbclient` (any cell error fails).
     The interactive `.qmd` gives the in-browser UX; the twin gives the CI guarantee. The same logic
     runs in both (Pyodide and CPython are both CPython-semantics).
  2. *Headless-browser smoke test (Playwright)* that loads the rendered page and asserts the pyodide
     cells ran. Real but slow/flaky and heavy infra — rejected for P0 (revisit if needed later).
  3. *Render-check only* (markup present, not executed). Rejected: no correctness guarantee.
- **Decision.** R10 = execute every `modules/**/*.ipynb` with `nbclient` (P0-D7). Browser chapters
  satisfy it via a committed **twin notebook**; CPU chapters are executable `.ipynb` directly.
- **Rationale.** Strongest correctness-per-rupee: reuses the grader logic already unit-tested in
  CPython (D0009), needs no browser in CI, and matches the spec's nbclient choice.
- **Consequences.** `infra/ci/run_notebooks.py` (+ pass/fail fixtures, 4 tests) and a `notebooks` CI
  job (its own `requirements-notebooks.txt`: nbclient, ipykernel). Authors accept a small, deliberate
  duplication between a browser chapter's `{pyodide}` cells and its twin; a future single-source
  improvement (extracting tagged cells, or loading shared code via the Pyodide VFS) is noted but not
  built in P0. The sample chapter's twin lands in task 15.

---

## D0009 — Auto-grader: `/lib` assert helper in `{pyodide}` cells (V-1 resolution)

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** P0-D5 / D0006 chose to build on quarto-live's native exercise grading **plus** a thin
  `/lib` assert helper, flagging spike **V-1**: quarto-live's grading examples are R/`webr`, so
  Python/`pyodide` grading parity had to be proven before the sample chapter relied on it
  (`P0_SPEC.md §9`). On inspecting the vendored extension (task 5): the bundled grader
  (`_gradethis.qmd`) is **R-only** (`gradethis`); a `PyodideGrader` exists in the runtime and
  `exercise`/`check`/`hint`/`solution` cell options work for `{pyodide}`, but the Python `check`-cell
  contract is under-documented and only verifiable in a browser (no headless execution).
- **Options considered.**
  1. **`/lib` assert helper as the primary grader (chosen).** `run_tests([(label, got, expected), …])`
     in plain `{pyodide}` cells. The grading logic is plain Python, so it is **unit-tested in CPython**
     (deterministic, off-browser evidence) and runs identically in the browser via Pyodide. Consistent
     `All N tests passed ✅` UX + float tolerance; hidden solutions via the `<details>` pattern.
  2. *quarto-live native `check:` grading as primary.* Richer UI, but its Python contract is
     under-documented and browser-only to verify — can't be gated in CI, weaker correctness story.
- **Decision.** The **`/lib` assert helper (`lib/grader.py`) is the default auto-grader**; quarto-live's
  native exercise widget (editor + hint + solution, and optionally `check:`) is **available for richer
  UX** and demonstrated in `site/sandbox-exercise.qmd §B`, but is not the default grading path. This is
  the spec's documented V-1 fallback, chosen because it is the only path with off-browser test evidence.
- **Rationale.** Correctness-first: grading logic that runs in CI (CPython) beats grading we can only
  eyeball in a browser. Zero extra deps, Pyodide-safe, fully controlled UX.
- **Consequences.** `lib/grader.py` + `lib/test_grader.py` (6 CPython tests, wired into the `checks`
  workflow). Chapters paste the helper into a `#| edit: false` setup cell (a future refinement loads
  `lib/grader.py` into the Pyodide VFS to remove duplication). Spike **V-1 retired**: Python grading
  logic is proven off-browser; in-browser pass/fail is a human/preview confirmation.

---

## D0008 — Design system: badge shortcode, shared SCSS partial, sepia deferred

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** P0 task 3 builds the visual vocabulary every chapter reuses: the Key Takeaways box,
  the 🟢/🟡/🔴 difficulty badges, the `browser|colab|gpu` compute badge, the `stable|frontier`
  status badge, and the dark/sepia reading modes (`STYLE_GUIDE` / P0_SPEC §1.1, §5.4). Two
  sub-choices needed deciding: how authors mark up badges, and how to deliver three reading themes
  when Quarto's native light/dark toggle supports only two.
- **Decisions.**
  1. **Badges = a Quarto shortcode** (`site/_extensions/larnix/badges`, `{{< badge difficulty=… >}}`
     / `compute=…` / `status=…`). Cleaner chapter markup than raw fenced divs and one Lua filter to
     maintain across the 240+ future chapters. The shortcode emits a `<span>` whose **visible label**
     carries the meaning (never colour alone) plus an `aria-label` ("difficulty: Beginner"); the
     coloured dot is decorative CSS. *Rejected:* fenced-div CSS classes (zero code but clunky,
     repeated markup).
  2. **Theme structure lives in a shared SCSS partial** (`theme/_larnix-components.scss`) imported by
     **both** `larnix.scss` (light/cosmo) and `larnix-dark.scss` (dark/darkly). Quarto serves
     light/dark as separate complete stylesheets, so component *layout* must exist in both; colours
     are driven by CSS custom properties + per-class rules, with dark overriding via cascade order.
     This avoids the bug where badges kept their colour but lost their pill/dot in dark mode.
  3. **Sepia reading mode = deferred** to a dedicated micro-task before the P0 DoD sign-off. A clean
     third theme needs a custom JS 3-way switcher (Quarto's built-in toggle is light/dark only),
     which is more than "simple." Light/dark ship now (fully supported, native toggle); sepia is
     tracked as an explicit follow-up so the "dark/sepia" DoD line is met, not silently dropped.
     **(Update 2026-06-28: shipped — see D0014 decision 5. Sepia is a token override layered on the
     light theme with a custom Light→Sepia→Dark switcher; the "dark/sepia" DoD line is now met.)**
- **Rationale.** Best authoring ergonomics + a11y-by-default for the most-repeated markup; one source
  of truth for component layout; honest scoping of the only non-trivial theme piece.
- **Consequences.** All chapters use the `badge` shortcode and the `.key-takeaways` fenced div.
  Colour pairs were contrast-checked (WCAG AA, worst 6.05:1) ahead of the automated a11y gate
  (task 10). A small "sepia switcher" task is added before task 18 (DoD).

---

## D0007 — PR-preview mechanism: gh-pages branch subfolders (`pr-preview-action`)

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** D0005 (P0-D9) chose **GitHub Pages + a PR preview** but explicitly left the preview
  *mechanism* open ("PR previews need a little extra wiring"). P0 task 2 must produce a public
  preview URL on every PR (P0 DoD). GitHub Pages offers two deploy models that don't mix cleanly:
  the **Actions-native** model (`upload-pages-artifact` + `deploy-pages`, single environment) and
  the **branch** model (publish to a `gh-pages` branch).
- **Options considered.**
  1. **gh-pages branch for both prod + previews (chosen).** Production deploys to the branch root;
     each PR deploys to `gh-pages/pr-preview/pr-<N>/` via `rossjrw/pr-preview-action`, which comments
     the URL and cleans up on close. One in-repo, ₹0 mechanism; no external account.
  2. *Actions-native Pages + Netlify deploy previews.* Cleaner production deploy and best preview
     UX, but previews require an external Netlify account/service — rejected to keep everything
     in-repo and ₹0 (`CLAUDE.md` → free-tier-first build principle).
  3. *Actions-native Pages only, no PR preview.* Fails the P0 "public preview URL" exit criterion.
- **Decision.** Use the **gh-pages branch** model. `publish.yml` (push to `main`) deploys the
  rendered `site/_site` to the branch root via `JamesIves/github-pages-deploy-action@v4`, excluding
  `pr-preview/` from cleanup; `pr-preview.yml` (`pull_request`) deploys per-PR previews via
  `rossjrw/pr-preview-action@v1`. Quarto pinned to **1.8.27** in CI (matches the Task 1 Docker pin);
  actions pinned to current majors (`quarto-actions@v2`).
- **Rationale.** Single coherent branch model that supports subfolder previews, stays docs-as-code
  and ₹0, and needs no secret beyond the automatic `GITHUB_TOKEN`.
- **Consequences.** Requires a one-time repo setting (Pages → *Deploy from a branch* → `gh-pages` /
  root). The live preview URL is verified on the first PR pushed to GitHub (not executable in the
  local sandbox). Later CI gates (R10 execution, prose/link/spell, a11y, R-gates — tasks 8–11) are
  added as separate workflows/jobs alongside these two.

---

## D0006 — P0 quality gates: notebook execution, prose/lint stack, R-gates, a11y, grader & quiz design

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** P0 (the pedagogy gate) must make the Varsity contract and the `RISKS.md §5` triggers
  *mechanically enforceable* in CI before any module is authored at scale. Decisions P0-D5–D8,
  D10–D11 from `docs/phases/P0_SPEC.md §3`.
- **Decisions.**
  1. **Auto-grader (P0-D5) = `quarto-live` native exercise grading + a thin `/lib` assert helper.**
     Web-search validation (2026-06-28) confirmed `quarto-live` ships first-class exercises with
     `setup`/`hints`/`solution` and a `check: true` grading cell for Pyodide blocks; the `grade()`
     helper just gives a consistent pass/fail UX (`All tests passed ✅`) and hidden solutions in
     `<details>`. Open-ended work uses **published rubrics**, not auto-grading (`RISKS.md R4`).
     *Caveat (spike V-1):* most quarto-live grading examples are R/`webr`, so Python/`pyodide`
     grading parity is verified on a scratch exercise in P0 before authoring the chapter; the `/lib`
     helper is the fallback. *Rejected:* nbgrader (needs a server, breaks in-browser ₹0); bare
     inline asserts (no consistent UX/reuse).
  2. **Quiz engine (P0-D6) = custom lightweight JS** reading a `quiz.yml`, scoring MCQ client-side,
     progress in `localStorage`. *Rejected:* Quarto quiz shortcode (less control over scoring); H5P
     (heavy external dep, not docs-as-code). Matches `CLAUDE.md` "start static."
  3. **CI notebook execution (P0-D7) = `quarto render` (freeze) for `.qmd` + `nbclient`/`jupyter
     execute` for `.ipynb`.** Single toolchain with the site build; any cell error fails CI (= the
     R10 gate). *Rejected:* nbval (brittle on nondeterministic output — revisit for P2 stochastic
     graders); papermill (overkill for P0's single CPU notebook).
  4. **Prose/link/spell (P0-D8) = Vale (custom Larnix style enforcing the banned-word list) +
     markdownlint-cli2 + codespell + lychee.** Enforces `STYLE_GUIDE §3` tone gate. *Rejected:*
     markdownlint-only (misses banned-words/tone).
  5. **R-gates (P0-D10) = Python scripts under `infra/ci/`** (`currency_check.py` [R1],
     `browser_import_lint.py` [R3], `free_fallback_check.py` [R6]; R10 = the execution job), each
     with a unit test, invoked on every PR. *Rejected:* inline shell/grep (untestable, brittle).
  6. **Accessibility (P0-D11) = add a minimal a11y CI gate** — alt-text presence + theme
     colour-contrast (WCAG AA) on built pages. Instantiates the cross-cutting a11y concern in
     `CLAUDE.md` early; expanded in later phases. *Rejected:* deferring all a11y to a later phase.
- **Rationale.** "Evals before features": the gates are built and proven on one chapter so every
  later chapter inherits them. Each choice favours docs-as-code, zero-backend, and the ₹0 path.
- **Consequences.** Drives P0 tasks 8–11 and 13 in `P0_SPEC.md §6`; defines the blocking CI set in
  the P0 DoD. Stochastic-grader tolerances explicitly deferred to P2.

---

## D0005 — P0 platform stack: Quarto + quarto-live (Pyodide) on GitHub Pages

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** P0 must build the content-delivery machine: an in-browser Python runtime and a
  host/deploy target. Decisions P0-D4 and P0-D9 from `docs/phases/P0_SPEC.md §3`.
- **Decisions.**
  1. **In-browser runtime (P0-D4) = `quarto-live` (Pyodide-backed live code cells).** Native Quarto
     integration, editable + runnable cells inline, least glue. Version-pinned (younger extension).
     *Rejected:* embedded JupyterLite (heavier, clunkier page integration, separate build);
     hand-rolled Pyodide + JS (most maintenance, reinvents the wheel).
  2. **Hosting/deploy (P0-D9) = GitHub Pages (production) + a PR preview deploy.** In-repo, free,
     simple; satisfies the "public preview URL" exit criterion. *Rejected:* Netlify / Vercel
     (better preview UX but external account/service; less natural for a Quarto static site).
- **Rationale.** Both keep the toolchain docs-as-code, ₹0, and runnable from a fresh clone on the
  builder's low-spec laptop (`CLAUDE.md` → Environment constraints). `quarto-live` is the single
  biggest architectural commitment in P0 and is the cleanest path to "runs in the browser, zero
  install."
- **Consequences.** Drives P0 tasks 1–2 and 5 in `P0_SPEC.md §6`. The "Open in Colab" pattern is
  built alongside for future `colab` chapters but no GPU lesson is authored in P0.

---

## D0004 — P0 sample-chapter scope: one Pyodide scikit-learn chapter; seed SR cards; defer M0 HF demo

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** P0 proves the whole platform on **one** sample chapter ("evals before features",
  `CLAUDE.md`). The literal M0 "Run your first model" uses HF `pipeline()`, which is **not
  Pyodide-safe** and so cannot honour the "first model in the browser, zero install" promise
  (`ROADMAP.md §1`). Decisions P0-D1, P0-D2, P0-D3 from `docs/phases/P0_SPEC.md`.
- **Options considered (P0-D1).**
  1. **scikit-learn in Pyodide (chosen)** — "train your first model in your browser" on Iris.
     Pyodide-safe; real "wow"; clean assert-graders; reusable as M0/M4 content.
  2. *transformers.js widget* — faithful to M0's HF demo, but JS (not a Python notebook) and
     complicates the grader path.
  3. *Pure-Python M1 chapter* — purest grader test but weakest hook; doesn't exercise data
     loading/output rendering.
- **Decisions.**
  1. **P0-D1 = scikit-learn in Pyodide.** Sample chapter = *"Train your first model — in your
     browser"* (🟢, `compute: browser`, `status: stable`).
  2. **P0-D2 = one `browser` chapter + a non-content `colab` fixture** (proves the "Open in Colab"
     pattern + GPU-notebook CI policy). **No** second full Colab chapter in P0.
  3. **P0-D3 = seed spaced-repetition cards from P0 onward** — `review_cards:` derived from the
     Key Takeaways, schema-validated in CI; the scheduler is deferred to P6. Avoids retrofitting
     every P1 chapter later.
  4. The **eventual M0 HF-`pipeline()` demo** mechanism (transformers.js vs `colab`) is **deferred
     to M0 grooming in P1**; it does not block P0.
- **Rationale.** Maximises machinery coverage (browser run + assert-grader + rubric + MCQ + Key
  Takeaways) at the 🟢 tier that dominates P1, while keeping the ₹0 in-browser promise and a genuine
  first-model hook. Resolves the HF-Pyodide tension without compromising the gate.
- **Consequences.** Drives P0 tasks 12–15 in `P0_SPEC.md §6`. Adds a `review_cards:` front-matter
  convention all future chapters follow. Surfaces an M0 decision for P1.

---

## D0003 — Final consistency pass: ₹0 boundary, compute buckets, front-matter field set

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** A cross-doc consistency pass found three mismatches: (a) `Larnix-PLAN.md` said the
  ₹0 path covers "Modules 0–9" while `CLAUDE.md`, `STYLE_GUIDE.md`, and `ROADMAP.md` said "0–10";
  (b) `ROADMAP.md`'s module-map listed M4 as `browser→colab` and M8 as `colab + gpu(opt)`, which
  diverged from `CLAUDE.md`'s canonical compute buckets; (c) the chapter front-matter field set was
  enumerated as 8 fields in `CLAUDE.md`/`STYLE_GUIDE.md` but 10 in `CHAPTER_TEMPLATE.md`.
- **Decisions.**
  1. **₹0 boundary = Modules 0–10** (canonical). `CLAUDE.md` is the highest authority (per D0002);
     M10 (Generative AI) runs on free Colab, so the ₹0 promise legitimately extends to M10. Fixed
     PLAN's two "0–9" references to "0–10."
  2. **Compute buckets** are canonical as stated in `CLAUDE.md`: `browser` = M0–M4, free
     Colab/Kaggle = M5–M10, **rented `gpu` = M11 only**. Therefore M4's dominant tier is `browser`
     (heavier chapters like XGBoost offer a free Colab fallback) and M8 is `colab` (no rented GPU —
     "rented GPU only for M11" is firm). Fixed the ROADMAP module-map cells.
  3. **Front-matter field set = the 10 fields in `CHAPTER_TEMPLATE.md`**: `title, module, chapter,
     difficulty, prereqs, learning_objectives, compute, status, last_reviewed, est_minutes`. The
     template is the implementation truth; `CLAUDE.md` and `STYLE_GUIDE.md` were completed to match.
  4. **M1 prerequisite = none** (matches PLAN). M0 is orientation, not a knowledge gate.
- **Rationale.** One value per fact, owned by the authoritative doc (D0002); the others are aligned
  to it rather than left to drift.
- **Consequences.** Edited `Larnix-PLAN.md` (₹0 → 0–10), `ROADMAP.md` (M1 prereq, M4/M8 compute,
  dominant-tier note, journey wording), `CLAUDE.md` + `STYLE_GUIDE.md` (front-matter list), and the
  doc indexes (`docs/README.md` now lists RISKS.md + Larnix-PLAN.md; stale "Stage 0" wording
  removed from both READMEs). No change to PLAN's per-module chapter counts or curriculum structure.

---

## D0002 — ROADMAP is the executive spine; PLAN/RISKS/STYLE_GUIDE own their domains

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** Multiple planning docs now exist (`ROADMAP.md`, `Larnix-PLAN.md`, `RISKS.md`,
  `STYLE_GUIDE.md`, `CHAPTER_TEMPLATE.md`, `CLAUDE.md`). Without a clear ownership rule they can
  drift and contradict each other (this surfaced as a chapter-count conflict — see D0001).
- **Options considered.**
  1. *One mega-doc* — fold everything into ROADMAP. Rejected: huge, unmaintainable, high drift.
  2. *No hierarchy* — let each doc restate everything. Rejected: guarantees contradictions.
  3. *Domain ownership with a single spine (chosen).* Each doc is authoritative for one domain;
     ROADMAP is the executive spine that references the others instead of duplicating them.
- **Decision.** Source-of-truth ownership is:

  | Domain | Source of truth |
  |--------|-----------------|
  | Mission, subsystems, working rules, Definition of Done | `CLAUDE.md` |
  | Curriculum — modules, chapter counts, prereqs, capstones, infra ladder, outcomes | `Larnix-PLAN.md` |
  | Risks — IDs, triggers, owners, mitigations, cadence | `RISKS.md` |
  | Pedagogy/format — Varsity contract, tiers, front-matter, compute/status fields | `STYLE_GUIDE.md` + `CHAPTER_TEMPLATE.md` |
  | Executive spine (phases, coverage map, outcome map, effort) | `ROADMAP.md` |

  `CLAUDE.md` principles override all. ROADMAP defers detail to the owning doc and links rather
  than restating.

- **Rationale.** Single-owner-per-domain prevents drift; the spine stays readable; updates have one
  obvious home.
- **Consequences.** `ROADMAP.md` carries a "reconciliation map" header declaring this split. When a
  fact lives in two docs, the non-owner must reference the owner, not re-state the value.

---

## D0001 — Canonical chapter count: PLAN's per-module estimate (~240+ full / ~180 stable-core)

- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** `RISKS.md` (R9) described the surface as "~180 chapters," while `Larnix-PLAN.md`'s
  per-module table sums to ~240+. This looked like two competing sources of truth for the same
  number.
- **Options considered.**
  1. *Trim PLAN's per-module counts down to ~180.* Rejected: the itemized per-module estimates are
     deliberate and pedagogically grounded; trimming to hit a round aside would be backwards.
  2. *Treat the figures as a scope distinction (chosen).* PLAN's ~240+ is the **full** build; ~180
     is the **stable-core** subset (math, classical ML, backprop, transformers — written to last),
     with the remainder being the smaller, version-pinned frontier surface.
- **Decision.** `Larnix-PLAN.md` is authoritative for chapter counts. Canonical figure:
  **~240+ chapters full, ~180 stable-core.** The "~180" in RISKS was a rounded aside, not a
  competing count.
- **Rationale.** Per D0002, curriculum counts are owned by PLAN. The full/stable-core split is real
  and useful (it ties directly to R1 currency: keep stable-core large, frontier surface small).
- **Consequences.** `RISKS.md` R9 updated (summary row + detail) to read "~240+ chapters; ~180
  stable-core" and to name PLAN as the curriculum source of truth. `ROADMAP.md` §2 states the same
  split. No change to PLAN's per-module numbers.
