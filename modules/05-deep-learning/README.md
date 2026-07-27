# M5 — Deep Learning Foundations

Build a neural net from scratch (neuron → micrograd → MLP), then translate that
understanding into idiomatic PyTorch on a free Colab/Kaggle GPU.

> **Status: in progress** (P2 build, `docs/phases/P2_SPEC.md §6.C`). Chapter
> files land one at a time; the landing page table gains links as they do.
> Built so far: [Ch1 — From logistic regression to a neuron](ch01-logreg-to-neuron.qmd) ·
> [Ch2 — Activation functions](ch02-activation-functions.qmd) ·
> [Ch3 — Layers & networks](ch03-layers-networks.qmd) ·
> [Ch4 — The forward pass](ch04-forward-pass.qmd) ·
> [Ch5 — Loss functions](ch05-loss-functions.qmd) ·
> [Ch6 — Backpropagation, spelled out](ch06-backpropagation.qmd) ·
> [Ch7 — Gradient-descent variants](ch07-gradient-descent-variants.qmd) ·
> [Ch8 — Build micrograd I: the autograd engine](ch08-micrograd-engine.qmd)

## Prerequisites

- M4 — Classical Machine Learning (logistic regression is the on-ramp: Ch1
  shows the model you know *is* a one-neuron network).
- M2 Ch8 (chain rule) and M2 Ch16 (the math of one neuron).

## Learning objectives

By the end of M5 you can:

- Build a neural net **from scratch** — neuron → autograd engine (micrograd) →
  MLP — and explain every line of backprop.
- Translate that understanding into idiomatic PyTorch
  (`tensor`/`autograd`/`nn.Module` + a hand-rolled training loop).
- Run the free-GPU workflow (Colab, with Kaggle as the documented alternate)
  confidently.
- Train reproducibly: seeds, checkpoints, diagnosing loss curves.

## Running thread & compute split

*Teach the machine to read your handwriting* — one digit classifier, built
twice. **Ch1–10 `browser`** (₹0; micrograd is dependency-free Python on
sklearn's built-in 8×8 `load_digits`); **Ch11 is the handoff chapter**
(why GPUs + the free Colab/Kaggle workflow, P2-D4); **Ch11–18 `colab`** (MNIST
via torchvision, CC BY-SA 3.0 — nothing vendored; ledgered in
`docs/ASSETS.md`).

## Assessment

- Per-chapter **quick check** (`quiz-chNN.yml`, 3–4 MCQ).
- Cumulative **module quiz** (`module-quiz.yml`) — transfer questions only.
- **Capstone:** scratch digits → PyTorch MNIST, two graded parts — see
  [`capstone.md`](capstone.md). Browser part grades seeded-deterministic;
  Colab part grades by calibrated property asserts (P2-D7).

## How to run

- **Ch1–10 in your browser (₹0):** open a chapter and press **Run** — no
  install, no account.
- **Ch11–18 on a free GPU (₹0):** click the chapter's **Open in Colab** button;
  the companion notebook grades your exercises inside Colab. Every colab
  chapter states its expected free-tier runtime.
- **Reproduced in CI:** browser chapters ship CPython twins; colab chapters
  ship generated companions executed CPU-scaled under `LARNIX_CI` (P2-D9).
