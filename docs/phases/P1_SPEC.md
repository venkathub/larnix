# P1_SPEC — Foundations track (M0–M3)

> **Phase:** P1 — *Foundations track* (per `ROADMAP.md §3 P1`).
> **Status:** ✅ **COMPLETE (2026-06-29).** All of §6 (Tasks 1–67) delivered: shared tooling +
> **50 chapters across M0–M3**, 4 module quizzes, 4 rubric-graded capstones, all gates green.
> Every §7 Definition-of-Done item is satisfied (see §7). Closed on branch
> `feat/p1-foundations-spec`. *(Spec approved 2026-06-28; all P1 decisions confirmed at their
> recommended options and logged in `DECISIONS.md` D0015–D0016; load-bearing technical claims
> web-validated 2026-06-28, see §9.)*
> **Evidence at close:** all 50 CPython twins execute cleanly (R10); 8 gate scripts + **111 unit
> tests** green; codespell clean and zero banned/hype words in learner content; full site renders
> (61 docs) and builds from a fresh clone; **§6.F Task 66 exhaustive ₹0 browser sweep — all 50
> chapters loaded and run on Pyodide, PASS**; offline datasets confirmed live (habits.csv 35 rows;
> Palmer Penguins 344×8); 4 module quizzes score and persist to `localStorage` (10/11/12/12).
> **Authoritative parents:** `CLAUDE.md` (operating agreement, generic DoD), `ROADMAP.md §3 P1`
> (phase goal + exit criteria), `Larnix-PLAN.md` (canonical M0–M3 chapter lists), `STYLE_GUIDE.md`
> (the Varsity contract, tiers, banned words), `CHAPTER_TEMPLATE.md` (10-field front-matter schema),
> `RISKS.md` (R-gates; R3/R6/R9/R10/R11/R12 are live in this phase), `docs/phases/P0_SPEC.md`
> (the proven platform this phase builds on; decisions D0004–D0014).
> **Entry criteria:** P0 DoD met ✅ (verified 2026-06-28 — site builds, gates green, sample chapter
> proven end-to-end).
> **Last updated:** 2026-06-29

P1 is the first **content-at-scale** phase. P0 proved the machine on one chapter; P1 authors the
**entire zero-to-literate on-ramp — Modules 0–3, ~50 chapters — every one of them in-browser at
₹0**. The bet here is *scale without regression*: the Varsity contract, the in-browser grader, the
quiz engine, and the six CI gates must hold across ~50 chapters, not one. Where P0 asked "can the
platform do this?", P1 asks "does the platform stay correct, ₹0, and beginner-true when there are
fifty chapters and four capstones?"

---

## 1. Scope

### 1.1 In scope — modules + chapters

The four Foundations modules, authored to the full Varsity contract, **all `compute: browser`,
all `status: stable`**, tiers 🟢→🟡:

| Module | Title | ~Ch | Tier | Compute | Capstone |
|--------|-------|-----|------|---------|----------|
| **M0** | How to Use This School / What is AI? (incl. setup + ₹0 cost) | 6 | 🟢 | browser | Set up the ₹0 toolchain; run your first pretrained model |
| **M1** | Python for AI | 14 | 🟢 | browser | Data-cleaning notebook (auto-graded) |
| **M2** | Math You Actually Need (intuition-first) | 16 | 🟢→🟡 | browser | "Math of one neuron" forward+backward notebook |
| **M3** | Data & Tooling (NumPy/Pandas/viz/envs) | 14 | 🟢→🟡 | browser | End-to-end EDA on a real public dataset |

**Total: ~50 chapters** (one of them — `M0 Ch01, "Train your first model"` — already shipped in P0
and is **reused, not rebuilt**; it may be renumbered per **P1-D1**). Plus 4 module quizzes, 4
graded capstones with rubrics, 4 expanded module READMEs, and the shared tooling in §6.A.

Subsystems exercised (`CLAUDE.md` → Architecture): **Content** (M0–M3 at scale), **Interactive
Compute** (Pyodide at scale — the first real stress test), **Auto-Grading** (the grader reused
across ~50 chapters; beginner scaffolding), **Assessment** (per-module quizzes + the first four
real capstone rubrics; SR cards seeded per chapter), **Currency & Ops** (the six P0 gates run on
every PR at scale; a new Pyodide-availability check and a dataset-license ledger).

### 1.2 Non-goals (explicit — to prevent scope creep)

- **No GPU or `colab` content.** Every P1 chapter runs in Pyodide. The free-Colab/Kaggle workflow,
  GPU templates, and stochastic-grader tolerances are **P2** (M4–M6). If a topic cannot run in the
  browser, it is reshaped to a conceptual chapter or deferred — it is **not** promoted to `colab`.
- **No classical-ML modelling depth.** Train/val/test, metrics, regularization, the full
  scikit-learn workflow are **M4 (P2)**. M0 Ch01's one-line model is a *taste*, not a teaching of
  ML methodology; M3's "scaling/encoding preview" and "data ethics preview" are **previews only**.
- **No deep learning / PyTorch / transformers.** M2 ends at the math of *one* neuron (pure
  NumPy/Python); building/ training networks is **M5+ (P3)**.
- **No paid API, no LLM keys, no Ollama.** Foundations needs none. The free-fallback *gate* (R6)
  stays green by having nothing that needs a key. (The M0 GenAI "taste" is a **client-side
  transformers.js widget**, not a server/API call — see P1-D3.)
- **No `status: frontier` content.** The "10-minute history" chapter names modern model families
  but is written as stable, version-light prose, not a frontier model spec. **No M11 specifics**
  (tokenizer / model size / GPU provider) — those are **P4**.
- **No accounts/auth/PII/server persistence.** Progress stays in `localStorage` (R7). No
  certification exam, no learning-track engine, no spaced-repetition *scheduler* — P1 only **seeds**
  review cards (the P6 engine consumes them later).
- **No new platform subsystems.** P1 reuses the P0 platform. The only tooling P1 adds is the
  small set in §6.A (grader-at-scale, twin generation, module-quiz aggregation, Pyodide-availability
  check, dataset ledger) — refinements, not new subsystems.
- **No content-authoring agents / automation beyond what exists.**

---

## 2. Content design (per module)

Conventions: difficulty 🟢 Beginner / 🟡 Intermediate / 🔴 Advanced (none in P1); compute is
`browser` for **every** chapter below; status is `stable` for **every** chapter below. Each module
threads **one running example** (`STYLE_GUIDE §4`) — confirmed in **P1-D2**.

### M0 — How to Use This School / What is AI? 🟢 · browser

- **Learning objectives.** A cold-landing learner can: (1) run real code in the browser at ₹0 and
  *feel* a model work; (2) confirm the complete ₹0 path and what (if anything) ever costs money;
  (3) say in plain words what AI/ML/DL/GenAI are and how they relate; (4) navigate the school —
  tiers, exercises, quizzes, capstones, the certificate.
- **Running thread.** *"Could a computer learn to do this?"* — opened by the Iris "tell the species
  apart" demo (the P0 chapter) and revisited as each concept is named. Persona framing: "Asha," the
  non-CS career-switcher from `ROADMAP §1`.

| # | Chapter | One-line | Tier | Compute |
|---|---------|----------|------|---------|
| 1 | Train your first model — in your browser | Fit + predict a classifier client-side, zero install (**ships from P0**). | 🟢 | browser |
| 2 | What you need & what it costs | The ₹0 path stated up front: browser now, free Colab/Ollama later, the one optional spend (M11) named honestly. | 🟢 | browser |
| 3 | What is AI, really? | Plain-language definition via everyday examples; AI as *learned behaviour*, not magic. | 🟢 | browser |
| 4 | AI vs ML vs DL vs GenAI — a family tree | How the terms nest, one concrete example per branch; a GenAI *taste* via a browser widget (P1-D3). | 🟢 | browser |
| 5 | A 10-minute history of AI | Perceptron → deep learning → transformers → foundation & reasoning models; stable, version-light. | 🟢 | browser |
| 6 | How this school works | Tiers, learning tracks, runnable code, auto-graders, quizzes, capstones, spaced review, the certificate. | 🟢 | browser |

> Ordering note: chapters are shown **wow-first** (run a model, then "here's the ₹0 path", then the
> concepts). Confirmed/changed in **P1-D1**.

### M1 — Python for AI 🟢 · browser

- **Learning objectives.** Enough Python to *handle data*: read/clean a file, write a function,
  use the core data structures, debug from a traceback, and write code a beginner can re-read —
  clarity over cleverness.
- **Running thread.** One small, deliberately **messy CSV** (proposed: `habits.csv` — `date, steps,
  sleep_hours, mood`, synthetic/CC0-by-us so we control the mess) cleaned a little more each chapter,
  culminating in the capstone cleaning script. `🧱 For Java developers` callouts thread the builder's
  own onboarding (dynamic typing, indentation-as-syntax, duck typing).

| # | Chapter | One-line | Tier | Compute |
|---|---------|----------|------|---------|
| 1 | Variables & types | Numbers, strings, booleans; dynamic typing (and what that means vs Java). | 🟢 | browser |
| 2 | Control flow | `if`/`for`/`while` driven by rows of the habits data. | 🟢 | browser |
| 3 | Functions | Define, arguments, return values; the unit of reuse. | 🟢 | browser |
| 4 | Data structures | Lists, dicts, sets, tuples — what each is for. | 🟢 | browser |
| 5 | Comprehensions | Concise list/dict transforms over data. | 🟢 | browser |
| 6 | Reading & writing files (CSV/JSON) | Get data in and out (Pyodide in-memory files). | 🟢 | browser |
| 7 | Errors & exceptions | `try`/`except`; failing safely on bad rows. | 🟢 | browser |
| 8 | Reading a traceback | Decode a stack trace to find the bug (may merge with Ch7 — see P1-D5). | 🟢 | browser |
| 9 | Just-enough OOP | Classes/objects you'll meet in libraries (no inheritance deep-dive). | 🟢 | browser |
| 10 | Clean, readable code | Naming, small functions, comments that earn their place. | 🟢 | browser |
| 11 | Pythonic data idioms | `zip`/`enumerate`/`dict.get`/unpacking for data work. | 🟢 | browser |
| 12 | A NumPy preview | Arrays and vectorized thinking — the bridge to M2/M3. | 🟢 | browser |
| 13 | Environments & packages (venv/pip) | How real projects pin dependencies (conceptual — see P1-D6). | 🟢 | browser |
| 14 | Notebooks, the IDE & Colab | Where you'll write code: in-browser vs local vs Colab (conceptual — see P1-D6). | 🟢 | browser |

### M2 — Math You Actually Need 🟢→🟡 · browser

- **Learning objectives.** Build *intuition* (picture before symbol) for the linear algebra,
  calculus, and probability that AI actually uses — enough to understand one neuron and, later,
  backprop.
- **Running thread.** *"Assemble one neuron, piece by piece."* Each chapter adds a Lego brick that
  the final chapter snaps together. Recurring concrete examples: **movie taste as vectors** (for
  similarity), **"predict the tip from the bill"** single-feature line (for derivatives/gradients).
  All visuals via Matplotlib in Pyodide.

| # | Chapter | One-line | Tier | Compute |
|---|---------|----------|------|---------|
| 1 | Why math for AI (and how little you need to start) | Sets fear aside; the map of what's coming. | 🟢 | browser |
| 2 | Vectors & geometry | Points and arrows; data as vectors. | 🟢 | browser |
| 3 | Matrices as transformations | A matrix moves space; see it. | 🟢 | browser |
| 4 | Matrix multiplication, intuitively | What matmul *does* before how it's computed. | 🟡 | browser |
| 5 | Dot products & similarity | How "alike" two vectors are (movie taste). | 🟢 | browser |
| 6 | Derivatives = sensitivity | How an output reacts to a nudge in the input. | 🟡 | browser |
| 7 | Gradients | The downhill direction; a ball rolling on a surface. | 🟡 | browser |
| 8 | The chain rule | The engine of backprop, built from the tip example. | 🟡 | browser |
| 9 | Probability basics | Chance, events, independence. | 🟢 | browser |
| 10 | Distributions | The shapes randomness takes. | 🟡 | browser |
| 11 | Mean, variance & standard deviation | Summarizing data in three numbers. | 🟢 | browser |
| 12 | Bayes, intuitively | Updating belief with evidence. | 🟡 | browser |
| 13 | Correlation vs causation | What data can and can't tell you. | 🟢 | browser |
| 14 | Sampling & uncertainty | Why a sample isn't the truth. | 🟡 | browser |
| 15 | Linear algebra in NumPy | Do the above in code, fast. | 🟡 | browser |
| 16 | The math of one neuron | Snap the pieces together: forward + backward pass by hand. | 🟡 | browser |

### M3 — Data & Tooling 🟢→🟡 · browser

- **Learning objectives.** Load, clean, explore, and visualize real data with NumPy/Pandas/
  Matplotlib; run a repeatable EDA; understand reproducibility and data-ethics *as habits*.
- **Running thread.** One real, **license-clean, Pyodide-loadable** public dataset threaded through
  (proposed: **Palmer Penguins, CC0** — see P1-D2/P1-D8). The capstone deliberately uses a
  *different* public dataset to test transfer.

| # | Chapter | One-line | Tier | Compute |
|---|---------|----------|------|---------|
| 1 | NumPy & vectorization | Array math without Python loops. | 🟢 | browser |
| 2 | Pandas Series & DataFrame | The data table you'll live in. | 🟢 | browser |
| 3 | Indexing & selection | Get exactly the rows/columns you want. | 🟢 | browser |
| 4 | Cleaning data | Missing values, wrong types, duplicates. | 🟡 | browser |
| 5 | Joins & groupby | Combine tables; aggregate by group. | 🟡 | browser |
| 6 | Reshaping | Long vs wide; pivot and melt. | 🟡 | browser |
| 7 | Plotting with Matplotlib | See your data; the core chart types. | 🟢 | browser |
| 8 | Statistical plots | Distributions & relationships (library choice — P1-D7). | 🟡 | browser |
| 9 | The EDA workflow | A repeatable first look at any dataset. | 🟡 | browser |
| 10 | Scaling & encoding (a preview) | Prep features for a model (preview only; depth in M4). | 🟡 | browser |
| 11 | Notebooks vs scripts | When to use which (conceptual — P1-D6). | 🟢 | browser |
| 12 | Environments & reproducibility | Pin it so it runs tomorrow (conceptual; overlaps M1 Ch13 — P1-D6). | 🟡 | browser |
| 13 | Data ethics (a preview) | Consent, bias, provenance — the habits, early. | 🟢 | browser |
| 14 | Messy real-world data | A guided tour of what actually breaks. | 🟡 | browser |

---

## 3. Decisions to make now

Each has a provisional ID (`P1-Dn`); on confirmation they are logged in `DECISIONS.md` as `D0015+`.
**The recommended option is listed first.** Pedagogical decisions first, then technical.

> **Confirmation status (2026-06-28).** **All P1 decisions are CONFIRMED at their recommended
> option (A)** and logged in `DECISIONS.md`: the pedagogical set (**P1-D1, P1-D2, P1-D3, P1-D4,
> P1-D5**) as **D0015**, and the technical set (**P1-D6, P1-D7, P1-D8, P1-D9, P1-D10, P1-D11**) as
> **D0016**. P1-D2/D3/D5/D7 were confirmed directly in the grooming Q&A; the remainder were approved
> at their recommended option with the spec.

### Pedagogical

**P1-D1 — M0 chapter ordering.**

- **(A, rec.) Wow-first, then cost, then concepts:** `1 Run a model → 2 What it costs → 3 What is
  AI → 4 Family tree → 5 History → 6 How this school works.` Honours "taste before theory"
  (`STYLE_GUIDE §2`), keeps the already-built P0 chapter as Ch1, and still satisfies "ships the
  cost chapter up front" (Ch2). *Con:* the existing chapter's `chapter: 1` is fine, but the cost
  chapter lands before the "what is AI" framing.
- (B) Concept-first: `1 What is AI → … → run a model last.` More like a textbook. *Con:* violates
  taste-before-theory; demotes the strongest hook; renumbers the P0 chapter.
- (C) Cost-chapter as Ch1 (₹0 promise literally first). *Con:* opens with logistics, not a win;
  weak hook for a cold lander.

**P1-D2 — Per-module running examples / datasets.** (One bundle decision.)

- **(A, rec.)** M0 = the Iris "tell species apart" demo + the "Asha" persona; **M1 = a synthetic
  messy `habits.csv`** (we author it → zero license risk, full control over the mess); **M2 = the
  "one neuron" assembly thread** (movie-taste vectors + tip-vs-bill line); **M3 = Palmer Penguins
  (CC0)**, capstone on a different public set. Rationale: relatable, license-clean, Pyodide-safe,
  and each thread builds to its capstone. *Con:* a synthetic M1 set is less "real" than a public one.
- (B) Use one real public dataset (e.g. Titanic) across *all* of M1–M3. *Con:* Titanic's framing
  (survival) is morbid for a first-ever dataset; one set can't serve both "messy-CSV teaching" and
  "clean EDA"; licensing/imagery vary.
- (C) Let each chapter pick its own example. *Con:* breaks `STYLE_GUIDE §4` (one running example per
  module); re-teaches context every chapter; worse for retention (R12).

**P1-D3 — The M0 GenAI "taste" (the deferred P0 Q-A).** How a beginner *feels* generative AI in M0
without breaking ₹0/browser.

- **(A, rec.) An embedded client-side `transformers.js` widget** (sentiment or image-caption) in
  M0 Ch4, runnable in the browser with no Python, no key, no Colab. Keeps the whole module
  `browser`/₹0; gives a genuine GenAI moment. *Con:* it's JS, outside the Pyodide grader path (so
  it's a demo, not an exercise); a small model download on first use.
- (B) Keep M0 to the scikit-learn taste only; defer all GenAI feel to M7+. *Con:* M0's promise is
  "what is AI *today*"; an all-classical taste under-sells GenAI for a 2026 audience.
- (C) An "Open in Colab" HF `pipeline()` demo. *Con:* introduces Colab in P1 (a non-goal); adds
  friction to the very first module; not ₹0-frictionless.

**P1-D4 — Beginner-scaffolding convention (applied across all ~50 chapters).**

- **(A, rec.) A small fixed scaffolding kit:** every chapter opens with a one-line *"You'll need
  from before"* recap; exercises always run **guided → implement → stretch**; `🧱 For Java
  developers` callouts in M1; a per-chapter "If you're stuck" hint before the hidden solution.
  Consistency aids retention (R12) and is lintable. *Con:* mild authoring overhead per chapter.
- (B) Free-form scaffolding per author judgement. *Con:* inconsistent UX across 50 chapters;
  un-lintable; weaker for true beginners.
- (C) Heavy scaffolding (worked sub-steps for every exercise). *Con:* slows confident learners;
  more to maintain.

**P1-D5 — Chapter granularity (scope control on ~50 chapters).**

- **(A, rec.) Keep PLAN's counts (6/14/16/14) but allow ≤3 documented merges** where two chapters
  are thin (candidate merges: M1 Ch7+Ch8 errors+tracebacks; M2 Ch10+Ch11 distributions + mean/
  variance; M3 Ch11+Ch12 notebooks + environments). Each merge logged. Protects pace while keeping
  single-idea chapters. *Con:* counts may drift from PLAN by a few.
- (B) Hold counts exactly. *Con:* some chapters are <1,000 words of real content (pads or splits
  awkwardly).
- (C) Aggressively consolidate to ~35 chapters. *Con:* breaks "one concept per chapter"; harder for
  beginners; diverges from PLAN materially.

### Technical

**P1-D6 — How environment/tooling chapters satisfy the "runnable example" gate.** Pyodide cannot
run `pip`/`venv`/a real IDE, yet `STYLE_GUIDE §2.3` requires a runnable example. Affects M1 Ch13–14
and M3 Ch11–12.

- **(A, rec.) Conceptual `browser` chapters with a runnable *in-scope proxy*** — e.g. the venv/pip
  chapter runs `import sys; help("modules")` / inspects `sys.path` / shows `micropip` *as the
  Pyodide analogue of pip*, and ships a **copy-paste, recorded** shell transcript (in a `> 💡` box)
  for the real local commands. The chapter still has a live cell; the OS-level commands are shown as
  verified output, not faked. *Con:* the live cell is illustrative, not the chapter's main act.
- (B) Tag these four as `compute: colab` with a recorded manual run. *Con:* introduces Colab into
  P1 (a non-goal); over-engineered for "here's how venvs work."
- (C) Make them pure prose with no code cell, and add a one-time linter exception. *Con:* breaks the
  uniform "every chapter has a runnable example" guarantee; special-cases the gate.

**P1-D7 — Plotting library for M3 statistical plots (Ch7–8).** *(Web-search updated — see §9: the
old "may not have a Pyodide wheel" worry is resolved. Seaborn's codebase is **pure Python** and all
its deps (numpy/pandas/matplotlib/scipy) ship in Pyodide, so `micropip.install("seaborn")` works.
The real trade-off is therefore **zero-install built-in vs a runtime network install**, not
"works vs doesn't".)*

- **(A, rec.) Matplotlib-only.** Matplotlib is **built into Pyodide** (zero install, no network,
  works offline — `STYLE_GUIDE §8`). Teach distributions/relationships with Matplotlib; show Seaborn
  as "a friendlier wrapper you'll meet later" in a `🔬` box with a one-line `micropip` install the
  curious can run. *Con:* slightly more verbose than Seaborn one-liners.
- (B) Matplotlib + Seaborn (Seaborn via `micropip.install` at runtime). **Feasible** (§9). *Con:*
  adds a first-use network download (breaks the offline/patchy-internet promise for that chapter)
  and a non-built-in import the R3 lint must explicitly allow as micropip-installed; heavier for a
  foundational chapter whose point is *seeing* data, not the plotting API.
- (C) Plotly (interactive, JS-rendered). *Con:* different mental model; heavier; not the standard a
  beginner meets in M4+ tutorials.

**P1-D8 — Dataset loading in Pyodide (M1 & M3).**

- **(A, rec.) Vendor small CSVs in-repo** (`/modules/<NN>/data/*.csv`, each ≤~50 KB) and load via a
  tiny `lib/data.py` helper that reads the bundled file; **Palmer Penguins shipped as a vendored CSV**
  (confirmed **CC0 1.0** — §9); sklearn/`load_*` built-ins used where they exist (Iris).
  Deterministic, offline-friendly (`STYLE_GUIDE §8` patchy-internet), license logged in
  `docs/ASSETS.md` (R11). *Con:* a few small data files in the repo. *(Note: a pure-Python
  `palmerpenguins` PyPI package exists and is micropip-installable, but vendoring the CSV avoids a
  runtime network fetch and keeps CI's twin notebooks offline-deterministic.)*
- (B) Fetch datasets from a URL at runtime (`pyodide.http`/`fetch`). *Con:* needs internet,
  breaks offline; flaky in CI's twin notebooks; external-dependency risk (R13).
- (C) Generate all data synthetically in-cell. *Con:* fine for M1's `habits.csv`, but M3's EDA must
  use *real* data to be honest (`Larnix-PLAN.md` M3 mantra).

**P1-D9 — Grader reuse across ~50 chapters (scaling D0009).** P0 pasted `lib/grader.py` into a
`#| edit: false` setup cell per chapter — fine for one chapter, duplicated 50× now.

- **(A, rec.) Load `lib/grader.py` into the Pyodide VFS once** via quarto-live's **`resources:`
  front-matter key** — confirmed (§9): "add the path to the `resources` key… quarto-live will
  automatically download named resources into the WebAssembly VFS as Python starts up." So chapters
  call `run_tests(...)` without pasting the helper. Single source of truth; the CPython unit tests in
  `lib/test_grader.py` remain the off-browser evidence (D0009). *Con:* one-time plumbing + must
  verify the include/import path from `modules/<NN>/`.
- (B) Keep pasting the helper per chapter. *Con:* 50× duplication; a grader bug means 50 edits;
  contradicts "small reviewable diffs."
- (C) Publish the grader as a pip/micropip package. *Con:* over-engineered for one file; adds an
  install step to every browser chapter.

**P1-D10 — Twin-notebook duplication at scale (scaling D0010).** Each browser chapter ships a CI
`.ipynb` twin running the worked example + exercise solutions under CPython (R10).

- **(A, rec.) A small generator** (`infra/ci/make_twin.py`) that extracts tagged `{pyodide}` cells
  and exercise solutions from the `.qmd` into the twin, so the twin can't silently drift from the
  chapter. Run in CI as a check (twin matches source) + committed. *Con:* a tool to build/maintain.
- (B) Hand-author every twin (the P0 approach). *Con:* 49 hand-maintained duplicates; drift risk;
  the exact thing D0010 flagged as a future improvement.
- (C) Drop twins; rely on a headless-browser smoke test of the live cells. *Con:* slow/flaky; heavy
  infra; rejected in D0010 for P0 and no cheaper at scale.

**P1-D11 — Module quiz structure.** P0 shipped one per-chapter `quiz.yml`. Modules now need a
module-level quiz (`CLAUDE.md` repo conventions: `quiz.yml` per module).

- **(A, rec.) Per-chapter "quick check" (2–3 MCQ) + one cumulative module quiz** (`module-quiz.yml`,
  ~8–12 MCQ) that the engine renders on the module README/landing. Reuses the P0 quiz engine and
  schema; gives both immediate recall and end-of-module consolidation (Varsity model). *Con:* two
  quiz artifacts per module.
- (B) Only a single end-of-module quiz. *Con:* loses the per-chapter recall checks that aid
  retention (R12).
- (C) Only per-chapter checks, no module quiz. *Con:* breaks the Varsity "end-of-module quiz →
  certification" model and the per-module DoD.

> **Deferred (recorded so they are *not* decided in P1):** stochastic-grader tolerances & GPU/Colab
> templates (P2); Ollama/free-API fallback pattern & `status: frontier` cadence (P3); M11 tokenizer
> / model size / GPU provider (P4); SR *scheduler*, certification exam, learning-track engine (P6).

---

## 4. Exercise & assessment plan

Every chapter ships **2–4 exercises**, scaffolded guided → implement → stretch (`STYLE_GUIDE §6`,
P1-D4), auto-graded by the `lib/grader.py` `run_tests([...])` assert harness running in Pyodide
(deterministic; off-browser evidence via `lib/test_grader.py`). Open-ended stretch tasks are
**rubric-graded** and labelled as such (R4). Each chapter seeds **3 spaced-repetition cards** from
its Key Takeaways (`review_cards:` block, schema-validated — P0-D3 convention).

### 4.1 Per-module exercise pattern (representative — full list authored per chapter)

| Module | Typical Ex 1 (guided 🟢) | Typical Ex 2 (implement 🟡, asserts) | Typical Ex 3 (stretch, rubric) |
|--------|--------------------------|--------------------------------------|--------------------------------|
| **M0** | Press-Run / complete one call | `accuracy(y_true,y_pred)` (already in Ch1) | Beat a baseline / explain a result |
| **M1** | Fill one line of a loop/function | Implement a CSV cleaner step (e.g. `drop_missing(rows)`) graded on known input/output | Extend the cleaner; handle a new mess type (rubric) |
| **M2** | Complete a vector/derivative expression | Implement `dot(a,b)`, `numeric_gradient(f,x)`, or a 1-neuron forward pass (asserts with float tolerance) | Re-derive/visualize a result a second way (rubric) |
| **M3** | Complete a Pandas selection | Implement a `groupby`/clean transform graded on a fixed DataFrame | An open EDA question on the data; defend with a plot + number (rubric) |

*Float-comparison note:* M2/M3 asserts use the grader's built-in tolerance (`tol`). No stochastic
training in P1, so no seeded-RNG tolerance design is needed (that's P2).

### 4.2 Module quizzes (P1-D11)

Per chapter: a 2–3-MCQ **quick check** (`{{< quiz quiz.yml >}}`). Per module: a cumulative
**`module-quiz.yml`** (~8–12 MCQ) covering the module's key ideas, rendered by the P0 JS engine,
scored client-side, answers + explanations shown, score in `localStorage`. Quiz YAML is
schema-linted in CI (`quiz_lint.py`).

### 4.3 Capstones + rubrics (one per module; format inherited from `modules/00-orientation/capstone.md`)

Each capstone is **rubric-graded** (0–2 per criterion; "Proficient" tops every row) and **must
report a number** ("did you measure it?", `ROADMAP §1` eval thread). All run in-browser at ₹0.

- **M0 — Set up & run.** *Brief:* confirm the ₹0 toolchain, run the Ch1 model, change one thing,
  report whether accuracy moved. *Rubric:* Runs · Correct (train-only fit, test-set accuracy) ·
  Measurement (before/after) · Explanation. *(Template already exists; finalize as real M0 content.)*
- **M1 — Data-cleaning notebook.** *Brief:* take the messy `habits.csv` and produce a clean,
  typed, de-duplicated table via your own functions. *Rubric:* Runs · Correctness (handles missing/
  types/dupes per spec) · Code quality (named functions, readable) · Reporting (rows-removed /
  before-after counts). *Auto-check component:* a graded final-shape/row-count assert + a rubric for
  code quality.
- **M2 — Math of one neuron.** *Brief:* implement a single neuron's forward pass and its gradient
  by hand (NumPy), verify the gradient against a numeric finite-difference. *Rubric:* Runs ·
  Correctness (analytic gradient matches numeric within tolerance) · Understanding (explains each
  term) · Measurement (reports the max gradient error). *Auto-check:* analytic-vs-numeric assert.
- **M3 — End-to-end EDA.** *Brief:* a full EDA on a *new* public dataset — load, clean, ≥3
  questions answered with plots + numbers, written findings. *Rubric:* Runs · Cleaning (documented,
  correct) · Insight (questions answered with evidence) · Measurement (every claim backed by a
  number/plot) · Ethics note (provenance/bias caveat). *Graded by rubric* (open-ended, R4).

### 4.4 Spaced-repetition seeding

~50 chapters × 3 cards ≈ **~150 review cards** authored in front-matter `review_cards:`, validated
by `review_cards_lint.py`. The P6 scheduler consumes them; P1 only guarantees the corpus exists and
validates, so no chapter needs retrofitting later.

---

## 5. Quality plan

### 5.1 Runs in CI vs Colab-verified

- **All P1 chapters run in CI (blocking).** Every chapter is `browser`; each ships a CPython
  **twin `.ipynb`** (P1-D10) executed by `run_notebooks.py` (R10). **Zero Colab-verified content in
  P1** — there is no GPU/`colab` chapter (a non-goal). The M0 transformers.js widget (P1-D3) is
  client-side JS: it is **not** in the notebook-execution path and is verified by a manual
  browser-preview note in its PR (it carries no grader).

### 5.2 Lint / link / spell gates (all from P0, blocking on every PR)

- **Prose tone:** Vale + the Larnix style (banned words: `simply`, `just`, `obviously`,
  `trivially`, hype). **Markdown:** markdownlint-cli2. **Spelling:** codespell (AI-term allow-list;
  extend for M2 math terms / M3 data terms). **Links:** lychee.

### 5.3 R-gates (from P0) + one new P1 check (blocking on PR)

- **R3 browser-import lint** — *the load-bearing gate this phase.* Every P1 chapter must import only
  Pyodide-safe packages. **New: extend `browser_import_lint.py` with an explicit Pyodide-safe
  allow-list** (numpy, pandas, matplotlib, scikit-learn, stdlib, `lib.*`, `micropip`) and **fail on
  anything else** (e.g. seaborn/torch). Packages that are *only* available via a runtime
  `micropip.install` (e.g. seaborn, if P1-D7-B is ever chosen) must be **explicitly annotated** in
  the chapter (a `# micropip:` marker the lint recognises) so an accidental bare `import torch`
  still fails. This catches the P1-D7 risk automatically. *(Pyodide's ~2 GB browser memory cap (§9)
  is comfortably clear for all foundation-scale data.)*
- **R6 free-fallback** — no-op (nothing needs a key); the gate stays green by construction.
- **R10 runs-in-CI** — every chapter's twin executes clean; a broken example fails the build.
- **R1 currency** — no-op (no `status: frontier` chapters); mechanism runs.
- **New — dataset license ledger (R11):** a `docs/ASSETS.md` entry for every dataset (name, source,
  license, where used); a small `infra/ci/assets_check.py` fails if a `data/` file isn't ledgered.

### 5.4 Accessibility (from P0, blocking)

`a11y_check.py` (alt-text presence + WCAG-AA contrast). **Every M2/M3 plot and M0 diagram needs
alt-text** describing the takeaway (not just "a chart") — added to the correctness checklist.

### 5.5 Correctness-review checklist (per-chapter PR gate — instantiates `STYLE_GUIDE §11` + R10)

The author ticks, for **every** chapter (✅ verified across all 50 chapters at phase close):

- [x] Every code cell executed in CI (twin) and previewed in-browser; outputs shown.
- [x] Every term defined on first use; no banned words; reads for a true beginner (the house test).
- [x] Numbers/claims verified; primary sources cited; no invented citations.
- [x] Front-matter complete + accurate (all 10 fields); `last_reviewed` set; `review_cards` present.
- [x] ₹0/`browser` path confirmed; R3 import lint clean (Pyodide-safe imports only).
- [x] Exercises have working asserts + hidden solutions; tiers match; stretch labelled rubric-graded.
- [x] Quiz answers + explanations verified; quick-check + module-quiz entries added.
- [x] Plots/diagrams have meaningful alt-text; no colour-only meaning.
- [x] Datasets used are ledgered in `docs/ASSETS.md` with a license (R11).

### 5.6 Scale-specific quality risks (new in P1)

- **R12 (drop-off):** P1 is the first long stretch a learner walks. Mitigation baked into design —
  short single-idea chapters, wow-first M0, consistent scaffolding (P1-D4), a satisfying capstone
  per module. (Analytics are post-launch; design is the lever now.)
- **R9 (maintenance burden):** ~50 chapters is the first real surface. Mitigation — single-source
  grader (P1-D9), generated twins (P1-D10), one running example per module (less re-authoring),
  and the merge allowance (P1-D5).
- **Consistency:** because authoring spans many sessions, a `docs/AUTHORING_CHECKLIST` (or reuse of
  §5.5) is pinned in each chapter PR so chapter #1 and chapter #50 read as one voice.

---

## 6. Task breakdown (ordered, independently committable)

Each task ≈ one commit/PR. **Shared tooling (§6.A) lands before content scale** (the "evals before
features" discipline applied within the phase), then modules in dependency order. Per `CLAUDE.md`,
each non-trivial chapter gets a one-paragraph plan (hook, worked example, exercises, twin/grader,
risks) approved before authoring.

> ✅ **All tasks (1–67) complete (2026-06-29).** §6.A shared tooling, §6.B M0 (6 ch), §6.C M1 (14 ch),
> §6.D M2 (16 ch), §6.E M3 (14 ch), and §6.F integration all delivered and committed on
> `feat/p1-foundations-spec`. **P1-D5 merge log: 0 of 3 optional merges used** — M1 Ch7/Ch8 and
> M3 Ch11/Ch12 were each kept as separate chapters (final counts 6/14/16/14 = 50).

### 6.A — Shared tooling first (unblocks all chapters)

1. **Grader single-source (P1-D9)** — load `lib/grader.py` into the Pyodide VFS / shared include;
   prove `run_tests` works from a `modules/<NN>/` chapter without pasting; keep CPython tests green.
2. **Twin generator (P1-D10)** — `infra/ci/make_twin.py` + a CI check that the committed twin
   matches the chapter source; unit tests; migrate the M0 Ch1 twin to the generated form.
3. **Module-quiz support (P1-D11)** — `module-quiz.yml` schema + engine mount on module READMEs;
   extend `quiz_lint.py`; per-chapter quick-check convention documented.
4. **Pyodide-safe allow-list (R3 extension)** — extend `browser_import_lint.py` with the explicit
   allow-list; tests for a pass (pandas) and a fail (seaborn/torch).
5. **Dataset helper + license ledger (P1-D8, R11)** — `lib/data.py` loader; vendor Palmer Penguins
   CSV + author `habits.csv`; create `docs/ASSETS.md` + `infra/ci/assets_check.py` + tests.
6. **Module scaffolding** — copy the capstone-template + README skeleton into M1/M2/M3; finalize the
   beginner-scaffolding kit (P1-D4) as a short authoring note + (where lintable) a check.

### 6.B — M0 (5 new chapters; Ch1 ships from P0)

7. Reconcile M0 ordering/numbering per P1-D1; update `modules/00-orientation/README.md`.
8. M0 Ch — *What you need & what it costs* (the ₹0 path up front).
9. M0 Ch — *What is AI, really?*
10. M0 Ch — *AI vs ML vs DL vs GenAI* (+ transformers.js taste widget, P1-D3).
11. M0 Ch — *A 10-minute history of AI.*
12. M0 Ch — *How this school works.*
13. M0 — module quiz + finalize the M0 capstone as real graded content + walkthrough.

### 6.C — M1 Python for AI (14 chapters + assessment)

14–27. One task per chapter (M1 Ch1…Ch14), each: chapter `.qmd` + twin + exercises + quick-check +
review cards. *(Apply the P1-D5 merge if Ch7/Ch8 are thin.)*
28. M1 — module quiz (`module-quiz.yml`).
29. M1 — capstone (data-cleaning notebook) + rubric + auto-check + walkthrough; README finalize.

### 6.D — M2 Math You Actually Need (16 chapters + assessment)

30–45. One task per chapter (M2 Ch1…Ch16). *(Apply P1-D5 merge if Ch10/Ch11 are thin.)*
46. M2 — module quiz.
47. M2 — capstone (math of one neuron: analytic vs numeric gradient) + rubric + auto-check +
    walkthrough; README finalize.

### 6.E — M3 Data & Tooling (14 chapters + assessment)

48–61. One task per chapter (M3 Ch1…Ch14). *(Apply P1-D5 merge if Ch11/Ch12 are thin.)*
62. M3 — module quiz.
63. M3 — capstone (end-to-end EDA on a new public dataset) + rubric + walkthrough; README finalize.

### 6.F — Phase integration + DoD ✅ complete

64. ✅ Nav/landing update: M0–M3 listed as live in `_quarto.yml` sidebar + `index.qmd` course catalog
    (each module tile marked Available with a landing link).
65. ✅ Full **fresh-clone build + green CI** pass across all 50 chapters; all 50 twins execute; no
    cross-chapter link/nav/lint issues. (Found + fixed M2 Ch12's missing `live-html`/`execute` block
    and added a render-safety guard to `chapter_structure_lint.py`.)
66. ✅ **₹0 confirmation pass:** every one of the 50 chapters loaded in a real browser and run on
    Pyodide — all PASS; the four capstone code paths run client-side (Iris, habits cleaning,
    one-neuron gradient check 3.27e-11, EDA stack); offline load of vendored datasets confirmed live.
67. ✅ **Docs:** `D0015+` decisions logged; `PORTFOLIO.md` quantified bullet added; `RUNBOOK.md`
    authoring-at-scale note added; `docs/WALKTHROUGH.md` extended with the zero→EDA learner path.

---

## 7. Definition of Done (P1)

Instantiates `ROADMAP §3 P1` exit criteria, expanded against the `CLAUDE.md` generic DoD and the
per-chapter Varsity contract (`STYLE_GUIDE §11`). ✅ **P1 is DONE — all items hold (2026-06-29):**

- [x] **M0–M3 complete** (50 chapters); **every chapter passes the Varsity contract** (hook →
      explanation → runnable example → Key Takeaways → 2–4 graded exercises) with complete, accurate
      10-field front-matter incl. `last_reviewed` and `review_cards`. *(Enforced by
      `chapter_structure_lint.py` + `frontmatter_lint.py` + `review_cards_lint.py` — all green.)*
- [x] **100% of M0–M3 notebooks run in JupyterLite/Pyodide (₹0 confirmed)** *and* **every chapter's
      CPython twin executes cleanly in CI** (R10). The R3 import lint confirms all imports are
      Pyodide-safe. *(All 50 twins execute; Task 66 ran all 50 live in-browser — PASS.)*
- [x] **Each module has a quiz** (per-chapter quick checks + a cumulative `module-quiz.yml`) **and a
      graded capstone with a rubric**; every capstone requires a measured number ("did you measure
      it?"). *(4 module quizzes scored 10/11/12/12 in-browser; 4 capstones finalized with rubrics.)*
- [x] **M0 ships "What you need & what it costs"** stating the ₹0 path up front. *(M0 Ch2.)*
- [x] **Exercises have working auto-graders + hidden solutions**; stretch tasks are labelled
      rubric-graded (R4). The grader is single-sourced (P1-D9); twins are generated/verified (P1-D10).
- [x] **CI green across the whole phase:** notebook execution (R10), Vale, markdownlint, codespell,
      lychee, a11y (alt-text + contrast), R1/R3/R6 gates, and the new assets-ledger check.
      *(8 gate scripts + 111 unit tests green; codespell clean; zero banned/hype words in content.)*
- [x] **All datasets ledgered in `docs/ASSETS.md` with a license** (R11); no un-ledgered `data/` file.
      *(penguins.csv CC0-1.0; habits.csv CC0-by-us; `assets_check.py` green.)*
- [x] **A non-technical learner can go zero → EDA capstone entirely in-browser at ₹0** — a clickable
      "5-minute (and full) walkthrough" path recorded in `docs/WALKTHROUGH.md`.
- [x] **Builds cleanly from a fresh clone**; a preview deploy renders M0–M3 correctly with working
      nav/search; the landing catalog shows M0–M3 live. *(Full site renders 61 docs; fresh-clone
      gates + twins re-verified.)*
- [x] **`DECISIONS.md` updated** with confirmed `D0015+` (P1-Dn) incl. the §6.F completion note;
      **`STYLE_GUIDE.md` adhered to** (lint/prose pass); module READMEs complete.
- [x] **`PORTFOLIO.md`** carries a quantified P1 bullet ("authored + auto-graded **50 in-browser
      chapters across 4 foundation modules, 100% runnable at ₹0**, with per-chapter review cards
      and 4 rubric-graded capstones").

---

## 8. Open questions (need your input before / during the build)

> ✅ **All resolved (2026-06-28) and logged in `DECISIONS.md` D0015–D0016.** Q-1→P1-D2 (synthetic
> `habits.csv` + Palmer Penguins CC0); Q-2→P1-D7 (Matplotlib-only, Seaborn as an optional note);
> Q-3→P1-D3 (client-side transformers.js taste); Q-4→P1-D6 (env/tooling chapters stay
> `browser`-conceptual with a runnable proxy + recorded transcript); Q-5→P1-D5 (merges allowed but
> **0 used** — counts held at 6/14/16/14); Q-6 (kept `🧱 For Java developers` as collapsible asides);
> Q-7 (M1/M2 capstones pair an auto-check with a rubric, M3 rubric-only); Q-8 (M0 = ₹0 what/why
> setup; M1/M3 = how-it-works under the hood). Originals preserved below for the record.

Focused ambiguities and missing-topic risks. Most map to a decision above; a few need a call.

- **Q-1 — Running datasets (→ P1-D2).** OK to author a synthetic `habits.csv` for M1 and use Palmer
  Penguins (CC0) for M3 (capstone on a different public set)? If you'd rather a specific real
  dataset (e.g. a domain you care about for the portfolio), name it.
- **Q-2 — Seaborn in M3 (→ P1-D7).** *Web search resolved the feasibility question (§9): Seaborn is
  pure-Python and installs in Pyodide via `micropip`, so it **can** be taught — but only at the cost
  of a first-use network download (no longer offline) and a non-built-in import.* My recommendation
  is therefore **Matplotlib-only** (built-in, zero-install, offline), with Seaborn shown as an
  optional `🔬` install-it-yourself note. Confirm, or say if you'd rather teach Seaborn proper.
- **Q-3 — M0 GenAI taste (→ P1-D3).** Is a client-side **transformers.js** widget the right "feel
  GenAI" moment for M0, or do you prefer to keep M0 purely classical and defer GenAI to M7+?
- **Q-4 — Environment chapters (→ P1-D6).** Agree that venv/pip/IDE/notebooks chapters stay
  `browser`-conceptual with a runnable Pyodide proxy + recorded shell transcript, rather than being
  promoted to `colab`? (Keeps P1 Colab-free.)
- **Q-5 — Chapter merges (→ P1-D5).** Do you want me to hold PLAN's exact counts (6/14/16/14), or
  may I merge up to 3 thin chapter-pairs (documented) to protect pace?
- **Q-6 — M1 "for Java developers" callouts.** These serve the *builder's* onboarding but sit in
  *learner* content. Keep them as collapsible `🧱` optional asides (recommended — they don't burden
  a non-Java beginner), or pull them into a separate builder-notes appendix?
- **Q-7 — Capstone grading mix.** For M1/M2 I propose a small **auto-check** (final shape / gradient
  error) *plus* a rubric. Acceptable, or do you want capstones to be rubric-only (purely
  human-judged) like M3?
- **Q-8 — Track placement of "setup".** M1 Ch13–14 (venv/pip, IDE/Colab) overlap M0's cost/setup
  chapter and M3 Ch11–12 (notebooks, environments). Confirm the split: **M0 = the ₹0 *what/why*
  one-time setup; M1/M3 = the *how it works* under the hood.** (Avoids teaching setup three times.)

---

*On approval, I will: (1) log the confirmed `P1-Dn` decisions in `DECISIONS.md` as `D0015+`, then
(2) begin §6.A Task 1 (grader single-source) — one small, reviewable commit at a time, planning
each non-trivial chapter before authoring, per `CLAUDE.md`. No chapter or code is written until
this spec and its decisions are confirmed.*

---

## 9. Validation log (web search, 2026-06-28)

Every load-bearing technical claim in this spec was checked against current sources. **Result: all
core assumptions hold; two findings sharpened a decision** (Seaborn feasibility → P1-D7; grader
VFS mechanism confirmed → P1-D9).

| Claim in spec | Verdict | Evidence |
|---|---|---|
| **Pyodide ships NumPy, pandas, SciPy, Matplotlib, scikit-learn** built-in (the whole M1–M3 stack runs zero-install) | ✅ Confirmed | Pyodide v314.0.1 *"Packages built in Pyodide"* + repo README: scientific stack "including NumPy, pandas, SciPy, Matplotlib, and **scikit-learn**." |
| **Iris/penguins-scale data + foundation work fits the browser** | ✅ Confirmed | Pyodide runs CPython on WASM; ~2 GB browser memory cap (marimo/WASM notes) — far above foundation-scale data. |
| **Seaborn can run in Pyodide** (was flagged as a risk in P1-D7) | ✅ Feasible (→ refines P1-D7) | seaborn docs: *"The seaborn codebase is **pure Python**"*; deps (numpy/pandas/matplotlib/scipy) are Pyodide built-ins; **micropip installs any pure-Python wheel from PyPI at runtime**. So the trade-off is zero-install vs runtime network install — **not** "works vs doesn't." Recommendation stays Matplotlib-only for offline/₹0. |
| **Datasets vendor-loadable + license-clean** — Palmer Penguins is CC0 | ✅ Confirmed | `allisonhorst/palmerpenguins` LICENSE = **CC0 1.0 Universal**; HF mirror `license: cc0-1.0`; a pure-Python `palmerpenguins` PyPI package also exists (we still vendor the CSV for offline-determinism). |
| **`micropip` is the Pyodide analogue of `pip`** (P1-D6 env chapter proxy) | ✅ Confirmed | Pyodide *Loading packages* + `pyodide/micropip`: install from PyPI/CDN/URL in-browser; JupyterLite layers `piplite` on top. |
| **transformers.js runs HF pipelines in-browser, no server/key** (P1-D3 GenAI taste) | ✅ Confirmed, current | HF *Transformers.js* docs: *"Run 🤗 Transformers directly in your browser, with no need for a server"*; pipelines incl. **sentiment-analysis** + **image-classification** (ONNX Runtime Web). Active 2025–2026 guides. |
| **quarto-live loads local files into the Pyodide VFS via `resources:`** (P1-D9 single-source grader) | ✅ Confirmed | quarto-live *Loading Resources*: *"add the path to the `resources` key… quarto-live will automatically download named resources into the WebAssembly VFS as R or **Python** starts up."* |
| **quarto-live = Pyodide engine + exercises/hints/solutions/custom grading** (P0 carry-over, reused at scale) | ✅ Confirmed | `r-wasm/quarto-live`: "Interactive R and **Python** code blocks. Exercises with optional hints, solutions, and custom grading… only a static web service required." |
| **PEP 783 / WASM wheels on PyPI** (context for future package reach) | ✅ Noted | Pyodide 314.0 ships PEP 783 support — Python packages can publish WebAssembly wheels to PyPI (widens micropip's reach over time). |

### Net effect on decisions

- **P1-D7 (Seaborn):** the open "does it even work?" risk is **retired** — it works via micropip.
  The recommendation (Matplotlib-only) now rests on **offline/₹0 + zero-install**, an editorial
  call, not a capability limit. Q-2 reframed accordingly.
- **P1-D9 (grader single-source):** the `resources:` VFS mechanism is **confirmed**, so loading
  `lib/grader.py` once (instead of pasting it into ~50 chapters) is a safe, documented path — no
  spike needed.
- **P1-D8 (datasets):** Palmer Penguins **CC0** confirmed; vendoring chosen over the PyPI package
  for offline-deterministic CI twins.
- No decision was reversed; no new blocker surfaced.

*Sources (all fetched 2026-06-28): pyodide.org v314 packages + loading-packages + accessing-files;
github.com/pyodide/pyodide & /micropip; seaborn.pydata.org/installing; jupyterlite pyodide docs;
github.com/allisonhorst/palmerpenguins (LICENSE) + HF SIH/palmer-penguins; huggingface.co/docs/
transformers.js; r-wasm.github.io/quarto-live (Loading Resources) + github.com/r-wasm/quarto-live.*
