# Review brief — Feature Build (pipeline stage 4)

> Hand-off for a fresh Claude Code session. Enrico wants to review the feature-build
> step, which currently feels like a black box. Read this, open the two files in
> **VS Code** (`/Users/enricomanfron/Downloads/Visual Studio Code.app`), and walk
> Enrico through them the way we did R1 (forecast models): explain what each step
> does, then flag anything worth a decision. Do NOT edit code during the review.

## What is being reviewed

Stage 4 of the SRQ1 pipeline (see the map: `harness/srq1_pipeline.png`). Two builders,
same logic, different grain:

- `thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py` — brand×month → `_03_engineered_dvhexclhd/`
- `thesis/data/preprocessing/nielsen_dvh/build_feature_matrix_bychain.py` — brand×chain → `_04_engineered_bychain/`

Input: the frozen snapshot `data/raw/nielsen_<cat>_clean_{facts_v,dim_market,dim_product,dim_period}.parquet`.
Output feeds the model benchmark (`scripts/srq1_benchmark_tuned.py`).

## Open these

```
open -a "/Users/enricomanfron/Downloads/Visual Studio Code.app" \
  thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py \
  thesis/data/preprocessing/nielsen_dvh/build_feature_matrix_bychain.py \
  harness/srq1_pipeline.png
```

## What the code does — the 7 steps (build_feature_matrix.py, 330 lines)

| Step | Where | What |
|---|---|---|
| Config | lines 92-93 | `MARKET_SCOPE = "DVH EXCL. HD"`, `MIN_PERIODS = 30` |
| 1-2 Load + scope | `load_scoped_facts()` L108; dedup L129-131; filter L133 | dedup market/product/period dims on their id, then keep ONLY the single `DVH EXCL. HD` market_id → cross-market double-count impossible by construction (the 6.16x fix) |
| 3 Aggregate | `aggregate_brand_month()` L156, groupby L159 | sum to brand×(year,month) |
| 4 Min-periods | `filter_min_periods()` L170 | keep brands with ≥30 observed months |
| 5 Grid | `reindex_to_grid()` L190 | reindex to a REGULAR monthly grid so a missing month doesn't turn a lag_1 into a calendar-lag_2 (L193-194) |
| 6 Features | `engineer_features()` L207 | lag_{1,2,3,4,8,13}, rolling_mean_4/std_4/mean_13, calendar (month/quarter/holiday_month), promo_intensity, `log_sales_units` (log target) |
| 7 Split | step 7 | forward-chaining train/val/test by date |
| 8 Save | | `{cat}_feature_matrix.parquet` + `{cat}_split_dates.json` + report |

Leakage-safety (docstring L44-46): `lag_k = sales_units.shift(k)`; rolling features on
`sales_units.shift(1)` (past only) → the current month never leaks into its own predictors.

## What to scrutinise with Enrico (the review flags)

1. **The DVH dedup + single-market filter (L129-133)** — the correctness keystone. Confirm the dedup is BEFORE the merge and that exactly one market_id is kept. This is what makes double-count impossible.
2. **Feature list (engineer_features, L207+)** — the 14 features are hard-coded here; the lag/window/holiday choices trace back to the EDA (`pre_csd_1.5_eda.py`). Confirm they match what Ch4/Ch6 claim.
3. **Grid reindex (L190)** — verify a brand with a gap month gets NaN (not a shifted lag). This is subtle and important for lag correctness.
4. **`fillna(0.0)` on features** happens later in the model script, not here — note that missing warmup lags become 0 at train time (already flagged in R1).
5. **The two-grain diff** — open `build_feature_matrix_bychain.py` side-by-side: the ONLY real difference is the groupby key (adds chain) and keeping the 11 leaf chains. Confirm nothing else diverges.
6. **MIN_PERIODS = 30** — feasible for all 4 categories (37-42 periods); 40 was infeasible for danskvand/energidrikke/RTD.

## Context you may need

- Pipeline map: `harness/srq1_pipeline.png` (stage 4 is this review)
- Harness / task list: `harness/thesis_tasks.json` (dashboard renders it)
- Prior R1 findings already logged: V1 (danskvand grain re-score), V2 (mean-MAPE)
- Locked decisions: `docs/handover/2026-07-01_enrico-to-brian-merge-handover.md` §2
- Market-scope fix rationale: journal + `_03_engineered_dvhexclhd/eda_findings_dvhexclhd.md`

## Output of the review

If new issues surface, add them to `harness/thesis_tasks.json` (track ENG-REVIEW,
status ready) the way V1/V2 were added, and note them here. Keep it read-only otherwise.
