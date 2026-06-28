# M3 Capstone — End-to-end EDA

> Skeleton authored in P1 §6.A.6: the brief + rubric are final; the hidden
> walkthrough is finalized with the M3 build (P1 §6.E). Open-ended and
> **rubric-graded**. Runs in the browser, ₹0.

## The brief

Run a full exploratory data analysis on a **new public dataset** (a different one
from the Palmer Penguins you used through the module — to test transfer): load it,
clean it, answer **at least three questions** with plots **and** numbers, and write
up your findings.

## Deliverables

- A runnable in-browser notebook: load → clean (documented) → explore → at least
  three questions each answered with a plot and a number → a short written findings
  section.
- An **ethics note**: where the data came from, its license, and one bias or
  provenance caveat.

## Rubric

Score each criterion 0–2; a "Proficient" capstone scores at the top of every row.

| Criterion | Not yet (0) | Developing (1) | Proficient (2) |
|-----------|-------------|----------------|----------------|
| **Runs** | Errors or does not run | Runs with hand-holding | Runs top-to-bottom, unaided |
| **Cleaning** | Undocumented / wrong | Some cleaning shown | Cleaning documented and correct |
| **Insight** | No real questions | Questions, weak evidence | ≥3 questions answered with plots + numbers |
| **Measurement** | Claims without numbers | Some numbers | Every claim backed by a number or plot |
| **Ethics note** | Absent | Names the source | Source, license, and a bias/provenance caveat |

This capstone is **rubric-graded** (open-ended — many valid datasets and questions).

## Did you measure it?

Every claim must be backed by **a number or a plot**. Findings with no measured
evidence cannot score above *Developing* on **Insight** or **Measurement**.

## What you need & what it costs

Runs in the browser via Pyodide — zero install, **₹0**. Use a small, license-clean
public dataset; vendor it at `data/<name>.csv`, load it via `lib/data.py`, and add
it to `docs/ASSETS.md` with its license (R11).
