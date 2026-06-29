# Portfolio

> Resume-ready, quantified bullets drafted as phases/modules complete.

## Larnix — open-access AI/ML learning platform · Phase P0 (platform + pedagogy gate)

*Solo build. Stack: Quarto, quarto-live/Pyodide, Python, GitHub Actions, GitHub Pages.*

- **Built a docs-as-code AI-course platform end-to-end and proved it on one
  zero-install sample chapter** — in-browser Python (Quarto + quarto-live/Pyodide),
  assert-based in-browser auto-grading, a dependency-free client-side quiz engine
  with `localStorage` progress, an "Open in Colab" GPU-notebook pattern, and a
  custom design system (difficulty/compute/status badges + a Key Takeaways box,
  light/dark) — deployed to GitHub Pages with automatic per-PR previews.
- **Engineered a 12-check CI quality pipeline** that makes the teaching contract
  mechanically enforceable: 3 schema linters (front-matter, quiz, spaced-repetition
  cards), 4 content R-gates (currency, Pyodide-safe imports, paid-API free-fallback,
  runs-in-CI notebook execution), prose-tone/spell/link checks (Vale + markdownlint +
  codespell + lychee), and a deterministic WCAG-AA accessibility gate. Backed by
  **8 tested gate scripts and 79 unit tests**.
- **Guaranteed "every example runs" without a GPU or a browser in CI**: browser
  chapters ship a CPython "twin" notebook executed by `nbclient`, while GPU/Colab
  notebooks are policy-skipped and manually verified — keeping **100% of the sample
  chapter runnable in-browser at ₹0**.
- **Documented 13 dated architecture-decision records** (platform stack, grader
  design, GPU-CI policy, single-project repo layout, a11y scope) for traceability
  and review.

*Why it matters: this is "evals before features" applied to content — the gates were
built and proven on one chapter before authoring at scale, so every later chapter
inherits a green, automated quality bar.*

## Larnix — open-access AI/ML learning platform · Phase P1 (foundations: M0–M3)

*Solo build. Stack: Quarto, quarto-live/Pyodide, Python (NumPy/Pandas/Matplotlib), GitHub Actions.*

- **Authored and auto-graded 50 runnable chapters across 4 modules** (Orientation,
  Python for AI, Math You Actually Need, Data & Tooling) — every chapter follows a
  hook → explanation → runnable worked example → Key Takeaways → 2–4 graded
  exercises contract, with **100% running in-browser at ₹0** (no install, no GPU,
  no account). Capped each module with a cumulative quiz (45 MCQ total) and a
  build-something capstone.
- **Guaranteed every example runs** by generating a CPython "twin" notebook for all
  50 chapters from their source — worked cells plus hidden-solution asserts — and
  executing all 50 cleanly in CI under `nbclient`; the math capstone derives one
  neuron's backprop by hand and **gradient-checks it to a 3.27e-11 max error**.
- **Built reusable in-browser infrastructure**: a single-source assert grader loaded
  into the Pyodide VFS, an offline dataset loader for vendored CC0 data (Palmer
  Penguins, 344×8), and client-side Matplotlib plots — so chapters stay DRY and
  every dataset/grader resolves identically in the browser and in CI.
- **Scaled authoring with parallel sub-agents under a fail-closed CI bar**: ~12 gate
  scripts and **111 unit tests** (front-matter/quiz/review-card schemas, Pyodide-safe
  imports, twin-drift, render-safety, WCAG-AA, prose/spell/banned-word) caught real
  defects (e.g. a missing render block) before merge; the full site (61 docs) renders
  cleanly and builds from a fresh clone.

*Why it matters: a complete beginner on a low-spec laptop can go from "what is AI" to
deriving a neuron's gradient by hand and running an EDA on real data — entirely free,
entirely in a browser — and every line is mechanically verified to run.*
