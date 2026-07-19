---
title: "M2 Capstone — The math of one neuron"
---

> Finalized with the M2 build (P1 §6.D). The full walkthrough and a working
> gradient check live in [Chapter 16 — The math of one neuron](ch16-the-math-of-one-neuron.qmd);
> this capstone asks you to rebuild it **with a required variation**, so the work
> shows transfer rather than a copy. Runs in the browser, ₹0.

## The brief

Implement a single neuron's **forward pass** and its **gradient by hand** in NumPy
(no autograd), then **verify your analytic gradient against a numeric
finite-difference** estimate. This is the whole module assembled into one moving
part — the seed of backpropagation.

**Required variation — pick ONE.** Chapter 16 uses a sigmoid activation with the
loss `(a − y)²`. Your capstone must change one of those two pieces and re-derive
the affected chain-rule link yourself:

- **Variation A — tanh activation.** Replace the sigmoid with `a = tanh(z)` and
  derive `da/dz` for it yourself (state the formula in your notebook).
- **Variation B — half squared-error loss.** Keep the sigmoid but use
  `L = ½·(a − y)²` and derive `dL/da` for it yourself (state the formula in your
  notebook).

A submission that reproduces Chapter 16's sigmoid + `(a − y)²` neuron unchanged
cannot score *Proficient* on Correctness or Understanding, even if the gradient
check passes — the check would be verifying the chapter's derivation, not yours.

## Deliverables

- A runnable in-browser notebook that defines the **varied** neuron (weights, bias,
  activation), computes the forward output and a loss, and derives the gradient of
  the loss with respect to each parameter.
- The **re-derived chain-rule link** for your chosen variation, written out in a
  markdown cell (Variation A: the formula for `da/dz` of tanh; Variation B: the
  formula for `dL/da` of the half squared-error loss).
- A check that compares your analytic gradient to a numeric one **for the varied
  neuron**, and prints the **maximum gradient error**.

## Rubric

Score each criterion 0–2; a "Proficient" capstone scores at the top of every row.

| Criterion | Not yet (0) | Developing (1) | Proficient (2) |
|-----------|-------------|----------------|----------------|
| **Runs** | Errors or does not run | Runs with hand-holding | Runs top-to-bottom, unaided |
| **Correctness** | Gradient wrong | Forward right, gradient off — or no variation (chapter's neuron copied) | Analytic gradient of the **varied** neuron matches numeric within tolerance |
| **Understanding** | No explanation | Names the steps | Explains each term (forward, loss, chain-rule gradient) **and states the re-derived link for the chosen variation** |
| **Measurement** | No error reported | Reports a value loosely | Reports the max analytic-vs-numeric gradient error |

<details><summary>Grader answer key — the re-derived links (hidden from learners)</summary>

- **Variation A (tanh):** `da/dz = 1 − tanh²(z) = 1 − a²`. The full gradient is
  `dL/dw_i = 2(a − y) · (1 − a²) · x_i` and `dL/db = 2(a − y) · (1 − a²)`.
  On the chapter's worked input `x=[2,3], w=[0.5,-1.0], b=0.5, y=1.0`:
  `a = tanh(−1.5) ≈ −0.905148`, `loss ≈ 3.629590`, and the analytic-vs-numeric
  max gradient error is about **7.65e-10** (still well under `1e-6`).
- **Variation B (½ loss):** `dL/da = a − y` (the ½ cancels the 2 from the power
  rule). The full gradient is `dL/dw_i = (a − y) · a(1 − a) · x_i` — exactly half
  of the chapter's gradient at every parameter. On the chapter's worked input the
  max gradient error is about **1.63e-11**.

Reject a "Variation B" submission whose gradients equal the chapter's values
unchanged — halving the loss must halve every gradient component.
</details>

**Auto-check (finalized with M2):** an assert that the analytic gradient matches
the finite-difference gradient within a float tolerance. The same check works
unchanged for either variation, because finite differences only need your `loss_at`
function — for the chapter's worked input, Variation A agrees to a **maximum error
of about 7.65e-10** and Variation B to about **1.63e-11** (both well under any
sensible `1e-6` tolerance). Reproduce a number of that order on your own input.

## Did you measure it?

Report the **maximum gradient error** between your analytic and numeric gradients
for the varied neuron. A capstone with no measured result cannot score above
*Developing*. As a reference, Chapter 16's original sigmoid + `(a − y)²` example
reports `max error = 3.27e-11`; any correct implementation of either variation
lands near `1e-9` or smaller.

## What you need & what it costs

Runs in the browser via Pyodide (NumPy + Matplotlib are built in) — zero install,
**₹0**.
