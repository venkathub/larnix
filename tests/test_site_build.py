"""Verify generated lesson assets and links, independently of the browser."""
from html.parser import HTMLParser
from copy import deepcopy
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urljoin
import json
import hashlib
from zipfile import ZipFile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_site import build
from render_foundations import load_notes, render as render_foundation
from curriculum import render as render_curriculum


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.refs = []
        self.scripts = []
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ['src', 'href']:
            if key in attrs:
                self.refs.append(attrs[key])
        if tag == 'script' and 'src' in attrs:
            self.scripts.append(urlsplit(attrs['src']).path)


class SiteBuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build()

    def test_foundation_disclosures_are_scoped_without_changing_shared_styles(self):
        manifest = json.loads((ROOT / 'web/lessons.json').read_text())
        rule = '.foundation-lesson :is(#deep-dive,#production,#interview)>.lesson-extra'
        for lesson_id, entry in manifest.items():
            if entry.get('format') == 'foundation':
                with self.subTest(lesson=lesson_id):
                    css = (ROOT / 'dist/lessons' / lesson_id / 'foundation.css').read_text()
                    self.assertIn('@media(min-width:651px){\n ' + rule, css)
                    self.assertIn('max-width:calc(670px + 24px + 24px);margin-inline:auto', css)
                    self.assertIn(rule + '>.extra-body.reading{max-width:none}', css)
                    self.assertIn('.foundation-lesson #deep-dive>.eyebrow{padding-inline:24px}', css)
                    self.assertIn('.foundation-lesson :is(#production,#interview).section'
                                  '{padding:0;scroll-margin-top:100px}', css)
                    self.assertIn(rule + '{margin:0 auto 14px}', css)
                    self.assertIn('.foundation-lesson #interview.section{padding-bottom:65px}', css)
                    self.assertIn('.foundation-lesson .case-evidence .evidence-pre'
                                  '{background:var(--surface-2);border:1px solid var(--line);'
                                  'border-radius:5px;padding:10px 12px}', css)
                    self.assertIn('.foundation-lesson .case-evidence>div:has(.evidence-pre)'
                                  '{grid-template-columns:1fr;gap:4px}', css)
                    self.assertIn('.foundation-lesson .case-evidence .evidence-pre::first-line'
                                  '{font-weight:600}', css)
        # Shared stylesheet at C2's base, 1fb476f. Future shared-style changes
        # must deliberately update this snapshot; this fix is foundation-only.
        shared = (ROOT / 'dist/assets/lesson.css').read_bytes()
        self.assertEqual(hashlib.sha256(shared).hexdigest(),
                         '06aebbaefb8ab903634dbc3a193777418560e339d43d65fb735ed2f913636e85',
                         msg='dist/assets/lesson.css changed: foundation-only fixes must leave '
                             'the shared stylesheet untouched; update this snapshot deliberately '
                             'only when an intended shared-style change is reviewed.')

    def test_downloadable_labs_are_complete_and_match_tested_sources(self):
        for lab in sorted((ROOT / 'labs').iterdir()):
            if not lab.is_dir():
                continue
            with self.subTest(lab=lab.name), ZipFile(ROOT / 'dist/labs' / f'{lab.name}.zip') as archive:
                names = {path.relative_to(lab).as_posix() for path in lab.rglob('*')
                         if path.is_file() and '__pycache__' not in path.parts}
                self.assertEqual(set(archive.namelist()), {f'{lab.name}/{name}' for name in names})
                self.assertTrue({'README.md', 'requirements.txt', 'lab.py', 'test_lab.py'} <= names)
                for name in names:
                    self.assertEqual(archive.read(f'{lab.name}/{name}'), (lab / name).read_bytes())

    def test_foundation_dates_and_runnable_lab_links_and_synthetic_notice(self):
        curriculum = json.loads((ROOT / 'docs/curriculum/curriculum.json').read_text())
        manifest = json.loads((ROOT / 'web/lessons.json').read_text())
        notes = load_notes()
        for module in curriculum['modules']:
            for lesson in module['lessons']:
                lesson_id = lesson['id']
                if manifest.get(lesson_id, {}).get('format') != 'foundation':
                    continue
                with self.subTest(lesson=lesson_id):
                    file = ROOT / 'dist/lessons' / lesson_id / 'index.html'
                    text = file.read_text()
                    reviewed = date.fromisoformat(notes[lesson_id].get('sources_reviewed_on', '2026-10-12'))
                    self.assertIn(f'Authoring references rechecked {reviewed:%B} {reviewed.day}, {reviewed.year}.', text)
                    if lesson['delivery']['artifact'] not in {'runnable_data_lab', 'runnable_service_lab'}:
                        continue
                    lab = Path(lesson['delivery']['artifact_path']).parent.name
                    label = lab.removesuffix('-foundations').replace('-', ' ')
                    ref = f'../../labs/{lab}.zip'
                    self.assertIn(ref, Page(text).refs)
                    self.assertTrue((file.parent / ref).is_file())
                    self.assertIn(f'Download runnable {label} lab + README', text)
                    before_controls = text.split('class="scenario-controls"')[0]
                    self.assertIn('SYNTHETIC fixed fixtures:', before_controls)
                    self.assertIn('in the browser.', before_controls)
                    self.assertIn(lesson['delivery']['artifact_path'], text)

        # No service lesson record ships in A1. Exercise both kinds with a copy of
        # one authored lab lesson, so neither coverage nor paths depend on its ID.
        module, original = next((m, l) for m in curriculum['modules'] for l in m['lessons']
                                if l['id'] in notes and l['delivery']['artifact'] == 'runnable_data_lab')
        for kind, lab, label in [('runnable_data_lab', 'data-foundations', 'data'),
                                 ('runnable_service_lab', 'service-foundations', 'service')]:
            with self.subTest(artifact=kind):
                lesson = deepcopy(original)
                lesson['delivery'].update(artifact=kind, artifact_path=f'labs/{lab}/README.md')
                html = render_foundation(notes[lesson['id']], lesson, module)
                self.assertIn(f'../../labs/{lab}.zip', Page(html).refs)
                self.assertIn(f'Download runnable {label} lab + README', html)
                self.assertTrue((ROOT / 'dist/labs' / f'{lab}.zip').is_file())
                records = deepcopy(curriculum)
                target = next(l for m in records['modules'] for l in m['lessons'] if l['id'] == lesson['id'])
                target['delivery'] = lesson['delivery']
                markdown = render_curriculum(records, json.loads((ROOT / 'docs/curriculum/sources.json').read_text()))
                self.assertIn(f'[{label.capitalize()} foundations lab](../../../labs/{lab}/README.md)',
                              markdown[f"modules/{module['id']}.md"])

    def test_shipped_navigation_uses_teaching_order_and_respects_dependencies(self):
        source = (ROOT / 'dist/assets/data.js').read_text()
        data = json.loads(source.removeprefix('window.LarnixData = ').removesuffix(';\n'))
        modules = {m['id']: m for m in data['modules']}
        order = [l for mid in data['order'] for l in modules[mid]['lessons']]
        prior = set()
        for lesson in order:
            self.assertTrue(set(lesson['prerequisites']) <= prior, lesson['id'])
            self.assertNotIn('estimate_basis', lesson)
            prior.add(lesson['id'])
        curriculum = json.loads((ROOT / 'docs/curriculum/curriculum.json').read_text())
        for module in curriculum['modules']:
            with self.subTest(module=module['id']):
                self.assertEqual([lesson['id'] for lesson in modules[module['id']]['lessons']],
                                 module['lesson_order'])

    def test_static_routes_and_assets(self):
        out = ROOT / 'dist'
        for file in out.rglob('*.html'):
            page = Page(file.read_text())
            self.assertEqual(len(page.ids), len(set(page.ids)), file)
            for ref in page.refs:
                url = urlsplit(ref)
                if url.scheme or ref.startswith('#/'):
                    continue
                target = file.parent / url.path if url.path else file
                if target.is_dir():
                    target = target / 'index.html'
                self.assertTrue(target.exists(), (file, ref))
                if url.fragment and not url.fragment.startswith('/'):
                    self.assertIn(url.fragment, Page(target.read_text()).ids, (file, ref))

    def test_shared_runtime_precedes_lesson_and_shell(self):
        previews = json.loads((ROOT / 'web/lessons.json').read_text())
        for lesson_id in previews:
            file = ROOT / 'dist/lessons' / lesson_id / 'index.html'
            text = file.read_text()
            self.assertIn(f'data-platform-lesson="{lesson_id}"', text)
            scripts = Page(text).scripts
            self.assertLess(scripts.index('../../assets/progress.js'), scripts.index('../../assets/lesson-ui.js'))
            self.assertLess(scripts.index('../../assets/lesson-ui.js'), scripts.index('lesson.js'))
            self.assertLess(scripts.index('lesson.js'), scripts.index('../../assets/lesson-shell.js'))

    def test_links_stay_inside_github_project_path(self):
        out = ROOT / 'dist'
        origin = 'https://venkathub.github.io'
        for file in out.rglob('*.html'):
            public_url = origin + '/larnix/' + file.relative_to(out).as_posix()
            for ref in Page(file.read_text()).refs:
                if urlsplit(ref).scheme or ref.startswith('//'):
                    continue
                resolved = urlsplit(urljoin(public_url, ref))
                self.assertTrue(resolved.path.startswith('/larnix/'), (file, ref))
                target = out / resolved.path.removeprefix('/larnix/')
                if target.is_dir():
                    target /= 'index.html'
                self.assertTrue(target.is_file(), (file, ref))

    def test_static_accessibility_basics(self):
        # A small regression gate, not a substitute for a browser/screen-reader audit.
        for file in (ROOT / 'dist').rglob('*.html'):
            page = Page(file.read_text())
            self.assertTrue(any(tag == 'html' and attrs.get('lang') == 'en'
                                for tag, attrs in page.elements), file)
            self.assertEqual(sum(tag == 'main' for tag, _ in page.elements), 1, file)
            self.assertTrue(any(tag == 'title' for tag, _ in page.elements), file)
            self.assertTrue(any(tag == 'a' and attrs.get('class') == 'skip'
                                for tag, attrs in page.elements), file)
            for tag, attrs in page.elements:
                if tag == 'img':
                    self.assertIn('alt', attrs, file)
                if tag == 'svg' and attrs.get('role') == 'img':
                    self.assertTrue(attrs.get('aria-label') or attrs.get('aria-labelledby'), file)
                for target in attrs.get('aria-labelledby', '').split():
                    self.assertIn(target, page.ids, (file, target))


if __name__ == '__main__':
    unittest.main()
