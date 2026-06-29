# M1 — Python for AI

Enough Python to *handle data*: read and clean a file, write a function, use the
core data structures, debug from a traceback, and write code a beginner can
re-read. Clarity over cleverness, from the first line.

## Prerequisites

- M0 — Orientation (you've run a model in the browser and know the ₹0 path).
- No prior programming required. If you've coded before, the
  `🧱 For Java developers` asides translate the surprises.

## Learning objectives

By the end of M1 you can:

- Use Python's core types, control flow, functions, and data structures.
- Read and write CSV/JSON, and handle errors without crashing.
- Read a traceback and find the bug.
- Clean a small, messy real-world table with your own functions.

## Running example

One deliberately **messy `habits.csv`** (`date, steps, sleep_hours, mood`;
synthetic, CC0 — see `docs/ASSETS.md`) that you clean a little more each chapter,
culminating in the capstone cleaning script.

## Chapters

All 🟢 Beginner · `browser` · `stable`. (Authored across P1; Ch7+Ch8 may merge — P1-D5.)

| # | Chapter |
|---|---------|
| 1 | [Variables & types](ch01-variables-and-types.qmd) |
| 2 | [Control flow](ch02-control-flow.qmd) |
| 3 | [Functions](ch03-functions.qmd) |
| 4 | [Data structures](ch04-data-structures.qmd) |
| 5 | Comprehensions |
| 6 | Reading & writing files (CSV/JSON) |
| 7 | Errors & exceptions |
| 8 | Reading a traceback |
| 9 | Just-enough OOP |
| 10 | Clean, readable code |
| 11 | Pythonic data idioms |
| 12 | A NumPy preview |
| 13 | Environments & packages (venv/pip) — conceptual |
| 14 | Notebooks, the IDE & Colab — conceptual |

## Assessment

- Per-chapter **quick check** (`quiz.yml`, 2–3 MCQ).
- Cumulative **module quiz** (`module-quiz.yml`, ~8–12 MCQ) on the module landing.
- **Capstone:** a data-cleaning notebook — see [`capstone.md`](capstone.md).

## How to run

- **In your browser (₹0):** open a chapter and press **Run** on each code block —
  Python runs client-side via Pyodide, no install.
- **Reproduced in CI:** each chapter ships a generated `*.ipynb` twin executed
  under CPython (R10), so every example is guaranteed to run.
