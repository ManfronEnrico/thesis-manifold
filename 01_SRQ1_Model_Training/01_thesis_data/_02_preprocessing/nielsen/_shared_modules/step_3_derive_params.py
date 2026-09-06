#!/usr/bin/env python
"""
Step 3 -- Derive the feature-engineering contract for one Nielsen category.

Ported from the CSD notebook's cells 41-53, MINUS 43/49/51 (which were
descriptive figures and now live in step 2). P0038 task 4.

WHAT THIS STEP IS FOR
---------------------
This is the ONLY step that decides parameters, and the JSON it writes is the
sole interface to step 4 (DEC-CONTRACT). Step 2 produces evidence and no
parameters; step 4 consumes parameters and derives none. Keeping the two apart
means re-deriving the contract is cheap -- it does not regenerate ~20 plots --
and it means there is exactly one place to look when asking "why this value".

DEC-NO-FALLBACK
---------------
Step 4 must fail loudly when the contract is missing or incomplete. Silent
in-code defaults are what let MIN_PERIODS drift to three different live values
(notebook 40, engineer_features 30, derived 15) without anyone noticing. So
this step writes every parameter step 4 needs, including the ones that look
constant, and records HOW each was obtained.

DEC-DISCOVER-COLUMNS
--------------
Never names a category, never enumerates a column. Parameters that depend on
category capability (peak months, log transform) are measured from the data
present; parameters that are modelling decisions (lags, horizon) are recorded
with their basis so the contract explains itself.

HORIZON IS A PARAMETER, NOT A CONSTANT (DEC-HORIZON, 2026-08-18)
---------------------------------------------------------------
The primary reported horizon is 3 months -- the quarter is the period in which
marketing budgets are authorised, so it is the first horizon a campaign
decision can actually reach. H=1 is reported alongside as a measurement anchor.
Both are real runs, so --horizon is a CLI argument and the resolved value is
written into the contract. pipeline_config.FORECAST_HORIZON is the default
only, not the source of truth.

This matters more than it looks. MIN_PERIODS is DERIVED as
warmup + horizon + 1, so it is 15 at H=1 and 17 at H=3. A single shared
constant would be correct for exactly one of the two horizons -- precisely the
drift DEC-CONTRACT exists to prevent. The contract therefore carries the
resolved MIN_PERIODS per run, and the output filename carries the horizon so
neither run can overwrite the other.

USAGE
    python step_3_derive_params.py --category CSD                 # H=3 (primary)
    python step_3_derive_params.py --category CSD --horizon 1     # anchor run
    python step_3_derive_params.py --all-categories --horizon 3
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

# Repo root on sys.path so `import PATHS` resolves when run as a script.
_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
	sys.path.insert(0, str(_REPO_ROOT))

from capture_utils import save_table, tee_console  # noqa: E402
from engineer_features import (  # noqa: E402
	DEFAULT_LAGS,
	DEFAULT_ROLLING_WINDOWS,
	DEFAULT_TRAIN_FRAC,
	DEFAULT_VAL_FRAC,
	resolve_split_cutoffs,
)
from pipeline_config import (  # noqa: E402
	CATEGORIES,
	FORECAST_HORIZON,
	LOG_TRANSFORM_TARGET,
	TARGET_COL,
	get_paths,
	normalise_category,
	suppress_warnings,
)
from step_1_load_and_aggregate import load_and_aggregate, load_merged  # noqa: E402

# Contract schema version. Bump when a field is added, removed or re-typed;
# step 4 refuses a version it does not know rather than guessing.
#
# 1.0 -> 1.1 (2026-08-18): holiday_months renamed to peak_months, and
# provenance.holiday_months_uplift to peak_months_uplift. A 1.0 contract is
# therefore refused rather than read with the renamed field silently missing --
# which is precisely the failure the version field exists to prevent.
CONTRACT_VERSION = "1.1"

BRAND_COL = "brand"
YEAR_COL = "period_year"
MONTH_COL = "period_month"

# Seasonality: a month counts as a PEAK month if its mean target exceeds the
# overall mean by this margin. The notebook hardcoded the RESULT ({1,4,6,10,12})
# rather than the rule, so every other category would have inherited CSD's
# seasonal profile. 10% is the notebook's implied threshold, now stated
# explicitly and applied per category.
#
# NAMING (2026-08-18): this was `holiday_month(s)` until the rename. The rule
# consults no holiday calendar -- there is no such input anywhere in the
# pipeline -- so the old name asserted a cause the computation never
# established, and the evidence frequently contradicts it: CSD peaks at
# quarter-ends (trade loading), Danskvand in summer (weather), Energidrikke at
# quarter-ends with no December peak at all.
#
# The name is also how the original defect survived review. A hardcoded
# {1,4,6,10,12} reads as a plausible list of holidays; read as "peak months for
# soft drinks" it is obviously wrong, since January is the weakest month of the
# year at -26.6%. A feature name should describe what was measured, not
# hypothesise why.
PEAK_UPLIFT_THRESHOLD = 0.10

# Augmented Dickey-Fuller: reject non-stationarity below this p-value.
ADF_ALPHA = 0.05


# ============================================================================
# PERIOD HELPERS
# ============================================================================
# The step-1 panel keys on (period_year, period_month) and carries NO date
# column. An earlier analysis picked up a spurious column and silently reported
# 4 months per category instead of 46 (P0038 F52). Period arithmetic therefore
# goes through these two functions and nowhere else.

def period_index(df: pd.DataFrame) -> pd.Series:
	"""Months since year 0, as a sortable integer. Ordering only, not a date."""
	return df[YEAR_COL].astype(int) * 12 + df[MONTH_COL].astype(int)


def to_date_frame(df: pd.DataFrame) -> pd.DataFrame:
	"""Add the `date` column that engineer_features helpers expect.

	resolve_split_cutoffs() reads df["date"]; the step-1 panel has no such
	column. Building it here rather than making every caller remember is what
	keeps the year/month pair the single representation of a period.
	"""
	out = df.copy()
	out["date"] = pd.to_datetime(
		dict(year=out[YEAR_COL].astype(int),
			 month=out[MONTH_COL].astype(int),
			 day=1)
	)
	return out


# ============================================================================
# PARAMETER DERIVATIONS
# ============================================================================
# Each returns (value, provenance). Provenance is not decoration: it is what
# lets the contract answer "why this value" without anyone reading this file,
# and it is what shows a reviewer whether a number was measured or decided.


def derive_lag_structure(horizon: int) -> tuple[dict, dict]:
	"""Lags, rolling windows, warm-up, and the DERIVED minimum series length.

	Lags and windows are modelling decisions, so they are recorded with their
	basis rather than computed. MIN_PERIODS is the exception: it follows
	arithmetically from the other three, and computing it here is exactly what
	stops it from being chosen (DEC-MINPERIODS).
	"""
	lags = list(DEFAULT_LAGS)
	windows = list(DEFAULT_ROLLING_WINDOWS)
	warmup = max(max(lags), max(windows))
	min_periods = warmup + horizon + 1

	params = {
		"lags": lags,
		"rolling_windows": windows,
		"warmup_periods": warmup,
		"min_periods": min_periods,
	}
	provenance = {
		"lags": (
			"modelling decision; the lag-12 term is retained because the "
			"autocorrelation analysis (step 2, section 3.16) finds it "
			"significant across the majority of leading brands"
		),
		"warmup_periods": "max(max(lags), max(rolling_windows))",
		"min_periods": (
			f"DERIVED: warmup({warmup}) + horizon({horizon}) + 1 = "
			f"{min_periods}. A brand with fewer months contributes zero "
			f"usable training rows, so the threshold excludes what is "
			f"unrepresentable under this feature specification rather than "
			f"what is judged low quality"
		),
	}
	return params, provenance


def derive_peak_months(df: pd.DataFrame) -> tuple[list[int], dict]:
	"""Months whose mean target exceeds the overall mean by the threshold.

	The notebook hardcoded {1, 4, 6, 10, 12} -- the RESULT for CSD -- so every
	other category would have inherited CSD's seasonality. Deriving this per
	category is the whole reason the contract is per-category.
	"""
	monthly = df.groupby(MONTH_COL)[TARGET_COL].mean()
	overall = df[TARGET_COL].mean()
	uplift = (monthly - overall) / overall
	months = sorted(int(m) for m in uplift[uplift > PEAK_UPLIFT_THRESHOLD].index)

	provenance = {
		"peak_months": (
			f"months whose mean {TARGET_COL} exceeds the overall mean by more "
			f"than {PEAK_UPLIFT_THRESHOLD:.0%}; measured on this category's "
			f"own data rather than inherited"
		),
		"peak_months_uplift": {
			str(int(m)): round(float(uplift.loc[m]), 4) for m in uplift.index
		},
	}
	return months, provenance


def derive_log_transform(df: pd.DataFrame) -> tuple[bool, dict]:
	"""Whether to model log1p(target), tested rather than assumed.

	Two signals: skewness of the raw target against the logged target, and
	whether an ADF test finds the logged aggregate stationary. The config
	carries LOG_TRANSFORM_TARGET as the modelling default; what is recorded
	here is whether THIS category's data actually supports it.
	"""
	y = df[TARGET_COL].dropna()
	skew_raw = float(y.skew())
	skew_log = float(np.log1p(y).skew())

	adf_p = None
	try:
		from statsmodels.tsa.stattools import adfuller
		series = df.groupby([YEAR_COL, MONTH_COL])[TARGET_COL].sum().sort_index()
		if len(series) >= 12:
			adf_p = float(adfuller(np.log1p(series))[1])
	except ImportError:
		# Recorded as null rather than raising: the skewness evidence still
		# stands, and the contract should not be unobtainable because an
		# optional dependency is missing.
		pass

	# Kim (2013): |skew| > 2 indicates substantial departure from normality.
	# The transform is supported when it materially reduces that departure.
	supported = abs(skew_log) < abs(skew_raw)
	verdict = "supports" if supported else "does NOT support"

	provenance = {
		"log_transform_target": (
			f"modelling default from configuration ({LOG_TRANSFORM_TARGET}); "
			f"this category's evidence {verdict} it -- skewness {skew_raw:.2f} "
			f"untransformed against {skew_log:.2f} after log1p"
		),
		"skew_raw": round(skew_raw, 4),
		"skew_log1p": round(skew_log, 4),
		"adf_pvalue_log": None if adf_p is None else round(adf_p, 6),
		"adf_stationary_at_5pct": None if adf_p is None else bool(adf_p < ADF_ALPHA),
	}
	return LOG_TRANSFORM_TARGET, provenance


def derive_split(df: pd.DataFrame, horizon: int) -> tuple[dict, dict]:
	"""Proportional train/val/test cutoffs, plus the evaluability check.

	The cutoffs come from engineer_features.resolve_split_cutoffs() rather than
	being recomputed here. That function is already the fix for the hardcoded
	dates that had drifted to a 24-27% test share against an intended 15%
	(F25/F28); reimplementing the logic would recreate the drift it removed.

	n_test_origins is what is new, and it is why this wrapper exists rather
	than step 5 calling resolve_split_cutoffs directly. A forecast origin is
	evaluable only if its target month falls INSIDE the test window, so
	n_origins = n_test_months - horizon + 1. At horizon 12 that is zero in
	every category (F52): the split looks perfectly healthy and yields nothing
	to report. Recording it lets step 5 assert evaluability instead of silently
	producing an unusable test set.
	"""
	dated = to_date_frame(df)
	train_end, val_end = resolve_split_cutoffs(dated)

	periods = sorted(period_index(df).unique())
	n_periods = len(periods)
	train_end_idx = train_end[0] * 12 + train_end[1]
	val_end_idx = val_end[0] * 12 + val_end[1]

	n_train = sum(1 for p in periods if p <= train_end_idx)
	n_val = sum(1 for p in periods if train_end_idx < p <= val_end_idx)
	n_test = n_periods - n_train - n_val
	n_origins = max(0, n_test - horizon + 1)

	params = {
		"train_end": list(train_end),
		"val_end": list(val_end),
		"train_frac": DEFAULT_TRAIN_FRAC,
		"val_frac": DEFAULT_VAL_FRAC,
		"n_periods": n_periods,
		"n_train_months": n_train,
		"n_val_months": n_val,
		"n_test_months": n_test,
		"n_test_origins": n_origins,
		"horizon_evaluable": n_origins > 0,
	}
	provenance = {
		"split": (
			f"proportional {DEFAULT_TRAIN_FRAC:.0%}/{DEFAULT_VAL_FRAC:.0%}/"
			f"remainder over distinct periods, derived from the panel rather "
			f"than fixed dates, so the ratio holds as the panel grows and "
			f"categories starting at different dates stay comparable"
		),
		"n_test_origins": (
			f"n_test_months({n_test}) - horizon({horizon}) + 1. A forecast "
			f"origin counts only when its target month falls inside the test "
			f"window"
		),
	}
	return params, provenance


def measure_retention(df: pd.DataFrame, min_periods: int, horizon: int,
					  warmup: int) -> dict:
	"""What the MIN_PERIODS threshold costs, in brands AND in training rows.

	Reported in both units deliberately. Counting brands makes the threshold
	look expensive (it drops 25-45% of them); counting usable training rows
	shows it costs essentially nothing, because the dropped brands each
	contribute zero (F47). Recording both is what stops the brand-count framing
	from being quoted on its own.
	"""
	counts = df.groupby(BRAND_COL).size()
	usable = (counts - warmup - horizon).clip(lower=0)
	kept = counts >= min_periods
	total_rows = int(usable.sum())

	return {
		"brands_total": int(len(counts)),
		"brands_retained": int(kept.sum()),
		"brands_dropped": int((~kept).sum()),
		"training_rows_retained": int(usable[kept].sum()),
		"training_rows_total": total_rows,
		"training_row_retention_pct": (
			round(100.0 * usable[kept].sum() / total_rows, 2)
			if total_rows else 0.0
		),
	}


# ============================================================================
# CONTRACT ASSEMBLY
# ============================================================================

def build_contract(category: str, df: pd.DataFrame, horizon: int) -> dict:
	"""Assemble every parameter step 4 needs, each with its provenance."""
	lag_params, lag_prov = derive_lag_structure(horizon)
	peak_months, peak_prov = derive_peak_months(df)
	log_transform, log_prov = derive_log_transform(df)
	split_params, split_prov = derive_split(df, horizon)
	retention = measure_retention(
		df, lag_params["min_periods"], horizon, lag_params["warmup_periods"]
	)

	provenance: dict = {}
	for block in (lag_prov, peak_prov, log_prov, split_prov):
		provenance.update(block)

	return {
		"contract_version": CONTRACT_VERSION,
		"category": category,
		"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
		"generated_by": "step_3_derive_params.py",

		# --- consumed by step 4 ---------------------------------------------
		"target_col": TARGET_COL,
		"forecast_horizon": horizon,
		"log_transform_target": log_transform,
		"lags": lag_params["lags"],
		"rolling_windows": lag_params["rolling_windows"],
		"warmup_periods": lag_params["warmup_periods"],
		"min_periods": lag_params["min_periods"],
		"peak_months": peak_months,
		"split": split_params,

		# --- evidence; not consumed, but the record of how the above arose --
		"retention": retention,
		"provenance": provenance,
	}


# ============================================================================
# RUNNER
# ============================================================================

def run(category: str, horizon: int) -> dict:
	"""Derive, report and persist the contract for one category at one horizon."""
	suppress_warnings()
	category = normalise_category(category)
	paths = get_paths(category)
	paths["tables_dir"].mkdir(parents=True, exist_ok=True)

	print("=" * 80)
	print(f"STEP 3 -- DERIVE PARAMETERS: {category} (horizon={horizon})")
	print("=" * 80)

	# Rebuild via step 1 rather than reading an intermediate file, matching
	# step 2: the contract must describe exactly what step 1 produces.
	print("\nRebuilding the analysis panel via step 1...")
	merged = load_merged(category, paths["views_dir"])
	df = load_and_aggregate(merged)
	print(f"  Panel: {len(df):,} rows x {len(df.columns)} columns, "
		  f"{df[BRAND_COL].nunique()} brands")

	contract = build_contract(category, df, horizon)
	_report(contract)
	_persist(contract, paths, horizon)
	return contract


def _report(c: dict) -> None:
	"""Print the contract in the order a reader would question it."""
	s, r = c["split"], c["retention"]

	print("\nDERIVED PARAMETERS")
	print(f"  target                = {c['target_col']}")
	print(f"  forecast_horizon      = {c['forecast_horizon']} month(s)")
	print(f"  log_transform_target  = {c['log_transform_target']}")
	print(f"  lags                  = {c['lags']}")
	print(f"  rolling_windows       = {c['rolling_windows']}")
	print(f"  warmup_periods        = {c['warmup_periods']}")
	print(f"  min_periods           = {c['min_periods']}  "
		  f"(= warmup + horizon + 1, derived)")
	print(f"  peak_months        = {c['peak_months']}")

	print("\nSPLIT")
	print(f"  train_end             = {tuple(s['train_end'])}")
	print(f"  val_end               = {tuple(s['val_end'])}")
	print(f"  months                = {s['n_train_months']} train / "
		  f"{s['n_val_months']} val / {s['n_test_months']} test "
		  f"(of {s['n_periods']})")
	print(f"  test origins          = {s['n_test_origins']} at horizon "
		  f"{c['forecast_horizon']}")

	if not s["horizon_evaluable"]:
		print("\n  !! HORIZON NOT EVALUABLE: the test window is shorter than the")
		print("     forecast horizon, so no forecast origin has its target")
		print("     inside the window. Step 5 will refuse this split.")
		print("     Lower --horizon, or extend the observed period.")

	print("\nRETENTION AT min_periods")
	print(f"  brands                = {r['brands_retained']} / "
		  f"{r['brands_total']} kept ({r['brands_dropped']} dropped)")
	print(f"  training rows         = {r['training_rows_retained']:,} / "
		  f"{r['training_rows_total']:,} "
		  f"({r['training_row_retention_pct']}%)")


def _persist(contract: dict, paths: dict, horizon: int) -> None:
	"""Write the contract JSON and a human-readable parameter table.

	The filename carries the horizon. Both H=1 and H=3 are real reported runs
	(DEC-HORIZON) and they disagree on min_periods -- 15 against 17 -- so a
	single filename would let whichever ran last silently overwrite the other's
	contract, and step 4 would engineer features against the wrong threshold.
	"""
	slug = paths["slug"]
	out = paths["step_output_dir"] / f"{slug}_eda_findings_h{horizon}.json"
	out.write_text(json.dumps(contract, indent=2), encoding="utf-8")
	print(f"\n  Contract -> {out}")

	rows = [
		("forecast_horizon", contract["forecast_horizon"]),
		("min_periods", contract["min_periods"]),
		("warmup_periods", contract["warmup_periods"]),
		("lags", str(contract["lags"])),
		("rolling_windows", str(contract["rolling_windows"])),
		("peak_months", str(contract["peak_months"])),
		("log_transform_target", contract["log_transform_target"]),
		("train_end", str(tuple(contract["split"]["train_end"]))),
		("val_end", str(tuple(contract["split"]["val_end"]))),
		("n_test_origins", contract["split"]["n_test_origins"]),
		("training_row_retention_pct",
		 contract["retention"]["training_row_retention_pct"]),
	]
	frame = pd.DataFrame(rows, columns=["parameter", "value"])

	save_table(
		frame,
		f"step_3_contract_h{horizon}",
		paths["tables_dir"],
		caption=(f"Feature-engineering parameters "
				 f"({contract['category']}, horizon {horizon} month(s))"),
		notes=[
			"Parameters governing feature construction and the temporal "
			"split. Values are measured from the category's own data where "
			"the quantity is measurable, and recorded with their basis where "
			"they reflect a modelling decision.",
			"The minimum series length follows from the feature "
			"specification: a brand-month observation is usable only once its "
			"lag features are defined, giving warm-up plus horizon plus one. "
			"Brands shorter than this cannot be represented under the "
			"specification and are excluded on that basis.",
			"Split boundaries are proportional to the observed period rather "
			"than fixed dates, which holds the ratio constant as the panel "
			"grows and keeps categories with different start dates "
			"comparable.",
			"Test origins report how many forecasts can be evaluated: an "
			"origin counts only when its target month falls within the test "
			"window.",
		],
	)
	print(f"  Table    -> {paths['tables_dir']}")


# ============================================================================
# CLI
# ============================================================================

def main(argv: list[str] | None = None) -> int:
	p = argparse.ArgumentParser(
		description="Derive the per-category feature-engineering contract."
	)
	g = p.add_mutually_exclusive_group(required=True)
	g.add_argument("--category", help="Category to process")
	g.add_argument("--all-categories", action="store_true",
				   help="Process every category in turn")
	p.add_argument(
		"--horizon", type=int, default=3,
		help="Forecast horizon in months. Default 3 -- the primary reported "
			 "horizon (DEC-HORIZON). Use 1 for the measurement-anchor run. "
			 f"The pipeline_config default is {FORECAST_HORIZON}.",
	)
	args = p.parse_args(argv)

	if args.horizon < 1:
		p.error(f"--horizon must be >= 1; got {args.horizon}")

	targets = list(CATEGORIES) if args.all_categories else [args.category]

	failed: list[tuple[str, str]] = []
	not_evaluable: list[str] = []
	for cat in targets:
		try:
			paths = get_paths(cat)
			log = paths["step_output_dir"] / f"step_3_h{args.horizon}_console.log"
			with tee_console(log):
				contract = run(cat, args.horizon)
			if not contract["split"]["horizon_evaluable"]:
				not_evaluable.append(cat)
		except Exception as exc:  # noqa: BLE001
			# One category failing must not abort the rest -- categories
			# genuinely differ, which is the premise of the column-discovery design.
			failed.append((cat, f"{type(exc).__name__}: {exc}"))
			print(f"\n  !! {cat} FAILED: {type(exc).__name__}: {exc}",
				  file=sys.stderr)

	if len(targets) > 1:
		print("\n" + "=" * 80)
		print(f"STEP 3 SUMMARY -- horizon {args.horizon}")
		print("=" * 80)
		print(f"  Succeeded: {len(targets) - len(failed)} / {len(targets)}")
		for cat, err in failed:
			print(f"    FAILED  {cat}: {err}")
		for cat in not_evaluable:
			print(f"    WARNING {cat}: horizon not evaluable (0 test origins)")

	return 1 if failed else 0


if __name__ == "__main__":
	raise SystemExit(main())
