# Larnix — visual and interactive teaching direction

Status: adopted design requirement for subsequent lesson and application implementation. Applies to all 42 modules and 188 lessons in the [curriculum](INDEX.md). There are 29 authored previews and a separate runnable data-programming artifact; no lesson is certified against the full completion contract. See DELIVERY.md for the current inventory. The narrative standard below also applies when revising the existing sample.

## Reference and interpretation

The user selected [linearalgebra.info](https://linearalgebra.info/) as the explanation and design reference. The homepage and [first public lesson](https://linearalgebra.info/unit-01.html) were inspected on 2026-10-11, including their rendered appearance. The observed pattern combines a dark visual canvas, large editorial headings, focused prose, embedded controls, worked numbers, comprehension checks and expandable derivations. Course navigation shows connections between units.

For Larnix, the central requirement is that a learner can manipulate a concept and explain the resulting change. The following layout, interaction proposals and acceptance criteria are Larnix design decisions. Use original wording, illustrations, examples, code and branding. Do not import the reference site's assets, lesson content or source implementation. Its pricing and account model are not requirements for Larnix.

## Narrative explanation standard for every lesson

The user additionally selected Zerodha Varsity as the explanation reference. Its [Technical Analysis introduction](https://zerodha.com/varsity/chapter/background/) was reviewed on 2026-10-11. It connects to prior learning, develops a familiar analogy, maps that analogy to a technical concept, discusses limitations and closes with key takeaways. Larnix adopts these broad teaching principles alongside the interactive direction from linearalgebra.info. All prose, scenarios, diagrams and exercises must be original.

Apply the following editorial requirements to every authored lesson, including advanced modules:

- Begin with a concrete situation and explain why the learner needs this concept. Briefly reconnect to the stated prerequisites.
- Use patient, conversational prose with explicit transitions. Introduce one idea at a time and define new terminology before relying on it. The main explanation must remain understandable without operating a widget.
- Use a familiar analogy where it helps, then explicitly map it to the mechanism and explain where it stops being accurate. A concrete engineering example can serve this purpose when an analogy would mislead.
- Carry one original example through the explanation, worked calculation or execution trace, interactive exploration and failure analysis. Introduce equations after their meaning; name every symbol and show intermediate steps. Introduce code after explaining its inputs, expected behavior and purpose.
- Address the questions a learner is likely to ask, such as why a simpler approach fails and when the method is appropriate. Explain assumptions, counterexamples and tradeoffs without hiding essential caveats in optional sections.
- Finish the main narrative with three to five specific takeaways, a short glossary of newly introduced terms and a bridge to the next lesson. Keep the existing understanding checks, sources, interview reasoning and production exercise.
- Preserve depth through clearly signposted derivations and implementation detail. Advanced lessons may rely on linked prerequisites; they should still explain each new reasoning step. Design the core concept for about 10 minutes; move extended derivations and production work into optional sections. Split a broad concept across the planned lesson sequence rather than growing the core indefinitely.

Before publication, review whether a learner with the stated prerequisites can explain why the mechanism works, reproduce the worked example and recognize a failure case. A prose outline or a collection of bullets does not satisfy the authored explanation requirement. The 188 existing lesson plans are authoring blueprints, not completed narrative chapters.

The vector-similarity sample has been revised against this standard with a continuous rental-help-desk story, explicit prerequisites, worked normalization, common questions, takeaways and glossary. Use it as the first reviewable example of the narrative format; further prototypes must still validate the approach for evidence flow and agent recovery.

## Ten-minute core and handwritten diagrams

The latest approved direction is a short visual core for every lesson. All three previews implement this format: 2 minutes for the situation and sketch, 4 minutes for three deliberate lab changes, 3 minutes for explanation and checks, and 1 minute for recall. These are pacing targets, not a guarantee of understanding or a timer-based completion rule.

- Use an original handwritten-style SVG wherever a diagram makes the mechanism clearer. Keep labels readable, provide a title and text alternative, and adapt to narrow screens and both themes.
- Prefer a short story, one visual mechanism and a compact worked comparison to repeated paragraphs. Define unfamiliar terms inline. Essential limitations stay visible.
- Keep prediction and transfer checks in the core route. Preserve full worked details, failure discussions, glossary, interview preparation and production tasks as optional disclosures.
- Deep links must open their containing disclosure, including citations and the Interview/Production views. Diagrams and core explanations remain available without JavaScript.
- The shared local Caveat font supplies handwritten labels; irregular SVG strokes supply the sketch treatment. This adds no external font requests. See `samples/shared/fonts/OFL.txt` for the font license.

## Teaching sequence for every lesson

| Step | What the learner encounters | Authoring requirement |
| --- | --- | --- |
| 1. Encounter the problem | A short, concrete situation and a question worth answering | Explain the need before introducing terminology; reuse the lesson's original scenario |
| 2. Make a prediction | A small choice or estimate before revealing the result | Target a plausible misconception; record the prediction locally |
| 3. Change something | An interactive diagram, simulator, trace or decision exercise | Name the control and the expected observation; start with a useful default |
| 4. Explain the change | Plain-language mechanism linked to the visible state | Connect the learner's action to the output; define unfamiliar terms at first use |
| 5. Work through the details | A small numerical example, trace or step-by-step procedure | Keep inputs consistent with the visual; show intermediate values and units |
| 6. Check understanding | A new example with feedback explaining the reasoning | Include at least two checks per lesson: one prediction and one transfer or diagnosis check |
| 7. Inspect a failure | A misleading result, edge case or resource failure | Expose the symptom, cause, boundary and recovery; include reset/replay |
| 8. Apply and defend | The planned production exercise and interview question | Connect the visual intuition to executable evidence, engineering tradeoffs and limitations |

Use one primary interactive explanation per lesson as the minimum design target. Add more only when they teach a distinct mechanism. A decision exercise, trace replay or adjustable table is suitable for governance and product topics; do not force geometry or animation into every subject. A static equivalent must communicate the same concept when interaction is unavailable.

## Reading and navigation layout

The course overview should present seven navigable topic groups, a prerequisite route, learner progress and a useful next lesson. Each module should explain what its lessons unlock. Keep the complete 42-module catalogue accessible through search and a compact index.

A lesson page should provide a compact persistent header, module/lesson position, contents navigation, progress, theme control and search. The opening area introduces the problem with a relevant visual. The body alternates focused prose with wider interactive panels. Finish with practice, interview reasoning, production guidance and links to prerequisite and follow-on lessons.

Provide **Learn**, **Interview** and **Production** entry points into the same authored lesson. Learn follows the narrative; Interview opens the question and answer rubric; Production opens decision criteria, failure symptoms, metrics and recovery. These should deep-link to shared content rather than create three inconsistent copies.

## Visual direction

- Use a deep navy or charcoal background with restrained teal, blue and warm accent colors. Offer a light theme with the same information hierarchy.
- Use expressive, large headings and comfortable reading typography. Keep prose around 60–75 characters per line; reserve monospace for code, measurements and execution traces.
- Place controls next to the values they affect. Keep inputs, intermediate state and outputs visible together where space allows.
- Use semantic colors consistently for selected input, active computation, evidence and failure. Pair colors with labels or shapes.
- Make diagrams and panels serve the explanation. Use 2D SVG for most relationships; introduce 3D only where spatial interaction improves understanding.
- Reveal derivations and advanced details progressively. Essential explanations, assumptions and failure warnings must remain visible without opening optional sections.
- Show animation only for meaningful state transitions. Include pause, step, reset and reduced-motion behavior. Avoid requiring animation to read a result.
- On narrow screens, stack prose, visualization and controls in causal order; offer numeric inputs or buttons as alternatives to dragging.

Final fonts, exact colors and spacing tokens will be selected in the prototype. The direction is an original Larnix design informed by the reference, rather than a pixel-for-pixel reproduction.

## Interaction plan across all 42 modules

These are representative starting interactions for each module. The remaining lessons must receive their own interaction specifications during full authoring. This table does not claim 188 individual widgets are already designed or built.

| Module | Representative interaction | Learner changes | Observable explanation |
| --- | --- | --- | --- |
| M01 · Product engineering | Pilot decision worksheet | Task volume, error cost, review rate | Which solution meets the stated business constraints and why |
| M02 · Software engineering | Request-lifecycle simulator | Concurrent requests, deadline, cancellation | Queue slots, active tasks, released resources and persisted outcomes |
| M03 · Mathematics | Vector comparison canvas | Direction, length, normalization | Dot product, cosine similarity and ranking differences |
| M04 · ML fundamentals | Classification threshold workbench | Threshold, prevalence, review capacity | Confusion counts, precision/recall and operational workload |
| M05 · Deep learning | Tiny network stepper | Weight, input, learning rate | Activations, loss, gradients and the next weight update |
| M06 · Data engineering | Dataset lineage inspector | Schema version, late event, deleted record | Which derived artifacts become invalid and need rebuilding |
| M07 · Transformers | Attention computation inspector | Tokens, mask, query/key values | Scores, normalized weights and the weighted value output |
| M08 · Training lifecycle | Checkpoint timeline | Interruption point and saved state | What can resume and what must be recomputed |
| M09 · Model APIs | Stream event player | Truncation, timeout, malformed event | Why partial output differs from a completed validated result |
| M10 · Prompt engineering | Controlled prompt comparison | One instruction or example | Differences on a fixed evaluation set; identify recorded versus live results |
| M11 · Structured outputs | Schema and evidence inspector | Missing field, contradiction, unsupported claim | Syntax, domain validation and evidence support as separate checks |
| M12 · Context engineering | Context budget composer | History, tool definitions, evidence and reserve | What fits, what is omitted and which constraints are lost |
| M13 · Ingestion | Document/chunk split view | Boundary, overlap, table handling | Evidence continuity and provenance across source and chunks |
| M14 · Embeddings | Similarity explorer | Query vector, metric, normalization | Neighbors and scores; show the limits of a toy 2D space |
| M15 · Vector indexes | Approximate search replay | Candidate budget, filter selectivity | Missed exact neighbors, recall and recorded search cost |
| M16 · Retrieval | Candidate-to-ranking workbench | Lexical/dense candidates, fusion, reranking | Which documents can be recovered and the candidate-recall ceiling |
| M17 · RAG | Evidence pipeline explorer | Question, retrieved chunks, stale source | Evidence reaching the answer, citation support and abstention |
| M18 · Knowledge systems | Versioned relation explorer | Entity link, effective date, source authority | Which paths support an answer and where sources conflict |
| M19 · Workflows and agents | Side-by-side execution paths | Task ambiguity, failure, allowed choices | Fixed branches versus adaptive actions and their costs |
| M20 · Tools | Tool-call contract inspector | Principal, arguments, request key | Validation, authorization and deduplication before a side effect |
| M21 · Agent runtimes | Crash-and-resume timeline | Crash location, checkpoint, receipt | Recovery without silently repeating a completed business action |
| M22 · Memory | Memory lifecycle inspector | Consent, preference correction, TTL, user | Stored facts, provenance, retrieval scope and deletion behavior |
| M23 · MCP | Protocol message stepper | Capabilities, version, transport failure | Negotiation, requests, results and explicit policy boundaries |
| M24 · Multi-agent/A2A | Delegation graph replay | Fan-out, timeout, conflicting result | Ownership, partial completion, duplicate work and budget consumption |
| M25 · Evaluation | Paired-result uncertainty explorer | Sample size, paired outcomes, slices | Estimate uncertainty and how an average can hide a critical regression |
| M26 · Task evaluation | Failure attribution board | Retrieval result, answer, tool state | Different scores for evidence, text quality and actual task completion |
| M27 · Observability | Trace waterfall inspector | Slow span, retry, sampled quality failure | Critical path, cost attribution and earliest failing component |
| M28 · Reliability | Bounded queue simulator | Arrival rate, service time, retries, queue limit | Backlog, dropped requests and tail latency under declared assumptions |
| M29 · Delivery | Release and rollback simulator | Model, prompt, schema and index versions | Compatible version sets and what an incomplete rollback misses |
| M30 · Security | Trust-boundary walkthrough | Untrusted document text, tool authority | Where an attack originates and which external control blocks it |
| M31 · Governance | Risk and review decision board | Intended use, affected group, evidence | Review obligations, ownership and unresolved assumptions |
| M32 · Economics | Cost-per-success calculator | Tokens, retry rate, review labor, success rate | End-to-end economics and sensitivity, using editable price assumptions |
| M33 · Fine-tuning | Adapter update inspector | Rank, target layer, example quality | Update capacity, parameter count and recorded held-out outcomes |
| M34 · Preference/RL | Reward objective sandbox | Preferences, reward definition, policy output | Reward exploitation and divergence between score and useful behavior |
| M35 · Serving | Prefill/decode scheduling replay | Request lengths, batching, cache reuse | TTFT, decode timing and memory with hardware assumptions visible |
| M36 · Distributed training | Training-memory allocator | Precision, sharding, checkpointing, devices | Per-device memory and communication/recompute tradeoffs |
| M37 · Vision/video | Visual evidence inspector | Crop, resolution, sampled frames | Missing details and events; compare claims with visible evidence |
| M38 · Speech | Conversation timeline | Speech boundary, interruption, reconnect | Turn state, cancelled audio and the status of pending actions |
| M39 · Generative media | Denoising trajectory explorer | Noise step, conditioning, recorded seed | Intermediate states and preservation failures with generation settings |
| M40 · Applied architectures | Forecast/recommendation comparison | Temporal split, baseline, cold-start case | Task-specific performance and unsupported generated explanations |
| M41 · System design | Architecture constraint workbench | Tenant count, traffic, failure, budget | Bottlenecks and tradeoffs supported by explicit estimates |
| M42 · Interview judgment | Evidence-based interview rehearsal | Answer, debugging hypothesis, new constraint | Rubric feedback linked to artifacts and prerequisite concepts |

## Original sample specification: M03-L01

**Opening problem:** A support-search system puts a poorly aligned document above a directly aligned one. Is the ranking measuring direction, magnitude or both?

**Prediction:** With query `q = (1, 0)`, choose between document `a = (1, 0)` and document `b = (2, 2)`. Ask which wins under dot product and whether the answer must stay the same under cosine similarity.

**Interaction:** Display three labeled arrows. Provide draggable endpoints and equivalent numeric fields. Show each dot product, vector norm and cosine value beside a ranked result list. Offer metric, normalization and reset controls. Preserve the same inputs when switching metrics.

**Worked result:** Dot products are `q·a = 1` and `q·b = 2`, so `b` ranks first. Cosine similarities are `1` and `1/√2 ≈ 0.707`, so `a` ranks first. Explain how normalization removes the magnitude advantage in this example.

**Transfer check:** Multiply `a` by a positive scalar while retaining its direction. Ask the learner to predict the dot-product change and the unchanged cosine similarity before updating the display.

**Failure check:** Set a document vector to zero. Display cosine as undefined, explain the zero denominator and show the chosen application handling policy. Never silently present a fabricated zero similarity as the mathematical result.

**Production bridge:** Connect the observation to selecting a metric consistent with the embedding model and index. Retain the existing production exercise and interview question. Explain that hand-authored 2D vectors demonstrate the mathematics; they do not demonstrate the semantic quality of a real embedding model.

**Acceptance:** Numeric outputs agree with hand calculations within the documented tolerance; keyboard and pointer controls produce identical states; metric changes preserve inputs; reset restores the fixture; the zero-vector case is explicit; both checks explain their answers.

## Implementation and authoring gates

Before a full lesson is considered ready, its author must supply the opening scenario, prediction, interaction controls/state/outputs, mechanism explanation, worked example, two checks with explanatory feedback, a failure case, and connections to interview and production work. Existing prerequisites and sources remain required.

For every interactive component, specify deterministic fixtures or the source of nondeterminism; input bounds; reset behavior; correct and edge-case outputs; keyboard operation; narrow-screen layout; reduced-motion behavior; and a static explanatory fallback. Label all synthetic, replayed and measured results. A simulation must not imply that it is querying a live model or measuring live infrastructure.

Learning progress should distinguish reading, attempting a check, demonstrating understanding and completing the production exercise. Scrolling alone must not imply mastery. Account requirements, server-side progress and analytics are separate product decisions.

Prototype three representative lessons before scaling the visual system: M03-L01 for mathematical manipulation, M17-L01 for evidence flow, and M21-L02 for state and recovery. Review explanation clarity and accessibility as well as appearance. Then apply the contract across the existing 188-lesson plan without reducing its interview or production depth.
