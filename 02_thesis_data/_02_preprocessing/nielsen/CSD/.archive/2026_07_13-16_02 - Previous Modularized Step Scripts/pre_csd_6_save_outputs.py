#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 6: Save Outputs

Input:  Step 5 output (split_applied_{grain}.parquet)
		- Final feature matrix with split labels

Output: Final outputs in engineered/{grain}/CSD/ directory
		- csd_feature_matrix.parquet (feature matrix for modeling)
		- csd_series_index.csv (series metadata per group)
		- csd_split_dates.json (train/val/test split boundaries)
		- csd_preprocessing_report.md (preprocessing summary)

Logic:
  - Import build_series_index() from shared codebase
  - Save final feature matrix
  - Generate series index (group-key metadata)
  - Document split dates
  - Create preprocessing summary report

USAGE
=====
  python pre_csd_6_save_outputs.py [--grain bymonth] [--grains bymonth,bychain]
"""

import argparse
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
sys.path.insert(0, str(ROOT_DIR / "02_thesis_data" / "_02_preprocessing" / "nielsen" / "_shared_modules"))

from PATHS import (
	get_category_pipeline_step_outputs_dir,
	get_category_engineered_bymonth_dir,
	get_category_engineered_bychain_dir,
)
from utility_scripts.scripts.METADATA import get_dimension_info
from engineer_features import build_series_index
from terminal_utils import (
	step_execution, print_file_load, print_file_save, print_info, print_data_preview
)
from timing_utils import log_step_timing
from rich.table import Table
from rich.console import Console

# Import GRAIN_CONFIG from Step 1
sys.path.insert(0, str(Path(__file__).parent))
from pre_csd_1_load_and_aggregate import GRAIN_CONFIG, DEFAULT_GRAIN, IMPLEMENTED_GRAINS

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step finalizes outputs: feature matrix, series metadata, split dates, and report.
# Key column definitions referenced:
#
# OUTPUT ARTIFACTS:
#   - csd_feature_matrix.parquet: Final feature matrix (group_keys × period × features × split)
#   - csd_series_index.csv: Group-level metadata (series name, total sales units)
#   - csd_split_dates.json: Train/val/test date boundaries (locked)
#   - csd_preprocessing_report.md: Summary of preprocessing steps, series, rows, features
#
# SERIES INDEX COLUMNS:
#   - group_keys...: Series identity (e.g. brand, for bymonth grain)
#   - n_periods: Total periods in feature matrix
#   - n_nonzero: Count of non-zero sales_units
#   - total_units: Sum of sales_units across all periods
#   - train_periods, val_periods, test_periods: Breakdown by split
#   - (sorted by total_units descending for top-20 report)
#
# KEY NULL SEMANTICS (documented in report):
#   - sales_units: NaN in calendar_filled (step 2) → NaN in feature matrix
#   - weighted_distribution: Averaged during aggregation; ~16.7% NULL; NaN in matrix where missing
#   - Engineered features (lags, rolling): NaN propagation from source data
#   - Do NOT impute NaNs; preserve for downstream time-series modeling

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_NUM = 6
STEP_NAME = "Save Outputs"

# CSD-specific split dates (from EDA analysis, Cell 7) — time-based, grain-independent
CSD_TRAIN_END = (2024, 10)    # From Cell 7: 24 months training
CSD_VAL_END = (2025, 4)       # From Cell 7: 6 months validation

STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# Only grains with a PATHS.py engineered-dir helper can route final output today.
# byregion has no THESIS_DATA_ENGINEERED_BYREGION_DIR yet (Phase 4b, deferred).
ENGINEERED_DIR_FOR_GRAIN = {
	"bymonth": get_category_engineered_bymonth_dir,
	"bychain": get_category_engineered_bychain_dir,
}


def input_parquet_for_grain(grain: str) -> Path:
	return STEP_OUTPUT_DIR / f"step_5_split_applied_{grain}.parquet"

# ============================================================================
# STEP LOGIC
# ============================================================================

def run_step(grain: str):
	"""Execute step 6 for a single grain."""
	if grain not in IMPLEMENTED_GRAINS:
		raise NotImplementedError(
			f"Grain '{grain}' is not yet implemented. See plans/P0027 Phase 4b (deferred)."
		)
	if grain not in ENGINEERED_DIR_FOR_GRAIN:
		raise NotImplementedError(
			f"No engineered-output directory helper wired up for grain '{grain}' in PATHS.py yet."
		)

	group_keys = GRAIN_CONFIG[grain]["group_keys"]
	min_periods = GRAIN_CONFIG[grain]["min_periods"]

	input_parquet = input_parquet_for_grain(grain)
	output_engineered_dir = ENGINEERED_DIR_FOR_GRAIN[grain](CATEGORY)
	output_feature_matrix = output_engineered_dir / f"{CATEGORY.lower()}_feature_matrix.parquet"
	output_series_index = output_engineered_dir / f"{CATEGORY.lower()}_series_index.csv"
	output_split_dates = output_engineered_dir / f"{CATEGORY.lower()}_split_dates.json"
	output_report = output_engineered_dir / f"{CATEGORY.lower()}_preprocessing_report.md"

	step_start = time.perf_counter()

	if not input_parquet.exists():
		raise FileNotFoundError(f"Input missing: {input_parquet}")

	print(f"Loading split-applied data for grain='{grain}' from step 5...")
	load_start = time.perf_counter()
	df = pd.read_parquet(input_parquet)
	load_elapsed = time.perf_counter() - load_start

	input_shape = df.shape
	print_file_load(input_parquet, input_shape, load_elapsed)

	print(f"\nGenerating series index...")
	series_idx = build_series_index(df, group_keys=group_keys)
	# Note: build_series_index already sorts by total_units descending

	print(f"\nSaving final outputs ({grain})...")
	output_engineered_dir.mkdir(parents=True, exist_ok=True)

	save_start = time.perf_counter()
	df.to_parquet(output_feature_matrix, index=False)
	save_elapsed = time.perf_counter() - save_start
	print_file_save(output_feature_matrix, df.shape, save_elapsed)

	series_idx.to_csv(output_series_index, index=False)
	print_info(f"Series index: {output_series_index.name}")

	train_df = df[df["split"] == "train"]
	test_df = df[df["split"] == "test"]

	def get_date_str(df_subset, min_or_max="min"):
		if len(df_subset) == 0:
			return "unknown"
		date_series = df_subset["period_year"].astype(str) + "-" + df_subset["period_month"].astype(str).str.zfill(2)
		return getattr(date_series, min_or_max)()

	split_dates = {
		"train_start": get_date_str(train_df, "min"),
		"train_end": f"{CSD_TRAIN_END[0]}-{CSD_TRAIN_END[1]:02d}-01",
		"val_start": f"{CSD_TRAIN_END[0]}-{CSD_TRAIN_END[1]+1 if CSD_TRAIN_END[1]<12 else 1:02d}-01",
		"val_end": f"{CSD_VAL_END[0]}-{CSD_VAL_END[1]:02d}-01",
		"test_start": f"{CSD_VAL_END[0]}-{CSD_VAL_END[1]+1 if CSD_VAL_END[1]<12 else 1:02d}-01",
		"test_end": get_date_str(test_df, "max"),
	}
	with open(output_split_dates, "w") as f:
		json.dump(split_dates, f, indent=2)
	print_info(f"Split dates: {output_split_dates.name}")

	n_series = df[group_keys].drop_duplicates().shape[0]
	n_rows = len(df)
	feature_cols = [c for c in df.columns
				   if c not in group_keys + ["period_year", "period_month", "split", "sales_units", "log_sales_units"]]

	console = Console()
	summary_table = Table(title=f"Nielsen {CATEGORY} Preprocessing Summary ({grain})")
	summary_table.add_column("Metric", style="cyan")
	summary_table.add_column("Value", style="green")
	summary_table.add_row("Grain", grain)
	summary_table.add_row("Group keys", ", ".join(group_keys))
	summary_table.add_row("Series in feature matrix", str(n_series))
	summary_table.add_row("Total rows", f"{n_rows:,}")
	summary_table.add_row("Rows per series (avg)", str(n_rows // n_series if n_series > 0 else 0))
	summary_table.add_row("Features engineered", str(len(feature_cols)))
	summary_table.add_row("Generated", pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))
	console.print(summary_table)

	split_table = Table(title="Split Boundaries")
	split_table.add_column("Split", style="cyan")
	split_table.add_column("Start", style="yellow")
	split_table.add_column("End", style="yellow")
	split_table.add_column("Periods", style="magenta", justify="right")
	split_table.add_row("Train", split_dates["train_start"], split_dates["train_end"], str(len(df[df["split"]=="train"])))
	split_table.add_row("Val", split_dates["val_start"], split_dates["val_end"], str(len(df[df["split"]=="val"])))
	split_table.add_row("Test", split_dates["test_start"], split_dates["test_end"], str(len(df[df["split"]=="test"])))
	console.print(split_table)

	if len(series_idx) > 0:
		top_20 = series_idx.head(20)
		print_data_preview(top_20, title="Top 20 Series by Total Sales Units", max_rows=20)

	def fmt_millions(n):
		if isinstance(n, (int, float)):
			if n >= 1_000_000:
				return f"{n / 1_000_000:.1f}M"
			else:
				return f"{n:,.0f}"
		return str(n)

	step_logs = []
	for step_num in range(1, 7):
		log_file = STEP_OUTPUT_DIR / f"step_{step_num}_log.json"
		if log_file.exists():
			try:
				with open(log_file, 'r') as f:
					logs = json.load(f)
					if logs:
						step_logs.append(logs[-1])
			except:
				pass

	total_elapsed = sum(log.get('elapsed_sec', 0) for log in step_logs)

	val_count = len(df[df["split"] == "val"])
	train_count = len(df[df["split"] == "train"])
	test_count = len(df[df["split"] == "test"])

	min_periods_display = min_periods if min_periods is not None else "n/a"

	report = f"""# Nielsen {CATEGORY} Preprocessing Report ({grain})

**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Category:** {CATEGORY}
**Grain:** {grain} (group keys: {', '.join(group_keys)})
**Market Scope:** All Market Types (aggregated across all 28 outlet channels)
**Min Periods Filter:** {min_periods_display}

---

## Executive Summary

| Metric | Value |
|---|---|
| Series in feature matrix | {n_series} |
| Total rows | {n_rows:,} |
| Rows per series (avg) | {n_rows // n_series if n_series > 0 else 0} |
| Features engineered | {len(feature_cols)} |
| Total pipeline time | {total_elapsed:.1f}s |

---

## Output Files

| Artifact | File | Description |
|---|---|---|
| Feature Matrix | `{output_feature_matrix.name}` | Final feature matrix for modeling |
| Series Index | `{output_series_index.name}` | Series-level metadata with sales units |
| Split Dates | `{output_split_dates.name}` | Train/val/test split date boundaries (JSON) |
| Report | `{output_report.name}` | This preprocessing summary report |

**Location:** `{output_engineered_dir}`

---

## Split Boundaries

| Split | Start | End | Rows |
|---|---|---|---|
| Train | {split_dates["train_start"]} | {split_dates["train_end"]} | {fmt_millions(train_count)} |
| Val | {split_dates["val_start"]} | {split_dates["val_end"]} | {fmt_millions(val_count)} |
| Test | {split_dates["test_start"]} | {split_dates["test_end"]} | {fmt_millions(test_count)} |

---

## Top 20 Series by Total Sales Units

"""
	top_20_display = series_idx.head(20).copy()
	if "total_units" in top_20_display.columns:
		top_20_display['total_units'] = top_20_display['total_units'].apply(fmt_millions)
	report += top_20_display.to_markdown(index=False) if len(series_idx) > 0 else "No data"

	report += f"""

---

## Feature Engineering Summary

**Lag Features (6):** `lag_1`, `lag_2`, `lag_3`, `lag_4`, `lag_8`, `lag_13`

**Rolling Features (3):** `rolling_mean_4`, `rolling_mean_13`, `rolling_std_4`

**Calendar Features (3):** `month` (1–12), `quarter` (1–4), `holiday_month` (binary)

**Transformations (1):** `log_sales_units` (ln of sales_units, NaN-safe)

**All Engineered Columns:**
{chr(10).join(f"- `{f}`" for f in sorted(feature_cols))}

---

## Data Quality Notes

### Null Handling
- **sales_units:** NaN in calendar-filled step indicates zero or missing observation. Preserved for downstream time-series modeling (NOT imputed).
- **weighted_distribution:** ~16.7% NULL in source data. Averaged during aggregation; NaN for missing series-months.
- **Engineered features:** NaN propagates where source is NaN. Lag/rolling operations do NOT forward-fill gaps.
- **log_sales_units:** NaN for non-positive or missing values (log-safe transformation).

### Filtering Criteria
- Only series with >={min_periods_display} non-zero observations retained
- NaN pattern from earlier steps preserved through final matrix

### Train/Val/Test Notes
- Split based on **date, not random sampling** (time-series integrity required)

---

## Configuration & Parameters (CSD EDA-Driven)

| Parameter | Value |
|---|---|
| Grain | {grain} |
| Group Keys | {', '.join(group_keys)} |
| Market Scope | All Market Types (aggregated across 28 retail outlet channels) |
| Min Periods Filter | {min_periods_display} |
| Lag Windows | 1, 2, 3, 4, 8, 13 months (autocorrelation-based) |
| Rolling Windows | 4-month, 13-month (Nielsen calendar + quarterly) |
| Holiday Months | 3 (Mar), 6 (Jun), 12 (Dec) — **Empirical CSD peaks** (not default {{1,4,6,10,12}}) |
| Split Method | Locked date-based (time-series) |

---

## Processing Summary

- **Total series processed:** {n_series}
- **Total rows in final matrix:** {fmt_millions(n_rows)}
- **Features engineered:** {len(feature_cols)}
- **Pipeline execution time:** {total_elapsed:.1f}s
- **Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
	output_report.write_text(report, encoding='utf-8')
	print_info(f"Report: {output_report.name}")
	print_info(f"Full path: {output_report}")

	print("\nOutput Files Summary:")
	outputs_table = Table(title="Generated Artifacts")
	outputs_table.add_column("Artifact", style="cyan")
	outputs_table.add_column("File", style="yellow")
	outputs_table.add_row("Feature Matrix", str(output_feature_matrix))
	outputs_table.add_row("Series Index", str(output_series_index))
	outputs_table.add_row("Split Dates", str(output_split_dates))
	outputs_table.add_row("Report", str(output_report))
	console.print(outputs_table)

	step_elapsed = time.perf_counter() - step_start
	log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, n_rows, LOG_FILE,
				   input_cols=input_shape[1], output_cols=input_shape[1])

	print(f"\n✓ All outputs saved to: {output_engineered_dir}")


def main():
	"""Execute step 6: Save outputs."""
	parser = argparse.ArgumentParser(description="CSD Step 6: Save Outputs")
	parser.add_argument("--grain", type=str, default=None, help=f"Single grain (default: {DEFAULT_GRAIN})")
	parser.add_argument("--grains", type=str, default=None, help="Comma-separated list of grains")
	args = parser.parse_args()

	if args.grains:
		grains = [g.strip() for g in args.grains.split(",") if g.strip()]
	elif args.grain:
		grains = [args.grain]
	else:
		grains = [DEFAULT_GRAIN]

	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		for grain in grains:
			print(f"\n{'=' * 60}")
			print(f"Grain: {grain}")
			print(f"{'=' * 60}")
			run_step(grain)


if __name__ == "__main__":
	main()
