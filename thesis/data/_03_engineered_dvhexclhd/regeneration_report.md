# Feature-matrix regeneration report (DVH EXCL. HD, MIN_PERIODS=30)

_Regenerated and verified 2026-06-23 (autonomous Path B run)._

## Feature matrices (per category)

| Category | Brands | Periods | Grid rows | Observed rows | Split (tr/val/te) | Test window |
|---|---|---|---|---|---|---|
| CSD | 77 | 42 | 3234 | 3077 | 24/6/12 | 2025-04..2026-03 |
| danskvand | 24 | 37 | 888 | 885 | 23/6/8 | 2025-08..2026-03 |
| energidrikke | 27 | 39 | 1053 | 1007 | 25/6/8 | 2025-08..2026-03 |
| RTD | 42 | 37 | 1554 | 1543 | 23/6/8 | 2025-08..2026-03 |

Brand counts match the locked DVH EXCL. HD @ MIN_PERIODS=30 figures exactly.
Each matrix has 22 columns: brand, period_index/year/month, sales_units,
promo_units, weighted_distribution, lag_{1,2,3,4,8,13}, rolling_mean_4,
rolling_std_4, rolling_mean_13, month, quarter, holiday_month, log_sales_units,
promo_intensity, split. NaN in lag/rolling/target columns is by design (the
brand series are reindexed to the full monthly grid to expose gaps for correct
lag computation; grid_rows − observed = grid-filled NaN rows).

## Market double-count — corrected evidence

The 28–86 `market_description` values per category are HIERARCHICAL (individual
chains ⊂ group aggregates ⊂ grand-total roll-ups). Brian's inherited Step 1
summed across ALL of them, counting each sale at every level. Scoping to the
single Nielsen-recommended grand-total level `DVH EXCL. HD` removes the
double-count.

| Category | Market levels | ALL-markets sum | DVH EXCL. HD | Inflation |
|---|---|---|---|---|
| CSD | 28 | 1180.2B units | 191.6B units | **6.16×** |
| danskvand | 86 | 171.5B units | 11.6B units | **14.76×** |
| energidrikke | 86 | 269.4B units | 15.9B units | **16.92×** |
| RTD | 86 | 49.5B units | 3.4B units | **14.41×** |

⚠️ **Supersedes the earlier "5.24× / true 32.2B" figure** recorded in the project
journal: re-measured on the current `data/raw` snapshot, CSD DVH EXCL. HD = 191.6B
units (a legitimate grand-total level, comparable to DVH/CONVENIENCE INCL. HD =
225.2B and EXCL. HD = 207.0B), and the all-markets sum is 6.16× that. The 32.2B
figure does not reproduce and should not be cited in Ch4.

## EDA (recomputed under DVH EXCL. HD, observed rows only)

| Category | Promo correlation | Peak month | Top brand | Total units |
|---|---|---|---|---|
| CSD | r=0.937 (n=2442 promo rows) | December | HARBOE | 6.87B |
| danskvand | no promo data (all zero) | June | HARBOE | 0.14B |
| energidrikke | r=0.988 (n=887 promo rows) | March | RED BULL | 0.30B |
| RTD | no promo data (all zero) | December | BREEZER | 0.10B |

Notes:
- CSD promo r=0.937 (journal cited 0.941; minor drift from data refresh — use 0.937).
- danskvand & RTD carry no promotional data (an unmeasured-variable coverage
  limitation, to be framed as such in Ch4).
- Top CSD brand by units is HARBOE, not Coca-Cola (confirms the journal correction).
- Seasonality is sensible: CSD/RTD peak in December, danskvand (water) in June,
  energidrikke in March.

## Reproduction

```
.venv/bin/python thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py
```

Reads `data/raw/nielsen_<cat>_clean_{facts_v,dim_market,dim_product,dim_period}.parquet`,
applies the DVH EXCL. HD scope + MIN_PERIODS=30, writes the four matrices here.
Self-contained (no dependency on the deleted `PATHS.py` / parquet view cache).

## Canonical vs reference code

- **Canonical / runnable:** `thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py`
  (consolidated, reads `data/raw/` directly).
- **Reference only:** `thesis/data/_02_preprocessing/nielsen/<cat>/pre_<cat>_*.py`
  (Brian's modular step 0-6 files, restored from git). They carry the same
  DVH EXCL. HD fix in step 1 for readability, but are NOT currently runnable —
  they depend on `PATHS.py` and a parquet view cache that the repo refactor
  deleted. Restoring that infra is optional future work; the consolidated
  builder already produces the authoritative matrices.
