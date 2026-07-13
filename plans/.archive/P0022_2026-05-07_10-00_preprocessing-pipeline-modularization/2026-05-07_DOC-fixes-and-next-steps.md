---
created: 2026-05-07 14:00:00
priority: HIGH
status: IN PROGRESS
---

# P0022 Fixes & Next Steps

**Current Status:** Phase 1 code complete, bugs found during testing, fixes needed before Phase 2

---

## 🔴 Critical Fixes (Do These First)

### Fix #1: Step 1 — Format Error in Date Range
**Task #10** | **Priority: BLOCKING** | Severity: HIGH

**Error:**
```
ValueError: Unknown format code 'd' for object of type 'float'
File "pre_csd_1_load_and_aggregate.py", line 132
print_info(f"Date range: {df['period_year'].min()}-{df['period_month'].min():02d}...")
```

**Root Cause:**
`df['period_month'].min()` returns a numpy float64, not an int. Format specifier `:02d` requires int.

**Fix:**
Cast to int before formatting:
```python
month_min = int(df['period_month'].min())
month_max = int(df['period_month'].max())
print_info(f"Date range: {df['period_year'].min()}-{month_min:02d} to {df['period_year'].max()}-{month_max:02d}")
```

**Apply to:**
- `pre_csd_1_load_and_aggregate.py` (line 132)
- `pre_csd_2_build_calendar.py` (line 164) — similar issue if present

---

### Fix #2: Step 1 — Load from Parquet Cache (if available)
**Task #9** | **Priority: BLOCKING** | Severity: HIGH

**Current Issue:**
Step 1 always loads from JSONL files, even though Step 0 just saved them to parquet. This is inefficient (15.79s to load JSONL when cached parquet would be ~2s).

**Desired Behavior:**
1. Check if Step 0 parquet outputs exist (`raw/csd_clean_facts.parquet`, etc.)
2. If yes → Load from cached parquet (fast)
3. If no → Fall back to JSONL files (slow but works)

**Implementation:**
In `pre_csd_1_load_and_aggregate.py`, modify `load_and_aggregate()` function:

```python
def load_and_aggregate(input_dir: Path, target_market: str, cached_parquet_dir: Path = None) -> pd.DataFrame:
    """
    Load Nielsen CSD data from parquet cache (if available) or JSONL files.
    
    Args:
        input_dir: JSONL input directory (fallback if no cache)
        target_market: Target market name
        cached_parquet_dir: Path to cached parquet files from step 0 (if any)
    """
    
    # Try to load from cached parquet first
    if cached_parquet_dir and (cached_parquet_dir / "csd_clean_facts.parquet").exists():
        print("  Loading view parquet files (cached from step 0)...")
        facts = pd.read_parquet(cached_parquet_dir / "csd_clean_facts_v.parquet")
        products = pd.read_parquet(cached_parquet_dir / "csd_clean_dim_product_v.parquet")
        periods = pd.read_parquet(cached_parquet_dir / "csd_clean_dim_period_v.parquet")
        markets = pd.read_parquet(cached_parquet_dir / "csd_clean_dim_market_v.parquet")
    else:
        # Fallback to JSONL
        print("  Loading view JSONL files...")
        facts = pd.read_json(input_dir / "csd_clean_facts_v.jsonl", lines=True)
        products = pd.read_json(input_dir / "csd_clean_dim_product_v.jsonl", lines=True)
        periods = pd.read_json(input_dir / "csd_clean_dim_period_v.jsonl", lines=True)
        markets = pd.read_json(input_dir / "csd_clean_dim_market_v.jsonl", lines=True)
    
    # Rest of logic unchanged...
```

**Apply to:**
- `pre_csd_1_load_and_aggregate.py` (entire function)

---

### Fix #3: Add Helper Functions to PATHS.py
**Task #11** | **Priority: HIGH** | Severity: MEDIUM

**Current Issue:**
Hard-coded paths in preprocessing_csd.py:
```python
SCRIPTS_DIR = ROOT_DIR / "thesis" / "data" / "preprocessing" / "nielsen" / CATEGORY
```

This repeats across all scripts. Should be centralized in PATHS.py.

**Add to PATHS.py:**

```python
def get_category_preprocessing_scripts_dir(category: str) -> Path:
    """
    Get the directory containing preprocessing scripts for a Nielsen category.
    
    Args:
        category: Category name (e.g., "CSD", "Energidrikke", "RTD", etc.)
    
    Returns:
        Path to thesis/data/preprocessing/nielsen/{category}/
    
    Example:
        >>> scripts_dir = get_category_preprocessing_scripts_dir("CSD")
        >>> print(scripts_dir / "pre_csd_0_cache.py")
    """
    return THESIS_DATA_PREPROCESSING_DIR / "nielsen" / category


def get_category_pipeline_step_outputs_dir(category: str) -> Path:
    """
    Get the directory for pipeline step intermediate outputs.
    
    Each step (1-6) saves its output parquet file here.
    
    Args:
        category: Category name
    
    Returns:
        Path to thesis/data/preprocessing/nielsen/{category}/pipeline_step_outputs/
    
    Example:
        >>> outputs_dir = get_category_pipeline_step_outputs_dir("CSD")
        >>> step1 = pd.read_parquet(outputs_dir / "step_1_aggregate.parquet")
    """
    return THESIS_DATA_PREPROCESSING_DIR / "nielsen" / category / "pipeline_step_outputs"
```

**Update all scripts to use:**
```python
from PATHS import get_category_preprocessing_scripts_dir, get_category_pipeline_step_outputs_dir

SCRIPTS_DIR = get_category_preprocessing_scripts_dir(CATEGORY)
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
```

**Apply to:**
- `PATHS.py` — Add the 2 new helper functions
- `preprocessing_csd.py` — Update SCRIPTS_DIR
- All 7 pre_csd_N_*.py scripts — Update STEP_OUTPUT_DIR

---

### Fix #4: Make --skip-raw the Default
**Task #12** | **Priority: HIGH** | Severity: MEDIUM

**Current Issue:**
Step 0 (caching raw data) is slow and optional. Currently runs by default. Should be skipped unless explicitly requested.

**Desired Behavior:**
```bash
python preprocessing_csd.py              # Skips step 0, runs steps 1-6
python preprocessing_csd.py --run-raw    # Includes step 0
python preprocessing_csd.py --run-step 0 # Runs only step 0
```

**Implementation in preprocessing_csd.py:**

Change arg parser:
```python
parser.add_argument(
    "--run-raw",
    action="store_true",
    help="Include step 0 (raw table caching) — slow, optional"
)
```

Change logic:
```python
def run_step(step_num: int, run_raw: bool = False) -> bool:
    if step_num == 0 and not run_raw:
        print(f"⊘ Skipping step 0 (use --run-raw to enable)")
        return False
    # ... rest unchanged
```

Change main():
```python
if args.run_step is not None:
    if args.run_step == 0 and not args.run_raw:
        print(f"Error: Step 0 requires --run-raw flag")
        sys.exit(1)
    run_step(args.run_step, run_raw=args.run_raw)
else:
    for step in STEPS:
        run_step(step, run_raw=args.run_raw)
```

**Apply to:**
- `preprocessing_csd.py` — Update argument parser and logic

---

## 📋 Fix Priority Order

1. **Fix #1 (Task #10):** Format error — 5 min — BLOCKS testing
2. **Fix #2 (Task #9):** Parquet caching — 15 min — Improves performance
3. **Fix #3 (Task #11):** PATHS.py helpers — 20 min — Code quality
4. **Fix #4 (Task #12):** --skip-raw default — 10 min — UX improvement

**Total time:** ~50 minutes

---

## ✅ After Fixes: Test Phase

**Task #13: Phase 1.5 Testing**

Once all fixes applied:
```bash
# Test 1: Full pipeline (skip raw by default)
python thesis/data/preprocessing/nielsen/CSD/preprocessing_csd.py

# Test 2: With raw caching
python thesis/data/preprocessing/nielsen/CSD/preprocessing_csd.py --run-raw

# Test 3: Individual steps
python thesis/data/preprocessing/nielsen/CSD/preprocessing_csd.py --run-step 1
python thesis/data/preprocessing/nielsen/CSD/preprocessing_csd.py --run-step 4

# Verify outputs
ls -la thesis/data/preprocessing/nielsen/CSD/engineered/
ls -la thesis/data/preprocessing/nielsen/CSD/pipeline_step_outputs/
```

**Success criteria:**
- ✅ All steps complete without errors
- ✅ Output files created: feature_matrix.parquet, series_index.csv, split_dates.json, report.md
- ✅ Timing logs recorded
- ✅ Rich terminal output displays correctly

---

## 🚀 Phase 2-4 Tasks

Once Phase 1.5 passes:

| Phase | Task | Description | Estimated Time |
|-------|------|-------------|-----------------|
| 2 | #14-17 | Apply pattern to 4 remaining categories | 2-3 hours |
| 3 | #18 | Master orchestrator preprocessing_all.py | 1 hour |
| 4 | #19-21 | Documentation (diagrams, guide, troubleshooting) | 1-2 hours |

**Total remaining:** 4-6 hours of work

---

## 🎯 Summary

**Current:** Phase 1 code is complete but has 4 bugs that block testing

**Next:** Fix bugs (#1-4) in priority order, test CSD end-to-end, then proceed to Phase 2

**Estimated:** ~1 hour for fixes + testing, then 2-3 hours for Phase 2 (remaining categories)

