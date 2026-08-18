"""
Shared configuration for the Nielsen preprocessing pipeline.

Ported from the CSD notebook's "Step 0.3 - Paths & Config" cell (P0038).
In the notebook these constants lived in the shared cell namespace, so every
later cell saw them for free. Scripts each have their own namespace, so the
config is centralised here and imported -- NOT re-declared per step, which is
exactly how the four categories drifted apart in the first place.

Everything is keyed on `category`; nothing here hardcodes a category name.
"""

from pathlib import Path

# PATHS is the single source of truth for locations -- never hardcode a path,
# not even in a comment.
from PATHS import (
	get_category_pipeline_step_outputs_dir,
	get_category_views_dir,
)

# ============================================================================
# CATEGORIES
# ============================================================================

# Canonical spelling, and the order results are reported in. The parquet files
# themselves use the lowercased form (see view_filenames below).
CATEGORIES: tuple[str, ...] = ("CSD", "Danskvand", "Energidrikke", "RTD")


def normalise_category(category: str) -> str:
	"""Map a case-insensitive category argument onto its canonical spelling.

	Exists because the CLI accepts `--category csd` while the paths and the
	canonical constants use "CSD". Raising on an unknown value (rather than
	silently proceeding) turns a typo into an immediate error instead of a
	confusing empty-cache failure three steps later.
	"""
	lookup = {c.lower(): c for c in CATEGORIES}
	key = category.strip().lower()
	if key not in lookup:
		raise ValueError(
			f"Unknown category {category!r}. Expected one of: {', '.join(CATEGORIES)}"
		)
	return lookup[key]


# ============================================================================
# ML TARGET DEFINITION (C1 -- must hold before any lag/split/feature work)
# ============================================================================
# Ported verbatim from the notebook. These are modelling decisions, identical
# across categories, so they are constants rather than derived parameters and
# do NOT belong in the per-category EDA contract JSON.

TARGET_COL: str = "sales_units"      # raw column in the dataset
FORECAST_HORIZON: int = 1            # H=1: predict t+1 from features at t
LOG_TRANSFORM_TARGET: bool = True    # Y = log1p(sales_units_{t+H}); ADF-confirmed

# Warmup: max lag or window needed before the first valid prediction row.
# Features use up to lag-13 and rolling-13, so the first 13 rows per brand carry
# NaN features and must be excluded from training / evaluation.
MAX_LAG: int = 13                    # lags: (1, 2, 3, 4, 8, 13)
MAX_WINDOW: int = 13                 # rolling windows: (4, 13)
WARMUP_PERIODS: int = max(MAX_LAG, MAX_WINDOW)   # = 13

# DEC-MINPERIODS (2026-08-18): the minimum series length is DERIVED from the
# feature specification above, never chosen. A brand-month row is trainable
# only once its lag features are defined, so
#
#     usable_rows(brand) = n_months(brand) - WARMUP_PERIODS - FORECAST_HORIZON
#
# and requiring at least one usable row gives n_months >= 15. A brand below
# that cannot enter the design matrix at all -- it is excluded because it is
# unrepresentable under this feature specification, not because it was judged
# low quality. That distinction is what makes the threshold defensible.
#
# Measured 2026-08-18 across all four categories: this threshold costs 0.0% of
# training rows relative to imposing no threshold, because the brands it drops
# were each contributing zero. The previous hardcoded 40 cost 20.5% (CSD),
# 16.8% (Danskvand), 40.8% (Energidrikke) and 30.2% (RTD).
#
# Because it is derived, it follows the lag structure automatically: MAX_LAG=6
# yields 9, MAX_LAG=3 yields 6. Do not hardcode a replacement.
MIN_PERIODS: int = WARMUP_PERIODS + FORECAST_HORIZON + 1   # = 15

# DEC-SCOPE (P0036, 2026-08-11): market scope is the DVH EXCL. HD *parent*, not
# its 9 regional children. Full measurement rationale lives at the point of use
# in step_1_load_and_aggregate.py; the ID is here because more than one step
# needs to name it.
DVH_PARENT_MARKET_ID: int = 1256338  # "DVH EXCL. HD"


# ============================================================================
# VISUALISATION (Rossmann + GeeksforGeeks style)
# ============================================================================

PLOT_COLOR: str = "#386B7F"
PALETTE: str = "plasma"
DPI: int = 150                       # thesis-appendix quality
FIGSIZE_DEFAULT: tuple[int, int] = (12, 6)
FIGSIZE_LARGE: tuple[int, int] = (14, 10)
FIGSIZE_XLARGE: tuple[int, int] = (16, 12)


def apply_plot_style() -> None:
	"""Apply the shared seaborn styling.

	A function rather than import-time side effects: importing this module to
	read TARGET_COL should not silently reconfigure matplotlib for the caller.
	"""
	import matplotlib
	import seaborn as sns

	try:
		# Jupyter kernel: render inline, no blocking window.
		get_ipython().run_line_magic("matplotlib", "inline")  # noqa: F821
	except NameError:
		# Plain-script context: non-interactive backend so plt.show() is a
		# no-op instead of opening a blocking OS window that stalls the run.
		matplotlib.use("Agg")

	sns.set(style="ticks")
	sns.set_palette("husl")


def suppress_warnings() -> None:
	"""Silence library warnings, as the notebook's `warnings.filterwarnings`
	cell did for the whole session.

	A function rather than an import-time call: the notebook could suppress
	globally because it WAS the whole program, but this module is imported by
	steps and by tests, and a blanket filter applied on import would hide
	warnings the caller never asked to lose. Each step opts in explicitly.
	"""
	import warnings

	warnings.filterwarnings("ignore")


# ============================================================================
# PER-CATEGORY PATHS
# ============================================================================

def view_filenames(category: str) -> list[str]:
	"""The 4 Nielsen view parquet files required for a category.

	Nielsen names these lowercase regardless of the canonical spelling, hence
	the .lower() -- this was the cause of the hardcoded "csd_..." strings in
	the notebook.
	"""
	slug = category.lower()
	return [
		f"{slug}_clean_facts_v.parquet",
		f"{slug}_clean_dim_product_v.parquet",
		f"{slug}_clean_dim_period_v.parquet",
		f"{slug}_clean_dim_market_v.parquet",
	]


def get_paths(category: str) -> dict[str, Path]:
	"""Resolve every path a pipeline step needs, from the category alone.

	Returns a dict rather than module-level constants because the constants
	would have to be bound at import time, before --category is parsed.

	NOTE the f-strings on findings/plots: the notebook hardcoded lowercase
	"csd_eda_findings.json" and "csd_eda_plots" (export lines 111-112). Left
	unchanged, a shared script run for Danskvand would have overwritten CSD's
	artifacts. This is P0038 finding F34.
	"""
	category = normalise_category(category)
	slug = category.lower()
	step_out = get_category_pipeline_step_outputs_dir(category)

	return {
		"category": category,
		"slug": slug,
		"views_dir": get_category_views_dir(category),
		"step_output_dir": step_out,
		"findings_json": step_out / f"{slug}_eda_findings.json",
		"plots_dir": step_out / f"{slug}_eda_plots",
		"tables_dir": step_out / f"{slug}_eda_tables",
	}


def print_target_definition() -> None:
	"""Echo the ML target contract, as the notebook's config cell did."""
	print("ML TARGET DEFINITION")
	print(f"  Y                    = log1p({TARGET_COL}_{{t+{FORECAST_HORIZON}}})")
	print(f"  Forecast horizon (H) = {FORECAST_HORIZON} month(s)")
	print(f"  Log transform        = {LOG_TRANSFORM_TARGET}")
	print(f"  Warmup buffer        = {WARMUP_PERIODS} periods (excluded per brand)")
