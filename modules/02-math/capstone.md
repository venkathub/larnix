# M2 Capstone — The math of one neuron

> Skeleton authored in P1 §6.A.6: the brief + rubric are final; the graded
> auto-check and the hidden walkthrough are finalized with the M2 build (P1 §6.D).
> Runs in the browser, ₹0.

## The brief

Implement a single neuron's **forward pass** and its **gradient by hand** in NumPy
(no autograd), then **verify your analytic gradient against a numeric
finite-difference** estimate. This is the whole module assembled into one moving
part — the seed of backpropagation.

## Deliverables

- A runnable in-browser notebook that defines the neuron (weights, bias,
  activation), computes the forward output and a loss, and derives the gradient of
  the loss with respect to each parameter.
- A check that compares your analytic gradient to a numeric one, and prints the
  **maximum gradient error**.

## Rubric

Score each criterion 0–2; a "Proficient" capstone scores at the top of every row.

| Criterion | Not yet (0) | Developing (1) | Proficient (2) |
|-----------|-------------|----------------|----------------|
| **Runs** | Errors or does not run | Runs with hand-holding | Runs top-to-bottom, unaided |
| **Correctness** | Gradient wrong | Forward right, gradient off | Analytic gradient matches numeric within tolerance |
| **Understanding** | No explanation | Names the steps | Explains each term (forward, loss, chain-rule gradient) |
| **Measurement** | No error reported | Reports a value loosely | Reports the max analytic-vs-numeric gradient error |

**Auto-check (finalized with M2):** an assert that the analytic gradient matches
the finite-difference gradient within a float tolerance.

## Did you measure it?

Report the **maximum gradient error** between your analytic and numeric gradients.
A capstone with no measured result cannot score above *Developing*.

## What you need & what it costs

Runs in the browser via Pyodide (NumPy + Matplotlib are built in) — zero install,
**₹0**.
