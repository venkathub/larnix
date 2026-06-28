# M0 Capstone — *(TEMPLATE — not graded P0 content)*

> **This is a template artifact.** P0 ships one sample chapter to prove the
> platform; it has no real capstone. This file shows the **rubric format** every
> P1+ module inherits. A module author copies this file to
> `modules/<NN>-<slug>/capstone.md`, replaces the brief, and tunes the rubric.

## The brief

> One short paragraph: a *build-something* task the learner does end-to-end using
> the module's skills. State the dataset/tools and the single thing they must
> produce. Keep it doable in the module's compute tier (₹0 path first).

**Example (M0):** Using the in-browser workflow from Chapter 1, train a
classifier on the Iris data, then **change one thing** (a different model or
setting) and report whether your accuracy went up or down on the test set.

## Deliverables

- A runnable notebook (or in-browser session) that loads data, trains, predicts,
  and prints an accuracy number.
- A 2–3 sentence note: what you changed, and the before/after accuracy.

## Rubric

Score each criterion 0–2; a "Proficient" capstone scores at the top of every row.

| Criterion | Not yet (0) | Developing (1) | Proficient (2) |
|-----------|-------------|----------------|----------------|
| **Runs** | Code errors or does not run | Runs with hand-holding | Runs top-to-bottom, unaided |
| **Correctness** | Tests on training data, or no split | Splits data but reports loosely | Trains on train only; accuracy measured on held-out test set |
| **Measurement** | No number reported | A number, but not compared | Before/after numbers reported and compared |
| **Explanation** | No reasoning | States what, not why | States what changed and why it likely moved the result |

## Did you measure it?

Every Larnix capstone must report **a number** and say what it means — this is the
course's "evals before features" habit applied to the learner. A capstone with no
measured result cannot score above *Developing*, however polished the prose.

## What you need & what it costs

State the compute tier and the ₹0 path explicitly (e.g. "runs in the browser,
zero install, ₹0" for M0–M4; "free Colab T4" for M5–M10; rented-GPU cost for M11
with its smaller-model free path).
