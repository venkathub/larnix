# Prerequisite-aware learning path

This is one valid full learning sequence. Module numbers are catalogue IDs, not a mandatory teaching order. Evaluation (M25) and security (M30) appear early and recur in practical work. The advanced M34 and M36 branches can be skipped on the application-engineering route because no downstream module requires them.

Entry readiness: basic programming literacy and comfort editing files/running a terminal. M02 supplies the Python, NumPy, pandas, plotting, API, concurrency and SQL bridge; M03 supplies the mathematical bridge. No prior LLM application experience is assumed. Experienced learners may demonstrate prerequisite outcomes rather than repeat lessons.

| Sequence | Module | Required earlier modules, including lesson-specific gates |
| --- | --- | --- |
| 1 | [M01 — AI product engineering](modules/M01.md) | Entry readiness |
| 2 | [M02 — Software engineering for AI](modules/M02.md) | Entry readiness |
| 3 | [M03 — Applied mathematics and statistics](modules/M03.md) | M02 |
| 4 | [M04 — Machine-learning fundamentals](modules/M04.md) | M02, M03 |
| 5 | [M05 — Deep-learning fundamentals](modules/M05.md) | M03, M04 |
| 6 | [M06 — Data engineering and dataset quality](modules/M06.md) | M02, M04 |
| 7 | [M25 — Evaluation methodology](modules/M25.md) | M01, M02, M03 |
| 8 | [M30 — AI application security](modules/M30.md) | M01, M02 |
| 9 | [M07 — Transformer and LLM architecture](modules/M07.md) | M05 |
| 10 | [M08 — Model training lifecycle](modules/M08.md) | M06, M07 |
| 11 | [M09 — Model APIs and application contracts](modules/M09.md) | M02, M07 |
| 12 | [M10 — Prompt engineering](modules/M10.md) | M09 |
| 13 | [M11 — Structured outputs and grounding](modules/M11.md) | M09, M10 |
| 14 | [M12 — Context engineering](modules/M12.md) | M10, M11 |
| 15 | [M13 — Document ingestion and understanding](modules/M13.md) | M06, M11 |
| 16 | [M14 — Embeddings and representations](modules/M14.md) | M03, M07 |
| 17 | [M15 — Vector indexes and databases](modules/M15.md) | M02, M14 |
| 18 | [M16 — Retrieval and ranking](modules/M16.md) | M13, M15 |
| 19 | [M17 — RAG fundamentals](modules/M17.md) | M12, M16, M25 |
| 20 | [M18 — Advanced knowledge systems](modules/M18.md) | M17 |
| 21 | [M19 — Workflows versus agents](modules/M19.md) | M09, M11 |
| 22 | [M20 — Tool engineering](modules/M20.md) | M02, M19, M30 |
| 23 | [M21 — Agent runtimes and harnesses](modules/M21.md) | M20 |
| 24 | [M22 — Memory and personalization](modules/M22.md) | M06, M12, M21 |
| 25 | [M23 — Model Context Protocol](modules/M23.md) | M09, M20 |
| 26 | [M24 — Multi-agent systems and A2A](modules/M24.md) | M21, M23 |
| 27 | [M27 — Observability and diagnosis](modules/M27.md) | M09, M25 |
| 28 | [M28 — Reliability and distributed systems](modules/M28.md) | M02, M09, M27 |
| 29 | [M29 — Deployment and delivery](modules/M29.md) | M02, M04, M06, M25, M28, M30 |
| 30 | [M26 — Task-specific evaluation](modules/M26.md) | M17, M21, M25 |
| 31 | [M31 — Responsible AI and governance](modules/M31.md) | M01, M06, M25, M30 |
| 32 | [M32 — Model selection and economics](modules/M32.md) | M01, M09, M25 |
| 33 | [M33 — Fine-tuning and distillation](modules/M33.md) | M08, M25 |
| 34 | [M34 — Preference and reinforcement learning](modules/M34.md) | M03, M33 |
| 35 | [M35 — Inference and serving systems](modules/M35.md) | M07, M28, M29, M32 |
| 36 | [M36 — Distributed training and advanced optimization](modules/M36.md) | M05, M08, M33 |
| 37 | [M37 — Vision and video systems](modules/M37.md) | M05, M11, M25 |
| 38 | [M38 — Speech and real-time agents](modules/M38.md) | M09, M19, M25 |
| 39 | [M39 — Generative media](modules/M39.md) | M05, M25, M30, M31 |
| 40 | [M40 — Applied AI architectures](modules/M40.md) | M04, M17, M21, M26, M29, M30 |
| 41 | [M41 — AI system design](modules/M41.md) | M27, M29, M30, M31, M32, M40 |
| 42 | [M42 — Interview and engineering judgment](modules/M42.md) | M41 |

## Reading the dependency contract

Each lesson lists direct prerequisites. Prerequisites are transitive: a lesson depends on the knowledge behind its prerequisites as well. Within a module, lessons form a sequence. Additional gates are explicit at the lesson where they apply; for example, M20-L02 requires security lesson M30-L02 before tool-authority design.

Reading links are not extra prerequisite modules. A source may introduce an idea earlier at a conceptual level and support a deeper treatment later. All 42 modules are retained in the complete plan, including advanced branches.

## Routes through the same catalogue

- **Predictive ML engineering:** M01–M06 → M25/M30 → M27–M29 → M31 → M35 → M40. Follow additional dependencies in those modules. M29-L05–L08 form the tracking, registry, scoring and retraining lifecycle. Advanced LLM lessons are not prerequisites for starting the foundational data/ML work.
- **Application engineering:** follow the full sequence and treat M34/M36 as optional advanced branches; use small-model or replay alternatives for compute-heavy exercises.
- **Interview preparation:** begin with the diagnostic questions in the relevant modules; follow prerequisite links for weak answers, then use M42 as the final rehearsal. M42 is not a replacement for the core material.
- **Production reference:** enter at a concrete problem such as M17 (RAG), M21 (agent recovery), M28 (reliability) or M35 (serving); check the prerequisite contract and completion criteria before applying the pattern.
