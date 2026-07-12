# Monolithic-to-Modularized Conversion: Key Insights & Fixes

**Document:** 2026-05-14_DOC-monolithic-to-modularized-insights.md  
**Plan:** P0022 (Preprocessing Pipeline Modularization)  
**Status:** Reference guide for future category conversions and subagent work  
**Audiences:** Future developers, subagents handling other categories (Energidrikke, Danskvand, RTD, Totalbeer)

---

## Overview

This document captures critical architectural insights, design decisions, and "fixes" discovered during the conversion of the monolithic Nielsen CSD preprocessing script (`preprocessing_csd.py`) into modularized steps (Step 0: validation, Step 1: load & aggregate, Steps 2-6: feature engineering).

These insights apply to all Nielsen categories and should guide future subagent work.

---

## 1. Architecture: Two-Stage Separation

### The Key Insight

**Stage 1 (JSONL → Parquet Conversion)** and **Stage 2 (Parquet preprocessing)** must be cleanly separated:

| Component | Responsibility | Why |
|-----------|-----------------|-----|
| **Stage 1: run_all_conversions.py** | Convert raw JSONL → Parquet views | Handles OOM gracefully, memory management, large files |
| **Stage 2, Step 0: pre_csd_0_cache.py** | Validate parquet cache exists | Checkpoint, fail-fast, clear instructions |
| **Stage 2, Step 1-6: Preprocessing steps** | Load, engineer, feature, split, index | Assume cache is valid, no fallbacks |

### Why This Matters

- JSONL files are **too large** to handle in downstream steps (Totalbeer causes OOM)
- Stage 1 orchestrator already has proper memory management and error recovery
- Downstream steps should **not duplicate** Stage 1 logic
- Clean separation → modular, testable, maintainable

### Implementation

✅ Step 1 now **only reads parquet** (no JSONL fallback)  
✅ Step 1 **calls Step 0** to validate cache first  
✅ Step 1 **assumes validation passed** → no defensive checks needed

---

## 2. Market Dimension: Include ALL Data, Don't Filter

### The Mistake (Fixed)

Original monolithic `preprocessing_csd.py` had:

```python
# Join facts × product × period × market
df = df.merge(markets[["market_id", "market_description"]], on="market_id")

# Filter to target market ❌ WRONG
df = df[df["market_description"] == TARGET_MARKET].copy()
```

This filtered to only one market type ("DVH EXCL. HD"), losing ~95% of the data.

### Why This Was Wrong

1. **Nielsen market_description** = retail outlet types (28 types: REMA 1000, NETTO, e-commerce, etc.)
   - NOT a country filter (data is already Denmark)
   - Represents different sales channels, not geographies

2. **Aggregation should combine across all channels**, not pick one

3. **Later feature engineering** needs complete data to work properly

### The Fix

✅ Join the market dimension (to have complete context)  
✅ **Do NOT filter by market** — aggregate across all market types  
✅ Retain all sales data from all 28 outlet channels

### Example Impact

- **Before:** ~500 rows (one market only)
- **After:** ~1,200 rows (all markets, combining across outlet types)

### Implementation in Step 1

```python
# Join facts × product × period × market (complete merged dataset)
df = facts.merge(products[["product_id", "brand"]], on="product_id")
df = df.merge(periods[["period_id", "period_year", "period_month"]], on="period_id")
df = df.merge(markets[["market_id", "market_description"]], on="market_id")
# ✅ NO market filtering — aggregate across all market types
```

---

## 3. Complete Dataset Join Before Aggregation

### The Insight

All dimensions must be **joined before aggregating**, even if you don't filter on them:

```python
# ✓ CORRECT: Join all 4 tables, THEN aggregate
df = facts.merge(products[["product_id", "brand"]], on="product_id")
df = df.merge(periods[["period_id", "period_year", "period_month"]], on="period_id")
df = df.merge(markets[["market_id", "market_description"]], on="market_id")
df = df[df["sales_units"] > 0].copy()
aggregated = df.groupby(["brand", "period_year", "period_month"]).agg(agg_dict).reset_index()

# ✗ WRONG: Aggregate without all context
df = facts.merge(products[...])
df = df.merge(periods[...])
# Missing market context!
aggregated = df.groupby(["brand", "period_year", "period_month"]).agg(...)
```

### Why This Matters

1. **Preserves complete context** — Each fact row includes which product, period, market
2. **Enables filtering logic** — Can decide to filter or aggregate based on complete info
3. **Future-proof** — If downstream steps need market info, it's there
4. **Nielsen schema design** — Dimensions exist for a reason; use them

---

## 4. Validation Checkpoint (Step 0) as Architectural Gate

### The Pattern

Every modularized step should **delegate validation to its predecessor**:

```
Step 0 (pre_csd_0_cache.py)
  └─ Validates: Parquet cache exists
  └─ Fails: Hard-fail with instructions
  └─ Output: Boolean (valid/invalid)

Step 1 (pre_csd_1_load_and_aggregate.py)
  └─ Calls: validate_parquet_cache() from Step 0
  └─ Assumes: If Step 0 passed, cache is valid
  └─ No fallbacks: Only reads parquet
  └─ Fails: Graceful abort if Step 0 validation fails
```

### Why This Matters

- **Single responsibility** — Step 0 owns validation logic
- **No code duplication** — Step 1 doesn't re-validate
- **Clear failure modes** — Validation errors point to Stage 1 (JSONL → Parquet conversion)
- **Modularity** — Steps can be tested independently once prerequisites pass

### Implementation

```python
# Step 1 imports and calls Step 0 validator
from pre_csd_0_cache import validate_parquet_cache

validation = validate_parquet_cache(CATEGORY, CACHE_VIEWS_DIR)
if not validation["valid"]:
    print("Step 0 validation failed. Run Stage 1 first.")
    return
```

---

## 5. Function Signature Simplification

### Before (Over-parameterized)

```python
def load_and_aggregate(input_dir: Path, target_market: str, 
                       cached_parquet_dir: Path = None) -> pd.DataFrame:
    # Conditional logic: parquet vs. JSONL fallback
    # Market filtering logic
    # Complex branching
```

### After (Minimal, Clear)

```python
def load_and_aggregate(parquet_dir: Path) -> pd.DataFrame:
    # Single input source (parquet only)
    # No filtering logic (aggregates all markets)
    # Straightforward: load → merge → aggregate
```

### Why Simpler is Better

- **Fewer parameters** = fewer edge cases
- **Single responsibility** = easier to test
- **Clear intent** = easier to understand
- **Harder to misuse** = less room for bugs

---

## 6. Comprehensive Docstrings for Thesis Submission

### Standards Applied to All Steps

Every step should have:

1. **Module docstring** (lines 1-40)
   - PURPOSE: What does this step do?
   - INPUT: Which files, where?
   - OUTPUT: Which files, where?
   - LOGIC: Step-by-step workflow
   - DEPENDENCIES: What must run first?
   - USAGE: How to run it?

2. **Function docstring** (PARAMETERS, RETURNS, NOTES)
   ```python
   def load_and_aggregate(parquet_dir: Path) -> pd.DataFrame:
       """
       Load Nielsen CSD parquet view files and merge into complete dataset.

       PARAMETERS
       ----------
       parquet_dir : Path
           Directory containing all 4 Nielsen CSD view parquet files.

       RETURNS
       -------
       pd.DataFrame
           Aggregated data with columns: brand, period_year, period_month,
           sales_units, sales_value, sales_liters, promo_units, weighted_dist

       NOTES
       -----
       All 4 Nielsen view tables are merged to create complete context before
       aggregation. Data is aggregated to brand × period granularity, combining
       sales across all market types (retail outlet channels).
       """
   ```

3. **Inline comments** for non-obvious logic
   ```python
   # Join facts × product × period × market to create complete merged dataset.
   # All dimensions are joined to preserve complete context before aggregation.
   df = facts.merge(products[["product_id", "brand"]], on="product_id")
   ```

### Why This Matters

- **Thesis submission requirement** — Examiners expect clear documentation
- **Future maintenance** — Developers can understand intent without reading code
- **Reproducibility** — Steps are self-documenting

---

## 7. Section Structure in Main Flow

### Pattern for All Steps

```python
def main():
    with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
        step_start = time.perf_counter()

        # ────────────────────────────────────────────────────────────────────
        # VALIDATION PHASE
        # ────────────────────────────────────────────────────────────────────
        # Call predecessor step, check assumptions

        # ────────────────────────────────────────────────────────────────────
        # LOADING/PROCESSING PHASE
        # ────────────────────────────────────────────────────────────────────
        # Core business logic

        # ────────────────────────────────────────────────────────────────────
        # SAVING PHASE
        # ────────────────────────────────────────────────────────────────────
        # Write outputs

        # ────────────────────────────────────────────────────────────────────
        # PREVIEW & LOGGING PHASE
        # ────────────────────────────────────────────────────────────────────
        # Print summaries, record timing
```

### Why This Helps

- **Consistent flow** across all steps
- **Easy to follow** — readers know where validation, core logic, output, logging happen
- **Reusable template** for subagents implementing other categories

---

## 8. Configuration Constants & Path Management

### Pattern

```python
CATEGORY = "CSD"
STEP_NUM = 1
STEP_NAME = "Load and Aggregate"

# Dynamic paths from PATHS.py
CACHE_VIEWS_DIR = THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
```

### Why Important

- **PATHS.py is single source of truth** — Changes to folder structure propagate automatically
- **Constants are importlib-reloaded** — Ensures latest config during development
- **Category is centralized** — Easy to convert to other categories (just change CATEGORY = "Energidrikke")

---

## 9. Logging & Timing Infrastructure

### Every Step Should Log

```python
from thesis.data.preprocessing.nielsen.shared.timing_utils import log_step_timing
from thesis.data.preprocessing.nielsen.shared.terminal_utils import (
    step_execution, print_file_load, print_file_save, print_data_preview, print_step_summary
)

# Measure elapsed time
step_start = time.perf_counter()
# ... do work ...
step_elapsed = time.perf_counter() - step_start

# Log to JSON
log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, output_shape[0], LOG_FILE,
               input_cols=None, output_cols=output_shape[1])
```

### Why Important

- **Audit trail** — When did this step run, how long, how many rows?
- **Performance monitoring** — Track which steps are bottlenecks
- **Reproducibility** — Timestamps and row counts for thesis verification
- **Debugging** — If something changes, logs show what and when

---

## 10. Insights for Future Categories (Energidrikke, RTD, etc.)

### Template to Reuse

Use the refactored CSD steps as a template for other Nielsen categories:

```
1. Copy pre_csd_0_cache.py → pre_energidrikke_0_cache.py
   - Change CATEGORY = "CSD" to "Energidrikke"
   - Change "csd_" prefixes to "energidrikke_"
   - Logic stays the same (validation of parquet cache)

2. Copy pre_csd_1_load_and_aggregate.py → pre_energidrikke_1_load_and_aggregate.py
   - Change CATEGORY, STEP_NUM, STEP_NAME
   - Change "csd_" prefixes to "energidrikke_"
   - Logic stays the same (load, merge, aggregate)
   - Join ALL 4 dimensions (facts, product, period, market)
   - NO market filtering
   - Only read parquet (no JSONL)
```

### Key Constants to Parameterize

```python
# These change per category:
CATEGORY = "Energidrikke"  # or "RTD", "Danskvand", "Totalbeer"
STEP_NUM = 1
STEP_NAME = "Load and Aggregate"

# These stay the same (PATHS.py handles them):
CACHE_VIEWS_DIR = THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"
```

### Subagent Instructions for Category Conversion

When subagents implement other categories, they should:

1. ✅ Use the CSD steps as template
2. ✅ Remember: Join ALL 4 dimensions (don't skip market)
3. ✅ Remember: No market filtering (aggregate across all outlet types)
4. ✅ Remember: Only read parquet, no JSONL fallback
5. ✅ Remember: Call predecessor step for validation
6. ✅ Remember: Include comprehensive docstrings for thesis submission
7. ✅ Remember: Use PATHS.py for all paths (category-agnostic)
8. ✅ Remember: Log timing and row counts

---

## 11. Summary: The Five Core Fixes

| Fix | Before | After | Why |
|-----|--------|-------|-----|
| **Stage separation** | Step 1 had JSONL fallback | Only reads parquet, relies on Stage 1 | JSONL is too large, OOM risk |
| **Market filtering** | Filtered to one market type | Aggregates across all 28 market types | Market = outlet channel, not geography; want complete data |
| **Validation pattern** | Self-validates inputs | Calls Step 0, assumes validation passed | Clear responsibility, no duplication |
| **Table joins** | Skipped market dimension | Joins all 4 dimensions | Complete context before aggregation |
| **Function signature** | 3 parameters, complex logic | 1 parameter, clear intent | Single responsibility, easier to test |

---

## 12. Checklist for Future Category Conversions

### Before Running a New Category's Steps:

- [ ] Understand Nielsen schema (facts + 3 dimension tables)
- [ ] Know that market_description = retail outlet types (28 types)
- [ ] Know that market = NOT a country/geography filter
- [ ] Confirm Stage 1 (JSONL → Parquet) has run for this category
- [ ] Confirm Step 0 validation passes (parquet cache exists)
- [ ] Review these insights (especially points 2, 3, 4, 5)

### When Implementing New Steps:

- [ ] Start with CSD template
- [ ] Change CATEGORY constant
- [ ] Change "csd_" prefixes
- [ ] Join ALL 4 dimensions (no skipping market)
- [ ] Do NOT filter by market
- [ ] Do NOT add JSONL fallback
- [ ] Include comprehensive docstrings
- [ ] Log timing and row counts
- [ ] Test with `python pre_<category>_<step>_<name>.py`

---

## References

- **Monolithic reference:** thesis/data/preprocessing/preprocessing_csd.py
- **Step 0 (validation):** thesis/data/preprocessing/nielsen/CSD/pre_csd_0_cache.py
- **Step 1 (load & aggregate):** thesis/data/preprocessing/nielsen/CSD/pre_csd_1_load_and_aggregate.py
- **Stage 1 orchestrator:** thesis/data/converted/nielsen/jsonl_to_parquet/run_all_conversions.py
- **Shared utilities:** thesis/data/preprocessing/nielsen/shared/{terminal_utils,timing_utils}.py
- **Path configuration:** PATHS.py (single source of truth)

---

**Last Updated:** 2026-05-14  
**Status:** Complete — ready for reference during future category conversions and subagent work
