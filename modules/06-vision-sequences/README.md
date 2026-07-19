# M6 — Specialized DL: Vision & Sequences

Convolution and CNNs from first principles to transfer learning; RNN/LSTM
sequence models to their limits; embeddings as the conceptual bridge to M7.

> **Status: in progress** (P2 build, `docs/phases/P2_SPEC.md §6.D`). Chapter
> files land one at a time; the landing page table gains links as they do.

## Prerequisites

- M5 — Deep Learning Foundations (the training harness from Ch18 is reused for
  every training chapter here; the Colab workflow from Ch11 is assumed).

## Learning objectives

By the end of M6 you can:

- Explain convolution/pooling and build + train CNNs.
- **Fine-tune a pretrained vision model** (transfer learning — the working
  practitioner's default).
- Build RNN/LSTM models and explain *why* they struggle with long sequences.
- Use **embeddings** for similarity/search — the conceptual bridge to M7.

## Running thread & data

*Teach the machine to see, then to read* — two acts, one arc.

- Vision: **Fashion-MNIST** (MIT) via torchvision; transfer learning on an
  **Oxford-IIIT Pets** subset (CC BY-SA 4.0); pretrained **ResNet** weights
  (BSD-3-Clause — the ledger's first model asset).
- Sequences: **SSA baby names** (US-gov public domain, makemore lineage) for
  the char-level generator; `data/glove-50d-sample.csv` (vendored 135-word
  GloVe subset, PDDL; script: `infra/datasets/make_glove_sample.py`) for
  in-browser semantic search. All ledgered in `docs/ASSETS.md` (R11).

## Assessment

- Per-chapter **quick check** (`quiz-chNN.yml`, 3–4 MCQ).
- Cumulative **module quiz** (`module-quiz.yml`) — transfer questions only.
- **Capstone:** image-classifier app + char-level sequence model — see
  [`capstone.md`](capstone.md). Property-graded floors + rubric (P2-D7/R4).

## How to run

- **Browser chapters (₹0):** Ch1–3, 8, 10, 13, 14 — NumPy on real arrays, no
  install.
- **Colab chapters (₹0):** Ch4–7, 9, 11, 12 — click **Open in Colab**; each
  states its expected free-tier runtime.
- **Reproduced in CI:** twins for browser chapters; CPU-scaled generated
  companions for colab chapters (P2-D9).
