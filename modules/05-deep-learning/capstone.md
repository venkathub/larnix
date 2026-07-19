---
title: "M5 Capstone — Digits from scratch → PyTorch"
---

> **Template — finalized with the M5 build** (P2 §6.C task 48). The brief below
> is the approved shape from `docs/phases/P2_SPEC.md §4.3`; auto-checks, the
> walkthrough, and calibrated thresholds land with the build. Part 1 runs in
> the browser (₹0); Part 2 runs on a free Colab/Kaggle GPU (₹0).

## The brief

Two graded parts — the same problem, built twice:

1. **From scratch (browser).** Train your micrograd/NumPy MLP on sklearn's 8×8
   digits. *Auto-check (seeded-deterministic):* test accuracy ≥ 0.90 and the
   gradient check passes against finite differences.
2. **In PyTorch (Colab).** Re-implement the classifier on MNIST with the Ch18
   reproducible training harness. *Auto-check (property, calibrated on ≥3
   recorded runs):* test accuracy ≥ 0.97, loss curve logged.
   **Transfer twist:** change one stated thing (hidden size or activation),
   re-run, and compare before/after with numbers.

## Rubric (0–2 per criterion)

| Criterion | What "2" looks like |
|-----------|---------------------|
| Runs | Both parts, top-to-bottom without edits. |
| Correct scratch backprop | Gradient check passes; you can point at the line for each step of the chain rule. |
| Idiomatic PyTorch port | `nn.Module` + the five-line loop; device-agnostic; no framework fights. |
| Measurement | Before/after numbers for the transfer twist; loss curves shown and read correctly. |
| Reproducibility | Seeded, config-driven, re-runnable by a stranger. |
