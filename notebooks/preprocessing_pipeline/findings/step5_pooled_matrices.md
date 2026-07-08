# Step 5 — Pooled feature matrices (4-cat and 5-cat)

**Goal**: build the two "pooled" feature matrices — the input for the
generalist models in the 7-model plan.

## Design

`build_pooled_feature_matrix(matrices_by_category)` simply:
1. Adds a `category` column to each input matrix.
2. Concatenates row-wise (no merging, no deduplication).
3. Casts `category` to pandas categorical (LightGBM consumes it natively).
4. Sorts by `(category, brand, date)` for deterministic output.

Brands are **not renamed** when they appear in multiple categories (e.g.
HARBOE appears in csd AND danskvand). The natural series identifier in the
pooled setting is the `(category, brand)` pair.

## Why no NaN handling needed

Because all 5 specialized matrices were produced via the same canonical
schema (`aggregate_brand_month_from_db` returns 8 columns regardless of
category), the pooled concat has no missing columns. `FeatureEngineer`
already produced consistent feature columns (`lag_*`, `rolling_*`,
`month`, etc.) across categories.

If we later choose to add category-specific richer features (e.g.
`baseline_sales` for danskvand/energidrikke/rtd/totalbeer but not csd),
those would generate NaN in CSD rows of pooled-5. LightGBM handles that
natively, so no preprocessing required.

## Results

### pooled-4 (4 new categories: danskvand + energidrikke + rtd + totalbeer)

```
rows: 13,869
brand × category pairs: 359
breakdown:
  danskvand       888 rows
  energidrikke  1,053 rows
  rtd           1,554 rows
  totalbeer    10,374 rows  ← dominates (266 of the 359 pairs)
splits: train=9,202  val=2,154  test=2,513
```

### pooled-5 (all 5 categories: csd + the 4 above)

```
rows: 17,103
brand × category pairs: 436  (= 359 + 77 csd brands)
breakdown:
  csd          3,234 rows
  danskvand      888 rows
  energidrikke 1,053 rows
  rtd          1,554 rows
  totalbeer   10,374 rows
splits: train=11,435  val=2,616  test=3,052
```

Output:
```
results/phase1/pooled_4/feature_matrix.parquet  1.4 MB
results/phase1/pooled_5/feature_matrix.parquet  1.8 MB
```

## Class imbalance note

`totalbeer` represents ~75% of pooled-4 rows and ~61% of pooled-5 rows.
This means a naive LightGBM may learn primarily the totalbeer pattern.

Mitigation options for the training step:
- Stratified sampling on `category`
- Class weights inversely proportional to row count
- Per-category early stopping
- Or: accept the imbalance and explicitly evaluate per-category MAE in the
  results table (which is what we plan to do anyway for specialized vs
  pooled comparison)

We'll start without rebalancing and check whether `totalbeer` performance
dominates the pooled metrics; if yes, add weights.

## Ready for training

7 feature matrices in `results/phase1/`, all sharing identical schema and
identical split boundaries (train ≤ Feb 2025, val Mar–Aug 2025, test Sep
2025–Mar 2026). Ready for the LightGBM training step.
