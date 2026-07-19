---
title: "M4 Capstone — An end-to-end tabular predictor + model card"
---

> **Template — finalized with the M4 build** (P2 §6.B task 28). The brief below
> is the approved shape from `docs/phases/P2_SPEC.md §4.3`; auto-checks, the
> walkthrough, and the vendored dataset sample land with the build. Runs in the
> browser, ₹0.

## The brief

Run the full classical-ML workflow on the **UCI Bank Marketing** dataset (new
data you haven't seen in the module, and naturally *imbalanced* — "will this
customer subscribe?"):

1. EDA-lite — know your data before you model it.
2. **Split first.** The test set is sealed before anything is fitted.
3. A baseline everyone must beat (majority class / a single feature).
4. At least **three model families** compared with cross-validation.
5. A tuned final model, evaluated **once** on the held-out split.
6. A **model card**: intended use, data provenance, metrics (including
   per-class), and known limitations.

## Auto-checks (graded in the browser)

- **Leakage tripwire:** no test row may ever be seen by `fit` — verified by the
  grader.
- **ROC-AUC floor** on the held-out split.

## Rubric (0–2 per criterion)

| Criterion | What "2" looks like |
|-----------|---------------------|
| Runs | Top-to-bottom without edits. |
| Honest evaluation | Split before fit; CV used correctly; no leakage anywhere. |
| Model comparison | ≥3 families compared fairly; the choice is justified with numbers. |
| Measurement | Every claim carries a number; the right metric for imbalanced data. |
| Model card | Complete, honest about failure modes and who should not use it. |
