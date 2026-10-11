# Sample lesson: When similarity changes its mind

An original implementation of **M03-L01 — Reason with vectors**, using Larnix's visual teaching direction. This is a reviewable lesson prototype, not the full learning platform.

## Open the lesson

Open `index.html` in a browser, or serve this directory from the repository root:

```bash
python3 -m http.server 8773 --bind 127.0.0.1 --directory samples/vector-similarity
```

Then visit `http://127.0.0.1:8773/`. The lesson uses local HTML, CSS and JavaScript with no build step, model API or account. The two further-reading links are external. Check progress lasts for the current page session and resets on reload.

## What works

- Original story, worked arithmetic, optional explanations of normalization/projections and matrix shapes.
- Draggable query/document vectors and keyboard-accessible coordinate inputs.
- Dot product versus cosine rankings, normalization, projection overlay and presets.
- Explicit zero-vector handling, ties, negative scores and invalid-input feedback.
- Three checks with explanation, completion feedback and retry.
- Production assignment with a downloadable Python scaffold and expected answers.
- Interview answer guide, dark/light themes, narrow-screen layout and static explanation if JavaScript is unavailable.

The Python file is deliberately a learner starter with TODOs. It is not presented as a completed solution. The browser's arithmetic implementation is complete and independently checked against hand-calculated fixtures.

## Verification

With Node.js available:

```bash
node --test samples/vector-similarity/tests/vector-math.test.cjs
node --check samples/vector-similarity/lesson.js
```

The tests cover ranking reversal, normalization, scale invariance, zero/negative scores, projection and invalid dimensions/values. Browser review covers interactions, feedback/reset, keyboard fields and layouts at 390px, the default preview width and 1440px. This does not replace a full accessibility audit or learner usability study.

## Files

- `index.html`: complete lesson content and semantic controls.
- `styles.css`: original responsive visual treatment.
- `vector-math.js`: dependency-free numerical functions used by the lesson and tests.
- `lesson.js`: interaction, ranking, feedback and theme behavior.
- `exercise.py`: original five-document learner scaffold.

The reference sites informed teaching direction and concepts. No reference implementation, assets or course content were copied.
