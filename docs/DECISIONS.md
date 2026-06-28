# Decisions

> Dated log of pedagogical & technical choices (options considered + rationale).
> Newest entries first. Each entry: context, options considered, decision, rationale, consequences.

---

## D0003 — Final consistency pass: ₹0 boundary, compute buckets, front-matter field set
- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** A cross-doc consistency pass found three mismatches: (a) `Larnix-PLAN.md` said the
  ₹0 path covers "Modules 0–9" while `CLAUDE.md`, `STYLE_GUIDE.md`, and `ROADMAP.md` said "0–10";
  (b) `ROADMAP.md`'s module-map listed M4 as `browser→colab` and M8 as `colab + gpu(opt)`, which
  diverged from `CLAUDE.md`'s canonical compute buckets; (c) the chapter front-matter field set was
  enumerated as 8 fields in `CLAUDE.md`/`STYLE_GUIDE.md` but 10 in `CHAPTER_TEMPLATE.md`.
- **Decisions.**
  1. **₹0 boundary = Modules 0–10** (canonical). `CLAUDE.md` is the highest authority (per D0002);
     M10 (Generative AI) runs on free Colab, so the ₹0 promise legitimately extends to M10. Fixed
     PLAN's two "0–9" references to "0–10."
  2. **Compute buckets** are canonical as stated in `CLAUDE.md`: `browser` = M0–M4, free
     Colab/Kaggle = M5–M10, **rented `gpu` = M11 only**. Therefore M4's dominant tier is `browser`
     (heavier chapters like XGBoost offer a free Colab fallback) and M8 is `colab` (no rented GPU —
     "rented GPU only for M11" is firm). Fixed the ROADMAP module-map cells.
  3. **Front-matter field set = the 10 fields in `CHAPTER_TEMPLATE.md`**: `title, module, chapter,
     difficulty, prereqs, learning_objectives, compute, status, last_reviewed, est_minutes`. The
     template is the implementation truth; `CLAUDE.md` and `STYLE_GUIDE.md` were completed to match.
  4. **M1 prerequisite = none** (matches PLAN). M0 is orientation, not a knowledge gate.
- **Rationale.** One value per fact, owned by the authoritative doc (D0002); the others are aligned
  to it rather than left to drift.
- **Consequences.** Edited `Larnix-PLAN.md` (₹0 → 0–10), `ROADMAP.md` (M1 prereq, M4/M8 compute,
  dominant-tier note, journey wording), `CLAUDE.md` + `STYLE_GUIDE.md` (front-matter list), and the
  doc indexes (`docs/README.md` now lists RISKS.md + Larnix-PLAN.md; stale "Stage 0" wording
  removed from both READMEs). No change to PLAN's per-module chapter counts or curriculum structure.

---

## D0002 — ROADMAP is the executive spine; PLAN/RISKS/STYLE_GUIDE own their domains
- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** Multiple planning docs now exist (`ROADMAP.md`, `Larnix-PLAN.md`, `RISKS.md`,
  `STYLE_GUIDE.md`, `CHAPTER_TEMPLATE.md`, `CLAUDE.md`). Without a clear ownership rule they can
  drift and contradict each other (this surfaced as a chapter-count conflict — see D0001).
- **Options considered.**
  1. *One mega-doc* — fold everything into ROADMAP. Rejected: huge, unmaintainable, high drift.
  2. *No hierarchy* — let each doc restate everything. Rejected: guarantees contradictions.
  3. *Domain ownership with a single spine (chosen).* Each doc is authoritative for one domain;
     ROADMAP is the executive spine that references the others instead of duplicating them.
- **Decision.** Source-of-truth ownership is:
  | Domain | Source of truth |
  |--------|-----------------|
  | Mission, subsystems, working rules, Definition of Done | `CLAUDE.md` |
  | Curriculum — modules, chapter counts, prereqs, capstones, infra ladder, outcomes | `Larnix-PLAN.md` |
  | Risks — IDs, triggers, owners, mitigations, cadence | `RISKS.md` |
  | Pedagogy/format — Varsity contract, tiers, front-matter, compute/status fields | `STYLE_GUIDE.md` + `CHAPTER_TEMPLATE.md` |
  | Executive spine (phases, coverage map, outcome map, effort) | `ROADMAP.md` |
  `CLAUDE.md` principles override all. ROADMAP defers detail to the owning doc and links rather
  than restating.
- **Rationale.** Single-owner-per-domain prevents drift; the spine stays readable; updates have one
  obvious home.
- **Consequences.** `ROADMAP.md` carries a "reconciliation map" header declaring this split. When a
  fact lives in two docs, the non-owner must reference the owner, not re-state the value.

---

## D0001 — Canonical chapter count: PLAN's per-module estimate (~240+ full / ~180 stable-core)
- **Date:** 2026-06-28
- **Status:** Accepted
- **Context.** `RISKS.md` (R9) described the surface as "~180 chapters," while `Larnix-PLAN.md`'s
  per-module table sums to ~240+. This looked like two competing sources of truth for the same
  number.
- **Options considered.**
  1. *Trim PLAN's per-module counts down to ~180.* Rejected: the itemized per-module estimates are
     deliberate and pedagogically grounded; trimming to hit a round aside would be backwards.
  2. *Treat the figures as a scope distinction (chosen).* PLAN's ~240+ is the **full** build; ~180
     is the **stable-core** subset (math, classical ML, backprop, transformers — written to last),
     with the remainder being the smaller, version-pinned frontier surface.
- **Decision.** `Larnix-PLAN.md` is authoritative for chapter counts. Canonical figure:
  **~240+ chapters full, ~180 stable-core.** The "~180" in RISKS was a rounded aside, not a
  competing count.
- **Rationale.** Per D0002, curriculum counts are owned by PLAN. The full/stable-core split is real
  and useful (it ties directly to R1 currency: keep stable-core large, frontier surface small).
- **Consequences.** `RISKS.md` R9 updated (summary row + detail) to read "~240+ chapters; ~180
  stable-core" and to name PLAN as the curriculum source of truth. `ROADMAP.md` §2 states the same
  split. No change to PLAN's per-module numbers.
