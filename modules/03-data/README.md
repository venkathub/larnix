# M3 — Data & Tooling

Load, clean, explore, and visualize real data with NumPy, Pandas, and Matplotlib;
run a repeatable EDA; and pick up reproducibility and data-ethics *as habits*.

## Prerequisites

- M1 — Python for AI and M2 — Math You Actually Need.
- Comfort with functions, lists/dicts, and a little NumPy.

## Learning objectives

By the end of M3 you can:

- Work fluently with NumPy arrays and Pandas `Series`/`DataFrame`.
- Index, clean, join, group, and reshape real tabular data.
- Plot the core chart types and read distributions and relationships.
- Run a repeatable EDA on a dataset you've never seen, and report findings with
  numbers and plots.

## Running example

One real, license-clean dataset threaded through: **Palmer Penguins (CC0** — see
`docs/ASSETS.md`), loaded offline from a vendored CSV via `lib/data.py`. The
capstone deliberately uses a *different* public dataset to test transfer.

## Chapters

🟢→🟡 · `browser` · `stable`. (Authored across P1; Ch11+Ch12 may merge — P1-D5.)

| # | Chapter | Tier |
|---|---------|------|
| 1 | NumPy & vectorization | 🟢 |
| 2 | Pandas Series & DataFrame | 🟢 |
| 3 | Indexing & selection | 🟢 |
| 4 | Cleaning data | 🟡 |
| 5 | Joins & groupby | 🟡 |
| 6 | Reshaping | 🟡 |
| 7 | Plotting with Matplotlib | 🟢 |
| 8 | Statistical plots | 🟡 |
| 9 | The EDA workflow | 🟡 |
| 10 | Scaling & encoding (a preview) | 🟡 |
| 11 | Notebooks vs scripts — conceptual | 🟢 |
| 12 | Environments & reproducibility — conceptual | 🟡 |
| 13 | Data ethics (a preview) | 🟢 |
| 14 | Messy real-world data | 🟡 |

## Assessment

- Per-chapter **quick check** (`quiz.yml`, 2–3 MCQ).
- Cumulative **module quiz** (`module-quiz.yml`, ~8–12 MCQ) on the module landing.
- **Capstone:** an end-to-end EDA on a *new* public dataset — see
  [`capstone.md`](capstone.md).

## How to run

- **In your browser (₹0):** open a chapter and press **Run**; data loads offline
  from the vendored CSV, plots render via Matplotlib — no install.
- **Reproduced in CI:** each chapter ships a generated `*.ipynb` twin executed
  under CPython (R10).
