# Larnix — STYLE_GUIDE.md

> The editorial and pedagogical standard for every chapter in Larnix. This file IS the pedagogy gate: Claude Code must read it before authoring content, and no chapter merges unless it conforms. It encodes the Zerodha-Varsity-style approach adapted for code-heavy AI education.

---

## 1. Who we write for

Two readers are always in the room:

- **The beginner** (the default reader): may be non-CS, may be a junior programmer, may be a career switcher. Assume they know *nothing* about the chapter's topic. Never assume prior ML. Define every term the first time it appears.
- **The returning practitioner**: skims for the idea, the code, and the "why." Serve them with clear Key Takeaways and runnable examples they can lift.

When the two conflict, **write for the beginner and let the practitioner skim.** Clarity for the newest reader is the house style.

---

## 2. The Varsity contract (mandatory structure for every chapter)

Every chapter MUST contain these parts, in this order. A chapter missing any part is not done.

1. **Hook** — open with a real-world analogy OR a working demo (taste before theory). Never open with a definition or a wall of math. Earn the reader's attention in the first three sentences.
2. **Plain-language explanation** — one concept per chapter. ~1,500–3,000 words of prose, OR a 15–25 minute notebook. If it needs more, split it into two chapters.
3. **At least one runnable worked example** — real code that actually executes (a notebook cell or snippet). No "illustrative" pseudo-code that can't run.
4. **Key Takeaways box** — 3–6 numbered points recapping what matters. (See format in §7.)
5. **Hands-on exercises** — 2–4 exercises with auto-graders and hidden solution walkthroughs, scaffolded by difficulty (see §6).

Plus required **front-matter** on every chapter (see CHAPTER_TEMPLATE.md): `title`, `module`, `chapter`, `difficulty`, `prereqs`, `learning_objectives`, `compute`, `status`, `last_reviewed`, `est_minutes`.

---

## 3. Tone & voice

- **Conversational and first-person.** Write like a knowledgeable friend explaining over coffee, not a textbook. "Let's build a tokenizer" beats "This section describes tokenization."
- **Plain language over jargon.** When a technical term is unavoidable, introduce it with its plain-English meaning first, *then* name it. Example: "the model's confidence in each next word — what we call the **logit**."
- **Short sentences. Short paragraphs.** Prefer 2–4 sentence paragraphs. Break up density.
- **Concrete over abstract.** Always ground an idea in a specific example, number, or picture before generalizing.
- **Encouraging, never condescending.** Acknowledge that a concept is hard when it is. Never write "simply," "just," "obviously," or "trivially" — they make a stuck reader feel stupid.
- **No hype.** Avoid "revolutionary," "game-changing," "magic." Respect the reader's intelligence; let the ideas impress on their own.

---

## 4. Analogies & running examples

- Every module has **one running example or analogy** that threads through its chapters (the way Zerodha Varsity teaches IPOs through a t-shirt entrepreneur). Decide it during grooming and reuse it.
- Analogies must **clarify, not decorate**. If an analogy breaks down in a way that would mislead, flag the limit explicitly ("the analogy stops here, because…").
- Reuse a small set of recurring example datasets/projects per track so the reader isn't re-learning context every chapter.

---

## 5. Code standards (clarity over cleverness)

- **Every code block runs.** CPU/in-browser notebooks execute in CI; GPU notebooks are Colab-verified with the run recorded in the PR.
- **Readable over clever.** Favour explicit, well-named, commented code a beginner can follow. This is a teaching codebase, not a code-golf entry.
- **Show output.** Include the expected output (printed result, shape, plot) so a reader who can't run it still learns.
- **Build up, don't dump.** Introduce code in small steps with explanation between them, rather than one large block.
- **No secrets, ever.** API examples read keys from environment variables and ALWAYS show a free fallback (Ollama / Groq / Gemini free tier). Never print or hardcode a key. Update `.env.example` when a new variable is introduced.
- **Pin versions** in any notebook that installs packages, so it keeps running as libraries change.

---

## 6. Exercises & scaffolding

Each chapter ships 2–4 exercises that progress in difficulty:

1. **Fill-in-the-blank / guided** — the structure is given; the learner completes one or two lines. (Confidence-builder.)
2. **Implement-this-function** — a clear spec + an auto-grader (assert-based unit tests). (Core practice.)
3. **Open-ended mini-task** — a small problem with multiple valid solutions, graded by rubric or by a looser check. (Stretch.)

Rules:

- Every coded exercise has a **working auto-grader** and a **hidden solution walkthrough** revealed only after an attempt.
- Match exercise difficulty to the chapter's tier. A 🟢 chapter must not hide a 🔴 exercise without labelling it a stretch goal.
- State the expected time to complete.

### Quizzes & module assessment (P1-D11)

Two quiz artifacts share one schema (`infra/ci/quiz_lint.py`), both rendered and
scored client-side by the P0 quiz engine (score saved to `localStorage`, ₹0):

- **Per-chapter quick check** — a `quiz.yml` (2–3 MCQ) beside each chapter, mounted
  in the chapter with `{{< quiz quiz.yml >}}`. Immediate recall after the lesson.
- **Cumulative module quiz** — one `module-quiz.yml` (~8–12 MCQ) per module,
  mounted on the **module landing page** (`modules/<NN>/index.qmd`) with
  `{{< quiz module-quiz.yml >}}`. End-of-module consolidation (the Varsity model).

Each MCQ needs an `answer` (0-based) and a one-line `explanation`. The linter flags
a module quiz outside the ~8–12 band with an advisory note (not a failure).

---

## 7. Required components & formatting

**Difficulty badges** (one per chapter, in front-matter and shown in the UI):

- 🟢 **Beginner** — no prior ML; gentle pace; in-browser where possible.
- 🟡 **Intermediate** — assumes earlier modules; introduces real tooling.
- 🔴 **Advanced** — assumes solid fundamentals; production/frontier depth.

**Compute tier** (front-matter `compute`):

- `browser` — runs in JupyterLite/Pyodide, zero install, ₹0.
- `colab` — needs a free Colab/Kaggle GPU; ships an "Open in Colab" button.
- `gpu` — needs a rented GPU (M11 only); states the approximate cost.

**Status** (front-matter `status`):

- `stable` — foundational; expected to last years. Reviewed annually.
- `frontier` — model/tool/framework-specific; expected to date. Reviewed quarterly; version-pinned.

**Key Takeaways box** (end of every chapter):

```
> ### Key Takeaways
> 1. <the single most important point>
> 2. <…>
> 3. <…>
```

**Callouts** (use sparingly, for genuine signal):

- `> 💡 Tip:` a practical shortcut.
- `> ⚠️ Watch out:` a common mistake or footgun.
- `> 🔬 Going deeper:` optional depth a beginner can skip.
- `> 🧱 For Java developers:` translation notes for the builder's own background (used mainly in M1).

---

## 8. Accessibility & the ₹0 promise

- A learner must be able to complete **Modules 0–10 for ₹0** (browser + Colab/Kaggle + Ollama). Protect this in every chapter: if a chapter would force a paid step, find the free path or move the paid step to an optional "going deeper" box.
- Any paid step (API key, rented GPU) must be **optional, clearly labelled with its cost, and paired with a free alternative.**
- Write for **patchy internet**: beginner notebooks are downloadable and runnable offline where feasible.
- Use alt text on diagrams; don't rely on colour alone to convey meaning.

---

## 9. Correctness & currency

- **Correctness beats coverage.** A wrong explanation is worse than a missing one. If unsure a fact, figure, or API is current, say so and mark the chapter `status: frontier` rather than guessing.
- **Separate stable core from frontier.** Foundations (math, classical ML, backprop, transformers) are written to last; model/tool specifics are isolated, version-pinned, and dated.
- Set `last_reviewed` on every change. The quarterly currency job flags stale frontier chapters and broken pinned dependencies.
- Cite primary sources (papers, official docs) over aggregators when a claim needs support. Never invent a citation.

---

## 10. Inclusivity & safety

- Use inclusive, neutral examples; avoid stereotypes and region-locked assumptions.
- Teach responsible-AI and security habits *in context* (e.g. mention prompt-injection risk when first building an LLM app), not only in Module 14.
- Be honest about limitations and failure modes of every technique — that honesty is part of the senior-engineering signal Larnix is meant to model.

---

## 11. Definition of Done for a single chapter

- [ ] Follows the Varsity contract (hook → explanation → runnable example → Key Takeaways → 2–4 graded exercises).
- [ ] Complete, accurate front-matter incl. `difficulty`, `compute`, `status`, `last_reviewed`.
- [ ] All code runs (CI for browser/CPU; recorded Colab run for GPU).
- [ ] Exercises have working auto-graders + hidden solutions; difficulty matches the tier.
- [ ] Free-tier path verified for the chapter's compute level.
- [ ] Tone/lint/link/spell checks pass; no banned words ("simply," "just," "obviously," "trivially," hype terms).
- [ ] Reads cleanly for a true beginner (the house test: would someone who's never seen this topic follow it?).
