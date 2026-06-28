# P0_SPEC — Platform MVP + the Pedagogy Gate

> **Phase:** P0 — *Platform MVP + the pedagogy gate* (per `ROADMAP.md §3`).
> **Status:** GROOMING — awaiting approval. No chapters or application code are written until this
> spec is approved and the listed decisions are confirmed + logged in `DECISIONS.md`.
> **Authoritative parents:** `CLAUDE.md` (operating agreement, DoD), `ROADMAP.md §3 P0`
> (phase goal + exit criteria), `STYLE_GUIDE.md` (Varsity contract), `CHAPTER_TEMPLATE.md`
> (front-matter schema), `RISKS.md §5` (the automated gates this phase must build).
> **Last updated:** 2026-06-28

P0 is the highest-leverage phase: it builds and *proves* the entire content-delivery machine on
**one** complete sample chapter before any module is authored at scale — the content-platform
equivalent of "evals before features" (`CLAUDE.md` → Working agreement). Everything later inherits
the gates built here.

---

## 1. Scope

### 1.1 In scope — subsystems built and proven on ONE sample chapter
All six subsystems (`CLAUDE.md` → Architecture), bootstrapped to MVP and proven end-to-end on a
single throwaway-quality-but-real sample chapter:

1. **Content System** — finalize the per-chapter template into a working `.qmd`/`.ipynb`; prove
   the front-matter schema is machine-enforceable. (`CHAPTER_TEMPLATE.md` already exists as prose;
   P0 turns it into an executable, linted artifact.)
2. **Build & Publish System** — Quarto static site that builds from a fresh clone; theme/design
   system (Key Takeaways box, 🟢/🟡/🔴 difficulty badges, `browser|colab|gpu` compute badge,
   `stable|frontier` status badge, dark/sepia mode), nav, and search.
3. **Interactive Compute Layer** — in-browser Python (JupyterLite/Pyodide) so a `browser` chapter
   runs with zero install; the **"Open in Colab"** button *pattern* (template + CI policy) for
   future `colab` chapters.
4. **Exercise & Auto-Grading System** — assert-based, in-browser grader harness (`/lib`); the
   hidden-solution `<details>` pattern; one MCQ concept check.
5. **Assessment / Progress System (MVP)** — a client-side JS quiz engine that reads a `quiz.yml`,
   renders + scores an MCQ, and persists progress in browser storage; the **spaced-repetition card
   seeding convention** (cards authored, engine deferred).
6. **Currency & Ops System** — GitHub Actions CI: execute browser/CPU notebooks; prose lint (Vale +
   markdownlint), link-check, spell-check; a **minimal a11y check** (alt-text presence + theme
   contrast, P0-D11); the four **R-gates** (`RISKS.md §5`): R1 currency check, R3 browser-import
   lint, R6 free-fallback check, R10 runs-in-CI; deploy to a public preview URL.

**Modules authored at scale:** **none.** Exactly **one sample chapter** (see §3 P0-D1).

### 1.2 Non-goals (explicit — to prevent scope creep)
- **No module authored at scale.** M0–M16 content is P1+. P0 produces *one* chapter only.
- **No GPU or `colab` chapter authored.** The Colab button + GPU-notebook CI policy are built and
  validated with a *minimal fixture*, not a real lesson. (GPU content starts P2; M11 rented-GPU is
  P4.)
- **No M11 specifics.** Tokenizer choice, model size, GPU provider (RunPod/Vast.ai/Modal) are
  **deferred to P4** per `ROADMAP.md`. P0 does not decide them.
- **No accounts, auth, PII, or server-side persistence.** Progress is browser-storage only
  (`RISKS.md R7`). Certification/proctoring is P6.
- **No real certification exam, no learning-track engine, no working spaced-repetition scheduler.**
  P0 only seeds the *data convention* for review cards; the SR engine is P6.
- **No frontier/`status: frontier` content.** The sample chapter is `stable`.
- **No paid-API lesson.** The free-fallback *gate* is built; no chapter that needs a key is written.
- **No content-authoring automation/agents, no community-PR tooling beyond what already exists.**
- **No analytics/telemetry beyond local progress.**

---

## 2. Content design (the single sample chapter)

P0 has no modules, so the usual "per-module" content design collapses to **one chapter**. It is
chosen to exercise the *maximum* of the machinery (assert-grader, MCQ, runnable browser cell,
Key Takeaways, hook) at the 🟢 tier that dominates P1, while being a *real* chapter we can keep.

**Proposed sample chapter (pending P0-D1):** a 🟢 **`browser`** chapter,
**"Train your first model — in your browser"**, runnable entirely in Pyodide via **scikit-learn**
(Iris/penguins): load data → fit a tiny classifier → predict → check accuracy. This is the
strongest single test of the platform because it is Pyodide-safe *and* produces a genuine "I made
a model with zero install" hook, and it yields clean assert-graders.

| Attribute | Value |
|---|---|
| **Learning objectives** | (1) Run Python in the browser with zero install; (2) Train & call a scikit-learn classifier; (3) Read a basic accuracy number and say what it means. |
| **Running example** | The Iris (or palmer-penguins) dataset — small, license-clean, Pyodide-loadable. |
| **Difficulty tier** | 🟢 Beginner |
| **Compute tier** | `browser` (Pyodide; scikit-learn is in the Pyodide package set) |
| **Status** | `stable` |
| **Chapter list (1)** | `Ch01 — Train your first model, in your browser` — fit + predict a classifier client-side, no install. |
| **est_minutes** | ~20 |

> **Why not the literal M0 "Run your first model (HF `pipeline()`)" chapter?** HF `transformers`
> is **not** Pyodide-safe, which collides with the "first model in the browser, zero install"
> promise (`ROADMAP §1` journey step 1). This tension is real and is surfaced as **Q-A** below.
> Using scikit-learn in Pyodide keeps the wow *and* the ₹0 in-browser promise for the gate.

A **minimal `colab` fixture** (not a chapter): a 3-cell notebook with an "Open in Colab" button,
used only to prove the button pattern + the GPU-notebook CI policy (manual-run record). It is not
counted as content.

---

## 3. Decisions to make now

Each decision has a provisional ID (`P0-Dn`). On your confirmation they are logged in
`DECISIONS.md` as `D0004+`. **Recommendation is listed first.**

> **Confirmation status (2026-06-28).** All decisions below are **CONFIRMED at their recommended
> option** and logged in `DECISIONS.md` (D0004–D0006). Specifically: **P0-D1 = A** (scikit-learn in
> Pyodide), **P0-D2 = A** (one `browser` chapter + non-content `colab` fixture; *no* second full
> Colab chapter), **P0-D3 = A** (seed SR cards now), **P0-D4 = A** (`quarto-live`), **P0-D9 = A**
> (GitHub Pages + PR preview), and **P0-D5/D6/D7/D8/D10 = recommended option (A)**. Plus a new
> **P0-D11 = add a minimal a11y CI check** (see §5.3).

### Pedagogical

**P0-D1 — Which chapter to build as the sample.**
- **(A, rec.) Pyodide scikit-learn "train your first model"** (Iris). Pyodide-safe; real "wow";
  clean assert-grader; reusable as M0/M4 content. *Con:* not 100% the literal M0 ch as planned.
- (B) A pure-Python M1 chapter (e.g. *functions* or *data structures*). Purest test of the
  assert-grader; trivially Pyodide-safe. *Con:* weakest hook; doesn't test data/plot rendering.
- (C) The literal M0 *"Run your first model"* with HF `pipeline()`. Most faithful to PLAN. *Con:*
  not Pyodide-safe → breaks the in-browser gate (see Q-A); would force `colab`.

**P0-D2 — Number of sample chapters.**
- **(A, rec.) Exactly one `browser` chapter + one non-content `colab` fixture.** Matches "one
  sample chapter only"; still proves the Colab pattern. *Con:* GPU CI policy proven on a stub.
- (B) Two full chapters (one `browser`, one `colab`). Proves more, end-to-end. *Con:* scope creep;
  violates the gate's "one chapter" intent; GPU verification adds wall-clock.

**P0-D3 — Spaced-repetition seeding now vs later.**
- **(A, rec.) Seed the *convention* only:** derive review cards from the Key Takeaways via a
  `review_cards:` block in front-matter/sidecar; ship a schema + one example; build the scheduler
  in P6. *Con:* cards exist but aren't yet scheduled.
- (B) Defer entirely to P6. *Con:* every P1 chapter would later need retrofitting.
- (C) Build a minimal SR scheduler now. *Con:* clear scope creep for P0.

### Technical

**P0-D4 — In-browser Python runtime.**
- **(A, rec.) `quarto-live` (Pyodide-backed live code cells in Quarto).** Native Quarto
  integration, editable runnable cells inline, least glue. *Con:* younger extension; pin version.
- (B) Embed **JupyterLite** via iframe. Full Jupyter UX. *Con:* heavier, clunkier page integration,
  separate build.
- (C) Hand-rolled Pyodide + custom JS. Max control. *Con:* most maintenance; reinvents the wheel.

**P0-D5 — Auto-grader harness design.**
- **(A, rec.) Use `quarto-live`'s native exercise grading + a thin assert convention in `/lib`.**
  Web-search validation (§9) confirms `quarto-live` already provides first-class exercises with
  `setup`, `hints`, `solution`, and **custom grading** (a `check: true` cell that returns pass/fail)
  for Pyodide/Python blocks. So the harness = quarto-live's grading primitive + a tiny reusable
  `grade()` assert helper for consistency. Runs fully client-side; matches `STYLE_GUIDE §6`. *Con:*
  most published grading examples are R/`webr`, so **P0 must verify Python/`pyodide` grading works
  equivalently** (see Risk V-1, §9) — the `/lib` assert helper is the fallback if it lags.
- (B) **nbgrader**-style metadata + server grading. Mature. *Con:* needs a server; breaks
  in-browser ₹0.
- (C) Pure inline `assert` cells, no harness. Simplest. *Con:* no consistent pass/fail UX, no reuse.
- (B) **nbgrader**-style metadata + server grading. Mature. *Con:* needs a server; breaks
  in-browser ₹0.
- (C) Pure inline `assert` cells, no harness. Simplest. *Con:* no consistent pass/fail UX, no reuse.

**P0-D6 — Quiz engine.**
- **(A, rec.) Custom lightweight JS** reading a per-chapter/module `quiz.yml`, scoring MCQ
  client-side, progress in `localStorage`. Zero backend, matches `CLAUDE.md` "start static". *Con:*
  we own the code.
- (B) A Quarto extension/shortcode for quizzes. Less custom JS. *Con:* less control over scoring
  /progress; ecosystem immaturity.
- (C) Third-party (e.g. H5P). Rich. *Con:* heavy, external dependency, not docs-as-code.

**P0-D7 — CI notebook-execution engine.**
- **(A, rec.) `quarto render` with execution (freeze) for `.qmd` + `nbclient`/`jupyter execute`
  for standalone `.ipynb`.** One toolchain with the site build; fails CI on any cell error. *Con:*
  two code paths (qmd vs ipynb).
- (B) **nbval** (pytest plugin validating outputs). Strong assertion of outputs. *Con:* brittle on
  nondeterministic output; better suited to P2 stochastic graders.
- (C) **papermill**. Parameterized execution. *Con:* overkill for P0's single CPU notebook.

**P0-D8 — Prose / link / spell stack.**
- **(A, rec.) Vale (custom Larnix style enforcing the banned-word list) + markdownlint-cli2 +
  codespell + lychee (link-check).** All fast, CI-friendly, configurable. *Con:* authoring the Vale
  style rules up front.
- (B) Only markdownlint + a basic link-checker. Less setup. *Con:* misses banned-words/tone gate
  (`STYLE_GUIDE §3`).

**P0-D9 — Hosting / deploy.**
- **(A, rec.) GitHub Pages for production + a PR preview deploy** (Pages or Netlify preview).
  In-repo, free, simple, satisfies the "public preview URL" exit criterion. *Con:* PR previews need
  a little extra wiring.
- (B) Netlify (prod + automatic deploy previews). Best preview UX. *Con:* external account/service.
- (C) Vercel. Good DX. *Con:* external; less natural for a Quarto static site than Pages/Netlify.

**P0-D10 — Where the R-gates live + how they run.**
- **(A, rec.) Python scripts under `infra/ci/`** (`currency_check.py` [R1], `browser_import_lint.py`
  [R3], `free_fallback_check.py` [R6]; R10 = the execution job in P0-D7), each with a tiny unit
  test, invoked by the Actions workflow on every PR. *Con:* a few scripts to maintain.
- (B) Inline shell/grep steps in the workflow YAML. Fast to write. *Con:* untestable, brittle,
  hard to reuse.

> **Deferred to later phases (recorded so they are *not* decided in P0):** M11 tokenizer / model
> size / GPU provider (P4); stochastic-grader tolerance design (P2); frontier-refresh cadence
> tooling specifics (P3/P7); certification exam + SR scheduler (P6).

---

## 4. Exercise & assessment plan

Scope is the single sample chapter; this proves each assessment mechanism once.

### 4.1 Exercises (sample chapter) — 3, scaffolded per `STYLE_GUIDE §6`
1. **Guided / fill-in-the-blank (🟢, ~5 min).** Complete one line to `.fit()` the classifier.
   *Graded:* assert harness checks the model is fitted and predicts the right shape; hidden
   solution in `<details>`.
2. **Implement-this-function (🟢/🟡, ~10 min).** Write `accuracy(y_true, y_pred) -> float`.
   *Graded:* assert-based unit tests (`assert accuracy([...],[...]) == expected`) running in
   Pyodide; prints `All tests passed ✅`.
3. **Open-ended stretch (🟡, optional, ~15 min).** Swap in a different feature/model and beat a
   stated baseline accuracy. *Graded:* **rubric** (2–3 bullets), not auto-graded — demonstrates the
   rubric path that `RISKS.md R4` mandates for open-ended work; the UI labels it "rubric-graded."

This deliberately exercises **both** grader types: deterministic assert (Ex 1–2) and rubric (Ex 3).

### 4.2 Module quiz (proof of engine)
A `quiz.yml` with **3 MCQs** on the chapter's ideas (what is a model / what accuracy means /
what "in the browser" buys you). The JS engine renders, scores client-side, shows correct answers
+ explanations, and stores the score in `localStorage`. This proves the P1 quiz mechanism.

### 4.3 Capstone + rubric (proof of mechanism, not a real capstone)
P0 has no module, so **no real capstone**. Instead, ship a one-page **sample `capstone.md` with a
rubric** as a *template artifact* (criteria, levels, "did you measure it?" line per `ROADMAP §1`
eval thread) so P1 authors inherit a proven rubric format. Clearly marked as a template, not
graded content.

### 4.4 Spaced-repetition card seeding
Per P0-D3(A): the sample chapter's **Key Takeaways → 3 review cards** in a `review_cards:` block
(Q/A pairs), validated by schema in CI. The scheduler that serves them is P6; P0 proves the
*authoring convention* so no P1 chapter needs retrofitting.

---

## 5. Quality plan

### 5.1 CI vs Colab-verified
- **Runs in CI (blocking):** the one `browser` sample-chapter notebook executes top-to-bottom via
  P0-D7; the auto-grader cells pass; the front-matter schema validates; the quiz.yml schema
  validates; the `review_cards` schema validates.
- **Colab-verified (manual, recorded):** the minimal `colab` *fixture* only — a recorded manual run
  link pasted into the PR, proving the GPU-notebook policy (`ROADMAP §3 P2` policy, dry-run here).
  No real GPU lesson in P0.

### 5.2 Lint / link / spell gates (all blocking on PR)
- **Prose tone:** Vale with the Larnix style — fails on banned words (`simply`, `just`,
  `obviously`, `trivially`, and the hype list) per `STYLE_GUIDE §3`.
- **Markdown:** markdownlint-cli2.
- **Spelling:** codespell (with an allow-list for AI terms).
- **Links:** lychee link-check (internal + external).

### 5.3 The four R-gates (P0-D10) — blocking on PR
- **R1 `currency_check.py`** — fails if any `status: frontier` chapter has `last_reviewed` > 90
  days (no-op now; mechanism proven).
- **R3 browser-import lint** — fails a `compute: browser` chapter that imports a non-Pyodide
  package (the sample chapter must pass cleanly).
- **R6 free-fallback check** — fails any required-path chapter needing a paid key with no free
  fallback (no-op now; mechanism proven).
- **R10 runs-in-CI** — every code block executes (5.1); a broken example fails the build.

### 5.4 Accessibility check (P0-D11) — blocking on PR
A **minimal** a11y gate (the cross-cutting a11y concern in `CLAUDE.md`, instantiated early):
- Alt-text presence on every image/diagram in the rendered site.
- Theme colour-contrast check on the Key Takeaways box, badges, and dark/sepia modes (WCAG AA).
- Implemented as a lightweight CI step (e.g. an axe/pa11y-style check against the built pages, or a
  scoped linter). Deliberately small in P0; expanded in later phases as content grows.

### 5.5 Correctness-review checklist (instantiates `STYLE_GUIDE §11` + `RISKS.md R10`)
A PR checklist the author must tick:
- [ ] Every code cell executed locally and in CI; outputs shown.
- [ ] Every term defined on first use; no banned words; reads for a true beginner.
- [ ] Numbers/claims verified; primary sources cited; no invented citations.
- [ ] Front-matter complete + accurate (all 10 fields); `last_reviewed` set.
- [ ] Free-tier/₹0 path confirmed for the chapter's compute tier.
- [ ] Exercises have working graders + hidden solutions; difficulty matches the tier.
- [ ] Quiz answers + explanations verified correct.

---

## 6. Task breakdown (ordered, independently committable)

Each task ≈ one commit/PR. Order respects dependencies.

1. **Scaffold the Quarto site** — `site/_quarto.yml`, project layout, a hello-world render; verify
   `quarto render` builds from a fresh clone. *(Build & Publish)*
2. **CI: build + deploy** — GitHub Actions workflow that builds the site and deploys to GitHub Pages
   (prod) + a PR preview; produce the public preview URL. *(Currency & Ops)*
3. **Theme / design system** — SCSS for the Key Takeaways box, 🟢/🟡/🔴 difficulty badges, compute +
   status badges, dark/sepia toggle; enable nav + search. *(Build & Publish)*
4. **Front-matter schema + lint** — encode the 10-field schema (`CHAPTER_TEMPLATE.md`); script
   `infra/ci/frontmatter_lint.py` + unit test; wire into CI. *(Content / Ops)*
5. **In-browser runtime** — integrate the chosen runtime (P0-D4); prove a runnable Pyodide cell
   on a scratch page. *(Interactive Compute)*
6. **Auto-grader harness** — integrate `quarto-live`'s native grading (`check:` cells) + a `/lib`
   `grade()` helper (P0-D5); **acceptance check V-1: prove Python/`pyodide` exercise grading works
   on a scratch exercise** before relying on it; demo hidden-solution pattern. *(Auto-Grading)*
7. **Quiz engine** — `quiz.yml` schema + JS render/score + `localStorage` progress (P0-D6); schema
   lint in CI. *(Assessment)*
8. **CI: notebook execution gate (R10)** — execute browser/CPU notebooks (P0-D7); fail on any cell
   error. *(Currency & Ops)*
9. **CI: prose/link/spell gates** — Vale (Larnix style + banned words), markdownlint, codespell,
   lychee (P0-D8). *(Currency & Ops)*
10. **CI: minimal a11y gate (P0-D11)** — alt-text presence + theme contrast (WCAG AA) on the built
    pages. *(Currency & Ops)*
11. **R-gates** — `infra/ci/` scripts for R1 currency, R3 browser-import lint, R6 free-fallback
    (P0-D10), each with a unit test; wire into CI. *(Currency & Ops)*
12. **Colab pattern + GPU CI policy** — "Open in Colab" button shortcode + a minimal `colab`
    fixture + the documented manual-run-record policy in `RUNBOOK.md`. *(Interactive Compute / Ops)*
13. **SR card seeding convention** — `review_cards:` schema + validator + one example (P0-D3).
    *(Assessment)*
14. **Author the ONE sample chapter** — full Varsity contract: hook → explanation → runnable
    scikit-learn example → Key Takeaways → 3 exercises (2 assert-graded + 1 rubric) (P0-D1). *(Content)*
15. **Wire the chapter in** — nav entry, quiz, graders, review cards; verify it renders, runs in
    JupyterLite (₹0) and in CI. *(Integration)*
16. **Template artifacts** — sample `capstone.md` + rubric template; update `CHAPTER_TEMPLATE.md`
    cross-refs if the build surfaced gaps. *(Content)*
17. **Docs + portfolio** — `DECISIONS.md` entries (D0004+) for confirmed P0-Dn; `RUNBOOK.md` local
    preview + CI sections; `PORTFOLIO.md` quantified bullet; module/site READMEs. *(Docs)*
18. **DoD verification pass** — fresh-clone build, green CI, preview renders, 5-minute walkthrough
    recorded. *(Gate)*

---

## 7. Definition of Done (P0) — instantiates the generic DoD from `CLAUDE.md`

P0 is done when **all** of the following hold (= `ROADMAP §3 P0` exit criteria, expanded against
the `CLAUDE.md` DoD):

- [ ] **Builds from a fresh clone** and the Quarto site **CI-deploys to a public preview URL**.
- [ ] **Theme** implements the Key Takeaways box, 🟢/🟡/🔴 difficulty badges, compute + status
      badges, dark/sepia, working nav + search.
- [ ] **`CHAPTER_TEMPLATE.md` front-matter schema (10 fields) is enforced by lint** in CI.
- [ ] **One sample chapter satisfies the full Varsity contract** (hook → explanation → runnable
      example → Key Takeaways → 2–4 graded exercises) with complete, accurate front-matter incl.
      `last_reviewed`.
- [ ] Its **notebook runs in JupyterLite (₹0)** *and* **executes cleanly in CI**.
- [ ] **≥1 exercise auto-graded in-browser** with a hidden solution walkthrough; **≥1 rubric-graded**
      exercise demonstrates the open-ended path (`RISKS.md R4`).
- [ ] **Quiz engine renders + scores an MCQ client-side**, persisting progress locally.
- [ ] **CI green:** notebook execution (R10), Vale, markdownlint, link-check, spell, **a11y
      (alt-text + contrast, P0-D11)**.
- [ ] **The R1/R3/R6/R10 automated gates exist** and run on every PR (`RISKS.md §5`).
- [ ] **SR card seeding convention** in place (cards authored + schema-validated; engine deferred).
- [ ] **Colab button pattern + GPU-notebook CI policy** documented and proven on the fixture.
- [ ] **`DECISIONS.md` updated** with the confirmed P0 decisions; **`RUNBOOK.md`** has local-preview
      + CI instructions; **`STYLE_GUIDE.md`** adhered to (lint/prose pass).
- [ ] **A "5-minute learner walkthrough"** path through the sample chapter that you can click/run.
- [ ] **`PORTFOLIO.md`** carries a quantified bullet (e.g. "built a docs-as-code AI-course platform:
      in-browser Python, assert-based auto-grading, a quiz engine, and a 6-gate CI pipeline, proven
      end-to-end on a zero-install sample chapter").

---

## 8. Open questions — RESOLVED (2026-06-28)

All blocking questions are answered; no open blockers remain for the P0 build.

- **Q-A → RESOLVED.** The P0 gate uses **scikit-learn-in-Pyodide** as the first model (P0-D1 = A).
  The *eventual* M0 HF-`pipeline()` wow (transformers.js widget vs `colab`) is **deferred to an M0
  decision in P1** — it does not block P0.
- **Q-B → RESOLVED.** Host on **GitHub Pages + PR preview** (P0-D9 = A).
- **Q-C → RESOLVED.** Runtime is **`quarto-live` (Pyodide)** (P0-D4 = A).
- **Q-D → RESOLVED.** **Seed spaced-repetition cards from P0 onward** (P0-D3 = A).
- **Q-E → RESOLVED.** **One `browser` chapter + a non-content `colab` fixture** (P0-D2 = A); no
  second full Colab chapter in P0.
- **Q-F → RESOLVED.** **Add a minimal a11y CI check** now (P0-D11): alt-text presence + theme
  contrast (WCAG AA). See §5.4.

*Carried forward (not P0 blockers):* the M0 HF-demo delivery mechanism (P1, M0 grooming); M11
tokenizer/model size/GPU provider (P4); stochastic-grader tolerances (P2).

---

*On approval, I will: (1) log the confirmed P0-Dn decisions in `DECISIONS.md` as D0004+, and (2)
begin Task 1 (Quarto scaffold) — one small, reviewable commit at a time, plan-before-writing each
non-trivial task per `CLAUDE.md`.*

---

## 9. Validation log (web search, 2026-06-28)

Every load-bearing technical claim in this spec was checked against current sources. **Result: all
core assumptions hold.** One refinement and one new spike-risk surfaced.

| Claim in spec | Verdict | Evidence |
|---|---|---|
| `quarto-live` exists, runs **Python via Pyodide** in static sites, needs only static hosting (Pages/Netlify) | ✅ Confirmed | `r-wasm/quarto-live` — "WebAssembly powered code blocks… webR and Pyodide engines… only a static web service (GitHub Pages, Quarto Pub, or Netlify) is required." |
| `quarto-live` supports **exercises with hints, solutions, and custom grading** | ✅ Confirmed (→ refines P0-D5) | quarto-live docs *Creating Exercises* / *Grading Solutions*: exercises take `setup`, `hints`, `solution`, and a `check: true` grading cell. |
| **scikit-learn runs in Pyodide** (sample chapter premise) | ✅ Confirmed | Pyodide.org (v314.x, 2026): ships "NumPy, pandas, SciPy, Matplotlib, and **scikit-learn**." scikit-learn issue #34278 shows active Pyodide-wheel work (cibuildwheel v4.1.0, Jun 2026). |
| **HF `transformers` is NOT Pyodide-safe**; browser path is **transformers.js** (Q-A premise) | ✅ Confirmed | HF Transformers.js docs: "Run 🤗 Transformers directly in your browser, with no need for a server… functionally equivalent to the Python library." Python `transformers` needs PyTorch, absent from Pyodide. |
| **Quarto → GitHub Pages via GitHub Actions** (P0-D9) | ✅ Confirmed | Official Quarto docs + `quarto-dev/quarto-actions` publish action; `actions/deploy-pages`. |
| Lint stack — **Vale + markdownlint-cli2 + lychee** (P0-D8) | ✅ Confirmed, current | `lycheeverse/lychee` + `lychee-action` (Rust link checker, GH Action); markdownlint-cli2-action; Vale widely paired with both for prose/structure/links. |
| **Notebook execution in CI** — nbclient / papermill (P0-D7) | ✅ Confirmed, current | `jupyter/nbclient` (programmatic execution); papermill actively used for parameterized notebooks in 2025. (We use `quarto render` for `.qmd`; nbclient for `.ipynb`.) |
| **a11y CI** — pa11y / axe-core for alt-text + contrast (P0-D11) | ✅ Confirmed, current | `pa11y/pa11y-ci` (CI-centric runner); axe-core "detects up to 57% of issues, zero false positives" (2025/2026 comparisons). Covers alt-text + colour-contrast (WCAG A/AA). |

### Refinement (no decision reversed)
- **R-1 → P0-D5.** `quarto-live` ships native exercise grading (`check:` cells, hints, solutions).
  P0-D5(A) is updated to **build on quarto-live's grading primitive** plus a thin `/lib` assert
  helper for consistency, rather than a fully hand-rolled harness. Less custom code; same UX.

### New spike-risk to retire early in P0
- **V-1 (verify in Task 5/6).** quarto-live's published **grading examples are predominantly R
  (`webr`)**; Python/`pyodide` exercise-grading parity must be **proven on a scratch exercise
  before** authoring the sample chapter. *Fallback:* if Python grading lags, the `/lib` assert
  helper (P0-D5 option C-style, but wrapped) carries the load. This is now an explicit acceptance
  check inside Task 6 ("Auto-grader harness"). Worth noting alongside `RISKS.md R3` (Pyodide limits)
  — both are platform-capability risks proven on the gate chapter, not on real content.

*Sources: r-wasm/quarto-live (GitHub + docs), pyodide.org v314, huggingface.co/docs/transformers.js,
quarto.org publishing docs + quarto-dev/quarto-actions, lycheeverse/lychee, jupyter/nbclient,
pa11y/pa11y-ci & axe-core comparisons — all fetched 2026-06-28.*
