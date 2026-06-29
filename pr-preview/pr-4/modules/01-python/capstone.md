# M1 Capstone — Data-cleaning notebook

> The Module 1 project. It runs entirely in your browser, at **₹0**. Graded by the
> rubric below; it must report **a number**.

## The brief

Take the messy `habits.csv` (`date, steps, sleep_hours, mood`) and produce a
**clean, correctly typed, de-duplicated** table using your own functions. Handle
the messes you met across the module: missing values, stray units/formats
(`8h`, `7,500`), inconsistent mood labels (`Good`/`good`/`ok`), duplicate rows,
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

**Auto-check (use this in your notebook):** assert your cleaned table has the
expected shape — for example, that every `steps` value is an `int`, every `mood`
is lowercase and stripped, there are no duplicate rows, and you report the
before/after counts.

## Did you measure it?

Report **a number** — rows removed, or before→after counts. A capstone with no
measured result cannot score above *Developing*.

## What you need & what it costs

Runs in the browser via Pyodide — zero install, **₹0**. The dataset is vendored
(`modules/01-python/data/habits.csv`, CC0; see `docs/ASSETS.md`) and loads offline.

## Walkthrough — one way to do it

Here is a complete, honest example that reuses the helpers you built across the
module: `clean_steps` (Ch7), `clean_mood` (Ch3), and a duplicate check (Ch4).

```python
import csv

def clean_steps(text):
    """Steps as an int, or None if blank/unparsable; strips a comma."""
    text = text.strip()
    if text == "":
        return None
    try:
        return int(text.replace(",", ""))
    except ValueError:
        return None

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
    if steps is None:        # drop rows with no usable steps
        continue
    clean.append({
        "date": row["date"],
        "steps": steps,                 # now an int
        "mood": clean_mood(row["mood"]),
    })

print("Before:", len(rows), "rows")
print("After: ", len(clean), "rows")
print("Removed:", len(rows) - len(clean), "(2 duplicates + 3 blank-steps rows)")
```

Running this on the vendored `habits.csv` prints:

```text
Before: 35 rows
After:  30 rows
Removed: 5 (2 duplicates + 3 blank-steps rows)
```

**The write-up:** "I started with **35** rows. I dropped **2** exact duplicate days
and **3** rows whose `steps` were blank, leaving **30** clean rows. Along the way I
fixed the comma values (`7,500` → `7500`) and tidied mood labels (an untrimmed `Good` →
`good`) instead of dropping them — those rows are still good data once cleaned."

That is a Proficient answer: it runs, uses small named functions, handles missing
values / types / duplicates / labels, and reports a measured before/after (35 → 30,
5 removed). Other valid choices — keeping blank-steps rows with a `0`, or also
cleaning `sleep_hours` (`8h` → `8`) — are fine too, as long as you measure the result.
