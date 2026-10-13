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
| 35 | [M35 — Inference and serving systems](modules/M35.md) | M02, M05, M07, M25, M28, M32 |
| 36 | [M36 — Distributed training and advanced optimization](modules/M36.md) | M05, M08, M33 |
| 37 | [M37 — Vision and video systems](modules/M37.md) | M05, M11, M25 |
| 38 | [M38 — Speech and real-time agents](modules/M38.md) | M09, M19, M25 |
| 39 | [M39 — Generative media](modules/M39.md) | M05, M25, M30, M31 |
| 40 | [M40 — Applied AI architectures](modules/M40.md) | M04, M06, M17, M21, M25, M26, M29, M30 |
| 41 | [M41 — AI system design](modules/M41.md) | M27, M29, M30, M31, M32, M40 |
| 42 | [M42 — Interview and engineering judgment](modules/M42.md) | M41 |

## Reading the dependency contract

Each lesson lists direct prerequisites. Prerequisites are transitive: a lesson depends on the knowledge behind its prerequisites as well. Stable lesson IDs identify topics, not required predecessors. Follow each module’s explicit teaching order; only listed prerequisites are required. Additional gates are explicit at the lesson where they apply; for example, M20-L02 requires security lesson M30-L02 before tool-authority design.

Reading links are not extra prerequisite modules. A source may introduce an idea earlier at a conceptual level and support a deeper treatment later. All 42 modules are retained in the complete plan, including advanced branches.

## Routes through the same catalogue

- **Application engineering:** follow the full sequence and treat M34/M36 as optional advanced branches; use small-model or replay alternatives for compute-heavy exercises.
- **Interview preparation:** begin with the diagnostic questions in the relevant modules; follow prerequisite links for weak answers, then use M42 as the final rehearsal. M42 is not a replacement for the core material.
- **Production reference:** enter at a concrete problem such as M17 (RAG), M21 (agent recovery), M28 (reliability) or M35 (serving); check the prerequisite contract and completion criteria before applying the pattern.


## Teaching order within modules

The same order drives module lists and next/previous navigation in the classroom. IDs and URLs stay unchanged.

- M01: [M01-L01](modules/M01.md#m01-l01) → [M01-L02](modules/M01.md#m01-l02) → [M01-L03](modules/M01.md#m01-l03) → [M01-L04](modules/M01.md#m01-l04)
- M02: [M02-L08](modules/M02.md#m02-l08) → [M02-L09](modules/M02.md#m02-l09) → [M02-L10](modules/M02.md#m02-l10) → [M02-L11](modules/M02.md#m02-l11) → [M02-L01](modules/M02.md#m02-l01) → [M02-L05](modules/M02.md#m02-l05) → [M02-L06](modules/M02.md#m02-l06) → [M02-L07](modules/M02.md#m02-l07) → [M02-L02](modules/M02.md#m02-l02) → [M02-L03](modules/M02.md#m02-l03) → [M02-L04](modules/M02.md#m02-l04)
- M03: [M03-L01](modules/M03.md#m03-l01) → [M03-L02](modules/M03.md#m03-l02) → [M03-L03](modules/M03.md#m03-l03) → [M03-L04](modules/M03.md#m03-l04) → [M03-L05](modules/M03.md#m03-l05) → [M03-L06](modules/M03.md#m03-l06)
- M04: [M04-L01](modules/M04.md#m04-l01) → [M04-L02](modules/M04.md#m04-l02) → [M04-L03](modules/M04.md#m04-l03) → [M04-L04](modules/M04.md#m04-l04) → [M04-L05](modules/M04.md#m04-l05) → [M04-L06](modules/M04.md#m04-l06) → [M04-L07](modules/M04.md#m04-l07)
- M05: [M05-L01](modules/M05.md#m05-l01) → [M05-L02](modules/M05.md#m05-l02) → [M05-L03](modules/M05.md#m05-l03) → [M05-L04](modules/M05.md#m05-l04)
- M06: [M06-L01](modules/M06.md#m06-l01) → [M06-L02](modules/M06.md#m06-l02) → [M06-L03](modules/M06.md#m06-l03) → [M06-L04](modules/M06.md#m06-l04) → [M06-L05](modules/M06.md#m06-l05) → [M06-L06](modules/M06.md#m06-l06) → [M06-L07](modules/M06.md#m06-l07)
- M25: [M25-L01](modules/M25.md#m25-l01) → [M25-L02](modules/M25.md#m25-l02) → [M25-L03](modules/M25.md#m25-l03) → [M25-L04](modules/M25.md#m25-l04)
- M30: [M30-L01](modules/M30.md#m30-l01) → [M30-L02](modules/M30.md#m30-l02) → [M30-L03](modules/M30.md#m30-l03) → [M30-L04](modules/M30.md#m30-l04)
- M07: [M07-L01](modules/M07.md#m07-l01) → [M07-L02](modules/M07.md#m07-l02) → [M07-L03](modules/M07.md#m07-l03) → [M07-L04](modules/M07.md#m07-l04)
- M08: [M08-L01](modules/M08.md#m08-l01) → [M08-L02](modules/M08.md#m08-l02) → [M08-L03](modules/M08.md#m08-l03) → [M08-L04](modules/M08.md#m08-l04)
- M09: [M09-L01](modules/M09.md#m09-l01) → [M09-L02](modules/M09.md#m09-l02) → [M09-L03](modules/M09.md#m09-l03) → [M09-L04](modules/M09.md#m09-l04)
- M10: [M10-L01](modules/M10.md#m10-l01) → [M10-L02](modules/M10.md#m10-l02) → [M10-L03](modules/M10.md#m10-l03) → [M10-L04](modules/M10.md#m10-l04)
- M11: [M11-L01](modules/M11.md#m11-l01) → [M11-L02](modules/M11.md#m11-l02) → [M11-L03](modules/M11.md#m11-l03) → [M11-L04](modules/M11.md#m11-l04)
- M12: [M12-L01](modules/M12.md#m12-l01) → [M12-L02](modules/M12.md#m12-l02) → [M12-L03](modules/M12.md#m12-l03) → [M12-L04](modules/M12.md#m12-l04)
- M13: [M13-L01](modules/M13.md#m13-l01) → [M13-L02](modules/M13.md#m13-l02) → [M13-L03](modules/M13.md#m13-l03) → [M13-L04](modules/M13.md#m13-l04)
- M14: [M14-L01](modules/M14.md#m14-l01) → [M14-L02](modules/M14.md#m14-l02) → [M14-L03](modules/M14.md#m14-l03) → [M14-L04](modules/M14.md#m14-l04)
- M15: [M15-L01](modules/M15.md#m15-l01) → [M15-L02](modules/M15.md#m15-l02) → [M15-L03](modules/M15.md#m15-l03) → [M15-L04](modules/M15.md#m15-l04)
- M16: [M16-L01](modules/M16.md#m16-l01) → [M16-L02](modules/M16.md#m16-l02) → [M16-L03](modules/M16.md#m16-l03) → [M16-L04](modules/M16.md#m16-l04)
- M17: [M17-L01](modules/M17.md#m17-l01) → [M17-L02](modules/M17.md#m17-l02) → [M17-L03](modules/M17.md#m17-l03) → [M17-L04](modules/M17.md#m17-l04)
- M18: [M18-L01](modules/M18.md#m18-l01) → [M18-L02](modules/M18.md#m18-l02) → [M18-L03](modules/M18.md#m18-l03) → [M18-L04](modules/M18.md#m18-l04)
- M19: [M19-L01](modules/M19.md#m19-l01) → [M19-L02](modules/M19.md#m19-l02) → [M19-L03](modules/M19.md#m19-l03) → [M19-L04](modules/M19.md#m19-l04)
- M20: [M20-L01](modules/M20.md#m20-l01) → [M20-L02](modules/M20.md#m20-l02) → [M20-L03](modules/M20.md#m20-l03) → [M20-L04](modules/M20.md#m20-l04)
- M21: [M21-L01](modules/M21.md#m21-l01) → [M21-L02](modules/M21.md#m21-l02) → [M21-L03](modules/M21.md#m21-l03) → [M21-L04](modules/M21.md#m21-l04)
- M22: [M22-L01](modules/M22.md#m22-l01) → [M22-L02](modules/M22.md#m22-l02) → [M22-L03](modules/M22.md#m22-l03) → [M22-L04](modules/M22.md#m22-l04)
- M23: [M23-L01](modules/M23.md#m23-l01) → [M23-L02](modules/M23.md#m23-l02) → [M23-L03](modules/M23.md#m23-l03) → [M23-L04](modules/M23.md#m23-l04)
- M24: [M24-L01](modules/M24.md#m24-l01) → [M24-L02](modules/M24.md#m24-l02) → [M24-L03](modules/M24.md#m24-l03) → [M24-L04](modules/M24.md#m24-l04)
- M27: [M27-L01](modules/M27.md#m27-l01) → [M27-L02](modules/M27.md#m27-l02) → [M27-L03](modules/M27.md#m27-l03) → [M27-L04](modules/M27.md#m27-l04)
- M28: [M28-L01](modules/M28.md#m28-l01) → [M28-L02](modules/M28.md#m28-l02) → [M28-L03](modules/M28.md#m28-l03) → [M28-L04](modules/M28.md#m28-l04)
- M29: [M29-L01](modules/M29.md#m29-l01) → [M29-L02](modules/M29.md#m29-l02) → [M29-L05](modules/M29.md#m29-l05) → [M29-L06](modules/M29.md#m29-l06) → [M29-L07](modules/M29.md#m29-l07) → [M29-L08](modules/M29.md#m29-l08) → [M29-L03](modules/M29.md#m29-l03) → [M29-L04](modules/M29.md#m29-l04)
- M26: [M26-L01](modules/M26.md#m26-l01) → [M26-L02](modules/M26.md#m26-l02) → [M26-L03](modules/M26.md#m26-l03) → [M26-L04](modules/M26.md#m26-l04)
- M31: [M31-L01](modules/M31.md#m31-l01) → [M31-L02](modules/M31.md#m31-l02) → [M31-L03](modules/M31.md#m31-l03) → [M31-L04](modules/M31.md#m31-l04)
- M32: [M32-L01](modules/M32.md#m32-l01) → [M32-L02](modules/M32.md#m32-l02) → [M32-L03](modules/M32.md#m32-l03) → [M32-L04](modules/M32.md#m32-l04)
- M33: [M33-L01](modules/M33.md#m33-l01) → [M33-L02](modules/M33.md#m33-l02) → [M33-L03](modules/M33.md#m33-l03) → [M33-L04](modules/M33.md#m33-l04)
- M34: [M34-L01](modules/M34.md#m34-l01) → [M34-L02](modules/M34.md#m34-l02) → [M34-L03](modules/M34.md#m34-l03) → [M34-L04](modules/M34.md#m34-l04)
- M35: [M35-L05](modules/M35.md#m35-l05) → [M35-L06](modules/M35.md#m35-l06) → [M35-L01](modules/M35.md#m35-l01) → [M35-L02](modules/M35.md#m35-l02) → [M35-L03](modules/M35.md#m35-l03) → [M35-L04](modules/M35.md#m35-l04)
- M36: [M36-L01](modules/M36.md#m36-l01) → [M36-L02](modules/M36.md#m36-l02) → [M36-L03](modules/M36.md#m36-l03) → [M36-L04](modules/M36.md#m36-l04)
- M37: [M37-L01](modules/M37.md#m37-l01) → [M37-L02](modules/M37.md#m37-l02) → [M37-L03](modules/M37.md#m37-l03) → [M37-L04](modules/M37.md#m37-l04)
- M38: [M38-L01](modules/M38.md#m38-l01) → [M38-L02](modules/M38.md#m38-l02) → [M38-L03](modules/M38.md#m38-l03) → [M38-L04](modules/M38.md#m38-l04) → [M38-L05](modules/M38.md#m38-l05)
- M39: [M39-L01](modules/M39.md#m39-l01) → [M39-L02](modules/M39.md#m39-l02) → [M39-L03](modules/M39.md#m39-l03) → [M39-L04](modules/M39.md#m39-l04)
- M40: [M40-L05](modules/M40.md#m40-l05) → [M40-L06](modules/M40.md#m40-l06) → [M40-L01](modules/M40.md#m40-l01) → [M40-L02](modules/M40.md#m40-l02) → [M40-L03](modules/M40.md#m40-l03) → [M40-L04](modules/M40.md#m40-l04)
- M41: [M41-L01](modules/M41.md#m41-l01) → [M41-L02](modules/M41.md#m41-l02) → [M41-L03](modules/M41.md#m41-l03) → [M41-L04](modules/M41.md#m41-l04)
- M42: [M42-L01](modules/M42.md#m42-l01) → [M42-L02](modules/M42.md#m42-l02) → [M42-L03](modules/M42.md#m42-l03) → [M42-L04](modules/M42.md#m42-l04)

## Predictive ML engineering

Data programming, model selection, features, predictive-model operations, edge export and applied baselines. The sequence includes every transitive prerequisite and does not require transformer, retrieval or agent modules. Production-scale reliability and LLM serving remain separate extensions.

These are lesson-level selections, not a requirement to finish every module containing them. All listed units retain their current planned/preview status.

**Target outcomes:** [M02-L07](modules/M02.md#m02-l07), [M04-L07](modules/M04.md#m04-l07), [M06-L07](modules/M06.md#m06-l07), [M29-L08](modules/M29.md#m29-l08), [M35-L06](modules/M35.md#m35-l06), [M40-L05](modules/M40.md#m40-l05), [M40-L06](modules/M40.md#m40-l06)

**Complete prerequisite route (47 lessons):**

1. [M01-L01](modules/M01.md#m01-l01)
2. [M01-L02](modules/M01.md#m01-l02)
3. [M01-L03](modules/M01.md#m01-l03)
4. [M01-L04](modules/M01.md#m01-l04)
5. [M02-L01](modules/M02.md#m02-l01)
6. [M02-L05](modules/M02.md#m02-l05)
7. [M02-L06](modules/M02.md#m02-l06)
8. [M02-L07](modules/M02.md#m02-l07)
9. [M02-L02](modules/M02.md#m02-l02)
10. [M02-L03](modules/M02.md#m02-l03)
11. [M02-L04](modules/M02.md#m02-l04)
12. [M03-L01](modules/M03.md#m03-l01)
13. [M03-L02](modules/M03.md#m03-l02)
14. [M03-L03](modules/M03.md#m03-l03)
15. [M03-L04](modules/M03.md#m03-l04)
16. [M04-L01](modules/M04.md#m04-l01)
17. [M04-L02](modules/M04.md#m04-l02)
18. [M04-L03](modules/M04.md#m04-l03)
19. [M04-L04](modules/M04.md#m04-l04)
20. [M04-L05](modules/M04.md#m04-l05)
21. [M04-L06](modules/M04.md#m04-l06)
22. [M04-L07](modules/M04.md#m04-l07)
23. [M05-L01](modules/M05.md#m05-l01)
24. [M05-L02](modules/M05.md#m05-l02)
25. [M05-L03](modules/M05.md#m05-l03)
26. [M06-L01](modules/M06.md#m06-l01)
27. [M06-L02](modules/M06.md#m06-l02)
28. [M06-L03](modules/M06.md#m06-l03)
29. [M06-L06](modules/M06.md#m06-l06)
30. [M06-L07](modules/M06.md#m06-l07)
31. [M25-L01](modules/M25.md#m25-l01)
32. [M25-L02](modules/M25.md#m25-l02)
33. [M25-L03](modules/M25.md#m25-l03)
34. [M25-L04](modules/M25.md#m25-l04)
35. [M30-L01](modules/M30.md#m30-l01)
36. [M30-L02](modules/M30.md#m30-l02)
37. [M30-L03](modules/M30.md#m30-l03)
38. [M29-L01](modules/M29.md#m29-l01)
39. [M29-L02](modules/M29.md#m29-l02)
40. [M29-L05](modules/M29.md#m29-l05)
41. [M29-L06](modules/M29.md#m29-l06)
42. [M29-L07](modules/M29.md#m29-l07)
43. [M29-L08](modules/M29.md#m29-l08)
44. [M35-L05](modules/M35.md#m35-l05)
45. [M35-L06](modules/M35.md#m35-l06)
46. [M40-L05](modules/M40.md#m40-l05)
47. [M40-L06](modules/M40.md#m40-l06)
