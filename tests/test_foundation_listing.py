"""Validate optional listings and preserve copyable, escaped code in the core."""
from copy import deepcopy
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes, render, validate_notes, worked_example


class ListingParser(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.in_listing = False
        self.in_code = False
        self.code = ''
        self.numbers = []
        self.scroll_attributes = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'figure' and attrs.get('class') == 'code-listing':
            self.in_listing = True
        if self.in_listing:
            if tag == 'pre':
                self.scroll_attributes = attrs
            elif tag == 'code':
                self.in_code = True
            elif tag == 'span':
                self.numbers.append(attrs['data-line'])

    def handle_endtag(self, tag):
        if tag == 'code':
            self.in_code = False
        elif tag == 'figure':
            self.in_listing = False

    def handle_data(self, data):
        if self.in_code:
            self.code += data


class FoundationListingTest(unittest.TestCase):
    def setUp(self):
        self.curriculum = json.loads((ROOT / 'docs/curriculum/curriculum.json').read_text())
        self.note = deepcopy(next(iter(load_notes().values())))
        self.note.pop('listing', None)
        self.module = next(m for m in self.curriculum['modules']
                           if any(l['id'] == self.note['id'] for l in m['lessons']))
        self.lesson = next(l for l in self.module['lessons'] if l['id'] == self.note['id'])
        self.listing = {'title': 'Rental <code> & trace', 'language': 'python',
                        'lines': ['rate = 20', '', 'if rate < 25:', '    print("<lamp>&")']}

    def validate(self):
        validate_notes({self.note['id']: self.note}, self.curriculum)

    def test_numbered_listing_is_escaped_and_copyable_beside_core_trace(self):
        for language in ('python', 'text'):
            with self.subTest(language=language):
                self.note['listing'] = dict(self.listing, language=language)
                self.validate()
                html = render(self.note, self.lesson, self.module)
                parsed = ListingParser(html)
                self.assertEqual(parsed.code, '\n'.join(self.listing['lines']))
                self.assertEqual(parsed.numbers, ['1', '2', '3', '4'])
                self.assertEqual(parsed.scroll_attributes['tabindex'], '0')
                self.assertEqual(parsed.scroll_attributes['aria-label'], self.listing['title'])
                self.assertIn('Rental &lt;code&gt; &amp; trace', html)
                self.assertIn('    print(&quot;&lt;lamp&gt;&amp;&quot;)', html)
                self.assertNotIn('<lamp>', html)
                core = html[html.index('<section class="revision-sheet'):html.index('<details class="study-route"')]
                self.assertIn('<figure class="code-listing">', core)
                self.assertNotIn('<details', core[:core.index('<figure class="code-listing">')])
                self.assertIn('</pre></figure><p class="sketch-caption">', core)
                self.assertIn('language-' + language, core)

    def test_without_listing_preserves_the_original_worked_example_markup(self):
        self.note['example'] = 'Original trace: 2 < 3 & "still true".'
        expected = '<p class="sketch-caption">' + escape(self.note['example'], quote=True) + '</p>'
        self.assertEqual(worked_example(self.note), expected)
        html = render(self.note, self.lesson, self.module)
        self.assertIn(expected, html)
        self.assertIn('<div class="revision-board"><div class="revision-picture">', html)
        self.assertNotIn('code-listing', html)
        self.assertNotIn('listing-trace', html)

    def test_malformed_listing_shapes_fail_validation(self):
        variants = [
            (None, 'listing must be an object'),
            ([], 'listing must be an object'),
            ({**self.listing, 'title': ''}, 'listing title must be a nonempty string'),
            ({**self.listing, 'title': '  '}, 'listing title must be a nonempty string'),
            ({**self.listing, 'title': 3}, 'listing title must be a nonempty string'),
            ({k: v for k, v in self.listing.items() if k != 'title'}, 'listing title must be a nonempty string'),
            ({**self.listing, 'language': 'javascript'}, 'listing language must be python or text'),
            ({**self.listing, 'language': []}, 'listing language must be python or text'),
            ({k: v for k, v in self.listing.items() if k != 'language'}, 'listing language must be python or text'),
            ({k: v for k, v in self.listing.items() if k != 'lines'}, 'listing lines must be a nonempty list'),
            ({**self.listing, 'lines': []}, 'listing lines must be a nonempty list'),
            ({**self.listing, 'lines': 'rate = 20'}, 'listing lines must be a nonempty list'),
            ({**self.listing, 'lines': [None]}, 'listing lines must contain only strings'),
            ({**self.listing, 'lines': ['rate = 20', 7]}, 'listing lines must contain only strings'),
            ({**self.listing, 'lines': ['a\nb']}, 'listing lines must not contain line breaks'),
            ({**self.listing, 'lines': ['a\rb']}, 'listing lines must not contain line breaks'),
            ({**self.listing, 'lines': ['', '  ']}, 'listing must contain visible code or text'),
        ]
        for listing, message in variants:
            with self.subTest(listing=listing):
                self.note['listing'] = listing
                with self.assertRaisesRegex(ValueError, message):
                    self.validate()


if __name__ == '__main__':
    unittest.main()
