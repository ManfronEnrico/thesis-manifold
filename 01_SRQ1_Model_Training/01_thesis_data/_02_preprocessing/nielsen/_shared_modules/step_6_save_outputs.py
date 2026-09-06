#!/usr/bin/env python
"""
Step 6 -- Write the final engineered artifacts for one category.

P0038 task 6, second half. Last step in the preprocessing pipeline; everything
downstream (model training, System A serving) reads what this writes.

WHAT IT WRITES, into _03_engineered/bymonth/{CATEGORY}/
    {slug}_feature_matrix_h{N}.parquet   the labelled matrix
    {slug}_series_index_h{N}.csv         per-brand summary
    {slug}_split_dates_h{N}.json         the boundaries ACTUALLY applied
    {slug}_manifest_h{N}.json            full provenance, see below

SPLIT DATES ARE READ BACK, NEVER RE-DERIVED
-------------------------------------------
The boundaries are recovered from the labelled frame itself -- the min and max
period actually carrying each label -- not recomputed from the contract. Those
two things should agree, and step 5 asserts that they do; but if they ever
diverge, the file must report what the data says, because that is what a model
was trained on. Deriving them a third time from constants is what let the
published split dates disagree with the real labels (F25/F28).

THE MANIFEST EXISTS BECAUSE THE CATEGORIES ARE NOT INTERCHANGEABLE
------------------------------------------------------------------
F59: Nielsen reports no promotion for Danskvand or RTD, so those categories have
no promo_intensity, and the four feature matrices genuinely differ in width
(47/29/47/45). A downstream consumer that assumes a common schema will either
crash or -- worse -- quietly train on a different feature set per category and
report the comparison as like-for-like.

So the manifest records the exact feature list, the capability flags, and the
contract that produced it. `--check-consistency` compares across categories and
reports what they do and do not share, rather than leaving it to be discovered.

USAGE
    python step_6_save_outputs.py --category CSD                 # H=3 (primary)
    python step_6_save_outputs.py --all-categories --horizon 3
    python step_6_save_outputs.py --all-categories --check-consistency
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

from PATHS import get_category_engineered_bymonth_dir  # noqa: E402
from capture_utils import save_table, tee_console  # noqa: E402
from engineer_features import build_series_index  # noqa: E402
from pipeline_config import (  # noqa: E402
	CATEGORIES,
	FORECAST_HORIZON,
	get_paths,
	normalise_category,
	suppress_warnings,
)
from step_4_engineer_features import ContractError, load_contract  # noqa: E402

BRAND_COL = "brand"
SPLITS = ("train", "val", "test")

# Columns that identify or label a row rather than describe it. Everything else
# in the matrix is a feature. Derived by exclusion so a newly engineered column
# is picked up automatically -- an allow-list would silently omit it.
NON_FEATURE_COLS = frozenset({
	"brand", "date", "period_index", "period_year", "period_month", "split",
	"sales_units", "log_sales_units",
})

# Same-month measures: present in the matrix, never offered as model inputs.
#
# These are not copies of the target -- no feature equals sales_units[t]
# (verified: each lag_k matches its own shift at 100%). They are different
# MEASUREMENTS of the same month's trading: the same sales expressed in kroner
# and litres, the promoted-unit count, and Nielsen's own baseline estimates.
#
# The problem is timing, not duplication. A forecast made at origin t predicts
# t+H; none of these is observable for t+H at origin t. Handing them to a model
# lets it read the month it is supposed to forecast.
#
# Measured on CSD H=3 (LightGBM, 300 trees):
#     base features                     WMAPE 17.20%
#     base + sales_value + sales_liters WMAPE 15.02%
# A 2.2pp gain bought by leakage.
#
# They stay in the matrix deliberately: sales_units is the target's source, and
# the rest are legitimate EDA material. Excluded from `features` so that a
# consumer selecting "everything the manifest lists" gets a defensible set.
# A LAGGED version of any of these would be a fair feature and should be built
# in engineer_features.py like promo_intensity, not smuggled in unshifted.
CONTEMPORANEOUS_COLS = frozenset({
	"sales_value", "sales_liters", "promo_units",
	"baseline_sales_units", "baseline_sales_value",
	"baseline_sales_in_liters",
	"baseline_sales_units_any_promo", "baseline_sales_value_any_promo",
	"baseline_sales_in_liters_any_promo",
	"sales_units_any_tpr", "sales_value_any_promo",
	"sales_in_liters_any_promo",
})


def add_period_index(df: pd.DataFrame) -> pd.DataFrame:
	"""Add a monotonic integer period counter, shared across all brands.

	Downstream consumers sort panels and index plot axes by period. `date` can
	do that, but an integer counter is what a panel model expects and what the
	serving path uses to find "the period after the last observed one".

	Computed from the calendar, NOT from row order: two brands observed in the
	same month must receive the same index, or a pooled model would place them
	at different points on the same axis. Anchored at the panel's first month so
	the value is stable for a given category+horizon.

	It is a NON_FEATURE_COL by construction -- a monotonic counter correlates
	with any trending target, so handing it to a model as a feature teaches it
	"later means bigger", which does not transfer beyond the observed window.
	"""
	d = df.copy()
	periods = d["date"].dt.year * 12 + d["date"].dt.month
	d["period_index"] = (periods - periods.min()).astype("int32")
	return d


def load_split(paths: dict, horizon: int) -> tuple[pd.DataFrame, Path]:
	path = paths["step_output_dir"] / f"step_5_split_applied_h{horizon}.parquet"
	if not path.exists():
		raise ContractError(
			f"No labelled split for {paths['category']} at horizon {horizon}.\n"
			f"  Expected: {path}\n"
			f"  Run: python step_5_apply_split.py --category "
			f"{paths['category']} --horizon {horizon}"
		)
	return pd.read_parquet(path), path


def read_back_split_dates(df: pd.DataFrame) -> dict:
	"""Recover the applied boundaries from the labels themselves.

	See the module docstring: these are read back, not re-derived, so the file
	reports what a model would actually have been trained on.
	"""
	out = {}
	for name in SPLITS:
		sub = df[df["split"] == name]
		if sub.empty:
			# Step 5 refuses an empty partition, so reaching here means step 5
			# was bypassed. Say so rather than writing "unknown" and moving on.
			raise ContractError(
				f"Partition '{name}' is empty in the labelled frame. Step 5 "
				f"rejects this, so the input was not produced by step 5."
			)
		out[f"{name}_start"] = sub["date"].min().strftime("%Y-%m")
		out[f"{name}_end"] = sub["date"].max().strftime("%Y-%m")
	return out


def build_manifest(df: pd.DataFrame, contract: dict, horizon: int,
				   split_dates: dict, files: dict) -> dict:
	"""Record everything needed to interpret these artifacts without guessing."""
	features = sorted(
		c for c in df.columns
		if c not in NON_FEATURE_COLS and c not in CONTEMPORANEOUS_COLS
	)
	return {
		"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
		"generated_by": "step_6_save_outputs.py",
		"category": contract["category"],
		"forecast_horizon": horizon,
		"target_col": contract["target_col"],
		"log_transform_target": contract["log_transform_target"],
		"contract_version": contract["contract_version"],
		"contract_generated_utc": contract["generated_utc"],
		"parameters_applied": {
			"min_periods": contract["min_periods"],
			"lags": contract["lags"],
			"rolling_windows": contract["rolling_windows"],
			"peak_months": contract["peak_months"],
		},
		# Capability flags. Explicit rather than inferable, because "no
		# promo_intensity column" and "promo_intensity happened to be dropped"
		# are indistinguishable downstream without this.
		"capabilities": {
			"has_promo": "promo_intensity" in df.columns,
			"has_weighted_dist": "weighted_dist" in df.columns,
		},
		"shape": {"rows": len(df), "columns": len(df.columns),
				  "brands": int(df[BRAND_COL].nunique()),
				  "n_features": len(features)},
		"features": features,
		"split_dates": split_dates,
		"n_test_origins": contract["split"]["n_test_origins"],
		"files": {k: v.name for k, v in files.items()},
	}


def run(category: str, horizon: int) -> dict:
	"""Write the final artifacts for one category at one horizon."""
	suppress_warnings()
	category = normalise_category(category)
	paths = get_paths(category)
	paths["tables_dir"].mkdir(parents=True, exist_ok=True)
	slug = paths["slug"]

	print("=" * 80)
	print(f"STEP 6 -- SAVE OUTPUTS: {category} (horizon={horizon})")
	print("=" * 80)

	contract, cpath = load_contract(paths, horizon)
	df, spath = load_split(paths, horizon)
	df = add_period_index(df)
	print(f"\nContract: {cpath.name}")
	print(f"Split:    {spath.name} -- {len(df):,} rows x {len(df.columns)} columns")

	out_dir = get_category_engineered_bymonth_dir(category)
	out_dir.mkdir(parents=True, exist_ok=True)

	files = {
		"feature_matrix": out_dir / f"{slug}_feature_matrix_h{horizon}.parquet",
		"series_index": out_dir / f"{slug}_series_index_h{horizon}.csv",
		"split_dates": out_dir / f"{slug}_split_dates_h{horizon}.json",
		"manifest": out_dir / f"{slug}_manifest_h{horizon}.json",
	}

	df.to_parquet(files["feature_matrix"], index=False)
	series_idx = build_series_index(df)
	series_idx.to_csv(files["series_index"], index=False)

	split_dates = read_back_split_dates(df)
	files["split_dates"].write_text(
		json.dumps(split_dates, indent=2), encoding="utf-8")

	manifest = build_manifest(df, contract, horizon, split_dates, files)
	files["manifest"].write_text(
		json.dumps(manifest, indent=2), encoding="utf-8")

	_report(manifest, series_idx, out_dir, files)
	_persist_table(manifest, paths, horizon)
	return manifest


def _report(m: dict, series_idx: pd.DataFrame, out_dir: Path, files: dict) -> None:
	print(f"\nARTIFACTS -> {out_dir}")
	for key, path in files.items():
		print(f"  {key:15} {path.name}")

	print("\nSUMMARY")
	print(f"  brands            = {m['shape']['brands']}")
	print(f"  rows              = {m['shape']['rows']:,}")
	print(f"  features          = {m['shape']['n_features']} "
		  f"(of {m['shape']['columns']} columns)")
	print(f"  promo available   = {m['capabilities']['has_promo']}")
	sd = m["split_dates"]
	print(f"  train             = {sd['train_start']} .. {sd['train_end']}")
	print(f"  val               = {sd['val_start']} .. {sd['val_end']}")
	print(f"  test              = {sd['test_start']} .. {sd['test_end']}")
	print(f"  test origins      = {m['n_test_origins']} at horizon "
		  f"{m['forecast_horizon']}")

	top = series_idx.head(5)
	print("\n  Largest brands by total units:")
	for _, r in top.iterrows():
		print(f"    {str(r[BRAND_COL]):<12} {r['total_units']:>14,.0f}  "
			  f"({r['n_periods']} periods)")


def _persist_table(m: dict, paths: dict, horizon: int) -> None:
	sd = m["split_dates"]
	rows = [
		("brands", m["shape"]["brands"]),
		("rows", m["shape"]["rows"]),
		("features", m["shape"]["n_features"]),
		("promotional data available", m["capabilities"]["has_promo"]),
		("train period", f"{sd['train_start']} .. {sd['train_end']}"),
		("validation period", f"{sd['val_start']} .. {sd['val_end']}"),
		("test period", f"{sd['test_start']} .. {sd['test_end']}"),
		("evaluable test origins", m["n_test_origins"]),
	]
	save_table(
		pd.DataFrame(rows, columns=["quantity", "value"]),
		f"step_6_final_dataset_h{horizon}",
		paths["tables_dir"],
		caption=(f"Final engineered dataset ({m['category']}, "
				 f"horizon {horizon} month(s))"),
		notes=[
			"The dataset delivered to the modelling stage. Split boundaries "
			"are read back from the labelled data rather than recomputed, so "
			"they describe what a model is actually trained and evaluated on.",
			"Feature counts differ across categories by design: Nielsen "
			"reports promotional measures for some categories and not others, "
			"and a feature that cannot be measured is omitted rather than "
			"filled with a placeholder value. Comparisons across categories "
			"must account for this difference in available information.",
		],
	)
	print(f"\n  Table    -> {paths['tables_dir']}")


def check_consistency(manifests: list[dict]) -> None:
	"""Report what the categories do and do not share.

	The alternative -- letting a downstream script discover mid-run that one
	category is missing a column -- produces either a crash or a silent
	comparison of models trained on different information.
	"""
	if len(manifests) < 2:
		return

	print("\n" + "=" * 80)
	print("CROSS-CATEGORY CONSISTENCY")
	print("=" * 80)

	sets = {m["category"]: set(m["features"]) for m in manifests}
	common = set.intersection(*sets.values())
	union = set.union(*sets.values())

	print(f"\n  Features common to all {len(sets)} categories: {len(common)}")
	print(f"  Features present in at least one:            {len(union)}")

	print("\n  Per category:")
	for m in manifests:
		cat = m["category"]
		missing = sorted(union - sets[cat])
		print(f"    {cat:<14} {len(sets[cat]):>3} features, "
			  f"promo={str(m['capabilities']['has_promo']):<5} "
			  f"peak_months={m['parameters_applied']['peak_months']}")
		if missing:
			print(f"      absent: {missing}")

	if len(common) < len(union):
		print("\n  NOTE: the categories do NOT share a feature space. A pooled "
			  "model or a\n  cross-category comparison must either restrict to "
			  f"the {len(common)} common features\n  or state explicitly that "
			  "the models saw different information.")
	else:
		print("\n  All categories share an identical feature space.")

	# Split geometry should match even where features do not -- it is derived
	# by the same proportional rule, so a difference means one category's panel
	# has a different length and the comparison is not like-for-like.
	print("\n  Split geometry:")
	for m in manifests:
		sd = m["split_dates"]
		print(f"    {m['category']:<14} train {sd['train_start']}..{sd['train_end']}  "
			  f"val {sd['val_start']}..{sd['val_end']}  "
			  f"test {sd['test_start']}..{sd['test_end']}  "
			  f"origins={m['n_test_origins']}")


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Step 6 -- write the final engineered artifacts."
	)
	parser.add_argument("--category", type=str, default=None)
	parser.add_argument("--all-categories", action="store_true")
	parser.add_argument(
		"--horizon", type=int, default=FORECAST_HORIZON,
		help=f"Forecast horizon in months. Default {FORECAST_HORIZON}.",
	)
	parser.add_argument(
		"--check-consistency", action="store_true",
		help=("After writing, report which features the categories share. "
			  "Implied by --all-categories."),
	)
	args = parser.parse_args()

	if args.all_categories:
		targets = list(CATEGORIES)
	elif args.category:
		targets = [args.category]
	else:
		parser.error("give --category or --all-categories")

	manifests: list[dict] = []
	failed: list[tuple[str, str]] = []
	for cat in targets:
		paths = get_paths(normalise_category(cat))
		paths["step_output_dir"].mkdir(parents=True, exist_ok=True)
		log = paths["step_output_dir"] / f"step_6_h{args.horizon}_console.log"
		try:
			with tee_console(log):
				manifests.append(run(cat, args.horizon))
		except ContractError as exc:
			print(f"\n!! {cat}: {exc}", file=sys.stderr)
			failed.append((cat, str(exc).splitlines()[0]))

	if args.check_consistency or args.all_categories:
		check_consistency(manifests)

	if failed:
		print(f"\n{len(failed)} of {len(targets)} categories failed:", file=sys.stderr)
		for cat, why in failed:
			print(f"  {cat}: {why}", file=sys.stderr)
		return 1

	print(f"\nStep 6 complete for {len(targets)} category(ies) at horizon "
		  f"{args.horizon}.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
