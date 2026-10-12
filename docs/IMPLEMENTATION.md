# Larnix implementation

## Current milestone: M01–M06 foundations and two advanced previews

Implemented through the rebuild branch and published from `main`. The reference repository has not been forked or imported.

- Catalogue of all 42 modules and 168 lesson plans, in the approved prerequisite order. The local catalogue draft uses seven handwritten roadmap stages, six modules per stage and one expanded module at a time.
- The root URL opens a handwritten welcome page with the first lesson, a returning learner's resume link, a revealable teaching example, and the ten-minute study sequence. Home and Curriculum are distinct destinations; `#/catalog` retains its existing filters and deep links. Lesson logos return home while the explicit Curriculum links return to the roadmap.
- Search across titles, topics and outcomes; Interview and Production views additionally search their respective question/exercise fields.
- Ctrl/⌘ K opens Search & commands; arrow keys move through results, Enter opens a lesson, and Escape closes the palette. A visible button supports touch and mouse. Topic, availability, bookmark and Learn/Interview/Production controls live in the palette. Stage and filter state survive reload through the URL; active filters and no-result states remain visible.
- The separate preview showcase is removed in the catalogue draft. Available lessons open directly from their modules; planned lessons open their blueprints. On mobile the roadmap starts collapsed and closes after a stage is selected.
- Module pages, lesson blueprints, direct prerequisite links, primary readings and next-lesson navigation.
- Twenty-six authored previews: all 24 foundation lessons M01–M06, plus RAG evidence flow (M17-L01) and agent crash recovery (M21-L02). The existing vector lab remains M03-L01.
- Each preview has a suggested 10-minute core, original handwritten-style SVG, three checks, and optional deeper explanation/interview/production sections. Direct links reveal optional content automatically.
- Shared quiz/theme component plus course navigation, bookmarks and independent reading/check/practice records.
- Local progress restores after reload; storage-disabled environments fall back to page memory. Reading and exercise flags are self-reported, not assessment results. Check correctness is derived from the latest saved answer; it is not a credential or tamper-proof grade.
- Dark/light themes, responsive catalogue and lesson layouts, semantic controls and keyboard access.

This milestone does not implement account synchronization, backend APIs, a release/assessment system, or the remaining 142 narrative lessons. Those lessons are shown as plans. A blueprint can be bookmarked but cannot be marked as an authored lesson completed through the catalogue.

## Run and check

```sh
python3 scripts/build_site.py
python3 -m http.server 8775 --bind 127.0.0.1 --directory dist
```

Visit `http://127.0.0.1:8775/`. This is a static build with no runtime package dependencies. Rebuild and reload after edits. `dist/` is generated and ignored by Git. Serve the entire directory so lesson assets and downloads resolve.

With Node.js on PATH, `make check` runs the curriculum validation, platform tests, lesson arithmetic/evidence/recovery tests, syntax checks and generated-route checks. Override `NODE=/absolute/path/to/node` if needed. `make build` builds; `make serve` builds and serves on port 8775.

Progress uses the `larnix.progress.v1` local-storage key. Storage is isolated by origin: switching port or domain starts a separate local record. The UI has a two-step reset. No analytics, tracking requests, external font requests or model calls are used. External source links open only when selected.

## Publishing

The classroom is published at https://venkathub.github.io/larnix/. GitHub Pages uses the GitHub Actions publishing source. `.github/workflows/publish.yml` validates and builds `dist/` on every push to `main`, then deploys it through the official Pages artifact actions. It can also be run manually on `main`. All site navigation and assets resolve relative to the project path; direct lesson URLs work without a rewrite service. `deployment.json` identifies the exact deployed source commit.

Branch protections remain in place. `.github/workflows/checks.yml` preserves the four required check names while adapting their implementation to the rebuilt static platform: schema/unit tests and basic static accessibility checks; executable JavaScript lesson engines plus any authored notebooks; spelling, curriculum consistency and internal links; and a downloadable preview artifact. The legacy `Notebook execution (R10)` name remains for compatibility: there are currently no authored `.ipynb` files, and incomplete learner Python starters are intentionally not executed as finished labs. The preview check uploads a review artifact rather than writing a public PR preview into production. Existing backup branches and the historical `gh-pages` branch are retained.

## Source map

| Location | Responsibility |
| --- | --- |
| `docs/curriculum/curriculum.json` | Approved lesson plans, prerequisites, order and interview/production content |
| `docs/curriculum/sources.json` | Primary reading registry |
| `web/lessons.json` | Implemented preview manifest and check-answer keys for the progress view |
| `web/index.html`, `web/app.js`, `web/app.css`, `web/roadmap.css` | Compact roadmap catalogue, keyboard command palette, plan pages and progress screen |
| `web/catalog.js` | Search/filter and check-summary rules |
| `web/progress.js` | Versioned browser state, sanitization and memory fallback |
| `web/lesson-shell.js` | Course navigation and self-reported progress controls in authored lessons |
| `samples/shared/lesson-ui.js` | Shared explanation checks, feedback, retry, theme and disclosure deep links |
| `samples/shared/quick-lesson.css`, `samples/shared/fonts/` | Short learning path, sketch diagrams and locally served OFL-licensed Caveat font |
| `samples/vector-similarity/`, `samples/rag-grounding/`, `samples/agent-recovery/` | Original lesson prose, labs and learner artifacts |
| `scripts/build_site.py`, `scripts/render_foundations.py` | Generates platform data and static lesson HTML; validates foundation topic coverage and fixtures |
| `samples/foundations/` | Original M01–M06 notes, case explorer and tested local math experiments |
| `tests/` | Platform logic, persistence and generated asset/navigation checks |

The three authored lesson pages retain their specialist lab engines. Shared components handle repeatable teaching UI. The current base lesson stylesheet comes from the vector sample and is emitted once as `assets/lesson.css`; the RAG and recovery labs add their own layout rules. This keeps the approved visual treatment without adding a framework solely for the prototype.

The roadmap stages are consecutive groups of six modules from `recommended_module_order`, not replacements for the seven topic groups or the prerequisite graph. Evaluation and security stay before language-model work.

The curriculum status is a planning baseline. Preview availability comes from a separate manifest, so an implemented prototype cannot accidentally turn all planned lessons into completed chapters.

## Add the next authored lesson

1. Follow the existing lesson ID, prerequisite and source plan. Research relevant primary sources again before authoring.
2. Write original narrative, worked example, checks, failure investigation, interview guide and practice artifacts under `samples/<slug>/`.
3. Put the learner’s question before lab controls, define unfamiliar terms at first use, and show state-derived evidence beside each result. Include concealed-answer transfer cases that test a new value or context and a limitation of the concept. Keep advanced controls optional.
4. Initialize the shared LessonUI with a stable lesson ID and quiz keys. Keep lab computation in a separate testable file. Identify synthetic or replayed behavior.
5. Add the manifest entry in `web/lessons.json`, including the matching answer keys. Add the appropriate test command to `make check`.
6. Build; verify links, artifacts and the lesson in the browser. Check storage restoration, keyboard controls, narrow-screen layout and explanatory accuracy.
7. Keep the lesson labeled as an interactive preview until its content and acceptance evidence have been reviewed for release.

## Remaining implementation sequence

1. Validate the foundation lessons with first-time learners, including accessibility, transfer and the ten-minute core pace.
2. Review learner-produced exercise evidence; the authored practice instructions are not completed production implementations.
3. Expand retrieval, agents, evaluation/security, operations and advanced branches in curriculum order.
4. Decide on accounts, cross-device progress and search indexing when their use cases are concrete.

Functional/browser checks and automated publishing do not constitute a full accessibility audit or a learner study.

## Notebook theme and UX research — October 12, 2026

The platform, module and lesson plans, progress page, and all three authored samples use `samples/shared/notebook.css`. The build emits this shared sheet after the existing layout styles. Warm paper is the default for new visitors; saved light/dark preferences remain intact. The dark palette uses a green notebook surface with cream ink.

Patrick Hand is served locally for upright handwritten explanations and UI text; Caveat is used for flowing headings and diagram annotations. Reading prose uses 22 px type with 1.5 line height; revision notes use 21 px with 1.35 line height. Code and exact numeric controls retain monospace. Paper dots, marginal rules, tape accents and irregular borders establish the handwritten notes theme without adding images or a framework. Current navigation also uses `aria-current`.

Research-informed decisions:

- [NN/g: Legibility, Readability, and Comprehension](https://www.nngroup.com/articles/legibility-readability-comprehension/) — distinguish visual character from readable content. Keep prose at a comfortable measure. The user requested handwriting throughout; use larger handwriting for prose and reserve monospace for code and exact numeric controls.
- [NN/g: The Role of Animation and Motion in UX](https://www.nngroup.com/articles/animation-purpose-ux/) — use brief motion to explain changes. Panels reveal in 180 ms, page introductions in 240 ms, and original sketches draw once in 650 ms. No looping decorative animation or scroll hijacking.
- [W3C: CSS reduced-motion technique](https://www.w3.org/WAI/WCAG22/Techniques/css/C39) — motion is opt-in through `prefers-reduced-motion: no-preference`; the sketch observer is skipped when reduced motion is requested. Content remains visible without animation or the observer.
- [W3C: Contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) — use at least 4.5:1 for normal text. Primary, muted and accent text tokens are checked against the three paper surfaces in both palettes.

`samples/shared/notebook.js` observes only original explanatory sketches, unobserves each after its first reveal, and never drives the lab calculations or progress state. New lessons should include both shared notebook assets. Existing keyboard search, module accordions and native controls remain available.

### Student revision treatment

All three authored lessons now open with a compact revision sheet: core idea, original concept diagram, worked example, exam trap, and active recall with a native revealable answer. The `#revision` anchor remains valid. The diagram is moved into the recap, preserving its accessible title and description without duplicating IDs. The full story and lab remain below, with two direct action links. Progress controls and the suggested study route are collapsed by default; revision answers do not mark progress. Prose, supporting captions, status labels, search, references, and exercise text now share the handwritten typeface instead of retaining the earlier sans-serif body.

Patrick Hand font provenance: [Google Fonts metadata](https://github.com/google/fonts/blob/main/ofl/patrickhand/METADATA.pb) and [designer handwriting description](https://github.com/google/fonts/blob/main/ofl/patrickhand/DESCRIPTION.en_us.html). The TTF and SIL OFL license are bundled under `samples/shared/fonts/`; no third-party font request is needed at runtime.

### Learner review follow-through

The next review pass addresses the observed learning friction rather than assigning a perfect score:

- All three samples name the technical concept up front and define the terms needed to interpret the opening notes.
- Each revision sheet uses a new-domain or new-value application question with a concealed explanation. These ungraded prompts do not change saved quiz scores.
- RAG exposes three guided scenarios. Advanced scenarios and state editing are in a native disclosure. Its nearby live result distinguishes missing retrieval, dropped context, stale evidence, conflicting evidence and absent source facts.
- Vector ranking feedback appears immediately after metric controls. The existing live announcement remains the keyboard/commit announcement so pointer moves do not add a second live region.
- Recovery exposes three guided scenarios, moves advanced crash settings into a disclosure, and puts the outcome immediately after step controls. Scenario selection is exposed with `aria-pressed`.
- “Checks correct” replaces “checks understood”; completing a quiz does not certify mastery. The RAG abstention behavior is explicitly identified as the teaching lab’s policy.
- Generated HTML versions JS/CSS URLs using content hashes to prevent a cached runtime from drifting from new markup. Link validation still resolves query-free file paths.

Before calling this a validated 10/10 learning experience, test with actual learners: ask a new learner to explain the concept in their own words, predict an unseen case before revealing its answer, and identify the first failing boundary in the lab. Observe whether they can do this within the proposed ten-minute core without guidance. Record misconceptions and navigation stalls; self-review and passing software tests alone cannot establish this outcome.


### Round 3 beginner walkthrough — October 12, 2026

Scope: M17-L01 RAG. This was an informed reviewer walkthrough, not a blinded beginner trial: the reviewer already knew the authored answers. No ten-minute comprehension or retention result is claimed.

Findings and repairs:

- The customer question previously followed the controls and result. It now precedes the guided scenarios, so direct lab entry has enough context to make a prediction.
- Learners could read that evidence was dropped without seeing the boundary. A compact, state-derived “Found → Sent to model” trace now sits beside the outcome. Tight context shows R1 + R2 + F1 → R2; retrieval miss shows R1 + R2 → R2.
- The transfer question used “context window” without an immediate explanation. It now explains the term as room for model input.
- The existing transfer case only exercised retrieval failure. A second concealed-answer case asks about correct evidence followed by an invented repair promise, testing the distinction between retrieval and generation.
- Generic missing-evidence feedback overclaimed that a fact was absent from all sources. It now directs the learner to compare the three boundaries instead of assuming that cause.

Browser evidence: exercised all six RAG scenarios; answered the three concept checks correctly; deliberately selected a wrong context answer and verified corrective feedback. Restored the original unanswered quiz state. Verified both transfer explanations and closed their disclosures. At 390 × 844 the question, guided controls, trace and tight-context feedback remain readable with no horizontal overflow. The regular reading pane also keeps the tight-context feedback beside its controls. The handwritten font pairing is unchanged. Repository checks pass for the curriculum, four JavaScript test files, syntax checks and two build/link tests.

Reviewer conclusion: the core now teaches a useful diagnostic distinction and provides visible evidence for it. The remaining acceptance gap is learner validation, not another visual redesign. Ask first-time learners to attempt both transfer cases without revealing answers, explain their diagnosis aloud, and record time and hesitation before describing the lesson as a proven ten-minute learning experience.


### Beginner improvements across every preview — October 12, 2026

All three entries in the preview manifest now use the same question-first, evidence-beside-result approach. This extends the RAG review; it does not label any of the 165 planned lessons as authored.

- **Vectors:** removed the winner from the prediction instructions, moved normalization beside metric selection, and added live raw coordinates and both scores next to the explanation. Normalization is defined where the first transfer question uses it. A second transfer case separates cosine alignment from factual correctness and freshness.
- **Recovery:** introduced the authorized task and explained reconciliation before controls. The result now compares saved agent evidence with provider refund count and amount, explicitly marked as an observer view. Replay controls sit in the optional settings disclosure. A second transfer case tests matching the amount as well as the operation ID; deduplication is explained in plain language in the first case.
- **RAG:** retained the reviewed question-first flow, found-versus-sent trace, and both transfer cases. Rechecked retrieval miss versus dropped context after the shared style changes.

Walkthrough evidence: vector dot, cosine and normalized-dot comparisons; opposite and zero-vector cases; recovery blind retry, reconciliation, unavailable lookup, changed amount and pre-dispatch replay; all six graded checks in the two updated previews, including deliberate wrong answers and corrective feedback. Both lessons began with no selected quiz answers and were restored to that state. Mobile checks used 390 × 844 with no horizontal overflow. The feedback and controls remain adjacent; the existing diagrams and handwritten fonts are preserved.

Honest review: vectors gives the most concrete entry point, although interpreting coordinates still needs basic math. RAG clearly distinguishes where evidence disappears, but its fixed ranking and mock generator do not demonstrate real retrieval quality. Recovery remains the most demanding preview because it requires reasoning about separate records and uncertainty; it is appropriate after the listed agent/state prerequisite, not as a first programming lesson. All three need first-time learner trials to validate transfer and the proposed ten-minute pace. Reviewer familiarity with the answers prevents calling these blind assessment results.


## Foundation delivery — M01–M06

All 24 foundation lessons now open as authored previews. Twenty-three use original notes in `samples/foundations/m01-m03.json` and `m04-m06.json`; M03-L01 retains its existing vector engine and narrative. The first six modules account for 24 of the 26 available previews; 142 lessons remain plans. Availability is still derived from the preview manifest, not by rewriting the approved planning baseline.

Each new lesson includes definitions, a handwritten mechanism sketch, a worked example, a misconception, three original illustrated cases with adjacent feedback and numerical evidence, three checks, two concealed-answer transfer prompts, every approved topic as an expanded note, verified primary sources, and a downloadable practice starter with acceptance criteria. The ten-minute route introduces one central mechanism; broader notes and production practice require additional time.

The case explorer switches between fixed synthetic fixtures and labels that limitation explicitly before the controls and below the visual. It does not pretend to run Python, train a model, call an API or measure production results. M03-L02 and M05-L02 additionally provide a computed quadratic-loss chart and step controls; M04-L03 provides a computed threshold slider with six per-ticket decisions, confusion counts, precision and recall. Undefined precision at zero alerts is preserved.

The build rejects missing topic coverage, malformed checks, incomplete cases and inconsistent chart scales. Tests independently calculate threshold counts, baseline mistakes, scalar gradient updates and shared-filter outputs; the page checks enforce 24-lesson foundation availability and match saved quiz keys to authored answers. Previous/next navigation opens authored lessons directly and stays visible after completion checks.

Authoring sources were rechecked against primary documentation, including Python, RFC 9110, PostgreSQL, D2L, SciPy, scikit-learn, PyTorch 2.9, Google ML framing, Microsoft HAX, Feast and Hugging Face. Individual lessons link the exact relevant pages. The reference GitHub project was not forked or imported. Coding starters are exercises for learners to develop and verify; they are not a claim that all described services or pipelines have been built.

Foundation acceptance evidence: browser-tested all 69 case selections across the 23 new pages at 390 × 844; each produced a distinct expected state and no horizontal overflow. Opened topic notes and practice starters in a representative lesson from each module. Verified correct checks, wrong-answer explanation, persistence after reload and reset in six representative lessons, restoring their initially unanswered state. Tested the threshold slider by keyboard at no-alert and .7 cutoffs; verified local gradient-step values. The desktop revision sheet, restored light/dark preference, direct next-lesson link and catalogue counts (24 foundation lessons / 26 total previews) were checked. No browser console errors were observed.

This is implementation and informed content review, not an independent learner trial or a comprehensive accessibility audit. The dense mathematics and systems modules still require the stated prerequisites; ten-minute comprehension and later retention remain to be validated with first-time learners.
