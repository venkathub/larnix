"""Render original foundation lesson notes with the shared notebook learning flow.

Content stays in reviewed JSON; generated HTML includes the complete lesson even
without JavaScript. Only the case explorer and saved checks need the runtime.
"""
from datetime import date
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_notes():
    notes = {}
    for path in sorted((ROOT / 'samples/foundations').glob('m*.json')):
        for item in json.loads(path.read_text()):
            if item['id'] in notes:
                raise ValueError(f'Duplicate foundation lesson: {item["id"]}')
            notes[item['id']] = item
    return notes


def validate_notes(notes, curriculum):
    """Reject incomplete coverage, misleading chart scales and broken checks."""
    plans = {l['id']: l for m in curriculum['modules'] for l in m['lessons']}
    for lesson_id, note in notes.items():
        if lesson_id not in plans:
            raise ValueError(f'Unknown lesson {lesson_id}')
        required = ['orientation', 'idea', 'example', 'trap']
        if not all(isinstance(note.get(k), str) and note[k].strip() for k in required):
            raise ValueError(f'{lesson_id}: missing introductory content')
        if len(note['story']) < 2 or len(note['mechanism']) != 3 or len(note['sketch']) != 3:
            raise ValueError(f'{lesson_id}: incomplete teaching sequence')
        if len(note['transfer']) != 2 or any(not t['question'] or not t['answer'] for t in note['transfer']):
            raise ValueError(f'{lesson_id}: incomplete transfer practice')
        if len(note['checks']) != 3:
            raise ValueError(f'{lesson_id}: three checks required')
        for q in note['checks']:
            if len(q['options']) != 3 or type(q['answer']) is not int or q['answer'] not in range(3) or not q['explanation']:
                raise ValueError(f'{lesson_id}: invalid check')
        topics = [t['title'] for t in note['topics']]
        if set(topics) != set(plans[lesson_id]['topics']) or len(topics) != len(set(topics)):
            raise ValueError(f'{lesson_id}: topic notes must cover the approved scope exactly')
        lab = note['lab']
        if len(lab['scenarios']) != 3 or not lab['question'] or not lab['limitation']:
            raise ValueError(f'{lesson_id}: incomplete case explorer')
        scales = set()
        for case in lab['scenarios']:
            if len(case['steps']) != 3 or len(case['evidence']) != 3 or not case['result'] or not case['why']:
                raise ValueError(f'{lesson_id}: incomplete illustrated case')
            if not 2 <= len(case['bars']) <= 3:
                raise ValueError(f'{lesson_id}: quantity comparison required')
            for bar in case['bars']:
                if not isinstance(bar['value'], (int, float)) or not isinstance(bar['max'], (int, float)) or not 0 <= bar['value'] <= bar['max'] or bar['max'] <= 0:
                    raise ValueError(f'{lesson_id}: invalid bar value/scale')
                scales.add(bar['max'])
        if len(scales) != 1:
            raise ValueError(f'{lesson_id}: use a consistent scale across illustrated cases')
        if not note['sources'] or any(not s['url'].startswith('https://') for s in note['sources']):
            raise ValueError(f'{lesson_id}: primary sources required')
        if 'sources_reviewed_on' in note:
            reviewed_on = note['sources_reviewed_on']
            try:
                if date.fromisoformat(reviewed_on).isoformat() != reviewed_on:
                    raise ValueError('noncanonical date')
            except (TypeError, ValueError) as error:
                raise ValueError(f'{lesson_id}: sources_reviewed_on must be a valid YYYY-MM-DD date') from error
        if len(note['practice']['steps']) != 3 or not note['practice']['starter'].strip():
            raise ValueError(f'{lesson_id}: missing practice starter')


def e(value):
    return escape(str(value), quote=True)


def paragraphs(items):
    return ''.join(f'<p>{e(item)}</p>' for item in items)


def recall(case, summary):
    return f'<p>{e(case["question"])}</p><details class="recall-answer"><summary>{e(summary)}</summary><p>{e(case["answer"])}</p></details>'


def stages(labels):
    return '<ol class="case-stages" aria-label="Follow the mechanism">' + ''.join(
        f'<li><svg aria-hidden="true" viewBox="0 0 220 90" preserveAspectRatio="none"><path d="M5 8 Q102 2 213 7 L215 82 Q101 88 6 82 Z"/></svg><span class="stage-number">{i+1:02}</span><strong>{e(label)}</strong></li>'
        for i, label in enumerate(labels)) + '</ol>'


def evidence(rows):
    return '<dl class="case-evidence">' + ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in rows) + '</dl>'


def bars(items):
    return '<div class="case-bars" aria-label="Compare the quantities">' + ''.join(
        f'<div class="case-bar"><div><span>{e(b["label"])}</span><strong>{e(b["value"])}</strong></div><span class="bar-track" aria-hidden="true"><span style="width:{100*b["value"]/b["max"]:.4f}%"></span></span></div>' for b in items) + '</div>'


def mini_lab(lesson_id):
    if lesson_id == 'M04-L03':
        return '''<details class="lesson-extra live-math"><summary>Try your own threshold · computed locally</summary><div class="extra-body"><p>Use the same six tickets. Predict how many will be reviewed before moving the cutoff.</p><label for="threshold-input">Alert when score ≥ <output id="threshold-value">0.8</output></label><input id="threshold-input" aria-label="Alert threshold" type="range" min="0" max="1" step="0.1" value="0.8"><p id="live-result" role="status" aria-live="polite"></p><ol id="score-tickets" class="score-tickets"></ol><p>A higher score sorts ahead of a lower score; these six cases cannot establish calibration.</p></div></details>'''
    if lesson_id not in {'M03-L02', 'M05-L02'}:
        return ''
    points = ' '.join(f'{45+(w+3)*30:.1f},{230-(w-3)**2*5:.1f}' for w in (i/10 for i in range(-30, 91)))
    return f'''<details class="lesson-extra live-math"><summary>Take a gradient step · computed locally</summary><div class="extra-body"><p>Loss = (w − 3)². The slope is 2(w − 3). Predict the direction before stepping.</p><div class="math-controls"><label>Learning rate <select id="rate-input" aria-label="Learning rate"><option>0.1</option><option selected>0.25</option><option>0.5</option><option>1</option><option>1.1</option><option>1.2</option></select></label><button type="button" id="step-learning">Take one step →</button><button type="button" id="reset-learning">Reset weight ↺</button></div><p id="live-result" role="status" aria-live="polite"></p><svg class="descent-chart" viewBox="0 0 450 280" role="img" aria-labelledby="descent-title descent-desc"><title id="descent-title">Gradient descent on a quadratic loss</title><desc id="descent-desc">Start at weight zero with loss nine.</desc><path class="plot-axis" d="M45 30 V230 H415"/><polyline class="loss-curve" points="{points}"/><circle id="descent-point" cx="135" cy="185" r="7"/><text x="18" y="24">loss</text><text x="409" y="254">w</text><text x="34" y="255">−3</text><text x="132" y="255">0</text><text x="220" y="255">3</text><text x="399" y="255">9</text><text x="233" y="218">minimum</text></svg><p id="descent-range"></p><p>This exact toy calculation demonstrates update size; real training losses need not have this shape.</p></div></details>'''


def render(note, lesson, module):
    title = e(lesson['title'])
    first = note['lab']['scenarios'][0]
    check_html = ''
    for i, q in enumerate(note['checks']):
        options = ''.join(f'<button type="button" data-answer="{j}">{e(text)}</button>' for j, text in enumerate(q['options']))
        check_html += f'<fieldset class="quiz" data-quiz="check{i+1}"><legend>{e(q["question"])}</legend><div class="answers stacked">{options}</div><p class="feedback" aria-live="polite">Choose an answer, then explain the reason.</p></fieldset>'
    topic_html = ''.join(f'<section class="topic-note"><h3>{e(t["title"])}</h3><p>{e(t["explanation"])}</p></section>' for t in note['topics'])
    sources = ''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["title"])} ↗</a></li>' for s in note['sources'])
    steps = ''.join(f'<li>{e(s)}</li>' for s in note['practice']['steps'])
    acceptance = ''.join(f'<li>{e(s)}</li>' for s in lesson['production_exercise']['acceptance'])
    signals = ''.join(f'<li>{e(s)}</li>' for s in lesson['interview']['strong_answer_signals'])
    scenario_buttons = ''.join(f'<button type="button" data-case="{i}" aria-pressed="{str(i==0).lower()}">{e(s["label"])}</button>' for i, s in enumerate(note['lab']['scenarios']))
    artifact_link = ''
    if lesson.get('delivery', {}).get('artifact') == 'runnable_data_lab':
        artifact_link = '<p><a href="../../labs/data-foundations.zip" download>Download runnable data lab + README</a></p>'
    prereqs = ', '.join(lesson['prerequisites']) or 'No earlier lesson required; read the definitions below.'
    return f'''<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(lesson['outcome'])}"><title>{title} · Larnix</title>
<link rel="stylesheet" href="../vector-similarity/styles.css"><link rel="stylesheet" href="../shared/quick-lesson.css"><link rel="stylesheet" href="foundation.css"><link rel="stylesheet" href="../shared/notebook.css"><link rel="preload" href="../shared/fonts/PatrickHand-Regular.ttf" as="font" type="font/ttf" crossorigin>
<script src="lesson-data.js" defer></script><script src="../shared/lesson-ui.js" defer></script><script src="lesson.js" defer></script><script src="mini-math.js" defer></script><script src="mini-lab.js" defer></script><script src="../shared/notebook.js" defer></script></head>
<body class="foundation-lesson" id="top"><a class="skip" href="#main">Skip to lesson</a><header class="topbar"><a class="brand" href="#top" aria-label="Larnix lesson home"><span class="brand-mark" aria-hidden="true">L</span>larnix.</a><span class="breadcrumb">Foundations / {e(module['id'])}</span><div class="header-actions"><span id="check-progress" class="progress-label" aria-live="polite">0 / 3 checks correct</span><button id="theme-toggle" type="button" class="quiet">Dark mode ◑</button></div></header>
<div class="page-shell"><aside class="lesson-nav" aria-label="Lesson contents"><p class="eyebrow">{e(module['id'])} · FOUNDATIONS</p><p class="nav-title">{title}</p><nav><a href="#revision">↺ Quick revision</a><a href="#story">2 min · See the idea</a><a href="#lab">4 min · Try three cases</a><a href="#mechanism">3 min · Explain &amp; check</a><a href="#takeaways">1 min · Recall it</a><a href="#deep-dive">＋ All topic notes</a><a href="#production">＋ Production practice</a><a href="#interview">＋ Interview prep</a></nav></aside>
<main id="main"><header class="revision-title"><div class="hero-kicker"><span class="section-tag">{e(lesson['id'])}</span><span>FOUNDATION FIELD NOTES</span></div><h1>{title}</h1><p class="lesson-orientation">{e(note['orientation'])}</p></header>
<section class="revision-sheet revision-first" id="revision" aria-label="Quick revision sheet"><div class="revision-idea"><span class="note-index" aria-hidden="true">01</span><div><h2>The idea in one sentence</h2><p>{e(note['idea'])}</p></div></div><div class="revision-board"><div class="revision-picture"><h2>02 · Picture the mechanism</h2>{stages(note['sketch'])}<p class="sketch-caption">{e(note['example'])}</p></div><div class="revision-notes"><div class="exam-trap"><h2>03 · The exam trap</h2><p>{e(note['trap'])}</p></div><div class="recall-card"><h2>04 · Apply it to a new case</h2>{recall(note['transfer'][0], 'Check your reasoning')}</div></div></div><nav class="revision-actions" aria-label="Choose how to learn"><a class="primary" href="#story">Teach me step by step ↓</a><a class="text-link" href="#lab">Try the lab ↗</a></nav></section>
<details class="study-route"><summary>The study route · about 10 minutes</summary><p class="pace-note">2 minutes to see the idea, 4 to explore the cases, 3 to explain and check, 1 to recall. This is a suggested introduction to the central concept. Topic notes, coding and production practice need extra time.</p><p>Prerequisites: {e(prereqs)}</p></details>
<section class="reading section" id="story"><p class="section-number">01 / SEE THE IDEA · 2 MIN</p><h2>Start with a real decision.</h2>{paragraphs(note['story'])}<p class="core-rule">{e(lesson['outcome'])}</p></section>
<section class="section lab-section" id="lab" aria-labelledby="lab-title"><div class="section-heading"><div><p class="section-number">02 / TRY THREE CASES · 4 MIN</p><h2 id="lab-title">Change the case.<br>Follow the evidence.</h2><p class="fixture-label">Illustrated fixtures · no live model or service</p></div></div><div class="lab-guide"><p><strong>Your question:</strong> {e(note['lab']['question'])}</p><p>Predict first. Then choose 1 → 2 → 3 and explain what changed.</p></div><div class="foundation-lab"><div class="scenario-controls" role="group" aria-label="Illustrated cases">{scenario_buttons}</div><div class="lab-feedback" role="status" aria-live="polite" aria-atomic="true"><p class="feedback-label">What happened</p><p id="case-result">{e(first['result'])}</p><p class="feedback-label">Why · what to inspect</p><p id="case-why">{e(first['why'])}</p></div><div class="case-visual" id="case-visual">{stages(first['steps'])}{bars(first['bars'])}{evidence(first['evidence'])}</div></div><p class="lab-caption">{e(note['lab']['limitation'])}</p>{mini_lab(lesson['id'])}<noscript><p class="callout">The first case is shown above. Case switching, calculators and saved checks need JavaScript; all explanations and practice instructions remain readable.</p></noscript></section>
<section class="reading section" id="mechanism"><p class="section-number">03 / EXPLAIN &amp; CHECK · 3 MIN</p><h2>What changed—and why?</h2>{paragraphs(note['mechanism'])}{check_html}</section>
<section class="reading section" id="takeaways"><p class="section-number">04 / RECALL IT · 1 MIN</p><h2>Can you use the idea elsewhere?</h2><div class="transfer-check"><h3>Explain before revealing</h3>{recall(note['transfer'][1], 'Check the new case')}</div><p class="core-rule">{e(note['idea'])}</p><div class="completion"><div><p class="eyebrow">YOUR QUICK CHECKS</p><h3 id="completion-title">0 of 3 answered correctly</h3><p id="completion-text"></p></div><button id="reset-checks" class="quiet" type="button">Retry all checks</button></div><div id="recap" class="takeaway" hidden><p>Explain the diagram with the answer hidden. Correct checks are practice feedback, not proof of mastery.</p></div></section>
<div class="optional-reading" id="deep-dive"><p class="eyebrow">ALL TOPIC NOTES · EXTRA STUDY</p><details class="lesson-extra"><summary>Open the topic notes<span aria-hidden="true">＋</span></summary><div class="extra-body reading">{topic_html}<h3>Primary sources</h3><p>Authoring references rechecked {e(note.get("sources_reviewed_on", "October 12, 2026"))}. Versioned pages apply to their stated versions; package behavior may differ.</p><ul class="source-list">{sources}</ul></div></details></div>
<section class="section" id="production"><details class="lesson-extra"><summary>Production practice · beyond the ten-minute core<span aria-hidden="true">＋</span></summary><div class="extra-body reading"><h2>Build the evidence.</h2><p>{e(lesson['production_exercise']['brief'])}</p><ol>{steps}</ol>{artifact_link}<h3>Starter fixture / worksheet</h3><pre class="practice-code"><code>{e(note['practice']['starter'])}</code></pre><a class="text-link" href="starter.txt" download>Download starter text ↓</a><h3>Acceptance evidence</h3><ul>{acceptance}</ul><p>Keep the input, versioned output, failure case and decision note together. Completing this exercise requires your implementation; switching the illustrated cases does not complete it.</p></div></details></section>
<section class="section" id="interview"><details class="lesson-extra"><summary>Interview practice<span aria-hidden="true">＋</span></summary><div class="extra-body reading"><h2>{e(lesson['interview']['question'])}</h2><p>Give your own answer before opening the prompts.</p><details class="recall-answer"><summary>What a strong answer should address</summary><ul>{signals}</ul><p>Explain the mechanism, use a concrete example, and name a verification method and limitation.</p></details></div></details></section>
<footer class="lesson-footer"><p>Original Larnix lesson · fictional teaching fixtures · optional practice runs on your own machine.</p><a href="../../#/catalog">Return to curriculum ↗</a></footer></main></div></body></html>'''
