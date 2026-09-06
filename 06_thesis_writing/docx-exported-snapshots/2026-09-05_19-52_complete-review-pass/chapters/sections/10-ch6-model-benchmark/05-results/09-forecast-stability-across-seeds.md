# Forecast stability across seeds

> Section of **Model Benchmark & Selection > Results > Forecast stability across seeds**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**5 comment(s) on this section** -- VERIFY, METACOMMENT, PROSE, WATERMARK, ACADEMIC, TABLE-REFERENCE, NAMING. Detail: `comments/sections/10-ch6-model-benchmark/05-results/09-forecast-stability-across-seeds.md`

---

Chapter 2 motivates evaluating the modelling substrate on accuracy, computational efficiency and stability, and SRQ1’s scope names stability as its fourth axis. This section supplies that measurement, which had not previously been made.
Stability is measured as the coefficient of variation of the forecast for each (brand, month) cell across five random seeds, with data, splits, features and protocol held identical. Only the seed varies, driving Optuna’s sampler and the models’ own stochastic elements.
| Category | Model | median CV | p90 CV | WMAPE mean | WMAPE sd |
|---|---|---|---|---|---|
| CSD | LightGBM | 0.112 | 0.295 | 15.4% | 0.65 |
| CSD | XGBoost | 0.123 | 0.422 | 15.1% | 0.59 |
| danskvand | LightGBM | 0.119 | 0.687 | 20.8% | 0.69 |
| danskvand | XGBoost | 0.124 | 0.539 | 21.8% | 1.04 |
| energidrikke | LightGBM | 0.174 | 0.634 | 14.1% | 1.18 |
| energidrikke | XGBoost | 0.174 | 0.730 | 13.9% | 0.79 |
| RTD | LightGBM | 0.125 | 0.397 | 33.5% | 1.64 |
| RTD | XGBoost | 0.104 | 0.400 | 35.1% | 0.92 |
**Two findings, and both matter more than the accuracy tables suggest.**
First, aggregate stability flatters the system by roughly three times. Aggregate WMAPE moves by about 4.7% of its own level across seeds, while the *typical individual forecast* moves by about 13%, and the ninetieth-percentile cell by 30–73%. Per-cell movements partly cancel within a volume-weighted sum, so a planner reading one brand’s number experiences considerably more run-to-run variability than a headline metric implies. Both figures are therefore reported; quoting only the aggregate would understate instability threefold.
Second, and more consequentially for this chapter: the winning model changes with the seed in every category.
| Category | Winner per seed |  |
|---|---|---|
| CSD | XGBoost, XGBoost, LightGBM, XGBoost, LightGBM | flips |
| danskvand | LightGBM ×3, XGBoost, LightGBM | flips |
| energidrikke | LightGBM, LightGBM, XGBoost, LightGBM, LightGBM | flips |
| RTD | XGBoost, XGBoost, LightGBM, LightGBM, LightGBM | flips |
**Table** **16** - Seed Stabiltiy across Models and Categories
Every input is identical; only the random seed differs. A per-category statement of which gradient-boosting model is best is therefore not a finding - it reports the outcome of one seed. §6.6 states the conclusion this supports instead.
