"""Original CPU lab: array shapes, validated joins, grouping and a labeled plot.

Run: python lab.py --output /tmp/larnix-data-evidence
All records are invented; no downloads, model services or credentials are used.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import tempfile

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'larnix-matplotlib'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

ROOT = Path(__file__).resolve().parent


def array_costs(days, rates):
    """Pair each rental with one rate; do not accidentally form all pairs."""
    days, rates = np.asarray(days, dtype=float), np.asarray(rates, dtype=float)
    if days.ndim != 1 or rates.ndim != 1 or days.shape != rates.shape:
        raise ValueError('Expected equal one-dimensional shapes')
    if not np.isfinite(days).all() or not np.isfinite(rates).all():
        raise ValueError('Days and rates must be finite')
    if (days < 0).any() or (rates < 0).any():
        raise ValueError('Days and rates must be nonnegative')
    return days * rates


def join_costs(rentals, rates):
    if rentals['rental_id'].isna().any() or rentals['rental_id'].duplicated().any():
        raise ValueError('Each rental needs a unique non-null ID')
    if rentals['equipment'].isna().any() or rates['equipment'].isna().any():
        raise ValueError('Equipment keys cannot be null')
    # validate rejects duplicate rate keys instead of silently multiplying rows.
    joined = rentals.merge(rates, on='equipment', how='left', validate='many_to_one', indicator=True)
    if joined['_merge'].ne('both').any() or joined['daily_rate'].isna().any():
        raise ValueError('Every rental needs a known non-null rate; do not fill with zero')
    joined['cost'] = array_costs(joined['days'], joined['daily_rate'])
    return joined.drop(columns='_merge')


def run(output):
    rentals = pd.read_csv(ROOT / 'rentals.csv')
    rates = pd.read_csv(ROOT / 'rates.csv')
    joined = join_costs(rentals, rates)
    summary = joined.groupby('equipment', as_index=False).agg(cost=('cost', 'sum'), rentals=('rental_id', 'count'))
    # Failure investigation: a broadcast is legal NumPy, but semantically wrong.
    wrong_shape = (joined['days'].to_numpy()[:, None] * joined['daily_rate'].to_numpy()).shape
    failures = {}
    cases = {
        'duplicate_rate': (rentals, pd.concat([rates, rates.iloc[[0]]], ignore_index=True)),
        'unknown_equipment': (rentals.assign(equipment=['drill', 'saw', 'drill', 'unknown']), rates),
        'null_rate': (rentals, rates.assign(daily_rate=[10, 15, np.nan])),
    }
    for name, (rental_case, rate_case) in cases.items():
        try:
            join_costs(rental_case, rate_case)
        except (ValueError, pd.errors.MergeError) as error:
            failures[name] = {'rejected': True, 'reason': str(error)}
        else:
            raise AssertionError(f'Expected {name} to be rejected')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    joined.to_csv(output / 'joined.csv', index=False)
    summary.to_csv(output / 'totals.csv', index=False)
    fig, ax = plt.subplots(figsize=(6, 4), layout='constrained')
    ax.bar(summary['equipment'], summary['cost'], color='#376344')
    ax.set(ylabel='Cost (fictional currency units)', xlabel='Equipment', title='Synthetic rental costs — four rentals')
    for i, row in summary.iterrows():
        ax.annotate(f'n={row["rentals"]}', (i, row['cost']), xytext=(0, 4), textcoords='offset points', ha='center')
    ax.set_ylim(0, 55)
    fig.savefig(output / 'costs.png', dpi=140)
    plt.close(fig)
    report = {
        'mode': 'executed locally on synthetic fixtures',
        'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__, 'matplotlib': matplotlib.__version__},
        'input_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ['rentals.csv', 'rates.csv']},
        'rows_before': len(rentals), 'rows_after': len(joined),
        'costs': joined['cost'].tolist(), 'total': float(joined['cost'].sum()),
        'wrong_broadcast_shape': list(wrong_shape), 'expected_shape': [4],
        'rejected_failures': failures,
        'limitations': 'Four invented rentals demonstrate mechanics, not statistical inference, performance or production readiness.',
    }
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))
