#!/usr/bin/env python3
"""Render and validate the Phase 1 curriculum using only the Python standard library."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "curriculum"
CONTRACT_CATEGORIES = {
    "problem", "interaction", "explanation", "checks", "artifact",
    "failure", "interview", "production", "attribution",
}


def load():
    curriculum = json.loads((BASE / "curriculum.json").read_text())
    sources = json.loads((BASE / "sources.json").read_text())
    return curriculum, sources


def validate(curriculum, source_data):
    """Validate content and the full lesson dependency graph before rendering."""
    errors = []
    modules = curriculum["modules"]
    sources = source_data["sources"]
    lessons = [lesson for module in modules for lesson in module["lessons"]]
    source_ids = [s["id"] for s in sources]
    lesson_ids = [lesson["id"] for lesson in lessons]
    module_ids = [m["id"] for m in modules]
    lesson_map = {lesson["id"]: lesson for lesson in lessons}

    def require(condition, message):
        if not condition:
            errors.append(message)

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def text_list(value, minimum=1):
        return isinstance(value, list) and len(value) >= minimum and all(text(v) for v in value)

    require(len(modules) == 42, "The approved scope requires 42 modules.")
    require(len(lessons) == curriculum["expected_lessons"], "Lesson count differs from the reviewed scope.")
    for label, ids in (("source", source_ids), ("module", module_ids), ("lesson", lesson_ids)):
        require(len(ids) == len(set(ids)), f"Duplicate {label} IDs.")
    require(module_ids == [f"M{n:02}" for n in range(1, 43)], "Module IDs must be M01–M42 in order.")
    urls = [s["url"] for s in sources]
    require(len(urls) == len(set(urls)), "Duplicate source URLs.")
    for source in sources:
        sid = source["id"]
        for field in ("title", "focus", "type", "reviewed_on", "verification", "version_policy"):
            require(text(source.get(field)), f"{sid}: missing {field}.")
        parsed = urlparse(source["url"])
        require(parsed.scheme == "https" and bool(parsed.netloc), f"{sid}: invalid HTTPS URL.")

    used_sources = set()
    for module in modules:
        mid = module["id"]
        require(text(module.get("title")), f"{mid}: title missing.")
        require(module.get("status") in {"planned", "in_progress"}, f"{mid}: invalid module delivery state.")
        require(module.get("depth") in {"core", "advanced"}, f"{mid}: invalid depth.")
        require(len(module["lessons"]) >= 4, f"{mid}: preserve the original four lessons.")
        require(module["lessons"][0]["prerequisites"] == module["prerequisites"],
                f"{mid}: entry prerequisites must match lesson 1.")
        require(set(module["sources"]) <= set(source_ids), f"{mid}: unknown module source.")
        used_sources.update(module["sources"])
        for number, lesson in enumerate(module["lessons"], 1):
            lid = lesson["id"]
            require(lid == f"{mid}-L{number:02}", f"{lid}: unexpected lesson ID/order.")
            require(lesson.get("status") in {"planned", "preview", "complete"}, f"{lid}: invalid lesson status.")
            basis = lesson.get("estimate_basis", {})
            for field in ("reviewed_on", "confidence", "assumption", "work", "validation"):
                require(text(basis.get(field)), f"{lid}: missing estimate basis {field}.")
            delivery = lesson.get("delivery", {})
            require(delivery.get("full_contract") in {"not_met", "verified"}, f"{lid}: missing contract state.")
            require((lesson['status'] == 'complete') == (delivery.get('full_contract') == 'verified'), f"{lid}: completion requires a verified contract.")
            if lesson['status'] == 'complete':
                evidence = delivery.get('completion_evidence', {})
                require(isinstance(evidence, dict) and set(evidence) == CONTRACT_CATEGORIES
                        and all(text(item) and (ROOT / item).is_file() for item in evidence.values()),
                        f"{lid}: full contract requires evidence for all nine contract categories.")
            if delivery.get('artifact_path'):
                require((ROOT / delivery['artifact_path']).is_file(), f"{lid}: missing runnable artifact.")
            for field in ("title", "outcome", "resource_mode"):
                require(text(lesson.get(field)), f"{lid}: missing {field}.")
            require(text_list(lesson.get("topics"), 3), f"{lid}: needs at least three topics.")
            require(text_list(lesson.get("sources")), f"{lid}: no source reading.")
            require(set(lesson["sources"]) <= set(source_ids), f"{lid}: unknown source.")
            require(set(lesson["sources"]) <= set(module["sources"]), f"{lid}: source absent from module register.")
            used_sources.update(lesson["sources"])
            require(len(lesson["prerequisites"]) == len(set(lesson["prerequisites"])),
                    f"{lid}: duplicate prerequisite.")
            for dependency in lesson["prerequisites"]:
                require(dependency in lesson_map, f"{lid}: unknown prerequisite {dependency}.")
            if number > 1:
                require(f"{mid}-L{number-1:02}" in lesson["prerequisites"],
                        f"{lid}: preceding lesson is not a prerequisite.")
            interview = lesson.get("interview", {})
            require(text(interview.get("question")), f"{lid}: missing interview question.")
            require(text_list(interview.get("strong_answer_signals"), 2), f"{lid}: weak interview guidance.")
            require(set(interview.get("rubric", {})) == {"0", "1", "2", "3"}, f"{lid}: missing interview rubric.")
            exercise = lesson.get("production_exercise", {})
            require(text(exercise.get("brief")), f"{lid}: missing production exercise.")
            require(text_list(exercise.get("acceptance"), 2), f"{lid}: missing acceptance criteria.")
            require(text_list(lesson.get("evidence_required"), 4), f"{lid}: incomplete evidence contract.")
            for kind in ("guided_study", "exercise"):
                hours = lesson.get("estimated_hours", {}).get(kind, [])
                require(len(hours) == 2 and all(isinstance(h, int) and h > 0 for h in hours)
                        and hours[0] <= hours[1], f"{lid}: invalid {kind} estimate.")

    require(used_sources == set(source_ids), "Source register contains an unused entry.")
    for name, values in (
        ("interview questions", [l["interview"]["question"] for l in lessons]),
        ("exercise briefs", [l["production_exercise"]["brief"] for l in lessons]),
        ("lesson titles", [l["title"] for l in lessons]),
    ):
        require(len(values) == len(set(values)), f"Duplicate {name}.")

    previews = json.loads((ROOT / 'web/lessons.json').read_text())
    require({l['id'] for l in lessons if l['status'] in {'preview', 'complete'}} == set(previews), 'Preview status and published lesson manifest differ.')
    for concern in curriculum.get('review_coverage', []):
        require(set(concern['lessons']) <= set(lesson_ids), 'Review coverage contains an unknown lesson.')
    # Detect cycles at lesson granularity, including cross-module gates.
    visiting, visited = set(), set()

    def visit(lid, trail):
        if lid in visiting:
            errors.append("Prerequisite cycle: " + " -> ".join(trail + [lid]))
            return
        if lid in visited or lid not in lesson_map:
            return
        visiting.add(lid)
        for dependency in lesson_map[lid]["prerequisites"]:
            visit(dependency, trail + [lid])
        visiting.remove(lid)
        visited.add(lid)

    for lid in lesson_ids:
        visit(lid, [])

    order = curriculum["recommended_module_order"]
    require(len(order) == len(module_ids) and set(order) == set(module_ids), "Learning path must cover every module exactly once.")
    position = {mid: index for index, mid in enumerate(order)}
    for lesson in lessons:
        for dependency in lesson["prerequisites"]:
            dep_module, own_module = dependency[:3], lesson["id"][:3]
            if dep_module != own_module and dep_module in position and own_module in position:
                require(position[dep_module] < position[own_module],
                        f"Learning path places {lesson['id']} before {dependency}.")
    track_members = [mid for track in curriculum["tracks"] for mid in track["modules"]]
    require(len(track_members) == len(module_ids) and set(track_members) == set(module_ids),
            "Tracks must partition all modules exactly once.")
    for track in curriculum["tracks"]:
        for mid in track["modules"]:
            module = next((m for m in modules if m["id"] == mid), None)
            require(module is not None and module["track"] == track["id"], f"{mid}: inconsistent track.")
    return errors


def render(curriculum, source_data):
    modules = curriculum["modules"]
    sources = {s["id"]: s for s in source_data["sources"]}
    module_map = {m["id"]: m for m in modules}
    lessons = [l for m in modules for l in m["lessons"]]
    files = {}

    def lesson_link(lid, inside_module=False):
        prefix = "" if inside_module else "modules/"
        return f"[{lid}]({prefix}{lid[:3]}.md#{lid.lower()})"

    def module_link(mid):
        return f"[{mid} — {module_map[mid]['title']}](modules/{mid}.md)"

    def source_link(sid):
        s = sources[sid]
        return f"[{sid}: {s['title']}]({s['url']})"

    for module in modules:
        mid = module["id"]
        prereqs = ", ".join(lesson_link(p, True) for p in module["prerequisites"]) or "Entry module; see the readiness guide in the curriculum overview."
        lines = [f"# {mid} — {module['title']}", "",
                 "[All modules](../INDEX.md) · [Learning path](../LEARNING_PATH.md) · [Source register](../SOURCES.md) · [Teaching design](../TEACHING_DESIGN.md)", "",
                 f"**Status:** {module['status']} · **Depth:** {module['depth']} · **Track:** {module['track']}", "",
                 f"**Entry prerequisites:** {prereqs}", "",
                 f"{len(module['lessons'])} lesson specifications follow. Each lesson will use a concrete problem, prediction, interactive explanation, worked example, inline checks and failure investigation before production and interview practice. Follow the teaching design for accessibility and original visual treatment. Delivery status is stated per lesson; a preview is not a completed lab. Complete the evidence package for each exercise; live deployment is not required. Later lessons may introduce an additional cross-module prerequisite.", "",
                 "## Module outcomes", ""]
        lines += [f"- {l['outcome']}" for l in module["lessons"]]
        for lesson in module["lessons"]:
            lid = lesson["id"]
            p = ", ".join(lesson_link(dep, True) for dep in lesson["prerequisites"]) or "Entry readiness only."
            h = lesson["estimated_hours"]
            lines += ["", f'<a id="{lid.lower()}"></a>', "", f"## {lid} — {lesson['title']}", "",
                      f"**Delivery:** {lesson['status']} · full lesson contract: {lesson['delivery']['full_contract']} · interaction: {lesson['delivery']['interaction']} · artifact: {lesson['delivery']['artifact']}", "",
                      f"**Prerequisites:** {p}", "",
                      f"**Learning outcome:** {lesson['outcome']}", "",
                      "**Topics:** " + "; ".join(lesson["topics"]) + ".", "",
                      f"**Study estimate:** {h['guided_study'][0]}–{h['guided_study'][1]} hours guided study + {h['exercise'][0]}–{h['exercise'][1]} hours exercise. These are learner-effort estimates, not an implementation schedule.", "",
                      f"**Estimate basis:** {lesson['estimate_basis']['work']} {lesson['estimate_basis']['assumption']} Confidence: {lesson['estimate_basis']['confidence']}.", "",
                      "### Primary readings", ""]
            if lesson['delivery'].get('artifact_path'):
                lines += [f"**Runnable artifact:** [Data foundations lab](../../../{lesson['delivery']['artifact_path']}) — artifact available; complete lesson narrative still planned.", ""]
            lines += [f"- {source_link(sid)} — {sources[sid]['focus']}." for sid in lesson["sources"]]
            lines += ["", "### Interview question", "", lesson["interview"]["question"], "",
                      "**A strong answer addresses:** " + "; ".join(lesson["interview"]["strong_answer_signals"]) + ".", "",
                      "Score 0–3 using the [shared interview rubric](../README.md#interview-rubric).", "",
                      "### Production exercise", "", lesson["production_exercise"]["brief"], "",
                      "**Acceptance criteria:**", ""]
            lines += [f"- {a}." for a in lesson["production_exercise"]["acceptance"]]
            lines += ["", "**Evidence to submit:**", ""]
            lines += [f"- {item}." for item in lesson["evidence_required"]]
            lines += ["", f"**Resources:** {lesson['resource_mode']}"]
        lines += ["", "## Module completion gate", "",
                  "Submit every lesson artifact, answer its interview question, and explain one failure-and-recovery case. A reviewer checks acceptance criteria and labels results as designed, simulated, replayed or measured. A plan or replay is not proof of production performance.", "",
                  "Readings support concepts. Larnix's lesson sequencing, scenarios, questions and acceptance criteria are original curriculum design. Recheck relevant source sections and pin implementation versions when writing the actual lessons.", ""]
        files[f"modules/{mid}.md"] = "\n".join(lines)

    lines = ["# Larnix — 42-module lesson index", "",
             f"{len(lessons)} original lesson plans, each with prerequisites, primary readings, an interview question with answer signals, and a production exercise with acceptance criteria.", "",
             "[Overview](README.md) · [Teaching design](TEACHING_DESIGN.md) · [Prerequisite-aware learning path](LEARNING_PATH.md) · [Sources](SOURCES.md) · [Coverage](COVERAGE.md) · [Validation report](AUDIT.md)", "",
             "The numeric catalogue groups topics; use the learning path to bring evaluation and security forward. Each linked plan states its delivery status. Authored previews and runnable artifacts do not by themselves satisfy the full lesson contract."]
    for track in curriculum["tracks"]:
        lines += ["", f"## {track['id']} — {track['title']}", ""]
        for mid in track["modules"]:
            module = module_map[mid]
            lines += [f"### {module_link(mid)}", ""]
            for lesson in module["lessons"]:
                lines.append(f"- {lesson_link(lesson['id'])} — {lesson['title']}")
            lines.append("")
    files["INDEX.md"] = "\n".join(lines).rstrip() + "\n"

    lines = ["# Primary source register", "",
             f"Planning review date: **{curriculum['planning_date']}**. **{len(sources)} primary sources**: original papers, official documentation/specifications, maintainer guidance, and author-written courses or textbooks.", "",
             "These are reading entry points, not claims that every lesson detail appears in one page. Select exact sections when writing lessons. Source concepts are attributed; the curriculum questions, scenarios and exercise specifications are original. No source code, course exercises or prose were imported.", "",
             "External pages were opened during research. The offline validator checks references and URL syntax; it does not re-fetch pages, validate every external link, or certify API compatibility. Recheck mutable pages and applicable licenses before implementation.", ""]
    for sid, source in sorted(sources.items()):
        used_by = [l["id"] for l in lessons if sid in l["sources"]]
        lines += [f"## {sid} — {source['title']}", "",
                  f"**Read:** [{source['title']}]({source['url']})", "",
                  f"**Type:** {source['type']} · **Reviewed:** {source['reviewed_on']}", "",
                  f"**Reading focus:** {source['focus']}.", "",
                  f"**Version policy:** {source['version_policy']}", "",
                  "**Lesson references:** " + (", ".join(lesson_link(lid) for lid in used_by) or "Module background reading.") + "", ""]
    files["SOURCES.md"] = "\n".join(lines)

    lines = ["# Prerequisite-aware learning path", "",
             "This is one valid full learning sequence. Module numbers are catalogue IDs, not a mandatory teaching order. Evaluation (M25) and security (M30) appear early and recur in practical work. The advanced M34 and M36 branches can be skipped on the application-engineering route because no downstream module requires them.", "",
             "Entry readiness: basic programming literacy and comfort editing files/running a terminal. M02 supplies the Python, NumPy, pandas, plotting, API, concurrency and SQL bridge; M03 supplies the mathematical bridge. No prior LLM application experience is assumed. Experienced learners may demonstrate prerequisite outcomes rather than repeat lessons.", "",
             "| Sequence | Module | Required earlier modules, including lesson-specific gates |", "| --- | --- | --- |"]
    for step, mid in enumerate(curriculum["recommended_module_order"], 1):
        deps = sorted({p[:3] for l in module_map[mid]["lessons"] for p in l["prerequisites"] if p[:3] != mid})
        lines.append(f"| {step} | {module_link(mid)} | {', '.join(deps) or 'Entry readiness'} |")
    lines += ["", "## Reading the dependency contract", "",
              "Each lesson lists direct prerequisites. Prerequisites are transitive: a lesson depends on the knowledge behind its prerequisites as well. Within a module, lessons form a sequence. Additional gates are explicit at the lesson where they apply; for example, M20-L02 requires security lesson M30-L02 before tool-authority design.", "",
              "Reading links are not extra prerequisite modules. A source may introduce an idea earlier at a conceptual level and support a deeper treatment later. All 42 modules are retained in the complete plan, including advanced branches.", "",
              "## Routes through the same catalogue", "",
              "- **Predictive ML engineering:** M01–M06 → M25/M30 → M27–M29 → M31 → M35 → M40. Follow additional dependencies in those modules. M29-L05–L08 form the tracking, registry, scoring and retraining lifecycle. Advanced LLM lessons are not prerequisites for starting the foundational data/ML work.",
              "- **Application engineering:** follow the full sequence and treat M34/M36 as optional advanced branches; use small-model or replay alternatives for compute-heavy exercises.",
              "- **Interview preparation:** begin with the diagnostic questions in the relevant modules; follow prerequisite links for weak answers, then use M42 as the final rehearsal. M42 is not a replacement for the core material.",
              "- **Production reference:** enter at a concrete problem such as M17 (RAG), M21 (agent recovery), M28 (reliability) or M35 (serving); check the prerequisite contract and completion criteria before applying the pattern.", ""]
    files["LEARNING_PATH.md"] = "\n".join(lines)

    lines = ["# Approved-scope coverage map", "",
             f"This maps all 42 modules to {len(lessons)} lesson units, including 20 additions from the October 13 coverage review. It establishes coverage of the agreed curriculum, not exhaustive coverage of every research topic in AI. Each linked unit contains topics, outcomes, readings, interview guidance and an exercise.", "",
             "| Module | Lesson-level coverage |", "| --- | --- |"]
    for module in modules:
        covered = "; ".join(f"{lesson_link(l['id'])}: {l['title']}" for l in module["lessons"])
        lines.append(f"| {module_link(module['id'])} | {covered} |")
    lines += ["", "## Cross-cutting coverage", "",
              "| Concern | Primary lessons and reinforcement |", "| --- | --- |",
              "| Baselines and product value | M01, M04, M19, M32, M40 |",
              "| Evaluation before release | M03-L04, M25, M26; explicit M17-L04 and M29 gates |",
              "| Trust boundaries and human control | M01-L03, M20, M23, M30, M31, M38 |",
              "| Data rights, provenance and deletion | M06, M13, M18, M22, M31, M39 |",
              "| Tenant isolation | M13-L03, M15-L04, M22-L04, M30-L04, M41 |",
              "| Failure recovery and rollback | M09, M20, M21, M28, M29, M35, M36 |",
              "| Cost and capacity | M01-L02, M12, M24, M27-L02, M32, M35, M41 |",
              "| Research-to-production judgment | M08, M25, M33–M36, M41, M42 |", "",
              "## Scope boundaries", "",
              "The scope is AI/ML Engineering: predictive modeling and its production lifecycle alongside LLM application engineering. Coverage is planned breadth, not a claim of completed instruction or equal depth in every subfield. Robotics/control, exhaustive theoretical proofs, custom accelerator design, every cloud-provider certification, and jurisdiction-specific legal advice are outside this 42-module plan. SSM/Mamba, graph neural networks, differential privacy, federated learning and conformal prediction are explicitly deferred specialist electives. Knowledge-graph retrieval is not GNN training; governance coverage is not differential-privacy training. Advanced research topics are introduced for engineering decisions, not as a replacement for specialist research training.", "",
              "The referenced GitHub repository remains a background reference only. The approved independent catalogue, primary literature and original production scenarios govern this plan. A matching concept name is not a copied lesson or implementation.", ""]
    lines += ["## October 13 review disposition", "", "Dedicated additions preserve existing IDs and avoid stretching a ten-minute preview into a full course. All 20 added narrative lessons remain planned; the M02 data lab is a separate runnable artifact.", "", "| Review concern | Primary treatment and reinforcement |", "| --- | --- |"]
    for concern in curriculum['review_coverage']:
        lines.append(f"| {concern['concern']} | " + ', '.join(lesson_link(lid) for lid in concern['lessons']) + ' |')
    lines += ["", "See [review response](REVIEW_2026-10-13.md) for evidence, archived-content mapping and remaining delivery work.", ""]
    files["COVERAGE.md"] = "\n".join(lines)

    hours = {key: [sum(l["estimated_hours"][key][i] for l in lessons) for i in (0, 1)]
             for key in ("guided_study", "exercise")}
    edges = sum(len(l["prerequisites"]) for l in lessons)
    counts = Counter(l["status"] for l in lessons)
    lines = ["# Phase 1 validation report", "",
             "Generated from the authoritative JSON records after content validation. Run `python3 scripts/curriculum.py check` from the repository root to verify the current files match the records.", "",
             "| Check | Result |", "| --- | --- |",
             f"| Approved modules | {len(modules)} / 42 |",
             f"| Lessons with all required fields | {len(lessons)} / {curriculum['expected_lessons']} |",
             f"| Unique interview questions and answer guidance | {len(lessons)} |",
             f"| Unique exercise briefs with acceptance criteria | {len(lessons)} |",
             f"| Source records | {len(sources)} |",
             f"| Direct prerequisite edges | {edges} |",
             "| Unknown prerequisites / dependency cycles | 0 / 0 |",
             "| Unknown source IDs / invalid source URL syntax | 0 / 0 |",
             "| Learning path | All modules once; every dependency precedes its dependent lesson |",
             f"| Lesson status | {counts['planned']} planned; {counts['preview']} previews; {counts['complete']} full-contract complete |", "",
             "## Effort assumptions", "",
             f"Guided study totals approximately {hours['guided_study'][0]}–{hours['guided_study'][1]} learner hours. Exercises add {hours['exercise'][0]}–{hours['exercise'][1]} hours if all are completed. These broad estimates describe learner effort, not an implementation commitment; prior knowledge and compute choices materially affect them.", "",
             "## What was reviewed", "",
             "The author reviewed the module-to-lesson mapping for conceptual gaps and repeated exercises, separated metrics from infrastructure health, added early security/evaluation gates, and provided resource alternatives for compute-heavy topics. Every lesson has an original scenario or engineering artifact and explicit review evidence.", "",
             "## Limits of this report", "",
             "The checker validates IDs, field completeness, unique questions/exercises, source references, dependency cycles, learning order, local Markdown targets, explicit anchors and generated-file consistency. It does not prove conceptual correctness, universal AI coverage, external link availability, legal compliance or working production systems. Exercise fixtures, solutions, measured benchmarks, learner pilots and independent technical review belong to later phases.", ""]
    usage = Counter(sid for lesson in lessons for sid in lesson['sources'])
    lines += ["## Source and delivery audit", "", f"Lessons with one source: {sum(len(l['sources']) == 1 for l in lessons)}. EVAL references: {usage['EVAL']}; NIST references: {usage['NIST']}. A focused specification can legitimately be a single source; source count alone is not evidence quality.", "", "Effort ranges were reviewed per lesson against its exercise on October 13. They remain editorial estimates, not validated timings. Every record contains its work basis, assumptions and calibration requirement.", "", "[Per-lesson delivery inventory](DELIVERY.md) · [Review response](REVIEW_2026-10-13.md)", ""]
    files["AUDIT.md"] = "\n".join(lines)
    delivery_lines = ["# Lesson delivery inventory", "", "Generated from curriculum.json and checked against the preview manifest. A tested engine is an executable mechanism, not proof that the full production exercise or nine-part lesson contract is complete.", "", "- 3 specialist browser engines: vector similarity, RAG evidence flow and crash recovery.", "- 3 additional lessons use a shared tested numerical calculator: M03-L02, M04-L03 and M05-L02. These are six engine-backed preview lessons across four runtime families, not six full production labs.", "- The original NumPy/pandas/plotting CPU lab supports three planned M02 lessons. It is a runnable artifact, not three authored lessons.", "- Illustrated cases and learner starters do not satisfy executable-artifact acceptance by themselves.", "", "| Lesson | Narrative status | Interaction | Artifact | Full contract |", "| --- | --- | --- | --- | --- |"]
    for lesson in lessons:
        d = lesson['delivery']
        delivery_lines.append(f"| {lesson_link(lesson['id'])} | {lesson['status']} | {d['interaction']} | {d['artifact']} | {d['full_contract']} |")
    files['DELIVERY.md'] = '\n'.join(delivery_lines) + '\n'
    return files


def check_local_links():
    errors = []
    paths = [ROOT / "README.md", *BASE.rglob("*.md")]
    for path in paths:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("mailto:"):
                continue
            target_path, _, anchor = target.partition("#")
            destination = (path.parent / target_path).resolve() if target_path else path
            if not destination.is_file():
                errors.append(f"Broken local link in {path.relative_to(ROOT)}: {target}")
                continue
            if anchor:
                content = destination.read_text()
                headings = re.findall(r"^#+\s+(.+)$", content, flags=re.MULTILINE)
                slugs = {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}
                explicit = set(re.findall(r'<a id="([^"]+)"', content))
                if anchor not in slugs | explicit:
                    errors.append(f"Missing anchor in {path.relative_to(ROOT)}: {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["render", "check"])
    args = parser.parse_args()
    try:
        curriculum, sources = load()
        errors = validate(curriculum, sources)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        raise SystemExit(f"Invalid curriculum input: {exc}") from exc
    if errors:
        raise SystemExit("\n".join(errors))
    expected = render(curriculum, sources)
    if args.command == "render":
        for relative, content in expected.items():
            path = BASE / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        print(f"Rendered {len(expected)} curriculum documents.")
    else:
        for relative, content in expected.items():
            path = BASE / relative
            if not path.exists() or path.read_text() != content:
                errors.append(f"Missing or stale generated document: {relative}")
        expected_modules = {BASE / name for name in expected if name.startswith("modules/")}
        for path in (BASE / "modules").glob("*.md"):
            if path not in expected_modules:
                errors.append(f"Unexpected module document: {path.name}")
        errors.extend(check_local_links())
        if errors:
            raise SystemExit("\n".join(errors))
        print(f"PASS: {len(curriculum['modules'])} modules, {sum(len(m['lessons']) for m in curriculum['modules'])} lessons, {len(sources['sources'])} sources; prerequisite graph, learning order, content completeness, local links and generated documents are valid.")


if __name__ == "__main__":
    main()
