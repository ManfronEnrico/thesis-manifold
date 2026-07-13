# Step Script Template: pre_{category}_{N}_{name}.py

This template shows the structure and terminal utilities for a single preprocessing step.

## Example: pre_csd_2_build_calendar.py

```python
#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 2: Build Calendar

Input:  Step 1 output (aggregate.parquet)
        - Brand-period aggregation with sales units, value, etc.

Output: Step 2 output (calendar_filled.parquet)
        - Same data but with all months from 2022-10 to 2026-03 (gaps filled with NaN)

Logic:
  - Create full date range (monthly granularity, 2022-10 to 2026-03)
  - Outer join with aggregated data
  - NaN indicates zero/missing sales for that brand-month
"""

import sys, time
from pathlib import Path
import pandas as pd
from datetime import datetime

# Find project root
current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        ROOT_DIR = current
        break
    current = current.parent
else:
    raise FileNotFoundError("Could not find project root")

sys.path.insert(0, str(ROOT_DIR))

from PATHS import THESIS_DATA_PREPROCESSING_DIR
from thesis.data.preprocessing.nielsen.shared.terminal_utils import (
    step_execution, print_file_load, print_file_save, print_data_preview,
    print_step_summary, print_info, print_warning
)
from thesis.data.preprocessing.nielsen.shared.timing_utils import log_step_timing

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_NUM = 2
STEP_NAME = "Build Calendar"

# Input/Output paths (explicit naming convention)
STEP_DIR = THESIS_DATA_PREPROCESSING_DIR / "nielsen" / CATEGORY / "pipeline_step_outputs"
INPUT_AGGREGATE_PARQUET = STEP_DIR / f"step_1_aggregate.parquet"
OUTPUT_CALENDAR_FILLED_PARQUET = STEP_DIR / f"step_2_calendar_filled.parquet"
LOG_FILE = STEP_DIR / f"step_{STEP_NUM}_log.json"

# Feature engineering constants (from engineer_features.py)
DEFAULT_CALENDAR_START = (2022, 10)
DEFAULT_CALENDAR_END = (2026, 3)

# ============================================================================
# STEP LOGIC
# ============================================================================

def build_calendar_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill calendar gaps in aggregated data.
    
    Input: df with (brand, period_year, period_month, sales_units, ...)
    Output: df with all months 2022-10 to 2026-03, NaN for missing months
    """
    # Create full date range
    months = pd.period_range(
        start=f"{DEFAULT_CALENDAR_START[0]}-{DEFAULT_CALENDAR_START[1]:02d}",
        end=f"{DEFAULT_CALENDAR_END[0]}-{DEFAULT_CALENDAR_END[1]:02d}",
        freq="M"
    )
    
    # Create full index (brand × month)
    brands = df["brand"].unique()
    full_index = pd.MultiIndex.from_product(
        [brands, months],
        names=["brand", "period"]
    )
    
    # Reindex df to fill missing months
    df = df.set_index(["brand", "period_year", "period_month"])
    # ... join logic ...
    df = df.reset_index()
    
    return df

def main():
    """Execute step 2: Build Calendar."""
    with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
        step_start = time.perf_counter()
        
        # ── Validate Input ──────────────────────────────────────────────────
        if not INPUT_AGGREGATE_PARQUET.exists():
            raise FileNotFoundError(f"Input missing: {INPUT_AGGREGATE_PARQUET}")
        
        # ── Load ────────────────────────────────────────────────────────────
        print("Loading aggregate data from step 1...")
        load_start = time.perf_counter()
        df = pd.read_parquet(INPUT_AGGREGATE_PARQUET)
        load_elapsed = time.perf_counter() - load_start
        
        input_shape = df.shape
        print_file_load(INPUT_AGGREGATE_PARQUET, input_shape, load_elapsed)
        
        print_info(f"Date range: {df['period_year'].min()}-{df['period_month'].min():02d} to {df['period_year'].max()}-{df['period_month'].max():02d}")
        print_info(f"Unique brands: {df['brand'].nunique()}")
        
        # ── Process ─────────────────────────────────────────────────────────
        print(f"\nBuilding calendar index ({DEFAULT_CALENDAR_START[0]}-{DEFAULT_CALENDAR_START[1]:02d} to {DEFAULT_CALENDAR_END[0]}-{DEFAULT_CALENDAR_END[1]:02d})...")
        process_start = time.perf_counter()
        
        df = build_calendar_index(df)
        
        process_elapsed = time.perf_counter() - process_start
        print(f"  ✓ Calendar filled in {process_elapsed:.2f}s")
        
        # ── Save ────────────────────────────────────────────────────────────
        print(f"\nSaving calendar-filled data...")
        STEP_DIR.mkdir(parents=True, exist_ok=True)
        
        save_start = time.perf_counter()
        df.to_parquet(OUTPUT_CALENDAR_FILLED_PARQUET, index=False)
        save_elapsed = time.perf_counter() - save_start
        
        output_shape = df.shape
        print_file_save(OUTPUT_CALENDAR_FILLED_PARQUET, output_shape, save_elapsed)
        
        # ── Preview ─────────────────────────────────────────────────────────
        print("\nData preview:")
        print_data_preview(df, title=f"{CATEGORY} Calendar-Filled Data", max_rows=10)
        
        # ── Summary ─────────────────────────────────────────────────────────
        step_elapsed = time.perf_counter() - step_start
        log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, output_shape[0], LOG_FILE)
        
        print_step_summary(
            STEP_NUM, STEP_NAME, step_elapsed,
            input_rows=input_shape[0],
            output_rows=output_shape[0]
        )

if __name__ == "__main__":
    main()
```

## Key Features Demonstrated

### 1. **Rich Progress/Summary Output**
```python
with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
    # Automatically prints header and timing
```

### 2. **Formatted File I/O Messages**
```python
print_file_load(INPUT_AGGREGATE_PARQUET, df.shape, load_elapsed)
print_file_save(OUTPUT_CALENDAR_FILLED_PARQUET, df.shape, save_elapsed)
# Outputs: ✓ Loaded: step_1_aggregate.parquet • 3,789 rows × 8 cols • 412.5 KB • 0.23s
```

### 3. **Info/Warning Messages**
```python
print_info(f"Date range: 2022-10 to 2026-03")
print_warning("Some brands have <30 non-zero periods")
```

### 4. **Data Preview as Table**
```python
print_data_preview(df, title="CSD Calendar-Filled Data", max_rows=10)
# Displays rich formatted table in terminal
```

### 5. **Summary Panel**
```python
print_step_summary(STEP_NUM, STEP_NAME, elapsed, input_rows, output_rows)
# Outputs box with step timing and row counts
```

## Expected Terminal Output

```
================================================================================
Nielsen CSD — Step 2: Build Calendar
================================================================================

Loading aggregate data from step 1...
✓ Loaded: step_1_aggregate.parquet • 3,789 rows × 8 cols • 412.5 KB • 0.23s
ℹ INFO: Date range: 2022-10 to 2026-03
ℹ INFO: Unique brands: 136

Building calendar index (2022-10 to 2026-03)...
  ✓ Calendar filled in 1.45s

Saving calendar-filled data...
✓ Saved: step_2_calendar_filled.parquet • 5,712 rows × 8 cols • 585.2 KB • 0.18s

Data preview:
┏━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┓
┃ brand ┃ date     ┃ sales_u ┃ sales_va ┃
┡━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━┩
│ 1724  │ 2022-10  │ 525.79  │ 9861.23  │
│ 1724  │ 2022-11  │ 433.32  │ 7926.89  │
│ 1724  │ 2022-12  │ 1076.21 │ 25073.00 │
└───────┴──────────┴─────────┴──────────┘

╭─────────────────────────────────────────────────────┬───────────────────╮
│ Summary                                             │      cyan         │
├─────────────────────────────────────────────────────┼───────────────────┤
│ Step 2: Build Calendar                              │                   │
│ Elapsed: 1.86s                                      │                   │
│ Input rows: 3,789                                   │                   │
│ Output rows: 5,712                                  │                   │
╰─────────────────────────────────────────────────────┴───────────────────╯

✓ Completed in 1.86s
```

## All Available Utilities

From `terminal_utils.py`:

- **Context managers:** `step_execution()`, `progress_bar()`
- **File I/O:** `print_file_load()`, `print_file_save()`
- **Data:** `print_data_preview()`, `print_timing_summary()`
- **Feedback:** `print_info()`, `print_warning()`, `print_error()`
- **Summaries:** `print_step_summary()`, `print_orchestrator_complete()`, `print_master_summary()`

See `terminal_utils.py` for full docstrings and usage.
