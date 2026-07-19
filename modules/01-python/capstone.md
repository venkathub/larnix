---
title: "M1 Capstone — Data-cleaning notebook"
---

> The Module 1 project. It runs entirely in your browser, at **₹0**. Graded by the
> rubric below; it must report **a number**.

## The brief

Take the messy `habits.csv` (`date, steps, sleep_hours, mood`) and produce a
**clean, correctly typed, de-duplicated** table using your own functions. Handle
the messes you met across the module: missing values, stray units/formats
(`8h`, `7,500`), inconsistent mood labels (`Good`/`good`/`ok`), duplicate rows,
mixed date formats (`07/01/2026` alongside `2026-01-07`), and impossible values
(`-5` steps, `26` sleep hours).

## Deliverables

- A runnable in-browser notebook that loads `habits.csv`, cleans it through small
  **named functions**, and prints the cleaned table.
- A short report of **what you removed/fixed** and the **before/after row counts**.

## Rubric

Score each criterion 0–2; a "Proficient" capstone scores at the top of every row.

| Criterion | Not yet (0) | Developing (1) | Proficient (2) |
|-----------|-------------|----------------|----------------|
| **Runs** | Errors or does not run | Runs with hand-holding | Runs top-to-bottom, unaided |
| **Correctness** | Misses most messes | Handles some (missing/types/dupes) | Handles the **full brief**: missing values, types, duplicates, bad labels, **mixed date formats**, and **impossible values** (dropped or marked missing, with the choice documented) |
| **Code quality** | One long block | Some structure | Small, named, readable functions; clear names |
| **Reporting** | No counts | A count, not compared | Before/after row counts + a note of what was fixed |

**Auto-check (use this in your notebook):** assert your cleaned table has the
expected shape — for example, that every `steps` value is a non-negative `int`,
every `date` is `YYYY-MM-DD`, every `mood` is lowercase and stripped, there are no
duplicate rows, and you report the before/after counts.

## Did you measure it?

Report **a number** — rows removed, or before→after counts. A capstone with no
measured result cannot score above *Developing*.

## What you need & what it costs

Runs in the browser via Pyodide — zero install, **₹0**. The dataset is vendored
(`modules/01-python/data/habits.csv`, CC0; see `docs/ASSETS.md`) and loads offline.

## Walkthrough — one way to do it

Here is a complete, honest example that reuses the helpers you built across the
module: `clean_steps` (Ch7), `clean_mood` (Ch3), and a duplicate check (Ch4) —
extended to cover the whole brief: dates are normalized, and impossible values
are treated as missing (then dropped or kept-as-missing, each choice documented).

```python
import csv

def clean_date(text):
    """Normalize a date to YYYY-MM-DD; the file's strays are DD/MM/YYYY."""
    text = text.strip()
    if "/" in text:
        day, month, year = text.split("/")
        return f"{year}-{month}-{day}"
    return text

def clean_steps(text):
    """Steps as an int, or None if blank, unparsable, or impossible (negative)."""
    text = text.strip()
    if text == "":
        return None
    try:
        steps = int(text.replace(",", ""))
    except ValueError:
        return None
    if steps < 0:            # you can't walk -5 steps — treat as missing
        return None
    return steps

def clean_sleep(text):
    """Sleep hours as a float, or None if blank, unparsable, or impossible (>24)."""
    text = text.strip()
    if text.endswith("h"):   # strip the stray unit: "8h" -> "8"
        text = text[:-1]
    if text == "":
        return None
    try:
        hours = float(text)
    except ValueError:
        return None
    if hours > 24:           # a day has 24 hours — 26 is a recording error
        return None
    return hours

def clean_mood(text):
    """Tidy a mood label: strip spaces, lowercase."""
    return text.strip().lower()

with open("data/habits.csv") as f:
    rows = list(csv.DictReader(f))

seen = set()
clean = []
for row in rows:
    key = tuple(row.values())
    if key in seen:          # drop exact duplicate rows
        continue
    seen.add(key)
    steps = clean_steps(row["steps"])
    if steps is None:        # drop rows with no usable steps (blank or impossible)
        continue
    clean.append({
        "date": clean_date(row["date"]),      # every date now YYYY-MM-DD
        "steps": steps,                       # now a non-negative int
        "sleep_hours": clean_sleep(row["sleep_hours"]),  # float, or None if missing/impossible
        "mood": clean_mood(row["mood"]),
    })

print("Before:", len(rows), "rows")
print("After: ", len(clean), "rows")
print("Removed:", len(rows) - len(clean), "(2 duplicates + 3 blank-steps rows + 1 impossible-steps row)")
```

Running this on the vendored `habits.csv` prints:

```text
Before: 35 rows
After:  29 rows
Removed: 6 (2 duplicates + 3 blank-steps rows + 1 impossible-steps row)
```

**The write-up:** "I started with **35** rows. I dropped **2** exact duplicate days
(`2026-01-14`, `2026-01-31`), **3** rows whose `steps` were blank (`2026-01-03`,
`2026-01-18`, `2026-01-26`), and **1** row with an impossible `-5` steps
(`2026-01-11`), leaving **29** clean rows. Along the way I fixed the comma values
(`7,500` → `7500`), stripped the stray sleep unit (`8h` → `8.0`), tidied mood
labels (an untrimmed `Good` → `good`), and normalized the two `DD/MM/YYYY` dates
(`07/01/2026` → `2026-01-07`, `20/01/2026` → `2026-01-20`) instead of dropping
them — those rows are still good data once cleaned. Two kept rows have
`sleep_hours = None`: one was blank (`2026-01-09`) and one was an impossible `26`
(`2026-01-12`) — I marked both as missing rather than dropping a day whose steps
were fine."

That is a Proficient answer: it runs, uses small named functions, handles the full
brief — missing values, types, duplicates, labels, mixed dates, and impossible
values — and reports a measured before/after (35 → 29, 6 removed). Other valid
choices — keeping blank-steps rows with a `0`, or dropping the two impossible-sleep
rows instead of marking them missing — are fine too, as long as each choice is
documented and you measure the result.
