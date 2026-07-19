---
title: "M6 Capstone — Image-classifier app + char-level sequence model"
---

> **Template — finalized with the M6 build** (P2 §6.D task 64). The brief below
> is the approved shape from `docs/phases/P2_SPEC.md §4.3`; auto-checks, the
> walkthrough, and calibrated thresholds land with the build. Both parts run on
> a free Colab/Kaggle GPU (₹0).

## The brief

Two parts — one arc: see, then read.

1. **See.** Transfer-learn a pretrained CNN on a small real-image dataset
   (goal: **≥ 0.90 validation accuracy**). Explain which layers you froze,
   which you trained, and why. Optional 🔬 aside: a Gradio cell inside Colab to
   try your classifier on your own photos.
2. **Read.** Train the char-level **name generator** (SSA names). Sample from
   it before and after training. Then make it fail: document **one clear
   long-range failure** — the limitation attention will fix in M7.

## Auto-checks (property-graded, calibrated on ≥3 recorded runs)

- Validation-accuracy floor on the transfer-learning part.
- Generator training loss fell by the stated fraction, and post-training
  samples differ from the untrained ones.

## Rubric (0–2 per criterion)

| Criterion | What "2" looks like |
|-----------|---------------------|
| Runs | Both parts, top-to-bottom on a free GPU session. |
| Transfer-learning correctness | Frozen vs trained layers identified and justified. |
| Sequence-model understanding | The failure analysis names *what* the model can't hold onto, with evidence. |
| Measurement | Numbers for every claim; curves shown and read correctly. |
| Honesty about limits | The write-up states what this model should not be used for. |
