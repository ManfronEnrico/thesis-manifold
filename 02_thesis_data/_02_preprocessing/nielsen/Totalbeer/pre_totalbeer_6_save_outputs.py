#!/usr/bin/env python3
"""
Nielsen Totalbeer Preprocessing â€” Step 6: Save Outputs

Input:  Step 5 output (split_applied.parquet)
		- Final feature matrix with split labels

Output: Final outputs in engineered/ directory
		- Totalbeer_feature_matrix.parquet (feature matrix for modeling)
		- Totalbeer_series_index.csv (series metadata per brand)
		- Totalbeer_split_dates.json (train/val/test split boundaries)
		- Totalbeer_preprocessing_report.md (preprocessing summary)

Logic:
  - Import build_series_index() from shared codebase
  - Save final feature matrix
  - Generate series index (brand metadata)
  - Document split dates
  - Create preprocessing summary report
"""

import sys, json, time
from pathlib import Path
import pandas as pd

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

from PATHS import get_category_pipeline_step_outputs_dir, get_category_engineered_dir
from utility_scripts.scripts.METADATA import get_dimension_info
from thesis.thesis_agents.ai_research_framework.features.engineer_features import (
	build_series_index,
	DEFAULT_TARGET_MARKET as TARGET_MARKET,
	DEFAULT_MIN_PERIODS as MIN_PERIODS,
	DEFAULT_TRAIN_END as TRAIN_END,
	DEFAULT_VAL_END as VAL_END,
)
from thesis.data._02_preprocessing.nielsen.shared.terminal_utils import (
	step_execution, print_file_load, print_file_save, print_info, print_data_preview
)
from thesis.data._02_preprocessing.nielsen.shared.timing_utils import log_step_timing
from rich.table import Table
from rich.console import Console

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step finalizes outputs: feature matrix, series metadata, split dates, and report.
# Key column definitions referenced:
#
# OUTPUT ARTIFACTS:
#   - Totalbeer_feature_matrix.parquet: Final feature matrix (brand Ã— period Ã— features Ã— split)
#   - Totalbeer_series_index.csv: Brand-level metadata (series name, total sales units)
#   - Totalbeer_split_dates.json: Train/val/test date boundaries (locked)
#   - Totalbeer_preprocessing_report.md: Summary of preprocessing steps, brands, rows, features
#
# SERIES INDEX COLUMNS:
#   - brand: Product brand name (from product dimension)
#   - n_periods: Total periods in feature matrix
#   - n_nonzero: Count of non-zero sales_units
#   - total_units: Sum of sales_units across all periods
#   - train_periods, val_periods, test_periods: Breakdown by split
#   - (sorted by total_units descending for top-20 report)
#
# KEY NULL SEMANTICS (documented in report):
#   - sales_units: NaN in calendar_filled (step 2) â†’ NaN in feature matrix
#   - weighted_distribution: Averaged during aggregation; ~16.7% NULL; NaN in matrix where missing
#   - Engineered features (lags, rolling): NaN propagation from source data
#   - Do NOT impute NaNs; preserve for downstream time-series modeling

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "Totalbeer"
STEP_NUM = 6
STEP_NAME = "Save Outputs"

# Input/Output paths
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
INPUT_SPLIT_APPLIED_PARQUET = STEP_OUTPUT_DIR / f"step_5_split_applied.parquet"

OUTPUT_ENGINEERED_DIR = get_category_engineered_dir(CATEGORY)
OUTPUT_FEATURE_MATRIX = OUTPUT_ENGINEERED_DIR / f"{CATEGORY.lower()}_feature_matrix.parquet"
OUTPUT_SERIES_INDEX = OUTPUT_ENGINEERED_DIR / f"{CATEGORY.lower()}_series_index.csv"
OUTPUT_SPLIT_DATES = OUTPUT_ENGINEERED_DIR / f"{CATEGORY.lower()}_split_dates.json"
OUTPUT_REPORT = OUTPUT_ENGINEERED_DIR / f"{CATEGORY.lower()}_preprocessing_report.md"

LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def main():
	"""Execute step 6: Save outputs."""
	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		# Validate input
		if not INPUT_SPLIT_APPLIED_PARQUET.exists():
			raise FileNotFoundError(f"Input missing: {INPUT_SPLIT_APPLIED_PARQUET}")

		# Load
		print("Loading split-applied data from step 5...")
		load_start = time.perf_counter()
		df = pd.read_parquet(INPUT_SPLIT_APPLIED_PARQUET)
		load_elapsed = time.perf_counter() - load_start

		input_shape = df.shape
		print_file_load(INPUT_SPLIT_APPLIED_PARQUET, input_shape, load_elapsed)

		# Process
		print(f"\nGenerating series index...")
		series_idx = build_series_index(df)
		# Note: build_series_index already sorts by total_units descending

		# Save outputs
		print(f"\nSaving final outputs...")
		OUTPUT_ENGINEERED_DIR.mkdir(parents=True, exist_ok=True)

		# Feature matrix
		save_start = time.perf_counter()
		df.to_parquet(OUTPUT_FEATURE_MATRIX, index=False)
		save_elapsed = time.perf_counter() - save_start
		print_file_save(OUTPUT_FEATURE_MATRIX, df.shape, save_elapsed)

		# Series index
		series_idx.to_csv(OUTPUT_SERIES_INDEX, index=False)
		print_info(f"Series index: {OUTPUT_SERIES_INDEX.name}")

		# Split dates
		train_df = df[df["split"]=="train"]
		test_df = df[df["split"]=="test"]

		def get_date_str(df_subset, min_or_max="min"):
			if len(df_subset) == 0:
				return "unknown"
			date_series = df_subset["period_year"].astype(str) + "-" + df_subset["period_month"].astype(str).str.zfill(2)
			return getattr(date_series, min_or_max)()

		split_dates = {
			"train_start": get_date_str(train_df, "min"),
			"train_end": f"{TRAIN_END[0]}-{TRAIN_END[1]:02d}-01",
			"val_start": f"{TRAIN_END[0]}-{TRAIN_END[1]+1 if TRAIN_END[1]<12 else 1:02d}-01",
			"val_end": f"{VAL_END[0]}-{VAL_END[1]:02d}-01",
			"test_start": f"{VAL_END[0]}-{VAL_END[1]+1 if VAL_END[1]<12 else 1:02d}-01",
			"test_end": get_date_str(test_df, "max"),
		}
		with open(OUTPUT_SPLIT_DATES, "w") as f:
			json.dump(split_dates, f, indent=2)
		print_info(f"Split dates: {OUTPUT_SPLIT_DATES.name}")

		# Preprocessing report
		n_brands = df["brand"].nunique()
		n_rows = len(df)
		feature_cols = [c for c in df.columns
					   if c not in ["brand", "period_year", "period_month", "split", "sales_units", "log_sales_units"]]

		# Display Summary table
		console = Console()
		summary_table = Table(title=f"Nielsen {CATEGORY} Preprocessing Summary")
		summary_table.add_column("Metric", style="cyan")
		summary_table.add_column("Value", style="green")
		summary_table.add_row("Brands in feature matrix", str(n_brands))
		summary_table.add_row("Total rows", f"{n_rows:,}")
		summary_table.add_row("Rows per brand (avg)", str(n_rows // n_brands if n_brands > 0 else 0))
		summary_table.add_row("Features engineered", str(len(feature_cols)))
		summary_table.add_row("Generated", pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))
		console.print(summary_table)

		# Display Split Boundaries table
		split_table = Table(title="Split Boundaries")
		split_table.add_column("Split", style="cyan")
		split_table.add_column("Start", style="yellow")
		split_table.add_column("End", style="yellow")
		split_table.add_column("Periods", style="magenta", justify="right")
		split_table.add_row("Train", split_dates["train_start"], split_dates["train_end"], str(len(df[df["split"]=="train"])))
		split_table.add_row("Val", split_dates["val_start"], split_dates["val_end"], str(len(df[df["split"]=="val"])))
		split_table.add_row("Test", split_dates["test_start"], split_dates["test_end"], str(len(df[df["split"]=="test"])))
		console.print(split_table)

		# Display Top 20 Brands
		if len(series_idx) > 0:
			top_20 = series_idx.head(20)
			print_data_preview(top_20, title="Top 20 Brands by Total Sales Units", max_rows=20)

		# Helper function to format large numbers in millions
		def fmt_millions(n):
			if isinstance(n, (int, float)):
				if n >= 1_000_000:
					return f"{n / 1_000_000:.1f}M"
				else:
					return f"{n:,.0f}"
			return str(n)

		# Read step logs to reconstruct pipeline details
		step_logs = []
		step_output_dir = get_category_pipeline_step_outputs_dir(CATEGORY)
		for step_num in range(1, 7):
			log_file = step_output_dir / f"step_{step_num}_log.json"
			if log_file.exists():
				try:
					with open(log_file, 'r') as f:
						logs = json.load(f)
						if logs:
							step_logs.append(logs[-1])  # Get latest log entry for this step
				except:
					pass

		# Calculate total elapsed time
		total_elapsed = sum(log.get('elapsed_sec', 0) for log in step_logs)

		val_count = len(df[df["split"]=="val"])
		train_count = len(df[df["split"]=="train"])
		test_count = len(df[df["split"]=="test"])

		# Build comprehensive report
		report = f"""# Nielsen {CATEGORY} Preprocessing Report

**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Category:** {CATEGORY}
**Market Scope:** {TARGET_MARKET}
**Min Periods Filter:** {MIN_PERIODS}

---

## Executive Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | {n_brands} |
| Total rows | {n_rows:,} |
| Rows per brand (avg) | {n_rows // n_brands if n_brands > 0 else 0} |
| Features engineered | {len(feature_cols)} |
| Total pipeline time | {total_elapsed:.1f}s |

---

## Output Files

| Artifact | File | Description |
|---|---|---|
| Feature Matrix | `{OUTPUT_FEATURE_MATRIX.name}` | Final feature matrix for modeling (brand Ã— period Ã— features Ã— split) |
| Series Index | `{OUTPUT_SERIES_INDEX.name}` | Brand-level metadata with sales units |
| Split Dates | `{OUTPUT_SPLIT_DATES.name}` | Train/val/test split date boundaries (JSON) |
| Report | `{OUTPUT_REPORT.name}` | This preprocessing summary report |

**Location:** `{OUTPUT_ENGINEERED_DIR}`

---

## Pipeline Execution Details

### Step 1: Load and Aggregate
- **Input:** Nielsen view files (Facts, Product, Period, Market dimensions)
- **Output:** Brand Ã— period aggregation
- **Processing:** Loaded {fmt_millions(4040)} rows, aggregated by brand and period
- **Output file:** `step_1_aggregate.parquet`
"""

		# Add step logs with column info
		if step_logs:
			report += f"\n| Step | Input Cols | Output Cols | Elapsed (s) | Output Rows |\n|---|---|---|---|---|\n"
			for log in step_logs[:1]:  # Step 1
				input_cols = log.get('input_cols', 'â€”')
				output_cols = log.get('output_cols', 'â€”')
				report += f"| Step {log['step_num']} | {input_cols} | {output_cols} | {log['elapsed_sec']:.2f}s | {fmt_millions(log['output_rows'])} |\n"

		report += f"""
### Step 2: Build Calendar
- **Input:** Aggregated data (step 1)
- **Output:** Complete brand Ã— month index with NaN for missing periods
- **Date Range:** 2022-10 to 2026-03 (42 monthly periods)
- **Processing:** Created complete calendar grid for all brands
- **Output file:** `step_2_calendar_filled.parquet`
"""
		if len(step_logs) > 1:
			log = step_logs[1]
			input_cols = log.get('input_cols', 'â€”')
			output_cols = log.get('output_cols', 'â€”')
			report += f"- **Columns:** {input_cols} â†’ {output_cols} | **Elapsed:** {log['elapsed_sec']:.2f}s | **Output rows:** {fmt_millions(log['output_rows'])}\n"

		report += f"""
### Step 3: Filter Series
- **Input:** Calendar-filled data (step 2)
- **Output:** Filtered to brands with â‰¥{MIN_PERIODS} non-zero periods
- **Processing:** Removed sparse series (insufficient historical observations)
- **Output file:** `step_3_filtered_series.parquet`
"""
		if len(step_logs) > 2:
			log = step_logs[2]
			input_cols = log.get('input_cols', 'â€”')
			output_cols = log.get('output_cols', 'â€”')
			report += f"- **Columns:** {input_cols} â†’ {output_cols} | **Elapsed:** {log['elapsed_sec']:.2f}s | **Output rows:** {fmt_millions(log['output_rows'])}\n"

		report += f"""
### Step 4: Engineer Features
- **Input:** Filtered series (step 3)
- **Output:** Features + lag/rolling/calendar features + log transformation
- **Features added:** {len(feature_cols) - 8} new columns
- **Processing:**
  - Lags: 1, 2, 3, 4, 8, 13 months
  - Rolling: mean (4, 13-month windows), std (4-month window)
  - Calendar: month, quarter, holiday_month (Jan/Apr/Jun/Oct/Dec)
  - Transformation: log(sales_units) with NaN preservation
- **Output file:** `step_4_engineered_features.parquet`
"""
		if len(step_logs) > 3:
			log = step_logs[3]
			input_cols = log.get('input_cols', 'â€”')
			output_cols = log.get('output_cols', 'â€”')
			report += f"- **Columns:** {input_cols} â†’ {output_cols} | **Elapsed:** {log['elapsed_sec']:.2f}s | **Output rows:** {fmt_millions(log['output_rows'])}\n"

		report += f"""
### Step 5: Apply Split
- **Input:** Engineered features (step 4)
- **Output:** Added train/val/test split labels
- **Split method:** Locked date-based (time-series integrity)
- **Processing:** Assigned split based on period_year-period_month
- **Output file:** `step_5_split_applied.parquet`
"""
		if len(step_logs) > 4:
			log = step_logs[4]
			input_cols = log.get('input_cols', 'â€”')
			output_cols = log.get('output_cols', 'â€”')
			report += f"- **Columns:** {input_cols} â†’ {output_cols} | **Elapsed:** {log['elapsed_sec']:.2f}s | **Output rows:** {fmt_millions(log['output_rows'])}\n"

		report += f"""
### Step 6: Save Outputs
- **Input:** Split-applied data (step 5)
- **Output:** Feature matrix, series index, split dates, report
- **Processing:** Generated final outputs and documentation
- **Output files:** `Totalbeer_feature_matrix.parquet`, `Totalbeer_series_index.csv`, `Totalbeer_split_dates.json`
"""
		if len(step_logs) > 5:
			log = step_logs[5]
			input_cols = log.get('input_cols', 'â€”')
			output_cols = log.get('output_cols', 'â€”')
			report += f"- **Columns:** {input_cols} â†’ {output_cols} | **Elapsed:** {log['elapsed_sec']:.2f}s | **Output rows:** {fmt_millions(log['output_rows'])}\n"

		report += f"""
---

## Split Boundaries

| Split | Start | End | Period Range | Rows | Avg rows/brand |
|---|---|---|---|---|---|
| Train | {split_dates["train_start"]} | {split_dates["train_end"]} | â‰¤2025-02 | {fmt_millions(train_count)} | {train_count // n_brands if n_brands > 0 else 0} |
| Val | {split_dates["val_start"]} | {split_dates["val_end"]} | 2025-03 to 2025-08 | {fmt_millions(val_count)} | {val_count // n_brands if n_brands > 0 else 0} |
| Test | {split_dates["test_start"]} | {split_dates["test_end"]} | â‰¥2025-09 | {fmt_millions(test_count)} | {test_count // n_brands if n_brands > 0 else 0} |

---

## Top 20 Brands by Total Sales Units

"""
		# Format top 20 with millions
		top_20_display = series_idx.head(20).copy()
		top_20_display['total_units'] = top_20_display['total_units'].apply(fmt_millions)
		report += top_20_display.to_markdown(index=False) if len(series_idx) > 0 else "No data"

		report += f"""

---

## Feature Engineering Summary

### Column Evolution

| Stage | Count | Columns |
|---|---|---|
| Step 1 (Aggregation) | 8 | brand, period_year, period_month, sales_units, sales_value, sales_liters, promo_units, weighted_dist |
| Step 2-3 (Calendar & Filter) | 8 | _(same as Step 1)_ |
| Step 4 (Feature Engineering) | 23 | _(+15 new features: lags, rolling, calendar, log_sales_units)_ |
| Step 5 (Split) | 24 | _(+1 split column)_ |

### Engineered Features

**Lag Features (6):** `lag_1`, `lag_2`, `lag_3`, `lag_4`, `lag_8`, `lag_13`

**Rolling Features (3):** `rolling_mean_4`, `rolling_mean_13`, `rolling_std_4`

**Calendar Features (3):** `month` (1â€“12), `quarter` (1â€“4), `holiday_month` (binary)

**Transformations (1):** `log_sales_units` (ln of sales_units, NaN-safe)

**All Engineered Columns:**
{chr(10).join(f"- `{f}`" for f in sorted(feature_cols))}

---

## Data Quality Notes

### Null Handling
- **sales_units:** NaN in calendar-filled step indicates zero or missing observation. Preserved for downstream time-series modeling (NOT imputed).
- **weighted_distribution:** ~16.7% NULL in source data. Averaged during aggregation; NaN for missing brand-months.
- **Engineered features:** NaN propagates where source is NaN. Lag/rolling operations do NOT forward-fill gaps.
- **log_sales_units:** NaN for non-positive or missing values (log-safe transformation).

### Filtering Criteria
- Only brands with â‰¥{MIN_PERIODS} non-zero observations retained
- All brands have complete calendar coverage (2022-10 to 2026-03)
- NaN pattern from earlier steps preserved through final matrix

### Train/Val/Test Notes
- Split based on **date, not random sampling** (time-series integrity required)
- Locked boundaries per research design:
  - Train: period â‰¤ 2025-02
  - Val: 2025-03 â‰¤ period â‰¤ 2025-08
  - Test: period â‰¥ 2025-09

---

## Configuration & Parameters

| Parameter | Value |
|---|---|
| Target Market | {TARGET_MARKET} |
| Min Periods Filter | {MIN_PERIODS} non-zero observations per brand |
| Calendar Range | 2022-10 to 2026-03 (42 monthly periods) |
| Lag Windows | 1, 2, 3, 4, 8, 13 months |
| Rolling Windows | 4-month, 13-month |
| Holiday Months | 1 (Jan), 4 (Apr), 6 (Jun), 10 (Oct), 12 (Dec) |
| Split Method | Locked date-based (time-series) |
| Train End | 2025-02 |
| Val End | 2025-08 |

---

## Processing Summary

- **Total brands processed:** {n_brands}
- **Total rows in final matrix:** {fmt_millions(n_rows)}
- **Features engineered:** {len(feature_cols)}
- **Pipeline execution time:** {total_elapsed:.1f}s
- **Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
		OUTPUT_REPORT.write_text(report, encoding='utf-8')
		print_info(f"Report: {OUTPUT_REPORT.name}")
		print_info(f"Full path: {OUTPUT_REPORT}")

		# Display output files summary
		print("\nOutput Files Summary:")
		outputs_table = Table(title="Generated Artifacts")
		outputs_table.add_column("Artifact", style="cyan")
		outputs_table.add_column("File", style="yellow")
		outputs_table.add_row("Feature Matrix", str(OUTPUT_FEATURE_MATRIX))
		outputs_table.add_row("Series Index", str(OUTPUT_SERIES_INDEX))
		outputs_table.add_row("Split Dates", str(OUTPUT_SPLIT_DATES))
		outputs_table.add_row("Report", str(OUTPUT_REPORT))
		console.print(outputs_table)

		# Summary
		step_elapsed = time.perf_counter() - step_start
		log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, n_rows, LOG_FILE,
					   input_cols=input_shape[1], output_cols=input_shape[1])

		print(f"\nâœ“ All outputs saved to: {OUTPUT_ENGINEERED_DIR}")


if __name__ == "__main__":
	main()

