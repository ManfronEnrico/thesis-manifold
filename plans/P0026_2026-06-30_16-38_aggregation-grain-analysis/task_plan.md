---
pid: P0026
created: 2026-06-30 16:38:00
updated: 2026-06-30 16:38:00
status: complete
completed: 2026-06-30 17:30:00
outcome_summary: "Implemented brand×region×period grain (9 DVH geographic regions, MIN_PERIODS=24). CSD pipeline produces 25,124 rows / 571 series — 10.6× more training data than previous brand×period grain. All 6 pipeline steps confirmed working."
---

# P0026 — Aggregation Grain Analysis for Nielsen CSD

## Problem

Current pipeline aggregates 9M raw fact rows to brand×period (3,917 rows).
This enables brand-level forecasting only. Prometheus needs to answer
marketing-manager questions at SKU and channel level too.

Key question: what is the richest grain we can train on without hitting
sparsity walls that make ML unreliable?

## Context

- **Raw facts**: 9,080,538 rows × 32 cols (product × market × period × measures)
- **Dimensions**: 2,103 products, 86 markets, 44 periods, 140 brands
- **Current output**: brand × period → 3,917 rows, 55 brands survive ≥40 period filter
- **Prometheus goal**: answer SKU-level, channel-level, brand-level, category-level predictive questions

## Candidate Grains

| Grain | Theoretical max rows | Question capability |
|---|---|---|
| brand × period (current) | 140 × 44 = 6,160 | "Faxe Kondi next 6 months?" |
| brand × market × period | 140 × 86 × 44 = 530,320 | + "Faxe Kondi in Coop?" |
| SKU × period | 2,103 × 44 = 92,532 | + "Faxe Kondi 33cl next quarter?" |
| SKU × market × period | 2,103 × 86 × 44 = 7,956,648 | All of the above |

## Decision (confirmed 2026-06-30)

**Grain: brand × region × period**
- Filter facts to DVH EXCL. HD family (22 markets) — already done in Step 1
- Keep only the 9 geographic REG. 1–9 markets (mutually exclusive, sum to national)
- Exclude: size tiers (Superettes/Small/Large/Hypermarkets), aggregate rollups (EAST/WEST, DVH EXCL. HD national total, REGION 1-6 alternate naming)
- Rationale: regions are mutually exclusive → no double-counting; enables regional predictive questions; brand total = sum of regions
- Store size tier → Phase 2 (add as feature column, not grain dimension)
- MIN_PERIODS: lower from 40 → 24 (empirically defensible: 2 full years, captures seasonality twice)

**Why not SKU × market:** median 18 non-zero periods, only 19.7% survive ≥40 periods — too sparse
**Why not brand × all 22 DVH markets:** size tiers and rollups overlap with regions → double-counting

## Tasks

### T-1 ✓ — Sparsity diagnostics (COMPLETE)
Results in findings.md

### T-2 ✓ — Market structure analysis (COMPLETE)
86 markets = chains + regions + size tiers + rollups. 22 are DVH EXCL. HD family.

### T-3 ✓ — Grain recommendation (COMPLETE)
Decision: brand × region (9 geographic REG. 1–9) × period, MIN_PERIODS ≥ 24

### T-4 — Implement Step 1 aggregation change ← EXECUTE NOW
Files to change:
- `thesis/data/_02_preprocessing/nielsen/CSD/pre_csd_1_load_and_aggregate.py`
  - Add market_id to groupby
  - Filter to REG. 1–9 markets only (exclude size tiers + rollups)
  - Output grain: brand × market_id × period
- `thesis/data/_02_preprocessing/nielsen/CSD/pre_csd_3_filter_series.py`
  - Change groupby from `brand` to `[brand, market_id]` for period counting
  - Lower DEFAULT_MIN_PERIODS from 40 → 24
- Steps 2, 4, 5, 6: verify they handle the new grain (market_id passthrough)
- Re-run full CSD pipeline, verify ~50k rows in feature matrix

## Dependency Chain

T-1 + T-2 (parallel, done) → T-3 (done) → T-4 (executing)

## Key Files

- Facts parquet: `thesis/data/_01_converted/nielsen/parquet_nielsen/CSD/views/csd_clean_facts_v.parquet`
- Product dim: `thesis/data/_01_converted/nielsen/parquet_nielsen/CSD/views/csd_clean_dim_product_v.parquet`
- Market dim: `thesis/data/_01_converted/nielsen/parquet_nielsen/CSD/views/csd_clean_dim_market_v.parquet`
- Step 1 script: `thesis/data/_02_preprocessing/nielsen/CSD/pre_csd_1_load_and_aggregate.py`
