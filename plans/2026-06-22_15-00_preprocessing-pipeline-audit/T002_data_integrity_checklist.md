---
name: T002-data-integrity-checklist
description: Cache reorganization verification and data source validation
created: 2026-06-22 16:30
updated: 2026-06-22 16:30
---

# T-002 Output: Data Source & Cache Reorganization Verification

## Summary

✅ **Cache verification PASSED** — All 4 required parquet view files exist at correct location

## Cache Location Verification

**Expected Location (from pre_csd_0_cache.py):**
```
thesis/data/converted/nielsen/parquet_nielsen/CSD/views/
```

**Actual Files Found:**
```
✓ csd_clean_facts_v.parquet          (73 MB)   - Fact table: sales transactions
✓ csd_clean_dim_product_v.parquet    (98 KB)   - Dimension: product/brand hierarchy
✓ csd_clean_dim_period_v.parquet     (3.6 KB)  - Dimension: time periods (Nielsen 4-4-5 calendar)
✓ csd_clean_dim_market_v.parquet     (2.3 KB)  - Dimension: retail outlet types
```

**Status**: ✅ All 4 files present and readable

## Cache Validation Details

| File | Size | Exists | Type | Purpose |
|------|------|--------|------|---------|
| csd_clean_facts_v.parquet | 73 MB | ✅ | Fact table | Sales units, promo units per brand×period |
| csd_clean_dim_product_v.parquet | 98 KB | ✅ | Dimension | Brand hierarchy, product codes |
| csd_clean_dim_period_v.parquet | 3.6 KB | ✅ | Dimension | Nielsen 4-4-5 calendar (period_year, period_month) |
| csd_clean_dim_market_v.parquet | 2.3 KB | ✅ | Dimension | Retail outlet types/markets |

## Path Resolution Verification

From `PATHS.py`:
```python
THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR = thesis/data/converted/nielsen/parquet_nielsen/
```

Cache directory: `{THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR}/CSD/views/`

✅ **Verified:** Path resolution correct; all files accessible

## Preprocessing Integration Check

From `pre_csd_0_cache.py` (lines 96-99):
```python
CACHE_VIEWS_DIR = THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"
# This resolves to: thesis/data/converted/nielsen/parquet_nielsen/CSD/views/
```

From `preprocessing_csd.py` orchestrator:
- ✅ Calls `pre_csd_0_cache.py` at startup to validate cache
- ✅ If cache missing, raises clear error with Stage 1 instructions
- ✅ If cache present, proceeds with Steps 1–6

## Post-June22-Fix Verification

**Previous Issue (before June 22):**
- Parquet cache at: `thesis/data/preprocessing/nielsen/CSD/views/`
- Expected by preprocessor: `thesis/data/converted/nielsen/parquet_nielsen/CSD/views/`
- Result: Path mismatch → "cache not found" error

**Current Status (post-June22-fix):**
- Parquet cache moved to: `thesis/data/converted/nielsen/parquet_nielsen/CSD/views/`
- Expected by preprocessor: Same location
- Result: ✅ **Cache location matches; no path errors**

## Data Schema Validation

From Stage 1 conversion (JSONL → Parquet):
- ✅ Facts table contains: brand, period_year, period_month, sales_units, promo_units
- ✅ Dimension tables present with expected columns
- ✅ No encoding errors; parquet format valid

## Reproducibility Check

- Cache files created: 2026-05-07 10:57 UTC
- Stable location: No relocation during audit
- File hashes: Consistent across multiple reads
- ✅ **Reproducible:** Same cache can be used across preprocessing runs

## Critical Findings

✅ **No blockers identified**

Cache reorganization complete and verified. Preprocessing pipeline can proceed without cache errors.

---

## Next Steps

✅ T-002 COMPLETE → Unblocks T-006 (Step 1 audit)

**Ready to audit:**
- T-003: Feature engineering (Step 4)
- T-004: Parameters
- T-005: Reproducibility
- T-006: Step 1 data integrity

---

**Status**: ✅ **T-002 COMPLETE**

Cache path mismatch resolved. All required parquet files present and accessible.

