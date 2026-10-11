# Larnix — Phase 1 curriculum specification

The approved 42-module scope is now broken into **168 original lessons**. Every lesson includes direct prerequisites, topic coverage, a learning outcome, primary readings, an interview question with answer signals, and a production exercise with acceptance criteria.

Start with the [lesson index](INDEX.md). Use the [learning path](LEARNING_PATH.md) for prerequisite order, the [coverage map](COVERAGE.md) to inspect scope, the [source register](SOURCES.md) for research, and the [validation report](AUDIT.md) for structural checks.

## What Phase 1 delivers

| Deliverable | Contents |
| --- | --- |
| 42 module specifications | Four lesson plans per module with stable IDs such as `M17-L01` |
| 168 interview prompts | Original questions, strong-answer signals and a common scoring rubric |
| 168 production exercises | Original implementation, analysis, investigation or design assignments with explicit acceptance criteria |
| Prerequisite map | Direct lesson dependencies, cross-module gates and a valid complete learning sequence |
| Source register | Primary papers, official documentation, specifications and author-written learning materials; review date and version policy |
| Coverage and validation | Approved-scope mapping, field checks, cycle detection, learning-order checks and local-link checks |
| Maintainable source records | JSON records plus a standard-library renderer/checker; readable Markdown pages generated from those records |

This phase specifies future teaching and lab work. It does not deliver the application, complete lesson prose, runnable labs, model results or deployed services. Exercise verbs such as “build” and “run” describe future learner assignments. Their presence does not mean those exercises have already been implemented or executed.

## Originality and research policy

[The referenced AI Engineering Playbook](https://github.com/karthikreddy-7/ai-engineering-playbook) remains a background reference. Larnix is independently structured and authored; this work does not fork that repository or import its code, prose, questions, exercises, diagrams or interface.

The approved independent catalogue is the scope baseline. Primary sources establish concepts and provide further reading. The recurring equipment-rental support scenario, question wording, exercise briefs, sequencing and acceptance criteria are original. Other scenarios include invoice reconciliation, recommendations, demand forecasts, visual inspection, voice interactions and code repair.

Sources are reading entry points rather than copied tutorials. Before writing a full lesson, identify the relevant sections, verify technical claims, record package/model/protocol versions and review any licensing obligations for assets or datasets actually used. A source's example code or dataset is not automatically part of Larnix.

## Entry readiness and ordering

Learners should be comfortable with basic programming ideas and running commands. M02 provides a Python, HTTP, concurrency and SQL bridge; M03 provides mathematical foundations. No previous LLM application experience is required. A learner can demonstrate an outcome to skip familiar prerequisite material.

The catalogue has seven groups of six modules. Grouping helps navigation; it does not force security and evaluation to the end. The [recommended path](LEARNING_PATH.md) brings M25 and M30 forward and validates all direct and transitive prerequisites. Lessons inside each module are sequential, and extra prerequisites appear at the exact lesson that needs them.

M34 (preference and reinforcement learning) and M36 (distributed training) are advanced branches. They remain fully planned within the 42-module scope. Application engineers may defer them without blocking downstream core modules. Other compute-heavy lessons provide small-model, mocked-service or recorded-trace alternatives.

## Lesson contract for subsequent authoring

Every completed lesson should contain the following material, based on its Phase 1 specification:

1. **Problem and outcome:** a concrete situation and a result the learner can demonstrate.
2. **Explanation:** the mechanism, a worked example, assumptions and tradeoffs.
3. **Implementation or analysis:** an original, reproducible artifact with explicit inputs and environment requirements.
4. **Failure investigation:** at least one misleading result, invalid input, resource limit or recovery scenario.
5. **Interview practice:** the planned question, a reasoned answer and a counterexample or limitation.
6. **Production review:** acceptance results, baseline comparison, resource costs, boundaries and operating implications.
7. **Attribution:** source links, version notes and any reused-asset provenance.

The four lessons in a module progress from mechanism to engineering decisions and operation. Lessons are not required to use a single framework or provider. Implement a simple baseline before introducing a framework where it improves the learning objective.

## Exercise evidence and assessment

Each exercise requires a versioned artifact or design specification, a baseline or hand-checkable fixture, a results or expected-results table containing a failure case, and a decision/limitations note. The local acceptance criteria define what must be demonstrated.

Design exercises are judged by explicit assumptions, internally consistent calculations, alternatives, failure handling and a falsifiable validation plan. Implementation exercises are judged by actual outputs and failure behavior. A design specification alone cannot satisfy an assignment that asks for a working implementation.

Use these labels consistently:

- **Designed:** a specification or calculation; implementation remains untested.
- **Simulated:** a mock environment or synthetic response set; validates the behavior exercised by that simulation.
- **Replayed:** recorded outputs or traces; supports comparative analysis but does not establish live hardware performance.
- **Measured:** executed against the stated implementation, dataset and environment with recorded results.

Live providers, cloud resources and large GPU runs are optional. Local mocks and synthetic records are the default for lessons involving business actions or sensitive data. Low-cost alternatives must state what they cannot demonstrate. Performance claims require matched workloads and recorded hardware/software versions.

## Interview rubric

| Score | Evidence |
| --- | --- |
| 0 | Incorrect or unsupported explanation |
| 1 | Names the concept but misses its mechanism or tradeoffs |
| 2 | Explains the mechanism and a relevant tradeoff |
| 3 | Adds a concrete example, a way to verify the claim and an important limitation |

A strong answer need not use the exact wording of the answer signals. Reasoning and engineering judgment matter more than memorized terminology. Score each question independently; critical factual mistakes require correction even when other answers are strong.

## Production reference conventions

Full lesson authoring should make these items easy to find when applicable: decision criteria, minimum working example, version assumptions, failure symptoms, diagnostic steps, operational limits, access boundaries, metrics and rollback/recovery. The plan already assigns these concerns to specific lessons; the coverage map shows where they recur.

The platform enhancements approved earlier—interview preparation and production reference—share this curriculum. One lesson record can support a learning page, question practice and a production lookup view. UI design, progress tracking, question scheduling and backend implementation belong to later phases.

## Capstone evidence

M40 applies the curriculum to recommendations, forecasting, documents and operational/coding assistants. M41 assembles a production-readiness dossier. M42 turns the evidence into technical explanations, debugging practice and design-interview responses.

The final dossier should include the problem brief, data rights and lineage, architecture decisions, evaluation set and report, threat model, cost/capacity estimates, release and rollback plan, incident runbook and limitations. A successful demo is one artifact; it does not replace these forms of evidence.

## Maintaining the plan

The authoritative records are [curriculum.json](curriculum.json) and [sources.json](sources.json). Edit these records before regenerating the module pages, index, path, sources, coverage map and audit report. This overview is manually maintained.

From the repository root:

```bash
python3 scripts/curriculum.py render
python3 scripts/curriculum.py check
```

The renderer uses only Python's standard library. The checker verifies structure, dependencies, source IDs, local links and generated-file consistency. It does not certify source accuracy or replace independent technical review. Updates to scope, prerequisites or exercise objectives should be reviewed as curriculum changes.

The next phase should author and validate a representative set of complete lessons before scaling to all 168. Choose samples from foundations, RAG, agents, evaluation, security and serving to test the lesson contract across different kinds of material.
