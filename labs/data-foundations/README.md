# Data foundations: original runnable lab

Supports the new M02-L05 (NumPy), M02-L06 (pandas) and M02-L07 (dataset inspection and plotting) plans. This is a working local artifact with tests and injected failures; those three complete narrative lessons are **still planned**. It is not a restoration of the 50 archived Pyodide chapters, and it does not claim the whole nine-part lesson contract is met.

## Reproduce

Use Python 3.12 (verified with 3.12.14). From this directory:

```sh
python3 -m venv /tmp/larnix-data-env
/tmp/larnix-data-env/bin/python -m pip install -r requirements.txt
/tmp/larnix-data-env/bin/python -m unittest discover -s . -p 'test_*.py'
/tmp/larnix-data-env/bin/python lab.py --output /tmp/larnix-data-evidence
```

Top-level package versions are pinned. Transitive dependencies are resolved by pip, so this is a reproducible teaching environment specification rather than a full supply-chain lockfile. The output records actual package versions and input hashes. No network is used after dependency installation. Fixtures are four invented rentals and three rates; no personal data or downloaded dataset is involved.

## Predict before running

1. Four rentals have day counts `[2, 3, 1, 4]` and matched rates `[10, 15, 10, 7]`. Work out each cost and total.
2. What shape results if the day vector is accidentally reshaped to `(4, 1)` before multiplication by `(4,)` rates?
3. What should happen if one rate key is duplicated or missing? Should a missing rate become zero?

The expected costs are `[20, 45, 10, 28]`, total **103 fictional currency units**. Correct broadcasting is elementwise on equal one-dimensional shapes. The mistaken broadcast produces a **4 × 4 matrix** of pairwise costs. A valid NumPy operation can still answer the wrong question.

## Inspect the evidence

- `joined.csv`: four input rentals remain four joined records.
- `totals.csv`: drill 30 (two rentals), saw 45 (one), sander 28 (one).
- `costs.png`: units and sample sizes are visible; it is descriptive, not causal.
- `report.json`: versions, hashes, results, wrong-broadcast dimensions and rejected failure cases.

The failure suite injects a duplicate rate, unknown equipment and a null rate. The corrected original inputs are run again. `merge(validate='many_to_one')` rejects fan-out; missing rates fail instead of silently lowering costs. Tests also cover shuffled rate order, duplicate rental IDs, invalid shapes and non-finite values.

## Extend and explain

Try a new rental and update the hand calculation first. Then add a nullable inspection field, report its missingness separately from valid costs, and plot the distribution when you have enough observations. Fit any learned preprocessing only on training data. Explain why these four rows cannot establish model quality, performance or group fairness.

Primary readings: [NumPy](https://numpy.org/doc/stable/user/absolute_beginners.html), [pandas](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html), [Matplotlib](https://matplotlib.org/stable/users/explain/quick_start.html).
