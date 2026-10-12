#!/usr/bin/env python3
"""Build the local Larnix platform from original curriculum and lesson sources."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'


def build():
    curriculum = json.loads((ROOT / 'docs/curriculum/curriculum.json').read_text())
    sources = json.loads((ROOT / 'docs/curriculum/sources.json').read_text())['sources']
    previews = json.loads((ROOT / 'web/lessons.json').read_text())
    lesson_ids = {lesson['id'] for module in curriculum['modules'] for lesson in module['lessons']}
    if not set(previews) <= lesson_ids:
        raise ValueError('Preview manifest contains unknown lessons')
    if OUT.is_symlink():
        raise ValueError('Build output must not be a symlink')
    OUT.mkdir(exist_ok=True)
    assets = OUT / 'assets'
    assets.mkdir(exist_ok=True)
    for name in ['app.js', 'app.css', 'catalog.js', 'progress.js', 'lesson-shell.js']:
        shutil.copy2(ROOT / 'web' / name, assets / name)
    shutil.copy2(ROOT / 'samples/shared/lesson-ui.js', assets / 'lesson-ui.js')
    shutil.copy2(ROOT / 'samples/shared/quick-lesson.css', assets / 'quick-lesson.css')
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
                shutil.copy2(path, target / path.name)
        document = (source / 'index.html').read_text()
        document = document.replace('<html lang="en"', f'<html data-platform-lesson="{lesson_id}" lang="en"')
        document = document.replace('href="styles.css"', 'href="../../assets/lesson.css"')
        document = document.replace('href="../vector-similarity/styles.css"', 'href="../../assets/lesson.css"')
        document = document.replace('src="../shared/lesson-ui.js"', 'src="../../assets/lesson-ui.js"')
        document = document.replace('href="../shared/quick-lesson.css"', 'href="../../assets/quick-lesson.css"')
        for other_id, other in previews.items():
            document = document.replace(f'href="../{other["directory"]}/"', f'href="../{other_id}/"')
        document = document.replace('<script ', '<script src="../../assets/progress.js" defer></script><script src="../../assets/data.js" defer></script><script ', 1)
        document = document.replace('</head>', '<link rel="stylesheet" href="../../assets/app.css"><script src="../../assets/lesson-shell.js" defer></script></head>')
        shell = '<div id="course-shell" class="course-shell" aria-label="Course navigation and progress"></div>'
        document = document.replace('<main id="main">', '<main id="main">'+shell)
        document = document.replace('Checks track this page session only.', 'Checks are saved in this browser when storage is available.')
        document = document.replace('This is a standalone sample. The remaining lessons are planned.', 'This interactive preview is part of the Larnix curriculum. The remaining lessons are planned.')
        document = document.replace('That lesson is planned. This is the second standalone sample.', 'That lesson is planned. Return to the catalogue to explore its lesson plan.')
        (target / 'index.html').write_text(document)
    print(f'Built {len(curriculum["modules"])} modules, {len(lesson_ids)} lesson plans and {len(previews)} interactive previews → {OUT}')


if __name__ == '__main__':
    build()
