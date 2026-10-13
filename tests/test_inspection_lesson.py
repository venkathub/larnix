"""Execute the inspection preview's synthetic fixture and report starter."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
from matplotlib.figure import Figure

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes


class InspectionLessonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.note = load_notes()['M02-L07']
        cls.starter = {'__name__': 'inspection_starter'}
        exec(compile(cls.note['practice']['starter'], 'M02-L07 starter', 'exec'), cls.starter)
        cls.raw = cls.starter['FIXTURE_CSV'].encode('utf-8')

    def test_case_evidence_matches_observed_counts_and_distributions(self):
        df, summary = self.starter['inspect_csv'](self.raw)
        self.assertEqual(len(df), 9)
        self.assertEqual(summary.loc['Walk-in'].to_dict(),
                         dict(rows=6, observed=5, mean=20, median=20, missing=1))
        self.assertEqual(summary.loc['Account'].to_dict(),
                         dict(rows=3, observed=3, mean=20, median=8, missing=0))
        cases = self.note['lab']['scenarios']
        for case, values in zip(cases, [[20, 20], [20, 20], [20, 8, 44]]):
            self.assertIn('SYNTHETIC', case['label'])
            self.assertEqual([b['value'] for b in case['bars']], values)
            self.assertTrue(all(b['max'] == 44 and '(units)' in b['label'] for b in case['bars']))
        first = dict(cases[0]['evidence'])
        counts = first['Audit behind the headline']
        for group in ['Walk-in', 'Account']:
            row = summary.loc[group]
            self.assertIn(f'{group}: {int(row.rows)} rows, n={int(row.observed)} observed, missing={int(row.missing)}', counts)
            self.assertIn(f'{group} {int(row["median"])}', first['What equal bars hide'])
        self.assertIn('Walk-in 100 / 5 = 20; Account 60 / 3 = 20 units', first['Mean calculation'])
        second = dict(cases[1]['evidence'])
        for group in ['Walk-in', 'Account']:
            row = summary.loc[group]
            self.assertEqual(second[f'{group} denominator'],
                             f'{int(row.rows)} rows = {int(row.observed)} observed + {int(row.missing)} missing; mean {row["mean"]:g}, median {row["median"]:g} units')
        values = {group: df.loc[df.customer_group.eq(group), 'cost'].dropna().astype(int).sort_values().tolist()
                  for group in ['Walk-in', 'Account']}
        distribution = dict(cases[2]['evidence'])['Observed distributions']
        self.assertEqual(distribution, f'Walk-in {values["Walk-in"]}; Account {values["Account"]} units')
        account = pd.Series(values['Account'])
        without = account[account.ne(44)]
        self.assertEqual(without.mean(), 8)
        self.assertEqual(account.mean() - without.mean(), 12)
        sensitivity = dict(cases[2]['evidence'])['Outlier sensitivity']
        self.assertIn(f'n={len(without)}, mean {without.mean():g}, median {without.median():g}', sensitivity)
        self.assertIn(f'raises mean by {account.mean() - without.mean():g}', sensitivity)
        self.assertEqual(df.loc[df.cost.isna(), 'rental_id'].tolist(), ['W6'])

    def test_transfer_and_recovered_missing_cost(self):
        answer = self.note['transfer'][0]['answer']
        for group, costs in [('Walk-in', [10, 10, 10, None]), ('Account', [4, 4, 22])]:
            series = pd.Series(costs)
            self.assertIn(f'{group} has {len(series)} rows, n={series.count()} observed, missing={series.isna().sum()}', answer)
        account = pd.Series([4, 4, 22])
        self.assertEqual(account.mean(), 10)
        self.assertEqual(account.median(), 4)
        self.assertIn(f'raises the mean by {account.mean() - account.iloc[:2].mean():g} units', answer)
        recovered = self.raw.replace(b'W6,Walk-in,\n', b'W6,Walk-in,20\n')
        df, summary = self.starter['inspect_csv'](recovered)
        self.assertEqual(summary.loc['Walk-in'].to_dict(),
                         dict(rows=6, observed=6, mean=20, median=20, missing=0))
        self.assertEqual(df.loc[df.customer_group.eq('Walk-in'), 'cost'].sum(), 120)
        self.assertNotEqual(hashlib.sha256(recovered).hexdigest(), hashlib.sha256(self.raw).hexdigest())
        for malformed in [self.raw.replace(b'W6,Walk-in,', b'W6,,'),
                          self.raw.replace(b'W6,Walk-in,', b'W1,Walk-in,'),
                          self.raw.replace(b'A3,Account,44', b'A3,Account,invalid'),
                          self.raw.replace(b'A3,Account,44', b'A3,Account,inf')]:
            with self.assertRaises(ValueError):
                self.starter['inspect_csv'](malformed)

    def test_report_records_same_input_and_labels_every_group(self):
        original_save = Figure.savefig
        captured = []

        def inspect_figure(fig, *args, **kwargs):
            for group, ax in zip(['Walk-in', 'Account'], fig.axes):
                expected = {'Walk-in': (5, 6, 1), 'Account': (3, 3, 0)}[group]
                self.assertIn(f'{group}: n={expected[0]}, rows={expected[1]}, missing={expected[2]}', ax.get_title())
                self.assertIn('within group', ax.get_xlabel())
                self.assertEqual(len(ax.collections[0].get_offsets()), expected[0])
                self.assertGreater(ax.get_ylim()[1], 44)
            self.assertEqual(fig.axes[0].get_ylim(), fig.axes[1].get_ylim())
            self.assertIn('fictional currency units per rental', fig.axes[0].get_ylabel())
            captured.append(True)
            return original_save(fig, *args, **kwargs)

        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / 'rentals.csv'
            input_path.write_bytes(self.raw)
            output = Path(tmp) / 'report'
            with patch.object(Figure, 'savefig', inspect_figure):
                self.starter['write_report'](input_path, output)
            provenance = json.loads((output / 'provenance.json').read_text())
            self.assertEqual(provenance['sha256'], hashlib.sha256(self.raw).hexdigest())
            self.assertEqual(set(provenance['versions']), {'python', 'pandas', 'matplotlib', 'numpy'})
            self.assertIn('SYNTHETIC', provenance['mode'])
            missingness = pd.read_csv(output / 'missingness.csv', index_col=0)
            self.assertEqual(missingness.loc['cost', 'missing_count'], 1)
            report = pd.read_csv(output / 'group_summary.csv', index_col=0)
            self.assertEqual(report.loc['Walk-in', 'missing'], 1)
            self.assertEqual(report.loc['Account', 'median'], 8)
            self.assertTrue((output / 'costs.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
            self.assertEqual(captured, [True])


if __name__ == '__main__':
    unittest.main()
