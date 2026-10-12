"""Verify generated lesson assets and links, independently of the browser."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urljoin
import json
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_site import build


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
