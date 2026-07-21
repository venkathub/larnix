# Larnix

[![Checks](https://github.com/venkathub/larnix/actions/workflows/checks.yml/badge.svg)](https://github.com/venkathub/larnix/actions/workflows/checks.yml)
[![Publish](https://github.com/venkathub/larnix/actions/workflows/publish.yml/badge.svg)](https://github.com/venkathub/larnix/actions/workflows/publish.yml)

A free, open-access, beginner-to-frontier school for AI/ML — modeled on Zerodha Varsity's pedagogy (plain language, analogies, short single-idea chapters, "Key Takeaways", difficulty tiers, quizzes) — where **every chapter runs in your browser at ₹0**: no installs, no GPU, no paywall.

**▶ Start learning now: [venkathub.github.io/larnix](https://venkathub.github.io/larnix)**

## What's live today

**4 modules · 50 chapters**, each with in-browser runnable Python, auto-graded exercises, a per-chapter quiz, a module quiz, and a graded capstone:

| Module | Chapters | You'll learn |
|---|---|---|
| M0 — Orientation | 6 | What AI/ML actually is, how to learn it, the map ahead |
| M1 — Python for AI | 14 | Python from zero to data-ready, entirely in the browser |
| M2 — Math You Actually Need | 16 | Vectors, matrices, calculus, probability — intuition first |
| M3 — Data & Tooling | 14 | NumPy, pandas, plotting, datasets, reproducibility |

**In progress:** M4 — Classical ML (regression, gradient descent, generalization).
**Planned (P2–P7):** M5–M16 — deep learning → transformers → LLM fine-tuning → build-your-own-LLM → career readiness. Full map: [curriculum](https://venkathub.github.io/larnix/curriculum.html) · [`docs/ROADMAP.md`](docs/ROADMAP.md).

## How it works

- **Quarto + [quarto-live](https://github.com/r-wasm/quarto-live) (Pyodide)** — Python executes in your browser tab; a low-spec laptop is enough
- **Auto-grading in the page** — exercises check themselves (`run_tests()`), quizzes track your best score locally
- **Every chapter has a notebook twin that CI executes** — if a chapter's code breaks, the build fails
- **Deterministic quality gates** — structure lint, quiz schema, accessibility (alt-text/contrast), link check, dataset license ledger, spell/style — all in [`checks.yml`](.github/workflows/checks.yml)

## Try it (5 minutes)

Open the [live site](https://venkathub.github.io/larnix), pick M0 Chapter 1, and press Run. To build locally or contribute, see [`docs/WALKTHROUGH.md`](docs/WALKTHROUGH.md) and [`docs/RUNBOOK.md`](docs/RUNBOOK.md); design rationale lives in [`docs/DECISIONS.md`](docs/DECISIONS.md).

## Status & contributing

Built in public, phase by phase ([`docs/ROADMAP.md`](docs/ROADMAP.md)). Issues and feedback welcome; the community-PR pipeline is being set up ([`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md)). Dataset licenses are tracked in [`docs/ASSETS.md`](docs/ASSETS.md).
