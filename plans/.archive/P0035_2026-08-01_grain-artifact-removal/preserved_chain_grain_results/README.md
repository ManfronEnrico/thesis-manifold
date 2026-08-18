# Preserved chain-grain SRQ1 results (pre-P0035)

Verbatim copies of `04_thesis_results/srq1/tuned_params.json` and
`tuned_summary.md` **as they stood before P0035 task 6** purged their
chain-grain entries.

Kept because **P0034** needs the old danskvand chain figure to explain the
22.0 -> 23.8 change to Enrico.

## The figures P0034 needs

| Grain | Category | Model | test WMAPE |
|---|---|---|---|
| `bychain` | danskvand | XGBoost | **22.0%** |
| `brand` (brand x month) | danskvand | XGBoost | **23.8%** |

So the "regression" from 22.0% to 23.8% is **not** a model getting worse — it is
the reported grain changing from brand x chain to brand x month per DEC-GRAIN
(2026-07-12). The brand x month number was always there in the same file, under
`## Dataset: brand`.

Full chain-grain table, for reference:

| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |
|---|---|---|---|---|---|
| CSD | LightGBM | 21.2% | 55.2% | 22.1% | 22.6% |
| CSD | XGBoost | 20.8% | 54.5% | 22.0% | 21.9% |
| danskvand | LightGBM | 24.1% | 7438153885.4% | 23.4% | 16.6% |
| danskvand | XGBoost | 22.0% | 7984019094.5% | 21.8% | 16.3% |
| energidrikke | LightGBM | 14.4% | 11431678131.8% | 21.2% | 14.6% |
| energidrikke | XGBoost | 13.9% | 16142103812.7% | 21.0% | 14.5% |
| RTD | LightGBM | 40.8% | 5019414818.6% | 30.2% | 40.0% |
| RTD | XGBoost | 38.8% | 5346112824.9% | 29.1% | 38.9% |

> Note the absurd `test mean MAPE` values (billions of percent) in both grains.
> That is a pre-existing division-by-near-zero artifact in the mean-MAPE
> computation, unrelated to grain. P0035 did not touch it — flagged for whoever
> owns SRQ1 metrics.

## Note on the `brand/` key prefix

The surviving entries in `tuned_params.json` use the prefix `brand/`, and
`tuned_summary.md` heads its surviving table `## Dataset: brand`. These are the
brand x month grain. The canonical `srq1_benchmark.py` in
`03_thesis_modelling/model_training/` has since renamed this grain tag to
`bymonth`, so **the results files and the script now disagree on the tag name**.
P0035 deliberately did not rename the keys in the results files, because doing so
would silently rewrite recorded experimental output. Regenerating these artifacts
with the current script will produce `bymonth/` keys.
