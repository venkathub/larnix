# Decisions

> Dated log of pedagogical & technical choices (options considered + rationale).
> Newest entries first. Each entry: context, options considered, decision, rationale, consequences.

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
