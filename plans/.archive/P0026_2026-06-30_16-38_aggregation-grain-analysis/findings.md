# P0026 Findings — Aggregation Grain Analysis

## Sparsity Diagnostics (T-1) — COMPLETE

| Grain | Series | Fill% | Median periods | ≥24% | ≥40% | Rows |
|---|---|---|---|---|---|---|
| brand × period (all DVH) | 149 | 100% | 34 | 61.9% | 43.5% | 4,429 |
| brand × market × period (all 86) | 7,514 | 58.6% | 29 | 55.0% | 36.8% | 200,981 |
| SKU × period | 8,755 | 100% | 25 | 51.4% | 33.8% | 229,448 |
| SKU × market × period | 415,619 | 55.2% | 18 | 43.4% | 19.7% | 9,080,538 |

**After DVH EXCL. HD filter (22 markets):**
| brand × market × period | 2,623 | 82.8% | 30 | 55.5% | 38.2% | 72,379 |

## Market Dimension Structure (T-2) — COMPLETE

86 markets = 3 overlapping segmentation schemes:
- **9 geographic regions** (REG. 1–9): mutually exclusive, sum to national — CHOSEN
- **4 store size tiers** (Superettes/Small/Large/Hypermarkets): mutually exclusive — excluded (overlap with regions)
- **Aggregate rollups** (EAST/WEST, national DVH EXCL. HD total, chain-level): excluded (double-count)

## Recommendation (T-3) — COMPLETE

**Grain: brand × region (REG. 1–9) × period**
**MIN_PERIODS: 24** (2 full years, captures seasonality twice)

## Implementation Result (T-4) — COMPLETE

Pipeline ran successfully 2026-06-30. Final feature matrix:
- **27,086 rows** at Step 1 (brand × region × period, 140 brands × 9 regions × 44 periods)
- **45,716 rows** after Step 2 calendar fill (zero-fill for missing brand×region×month)
- **25,124 rows** after Step 3 filter (571 series surviving ≥24 non-zero periods, 78 brands)
- **25,124 rows** through Steps 4–6 (feature engineering + split)
- Split: train 14,275 / val 3,426 / test 7,423
- Output: `thesis/data/_03_engineered/nielsen/CSD/csd_feature_matrix.parquet`

**vs previous grain (brand × period):**
- 25,124 rows vs 2,365 rows — **10.6× more training data**
- 78 brands × 9 regions = 571 series vs 55 brands = 55 series
- Enables regional predictive questions for Prometheus
