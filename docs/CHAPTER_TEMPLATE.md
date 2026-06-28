---
# ── Larnix chapter front-matter (all fields required) ───────────────────────────
title: "<Chapter title — one concept, plain language>"
module: "M<NN> — <module name>"
chapter: <NN>                     # order within the module
difficulty: "beginner"            # beginner | intermediate | advanced
prereqs: ["M<NN> Ch<NN> — <name>"] # chapters/skills assumed; [] if none
learning_objectives:              # 2–4, each a verb the reader can do after this
  - "Explain <…> in plain language"
  - "Implement <…>"
  - "Decide when to use <…> vs <…>"
compute: "browser"                # browser | colab | gpu
status: "stable"                  # stable | frontier
last_reviewed: "YYYY-MM-DD"
est_minutes: 25                   # realistic time to read + run
# ── Optional: spaced-repetition cards seeded from the Key Takeaways (P0-D3) ──
# review_cards:
#   - id: <slug>                  # optional, unique within the chapter
#     q: "<question a learner can self-test>"
#     a: "<concise answer>"
# ───────────────────────────────────────────────────────────────────────────────
---

<!--
  HOW TO USE THIS TEMPLATE (delete this comment in the final chapter):
  - Fill every section below in order. Do not remove or reorder sections.
  - Obey STYLE_GUIDE.md: beginner-first, conversational, clarity over cleverness,
    no banned words ("simply", "just", "obviously", "trivially", hype terms).
  - Every code block must actually run. Show its output.
  - If the chapter needs more than ~3,000 words / 25 min, split it into two.
-->

<!--
  LARNIX AUTHORING MECHANISMS (proven in P0 — see DECISIONS D0005–D0013):

  • Badge row (put right under the title):
      {{< badge difficulty=beginner >}} {{< badge compute=browser >}} {{< badge status=stable >}}

  • Browser chapters (compute: browser) run Python in the browser via Pyodide.
    Use `{pyodide}` code cells, and add this to the front-matter ABOVE
    (live-html is a distinct format that does NOT inherit the project theme, and
    its theme path is relative to THIS file — modules/<NN>-slug/ is two levels
    down, hence ../../theme):

        format:
          live-html:
            theme:
              light: [cosmo, ../../theme/larnix.scss]
              dark:  [darkly, ../../theme/larnix-dark.scss]
            toc: true
        execute:
          enabled: false   # {pyodide} cells run in the browser, never at render

    Each browser chapter also ships a CI "twin" `.ipynb` (same front-matter) that
    runs the worked example + exercise solutions under CPython (R10 gate, D0010).

  • GPU/colab chapters: add an Open-in-Colab button with {{< colab path/to.ipynb >}}.

  • Key Takeaways box:  ::: {.key-takeaways}  ### Key Takeaways  1. … :::

  • Auto-graded exercise: paste the grader helper (lib/grader.py) into a
    `#| edit: false` setup cell, then call run_tests([(label, got, expected), …]).

  • End-of-chapter quiz: author quiz.yml beside the chapter, mount with
    {{< quiz quiz.yml >}}.
-->

# <Chapter title>

## The hook
<!-- Open with a real-world analogy OR a working demo. NO definitions first.
     Earn attention in the first three sentences. Tie to the module's running example. -->

<Analogy or a 3–5 line "watch this work" demo that motivates the whole chapter.>

> By the end of this chapter you'll be able to: <one-sentence promise tied to the objectives>.

---

## The idea, in plain language
<!-- One concept. Build it up step by step. Define every new term on first use:
     plain-English meaning FIRST, then the technical name in bold. Use a picture,
     number, or concrete case before generalizing. Keep paragraphs to 2–4 sentences. -->

<Explanation.>

> 💡 Tip: <a practical shortcut, optional>
> ⚠️ Watch out: <a common mistake or footgun, optional>

---

## Let's build it (worked example)
<!-- Real, runnable code introduced in small steps with explanation between them.
     Show expected output. No secrets — read keys from env; show the free fallback. -->

```python
# Step 1 — <what this does and why>
<runnable code>
```

```
<expected output>
```

```python
# Step 2 — <next small step>
<runnable code>
```

<Walk through what just happened and what it means.>

> 🔬 Going deeper (optional): <depth a beginner can safely skip>

---

## Key Takeaways
<!-- 3–6 numbered points. The reader should be able to read ONLY this and remember the chapter. -->

> ### Key Takeaways
>
> 1. <the single most important point>
> 2. <…>
> 3. <…>

---

## Practice
<!-- 2–4 exercises, scaffolded by difficulty. Each needs an auto-grader + a hidden
     solution. Match difficulty to the chapter tier; label any stretch task. -->

### Exercise 1 — Guided (≈5 min) 🟢

<Fill-in-the-blank or one-line completion. Structure provided.>

```python
# TODO: complete the marked line(s)
<scaffolded code with a clear blank>
```

<details><summary>Show solution</summary>

```python
<reference solution>
```

<One-paragraph walkthrough of why this is the answer.>
</details>

---

### Exercise 2 — Implement (≈15 min) 🟡

<Clear spec for a function/step. Graded by the assert-based tests below.>

```python
def <name>(<args>):
    """<spec>"""
    # TODO: implement
    ...
```

```python
# Auto-grader (hidden from the learner; runs in the sandbox)
assert <name>(<input>) == <expected>
assert <…>
print("All tests passed ✅")
```

<details><summary>Show solution</summary>

```python
<reference solution>
```

</details>

---

### Exercise 3 — Stretch (optional, ≈20 min) 🔴

<Open-ended mini-task with multiple valid solutions. Graded by rubric or a loose check.>

**Rubric:** <2–3 bullet criteria for a good solution.>

<details><summary>Show one possible solution</summary>

```python
<one valid approach>
```

<Note that other approaches are fine, and what trade-offs they carry.>
</details>

---

## Where this fits / what's next
<!-- 1–2 sentences linking back to the module's running example and forward to the next chapter. -->

<Link to the next chapter and how this idea gets used later.>

## Further reading (optional)
<!-- Primary sources preferred (papers, official docs). Never invent a citation. -->
- <source>
