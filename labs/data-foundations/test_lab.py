import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
import pandas as pd
from lab import array_costs, join_costs, run


class DataLabTest(unittest.TestCase):
    def setUp(self):
        self.rentals = pd.DataFrame({'rental_id': ['x', 'y'], 'equipment': ['a', 'b'], 'days': [3, 2]})
        self.rates = pd.DataFrame({'equipment': ['b', 'a'], 'daily_rate': [7, 11]})

    def test_arrays_agree_with_independent_loop_and_reject_broadcast(self):
        expected = [d*r for d,r in zip([3, 2], [11, 7])]
        np.testing.assert_array_equal(array_costs([3, 2], [11, 7]), expected)
        for days, rates in [([[3], [2]], [11, 7]), ([3], [11, 7]), ([float('nan')], [1]), ([-1], [2])]:
            with self.assertRaises(ValueError):
                array_costs(days, rates)

    def test_join_uses_keys_not_input_row_order(self):
        result = join_costs(self.rentals, self.rates)
        self.assertEqual(result['cost'].tolist(), [33, 14])
        self.assertEqual(len(result), len(self.rentals))

    def test_invalid_cardinality_and_missing_values_fail_closed(self):
        with self.assertRaises(pd.errors.MergeError):
            join_costs(self.rentals, pd.concat([self.rates, self.rates.iloc[[0]]]))
        with self.assertRaises(ValueError):
            join_costs(self.rentals, self.rates.iloc[[0]])
        with self.assertRaises(ValueError):
            join_costs(self.rentals.assign(rental_id=['x', 'x']), self.rates)
        with self.assertRaises(ValueError):
            join_costs(self.rentals, self.rates.assign(daily_rate=[np.nan, 11]))

    def test_artifacts_and_failure_report_reproduce(self):
        with tempfile.TemporaryDirectory() as directory:
            first = run(directory)
            second = run(directory)
            self.assertEqual(first, second)
            self.assertEqual(first['costs'], [20, 45, 10, 28])
            self.assertEqual(first['total'], 103)
            self.assertEqual(first['wrong_broadcast_shape'], [4, 4])
            self.assertEqual(set(first['rejected_failures']), {'duplicate_rate', 'unknown_equipment', 'null_rate'})
            self.assertEqual(json.loads((Path(directory)/'report.json').read_text()), first)
            self.assertEqual((Path(directory)/'costs.png').read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
            totals = pd.read_csv(Path(directory)/'totals.csv').set_index('equipment')
            self.assertEqual(totals['cost'].to_dict(), {'drill': 30, 'sander': 28, 'saw': 45})


if __name__ == '__main__':
    unittest.main()
