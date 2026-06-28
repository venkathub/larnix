# CLAUDE.md — Larnix Engineering & Curriculum Operating Agreement

## Mission
Build Larnix: a free, open-access, beginner-to-frontier school for AI/ML, modeled on
Zerodha Varsity's pedagogy (plain language, analogies, short single-idea chapters, "Key
Takeaways", three difficulty tiers, end-of-module quizzes, certification). It spans 17 modules
from "what is AI" through classical ML, deep learning, transformers, LLMs, reinforcement
learning & reasoning, generative AI, building a custom LLM end-to-end, RAG/agents, MLOps/LLMOps,
responsible AI, and career readiness. Every chapter ships runnable code; every module ends in
graded exercises and a build-something capstone. The goal is a deployed, demonstrable platform
where a complete beginner on a low-spec laptop can become job-ready — and where the platform's
own engineering proves production AI/web depth.

## Audience — two audiences, kept distinct
1. THE LEARNER (the product's user): a BROAD audience — true beginners, non-CS folks, junior
   programmers, and career switchers. Content must start from zero, use analogies before symbols,
   and never assume prior ML. Three difficulty tiers per topic: Beginner / Intermediate / Advanced.
2. THE BUILDER (me, who runs Claude Code): a senior backend engineer (10+ yrs Java full-stack)
   transitioning into AI engineering. Code, build tooling, READMEs, and decisions must read as the
   work of someone who can take a system from prototype to reliable production. Favour clarity and
   correctness over cleverness, in both prose and code.

## The "Varsity contract" (the pedagogy gate — non-negotiable for every chapter)
Every chapter MUST contain, in this order:
1. A hook: a real-world analogy or a working demo first (taste before theory).
2. Plain-language explanation, one concept per chapter, ~1,500–3,000 words OR a 15–25 min notebook.
3. At least one runnable worked example (a notebook cell or snippet that actually executes).
4. A "Key Takeaways" box: 3–6 numbered points.
5. 2–4 hands-on exercises with auto-graders and hidden solution walkthroughs.
Front-matter on every chapter: title, module, chapter, difficulty (beginner|intermediate|advanced),
prereqs, learning_objectives, compute (browser|colab|gpu), status (stable|frontier),
last_reviewed (date), est_minutes. No chapter is "done" until it satisfies this contract and passes CI.

## Architecture (6 subsystems)
1. Content System — modules -> chapters -> lessons authored as Quarto (.qmd) + Jupyter (.ipynb);
   the per-chapter template; the 17-module curriculum itself; the style guide & tone.
2. Build & Publish System — Quarto static-site generation, theming (Key Takeaways box,
   difficulty badges, dark/sepia mode), navigation, search; hosting on GitHub Pages/Netlify.
3. Interactive Compute Layer — in-browser Python (JupyterLite/Pyodide) for beginner chapters so
   they run with zero install; "Open in Colab/Kaggle" buttons for GPU chapters; notebook templates.
4. Exercise & Auto-Grading System — assert-based unit-test graders runnable in-browser, MCQ
   concept checks, scaffolded difficulty (fill-in-the-blank -> implement -> open-ended), hidden solutions.
5. Assessment, Progress & Certification System — per-module quizzes, capstone rubrics,
   spaced-repetition review, progress tracking, learning tracks, certificate issuance.
6. Currency & Ops System — CI gates (execute notebooks, lint prose, link-check, spell-check),
   version pinning, "last_reviewed" dates, quarterly refresh, changelog, community-PR pipeline.
Cross-cutting: accessibility (free-tier-first, ₹0 path), correctness review, docs-as-code discipline.

## Tech stack (chosen for docs-as-code + low-spec author + ₹0 learner)
- Authoring: Quarto (.qmd) + Jupyter notebooks (.ipynb) + Markdown. Everything is plain text and diffable.
- In-browser compute: JupyterLite + Pyodide (e.g. quarto-live) for M0–M4 and all quick "try it" cells.
- GPU compute (external, never local): Google Colab + Kaggle free tiers for M5–M10; a rented GPU
  (RunPod/Vast.ai, billed by the second) ONLY for the M11 custom-LLM pretraining capstone.
- Hosting + CI: GitHub + GitHub Actions; static deploy to GitHub Pages / Netlify / Vercel.
- Quiz/progress/cert layer: start static (JS quiz engine reading chapter front-matter; progress in
  browser storage); add a minimal backend only when certification needs server-side proctoring.
- Quality tooling: papermill/nbval (execute notebooks in CI), markdownlint + Vale (prose), a
  link-checker, codespell.
- LLM access used INSIDE lessons: env-var driven; every paid-API example (OpenAI/Anthropic/Gemini)
  ships with a free local fallback (Ollama) or free tier (Groq/Gemini). Keys are never required to learn.

## Environment constraints
- The BUILDER's laptop is low-spec. It runs only Claude Code + editor + a browser + the Quarto CLI
  + Docker for local site preview. No model and no GPU job ever runs on it.
- GPU-dependent chapters are authored and test-executed on Colab/Kaggle (or a short rented-GPU
  session), NOT locally. CI executes only the CPU/in-browser notebooks; GPU notebooks are validated
  via a documented manual Colab run recorded in the chapter's PR.
- Free-tier-first is a PRODUCT PRINCIPLE and a BUILD PRINCIPLE: a learner must be able to complete
  Modules 0–10 for ₹0 (browser + Colab/Kaggle + Ollama). The only optional spend is a few hundred
  rupees of rented GPU time for the M11 capstone, and even that has a smaller-model free path.
- Cost/accessibility discipline is a first-class, visible feature: ship a "What you need & what it
  costs" chapter in M0 with the ₹0 path stated up front.

## Working agreement (how you, Claude Code, must operate)
- **One module (or one subsystem) per session**, built in dependency order. Do not scaffold the
  whole curriculum at once.
- **Pedagogy gate before content scale.** In P0, before authoring any module at scale, build and
  prove: the per-chapter template, the in-browser runner, the auto-grader harness, the quiz engine,
  and the CI notebook-execution gate — on ONE complete sample chapter end-to-end. Every later chapter
  must pass these gates. (This is the content-platform equivalent of "evals before features".)
- **Plan before writing.** For any non-trivial chapter, module, or code task, first output a short
  plan (files to touch, the analogy/hook, the worked example, the exercises, test/grader strategy,
  risks) and WAIT for my approval before producing it.
- **Everything runs.** Every notebook must execute top-to-bottom in CI (CPU/in-browser) or be
  manually Colab-verified (GPU) with the result recorded. No "illustrative" code that doesn't run.
- **Correctness over coverage.** A wrong explanation is worse than a missing one. Flag anything you
  are unsure is current or accurate; do not bluff. Mark fast-moving content status: frontier.
- **Small, reviewable diffs.** Prefer one chapter (or one task) per commit with clear messages.
- **Decisions are logged.** Any pedagogical OR technical choice (chunking strategy, which framework
  a lesson teaches, compute tier for a chapter, quiz format, tokenizer used in M11, hosting,
  grader design) gets a dated entry in docs/DECISIONS.md with options considered + rationale.
  This doubles as my interview prep — be thorough on the "why."
- **No secrets in code or notebooks.** Use env vars + .env.example. Lesson API examples read keys
  from the environment and always show the free fallback. Never print real keys.
- **Ask, don't assume.** If a requirement is ambiguous, ask one focused question. State any
  assumption you do make, inline.
- **Honesty over agreeableness.** If a chapter ordering is confusing, a topic is missing, or a
  shortcut creates content/tech debt, say so and propose the better path.

## Repo conventions
- /modules/<NN>-<slug>/ — each module: chapters as .qmd/.ipynb, a module README (objectives,
  prereqs, chapter list, capstone), quiz.yml, capstone.md with a rubric.
- /site — _quarto.yml, theme/CSS (Key Takeaways box, difficulty badges, dark/sepia), nav, search.
- /lib — shared grader utilities, notebook helpers, the in-browser runner glue.
- /assessments — quiz engine, certification exam config, learning-track definitions.
- /infra — GitHub Actions workflows, docker-compose for local preview, deploy config.
- /docs — ROADMAP.md, DECISIONS.md, STYLE_GUIDE.md (the Varsity contract + tone), CHAPTER_TEMPLATE.md,
  RUNBOOK.md, CONTRIBUTING.md, PORTFOLIO.md, per-phase specs under docs/phases/.
- Conventional commit messages. Feature branches; CI must pass before merge to main.

## Definition of Done (every phase / every module)
- [ ] Every chapter satisfies the Varsity contract (hook -> explanation -> runnable example ->
      Key Takeaways -> 2–4 graded exercises) and has complete front-matter incl. last_reviewed.
- [ ] All in-browser/CPU notebooks execute cleanly in CI; GPU notebooks are Colab-verified and the
      run is recorded in the PR.
- [ ] Exercises have working auto-graders + hidden solution walkthroughs; the module quiz exists;
      the capstone has a rubric.
- [ ] Beginner chapters verified to run in JupyterLite (₹0); GPU chapters have working
      Colab/Kaggle buttons. The free-tier path for the module is confirmed.
- [ ] Module README + docs/DECISIONS.md updated; STYLE_GUIDE adhered to (lint/prose checks pass).
- [ ] Builds cleanly from a fresh clone; a preview deploy renders correctly.
- [ ] A "5-minute learner walkthrough" path through the new content that I can click/run.
- [ ] A resume-ready, quantified bullet drafted in docs/PORTFOLIO.md (e.g. "authored + auto-graded
      X chapters across Y modules; Z% of content runs in-browser at zero cost").