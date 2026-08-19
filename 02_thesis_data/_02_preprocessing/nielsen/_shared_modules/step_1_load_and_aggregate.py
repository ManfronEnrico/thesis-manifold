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
	TARGET_COL,
	get_paths,
	normalise_category,
	suppress_warnings,
	view_filenames,
)
from terminal_utils import print_info, step_execution
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
# AGGREGATION SPEC -- column-discovery column discovery
# ============================================================================
# Measures are DISCOVERED from the merged frame, not enumerated.
#
# The notebook hardcoded five columns (sales_units, sales_value,
# sales_in_liters, sales_units_any_promo, weighted_distribution). Measured
# 2026-08-12 across the four categories, the fact views actually carry 35
# distinct measure columns -- the whole `baseline_*` family, the
# `numeric_distribution` family, `universe_number_of_stores`,
# `sales_units_any_tpr`, and more. A fixed list silently discards all of them,
# not because anyone judged them uninformative but because the notebook listed
# five and the list was inherited unexamined. That is the same defect class as
# F28/F38: an inherited literal wearing the appearance of a decision.
#
# Column availability also differs BETWEEN categories in ways a fixed list
# cannot express -- and not only by presence. The same measure is spelled
# differently per category:
#     weighted_distribution_disp_w_o_feat   (CSD)
#     weighted_distribution_disp_wo_feat    (Energidrikke, RTD)
#     weighted_distribution_disp_and_feat   (RTD)
# Discovery handles all three without naming any of them.
#
# Related: P0036 task 11 ("recover discarded product-dimension features").
# This removes the step-1 half of that problem -- measures are no longer
# dropped on the way into the panel.

# Join keys and identifiers: structural, never aggregated as measures.
NON_MEASURE_COLS: frozenset[str] = frozenset({
	"product_id", "period_id", "market_id", "market_description",
	"brand", "period_year", "period_month",
})

# How to aggregate, decided by what the measure IS rather than by name lookup.
#
# Additive (sum): counts and volumes -- summing across the products in a brand
#   is meaningful, because the brand's total IS the sum of its products.
# Intensive (mean): rates, ratios, distributions, per-store averages -- these
#   are already normalised, so summing them is meaningless (a "70% weighted
#   distribution" plus another "70%" is not 140%).
#
# Matched on substrings so a newly-arrived Nielsen column is classified by its
# semantics rather than needing to be added here.
INTENSIVE_PATTERNS: tuple[str, ...] = (
	"distribution",     # weighted_/numeric_distribution and all their variants
	"avg_",             # avg_no_of_items_per_store_reach, avg_number_of_stores_
	"universe_",        # universe_number_of_stores -- a market property
	"_reach",           # number_of_items_reach, *_reach variants
)

# The forecast target. Not a "category capability" -- it is what the pipeline
# predicts (Y = log1p(sales_units_{t+1}), see pipeline_config). Without it there
# is nothing to forecast and every later step is meaningless, so its absence is
# an error rather than something to degrade around. This is the ONLY column
# named explicitly, and it is named because of its role, not its category.
REQUIRED_MEASURES: frozenset[str] = frozenset({TARGET_COL})

# Output names kept stable for the few columns downstream code refers to by
# name. Everything else keeps its source name verbatim.
RENAMES: dict[str, str] = {
	"sales_in_liters": "sales_liters",
	"sales_units_any_promo": "promo_units",
	"weighted_distribution": "weighted_dist",

	# --- per-category spelling variants (P0038, 2026-08-18) -----------------
	# Nielsen spells the same three display/feature measures differently per
	# category. Without canonicalisation they present as six distinct features,
	# and any cross-category comparison misreports what the categories share
	# (found by step 6 --check-consistency). The common-to-all count stays 23,
	# since these three measures are absent from Danskvand regardless; what the
	# canonicalisation fixes is the pairwise picture -- CSD and Energidrikke now
	# show as feature-identical (41 each), and RTD differs from them by exactly
	# the two promo columns rather than by five apparent absences, so a real
	# capability gap is no longer masked by three spelling artifacts.
	#
	#   measure                  CSD            Energidrikke   RTD
	#   display AND feature      disp_feat      disp_feat      disp_and_feat
	#   display WITHOUT feature  disp_w_o_feat  disp_wo_feat   disp_wo_feat
	#   feature WITHOUT display  feat_w_o_disp  feat_wo_disp   feat_wo_disp
	#
	# This is a naming difference, not a capability difference -- precisely the
	# case DEC-DISCOVER-COLUMNS anticipated. Canonical form spells out and/without:
	# "disp_feat" does not say whether it means "display and feature" or the
	# pair, and "w_o" is an abbreviation the reader must decode.
	"weighted_distribution_disp_feat": "weighted_distribution_disp_and_feat",
	"weighted_distribution_disp_w_o_feat": "weighted_distribution_disp_without_feat",
	"weighted_distribution_disp_wo_feat": "weighted_distribution_disp_without_feat",
	"weighted_distribution_feat_w_o_disp": "weighted_distribution_feat_without_disp",
	"weighted_distribution_feat_wo_disp": "weighted_distribution_feat_without_disp",
}


def classify_measure(column: str) -> str:
	"""Return "mean" for intensive measures, "sum" for additive ones."""
	lowered = column.lower()
	if any(p in lowered for p in INTENSIVE_PATTERNS):
		return "mean"
	return "sum"


def _sum_nan_as_zero(series: pd.Series) -> float:
	"""Sum treating NaN as zero.

	Nielsen leaves a measure null (not 0) for a brand-period where the event did
	not occur -- most visibly the promo family. A plain "sum" would propagate
	NaN across the group and wipe out an otherwise valid brand-month.

	Generalised from the notebook's promo-only
	`lambda x: sum(pd.Series(x).fillna(0))`: the null-means-zero convention is a
	property of how Nielsen encodes additive measures, not of the promo columns
	specifically.
	"""
	return series.fillna(0).sum()


def discover_measures(df: pd.DataFrame) -> list[str]:
	"""Every numeric column that is a measure rather than a join key.

	Column-discovery: a column the pipeline has never seen is included automatically,
	classified by `classify_measure`. Nothing is dropped for not being on a list.
	"""
	missing = REQUIRED_MEASURES - set(df.columns)
	if missing:
		raise KeyError(
			f"Forecast target column(s) {sorted(missing)} absent from the merged "
			f"frame -- there is nothing to predict. This is not a category "
			f"capability difference; check the Stage 1 conversion. "
			f"Present columns: {sorted(df.columns)}"
		)

	numeric = df.select_dtypes(include="number").columns
	return [c for c in numeric if c not in NON_MEASURE_COLS]


def build_agg_dict(df: pd.DataFrame) -> tuple[dict, list[str]]:
	"""Return (agg_dict, output_names) covering every discovered measure."""
	agg_dict: dict[str, object] = {}
	output_names: list[str] = []

	for source in discover_measures(df):
		how = classify_measure(source)
		# NaN-as-zero for additive measures: Nielsen leaves a measure null (not
		# 0) where the event did not occur -- notably the promo family -- and a
		# plain sum would propagate NaN across the group, wiping out an
		# otherwise valid brand-month. Intensive measures keep pandas' default
		# NaN-skipping mean, since a missing rate is genuinely unknown rather
		# than zero.
		agg_dict[source] = "mean" if how == "mean" else _sum_nan_as_zero
		output_names.append(RENAMES.get(source, source))

	return agg_dict, output_names


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
	# Predicate pushdown on market_id, NOT a convenience: the CSD facts table is
	# 10.3M rows x 32 float64 columns, and the DEC-SCOPE filter below keeps only
	# ~2% of them (measured 2026-08-12: CSD 2.16%, Danskvand 1.99%,
	# Energidrikke 1.59%, RTD 2.07%). Materialising the full frame first costs
	# ~2.6GB dense plus pyarrow's conversion copy, and raised ArrowMemoryError
	# on a 15.8GB machine. Filtering at the reader keeps the working set ~46x
	# smaller. The pandas-level filter further down is deliberately KEPT: it is
	# now a no-op on the data but remains the readable statement of DEC-SCOPE,
	# and it still guards the case where a future engine ignores `filters=`.
	facts = pd.read_parquet(
		views_dir / facts_f,
		filters=[("market_id", "==", DVH_PARENT_MARKET_ID)],
	)
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

	agg_dict, output_names = build_agg_dict(df_merged)

	n_mean = sum(1 for v in agg_dict.values() if v == "mean")
	print(
		f"  Discovered {len(agg_dict)} measure columns "
		f"({len(agg_dict) - n_mean} additive, {n_mean} intensive)"
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
