"""Run the full Nielsen preprocessing pipeline for one category at one horizon.

This is the shared orchestrator that replaces the four per-category ones. Those
were 184 lines each and differed only in the category name (F-plan), which is
exactly the duplication DEC-DISCOVER-COLUMNS exists to prevent: a fix applied to one
was a fix missing from three.

	Steps 0-2 are horizon-independent -- they validate the cache, build the
	brand x month panel, and describe it. Nothing about them changes when the
	forecast horizon changes.

	Steps 3-6 are horizon-dependent. Step 3 measures the panel and writes a
	contract; steps 4-6 apply it. Two horizons therefore mean two contracts and
	two sets of artifacts, distinguished by the h{N} suffix.

That split is the reason for --skip-shared: re-running H=3 after H=1 does not
need steps 0-2 repeated, and on CSD that is most of the wall clock.

Steps are invoked in-process, not via subprocess. Each step module already
exposes a clean run(); calling it directly keeps tracebacks intact and lets the
orchestrator hold the per-step timing and failure record itself.

Usage:
	python run_preprocessing.py --category CSD --horizon 3
	python run_preprocessing.py --all-categories --horizon 3 --skip-shared
	python run_preprocessing.py --category CSD --horizons 1,3
	python run_preprocessing.py --category CSD --from-step 4
"""
from __future__ import annotations

import argparse
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path

_HERE = Path(__file__).resolve().parent
def _find_repo_root() -> Path:
    """Walk up from this file to the repo root (anchored on .env.example).

    Replaces a hard-coded parents[N] hop, which silently points at the wrong
    directory whenever a script moves between folder depths -- as happened in
    the 2026-09-06 restructure.
    """
    _start = Path(__file__).resolve().parent
    for _cand in (_start, *_start.parents):
        if any((_cand / _a).exists() for _a in (".env.example", ".env", "PATHS.py")):
            return _cand
    raise FileNotFoundError(f"Could not find project root above {_start}")


_REPO_ROOT = _find_repo_root()
for _p in (str(_HERE), str(_REPO_ROOT)):
	if _p not in sys.path:
		sys.path.insert(0, _p)

from pipeline_config import (  # noqa: E402
	CATEGORIES,
	FORECAST_HORIZON,
	get_paths,
	normalise_category,
	suppress_warnings,
)
from capture_utils import tee_console  # noqa: E402

import step_0_validate_cache  # noqa: E402
import step_1_load_and_aggregate  # noqa: E402
import step_2_eda_descriptive  # noqa: E402
import step_3_derive_params  # noqa: E402
import step_4_engineer_features  # noqa: E402
import step_5_apply_split  # noqa: E402
import step_6_save_outputs  # noqa: E402

def print_header(text: str) -> None:
	"""Plain rule, matching the convention the steps themselves use.

	Deliberately not terminal_utils.print_orchestrator_start: those helpers
	render rich panels containing a U+2713 glyph, which raises
	UnicodeEncodeError under the cp1252 default encoding the moment the console
	is teed to a file on Windows.
	"""
	print("\n" + "=" * 80)
	print(f"  {text}")
	print("=" * 80)


# ---------------------------------------------------------------------------
# The pipeline, declared rather than hardcoded into a call sequence.
#
# `horizon_dependent` is the only structural fact the orchestrator needs about a
# step: it decides both which steps --skip-shared may skip and whether the h{N}
# suffix belongs in the artifact names. Adding a step means adding a row here.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Step:
	num: int
	name: str
	module: object
	horizon_dependent: bool


PIPELINE: tuple[Step, ...] = (
	Step(0, "validate cache", step_0_validate_cache, False),
	Step(1, "load and aggregate", step_1_load_and_aggregate, False),
	Step(2, "descriptive EDA", step_2_eda_descriptive, False),
	Step(3, "derive contract", step_3_derive_params, True),
	Step(4, "engineer features", step_4_engineer_features, True),
	Step(5, "apply split", step_5_apply_split, True),
	Step(6, "save outputs", step_6_save_outputs, True),
)


@dataclass
class StepResult:
	step: Step
	status: str          # "ok" | "failed" | "skipped"
	seconds: float = 0.0
	detail: str = ""
	# What the step DID, as opposed to how long it took. Populated by
	# _step_metrics() from the value the step already returns; see there for why
	# this is extracted centrally rather than added to each step module.
	metrics: dict = field(default_factory=dict)


@dataclass
class RunResult:
	category: str
	horizon: int
	steps: list[StepResult] = field(default_factory=list)

	@property
	def failed(self) -> list[StepResult]:
		return [r for r in self.steps if r.status == "failed"]

	@property
	def ok(self) -> bool:
		return not self.failed


def _invoke(step: Step, category: str, horizon: int, make_plots: bool,
			allow_unevaluable: bool):
	"""Call one step's run() with the arguments that step actually takes.

	Each step's signature differs because each step needs different things, and
	flattening them into a single **kwargs call would hide that. The mapping is
	explicit so a signature change fails loudly here rather than silently
	passing the wrong positional argument.
	"""
	if step.num == 0:
		return step.module.run(category)
	if step.num == 1:
		return step.module.run(category)
	if step.num == 2:
		return step.module.run(category, make_plots=make_plots)
	if step.num == 3:
		return step.module.run(category, horizon)
	if step.num == 4:
		return step.module.run(category, horizon)
	if step.num == 5:
		return step.module.run(category, horizon, allow_unevaluable)
	if step.num == 6:
		return step.module.run(category, horizon)
	raise ValueError(f"No invocation defined for step {step.num}")


# The brand column name, duplicated from the step modules (each of steps 2-6
# defines its own BRAND_COL = "brand"). Importing one step's copy here would
# make the orchestrator arbitrarily depend on that step; the value is only used
# to compute an optional summary, and every use is guarded by a column check, so
# a rename degrades the metric rather than breaking the run.
BRAND_COL = "brand"


def _step_metrics(step: Step, out) -> dict:
	"""What the step DID, taken from the value it already returns.

	Added 2026-09-07 (P0046). The manifest recorded that a step ran and how long
	it took, which evidences execution but not *content*: an appendix reader
	could not tell whether step 4 kept 40 brands or 4, and a silent collapse in
	row count -- the failure mode most likely to invalidate a result -- looked
	identical to a healthy run.

	Extracted CENTRALLY, from each step's existing return value, rather than by
	adding instrumentation to seven step modules. Every step already returns
	something meaningful (a DataFrame, a contract, a manifest) and the
	orchestrator was discarding all of it except step 2's failure list. Reading
	what is already there keeps the step modules untouched, so this cannot drift
	from what they compute -- there is no second code path to keep in sync.

	Unknown shapes yield {} rather than raising: a metric is a nice-to-have, and
	no pipeline run should fail because a summary could not be computed.
	"""
	try:
		if step.num == 0:                       # dict: cache validation
			return {"views_required": len(out.get("required", [])),
					"views_missing": len(out.get("missing", [])),
					"views_empty": len(out.get("empty", []))}

		if step.num == 1:                       # DataFrame: aggregated panel
			m = {"rows": len(out), "columns": len(out.columns)}
			if BRAND_COL in out.columns:
				m["brands"] = int(out[BRAND_COL].nunique())
			if "date" in out.columns and len(out):
				m["period"] = (f"{out['date'].min():%Y-%m} .. "
							   f"{out['date'].max():%Y-%m}")
			return m

		if step.num == 2:                       # EdaContext
			return {"tables_written": len(getattr(out, "tables_written", [])),
					"plots_written": len(getattr(out, "plots_written", [])),
					"sections_skipped": len(getattr(out, "skipped", [])),
					"sections_failed": len(getattr(out, "failed", []))}

		if step.num == 3:                       # dict: measured contract
			m = {"lags": len(out.get("lags", [])),
				 "rolling_windows": len(out.get("rolling_windows", [])),
				 "min_periods": out.get("min_periods"),
				 "log_transform_target": out.get("log_transform_target")}
			# The retention block is the record of what the contract EXCLUDES,
			# which is the number a reader most wants and the one a timing-only
			# log hides completely.
			ret = out.get("retention") or {}
			for k in ("brands_before", "brands_after", "rows_before", "rows_after"):
				if k in ret:
					m[k] = ret[k]
			return m

		if step.num == 4:                       # DataFrame: feature matrix
			m = {"rows": len(out), "columns": len(out.columns)}
			if BRAND_COL in out.columns:
				m["brands"] = int(out[BRAND_COL].nunique())
			return m

		if step.num == 5:                       # DataFrame: labelled split
			m = {"rows": len(out)}
			if "split" in out.columns:
				m["split_rows"] = {k: int(v) for k, v
								   in out["split"].value_counts().items()}
			return m

		if step.num == 6:                       # dict: output manifest
			m = dict(out.get("shape", {}))
			m["n_test_origins"] = out.get("n_test_origins")
			m["files"] = len(out.get("files", {}))
			return m

	except Exception as exc:  # noqa: BLE001 -- a metric must never fail a run
		return {"metrics_error": f"{type(exc).__name__}: {exc}"}

	return {}


def _check_step_outcome(step: Step, result) -> str:
	"""Return a failure reason, or "" when the step succeeded.

	Step 2 is the one step that reports partial failure through its return value
	rather than by raising: individual EDA sections are caught and collected so
	one bad section does not lose the other forty. The orchestrator has to read
	that, otherwise a step that printed FAILED would be recorded as ok.
	"""
	if step.num == 2 and getattr(result, "failed", None):
		names = ", ".join(title for title, _ in result.failed)
		return f"{len(result.failed)} EDA section(s) failed: {names}"
	return ""


def run_pipeline(
	category: str,
	horizon: int,
	*,
	from_step: int = 0,
	to_step: int = 6,
	skip_shared: bool = False,
	make_plots: bool = True,
	allow_unevaluable: bool = False,
) -> RunResult:
	"""Run steps from_step..to_step for one category at one horizon."""
	category = normalise_category(category)
	result = RunResult(category=category, horizon=horizon)

	for step in PIPELINE:
		if not (from_step <= step.num <= to_step):
			continue

		if skip_shared and not step.horizon_dependent:
			result.steps.append(StepResult(
				step, "skipped",
				detail="horizon-independent; --skip-shared",
			))
			continue

		label = f"STEP {step.num} -- {step.name}"
		if step.horizon_dependent:
			label += f"  (H={horizon})"
		print_header(label)

		started = time.perf_counter()
		try:
			out = _invoke(step, category, horizon, make_plots, allow_unevaluable)
		except Exception as exc:  # noqa: BLE001 -- recorded, then re-raised as a stop
			elapsed = time.perf_counter() - started
			traceback.print_exc()
			result.steps.append(StepResult(
				step, "failed", elapsed, f"{type(exc).__name__}: {exc}",
			))
			# A later step consumes an earlier step's output, so continuing past
			# a failure would either crash confusingly or -- worse -- succeed
			# against a stale artifact from a previous run.
			break

		elapsed = time.perf_counter() - started
		reason = _check_step_outcome(step, out)
		if reason:
			result.steps.append(StepResult(step, "failed", elapsed, reason))
			break

		result.steps.append(StepResult(step, "ok", elapsed,
									   metrics=_step_metrics(step, out)))

	return result


def write_run_manifest(results: list[RunResult]) -> list[Path]:
	"""Persist the run record as JSON, one manifest per category.

	Added 2026-09-06 (P0046 F20). The orchestrator already measured per-step
	timing and outcome, but only *printed* them: the run-level record existed
	solely as prose inside run_preprocessing_console.log. Nothing could answer
	"when did RTD last run, did every step pass, how long did step 4 take?"
	without a human reading a log file.

	Steps 0, 1, 4 and 5 write their own step_N_log.json; steps 2, 3 and 6 write
	console output only. Those step logs are RICHER than this manifest for the
	steps that have them -- step 4's log carries the full reduction chain
	(rows_in, rows_calendar, rows_filtered, rows_out, brands at each stage) --
	but none of them records the RUN: the ordering, which steps were skipped,
	whether the run succeeded as a whole. That is what this file adds, and the
	two are complementary rather than redundant. The appendix reads the step
	logs for content and this manifest for execution.

	Two things this deliberately does NOT do, both learned by getting them
	wrong first:

	* It does not write a single file. --all-categories produces results for
	  every category, and filing them all under results[0]'s directory would
	  put RTD's record in CSD's folder. Runs are grouped by category, and each
	  category owns its own manifest.

	* It does not overwrite. Horizons run separately (--horizon 1, then
	  --horizon 3), so a plain write would erase the H=1 record the moment H=3
	  ran, and the appendix would report one horizon as though it were the
	  whole pipeline. Horizons not in this run are carried forward; horizons
	  in this run are replaced.
	"""
	import json
	from datetime import datetime, timezone

	def _entry(r: RunResult) -> dict:
		return {
			"horizon": r.horizon,
			"ok": r.ok,
			"total_seconds": round(sum(st.seconds for st in r.steps), 3),
			"steps": [
				{"step": st.step.num, "name": st.step.name,
				 "status": st.status, "seconds": round(st.seconds, 3),
				 **({"detail": st.detail} if st.detail else {}),
				 **({"metrics": st.metrics} if st.metrics else {})}
				for st in r.steps
			],
		}

	by_category: dict[str, list[RunResult]] = {}
	for r in results:
		by_category.setdefault(r.category, []).append(r)

	written: list[Path] = []
	stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

	for category, runs in by_category.items():
		out = get_paths(category)["step_output_dir"] / "run_manifest.json"
		fresh = {r.horizon: _entry(r) for r in runs}

		# Carry forward horizons this run did not touch. An unreadable manifest
		# is replaced rather than raised on: losing an old record is a smaller
		# harm than failing a pipeline run that otherwise succeeded.
		if out.is_file():
			try:
				prior = json.loads(out.read_text(encoding="utf-8"))
				for e in prior.get("runs", []):
					if e.get("horizon") not in fresh:
						fresh[e["horizon"]] = e
			except (json.JSONDecodeError, OSError, KeyError, TypeError) as exc:
				print(f"  (existing manifest at {out} unreadable, replacing: {exc})")

		payload = {
			"category": category,
			"written_at_utc": stamp,
			"runs": [fresh[h] for h in sorted(fresh)],
		}
		out.parent.mkdir(parents=True, exist_ok=True)
		out.write_text(json.dumps(payload, indent=2), encoding="utf-8",
					   newline="\n")
		written.append(out)
		print(f"\nRun manifest -> {out}")

	return written


def _fmt_metrics(m: dict) -> str:
	"""Render a step's metrics as one compact line, e.g. 'rows=1,472  brands=38'."""
	parts = []
	for k, v in m.items():
		if isinstance(v, dict):
			inner = " ".join(f"{ik}={iv:,}" if isinstance(iv, int) else f"{ik}={iv}"
							 for ik, iv in v.items())
			parts.append(f"{k}=[{inner}]")
		elif isinstance(v, int) and not isinstance(v, bool):
			parts.append(f"{k}={v:,}")
		elif v is not None:
			parts.append(f"{k}={v}")
	return "  ".join(parts)


def print_summary(results: list[RunResult]) -> None:
	print_header("PIPELINE SUMMARY")

	for res in results:
		total = sum(r.seconds for r in res.steps)
		mark = "OK" if res.ok else "FAILED"
		print(f"\n  {res.category}  H={res.horizon}   [{mark}]   {total:6.1f}s")
		for r in res.steps:
			if r.status == "skipped":
				print(f"    step {r.step.num}  {'skipped':>9}   -- {r.detail}")
			else:
				flag = "" if r.status == "ok" else "  <-- FAILED"
				print(f"    step {r.step.num}  {r.seconds:7.1f}s   "
					  f"{r.step.name}{flag}")
				if r.metrics:
					# One line, so a collapsed row or brand count is visible
					# here rather than only after opening the manifest.
					print(f"             {_fmt_metrics(r.metrics)}")
				if r.detail:
					print(f"             {r.detail}")

	failed = [r for r in results if not r.ok]
	print()
	if failed:
		print(f"  {len(failed)} of {len(results)} run(s) FAILED:")
		for res in failed:
			for r in res.failed:
				print(f"    {res.category} H={res.horizon} step {r.step.num}: "
					  f"{r.detail}")
	else:
		print(f"  All {len(results)} run(s) completed.")


def _parse_horizons(args, parser) -> list[int]:
	if args.horizons:
		try:
			horizons = [int(h) for h in args.horizons.split(",") if h.strip()]
		except ValueError:
			parser.error(f"--horizons must be a comma-separated list of "
						 f"integers; got {args.horizons!r}")
		if not horizons:
			parser.error("--horizons was empty")
	else:
		horizons = [args.horizon]

	for h in horizons:
		if h < 1:
			parser.error(f"horizon must be >= 1; got {h}")
	return horizons


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Run the Nielsen preprocessing pipeline (steps 0-6).",
	)
	target = parser.add_mutually_exclusive_group(required=True)
	target.add_argument("--category", help="Category to process")
	target.add_argument("--all-categories", action="store_true",
						help="Process every category in turn")

	horizon = parser.add_mutually_exclusive_group()
	horizon.add_argument(
		"--horizon", type=int, default=FORECAST_HORIZON,
		help=f"Forecast horizon in months (default {FORECAST_HORIZON}). "
			 "The primary reported horizon is 3 (DEC-HORIZON).",
	)
	horizon.add_argument(
		"--horizons",
		help="Comma-separated horizons to run in sequence, e.g. 1,3. Steps 0-2 "
			 "run once for the first horizon and are skipped thereafter, since "
			 "they do not depend on the horizon.",
	)

	parser.add_argument("--from-step", type=int, default=0, metavar="N",
						help="First step to run (default 0).")
	parser.add_argument("--to-step", type=int, default=6, metavar="N",
						help="Last step to run (default 6).")
	parser.add_argument(
		"--skip-shared", action="store_true",
		help="Skip steps 0-2. They are horizon-independent, so this is the "
			 "fast path when re-running a second horizon or iterating on the "
			 "contract.",
	)
	parser.add_argument("--no-plots", action="store_true",
						help="Step 2 computes tables without rendering figures.")
	parser.add_argument(
		"--allow-unevaluable", action="store_true",
		help="Let step 5 label a split with zero evaluable test origins. The "
			 "result cannot be evaluated; this exists for inspection only.",
	)
	parser.add_argument("--no-log", action="store_true",
						help="Do not tee the orchestrator console to a file.")

	args = parser.parse_args()

	if not (0 <= args.from_step <= 6 and 0 <= args.to_step <= 6):
		parser.error("--from-step and --to-step must be between 0 and 6")
	if args.from_step > args.to_step:
		parser.error(f"--from-step ({args.from_step}) is after --to-step "
					 f"({args.to_step})")

	horizons = _parse_horizons(args, parser)
	categories = list(CATEGORIES) if args.all_categories else [args.category]

	suppress_warnings()

	results: list[RunResult] = []
	for category in categories:
		category = normalise_category(category)
		for i, h in enumerate(horizons):
			# Steps 0-2 produce the same panel regardless of horizon, so on a
			# multi-horizon run they are skipped after the first pass. An
			# explicit --skip-shared applies to every pass.
			skip_shared = args.skip_shared or i > 0
			results.append(run_pipeline(
				category, h,
				from_step=args.from_step,
				to_step=args.to_step,
				skip_shared=skip_shared,
				make_plots=not args.no_plots,
				allow_unevaluable=args.allow_unevaluable,
			))

	print_summary(results)
	write_run_manifest(results)
	return 1 if any(not r.ok for r in results) else 0


if __name__ == "__main__":
	if "--no-log" in sys.argv:
		raise SystemExit(main())

	# Tee the orchestrator's own console. Each step already writes its own
	# step_N_h{M}_console.log; this file is the run-level view -- the ordering,
	# the timings and the summary -- which no individual step log contains.
	_args = sys.argv[1:]
	_cat = None
	for _i, _a in enumerate(_args):
		if _a == "--category" and _i + 1 < len(_args):
			_cat = _args[_i + 1]
		elif _a.startswith("--category="):
			_cat = _a.split("=", 1)[1]

	if _cat is None:
		# --all-categories has no single output dir to own; log under the first.
		_cat = CATEGORIES[0]

	try:
		_paths = get_paths(normalise_category(_cat))
	except Exception:
		raise SystemExit(main())

	_paths["step_output_dir"].mkdir(parents=True, exist_ok=True)
	_log = _paths["step_output_dir"] / "run_preprocessing_console.log"
	with tee_console(_log):
		_rc = main()
	print(f"\nOrchestrator log: {_log}")
	raise SystemExit(_rc)
