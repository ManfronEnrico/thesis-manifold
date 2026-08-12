#!/usr/bin/env python3
"""
Nielsen Preprocessing -- Step 1: Load, Merge and Aggregate

Shared across all categories; select with --category.

Input:  The 4 Nielsen view parquet files (validated by step 0)
Output: step_1_aggregate_bymonth.parquet  -- brand x month panel
        step_1_console.log, step_1_log.json

Logic:
  1. Load facts + the 3 dimension views
  2. Merge to row level
  3. Filter to the DVH EXCL. HD parent market  (DEC-SCOPE)
  4. Assert exactly one market survives       (fan-out guard)
  5. Filter to positive sales
  6. Aggregate to brand x period_year x period_month  (DEC-GRAIN)

Ported from the CSD notebook cells "Step 1" and "Step 2" (P0038 task 2),
which in turn came from pre_csd_1_load_and_aggregate.py.
"""

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Project root discovery
# ---------------------------------------------------------------------------
current = Path.cwd()
while current != current.parent:
	if (current / "CLAUDE.md").exists():
		ROOT_DIR = current
		break
	current = current.parent
else:
	raise FileNotFoundError("Could not find project root (CLAUDE.md)")

sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "02_thesis_data" / "_02_preprocessing" / "nielsen" / "_shared_modules"))

from capture_utils import print_and_save_table, tee_console
from pipeline_config import (
	CATEGORIES,
	DVH_PARENT_MARKET_ID,
	get_paths,
	normalise_category,
	suppress_warnings,
	view_filenames,
)
from terminal_utils import print_info, print_warning, step_execution
from timing_utils import log_step_timing

STEP_NUM = 1
STEP_NAME = "Load, Merge and Aggregate"

# ============================================================================
# GRAIN
# ============================================================================
# GRAIN HISTORY: SRQ1 scope is locked to brand x month only (DEC-GRAIN,
# 2026-07-12); the "bychain" and "byregion" grains were dropped to a documented
# limitation + future work, and their config entries removed (P0035, 2026-08-01).
# The parameter survives so a future grain can be registered -- do NOT resurrect
# the deleted PATHS helpers if one is.

GRAIN = "bymonth"
GROUP_KEYS: dict[str, list[str]] = {"bymonth": ["brand"]}


# ============================================================================
# AGGREGATION SPEC
# ============================================================================
# The measure columns, in output order, as (source_column, output_name, how).
#
# Built against what the frame ACTUALLY has rather than as a fixed dict, because
# the categories are not column-compatible: measured 2026-08-12, Danskvand has
# 15 fact columns and RTD 31, and NEITHER carries sales_units_any_promo (CSD and
# Energidrikke have 32 and do). The notebook's fixed agg_dict raises KeyError on
# both. Capability tiers are a step-4 concern by design, but they surface here
# too, because you cannot aggregate a column that does not exist.

MEASURE_SPEC: list[tuple[str, str, str]] = [
	("sales_units", "sales_units", "sum"),
	("sales_value", "sales_value", "sum"),
	("sales_in_liters", "sales_liters", "sum"),
	("sales_units_any_promo", "promo_units", "promo_sum"),
	("weighted_distribution", "weighted_dist", "mean"),
]

# Columns without which the panel is meaningless -- absence is an error, not a
# capability difference to degrade around.
REQUIRED_MEASURES = {"sales_units"}


def _promo_sum(series: pd.Series) -> float:
	"""Sum treating NaN as zero.

	Nielsen leaves the promo column null (not 0) for a brand-period with no
	promotion, so a plain "sum" would propagate NaN across the group and wipe
	out an otherwise valid brand-month. Ported from the notebook's
	`lambda x: sum(pd.Series(x).fillna(0))`.
	"""
	return series.fillna(0).sum()


def build_agg_dict(df: pd.DataFrame) -> tuple[dict, list[str], list[str]]:
	"""Return (agg_dict, output_names, skipped) for the columns actually present."""
	agg_dict: dict[str, object] = {}
	output_names: list[str] = []
	skipped: list[str] = []

	for source, output, how in MEASURE_SPEC:
		if source not in df.columns:
			if source in REQUIRED_MEASURES:
				raise KeyError(
					f"Required measure column {source!r} is absent from the merged "
					f"frame. Present columns: {sorted(df.columns)}"
				)
			skipped.append(source)
			continue
		agg_dict[source] = _promo_sum if how == "promo_sum" else how
		output_names.append(output)

	return agg_dict, output_names, skipped


# ============================================================================
# LOAD + MERGE
# ============================================================================

# DEC-SCOPE (P0036, 2026-08-11): market scope is the DVH EXCL. HD *parent*,
# not its 9 regional children. This reverses P0026's region choice.
#
# P0026 chose the 9 children to avoid double-counting, which is correct when
# SUMMING markets -- but selecting the parent alone avoids it equally well,
# since parent and children are alternative views of the same universe.
#
# Measured at brand x month (the modelling grain), parent vs children:
#   - promo columns : ~23,400 nonzero  vs  0  <- decisive; the whole promo
#                     feature family is empty at region scope
#   - distinct brands: 140 vs 140      <- no brand loss
#   - brand-month rows: 3,917 vs 3,975 <- costs 1.5%, not a gain
#   - fact rows      : 37,999 vs 243,691 <- children repeat each brand-period
#                     9x, inflating row count without adding information
#
# Net: costs 1.5% of brand-month rows, buys the entire promo feature set.
# The ID itself lives in pipeline_config (more than one step names it).


def load_merged(category: str, views_dir: Path) -> pd.DataFrame:
	"""Load and merge the 4 Nielsen view parquet files (grain-independent)."""
	facts_f, product_f, period_f, market_f = view_filenames(category)

	print("  Loading view parquet files...")
	facts = pd.read_parquet(views_dir / facts_f)
	products = pd.read_parquet(views_dir / product_f)
	periods = pd.read_parquet(views_dir / period_f)
	markets = pd.read_parquet(views_dir / market_f)

	print(f"  Facts shape:    {facts.shape}")
	print(f"  Products shape: {products.shape}")
	print(f"  Periods shape:  {periods.shape}")
	print(f"  Markets shape:  {markets.shape}")

	# Each dimension join must be many-to-one: a fact row may match at most one
	# dimension row. `validate="m:1"` makes pandas raise if a dimension table
	# carries a duplicate key, which is the fan-out shape the nunique() guard
	# below CANNOT see -- duplicate rows sharing one id multiply the fact rows
	# while leaving nunique() at 1. Measured 2026-08-12: all four categories
	# have 0 duplicate market_ids today, so this is a regression guard, not a
	# fix for a live defect.
	merged = facts.merge(
		products[["product_id", "brand"]], on="product_id", validate="m:1"
	)
	merged = merged.merge(
		periods[["period_id", "period_year", "period_month"]],
		on="period_id",
		validate="m:1",
	)
	merged = merged.merge(
		markets[["market_id", "market_description"]], on="market_id", validate="m:1"
	)

	# Filter to the DVH EXCL. HD parent market (DEC-SCOPE, see block above).
	merged = merged[merged["market_id"] == DVH_PARENT_MARKET_ID].copy()

	# Guard: exactly one market must survive. A market_description-based join
	# resolving to >1 market_id would fan out and silently multiply every
	# downstream SUM() -- the 6.16x defect P0027 found. Assert == 1, not > 0.
	#
	# This catches the DISTINCT-id case only. The same-id duplicate-row case
	# (which multiplies rows while leaving nunique() at 1) is caught upstream by
	# validate="m:1" on the merges. Both halves are needed; neither alone is
	# sufficient.
	_n_markets = merged["market_id"].nunique()
	if _n_markets != 1:
		raise ValueError(
			f"Expected exactly 1 market after filtering to "
			f"{DVH_PARENT_MARKET_ID}, got {_n_markets}. "
			f"Aggregates would be double-counted."
		)

	# Filter to positive sales only.
	merged = merged[merged["sales_units"] > 0].copy()

	return merged


# ============================================================================
# AGGREGATE
# ============================================================================

def load_and_aggregate(df_merged: pd.DataFrame, grain: str = GRAIN) -> pd.DataFrame:
	"""Aggregate the merged row-level dataset to the requested grain."""
	if grain not in GROUP_KEYS:
		raise ValueError(
			f"Unknown grain {grain!r}. Valid grains: {list(GROUP_KEYS)}. "
			f"To add one, register it here -- do not reintroduce the PATHS "
			f"helpers removed by P0035."
		)

	agg_dict, output_names, skipped = build_agg_dict(df_merged)

	if skipped:
		print_warning(
			f"Measure column(s) absent for this category, aggregating without "
			f"them: {', '.join(skipped)}"
		)

	keys = GROUP_KEYS[grain] + ["period_year", "period_month"]
	aggregated = df_merged.groupby(keys).agg(agg_dict).reset_index()
	aggregated.columns = keys + output_names

	return aggregated


# ============================================================================
# MAIN
# ============================================================================

def run(category: str, grain: str = GRAIN) -> pd.DataFrame:
	"""Execute step 1 for one category. Returns the aggregated panel."""
	suppress_warnings()
	category = normalise_category(category)
	paths = get_paths(category)
	paths["step_output_dir"].mkdir(parents=True, exist_ok=True)

	out_parquet = paths["step_output_dir"] / f"step_{STEP_NUM}_aggregate_{grain}.parquet"
	log_path = paths["step_output_dir"] / f"step_{STEP_NUM}_console.log"

	with tee_console(log_path):
		with step_execution(STEP_NUM, STEP_NAME, category):
			step_start = time.perf_counter()

			# ---- load + merge -------------------------------------------
			print("=" * 80)
			print("LOAD AND MERGE CACHED PARQUET VIEWS")
			print("=" * 80)

			t0 = time.perf_counter()
			df_merged = load_merged(category, paths["views_dir"])
			print()
			print(f"Merged row-level shape: {df_merged.shape}")
			print(f"Unique brands:          {df_merged['brand'].nunique()}")
			print(f"Elapsed:                {time.perf_counter() - t0:.2f}s")
			print("=" * 80)

			# ---- aggregate ----------------------------------------------
			print()
			print("=" * 80)
			print(f"AGGREGATE TO {grain.upper()} GRAIN")
			print("=" * 80)

			t1 = time.perf_counter()
			df = load_and_aggregate(df_merged, grain)
			print()
			print(f"Aggregated shape: {df.shape}")
			print(f"Unique brands:    {df['brand'].nunique()}")

			if len(df) > 0:
				s = df.sort_values(["period_year", "period_month"])
				first, last = s.iloc[0], s.iloc[-1]
				n_periods = df[["period_year", "period_month"]].drop_duplicates().shape[0]
				print(
					f"Date range:       {int(first.period_year)}-{int(first.period_month):02d}"
					f" to {int(last.period_year)}-{int(last.period_month):02d}"
					f"  ({n_periods} distinct periods)"
				)
			print(f"Elapsed:          {time.perf_counter() - t1:.2f}s")
			print("=" * 80)

			# ---- persist ------------------------------------------------
			# Preview table goes to disk as well as stdout: this is the
			# notebook's `df.head(10)` cell output, which used to be retained
			# in the .ipynb and would otherwise be lost to the terminal.
			print_and_save_table(
				df.head(10),
				f"step_{STEP_NUM}_preview",
				paths["tables_dir"],
				caption=f"{category} -- brand x month panel (first 10 rows)",
			)

			df.to_parquet(out_parquet, index=False)
			print()
			print_info(f"Wrote {out_parquet.name}  ({len(df):,} rows x {len(df.columns)} cols)")

			elapsed = time.perf_counter() - step_start
			log_step_timing(
				STEP_NUM,
				STEP_NAME,
				category,
				elapsed,
				len(df),
				paths["step_output_dir"] / f"step_{STEP_NUM}_log.json",
			)
			print_info(f"Console log: {log_path}")

	return df


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Load, merge and aggregate Nielsen views to the modelling grain."
	)
	parser.add_argument(
		"--category",
		required=True,
		help=f"Category to process. One of: {', '.join(CATEGORIES)}",
	)
	parser.add_argument(
		"--grain",
		default=GRAIN,
		choices=sorted(GROUP_KEYS),
		help=f"Aggregation grain (default: {GRAIN}).",
	)
	args = parser.parse_args()

	run(args.category, args.grain)
	return 0


if __name__ == "__main__":
	sys.exit(main())
