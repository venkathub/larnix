# M4 — Classical Machine Learning

Train, tune, and honestly evaluate models with scikit-learn — the full tabular
workflow, in the browser at ₹0 (including real XGBoost via the Pyodide
built-in, P2-D6).

> **Status: in progress** (P2 build, `docs/phases/P2_SPEC.md §6.B`). Chapter
> files land one at a time; the landing page table gains links as they do.
> Built so far: [Ch1 — What is learning?](ch01-what-is-learning.qmd) ·
> [Ch2 — Linear regression](ch02-linear-regression.qmd) ·
> [Ch3 — Cost functions & gradient descent](ch03-cost-gradient-descent.qmd) ·
> [Ch4 — Generalization: splits & CV](ch04-generalization-splits-cv.qmd) ·
> [Ch5 — Logistic regression](ch05-logistic-regression.qmd) ·
> [Ch6 — Classification metrics](ch06-classification-metrics.qmd) ·
> [Ch7 — Overfitting & regularization](ch07-overfitting-regularization.qmd) ·
> [Ch8 — Bias–variance](ch08-bias-variance.qmd)

## Prerequisites

- M3 — Data & Tooling (Pandas/EDA are used without re-teaching).
- M2 — Math You Actually Need (gradients — Ch7; Bayes — Ch12).

## Learning objectives

By the end of M4 you can:

- Frame a problem as supervised/unsupervised learning.
- Train, tune, and **honestly evaluate** models with scikit-learn — split/CV,
  the right metric, leakage awareness.
- Explain *why* models fail: overfitting, bias–variance, imbalance.
- Run the full tabular workflow end-to-end and write a **model card**.

## Running thread & data

*The apprentice appraiser* — generalization as the module spine.

- Regression: `data/california-housing-sample.csv` (800-row seeded sample,
  public domain; script: `infra/datasets/make_california_sample.py`).
- Classification: Palmer Penguins, reused from M3 (CC0).
- Capstone: UCI Bank Marketing (CC BY 4.0; sample vendored with the capstone
  task). All ledgered in `docs/ASSETS.md` (R11).

## Assessment

- Per-chapter **quick check** (`quiz-chNN.yml`, 3–4 MCQ).
- Cumulative **module quiz** (`module-quiz.yml`) — transfer questions only.
- **Capstone:** end-to-end tabular predictor + model card — see
  [`capstone.md`](capstone.md). Auto-checks: leakage tripwire + ROC-AUC floor;
  the rest is rubric-graded.

## How to run

- **In your browser (₹0):** every chapter, Ch1–Ch20 — no install, no account.
  Ch12's XGBoost cell downloads the wheel from the Pyodide CDN on first use
  (needs internet for that cell; noted in the chapter).
- **Reproduced in CI:** each chapter ships a generated `*.ipynb` twin executed
  under CPython (R10), with seeded-deterministic graders (P2-D7).
