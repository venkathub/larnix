# M1 Capstone — Data-cleaning notebook

> Skeleton authored in P1 §6.A.6: the brief + rubric are final; the graded
> auto-check and the hidden walkthrough are finalized with the M1 build (P1 §6.C).
> Runs in the browser, ₹0.

## The brief

Take the messy `habits.csv` (`date, steps, sleep_hours, mood`) and produce a
**clean, correctly typed, de-duplicated** table using your own functions. Handle
the messes you met across the module: missing values, stray units/formats
(`8h`, `7,500`), inconsistent mood labels (`Good`/`good`/` ok `), duplicate rows,
mixed date formats, and impossible values.

## Deliverables

- A runnable in-browser notebook that loads `habits.csv`, cleans it through small
  **named functions**, and prints the cleaned table.
- A short report of **what you removed/fixed** and the **before/after row counts**.

## Rubric

Score each criterion 0–2; a "Proficient" capstone scores at the top of every row.

| Criterion | Not yet (0) | Developing (1) | Proficient (2) |
|-----------|-------------|----------------|----------------|
| **Runs** | Errors or does not run | Runs with hand-holding | Runs top-to-bottom, unaided |
| **Correctness** | Misses most messes | Handles some (missing/types/dupes) | Handles missing values, types, duplicates, and bad labels per spec |
| **Code quality** | One long block | Some structure | Small, named, readable functions; clear names |
| **Reporting** | No counts | A count, not compared | Before/after row counts + a note of what was fixed |

**Auto-check (finalized with M1):** a graded assert on the cleaned table's final
shape / row count and dtypes, alongside the human-graded rubric above.

## Did you measure it?

Report **a number** — rows removed, or before→after counts. A capstone with no
measured result cannot score above *Developing*.

## What you need & what it costs

Runs in the browser via Pyodide — zero install, **₹0**. The dataset is vendored
(`modules/01-python/data/habits.csv`, CC0; see `docs/ASSETS.md`) and loads offline.
