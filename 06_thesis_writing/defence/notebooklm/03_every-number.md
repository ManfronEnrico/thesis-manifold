# Every number we might be asked for

> **Source file for NotebookLM.** Every figure here is read from
> `05_thesis_results/`, not from the thesis prose. Where the thesis and the
> artefact disagree, both are given and the disagreement is named.
>
> Useful for quiz and multiple-choice generation: each figure has one correct
> value and a stated unit.

## The scenario ladder — 63 funded runs, all seven scenarios

Source: `08_experimental_evaluation/tables/22_scenario_comparison.csv`.
Nine runs per scenario (3 brands × 3 repeats).

| Measure | A plain | B data+code | C model | D prod+code | E prod+model | F both | G prod+both |
|---|---:|---:|---:|---:|---:|---:|---:|
| Runs completed | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Usable answers | **6** | 9 | 9 | 9 | 9 | 9 | 9 |
| Median APE % | 502.2 | 2.9 | 14.6 | **0.9** | 14.6 | 7.3 | 1.8 |
| Mean APE % | 662.1 | 27.9 | **13.1** | 25.0 | 13.1 | 18.3 | 15.6 |
| CV across repeats % | 26.7 | 4.1 | **0.0** | 8.1 | **0.0** | 1.7 | 3.3 |
| Replicability % | 0 | 0 | **100** | 0 | **100** | 33 | 33 |
| Top-answer agreement | 0.33 | 0.44 | **1.00** | 0.56 | **1.00** | 0.67 | 0.78 |
| Tokens per answer | 60,566 | 39,420 | **1,165** | 109,228 | 30,168 | 38,437 | 81,827 |
| Cost/answer USD (est.) | 0.3798 | 0.4667 | **0.0091** | 0.7664 | 0.1994 | 0.4253 | 0.5536 |
| Response time s | 69.5 | 123.8 | **6.0** | 111.3 | 31.7 | 103.9 | 84.4 |

### The derived headline figures

- **51.3× cheaper** — C ($0.0091) against B ($0.4667). The thesis says "roughly fifty".
- **20.6× faster** — C (6.0 s) against B (123.8 s). The thesis says "roughly twenty".
- **Median error moves 502.2% → 2.9%** on the A→B step: data access.
- **B→C is worse on the median** (2.9 → 14.6) **and better on the mean** (27.9 → 13.1).

### Two things a careful reader will notice

1. **Scenario D is the most accurate rung on the median at 0.9%** — better than
   B. This is an orchestrator effect on the *code* path, not evidence for the
   dedicated model.
2. **Per-scenario costs are token estimates and therefore upper bounds.** The
   token estimate overshot actual billing by about 29 per cent.

## Cost of the evaluation

| Figure | Value | What it is |
|---|---:|---|
| Actual spend | **$19.60** | change in account balance across the two invocations — the only non-estimated figure |
| Token-based estimate | $25.20 | a 29% overshoot |
| Billing endpoint | $18.46 | one incomplete billing window; not comparable |
| Per run | ≈$0.31 | 19.60 / 63 |

A larger evaluation sizes directly from this: 4 brands × 5 repeats × 7 scenarios
= 140 runs ≈ $43.

## SRQ1 — statistical and linear baselines, weighted MAPE %

Source: `05_model_benchmark/tables/19_statistical_baselines.md`. Lower is better.

| Category | Naive | SeasonalNaive | Drift | Ridge | ARIMA | Prophet |
|---|---:|---:|---:|---:|---:|---:|
| CSD | 42.9 | **19.2** | 47.7 | 23.8 | 21.8 | 105.7 |
| Danskvand | 32.5 | 35.9 | 32.0 | 74.9 | 33.5 | **19.4** |
| Energidrikke | 18.9 | 23.8 | **17.7** | 23.6 | 19.4 | 975.0 |
| RTD | 89.3 | **27.3** | 95.9 | 52.4 | 53.3 | 66.8 |

**The uncomfortable fact, reported not buried:** a parameter-free benchmark wins
two of four categories — seasonal naive on CSD and RTD, Prophet on Danskvand.

**Prophet's variance is enormous**: best model on Danskvand at 19.4, and 975.0 on
Energidrikke. The explanation is that Prophet is built for daily series with
holiday effects; at monthly grain its holiday machinery gets no usable input.
Where the seasonal structure suits it, it wins; where it does not, it diverges.
That variance is itself an argument for selecting per category rather than
globally.

## SRQ1 — seed stability, and why no winner is named

Source: `20_seed_stability_p1.md`, `21_seed_stability_p2.md`. Five seeds per cell.

| Measure | Category | LightGBM | XGBoost |
|---|---|---:|---:|
| mean WMAPE % | CSD | 18.87 | 18.61 |
| mean WMAPE % | Danskvand | 27.01 | 25.80 |
| mean WMAPE % | Energidrikke | 16.24 | 16.95 |
| mean WMAPE % | RTD | 30.50 | 30.08 |
| sd of WMAPE (pp) | Danskvand | **2.81** | 1.04 |
| sd of WMAPE (pp) | CSD | 0.67 | 0.83 |

The gap between the families is 0.3 to 1.2 percentage points. The
between-seed standard deviation reaches **2.81 pp**. The difference is inside the
noise, so the defensible claim is that they are indistinguishable here.

## Memory — and an inconsistency inside the thesis

Source: `15_substrate_resource_profile.md`, measured on CSD by resident set size,
sampled every 5 ms in a separate process per model.

| | Ridge | LightGBM | XGBoost | ARIMA | Prophet |
|---|---:|---:|---:|---:|---:|
| Peak fit memory (MB) | 1.5 | 17.9 | **34.5** | 2.1 | 5.2 |
| Peak prediction memory (MB) | 0.02 | 0.07 | 0.65 | 0.11 | 1.73 |
| Fit time (s) | 0.008 | 1.758 | 1.679 | 0.04 | 11.373 |
| Prediction time (ms) | 2.2 | 15.5 | 11.8 | 4.7 | 95.3 |
| Share of 4096 MB budget (%) | 0.04 | 0.44 | **0.84** | 0.05 | 0.13 |
| Features | 18 | 18 | 18 | 1 | 1 |

⚠ **The submitted thesis reports two different figures for the same quantity.**
Chapter 9 says XGBoost 34.5 / LightGBM 17.9, matching the artefact above.
Chapter 6's Table 20 says XGBoost 31.9 / LightGBM 14.9, and Chapter 7 follows
Chapter 6. These are two profiling runs at different dates that were never
reconciled. Neither changes any conclusion — 0.84% versus 0.78% of budget — but
know which is which.

**End-to-end peak: ≈231 MB**, under 6 per cent of the budget. Composed of
~194 MB Python runtime and libraries, ~15 MB data, ~32 MB active model, <1 MB
coordinator state, and negligible for the agentic layer because the language
model runs remotely.

## Prediction intervals — the negative result

| Level | Coverage | Width, as a multiple of the forecast |
|---|---|---|
| 90% | 83.9–91.7% against a 90% target | **8 to 34×** — unusable everywhere |
| 80% | close to nominal for CSD, RTD, Energidrikke; ~6 pp below for Danskvand | **3 to 4×** for CSD, Danskvand, RTD; >10× for Energidrikke |

So there is an operating point at 80 per cent for three of four categories, and
none at 90 per cent anywhere. The guarantee is **marginal** — promised on average
across cells, not for any particular brand or month.

**The confidence index discriminates nothing.** Both of its terms are functions
of a quantile that is fixed within a category, so it returns values between 3 and
7 on a scale of 100 against a threshold of 40, and every forecast in every
category tiers "Low". Four attainable values exist across all brands. It is not
repairable by re-weighting or re-thresholding, because the quantity being
thresholded does not vary within a category.

## The panel

| | |
|---|---|
| Categories | 4 (CSD, Danskvand, Energidrikke, RTD) |
| Grain | brand × month |
| Periods | up to 44 monthly; 46 observations for CSD |
| Brands retained | 95 / 29 / 44 / 62 (CSD / Danskvand / Energidrikke / RTD) |
| Forecast horizon | 3 months (primary) |
| Features the model consumes | **18** |
| Retention threshold | derived, not chosen: `warmup + horizon + 1` = 17 at H=3 |

Promotional measures are reported for CSD and Energidrikke only. Where absent
the column is omitted, never zero-filled — a constant-zero column would assert
that no promotion ran.

## The 18 features

| Group | Columns |
|---|---|
| Lags | lag_1, lag_2, lag_3, lag_4, lag_8, lag_13 |
| Rolling | rolling_mean_4, rolling_std_4, rolling_mean_13 |
| Calendar | month, quarter, peak_month |
| Promotion | promo_intensity |
| Holiday | days_in_month, n_holidays, non_holiday_days |
| Intermittency | zero_run_flag, zero_run_length |

⚠ **No lag is a multiple of 12.** See `04_known-flaws.md`.

## The experiment's three brands

Chosen by volume stratification from the qualifying population — largest, median,
smallest. They span three orders of magnitude, roughly 2,850 to 6.4 million units
per month.

| Brand | Stratum | Scenario A error |
|---|---|---|
| HARBOE | max volume | 18.5% |
| 7-UP | median volume | 1305.8% |
| ØRBÆK | min volume | unscored — three failures |

Scenario A answered 120,000, 62,000 and 90,000 for a brand selling ~2,850 units.
Those are wrong by orders of magnitude, so they are **classified as failures
rather than scored** — averaging them would let an arbitrary number determine the
scenario's mean.

Three inclusion criteria, all applied before any run and identically to every
scenario: at least as many held-out months as the horizon; no zero months in the
held-out window; and at least 1,000 units in the scored month. The third is a
property of the *metric*, not the method — below roughly that volume, percentage
error is dominated by integer rounding. 14 of the 76 brands meeting the first two
criteria sell fewer than 100 units in the scored month.

## Citations and the library

88 items in the Zotero group library at the 2026-09-15 17:44 pull.
