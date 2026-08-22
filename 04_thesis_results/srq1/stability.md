# SRQ1 — forecast stability across seeds

5 seeds, 40 Optuna trials each, expanding-window CV.
Everything except the random seed is held identical: data, splits,
features, protocol. The seed drives Optuna's sampler and the model's own
stochastic elements (subsample, colsample, tie-breaking).

**Stability = coefficient of variation (std/mean) of the forecast for each
(brand, month) cell across seeds.** A CV of 0.05 means the forecast moved
by ~5% of its own level on seed alone.

| Category | Model | median CV | p90 CV | WMAPE mean | WMAPE sd | WMAPE range |
|---|---|---|---|---|---|---|
| CSD | LightGBM | 0.112 | 0.295 | 15.4% | 0.65 | 14.9–16.5% |
| CSD | XGBoost | 0.123 | 0.422 | 15.1% | 0.59 | 14.4–15.9% |
| danskvand | LightGBM | 0.119 | 0.687 | 20.8% | 0.69 | 19.7–21.5% |
| danskvand | XGBoost | 0.124 | 0.539 | 21.8% | 1.04 | 20.4–22.9% |
| energidrikke | LightGBM | 0.174 | 0.634 | 14.1% | 1.18 | 12.8–15.9% |
| energidrikke | XGBoost | 0.174 | 0.730 | 13.9% | 0.79 | 13.1–15.1% |
| RTD | LightGBM | 0.125 | 0.397 | 33.5% | 1.64 | 31.8–35.7% |
| RTD | XGBoost | 0.104 | 0.400 | 35.1% | 0.92 | 34.0–36.3% |

## Does the selected model change with the seed?

The benchmark's output is not just an error figure — it is a *choice* of
model per category. If that choice is seed-dependent, the selection is
not a finding.

| Category | winner per seed | verdict |
|---|---|---|
| CSD | XGBoost, XGBoost, LightGBM, XGBoost, LightGBM | **FLIPS** |
| danskvand | LightGBM, LightGBM, LightGBM, XGBoost, LightGBM | **FLIPS** |
| energidrikke | LightGBM, LightGBM, XGBoost, LightGBM, LightGBM | **FLIPS** |
| RTD | XGBoost, XGBoost, LightGBM, LightGBM, LightGBM | **FLIPS** |

**4 of 4 categories change their winning model on the seed
alone.** Every input is identical; only the random seed differs.

**Consequence for the write-up.** A statement of the form "model X is best
for category Y" is not supported where the winner flips — it reports one
seed's outcome. The defensible claim is that the two gradient-boosting
models are **statistically indistinguishable** on this data, with the
between-seed spread exceeding the between-model difference. That is a
weaker headline but a true one, and it is itself a result: it says the
choice between LightGBM and XGBoost does not matter here, which is useful
to a practitioner deciding what to deploy.

**Reading the table.** `median CV` is the typical cell; `p90 CV` is the
tail — the cells a planner would notice moving. `WMAPE sd` is the
stability of the *aggregate* metric, which is systematically smaller than
per-cell CV because per-cell movements partly cancel in a sum. **Report
both**: aggregate stability flatters the system relative to what a user
of an individual forecast experiences.

**Measured gap: aggregate WMAPE moves by ~4.7% of its own level across
seeds, while the typical individual forecast moves by ~13% — roughly
three times more.** A planner reading one brand's number experiences the
second figure, not the first. Reporting only aggregate stability would
understate run-to-run variability by a factor of three.

