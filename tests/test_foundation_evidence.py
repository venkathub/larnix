"""Evidence preserves recorded lines without changing ordinary prose markup."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import evidence


class FoundationEvidenceTest(unittest.TestCase):
    def test_multiline_values_are_preformatted_and_escaped(self):
        self.assertEqual(
            evidence([('Trace <label>', '  <script>\n"quoted" & \'text\'')]),
            '<dl class="case-evidence"><div><dt>Trace &lt;label&gt;</dt>'
            '<dd><pre class="evidence-pre">  &lt;script&gt;\n'
            '&quot;quoted&quot; &amp; &#x27;text&#x27;</pre></dd></div></dl>')

    def test_single_line_values_keep_the_original_markup(self):
        self.assertEqual(
            evidence([('Input', '“  Drill STOPPED  ”'), ('Result', '1 < 2 & 3')]),
            '<dl class="case-evidence"><div><dt>Input</dt>'
            '<dd>“  Drill STOPPED  ”</dd></div><div><dt>Result</dt>'
            '<dd>1 &lt; 2 &amp; 3</dd></div></dl>')


if __name__ == '__main__':
    unittest.main()
