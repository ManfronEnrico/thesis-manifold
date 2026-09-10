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
| CSD | LightGBM | 0.182 | 0.488 | 18.9% | 0.67 | 18.3–20.0% |
| CSD | XGBoost | 0.152 | 0.517 | 18.6% | 0.83 | 17.8–19.5% |
| Danskvand | LightGBM | 0.138 | 0.522 | 27.0% | 2.81 | 24.6–31.9% |
| Danskvand | XGBoost | 0.174 | 0.611 | 25.8% | 1.04 | 24.7–27.0% |
| Energidrikke | LightGBM | 0.239 | 0.707 | 16.2% | 0.59 | 15.5–16.9% |
| Energidrikke | XGBoost | 0.243 | 0.773 | 17.0% | 1.08 | 15.5–18.0% |
| RTD | LightGBM | 0.099 | 0.236 | 30.5% | 0.30 | 30.2–30.9% |
| RTD | XGBoost | 0.114 | 0.522 | 30.1% | 1.04 | 29.1–31.6% |

## Does the selected model change with the seed?

The benchmark's output is not just an error figure -- it is a *choice* of
model per category. If that choice is seed-dependent, the selection is
not a finding.

| Category | winner per seed | verdict |
|---|---|---|
| CSD | XGBoost, XGBoost, XGBoost, LightGBM, LightGBM | **FLIPS** |
| Danskvand | LightGBM, LightGBM, XGBoost, XGBoost, XGBoost | **FLIPS** |
| Energidrikke | XGBoost, LightGBM, LightGBM, LightGBM, XGBoost | **FLIPS** |
| RTD | XGBoost, LightGBM, XGBoost, XGBoost, XGBoost | **FLIPS** |

**4 of 4 categories change their winning model on the seed
alone.** Every input is identical; only the random seed differs.

**Consequence for the write-up.** A statement of the form "model X is best
for category Y" is not supported where the winner flips -- it reports one
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

**Measured gap: aggregate WMAPE moves by ~4.6% of its own level across
seeds, while the typical individual forecast moves by ~17% -- about 3.6x
more.** A planner reading one brand's number experiences the second
figure, not the first. Reporting only aggregate stability would
understate run-to-run variability by roughly 4x.

