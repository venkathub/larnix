"""Acceptance checks for authored foundation coverage and teaching fixtures."""
import json
import contextlib
import io
import sys
import unittest

import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes, validate_notes


class FoundationLessonsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.curriculum = json.loads((ROOT / 'docs/curriculum/curriculum.json').read_text())
        cls.manifest = json.loads((ROOT / 'web/lessons.json').read_text())
        cls.notes = load_notes()

    def test_all_six_modules_are_authored_without_replacing_vector_lab(self):
        expected = {lid for lid, entry in self.manifest.items()
                    if entry.get('format') == 'foundation'} | {'M03-L01'}
        original = {l['id'] for m in self.curriculum['modules'][:6] for l in m['lessons'][:4]}
        authored = {l['id'] for m in self.curriculum['modules'][:6] for l in m['lessons']
                    if l['status'] in {'preview', 'complete'}}
        self.assertTrue(original <= expected)
        self.assertEqual(expected, authored)
        self.assertEqual(set(self.notes), expected - {'M03-L01'})
        self.assertEqual(self.manifest['M03-L01']['directory'], 'vector-similarity')
        validate_notes(self.notes, self.curriculum)

    def test_manifest_descriptions_match_foundation_ideas(self):
        for lesson_id, entry in self.manifest.items():
            if entry.get('format') == 'foundation':
                with self.subTest(lesson=lesson_id):
                    self.assertEqual(entry['description'], self.notes[lesson_id]['idea'])

    def test_source_review_dates_require_iso_calendar_dates(self):
        for value in ['2026-10-13', '2024-02-29']:
            with self.subTest(valid=value):
                note = dict(self.notes['M02-L05'], sources_reviewed_on=value)
                validate_notes({'M02-L05': note}, self.curriculum)
        for value in ['October 13, 2026', '20261013', '2026-W42-2',
                      '2026-02-29', '2026-1-3', '', None, 20261013]:
            with self.subTest(invalid=value):
                note = dict(self.notes['M02-L05'], sources_reviewed_on=value)
                with self.assertRaisesRegex(ValueError, 'sources_reviewed_on.*YYYY-MM-DD'):
                    validate_notes({'M02-L05': note}, self.curriculum)

    def test_saved_check_keys_match_the_rendered_lesson_answers(self):
        for lesson_id, note in self.notes.items():
            with self.subTest(lesson=lesson_id):
                self.assertEqual(self.manifest[lesson_id]['answers'],
                                 {f'check{i+1}': str(q['answer']) for i, q in enumerate(note['checks'])})
                self.assertEqual(self.manifest[lesson_id]['checks'], len(note['checks']))
                self.assertEqual(self.manifest[lesson_id]['format'], 'foundation')

    def test_numpy_cost_fixtures_match_executed_arithmetic(self):
        cases = self.notes['M02-L05']['lab']['scenarios']
        days = np.array([2, 4, 3], dtype=np.int64)
        rates = np.array([12, 7, 9], dtype=np.float64)
        loop = np.array([float(days[i]) * float(rates[i]) for i in range(3)])
        costs = days * rates
        np.testing.assert_allclose(costs, loop, rtol=0, atol=1e-9)
        np.testing.assert_allclose(costs, [24, 28, 27], rtol=0, atol=1e-9)
        pairwise = days[:, None] * rates
        self.assertEqual(pairwise.shape, (3, 3))
        with self.assertRaises(ValueError):
            days * rates[:2]
        for case, count in zip(cases, [costs.size, pairwise.size, 0]):
            self.assertIn('SYNTHETIC', case['label'])
            self.assertEqual([b['value'] for b in case['bars']], [3, count])
            self.assertEqual([b['max'] for b in case['bars']], [9, 9])
        matched = dict(cases[0]['evidence'])
        wrong = dict(cases[1]['evidence'])
        self.assertEqual(matched['Loop / vectorized'],
                         f'{loop.astype(int).tolist()} / {costs.astype(int).tolist()} units')
        self.assertEqual(matched['Total / shape'], f'{costs.sum():.0f} units / {costs.shape}')
        self.assertEqual(wrong['Pairwise costs'], f'{pairwise.astype(int).tolist()} units')
        self.assertEqual(wrong['Wrong total / correct total'],
                         f'{pairwise.sum():.0f} units / {costs.sum():.0f} units')
        failure = dict(cases[2]['evidence'])['Failure / recovery']
        self.assertIn('ValueError', failure)
        self.assertIn(f'total {costs.sum():.0f}', failure)

    def pandas_starter(self):
        namespace = {}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(self.notes['M02-L06']['practice']['starter'],
                         'M02-L06 starter', 'exec'), namespace)
        return namespace

    def test_pandas_join_fixtures_match_executed_rows_and_costs(self):
        starter = self.pandas_starter()
        rentals, rates = starter['RENTALS'], starter['RATES']
        audit_join = starter['audit_join']
        cases = self.notes['M02-L06']['lab']['scenarios']
        clean, missing, audit = audit_join(rentals, rates)
        self.assertTrue(missing.empty)
        self.assertEqual(audit, dict(rows_before=3, rows_after=3, missing_rates=0))
        self.assertEqual(clean['cost'].tolist(), [24, 12, 20])
        self.assertEqual(clean['cost'].sum(), 56)
        duplicate = pd.concat([rates, rates.iloc[[0]]], ignore_index=True)
        with self.assertRaises(pd.errors.MergeError):
            audit_join(rentals, duplicate)
        unsafe = rentals.merge(duplicate, on='equipment', how='left')
        unsafe['cost'] = unsafe['days'] * unsafe['daily_rate']
        self.assertEqual(unsafe['cost'].tolist(), [24, 24, 12, 12, 20])
        self.assertEqual(unsafe['cost'].sum(), 92)
        unknown, missing, audit = audit_join(
            rentals.assign(equipment=['drill', 'drill', 'hoist']), rates)
        self.assertEqual(audit, dict(rows_before=3, rows_after=3, missing_rates=1))
        self.assertEqual(missing['rental_id'].tolist(), ['R3'])
        self.assertEqual(missing['_merge'].tolist(), ['left_only'])
        self.assertTrue(pd.isna(unknown.loc[2, 'cost']))
        self.assertEqual(str(unknown['daily_rate'].dtype), 'Int64')
        self.assertEqual(unknown['cost'].sum(), 36)  # partial, never the full total
        for case, output, missing_count in zip(cases, [clean, unsafe, unknown], [0, 0, 1]):
            with self.subTest(case=case['label']):
                self.assertIn('SYNTHETIC', case['label'])
                self.assertEqual([b['value'] for b in case['bars']], [len(rentals), len(output)])
                self.assertEqual([b['max'] for b in case['bars']], [5, 5])
                self.assertEqual(case['evidence'][0][1],
                                 f'{len(rentals)} / {len(output)}; missing rates {missing_count}')
                self.assertIn(str(output['cost'].tolist()), case['evidence'][1][1])
                self.assertIn(f'{output["cost"].sum()} ', case['evidence'][1][1])
        self.assertIn(f'{unsafe["cost"].sum()} − {clean["cost"].sum()} = 36',
                      cases[1]['evidence'][2][1])
        self.assertIn('full total withheld', cases[2]['evidence'][2][1])
        # A matched key with a null price must also be preserved and reported.
        null_rates = rates.assign(daily_rate=pd.Series([12, None], dtype='Int64'))
        null_joined, missing, audit = audit_join(rentals, null_rates)
        self.assertEqual(missing['rental_id'].tolist(), ['R3'])
        self.assertEqual(missing['_merge'].tolist(), ['both'])
        self.assertEqual(audit['missing_rates'], 1)
        self.assertTrue(pd.isna(null_joined.loc[2, 'cost']))
        shuffled, missing, _ = audit_join(rentals, rates.iloc[::-1])
        pd.testing.assert_frame_equal(shuffled, clean)
        for invalid in [rentals.assign(rental_id=['R1', 'R1', 'R3']),
                        rentals.assign(rental_id=['R1', None, 'R3']),
                        rentals.assign(equipment=['drill', None, 'lamp'])]:
            with self.assertRaises(ValueError):
                audit_join(invalid, rates)
        with self.assertRaises(ValueError):
            audit_join(rentals, rates.assign(equipment=['drill', None]))

    def test_pandas_groups_pivot_and_transfer_reconcile(self):
        starter = self.pandas_starter()
        joined = starter['joined']
        branches = joined.groupby('branch', dropna=False)['cost'].sum()
        equipment = joined.groupby('equipment', dropna=False)['cost'].sum()
        self.assertEqual(branches.to_dict(), {'North': 44, 'South': 12})
        self.assertEqual(equipment.to_dict(), {'drill': 36, 'lamp': 20})
        cells = joined.groupby(['branch', 'equipment'], as_index=False, dropna=False)['cost'].sum()
        wide = cells.pivot(index='branch', columns='equipment', values='cost')
        self.assertTrue(pd.isna(wide.loc['South', 'lamp']))
        evidence = dict(self.notes['M02-L06']['lab']['scenarios'][0]['evidence'])['Branch totals / pivot']
        self.assertIn(f'South {wide.loc["South"].tolist()}', evidence)
        self.assertIn('After the audit, fill the absent cell with 0', evidence)
        wide = wide.fillna(0)
        self.assertEqual(wide.loc['North'].tolist(), [24, 20])
        self.assertEqual(wide.loc['South'].tolist(), [12, 0])
        self.assertEqual(wide.sum().sum(), branches.sum())
        self.assertEqual(equipment.sum(), joined['cost'].sum())
        note = self.notes['M02-L06']
        evidence = dict(note['lab']['scenarios'][0]['evidence'])['Branch totals / pivot']
        for branch in ['North', 'South']:
            self.assertIn(f'{branch} {branches[branch]}', evidence)
            self.assertIn(f'{branch} {wide.loc[branch].tolist()}', evidence)
        # pivot cannot conceal repeated cells; a learner must choose aggregation.
        with self.assertRaises(ValueError):
            pd.concat([cells, cells.iloc[[0]]]).pivot(
                index='branch', columns='equipment', values='cost')
        rentals = pd.DataFrame({'equipment': ['saw', 'saw'], 'days': [2, 3]})
        rates = pd.DataFrame({'equipment': ['saw'], 'daily_rate': [8]})
        answer = note['transfer'][0]['answer']
        for rate_table in [rates, pd.concat([rates, rates])]:
            result = rentals.merge(rate_table, on='equipment', how='left')
            costs = result['days'] * result['daily_rate']
            self.assertIn(f'{len(result)} rows', answer)
            self.assertIn(str(costs.tolist()), answer)
            self.assertIn(f'total {costs.sum()}', answer)

    def test_numpy_transfer_and_topic_numbers(self):
        note = self.notes['M02-L05']
        days, rates = np.array([5, 2]), np.array([6, 11])
        matched, wrong = days * rates, days[:, None] * rates
        answer = note['transfer'][0]['answer']
        for output in [str(matched.tolist()), str(wrong.tolist()),
                       f'total {matched.sum()}', f'total {wrong.sum()}']:
            self.assertIn(output, answer)
        days, rates = np.array([2, 4, 3]), np.array([12, 7, 9])
        matrix = days[:, None] * rates
        topics = {t['title']: t['explanation'] for t in note['topics']}
        for axis in [0, 1]:
            self.assertIn(str(matrix.sum(axis=axis).tolist()), topics['axis reductions'])
        costs = days * rates
        self.assertIn(str(costs[costs >= 27].tolist()), topics['boolean indexing'])
        reordered = days * rates[[1, 0, 2]]
        self.assertIn(str(reordered.tolist()), note['transfer'][1]['answer'])
        self.assertIn(f'total {reordered.sum()}', note['transfer'][1]['answer'])
        view = rates[:2]
        view[0] = 0
        self.assertIn(str(rates.tolist()), topics['views versus copies'])
        rates = np.array([12, 7, 9])
        copy = rates[:2].copy()
        copy[0] = 0
        np.testing.assert_array_equal(rates, [12, 7, 9])

    def test_threshold_fixture_counts_match_the_original_six_tickets(self):
        scores = [.9, .8, .7, .4, .3, .1]
        labels = [1, 0, 1, 1, 0, 0]
        for threshold, case in zip([.8, .4, .1], self.notes['M04-L03']['lab']['scenarios']):
            predictions = [score >= threshold for score in scores]
            caught = sum(p and y for p, y in zip(predictions, labels))
            values = {b['label']: b['value'] for b in case['bars']}
            self.assertEqual(values['Reviewed tickets'], sum(predictions))
            self.assertEqual(values['Caught urgent tickets'], caught)
            if 'Missed urgent tickets' in values:
                self.assertEqual(values['Missed urgent tickets'], sum(labels) - caught)
            if 'Over capacity: tickets' in values:
                self.assertEqual(values['Over capacity: tickets'], max(0, sum(predictions) - 4))

    def test_baselines_do_not_confuse_accuracy_with_catching_rare_cases(self):
        cases = self.notes['M04-L01']['lab']['scenarios']
        # 8 on-time, 2 late. Models: always on-time; 2 TP + 2 FP;
        # strict rule with 1 TP + 0 FP. These tradeoffs are the lesson.
        for case, (tp, fp) in zip(cases, [(0, 0), (2, 2), (1, 0)]):
            values = {b['label']: b['value'] for b in case['bars']}
            self.assertEqual(values['Correct records'], tp + (8-fp))
            self.assertEqual(values['Missed late records'], 2-tp)
            self.assertEqual(values['False alarms: records'], fp)

    def test_training_fixtures_match_independent_scalar_calculations(self):
        x, target, weight, rate = 2, 6, 1, .1
        loss = (weight*x-target)**2
        gradient = 2*(weight*x-target)*x
        updated = weight-rate*gradient
        after = (updated*x-target)**2
        for case, expected in zip(self.notes['M05-L01']['lab']['scenarios'], [loss, loss, after]):
            bars = {b['label']: b['value'] for b in case['bars']}
            self.assertAlmostEqual(bars['Current squared loss'], expected)
        for rate, case in zip([.25, 1, 1.2], self.notes['M05-L02']['lab']['scenarios']):
            weight = 0
            for _ in range(2):
                weight -= rate * 2 * (weight-3)
            bars = {b['label']: b['value'] for b in case['bars']}
            self.assertAlmostEqual(bars['After 2: squared loss'], (weight-3)**2)

    def test_shared_filter_fixture_reuses_the_same_local_operation(self):
        strips = [[0, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]]
        for strip, case in zip(strips, self.notes['M05-L04']['lab']['scenarios']):
            expected = [b-a for a, b in zip(strip, strip[1:])]
            self.assertEqual([b['value'] for b in case['bars']], expected)


if __name__ == '__main__':
    unittest.main()
