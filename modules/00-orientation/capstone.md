# M0 Capstone — Set up & run

> The Module 0 project. It runs entirely in your browser, at **₹0**. Graded by the
> rubric below; it must report **a number**.

## The brief

Using the in-browser workflow from [Chapter 1](ch01-train-your-first-model.qmd),
train the iris classifier, then **change one thing** — a different model or a
different setting — and report whether your test-set accuracy went **up, down, or
stayed the same**.

## Deliverables

- A runnable in-browser session (start from the Chapter 1 cells) that loads the
  data, splits it, trains, predicts, and prints a test-set accuracy.
- A 2–3 sentence note: **what you changed**, the **before** and **after** accuracy,
  and a guess at **why** it moved (or didn't).

## Rubric

Score each criterion 0–2; a "Proficient" capstone scores at the top of every row.

| Criterion | Not yet (0) | Developing (1) | Proficient (2) |
|-----------|-------------|----------------|----------------|
| **Runs** | Errors or does not run | Runs with hand-holding | Runs top-to-bottom, unaided |
| **Correctness** | Tests on training data, or no split | Splits data but reports loosely | Trains on the training set only; accuracy measured on the held-out test set |
| **Measurement** | No number reported | A number, but not compared | Before **and** after accuracy reported and compared |
| **Explanation** | No reasoning | States what changed, not why | States what changed and a plausible reason it moved the result |

## Did you measure it?

Every Larnix capstone reports **a number** and says what it means. A capstone with
no before/after accuracy cannot score above *Developing*, however tidy the prose.

## What you need & what it costs

Runs in the browser via Pyodide — zero install, **₹0**. The iris data ships with
scikit-learn (`load_iris`); nothing is downloaded or paid for.

## Walkthrough — one way to do it

Here is a complete, honest example. Starting from Chapter 1, the only change is the
**split size**: `test_size=0.25` becomes `test_size=0.5`.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)

# Before: the Chapter 1 setup (a quarter held out for testing)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)
before = accuracy_score(yte, LogisticRegression(max_iter=200).fit(Xtr, ytr).predict(Xte))
print(f"Before (test_size=0.25): {before:.2%}")

# After: the one change — hold out half the data for testing instead
Xtr2, Xte2, ytr2, yte2 = train_test_split(X, y, test_size=0.5, random_state=0)
after = accuracy_score(yte2, LogisticRegression(max_iter=200).fit(Xtr2, ytr2).predict(Xte2))
print(f"After  (test_size=0.50): {after:.2%}")
```

Running this prints:

```text
Before (test_size=0.25): 97.37%
After  (test_size=0.50): 93.33%
```

**The write-up:** "I changed `test_size` from 0.25 to 0.50. Accuracy dropped from
**97.37%** to **93.33%**. With half the flowers held out, the model had fewer
examples to learn from *and* was graded on a larger, harder test set — so a small
drop is exactly what I'd expect."

That is a Proficient answer: it runs, trains on the training set only, reports a
measured before/after, and explains the movement. (A different valid change — for
example swapping in `KNeighborsClassifier(n_neighbors=5)` on the original split —
leaves accuracy at 97.37%; "it stayed the same, and here's why" is an equally good
capstone, as long as you measured it.)
