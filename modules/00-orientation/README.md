# M0 — Orientation

The on-ramp. You run a real model in your browser first, then learn — in plain
language — what AI is, what it costs (₹0 to start), and how this school works. No
prior machine learning, no install, no account.

## Prerequisites

None. If you can open a web page, you can do this module.

## Learning objectives

By the end of M0 you can:

- Run real code in the browser at ₹0 and *feel* a model work.
- Confirm the complete ₹0 path — and what, if anything, ever costs money.
- Say in plain words what AI / ML / DL / GenAI are and how they relate.
- Navigate the school: tiers, exercises, quizzes, capstones, the certificate.

## Running thread

*"Could a computer learn to do this?"* — opened by the Iris "tell the species
apart" demo in Chapter 1 and revisited as each idea is named. We follow **Asha**, a
non-CS career-switcher, as the stand-in for every beginner here.

## Chapters

Ordered **wow-first** (run a model, then the ₹0 path, then the concepts — P1-D1).
All 🟢 Beginner · `browser` · `stable`.

| # | Chapter | Status |
|---|---------|--------|
| 1 | [Train your first model — in your browser](ch01-train-your-first-model.qmd) | shipped |
| 2 | [What you need & what it costs](ch02-what-you-need-and-what-it-costs.qmd) | shipped |
| 3 | [What is AI, really?](ch03-what-is-ai-really.qmd) | shipped |
| 4 | AI vs ML vs DL vs GenAI — a family tree | authored in P1 |
| 5 | A 10-minute history of AI | authored in P1 |
| 6 | How this school works | authored in P1 |

## Assessment

- Per-chapter **quick check** (`quiz.yml`, 2–3 MCQ).
- Cumulative **module quiz** (`module-quiz.yml`, ~8–12 MCQ) on the module landing.
- **Capstone:** set up the ₹0 toolchain and run your first model, change one thing,
  and report whether accuracy moved — see [`capstone.md`](capstone.md).

## How to run

- **In your browser (₹0):** open a chapter and press **Run** on each code block —
  Python executes client-side via Pyodide, no install.
- **Reproduced in CI:** each chapter ships a generated `*.ipynb` twin that runs the
  same code under CPython (the R10 gate), so every example is guaranteed to work.
