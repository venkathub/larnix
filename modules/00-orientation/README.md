# M0 — Orientation

The on-ramp: what AI/ML is, what you need (and what it costs — ₹0 to start), and
your first hands-on model. No prior machine learning is assumed.

## Prerequisites

None. If you can open a web page, you can do this module.

## Learning objectives

By the end of M0 you can:

- Run Python in your browser with zero install.
- Train and call a scikit-learn classifier, and read its accuracy.
- Describe the machine-learning loop: load → split → train → predict → measure.

## Chapters

| # | Chapter | Tier | Compute | Status |
|---|---------|------|---------|--------|
| 1 | [Train your first model — in your browser](ch01-train-your-first-model.qmd) | 🟢 Beginner | `browser` | stable |

## Capstone

_(Module capstone + rubric are added when M0 is built out in P1. P0 ships this
one sample chapter to prove the platform; the capstone rubric format is shown as
a template artifact in P0 task 16.)_

## How to run

- **In your browser (₹0):** open the chapter and press **Run** on each code block —
  Python executes client-side via Pyodide, no install.
- **Reproduced in CI:** each browser chapter has a companion `*.ipynb` twin that
  runs the same code under CPython in CI (the R10 gate), so the examples are
  guaranteed to work.
