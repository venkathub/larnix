# M2 — Math You Actually Need

Build *intuition* — picture before symbol — for the linear algebra, calculus, and
probability that AI actually uses. Enough to understand one neuron and, later,
backpropagation. No proofs, no fear.

## Prerequisites

- M1 — Python for AI (you can write a function and use NumPy arrays a little).
- School-level arithmetic. Everything else is built up from pictures.

## Learning objectives

By the end of M2 you can:

- Read vectors and matrices as geometry (points, arrows, transformations).
- Explain derivatives and gradients as *sensitivity* and *downhill direction*.
- Apply the chain rule to a tiny network by hand.
- Use the core ideas of probability, distributions, and summary statistics.
- Assemble a single neuron's forward and backward pass in NumPy.

## Running example

*"Assemble one neuron, piece by piece."* Each chapter adds a Lego brick that the
final chapter snaps together. Recurring concrete examples: **movie taste as
vectors** (similarity) and **"predict the tip from the bill"** (derivatives and
gradients). All visuals via Matplotlib in the browser.

## Chapters

🟢→🟡 · `browser` · `stable`. (Authored across P1; Ch10+Ch11 may merge — P1-D5.)

| # | Chapter | Tier |
|---|---------|------|
| 1 | [Why math for AI (and how little you need to start)](ch01-why-math-for-ai.qmd) | 🟢 |
| 2 | [Vectors & geometry](ch02-vectors-geometry.qmd) | 🟢 |
| 3 | [Matrices as transformations](ch03-matrices-as-transformations.qmd) | 🟢 |
| 4 | [Matrix multiplication, intuitively](ch04-matrix-multiplication.qmd) | 🟡 |
| 5 | [Dot products & similarity](ch05-dot-products-similarity.qmd) | 🟢 |
| 6 | [Derivatives = sensitivity](ch06-derivatives-sensitivity.qmd) | 🟡 |
| 7 | [Gradients](ch07-gradients.qmd) | 🟡 |
| 8 | [The chain rule](ch08-chain-rule.qmd) | 🟡 |
| 9 | [Probability basics](ch09-probability-basics.qmd) | 🟢 |
| 10 | [Distributions](ch10-distributions.qmd) | 🟡 |
| 11 | [Mean, variance & standard deviation](ch11-mean-variance-std.qmd) | 🟢 |
| 12 | [Bayes, intuitively](ch12-bayes-intuitively.qmd) | 🟡 |
| 13 | [Correlation vs causation](ch13-correlation-vs-causation.qmd) | 🟢 |
| 14 | [Sampling & uncertainty](ch14-sampling-uncertainty.qmd) | 🟡 |
| 15 | [Linear algebra in NumPy](ch15-linear-algebra-in-numpy.qmd) | 🟡 |
| 16 | [The math of one neuron](ch16-the-math-of-one-neuron.qmd) | 🟡 |

## Assessment

- Per-chapter **quick check** (`quiz.yml`, 2–3 MCQ).
- Cumulative **module quiz** (`module-quiz.yml`, ~8–12 MCQ) on the module landing.
- **Capstone:** the math of one neuron — forward + backward by hand, verified
  against a numeric gradient — see [`capstone.md`](capstone.md).

## How to run

- **In your browser (₹0):** open a chapter and press **Run**; plots render via
  Matplotlib in Pyodide, no install.
- **Reproduced in CI:** each chapter ships a generated `*.ipynb` twin executed
  under CPython (R10).
