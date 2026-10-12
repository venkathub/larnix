#!/usr/bin/env python3
"""Build the local Larnix platform from original curriculum and lesson sources."""
from pathlib import Path
import json
import shutil
import hashlib
import re
from urllib.parse import urlsplit
from render_foundations import load_notes, render as render_foundation, validate_notes

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'


def build():
    curriculum = json.loads((ROOT / 'docs/curriculum/curriculum.json').read_text())
    sources = json.loads((ROOT / 'docs/curriculum/sources.json').read_text())['sources']
    previews = json.loads((ROOT / 'web/lessons.json').read_text())
    foundation_notes = load_notes()
    validate_notes(foundation_notes, curriculum)
    lesson_ids = {lesson['id'] for module in curriculum['modules'] for lesson in module['lessons']}
    if not set(previews) <= lesson_ids:
        raise ValueError('Preview manifest contains unknown lessons')
    if OUT.is_symlink():
        raise ValueError('Build output must not be a symlink')
    OUT.mkdir(exist_ok=True)
    (OUT / '.nojekyll').touch()
    assets = OUT / 'assets'
    assets.mkdir(exist_ok=True)
    for name in ['app.js', 'app.css', 'roadmap.css', 'catalog.js', 'progress.js', 'lesson-shell.js']:
        shutil.copy2(ROOT / 'web' / name, assets / name)
    shutil.copy2(ROOT / 'samples/shared/lesson-ui.js', assets / 'lesson-ui.js')
    for name in ['quick-lesson.css', 'notebook.css', 'notebook.js']:
        shutil.copy2(ROOT / 'samples/shared' / name, assets / name)
    shutil.copytree(ROOT / 'samples/shared/fonts', assets / 'fonts', dirs_exist_ok=True)
    shutil.copy2(ROOT / 'samples/vector-similarity/styles.css', assets / 'lesson.css')
    shutil.copy2(ROOT / 'web/index.html', OUT / 'index.html')
    data = {'modules': curriculum['modules'], 'tracks': curriculum['tracks'],
            'order': curriculum['recommended_module_order'], 'sources': sources, 'previews': previews}
    (assets / 'data.js').write_text('window.LarnixData = ' + json.dumps(data, ensure_ascii=False).replace('<', '\\u003c') + ';\n')
    for lesson_id, preview in previews.items():
        source = ROOT / 'samples' / preview['directory']
        target = OUT / 'lessons' / lesson_id
        target.mkdir(parents=True, exist_ok=True)
        for path in source.iterdir():
            if path.is_file() and path.suffix in ['.js', '.css', '.py', '.json']:
                if preview.get('format') == 'foundation' and path.suffix == '.json':
                    continue  # Emit only this lesson's notes in lesson-data.js below.
                shutil.copy2(path, target / path.name)
        if preview.get('format') == 'foundation':
            module = next(m for m in curriculum['modules'] if any(l['id'] == lesson_id for l in m['lessons']))
            lesson = next(l for l in module['lessons'] if l['id'] == lesson_id)
            note = foundation_notes[lesson_id]
            document = render_foundation(note, lesson, module)
            (target / 'lesson-data.js').write_text('window.FoundationLesson = ' + json.dumps(note, ensure_ascii=False).replace('<', '\\u003c') + ';\n')
            (target / 'starter.txt').write_text(note['practice']['starter'] + '\n')
        else:
            document = (source / 'index.html').read_text()
        document = document.replace('<html lang="en"', f'<html data-platform-lesson="{lesson_id}" lang="en"')
        document = document.replace('href="styles.css"', 'href="../../assets/lesson.css"')
        document = document.replace('href="../vector-similarity/styles.css"', 'href="../../assets/lesson.css"')
        document = document.replace('src="../shared/lesson-ui.js"', 'src="../../assets/lesson-ui.js"')
        document = document.replace('href="../shared/quick-lesson.css"', 'href="../../assets/quick-lesson.css"')
        document = document.replace('href="../shared/fonts/PatrickHand-Regular.ttf"', 'href="../../assets/fonts/PatrickHand-Regular.ttf"')
        document = document.replace('src="../shared/notebook.js"', 'src="../../assets/notebook.js"')
        document = document.replace('<link rel="stylesheet" href="../shared/notebook.css">', '')
        for other_id, other in previews.items():
            document = document.replace(f'href="../{other["directory"]}/"', f'href="../{other_id}/"')
        document = document.replace('<script ', '<script src="../../assets/progress.js" defer></script><script src="../../assets/data.js" defer></script><script ', 1)
        document = document.replace('</head>', '<link rel="stylesheet" href="../../assets/app.css"><link rel="stylesheet" href="../../assets/notebook.css"><script src="../../assets/lesson-shell.js" defer></script></head>')
        shell = '<div id="course-shell" class="course-shell" aria-label="Course navigation and progress"></div>'
        document = document.replace('<main id="main">', '<main id="main">'+shell)
        document = document.replace('Checks track this page session only.', 'Checks are saved in this browser when storage is available.')
        document = document.replace('This is a standalone sample. The remaining lessons are planned.', 'This interactive preview is part of the Larnix curriculum. The remaining lessons are planned.')
        document = document.replace('That lesson is planned. This is the second standalone sample.', 'That lesson is planned. Return to the catalogue to explore its lesson plan.')
        (target / 'index.html').write_text(document)
    # Content-version assets so a rebuilt page cannot reuse an earlier lesson runtime.
    for page in OUT.rglob('*.html'):
        def version_asset(match):
            ref = match.group(2)
            url = urlsplit(ref)
            asset = page.parent / url.path
            if url.scheme or asset.suffix not in {'.js', '.css'} or not asset.is_file():
                return match.group(0)
            version = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
            return f'{match.group(1)}="{url.path}?v={version}"'
        page.write_text(re.sub(r'(src|href)="([^"]+)"', version_asset, page.read_text()))
    print(f'Built {len(curriculum["modules"])} modules, {len(lesson_ids)} lesson plans and {len(previews)} interactive previews → {OUT}')


if __name__ == '__main__':
    build()
