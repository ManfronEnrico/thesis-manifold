#!/usr/bin/env python
"""
Step 4 -- Build the feature matrix for one Nielsen category from its contract.

P0038 task 5. Consumes the JSON step 3 writes; derives nothing itself.

WHY THIS STEP DERIVES NOTHING
-----------------------------
Step 3 decides, step 4 applies (DEC-CONTRACT). The archived per-category
scripts did the opposite -- pre_csd_4_engineer_features.py carried its own
CSD_HOLIDAY_MONTHS = {3, 6, 12}, and the three non-CSD scripts each carried
{1, 4, 6, 10, 12} under a category-prefixed name that made an inherited
constant look measured. Four scripts, four private opinions about the same
parameter, none of them re-measured after the data changed.

So this file contains NO parameter values. Every number it uses is read from
{slug}_eda_findings_h{N}.json. If you find yourself adding a constant here,
it belongs in step 3.

DEC-NO-FALLBACK
---------------
A missing or unreadable contract is a hard failure, never a default. This is
the consumer half of the guarantee: step 3 writes every parameter including the
ones that look constant, and step 4 refuses to run without them. `require()`
below is the whole mechanism -- it fails on absence rather than substituting,
so a contract that drifts out of schema stops the pipeline instead of silently
engineering features against a stale threshold.

The version check is the same guarantee applied to shape rather than content:
a contract whose schema this file does not know is refused, because a field
that moved is indistinguishable from a field that is missing.

DEC-DISCOVER-COLUMNS
--------------
Never names a category and never enumerates a column. Category differences
arrive through the contract, and measure columns are whatever step 1 produced.

USAGE
    python step_4_engineer_features.py --category CSD                 # H=3 (primary)
    python step_4_engineer_features.py --category CSD --horizon 1     # anchor run
    python step_4_engineer_features.py --all-categories --horizon 3
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# Repo root on sys.path so `import PATHS` resolves when run as a script.
_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
	sys.path.insert(0, str(_REPO_ROOT))

from capture_utils import save_table, tee_console  # noqa: E402
from engineer_features import (  # noqa: E402
	engineer_features,
	filter_series,
	make_calendar,
)
from pipeline_config import (  # noqa: E402
	CATEGORIES,
	FORECAST_HORIZON,
	get_paths,
	normalise_category,
	suppress_warnings,
)
from step_1_load_and_aggregate import load_and_aggregate, load_merged  # noqa: E402

# Contract schema versions this file knows how to read. A version outside this
# set is refused rather than parsed optimistically -- see load_contract().
SUPPORTED_CONTRACT_VERSIONS = frozenset({"1.1"})

BRAND_COL = "brand"
GROUP_KEYS = [BRAND_COL]


# ============================================================================
# CONTRACT LOADING
# ============================================================================

class ContractError(RuntimeError):
	"""Raised when the contract is absent, unparseable, or not understood.

	A distinct type so the orchestrator can tell "step 3 has not run for this
	category/horizon" apart from a genuine feature-engineering failure.
	"""


def require(contract: dict, key: str, path: Path):
	"""Read a required contract field, or fail naming the file and the field.

	This is DEC-NO-FALLBACK in three lines. Reading with a default is the
	single habit that let MIN_PERIODS reach three disagreeing live values
	without anyone noticing, because a wrong-but-present number produces a
	plausible feature matrix and no error.
	"""
	if key not in contract:
		raise ContractError(
			f"Contract is missing required field '{key}'.\n"
			f"  Contract: {path}\n"
			f"  This step derives no parameters, so it cannot proceed without "
			f"it. Re-run step 3 for this category and horizon."
		)
	return contract[key]


def load_contract(paths: dict, horizon: int) -> tuple[dict, Path]:
	"""Read and validate the step 3 contract for one category and horizon."""
	path = paths["step_output_dir"] / f"{paths['slug']}_eda_findings_h{horizon}.json"

	if not path.exists():
		raise ContractError(
			f"No contract for {paths['category']} at horizon {horizon}.\n"
			f"  Expected: {path}\n"
			f"  Run: python step_3_derive_params.py --category "
			f"{paths['category']} --horizon {horizon}"
		)

	try:
		contract = json.loads(path.read_text(encoding="utf-8"))
	except json.JSONDecodeError as exc:
		raise ContractError(f"Contract is not valid JSON: {path}\n  {exc}") from exc

	version = contract.get("contract_version")
	if version not in SUPPORTED_CONTRACT_VERSIONS:
		raise ContractError(
			f"Unsupported contract_version {version!r}.\n"
			f"  Contract: {path}\n"
			f"  This step understands: {sorted(SUPPORTED_CONTRACT_VERSIONS)}\n"
			f"  A schema this step does not know may have moved or re-typed a "
			f"field, which is indistinguishable from a missing one. Refusing "
			f"rather than guessing (DEC-NO-FALLBACK)."
		)

	# The horizon is in the filename AND in the body. If they disagree, the
	# file was hand-edited or copied, and either value could be the intended
	# one -- so neither is trusted.
	stated = contract.get("forecast_horizon")
	if stated != horizon:
		raise ContractError(
			f"Contract horizon disagrees with its filename.\n"
			f"  Contract: {path}\n"
			f"  Filename says h{horizon}, body says forecast_horizon={stated}.\n"
			f"  Re-run step 3 rather than editing the JSON."
		)

	return contract, path


# ============================================================================
# FEATURE MATRIX
# ============================================================================

def build_matrix(df: pd.DataFrame, contract: dict, path: Path) -> tuple[pd.DataFrame, dict]:
	"""Calendar -> filter -> engineer, entirely on contract values.

	Order matters and is not interchangeable:

	1. make_calendar first, so every series is on a complete month grid before
	   any lag is taken. Lagging a gappy series makes lag_1 mean "the previous
	   OBSERVED month", which is a different quantity per row.
	2. filter_series second, so the min_periods threshold counts non-zero
	   observations on that completed grid rather than raw row counts.
	3. engineer_features last, so lags and rolling windows are computed only on
	   series that survive into training.
	"""
	target = require(contract, "target_col", path)
	min_periods = require(contract, "min_periods", path)
	lags = require(contract, "lags", path)
	rolling_windows = require(contract, "rolling_windows", path)
	peak_months = require(contract, "peak_months", path)

	stats = {"rows_in": len(df), "brands_in": int(df[BRAND_COL].nunique())}

	filled, _dates = make_calendar(df, group_keys=GROUP_KEYS)
	stats["rows_calendar"] = len(filled)

	kept = filter_series(
		filled,
		min_periods=min_periods,
		target_col=target,
		group_keys=GROUP_KEYS,
	)
	stats["rows_filtered"] = len(kept)
	stats["brands_filtered"] = int(kept[BRAND_COL].nunique()) if len(kept) else 0

	if kept.empty:
		raise ContractError(
			f"No brand survived min_periods={min_periods}.\n"
			f"  Contract: {path}\n"
			f"  Either the panel is shorter than the contract assumes, or the "
			f"contract was derived against different data. Re-run step 3."
		)

	out = engineer_features(
		kept,
		target_col=target,
		lags=lags,
		rolling_windows=rolling_windows,
		group_keys=GROUP_KEYS,
		peak_months=peak_months,
	)
	stats["rows_out"] = len(out)
	stats["cols_out"] = len(out.columns)
	stats["brands_out"] = int(out[BRAND_COL].nunique())

	# Category capability, recorded rather than assumed. Nielsen reports
	# promotion for some categories and not others, so the feature set is not
	# identical across the four -- and that difference must be visible in the
	# run log, because a model comparison across categories is otherwise
	# comparing different feature spaces without saying so.
	stats["has_promo"] = "promo_units" in kept.columns

	_verify(out, contract, stats)
	return out, stats


def _verify(df: pd.DataFrame, contract: dict, stats: dict) -> None:
	"""Confirm the matrix actually carries what the contract asked for.

	Cheap, and it catches the failure mode that produced the wrong peak-month
	feature in the first place: engineer_features accepted the parameter and
	the pipeline ran, so nothing surfaced until someone read the constant. An
	assertion on the OUTPUT rather than the input is what makes the contract
	enforceable instead of merely documented.
	"""
	expected = {f"lag_{lag}" for lag in contract["lags"]}
	expected |= {f"rolling_mean_{w}" for w in contract["rolling_windows"]}
	expected |= {"month", "quarter", "peak_month"}

	# promo_intensity is required exactly where its source column exists.
	# Asserting it unconditionally would fail the categories Nielsen reports no
	# promotion for; dropping the assertion would stop catching a genuine
	# omission in the categories that do have it. Neither is acceptable, so the
	# expectation follows the capability.
	if stats.get("has_promo"):
		expected |= {"promo_intensity"}

	missing = sorted(expected - set(df.columns))
	if missing:
		raise ContractError(
			f"Feature engineering did not produce the contracted columns: {missing}"
		)

	# The flag must be set on exactly the contracted months and no others.
	flagged = sorted(int(m) for m in df.loc[df["peak_month"] == 1, "month"].unique())
	contracted = sorted(int(m) for m in contract["peak_months"])
	if flagged != contracted:
		raise ContractError(
			f"peak_month flag disagrees with the contract.\n"
			f"  Contract: {contracted}\n"
			f"  Flagged:  {flagged}"
		)
	stats["peak_months_verified"] = contracted

	if contract["log_transform_target"] and "log_sales_units" not in df.columns:
		raise ContractError(
			"Contract sets log_transform_target=true but log_sales_units is "
			"absent from the matrix."
		)

	# --- degenerate-feature guard (P0036 task 4) ---------------------------
	#
	# A feature that is present but constant carries no information, and its
	# silence is the problem: a column of zeros is made of valid numbers, so
	# nothing downstream objects. The promo family was entirely zero at region
	# scope for weeks before anyone noticed (P0032 F10.2).
	#
	# Scoped to every engineered feature, not just promo -- the original task
	# asked for exactly that generality, and the next silent-zero column will
	# not be one anybody predicted.
	#
	# A legitimately ABSENT column is not a failure (DEC-NO-PROMO-FILL: a
	# category with no promotion has no promo_intensity, correctly). That case
	# belongs to the presence check above. This one fires only on columns that
	# exist and say nothing.
	_exempt = {
		# Calendar and identity columns are constant-by-design at some grains.
		"brand", "date", "period_index", "period_year", "period_month",
		"split", "month", "quarter",
		# peak_month is legitimately all-zero when a category has no peak
		# months in its contract; verified against the contract just above.
		"peak_month",
	}
	_degenerate = []
	for _c in sorted(set(df.columns) - _exempt):
		if not pd.api.types.is_numeric_dtype(df[_c]):
			continue
		_vals = df[_c].dropna()
		if len(_vals) == 0:
			_degenerate.append((_c, "all-null"))
		elif _vals.nunique() == 1:
			_degenerate.append((_c, f"constant ({_vals.iloc[0]:g})"))

	if _degenerate:
		_detail = "\n".join(f"    {c:<34} {why}" for c, why in _degenerate)
		raise ContractError(
			f"{len(_degenerate)} engineered feature(s) carry no information:\n"
			f"{_detail}\n"
			f"  A constant column cannot inform a model, and it fails silently "
			f"because its values are individually valid.\n"
			f"  Either the source measure is empty at this scope (check the "
			f"market filter), or the feature's inputs are missing.\n"
			f"  If the column is legitimately unavailable for this category, it "
			f"should be OMITTED rather than filled (DEC-NO-PROMO-FILL)."
		)
	stats["degenerate_features"] = 0


# ============================================================================
# RUN
# ============================================================================

def run(category: str, horizon: int) -> pd.DataFrame:
	"""Build and persist the feature matrix for one category at one horizon."""
	suppress_warnings()
	category = normalise_category(category)
	paths = get_paths(category)
	paths["tables_dir"].mkdir(parents=True, exist_ok=True)

	print("=" * 80)
	print(f"STEP 4 -- ENGINEER FEATURES: {category} (horizon={horizon})")
	print("=" * 80)

	contract, cpath = load_contract(paths, horizon)
	print(f"\nContract: {cpath.name} (version {contract['contract_version']})")
	_report_contract(contract)

	if not contract["split"]["horizon_evaluable"]:
		print(f"\n  !! This contract reports zero evaluable test origins at "
			  f"horizon {horizon}.")
		print("     The matrix will build, but step 5 will refuse the split.")

	# Rebuilt via step 1 rather than read from an intermediate, matching steps
	# 2 and 3: all three must describe exactly what step 1 produces today.
	print("\nRebuilding the analysis panel via step 1...")
	merged = load_merged(category, paths["views_dir"])
	df = load_and_aggregate(merged)
	print(f"  Panel: {len(df):,} rows x {len(df.columns)} columns, "
		  f"{df[BRAND_COL].nunique()} brands")

	print("\nApplying the contract...")
	matrix, stats = build_matrix(df, contract, cpath)
	_report_stats(stats)
	_persist(matrix, stats, contract, paths, horizon)
	return matrix


def _report_contract(c: dict) -> None:
	print(f"  target                = {c['target_col']}")
	print(f"  min_periods           = {c['min_periods']}")
	print(f"  lags                  = {c['lags']}")
	print(f"  rolling_windows       = {c['rolling_windows']}")
	print(f"  peak_months        = {c['peak_months']}")
	print(f"  log_transform_target  = {c['log_transform_target']}")


def _report_stats(s: dict) -> None:
	print("\nFEATURE MATRIX")
	print(f"  panel in              = {s['rows_in']:,} rows / "
		  f"{s['brands_in']} brands")
	print(f"  after calendar fill   = {s['rows_calendar']:,} rows")
	print(f"  after min_periods     = {s['rows_filtered']:,} rows / "
		  f"{s['brands_filtered']} brands "
		  f"({s['brands_in'] - s['brands_filtered']} dropped)")
	print(f"  engineered            = {s['rows_out']:,} rows x "
		  f"{s['cols_out']} columns")
	print(f"  peak flag set on      = {s['peak_months_verified']} "
		  f"(matches contract)")
	print(f"  promo_intensity       = "
		  f"{'built' if s.get('has_promo') else 'OMITTED (category has no promo_units)'}")


def _persist(df: pd.DataFrame, stats: dict, contract: dict,
			 paths: dict, horizon: int) -> None:
	"""Write the matrix and a provenance sidecar.

	The filename carries the horizon for the same reason the contract's does:
	H=1 and H=3 disagree on min_periods, so they are different matrices and one
	must not overwrite the other.

	The sidecar records WHICH contract produced this matrix. Without it, a
	parquet on disk is unattributable -- you can see the columns but not the
	thresholds behind them, which is exactly the position every previous
	notebook run left its outputs in.
	"""
	out = paths["step_output_dir"] / f"step_4_engineered_features_h{horizon}.parquet"
	df.to_parquet(out, index=False)
	print(f"\n  Matrix   -> {out}")

	sidecar = paths["step_output_dir"] / f"step_4_log_h{horizon}.json"
	sidecar.write_text(json.dumps({
		"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
		"generated_by": "step_4_engineer_features.py",
		"category": contract["category"],
		"forecast_horizon": horizon,
		"contract_version": contract["contract_version"],
		"contract_generated_utc": contract["generated_utc"],
		"parameters_applied": {
			"target_col": contract["target_col"],
			"min_periods": contract["min_periods"],
			"lags": contract["lags"],
			"rolling_windows": contract["rolling_windows"],
			"peak_months": contract["peak_months"],
		},
		"result": stats,
		"output_parquet": out.name,
	}, indent=2), encoding="utf-8")
	print(f"  Log      -> {sidecar}")

	rows = [
		("rows_in", stats["rows_in"]),
		("brands_in", stats["brands_in"]),
		("rows_after_calendar_fill", stats["rows_calendar"]),
		("brands_after_min_periods", stats["brands_filtered"]),
		("rows_after_min_periods", stats["rows_filtered"]),
		("rows_engineered", stats["rows_out"]),
		("columns_engineered", stats["cols_out"]),
		("min_periods_applied", contract["min_periods"]),
		("peak_months_applied", str(contract["peak_months"])),
	]
	save_table(
		pd.DataFrame(rows, columns=["quantity", "value"]),
		f"step_4_feature_matrix_h{horizon}",
		paths["tables_dir"],
		caption=(f"Feature matrix construction "
				 f"({contract['category']}, horizon {horizon} month(s))"),
		notes=[
			"Row counts at each stage of matrix construction. The calendar "
			"fill completes each brand's month grid so that a lag refers to a "
			"fixed interval rather than to the previous observed month.",
			"Brands below the minimum series length are excluded before "
			"feature construction. The threshold is not a quality judgement: "
			"a shorter series yields no observation whose lag features are "
			"defined under this specification.",
			"Every parameter above is read from the step 3 contract for this "
			"category and horizon. This step derives none of them, so the "
			"matrix and the recorded parameters cannot disagree.",
		],
	)
	print(f"  Table    -> {paths['tables_dir']}")


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Step 4 -- build the feature matrix from the step 3 contract."
	)
	parser.add_argument("--category", type=str, default=None)
	parser.add_argument("--all-categories", action="store_true")
	parser.add_argument(
		"--horizon", type=int, default=FORECAST_HORIZON,
		help=(f"Forecast horizon in months. Selects which contract to read; "
			  f"it is not re-derived here. Default {FORECAST_HORIZON}."),
	)
	args = parser.parse_args()

	if args.all_categories:
		targets = list(CATEGORIES)
	elif args.category:
		targets = [args.category]
	else:
		parser.error("give --category or --all-categories")

	failed: list[tuple[str, str]] = []
	for cat in targets:
		paths = get_paths(normalise_category(cat))
		paths["step_output_dir"].mkdir(parents=True, exist_ok=True)
		log = paths["step_output_dir"] / f"step_4_h{args.horizon}_console.log"
		try:
			with tee_console(log):
				run(cat, args.horizon)
		except ContractError as exc:
			# Reported and carried past, so one category missing its contract
			# does not hide the state of the other three.
			print(f"\n!! {cat}: {exc}", file=sys.stderr)
			failed.append((cat, str(exc).splitlines()[0]))

	if failed:
		print(f"\n{len(failed)} of {len(targets)} categories failed:", file=sys.stderr)
		for cat, why in failed:
			print(f"  {cat}: {why}", file=sys.stderr)
		return 1

	print(f"\nStep 4 complete for {len(targets)} category(ies) at horizon "
		  f"{args.horizon}.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
