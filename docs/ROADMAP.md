# Larnix — Product & Build Roadmap

> Status: **APPROVED (2026-06-28).** Build proceeds in dependency order P0 → P7. No chapters or
> application code are written until each phase's entry criteria are met; P0 has not started yet.
> See `CLAUDE.md` (operating agreement) and `STYLE_GUIDE.md` (the Varsity contract).
>
> Last updated: 2026-06-28

## How this document fits the docs-set (reconciliation map)

This roadmap is the **executive spine**. It is consistent with, and defers detail to, the other
canonical docs. Where they go deeper, this file points to them rather than duplicating (and
risking drift from) them:

| Doc | Role | This roadmap's relationship |
|-----|------|------------------------------|
| `CLAUDE.md` | Operating agreement (mission, subsystems, working rules, DoD) | Source of truth for principles; quoted, not restated. |
| `docs/Larnix-PLAN.md` | **Canonical full curriculum** (module chapters, prereqs, infra ladder, outcomes) | Module map, chapter counts, prereqs in §2 below are **synced to PLAN**. |
| `docs/RISKS.md` | **Living 14-risk register** (R1–R14, owners, triggers, cadence) | §4 below is the executive top-5, using RISKS.md's canonical IDs. RISKS.md is authoritative. |
| `docs/STYLE_GUIDE.md` + `docs/CHAPTER_TEMPLATE.md` | The pedagogy gate (Varsity contract, tiers, compute/status fields, front-matter) | Difficulty/compute/status notation here matches the style guide exactly. |
| `docs/DECISIONS.md` | Dated decision log | Choices implied here get logged there when made. |

**Reconciliation actions taken in this revision** (cross-check vs PLAN/RISKS/STYLE_GUIDE):
1. Module titles, chapter-count estimates, prerequisites, and difficulty tiers in §2 are now
   **aligned to `Larnix-PLAN.md`** (previously they were independent estimates).
2. Difficulty uses the style guide's **🟢/🟡/🔴** notation (with B/I/A in prose); compute uses the
   canonical **`browser | colab | gpu`** field.
3. The risk register (§4) is **re-keyed to RISKS.md IDs (R1, R3, R9, R10, R12)** so the two docs
   can't diverge; RISKS.md remains the authoritative living register with all 14 risks + triggers.
4. The phase plan (§3) adds **P7 (ongoing maintenance/currency)** to match PLAN, and names the
   **learning tracks + "AI Engineer Certified"** credential in P6.
5. The M11 capstone is upgraded to PLAN's full pipeline (**data → tokenizer → pretrain →
   post-train → quantize/GGUF → serve via Ollama + vLLM**).
6. Added a **free-tier compute/cost ladder** (§2.1) and a **2026 market-alignment table** (§5.1)
   grounded in current hiring data — see Sources at the end.

---

## 1. Product vision & the single end-to-end learner journey

**Vision.** Larnix is a free, open-access, beginner-to-frontier school for AI/ML that takes a
complete beginner on a low-spec laptop — no GPU, no prior ML, possibly non-CS — and makes them
**job-ready as an AI/LLM engineer at ₹0** for the core path. It borrows Zerodha Varsity's
pedagogy wholesale: plain language, an analogy or working demo *before* any symbol, short
single-idea chapters, "Key Takeaways" boxes, three difficulty tiers per topic, graded exercises,
end-of-module quizzes, capstones, and certification. Every chapter ships code that actually runs —
in the browser for foundations, on free Colab/Kaggle GPUs for deep learning and LLMs, and on a
brief rented GPU only for the one custom-LLM pretraining capstone. The platform's own engineering
(Quarto docs-as-code, in-browser Pyodide compute, an auto-grader harness, CI that executes every
notebook, a quiz/cert layer) is itself a production-grade portfolio piece that proves the builder
can ship reliable AI/web systems. The curriculum is deliberately aimed at **what employers
actually hire for in 2026** — LLM fine-tuning, RAG, agents, MLOps, and *evaluation* — not at
skills the market has already commoditized (see §5.1).

**The forcing journey (zero → job-ready).** One learner, "Asha," a non-CS career switcher on a
4 GB laptop, walks the full spine and in doing so forces us to build every subsystem and every
difficulty tier:

1. **Lands cold (M0).** Reads "What is AI" and the "Prerequisites & Setup / what it costs"
   chapter, confirms the ₹0 path, and runs her first pretrained model *in the browser* with zero
   install. → *Forces: Quarto site, theme/design system, JupyterLite runner, chapter template,
   the cost chapter.*
2. **Builds literacy (M1–M3).** Python, the math that matters, and data wrangling — all
   in-browser, all auto-graded, all 🟢/🟡 tier. → *Forces: in-browser auto-grader at scale, MCQ
   quiz engine, beginner-tier scaffolding.*
3. **Trains real models (M4–M6).** Classical ML (still in-browser; a couple of heavier chapters
   offer a free Colab fallback), then neural nets from scratch and in PyTorch (M5) and CNNs/RNNs
   (M6) on **free Colab/Kaggle GPUs** via one-click "Open in Colab." → *Forces: GPU compute layer,
   Colab templates, GPU-notebook CI policy, 🟡 tier.*
4. **Reaches the frontier (M7–M10).** Transformers from scratch, using/fine-tuning LLMs (LoRA),
   RL/RLHF/DPO/GRPO + reasoning models, and diffusion/multimodal — running models locally via
   **Ollama** with free-API fallbacks. → *Forces: Ollama + free-API fallback pattern, 🔴 tier,
   frontier-status currency tooling.*
5. **Builds her own LLM (M11).** Curates data, trains a tokenizer, pretrains a small GPT,
   post-trains it, quantizes to GGUF, and serves it via Ollama + vLLM — on a **rented GPU billed
   by the second**, with a smaller free-tier path. → *Forces: rented-GPU runbook,
   distributed-training content, cost discipline under real spend.*
6. **Becomes an engineer (M12–M13).** Ships a grounded RAG system and a tool-using agent over
   **MCP**, then wraps it in production MLOps/LLMOps (CI/CD, **evaluation harnesses**, monitoring,
   cost control). → *Forces: agents/MCP content, deployment patterns, the eval thread.*
7. **Gets hired (M14–M16).** Learns responsible AI & the **OWASP LLM Top 10**, completes an
   applied elective in her domain, then does interview prep (incl. ML/LLM system design), builds a
   portfolio, earns the **certificate**, and follows a spaced-repetition review track. → *Forces:
   certification/exam engine, learning tracks, spaced-repetition, the launch.*

Because Asha must succeed end-to-end at near-zero cost, every subsystem (content, build/publish,
interactive compute, auto-grading, assessment/cert, currency/ops) and every difficulty tier
(🟢 → 🟡 → 🔴) becomes mandatory, not optional.

**Cross-cutting thread — evaluation & measurement.** 2026 hiring data shows the single skill that
separates senior from junior AI engineers is the ability to *measure whether an AI system works*.
Larnix therefore treats evaluation as a spine, not a topic: introduced in M4 (metrics, CV), made
rigorous in M8 (LLM eval, AI-as-judge), applied in M9 (before/after reasoning evals), M11 (eval
your custom model), M12 (RAG eval), and M13 (online eval, regression testing, drift). Every
capstone is graded partly on "did you measure it?"

---

## 2. Module map (M0–M16) — synced to `Larnix-PLAN.md`

Difficulty uses the style guide's tiers: 🟢 **Beginner (B)** · 🟡 **Intermediate (I)** · 🔴
**Advanced (A)**; a `→` means the module spans tiers. Compute is the style guide's per-chapter
field (`browser | colab | gpu`); the column shows each module's **dominant** tier (individual
chapters may differ — e.g. a couple of heavier M4 chapters such as XGBoost ship a free Colab
fallback, while many M12 demos run in-browser). This matches the canonical compute buckets in
`CLAUDE.md` (browser = M0–M4, free Colab/Kaggle = M5–M10, rented GPU = M11 only). Chapter counts
are PLAN's canonical estimates.

| # | Module | Tier | Prereqs | ~Ch | Compute | Capstone |
|---|--------|------|---------|-----|---------|----------|
| **M0** | How to Use This School / What is AI? (incl. Prerequisites & Setup / what it costs) | 🟢 B | none | 6 | browser | Set up the ₹0 toolchain; run your first pretrained model |
| **M1** | Python for AI | 🟢 B | none | 14 | browser | Data-cleaning CLI/notebook (auto-graded) |
| **M2** | Math You Actually Need (intuition-first) | 🟢→🟡 | M1 | 16 | browser | "Math of one neuron" forward+backward notebook |
| **M3** | Data & Tooling (NumPy/Pandas/viz/envs) | 🟢→🟡 | M1 | 14 | browser | End-to-end EDA on a real public dataset |
| **M4** | Classical Machine Learning | 🟡 I | M2, M3 | 20 | browser | End-to-end tabular predictor + model card |
| **M5** | Deep Learning Foundations | 🟡 I | M4 | 18 | colab | Neural net from scratch → re-implemented in PyTorch |
| **M6** | Specialized DL: Vision & Sequences (CNNs, RNN/LSTM, embeddings) | 🟡→🔴 | M5 | 14 | colab | Image classifier app + char-level sequence model |
| **M7** | NLP & the Transformer | 🔴 A | M5, M6 | 14 | colab | Build a small GPT from scratch (nanoGPT-style) |
| **M8** | Large Language Models (adapt + evaluate) | 🔴 A | M7 | 16 | colab | Fine-tune (LoRA) + rigorously evaluate a small LLM |
| **M9** | Reinforcement Learning & Reasoning Models | 🔴 A | M5, M8 | 14 | colab | Post-train a model to reason measurably better (before/after evals) |
| **M10** | Generative AI (diffusion, multimodal, audio) | 🔴 A | M7 | 12 | colab | Text-to-image mini-app + multimodal "describe this image" |
| **M11** | Build Your Own LLM End-to-End | 🔴 A | M7, M8, M9 | 18 | gpu | **Custom LLM: data → tokenizer → pretrain → post-train → quantize (GGUF) → serve (Ollama + vLLM)** |
| **M12** | AI Engineering: RAG, Agents & MCP | 🟡→🔴 | M8 | 20 | colab + browser | Production-style RAG + tool-using agent over MCP, with eval |
| **M13** | Production AI: MLOps & LLMOps | 🔴 A | M12 | 16 | colab + browser | Deployed, monitored, cost-instrumented AI service with CI/CD |
| **M14** | Responsible AI: Safety, Security, Ethics | 🟡→🔴 | M8, M12 | 12 | browser | Red-team & harden your app against the OWASP LLM Top 10 |
| **M15** | Applied ML Electives (pick-N: forecasting / recsys / speech / tabular DL / GNN) | 🟡→🔴 | M4, M6 | 12 | colab + browser | One elective shipped end-to-end |
| **M16** | Career & Job-Readiness | 🟢→🔴 | any | 12 | browser | Portfolio of 3–4 deployed projects + passed mock-interview loop |

**Totals.** ~**248 chapters** across 17 modules at full build; ~**180 are stable-core** (math,
classical ML, backprop, transformers — written to last) with a deliberately small frontier
surface (specific models/tools/vector-DBs — version-pinned, dated, swappable). Browser-runnable
share targeted high (all of M0–M3, M14, M16 plus every "try it" cell) to protect the ₹0 promise:
**a learner completes M0–M10 for ₹0**.

### 2.1 Free-tier compute & cost ladder (the ₹0 spine)

From `Larnix-PLAN.md` §B0 — *nothing paid until a module truly needs it, and every paid step has
a free or local alternative.* This is both a product principle and a build principle.

| Tier | First needed in | What you need | Free / local default | Optional paid (scale/convenience) |
|------|-----------------|---------------|----------------------|-----------------------------------|
| 0 — Just a browser | M0–M4 | Browser | JupyterLite in-page; Colab free | — |
| 1 — Free GPU notebooks | M5–M10 | Google + Kaggle + HF accounts | Colab T4, Kaggle weekly GPU hours, HF Hub | Colab Pro for longer GPUs |
| 2 — Hosted LLM APIs | M8, M12, M14 | An LLM API key | **Ollama** (no key); Groq / Gemini free tiers | OpenAI / Anthropic / Gemini pay-per-token |
| 3 — Local inference | M11, M13 | Run models locally | Ollama / llama.cpp / LM Studio + GGUF | Consumer GPU |
| 4 — Train a custom LLM | M11, M9 | Cloud GPU + HF Hub | Small model on free T4; smaller-model free path | Rent A100/H100 by the second (RunPod/Lambda/Vast.ai/Modal) |
| 5 — Production / MLOps | M12–M13 | Git, Docker, vector DB, tracking | Chroma/pgvector local; Qdrant/MLflow/W&B free tiers | Managed vector DB / observability |

Infra is taught **just-in-time**: the setup chapter ships inside M0; the "Cloud GPU & training
setup" chapter ships inside M11 — never front-loaded.

---

## 3. Phase plan (P0–P7), in dependency order

Each phase lists **goal · subsystems + modules · skills/pedagogy · entry criteria · exit criteria
(DoD)**. The phase DoD is *in addition* to the per-chapter Varsity contract (`STYLE_GUIDE.md §11`)
and the per-module DoD in `CLAUDE.md`. Phases map 1:1 to PLAN's roadmap.

### P0 — Platform MVP + the pedagogy gate
- **Goal.** Build and *prove* the entire content-delivery machine on **one** complete sample
  chapter before any module is authored at scale ("evals before features").
- **Subsystems.** Content (chapter template), Build & Publish (Quarto site, theme/design system,
  nav, search, difficulty badges, Key Takeaways box, dark/sepia), Interactive Compute
  (JupyterLite/Pyodide runner + "Open in Colab"), Exercise & Auto-Grading (assert-based in-browser
  harness, MCQ), Assessment (JS quiz engine from front-matter), Currency & Ops (CI: execute
  notebooks via nbval/papermill, markdownlint + Vale, link-check, codespell, deploy).
  **Modules.** None at scale — one sample chapter only.
- **Skills/pedagogy.** Proves the Varsity contract is mechanically enforceable; docs-as-code; CI
  as a quality gate; the ₹0 in-browser path.
- **Entry.** Empty repo; `CLAUDE.md` agreed; this roadmap approved.
- **Exit (DoD).**
  - [ ] Quarto site builds from a fresh clone and CI-deploys to a public preview URL.
  - [ ] Theme implements Key Takeaways box, difficulty badges, dark/sepia, nav + search.
  - [ ] `CHAPTER_TEMPLATE.md` + front-matter schema enforced by lint.
  - [ ] One sample chapter satisfies the full Varsity contract end-to-end.
  - [ ] Its notebook runs in JupyterLite (₹0) **and** executes in CI.
  - [ ] ≥1 exercise auto-graded in-browser with a hidden solution walkthrough.
  - [ ] Quiz engine renders + scores an MCQ client-side.
  - [ ] CI green: notebook execution, Vale, markdownlint, link-check, spell.
  - [ ] The R1/R3/R6/R10 automated gates exist (currency check, browser-import lint,
        free-fallback check, runs-in-CI) per `RISKS.md §5`.

### P1 — Foundations track (M0–M3)
- **Goal.** Author zero-to-literate entirely in-browser at ₹0: orientation + setup/cost chapter,
  Python, math-that-matters, data wrangling.
- **Subsystems.** Content (M0–M3), Interactive Compute (Pyodide at scale), Auto-Grading (scaled,
  beginner scaffolding), Assessment (per-module quizzes + first capstone rubrics), Currency/Ops.
  **Modules.** M0, M1, M2, M3.
- **Skills/pedagogy.** 🟢 tier; analogy-before-symbol; the explicit ₹0 cost chapter; scaffolded
  difficulty; proving the in-browser grader scales.
- **Entry.** P0 DoD met.
- **Exit (DoD).**
  - [ ] M0–M3 complete; every chapter passes the Varsity contract + CI.
  - [ ] 100% of M0–M3 notebooks run in JupyterLite (₹0 confirmed).
  - [ ] Each module has a quiz + a graded capstone with a rubric.
  - [ ] M0 ships "Prerequisites & Setup / what it costs" stating the ₹0 path up front.
  - [ ] A non-technical learner can go zero → EDA capstone in-browser; `PORTFOLIO.md` bullet drafted.

### P2 — Core ML & Deep Learning (M4–M6)
- **Goal.** Classical ML → deep learning → CNNs/RNNs; introduce the free-GPU workflow; prove
  auto-graders work for model-training exercises.
- **Subsystems.** Content (M4–M6), Interactive Compute (Colab/Kaggle integration, GPU templates),
  Auto-Grading (seeded/tolerance asserts for stochastic outputs), Currency/Ops (GPU-notebook CI
  policy: manual Colab verification recorded in PR).
  **Modules.** M4, M5, M6.
- **Skills/pedagogy.** 🟡 tier; browser→Colab handoff; reproducibility/version pinning under GPU;
  model cards as habit; first real evaluation practice.
- **Entry.** P1 DoD met.
- **Exit (DoD).**
  - [ ] M4–M6 complete; classical ML stays in-browser where feasible.
  - [ ] Every GPU chapter has a working "Open in Colab/Kaggle" button + a recorded manual run.
  - [ ] Auto-graders handle stochastic training (seeded/tolerance asserts).
  - [ ] Free-tier path confirmed on free Colab/Kaggle; per-module quizzes + rubric'd capstones.

### P3 — Transformers, LLMs, RL & Reasoning, Generative AI (M7–M10)
- **Goal.** Reach the frontier: transformers from scratch; using/fine-tuning LLMs (LoRA + eval);
  RL/RLHF/DPO/GRPO + reasoning; diffusion/multimodal — runnable free via Ollama + free API tiers.
- **Subsystems.** Content (M7–M10), Interactive Compute (Ollama + Groq/Gemini fallback pattern;
  env-var keys + `.env.example`), Currency/Ops (`status: frontier` + quarterly-refresh process).
  **Modules.** M7, M8, M9, M10.
- **Skills/pedagogy.** 🔴 tier; "every paid example ships a free fallback"; correctness on
  fast-moving topics (flag-don't-bluff); rigorous LLM evaluation; frontier currency discipline.
- **Entry.** P2 DoD met.
- **Exit (DoD).**
  - [ ] M7–M10 complete; every LLM/API example has an Ollama or free-tier fallback (keys never required).
  - [ ] No secrets in notebooks; keys read from env.
  - [ ] Fast-moving chapters carry `status: frontier` + `last_reviewed`; refresh process documented.
  - [ ] GPU chapters Colab-verified & recorded; per-module quizzes + rubric'd capstones.

### P4 — Build Your Own LLM end-to-end (M11)
- **Goal.** The signature module: data → tokenizer → pretrain → distributed training → post-train
  → quantize (GGUF) → serve (Ollama + vLLM), on a rented GPU billed by the second, with a smaller
  free path.
- **Subsystems.** Content (M11), Interactive Compute (rented-GPU runbook — RunPod/Vast.ai/Modal —
  + smaller-model free path), Currency/Ops (cost-tracking, asset/license ledger), Assessment (the
  most rigorous capstone rubric).
  **Modules.** M11.
- **Skills/pedagogy.** 🔴 tier; cost discipline under real spend (default path ≤ ₹500, with a free
  path); distributed training (FSDP/DeepSpeed/ZeRO); full reproducibility of an expensive run;
  data provenance/licensing taught explicitly.
- **Entry.** P3 DoD met.
- **Exit (DoD).**
  - [ ] M11 complete; a learner can pretrain a small (~100M–1B) GPT and serve it via Ollama + vLLM.
  - [ ] A documented free/smaller-model path completes M11 at ₹0.
  - [ ] `RUNBOOK.md` covers rent → train → checkpoint → tear-down (stop the meter) + cost log.
  - [ ] Distributed-training chapter included; capstone rubric records the run + spend; scope copy
        manages the "expected GPT-4" risk (`RISKS.md R2`); asset licenses logged (`R11`).

### P5 — AI Engineering + Production MLOps/LLMOps (M12–M13)
- **Goal.** Turn model-builders into shippers: RAG, agents & MCP; then serving, CI/CD, evals,
  monitoring, cost control for ML and LLM systems.
- **Subsystems.** Content (M12–M13), Interactive Compute (browser demos + Colab + local Ollama),
  Assessment (production-grade rubrics with eval gates), Currency/Ops (these modules dogfood the
  platform's own ops).
  **Modules.** M12, M13.
- **Skills/pedagogy.** 🔴 tier; evaluation-first engineering (the senior/junior separator);
  observability & cost; the builder's backend strengths surface (system design, reliability).
- **Entry.** P4 DoD met.
- **Exit (DoD).**
  - [ ] M12–M13 complete; RAG + agent-over-MCP capstone runs with a free fallback.
  - [ ] MLOps capstone deploys a service with CI/CD, an eval gate, monitoring & a cost budget.
  - [ ] Per-module quizzes + rubric'd capstones; stack choices logged in `DECISIONS.md`.

### P6 — Responsible AI, Applied Electives, Career & Job-Readiness + Launch (M14–M16)
- **Goal.** Close the loop to "job-ready": responsible AI & OWASP LLM Top 10; an applied elective;
  portfolio/interview prep; certification, learning tracks, spaced-repetition — and public launch.
- **Subsystems.** Content (M14–M16), Assessment & Certification (exam config, certificate
  issuance, spaced-repetition, learning-track definitions in `/assessments`), Build & Publish
  (launch polish, landing), Currency/Ops (quarterly-refresh cadence operationalized).
  **Modules.** M14, M15, M16.
- **Skills/pedagogy.** Responsible-AI literacy; ML/LLM system-design interview prep; the full
  certification + spaced-repetition + tracks experience; honest outcome framing (`RISKS.md R5`).
- **Entry.** P5 DoD met.
- **Exit (DoD).**
  - [ ] M14–M16 complete; OWASP LLM Top 10 red-team capstone shipped.
  - [ ] Certification exam + certificate issuance work; **named learning tracks** live —
        *Absolute Beginner → ML Practitioner → AI Engineer (LLMs) → LLM Builder → MLOps/Production*,
        gated final **"AI Engineer Certified"** (on the M11 + M12–13 capstones); spaced-repetition live.
  - [ ] Full zero→job-ready journey clickable end-to-end; launch checklist green.
  - [ ] No guaranteed-outcome claims in copy (`R5`); accounts/PII deferred or privacy-reviewed (`R7`).
  - [ ] `PORTFOLIO.md` carries the headline quantified bullet for the whole platform.

### P7 — Maintenance & currency (ongoing)
- **Goal.** Keep the largest practical risk (`R9`) and staleness (`R1`) in check forever.
- **Subsystems.** Currency & Ops primarily; all content secondarily.
- **Activities.** Quarterly review sprint + per-chapter owners; "What changed in AI" changelog;
  community-PR pipeline (`CONTRIBUTING.md`, good-first-issue); the automated triggers in
  `RISKS.md §5` gate every PR.
- **Entry.** Anything shipped. **Exit.** Never closes; lives in maintenance.

---

## 4. Risk register — executive top-5 (authoritative register: `docs/RISKS.md`)

`RISKS.md` is the **living register of all 14 risks** (R1–R14) with owners, measurable triggers,
and a review cadence. Below are the top-5 the brief calls out, **using RISKS.md's canonical IDs**
so the two documents cannot diverge, each mapped to how the phases de-risk it.

| ID | Risk | Why it hurts Larnix | How the phases de-risk it |
|----|------|---------------------|---------------------------|
| **R1** | **Frontier content goes stale** | AI moves weekly; a wrong "latest model/API" makes the platform look untrustworthy | P0 builds the `currency_check` CI gate + `status`/`last_reviewed` front-matter; P3 isolates the fastest content (M7–M10) and stands up quarterly refresh; P7 operationalizes the cadence + changelog. Stable-core kept large, frontier surface small. |
| **R3** | **In-browser compute limits break a lesson** | Pyodide has memory/package/GPU limits; breaks the ₹0 promise if hit silently | P0 builds a lint that *rejects a `browser` chapter importing a non-Pyodide package*; P1 keeps foundations Pyodide-safe; P2 introduces the clean browser→Colab handoff; P4 reserves rented GPU for M11 only, always with a free path. |
| **R9** | **Content-maintenance burden / scope creep (~240+ chapters; ~180 stable-core)** | The biggest *practical* risk: easy to start, hard to keep correct & current; scope sprawl stalls everything | `CLAUDE.md`'s "one module/subsystem per session"; P0 forbids authoring at scale until the gate passes; hard per-phase DoD; pick-N electives (M15); community-PR pipeline from P6; trigger pauses authoring when the maintenance backlog exceeds cap. |
| **R10** | **AI-drafted content contains errors** | A wrong explanation teaches the wrong thing and destroys credibility | "Every code block runs in CI" (P0+); GPU notebooks Colab-verified & recorded (P2+); correctness-review box in the chapter DoD; flag-don't-bluff + `status: frontier`; never invent a citation; regression example added on any found error. |
| **R12** | **Learner drop-off / low completion** | A long curriculum for a broad audience has high attrition; unfinished ≠ mission achieved | Varsity pedagogy from P0 (hook-first, one idea, short chapters); fast win in M0 (run a model in 5 lines); three tiers + named tracks so beginners aren't shown 🔴 modules; quizzes/progress from P1; capstones each module; P6 adds certification + spaced-repetition to pull learners back. |

*Also tracked in `RISKS.md` and relevant here:* R2 (custom-LLM scope expectation, P4), R5
("job-ready" ≠ guaranteed offer, P6), R6 (no forced API spend, P0+), R7 (DPDP/GDPR, P6), R11
(dataset/model licensing, P3–P4), R13 (free-tier changes), R14 (solo-maintainer bus factor).

---

## 5. Curriculum coverage map (foundation → frontier, no gaps)

Each in-demand skill is mapped to where it is **taught** and where it is **practiced**
(exercise / capstone).

| In-demand skill | Taught in | Practiced in (exercise / capstone) |
|-----------------|-----------|-------------------------------------|
| Python for AI/ML | M1 | M1 auto-graded exercises + data-cleaning capstone |
| Math (linear algebra, calculus, probability, statistics) | M2 | M2 "math of one neuron" capstone |
| Data wrangling / EDA / visualization | M3 | M3 end-to-end EDA capstone |
| Classical ML (regression, trees, ensembles, model selection) | M4 | M4 tabular-predictor capstone + model card |
| Deep learning (neural nets, backprop, PyTorch) | M5 | M5 "scratch then PyTorch, beat baseline" capstone |
| CNNs (computer vision) | M6 | M6 fine-tune pretrained CNN + inference demo |
| RNNs / sequence models / embeddings | M6 | M6 char-level sequence-model capstone |
| Transformers & attention (from scratch) | M7 | M7 "build a small GPT" capstone |
| LLM usage / prompting / fine-tuning (PEFT/LoRA, eval) | M8 | M8 LoRA fine-tune + eval-vs-base capstone |
| LLM **evaluation** (perplexity, functional correctness, AI-as-judge) | M8 (+ M12/M13) | M8 eval harness; M12 RAG eval; M13 online eval/regression |
| RL / RLHF / DPO / GRPO (+ reasoning, verifiable rewards) | M9 | M9 post-train-to-reason-better capstone (before/after evals) |
| Diffusion / multimodal generative AI | M10 | M10 text-to-image + multimodal demo |
| Custom-LLM pretraining (data→tokenizer→pretrain→post-train→quantize→serve) | M11 | M11 custom-LLM capstone |
| Distributed training (FSDP/DeepSpeed/ZeRO, mixed precision) | M11 | M11 multi-GPU job + recorded run |
| RAG (retrieval, chunking, hybrid search, reranking) | M12 | M12 grounded RAG capstone |
| Agents & MCP (tool use, multi-agent, function calling) | M12 | M12 tool-using agent-over-MCP capstone |
| MLOps / LLMOps (serving, CI/CD, monitoring, drift, cost) | M13 | M13 deployed-monitored-cost-instrumented capstone |
| Responsible AI / security / OWASP LLM Top 10 | M14 | M14 OWASP red-team + mitigation capstone |
| Applied domain depth (forecasting/recsys/speech/tabular DL/GNN) | M15 | M15 learner-chosen end-to-end project |
| Interviews / ML & LLM system design / portfolio / certification | M16 | M16 portfolio + mock-interview + certificate |

**Gap check.** Foundations (M0–M3) → classical ML (M4) → DL & architectures (M5–M7) → applied
LLM/RL/GenAI frontier (M8–M11) → engineering & ops (M12–M13) → responsibility, application, career
(M14–M16). No band is skipped; every adjacent pair shares a prerequisite edge.

### 5.1 2026 market alignment (does Larnix teach what employers hire for?)

Grounded in current hiring analyses (Jun 2026; see Sources). The point: Larnix concentrates on the
**differentiators and high-pay specializations**, treats **table-stakes** as baseline, and
deliberately *doesn't* over-invest in **declining** skills.

| 2026 hiring signal | Market status | Where Larnix covers it |
|--------------------|---------------|------------------------|
| Python, PyTorch, Git, SQL, CLI, basic ML, prompt engineering | **Table-stakes** (90%+ of postings) | M1, M3, M4, M5; prompt engineering folded into M8/M12 as baseline (not a standalone module — matches the market) |
| **LLM fine-tuning & inference optimization** (LoRA/QLoRA, RLHF/DPO, quantization, vLLM) | **Top differentiator**, highest salary ceiling | M8 (LoRA + eval), M9 (RLHF/DPO/GRPO), M11 (quantize/GGUF + vLLM serving) |
| **MLOps & production deployment** (Docker/K8s, CI/CD, monitoring, drift) | Differentiator, most job options | M13 |
| **RAG architecture & vector DBs** (chunking, hybrid search, reranking) | Differentiator, dominant enterprise pattern | M12 |
| **AI agent development** (LangGraph/CrewAI, tool-calling, MCP, multi-agent) | Fastest-growing (~136% YoY) | M12 (MCP now the de-facto agent-integration standard) |
| **Evaluation & measurement** | The senior/junior separator | Cross-cutting thread: M8, M9, M12, M13 + every capstone rubric |
| Distributed training; RL; AI safety/alignment; CUDA/GPU | High-pay **specializations** | M11 (distributed training), M9 (RL), M14 (safety/OWASP); CUDA flagged as optional going-deeper |
| Standalone NLP; prompt-engineering-as-a-career; AutoML | **Declining / commoditized** | Intentionally *not* standalone modules; NLP folded into M6–M8, prompt-eng into M8/M12 — Larnix avoids over-investing here |
| Supplementary languages (Rust/Go/C++/TypeScript) | Growing for infra/apps | Python-first; noted as optional "going deeper" + a possible M15/M16 elective, not core |

**Frontier currency notes (status: frontier).** M9 should cover the 2026 post-training shift —
GRPO and verifiable-reward methods (DAPO/RLVR) now lead RLHF for reasoning/tool-use, per
DeepSeek-R1-style training. M12 should treat **MCP** as the de-facto standard (industry-wide
adoption across Anthropic/OpenAI/Google since its Nov-2024 launch). These are version-pinned and
on the quarterly refresh.

---

## 6. Learner-outcome map (what a graduate can build → roles)

| A Larnix graduate can demonstrably… | Evidence (capstones) | Prepares for role |
|-------------------------------------|----------------------|-------------------|
| Build, tune & evaluate classical ML models with model cards | M4 | **ML Engineer**, Data Scientist (entry) |
| Train deep nets, CNNs/RNNs; do transfer learning & deploy inference | M5–M6 | **ML Engineer** |
| Implement transformers from scratch & reason about attention | M7 | **Applied Scientist**, AI/LLM Engineer |
| Fine-tune open LLMs (LoRA), evaluate rigorously, run them locally | M8 | **AI/LLM Engineer** |
| Apply RL/RLHF/DPO/GRPO; understand reasoning models | M9 | Applied Scientist, **AI/LLM Engineer** |
| Build diffusion/multimodal generative apps | M10 | AI/LLM Engineer, GenAI Engineer |
| **Build a custom LLM end-to-end** incl. distributed training, with cost control | M11 | **AI/LLM Engineer**, Applied Scientist |
| Ship grounded RAG systems and tool-using agents over MCP | M12 | **AI/LLM Engineer** |
| Operate ML/LLM systems in production: CI/CD, evals, monitoring, cost | M13 | **MLOps / LLMOps Engineer** |
| Red-team & secure LLM apps against the OWASP LLM Top 10 | M14 | AI/LLM Engineer, ML Security |
| Deliver an end-to-end domain project & interview for the role | M15–M16 | All target roles |

**Target roles, explicitly:** **AI/LLM Engineer** (primary, hottest market — M8, M11, M12, M14),
**ML Engineer** (M4–M6, M13), **MLOps/LLMOps Engineer** (M13 + the platform's own CI/ops as a
portfolio proof), **Applied Scientist / Research Engineer** (M2, M7, M9, M11), and **Data
Scientist** (M4 + M15 electives). Job-readiness deliverables are baked in (M16): a public GitHub
portfolio of 3–4 deployed projects (incl. the custom LLM from M11 and the production RAG/agent app
from M12–13), a technical blog, coding + ML-theory + ML/LLM system-design interview prep, a passed
mock-interview loop, and the gated **"AI Engineer Certified"** credential.

---

## 7. Rough effort estimate per phase (part-time)

Assumptions: solo builder, **part-time ≈ 8–12 hrs/week**, Claude Code-assisted authoring on a
low-spec laptop, content-first. GPU modules add wall-clock for manual Colab/rented-GPU
verification, not build hours. Ranges are planning numbers, refined per-module in
`docs/phases/`.

| Phase | Scope | Effort (part-time weeks) | Notes |
|-------|-------|--------------------------|-------|
| **P0** | Platform MVP + pedagogy gate (1 sample chapter, full stack) | **4–6 weeks** | Highest leverage; front-loads all tooling. Do not rush. |
| **P1** | M0–M3 foundations, in-browser (~50 ch) | **9–13 weeks** | High chapter count, low compute friction. |
| **P2** | M4–M6 core ML & DL + Colab integration (~52 ch) | **9–13 weeks** | Colab-verification adds wall-clock. |
| **P3** | M7–M10 frontier (~56 ch) | **13–18 weeks** | Most demanding; correctness-heavy; frontier churn. |
| **P4** | M11 build-your-own-LLM (~18 ch) | **5–8 weeks** | One module but deep; rented-GPU runbook + reproducibility. |
| **P5** | M12–M13 AI engineering + MLOps/LLMOps (~36 ch) | **9–13 weeks** | Plays to backend strength; system-design heavy. |
| **P6** | M14–M16 + certification + launch (~36 ch) | **9–13 weeks** | Cert/exam engine + spaced-repetition + launch polish. |
| **P7** | Maintenance & currency | **ongoing** | ~ quarterly refresh sprints; community PRs offset over time. |
| **Total** | P0–P6 | **≈ 58–84 weeks (~13–19 months part-time)** | Sequential by dependency; some P5/P6 tooling can overlap late P4. |

---

## Appendix — sequencing principles (recap from `CLAUDE.md`)

- **Pedagogy gate before content scale** — P0 must fully pass before P1.
- **One module/subsystem per session**, strict dependency order.
- **Plan before writing** every non-trivial chapter/module; wait for approval.
- **Everything runs** (CI for CPU/browser; recorded Colab/rented-GPU for GPU).
- **Correctness over coverage**; flag-don't-bluff; `status: frontier` on fast-moving topics.
- **Decisions logged** in `docs/DECISIONS.md`; **₹0 free-tier path** is a product *and* build principle.

## Sources (market alignment, §1 & §5.1 — fetched 2026-06-28)

- JobsByCulture, *Top AI/ML Skills Employers Actually Hire For in 2026* (analysis of 1,886 roles /
  116 companies) — table-stakes vs differentiators vs specializations; evaluation as the
  senior/junior separator; declining skills; supplementary languages.
- llm-stats.com, *Post-Training in 2026: GRPO, DAPO, RLVR & Beyond*; Sundeep Teki, *Post-Training
  LLMs Guide: SFT, RLHF, DPO & GRPO (2026)*; arXiv:2501.12948 *DeepSeek-R1* — the GRPO/verifiable-
  reward shift informing M9.
- Model Context Protocol 2026 roadmap & enterprise-adoption guides — MCP as the de-facto
  agent-integration standard informing M12.
