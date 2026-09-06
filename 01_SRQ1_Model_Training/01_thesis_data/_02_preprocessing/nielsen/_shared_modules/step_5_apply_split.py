#!/usr/bin/env python
"""
Step 5 -- Label the feature matrix with train / val / test for one category.

P0038 task 6, first half. Consumes step 4's matrix and the step 3 contract.

WHY THIS STEP CAN REFUSE
------------------------
Step 5 is the last point at which an unusable experiment can be stopped before
it produces numbers. The contract records `horizon_evaluable` and
`n_test_origins`; if the test window is shorter than the forecast horizon, then
NO forecast origin has its target month inside the window, and every metric
computed downstream would be over an empty set -- or worse, over a silently
truncated one that still returns a plausible-looking float.

Step 4 only warns, because a matrix is still a valid artifact. A SPLIT is not:
it is the object that defines the evaluation, so an unevaluable split is a
contradiction in terms. Hence `--allow-unevaluable` exists but must be typed
deliberately (DEC-HORIZON: H=12 has zero evaluable origins in every category).

WHY THE CUTOFFS COME FROM THE CONTRACT
--------------------------------------
`apply_split()` can derive cutoffs proportionally on its own. It is NOT allowed
to do so here. Step 3 already resolved and recorded them, and re-deriving would
mean two independent computations of the same boundary that agree only by
coincidence -- exactly the drift that let TRAIN_END/VAL_END rot to a 24-27% test
share (F25/F28). The contract is the single source; this step passes its values
through and then verifies the labels match what was asked for.

USAGE
    python step_5_apply_split.py --category CSD                 # H=3 (primary)
    python step_5_apply_split.py --category CSD --horizon 1     # anchor run
    python step_5_apply_split.py --all-categories --horizon 3
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
from engineer_features import apply_split  # noqa: E402
from pipeline_config import (  # noqa: E402
	CATEGORIES,
	FORECAST_HORIZON,
	get_paths,
	normalise_category,
	suppress_warnings,
)
from step_4_engineer_features import ContractError, load_contract, require  # noqa: E402

BRAND_COL = "brand"
SPLITS = ("train", "val", "test")


def load_matrix(paths: dict, horizon: int) -> tuple[pd.DataFrame, Path]:
	"""Read step 4's feature matrix for this category and horizon."""
	path = paths["step_output_dir"] / f"step_4_engineered_features_h{horizon}.parquet"
	if not path.exists():
		raise ContractError(
			f"No feature matrix for {paths['category']} at horizon {horizon}.\n"
			f"  Expected: {path}\n"
			f"  Run: python step_4_engineer_features.py --category "
			f"{paths['category']} --horizon {horizon}"
		)
	return pd.read_parquet(path), path


def check_evaluable(contract: dict, horizon: int, allow: bool) -> None:
	"""Refuse a split whose test window cannot evaluate the horizon.

	This is the guard the plan asked step 5 to own. `n_test_origins` is
	`n_test_months - horizon + 1`: an origin counts only when its target month
	falls inside the test window. At zero, every downstream metric is computed
	over nothing -- and an empty mean is not an error in pandas, it is NaN, or
	after a dropna, a confident number derived from no data.
	"""
	split = contract["split"]
	origins = split["n_test_origins"]

	if split["horizon_evaluable"] and origins > 0:
		return

	message = (
		f"Split is not evaluable at horizon {horizon}.\n"
		f"  Test window: {split['n_test_months']} month(s)\n"
		f"  Forecast origins with their target inside it: {origins}\n"
		f"  A forecast made at origin t targets t+{horizon}. With a test window "
		f"shorter than the horizon, no origin's target lands in the window, so "
		f"every downstream metric would be computed over an empty set.\n"
		f"  Lower --horizon, or extend the observed period."
	)
	if not allow:
		raise ContractError(
			message + "\n  Pass --allow-unevaluable to label the split anyway "
			"(it will not be usable for evaluation)."
		)
	print(f"\n  !! PROCEEDING ANYWAY (--allow-unevaluable)\n  {message}")


def verify_labels(df: pd.DataFrame, contract: dict) -> dict:
	"""Confirm the labels match the boundaries the contract specified.

	Same principle as step 4's output check: `apply_split()` accepts cutoffs and
	labels rows without complaint, so agreement between the contract and the
	labelled frame has to be asserted, not assumed. Counting distinct MONTHS
	rather than rows is what makes this meaningful -- row counts vary with how
	many brands were active, month counts are the split itself.
	"""
	split = contract["split"]
	counts = {}
	for name in SPLITS:
		sub = df[df["split"] == name]
		counts[name] = {
			"rows": len(sub),
			"months": int(sub["date"].nunique()),
			"brands": int(sub[BRAND_COL].nunique()),
		}

	empty = [n for n in SPLITS if counts[n]["rows"] == 0]
	if empty:
		raise ContractError(
			f"Split produced empty partition(s): {empty}. Every partition must "
			f"be non-empty; an empty validation or test set is never intended."
		)

	expected = {
		"train": split["n_train_months"],
		"val": split["n_val_months"],
		"test": split["n_test_months"],
	}
	mismatched = {
		n: (expected[n], counts[n]["months"])
		for n in SPLITS
		if counts[n]["months"] != expected[n]
	}
	if mismatched:
		raise ContractError(
			f"Labelled month counts disagree with the contract "
			f"(expected, actual): {mismatched}.\n"
			f"  The contract's cutoffs were passed to apply_split, so this "
			f"means the matrix covers a different period than step 3 measured. "
			f"Re-run step 3 and step 4 for this category and horizon."
		)

	# Ordering is the property that makes this a TIME-SERIES split rather than a
	# random one. Cheap to check, and its failure is silent: a shuffled split
	# trains on the future and reports excellent, meaningless accuracy.
	bounds = {n: (df.loc[df["split"] == n, "date"].min(),
				  df.loc[df["split"] == n, "date"].max()) for n in SPLITS}
	if not (bounds["train"][1] < bounds["val"][0] < bounds["val"][1] < bounds["test"][0]):
		raise ContractError(
			f"Split partitions are not strictly ordered in time: "
			f"train {bounds['train']}, val {bounds['val']}, test {bounds['test']}. "
			f"A temporal split must not overlap -- overlapping partitions train "
			f"on the future."
		)

	for name in SPLITS:
		counts[name]["start"] = bounds[name][0].strftime("%Y-%m")
		counts[name]["end"] = bounds[name][1].strftime("%Y-%m")
	return counts


def run(category: str, horizon: int, allow_unevaluable: bool) -> pd.DataFrame:
	"""Label and persist the split for one category at one horizon."""
	suppress_warnings()
	category = normalise_category(category)
	paths = get_paths(category)
	paths["tables_dir"].mkdir(parents=True, exist_ok=True)

	print("=" * 80)
	print(f"STEP 5 -- APPLY SPLIT: {category} (horizon={horizon})")
	print("=" * 80)

	contract, cpath = load_contract(paths, horizon)
	print(f"\nContract: {cpath.name} (version {contract['contract_version']})")

	check_evaluable(contract, horizon, allow_unevaluable)

	matrix, mpath = load_matrix(paths, horizon)
	print(f"Matrix:   {mpath.name} -- {len(matrix):,} rows x {len(matrix.columns)} columns")

	# Cutoffs come from the contract, never re-derived here. See module docstring.
	split = require(contract, "split", cpath)
	train_end = tuple(split["train_end"])
	val_end = tuple(split["val_end"])
	print(f"\nApplying cutoffs from the contract: train<={train_end}, val<={val_end}")

	labelled = apply_split(matrix, train_end=train_end, val_end=val_end)
	counts = verify_labels(labelled, contract)
	_report(counts, contract, horizon)
	_persist(labelled, counts, contract, paths, horizon)
	return labelled


def _report(counts: dict, contract: dict, horizon: int) -> None:
	total_rows = sum(counts[n]["rows"] for n in SPLITS)
	print("\nSPLIT APPLIED")
	for name in SPLITS:
		c = counts[name]
		print(f"  {name:5} = {c['months']:2} months ({c['start']} .. {c['end']}), "
			  f"{c['rows']:6,} rows, {c['brands']:3} brands "
			  f"[{c['rows'] / total_rows:5.1%}]")
	print(f"  test origins at horizon {horizon}: "
		  f"{contract['split']['n_test_origins']}")


def _persist(df: pd.DataFrame, counts: dict, contract: dict,
			 paths: dict, horizon: int) -> None:
	out = paths["step_output_dir"] / f"step_5_split_applied_h{horizon}.parquet"
	df.to_parquet(out, index=False)
	print(f"\n  Split    -> {out}")

	sidecar = paths["step_output_dir"] / f"step_5_log_h{horizon}.json"
	sidecar.write_text(json.dumps({
		"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
		"generated_by": "step_5_apply_split.py",
		"category": contract["category"],
		"forecast_horizon": horizon,
		"contract_version": contract["contract_version"],
		"cutoffs_applied": {
			"train_end": contract["split"]["train_end"],
			"val_end": contract["split"]["val_end"],
		},
		"n_test_origins": contract["split"]["n_test_origins"],
		"partitions": counts,
		"output_parquet": out.name,
	}, indent=2), encoding="utf-8")
	print(f"  Log      -> {sidecar}")

	rows = []
	for name in SPLITS:
		c = counts[name]
		rows.append((name, c["months"], f"{c['start']} .. {c['end']}",
					 c["rows"], c["brands"]))
	save_table(
		pd.DataFrame(rows, columns=["partition", "months", "period",
									"rows", "brands"]),
		f"step_5_split_h{horizon}",
		paths["tables_dir"],
		caption=(f"Temporal split ({contract['category']}, "
				 f"horizon {horizon} month(s))"),
		notes=[
			"Partitions are contiguous in time and non-overlapping: every "
			"validation month follows every training month, and every test "
			"month follows every validation month. This preserves the "
			"forecasting task, in which only the past is available at the time "
			"a prediction is made.",
			"Boundaries are proportional to the observed period rather than "
			"fixed dates, so the ratio holds as the panel grows and categories "
			"beginning at different dates remain comparable.",
			f"At a {horizon}-month horizon the test window admits "
			f"{contract['split']['n_test_origins']} forecast origin(s): an "
			f"origin is counted only when the month it targets falls inside "
			f"the window.",
		],
	)
	print(f"  Table    -> {paths['tables_dir']}")


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Step 5 -- label the feature matrix train/val/test."
	)
	parser.add_argument("--category", type=str, default=None)
	parser.add_argument("--all-categories", action="store_true")
	parser.add_argument(
		"--horizon", type=int, default=FORECAST_HORIZON,
		help=f"Forecast horizon in months. Default {FORECAST_HORIZON}.",
	)
	parser.add_argument(
		"--allow-unevaluable", action="store_true",
		help=("Label the split even when the contract reports zero evaluable "
			  "test origins. The result cannot be used for evaluation; this "
			  "exists for inspection only."),
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
		log = paths["step_output_dir"] / f"step_5_h{args.horizon}_console.log"
		try:
			with tee_console(log):
				run(cat, args.horizon, args.allow_unevaluable)
		except ContractError as exc:
			print(f"\n!! {cat}: {exc}", file=sys.stderr)
			failed.append((cat, str(exc).splitlines()[0]))

	if failed:
		print(f"\n{len(failed)} of {len(targets)} categories failed:", file=sys.stderr)
		for cat, why in failed:
			print(f"  {cat}: {why}", file=sys.stderr)
		return 1

	print(f"\nStep 5 complete for {len(targets)} category(ies) at horizon "
		  f"{args.horizon}.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
