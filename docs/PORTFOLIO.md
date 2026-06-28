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
