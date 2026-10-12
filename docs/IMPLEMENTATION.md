# Larnix implementation

## Current milestone: local platform and three representative lessons

Implemented on the rebuild branch. Main remains the empty baseline. The reference repository has not been forked or imported.

- Catalogue of all 42 modules and 168 lesson plans, in the approved prerequisite order.
- Search across titles, topics and outcomes; Interview and Production views additionally search their respective question/exercise fields.
- Combined topic-group, availability and bookmark filters, URL-preserved filter state, explicit no-result states.
- Module pages, lesson blueprints, direct prerequisite links, primary readings and next-lesson navigation.
- Three integrated interactive previews: vector similarity (M03-L01), RAG evidence flow (M17-L01), and agent crash recovery (M21-L02).
- Shared quiz/theme component plus course navigation, bookmarks and independent reading/check/practice records.
- Local progress restores after reload; storage-disabled environments fall back to page memory. Reading and exercise flags are self-reported, not assessment results. Check correctness is derived from the latest saved answer; it is not a credential or tamper-proof grade.
- Dark/light themes, responsive catalogue and lesson layouts, semantic controls and keyboard access.

This milestone does not implement account synchronization, backend APIs, a release/assessment system, or 165 additional narrative lessons. Those lessons are shown as plans. A blueprint can be bookmarked but cannot be marked as an authored lesson completed through the catalogue.

## Run and check

```sh
python3 scripts/build_site.py
python3 -m http.server 8775 --bind 127.0.0.1 --directory dist
```

Visit `http://127.0.0.1:8775/`. This is a static build with no runtime package dependencies. Rebuild and reload after edits. `dist/` is generated and ignored by Git. Serve the entire directory so lesson assets and downloads resolve.

With Node.js on PATH, `make check` runs the curriculum validation, platform tests, lesson arithmetic/evidence/recovery tests, syntax checks and generated-route checks. Override `NODE=/absolute/path/to/node` if needed. `make build` builds; `make serve` builds and serves on port 8775.

Progress uses the `larnix.progress.v1` local-storage key. Storage is isolated by origin: switching port or domain starts a separate local record. The UI has a two-step reset. No analytics, tracking requests, external fonts or model calls are used. External source links open only when selected.

## Source map

| Location | Responsibility |
| --- | --- |
| `docs/curriculum/curriculum.json` | Approved lesson plans, prerequisites, order and interview/production content |
| `docs/curriculum/sources.json` | Primary reading registry |
| `web/lessons.json` | Implemented preview manifest and check-answer keys for the progress view |
| `web/index.html`, `web/app.js`, `web/app.css` | Catalogue, plan pages, progress screen and responsive layout |
| `web/catalog.js` | Search/filter and check-summary rules |
| `web/progress.js` | Versioned browser state, sanitization and memory fallback |
| `web/lesson-shell.js` | Course navigation and self-reported progress controls in authored lessons |
| `samples/shared/lesson-ui.js` | Shared explanation checks, feedback, retry and theme behavior |
| `samples/vector-similarity/`, `samples/rag-grounding/`, `samples/agent-recovery/` | Original lesson prose, labs and learner artifacts |
| `scripts/build_site.py` | Generates platform data, copies assets and integrates authored lessons |
| `tests/` | Platform logic, persistence and generated asset/navigation checks |

The three authored lesson pages retain their specialist lab engines. Shared components handle repeatable teaching UI. The current base lesson stylesheet comes from the vector sample and is emitted once as `assets/lesson.css`; the RAG and recovery labs add their own layout rules. This keeps the approved visual treatment without adding a framework solely for the prototype.

The curriculum status is a planning baseline. Preview availability comes from a separate manifest, so an implemented prototype cannot accidentally turn all planned lessons into completed chapters.

## Add the next authored lesson

1. Follow the existing lesson ID, prerequisite and source plan. Research relevant primary sources again before authoring.
2. Write original narrative, worked example, checks, failure investigation, interview guide and practice artifacts under `samples/<slug>/`.
3. Initialize the shared LessonUI with a stable lesson ID and quiz keys. Keep lab computation in a separate testable file. Identify synthetic or replayed behavior.
4. Add the manifest entry in `web/lessons.json`, including the matching answer keys. Add the appropriate test command to `make check`.
5. Build; verify links, artifacts and the lesson in the browser. Check storage restoration, keyboard controls, narrow-screen layout and explanatory accuracy.
6. Keep the lesson labeled as an interactive preview until its content and acceptance evidence have been reviewed for release.

## Remaining implementation sequence

1. Refine the shared lesson components using the three prototypes, including accessibility and learner review.
2. Author M01–M06 in reviewed module batches, with full narrative, meaningful interactions and exercise evidence.
3. Expand retrieval, agents, evaluation/security, operations and advanced branches in curriculum order.
4. Decide on accounts, cross-device progress, search indexing and publication requirements when their use cases are concrete.

Verification is a local functional/browser review, not a full accessibility audit, learner study or production deployment.
