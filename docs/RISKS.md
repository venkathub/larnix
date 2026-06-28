# Larnix — RISKS.md (living risk register)

> Every known caveat for Larnix, turned into a tracked risk with a **measurable trigger** that forces action. This is a living document: review it on the cadence in §5, update `Status` and `Last reviewed` as things change, and add new rows as they surface. It is the source for the risk register the master prompt asks Claude Code to produce in Stage 0.

---

## 1. How to use this register

- A risk is only managed when it has an **owner**, a **mitigation already in motion**, and a **trigger** — the specific, observable condition that means "act now." Triggers are written so they can be checked by a human in a review or, ideally, automated in CI.
- When a trigger fires, the risk is escalated: do the mitigation's "on trigger" action, log it, and reset `Last reviewed`.
- Likelihood/Impact use a simple **L / M / H** scale. **Exposure** = the combination you should worry about most; anything **H impact** is reviewed every cycle regardless of likelihood.
- `Owning phase` maps to the P0–P6 roadmap in `ROADMAP.md`. "Ongoing" means it never fully closes and lives in maintenance (P6+).

---

## 2. At-a-glance summary

| ID | Risk | Likelihood | Impact | Owning phase | Status |
|----|------|:----------:|:------:|--------------|--------|
| R1 | Frontier content goes stale | **H** | **H** | P0 (mechanism) → Ongoing | Open |
| R2 | Custom-LLM scope vs learner expectation | M | M | P4 (M11) | Open |
| R3 | In-browser compute limits break a lesson | M | M | P0 (mechanism) → per-phase | Open |
| R4 | Auto-grading open-ended work is unreliable | M | M | P0 (harness) → P6 (cert) | Open |
| R5 | "Job-ready" misread as guaranteed offer | M | **H** | P6 (M16) | Open |
| R6 | API spend forced on a learner | L | **H** | P0 (principle) → Ongoing | Open |
| R7 | Data-protection obligations (DPDP / GDPR) | M | **H** | P6 (accounts/cert) | Open |
| R8 | Certification proctoring burden & fairness | M | M | P6 (cert) | Deferred |
| R9 | Content-maintenance burden (~240+ chapters; ~180 stable-core) | **H** | **H** | All phases → Ongoing | Open |
| R10 | AI-drafted content contains errors | **H** | **H** | P0 (gates) → All | Open |
| R11 | Dataset / model licensing problems | M | **H** | P3–P4 (data lessons) | Open |
| R12 | Learner drop-off / low completion | **H** | M | P1 → Ongoing | Open |
| R13 | Free third-party tiers change (Colab/Kaggle/API) | M | M | Ongoing | Watch |
| R14 | Solo-maintainer bus factor | M | **H** | Ongoing | Watch |

---

## 3. Detailed entries

### R1 — Frontier content goes stale

- **Category:** Content currency. **Likelihood:** H · **Impact:** H.
- **Why it matters:** AI moves weekly; a wrong "latest model / current API" makes the whole platform look untrustworthy.
- **Mitigations (in motion):**
  - Enforce the `status: stable | frontier` and `last_reviewed` front-matter on every chapter (STYLE_GUIDE §7, §9).
  - Quarantine volatile specifics behind callouts + a thin abstraction (one `get_model()` helper) so a refresh touches few files.
  - Per-module owner; quarterly review sprint; "What changed in AI" changelog; community "report outdated content" issue template.
- **Trigger / threshold:** CI job `scripts/currency_check.py` **fails the build** when any `status: frontier` chapter has `last_reviewed` older than **90 days**, OR when the scheduled notebook-execution run breaks on a dependency. **On trigger:** assign the chapter to its owner, refresh, re-pin, reset date.
- **Owning phase:** P0 (build the check) → Ongoing. **Owner:** module owner / maintainer.

### R2 — Custom-LLM scope vs learner expectation

- **Category:** Expectation. **Likelihood:** M · **Impact:** M.
- **Why it matters:** "Build your own LLM" can be misread as "train a GPT-4." Disappointment if unmanaged.
- **Mitigations:**
  - M11's first chapter states the scope plainly: a *real but small* (~100M–1B) model to learn the **whole pipeline**; frontier scale is out of scope, with the cost math shown.
  - Teach code that scales by **config, not rewrite** (FSDP/DeepSpeed knobs) + a "scale-up appendix" estimating frontier cost.
  - Default capstone = continued-pretraining / domain-adaptation of a small base model (genuine "my model" feel, few hundred ₹); from-scratch is the stretch goal.
- **Trigger / threshold:** Learner feedback on M11 capstone shows a recurring "expected bigger / felt misled" theme (≥3 reports), OR the capstone's stated cost exceeds **₹500** on the default path. **On trigger:** sharpen the scope copy and/or swap the default to the cheaper path.
- **Owning phase:** P4 (M11). **Owner:** M11 author.

### R3 — In-browser compute limits break a lesson

- **Category:** Technical / accessibility. **Likelihood:** M · **Impact:** M.
- **Why it matters:** Pyodide has memory/package/GPU limits; a `browser` chapter that secretly needs PyTorch will fail for beginners.
- **Mitigations:**
  - The `compute: browser | colab | gpu` field routes each chapter; `browser` is restricted to Pyodide-safe work (pure Python, NumPy/Pandas/scikit-learn, small data).
  - CI lint **rejects a `browser` chapter that imports a non-Pyodide package**.
  - Every in-browser cell ships an "Open in Colab" fallback; test on a low-end phone, not just a dev machine.
- **Trigger / threshold:** CI lint flags a disallowed import in a `browser` chapter, OR a browser notebook exceeds the Pyodide memory ceiling in the execution run. **On trigger:** re-tag the chapter `colab` or split out the heavy part.
- **Owning phase:** P0 (build the lint) → checked every phase. **Owner:** platform/CI owner.

### R4 — Auto-grading open-ended work is unreliable

- **Category:** Assessment. **Likelihood:** M · **Impact:** M.
- **Why it matters:** Deterministic graders can't fairly score RAG quality, generated images, or a custom model's outputs.
- **Mitigations:**
  - Match grader to type: fill-in & implement-this-function → `assert` graders (fully auto); open-ended & capstones → **published rubrics**, not auto-grading.
  - Use measurable proxies where they exist (RAGAS-style metrics; exact-match on decomposed sub-tasks).
  - Certification gates on **rubric-reviewed capstones** (peer review + spot-checks); AI-as-a-judge is an *assist with stated limits*, never the sole gate.
  - Tell learners explicitly which exercises are auto-graded vs rubric-graded.
- **Trigger / threshold:** Any capstone is found to be gated **solely** by AI-as-a-judge, OR rubric inter-rater disagreement on certification reviews is high (spot-check audit). **On trigger:** add human review / refine the rubric.
- **Owning phase:** P0 (grader harness) → P6 (certification). **Owner:** assessment owner.

### R5 — "Job-ready" misread as guaranteed offer

- **Category:** Expectation / reputational / regulatory. **Likelihood:** M · **Impact:** H.
- **Why it matters:** Outcome over-promises mislead learners and invite regulatory/advertising-standards risk.
- **Mitigations:**
  - M16 and all marketing state plainly: Larnix builds the demonstrable skills + portfolio employers screen for; it cannot guarantee outcomes. No "get a job in N weeks" claims.
  - Maximize what's controllable: deployed portfolio projects, interview prep (coding / ML theory / system design), build-in-public coaching.
  - Optional voluntary outcome survey to measure honestly over time.
- **Trigger / threshold:** Any public copy contains a guaranteed-outcome or guaranteed-salary claim (copy review). **On trigger:** remove/reword before publish.
- **Owning phase:** P6 (M16 + launch copy). **Owner:** maintainer / whoever owns marketing copy.

### R6 — API spend forced on a learner

- **Category:** Accessibility / cost. **Likelihood:** L · **Impact:** H.
- **Why it matters:** The ₹0 promise is Larnix's signature; a mandatory paid key would break it and exclude the core audience.
- **Mitigations:**
  - Platform **never requires** a paid key to learn: every API example pairs with a free fallback (Ollama / Groq / Gemini free tier).
  - A "cost guardrails" lesson: hard spend limits, small models in dev, keys via env + `.env.example`, never committed.
- **Trigger / threshold:** Any chapter's required path (not an optional "going deeper" box) needs a paid key with **no** free fallback (CI/style review). **On trigger:** add the fallback or move the paid step to optional.
- **Owning phase:** P0 (principle) → Ongoing. **Owner:** style-guide enforcer / reviewer.

### R7 — Data-protection obligations (DPDP / GDPR)

- **Category:** Legal / privacy. **Likelihood:** M · **Impact:** H.
- **Why it matters:** Storing accounts, progress, or certificates makes Larnix a data controller under India's **DPDP Act, 2023** (and GDPR for EU learners). *Not legal advice — confirm specifics with counsel.*
- **Mitigations:**
  - **Defer collection:** ship the MVP accountless — progress in browser storage, no PII.
  - Add accounts only when certification needs them; then minimize data, add a privacy policy + consent, secure storage, and a deletion path.
- **Trigger / threshold:** A feature is proposed that stores any personal data (email, name, identity, proctoring footage). **On trigger:** STOP feature work, get a privacy review + counsel sign-off before building.
- **Owning phase:** P6 (accounts/cert). **Owner:** maintainer (with legal review).

### R8 — Certification proctoring burden & fairness

- **Category:** Operational / fairness. **Likelihood:** M · **Impact:** M.
- **Why it matters:** Proctoring adds cost, privacy exposure, and fairness/bias concerns (and intersects R7).
- **Mitigations:**
  - Start with **un-proctored completion certificates** (low stakes) + **project-based assessment** over high-stakes proctored MCQs.
  - Add proctoring only if the credential's market value demands it; if so, evaluate vendor privacy + accessibility/fairness first.
- **Trigger / threshold:** Demand to make the credential high-stakes/proctored is raised. **On trigger:** run a privacy + fairness + cost assessment before adopting.
- **Owning phase:** P6 (cert). **Status:** Deferred. **Owner:** maintainer.

### R9 — Content-maintenance burden (~240+ chapters; ~180 stable-core)

- **Category:** Sustainability. **Likelihood:** H · **Impact:** H.
- **Why it matters:** A large surface is the project's biggest *practical* risk — easy to start, hard to keep correct and current. Per-module estimates in `Larnix-PLAN.md` (the curriculum source of truth) sum to **~240+ chapters**, of which **~180 are stable-core** (math, classical ML, backprop, transformers — written to last) and the remainder are the smaller, version-pinned frontier surface (ties to R1). The two figures are a scope distinction, not two competing counts.
- **Mitigations:**
  - **Phase ruthlessly:** ship Foundations (P1) first, prove the model and the gates, then expand. Don't author all modules before the machinery is proven.
  - Keep **stable-core large, frontier-surface small** (ties to R1).
  - Treat **community contribution** as a first-class pipeline: CONTRIBUTING.md, PR templates, good-first-issue labels.
  - Reuse running examples per track so context isn't re-authored each chapter.
- **Trigger / threshold:** Open "needs update" issues exceed a backlog cap (e.g. **>20**), OR a full phase ships before its predecessor's gates are green. **On trigger:** pause new authoring; burn down maintenance.
- **Owning phase:** All → Ongoing. **Owner:** maintainer.

### R10 — AI-drafted content contains errors

- **Category:** Correctness. **Likelihood:** H · **Impact:** H.
- **Why it matters:** Claude Code drafts chapters; subtle technical errors can slip in and teach the wrong thing.
- **Mitigations:**
  - "**Every code block runs in CI**" — a wrong example fails the build (catches a large class of errors automatically).
  - SME/correctness-review checklist in the chapter Definition of Done (STYLE_GUIDE §11).
  - Style-guide rule: *if unsure a fact is current/correct, mark it `frontier` and flag it rather than guess.*
  - Prefer primary sources; never invent a citation.
- **Trigger / threshold:** A merged chapter is found with a factual/technical error in review or via learner report, OR a chapter merges without the correctness-review box checked. **On trigger:** fix, and add a regression check/example so the same class can't recur silently.
- **Owning phase:** P0 (gates) → All. **Owner:** reviewer / module owner.

### R11 — Dataset / model licensing problems

- **Category:** Legal / IP. **Likelihood:** M · **Impact:** H.
- **Why it matters:** Lessons use datasets and pretrained models with varied licenses; redistribution or training-data provenance issues create real exposure — especially in the M11 pretraining-data lesson.
- **Mitigations:**
  - Prefer permissively-licensed / public datasets and models.
  - Record each asset's **license** in the chapter front-matter or a `/docs/ASSETS.md` ledger.
  - Avoid assets with redistribution restrictions; teach data provenance explicitly in M11 as part of the curriculum.
- **Trigger / threshold:** A chapter introduces a dataset/model with an unverified or restrictive license (review of the asset ledger). **On trigger:** swap for a permissive alternative or document compliant usage before merge.
- **Owning phase:** P3–P4 (data-heavy lessons). **Owner:** data-lesson author.

### R12 — Learner drop-off / low completion

- **Category:** Pedagogical / product. **Likelihood:** H · **Impact:** M.
- **Why it matters:** Long curricula for broad audiences have high attrition; a course nobody finishes doesn't achieve the mission.
- **Mitigations:**
  - The whole pedagogy is built against this: short single-idea chapters, hooks first, runnable wins early, Key Takeaways, named learning tracks so beginners aren't shown advanced modules.
  - Front-load a fast, satisfying win (M0: run a model in 5 lines).
  - Optional privacy-respecting analytics on where learners stall, feeding chapter improvement.
- **Trigger / threshold:** Analytics show a chapter with an outsized drop-off vs its neighbours (once analytics exist). **On trigger:** review that chapter for difficulty spike / missing scaffolding.
- **Owning phase:** P1 → Ongoing. **Owner:** maintainer.

### R13 — Free third-party tiers change (Colab / Kaggle / API)

- **Category:** External dependency. **Likelihood:** M · **Impact:** M.
- **Why it matters:** The ₹0 path leans on free tiers we don't control; a terms/pricing change could break it.
- **Mitigations:**
  - Don't hard-couple to one provider: keep Colab **and** Kaggle as interchangeable GPU options; keep multiple free LLM fallbacks (Ollama local + Groq/Gemini).
  - Abstract provider-specific setup into one swappable setup chapter, not scattered everywhere.
- **Trigger / threshold:** A relied-on free tier removes/limits its offer (surfaced via the currency/notebook-execution runs or community report). **On trigger:** switch the default to the next free option; update the setup chapter.
- **Owning phase:** Ongoing. **Status:** Watch. **Owner:** maintainer.

### R14 — Solo-maintainer bus factor

- **Category:** Sustainability. **Likelihood:** M · **Impact:** H.
- **Why it matters:** A single maintainer is a single point of failure for a large, evolving platform.
- **Mitigations:**
  - Docs-as-code with everything in Git, plus rich `DECISIONS.md`, so context isn't only in one head.
  - Build the community-contribution pipeline early (R9) to grow co-maintainers.
  - Keep the build reproducible from a fresh clone (in the Definition of Done) so a new contributor can onboard fast.
- **Trigger / threshold:** Maintenance backlog persists because no second contributor exists after Foundations ships. **On trigger:** prioritize contributor onboarding / recruit co-maintainers.
- **Owning phase:** Ongoing. **Status:** Watch. **Owner:** maintainer.

---

## 4. Risks that are explicitly accepted (for now)

- **Small-scale-only custom LLM (R2):** accepted by design on cost grounds; mitigated by honest scoping, not by buying frontier compute.
- **Proctoring deferred (R8):** accepted that early certificates are completion-style and un-proctored; revisit only if the credential needs to be high-stakes.

---

## 5. Review cadence

- **Every PR:** the automated triggers (R1 currency check, R3 import lint, R6 free-fallback check, R10 runs-in-CI) gate the merge.
- **Monthly:** skim this register; update `Status` and `Last reviewed`; clear any fired triggers.
- **Quarterly:** full review — re-score likelihood/impact, refresh all `frontier` content, burn down the maintenance backlog (R9), reassess deferred/accepted risks.
- **On every new phase (Stage 1 grooming):** add any phase-specific risks the spec surfaces.

*Last reviewed: <YYYY-MM-DD> · Maintainer: <name>*
