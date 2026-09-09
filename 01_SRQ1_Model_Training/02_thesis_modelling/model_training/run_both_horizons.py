"""
Run the SRQ1 suite at both reported horizons.
=============================================

DEC-HORIZON (Brian, 2026-09-07) requires H=1 and H=3 both benchmarked. This runs
the suite twice, once per horizon, by setting SRQ1_HORIZON for each child
process. Every script then picks its own input matrix and output directory from
that one value (see srq1/_horizon.py), so:

  * H=3 writes to  05_thesis_results/model_benchmark/{tables,figures,models}/
  * H=1 writes to  05_thesis_results/model_benchmark/h1/{...}/

**An H=1 run cannot overwrite an H=3 result.** That is the whole point of the
split, and it is why this is a wrapper rather than a note in a README telling
someone to export a variable by hand.

ORDER MATTERS. The suite is a dependency chain, not a bag of scripts:

    benchmark      -> metrics.csv          (untuned baseline, all models)
    benchmark_cv   -> cv_metrics.csv       (rolling-origin CV; selection input)
    benchmark_tuned-> tuned_metrics.csv    (Optuna; needs the CV study)
    calibration    -> calibration.csv      (reads tuned_params.json)
    train_persist  -> models/              (selects on cv_metrics, serves SRQ2)
    figures        -> figures/             (read metrics.csv + tuned_params)

Running these out of order does not crash -- several guard their reads with
is_file() and degrade silently instead, which is exactly how model selection
came to fall through to a hardcoded default (F25). Hence one ordered list here.

USAGE
    python run_both_horizons.py                 # both horizons, full suite
    python run_both_horizons.py --horizon 3     # one horizon
    python run_both_horizons.py --dry-run       # print the plan, run nothing
    python run_both_horizons.py --only benchmark,benchmark_cv

WALL CLOCK: the tuned stage is ~24 Optuna studies and stability is 40 fits, so a
full two-horizon run is hours, not minutes. --only exists for that reason.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRQ1 = HERE / "srq1"


def _interpreter() -> str:
    """The project venv's python, not whatever `python` resolves to.

    A bare `python` on this machine is a system 3.14 carrying DIFFERENT library
    versions from the venv (measured 2026-09-08: xgboost 3.4.1/3.2.0, lightgbm
    4.7.0/4.6.0, sklearn 1.9.0/1.8.0). Model output is version-sensitive, so a
    suite run under the wrong interpreter produces numbers that cannot be
    compared with the committed results -- and silently, because both
    interpreters import cleanly and run to completion.

    That would defeat DEC-DETERMINISM (F18): pinning XGB_N_JOBS=1 makes a run
    reproducible only against the same library build. Every script's own usage
    line names .venv/Scripts/python.exe; this makes that the default rather than
    a convention someone has to remember.
    """
    root = next((q for q in HERE.parents if (q / "PATHS.py").is_file()), None)
    if root is not None:
        for rel in ("Scripts/python.exe", "bin/python"):
            cand = root / ".venv" / rel
            if cand.is_file():
                return str(cand)
    print("  !! .venv not found -- falling back to the current interpreter. "
          "Library versions may differ from the committed results.", flush=True)
    return sys.executable


PYTHON = _interpreter()

# name -> script path. Ordered by dependency; see the module docstring.
STAGES: list[tuple[str, Path]] = [
    # -- tier 1: no dependencies, produce the inputs everything else selects on
    ("benchmark",        SRQ1 / "srq1_benchmark.py"),
    ("benchmark_cv",     SRQ1 / "srq1_benchmark_cv.py"),
    ("benchmark_tuned",  SRQ1 / "srq1_benchmark_tuned.py"),
    ("baselines_stat",   SRQ1 / "srq1_baselines_stat.py"),
    # -- tier 2: read tuned_params.json / cv_params.json
    ("calibration",      SRQ1 / "srq1_calibration.py"),
    ("mase",             SRQ1 / "srq1_mase.py"),
    ("demand_classes",   SRQ1 / "srq1_demand_classes.py"),
    ("stability",        SRQ1 / "srq1_stability.py"),
    # -- tier 3: separate modelling questions, same features
    ("ridge_cv",         SRQ1 / "srq1_ridge_cv.py"),
    ("pooled",           SRQ1 / "srq1_pooled.py"),
    ("pooled_perbrand",  SRQ1 / "srq1_pooled_perbrand.py"),
    ("ridge_pooled",     SRQ1 / "srq1_ridge_pooled.py"),
    # -- tier 4: feature/ablation evidence (holiday enrichment, VIF, SHAP)
    ("feature_diag",     SRQ1 / "srq1_feature_diagnostics.py"),
    ("holiday_ablation", SRQ1 / "srq1_holiday_ablation.py"),
    ("holiday_tuned",    SRQ1 / "srq1_holiday_ablation_tuned.py"),
    # -- tier 5: serving + reporting, must follow selection inputs
    ("train_persist",    HERE / "train_and_persist.py"),
    ("training_report",  HERE / "training_report.py"),
    ("shap_figures",     SRQ1 / "srq1_generate_shap_figures.py"),
    ("perf_figures",     SRQ1 / "srq1_generate_performance_figures.py"),
    ("enrich_appendix",  SRQ1 / "srq1_export_enrichment_appendix.py"),
]


# Stages deliberately NOT in the default run, and why.
#
#   srq1_profiling.py  -- measures memory/latency at n_jobs=-1 (DEC-DETERMINISM).
#                         It is a resource measurement, not an accuracy result,
#                         and it is horizon-insensitive by design.
#
# NOTE: stability, pooled and the holiday ablations WERE excluded here. That was
# wrong -- the horizon fix changed the features they all read, so their tables
# describe a different task than the one the thesis now reports. Only profiling
# stays out.
OPTIONAL = ("profiling",)

HORIZONS = (3, 1)  # primary first, so a run interrupted early still has H=3


def _results_root_for(horizon: int) -> Path:
    """Where `horizon` writes its results.

    Mirrors srq1/_horizon.results_root(), but takes the horizon as an argument.
    That module resolves SRQ1_HORIZON once at import, so importing it here would
    pin this parent process to a single horizon while it orchestrates both.
    """
    sys.path.insert(0, str(SRQ1))
    from _horizon import PRIMARY  # noqa: E402
    from PATHS import THESIS_RESULTS_SRQ1_DIR  # noqa: E402
    return (THESIS_RESULTS_SRQ1_DIR if horizon == PRIMARY
            else THESIS_RESULTS_SRQ1_DIR / f"h{horizon}")


# The artefact each stage writes, relative to its horizon's results root. Used
# ONLY by --resume to decide what is already done. A stage with no entry here
# always runs.
#
# Resume exists because this suite gets killed: it is hours long and competes
# for RAM with everything else on the machine. Without it, a kill in the last
# stage discards every completed Optuna study before it.
PRODUCES: dict[str, str] = {
    "benchmark":        "tables/metrics.csv",
    "benchmark_cv":     "tables/cv_metrics.csv",
    "benchmark_tuned":  "tables/tuned_metrics.csv",
    "baselines_stat":   "tables/stat_baselines.csv",
    "calibration":      "tables/calibration.csv",
    "mase":             "tables/mase.csv",
    "demand_classes":   "tables/demand_classes.csv",
    "stability":        "tables/stability.csv",
    "ridge_cv":         "tables/ridge_cv_alpha.csv",
    "pooled":           "tables/pooled_metrics.csv",
    "pooled_perbrand":  "tables/pooled_perbrand.csv",
    "ridge_pooled":     "tables/ridge_pooled.csv",
    "feature_diag":     "tables/feature_vif.csv",
    "holiday_ablation": "tables/holiday_ablation_metrics.csv",
    "holiday_tuned":    "tables/holiday_ablation_tuned_metrics.csv",
    "train_persist":    "models/index.json",
    "training_report":  "tables/training_report.md",
    "shap_figures":     "tables/shap_importance.csv",
}



def _done(name: str, horizon: int, started: float) -> bool:
    """True if this stage's artefact exists AND was written by THIS run.

    The mtime test is the point. An artefact left over from a previous run
    describes different code or different data, and treating it as done is how a
    "completed" suite comes to hold a stale table nobody notices -- the same
    silent-staleness failure as F21/F25. Only a file written after this run began
    counts.
    """
    rel = PRODUCES.get(name)
    if rel is None:
        return False
    return (_results_root_for(horizon) / rel).is_file() and \
        (_results_root_for(horizon) / rel).stat().st_mtime >= started


def _run(name: str, script: Path, horizon: int, dry: bool,
         started: float | None = None) -> tuple[str, int, float]:
    env = dict(os.environ, SRQ1_HORIZON=str(horizon))
    label = f"H={horizon} {name}"
    if dry:
        print(f"  [dry] {label:<28} {script.name}")
        return (label, 0, 0.0)

    if started is not None and _done(name, horizon, started):
        print(f"\n  -- {label} already produced this run; skipping", flush=True)
        return (label, 0, 0.0)

    print(f"\n{'=' * 74}\n  {label}  --  {script.name}\n{'=' * 74}", flush=True)
    t0 = time.perf_counter()
    r = subprocess.run([PYTHON, str(script)], env=env, cwd=str(script.parent))
    dt = time.perf_counter() - t0
    print(f"  -> {label} exit={r.returncode} in {dt:,.1f}s", flush=True)
    if r.returncode != 0:
        # Say so at the point of failure, not only in the summary hours later.
        print(f"  !! {label} FAILED -- later stages that read its output will "
              f"degrade rather than crash. Check before trusting the results.",
              flush=True)
    return (label, r.returncode, dt)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--horizon", type=int, choices=(1, 3), default=None,
                    help="run one horizon only (default: both, H=3 first)")
    ap.add_argument("--only", default=None,
                    help="comma-separated stage names from the ordered list")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan without running anything")
    ap.add_argument("--resume", metavar="STAMP_FILE", nargs="?", const="auto",
                    help=("skip stages whose artefact was already written by this "
                          "run. Use after a kill: the suite is hours long and "
                          "competes for RAM, so a late kill would otherwise throw "
                          "away every completed Optuna study."))
    ap.add_argument("--tuning", choices=("cv", "fast"), default="cv",
                    help=("cv (default): run benchmark_cv -- 16 studies (4 "
                          "categories x 2 models x 2 objectives) x 100 trials x "
                          "4 folds, ~6,400 fits, the rigorous result that ships. "
                          "fast: drop benchmark_cv from the plan; train_persist "
                          "falls back to benchmark_tuned's single-split search "
                          "(30 trials, minutes not hours) -- an accepted, "
                          "documented fallback (P0044 F27), not a hack. Use "
                          "fast for a contended/smoke-test run, cv for the "
                          "result that ships."))
    a = ap.parse_args()

    stages = STAGES
    if a.only:
        want = [s.strip() for s in a.only.split(",") if s.strip()]
        known = {n for n, _ in STAGES}
        unknown = [w for w in want if w not in known]
        if unknown:
            # Hard failure, not a silent skip: a typo'd stage name would
            # otherwise look like a run that simply chose to do less.
            ap.error(f"unknown stage(s): {unknown}. Known: {sorted(known)}")
        stages = [(n, p) for n, p in STAGES if n in want]

    if a.tuning == "fast":
        dropped = [n for n, _ in stages if n == "benchmark_cv"]
        stages = [(n, p) for n, p in stages if n != "benchmark_cv"]
        if dropped:
            print("--tuning fast: dropping benchmark_cv from the plan -- "
                  "train_persist will fall back to benchmark_tuned's params "
                  "(single validation split, not 4-fold CV).", flush=True)

    horizons = (a.horizon,) if a.horizon else HORIZONS

    missing = [str(p) for _, p in stages if not p.is_file()]
    if missing:
        print("Cannot start -- script(s) not found:")
        for m in missing:
            print(f"  {m}")
        return 2

    print(f"Plan: {len(stages)} stage(s) x {len(horizons)} horizon(s) "
          f"= {len(stages) * len(horizons)} run(s)  (tuning={a.tuning})")
    print(f"Horizons: {list(horizons)}  (H=3 writes the primary tree; "
          f"H=1 writes h1/)")

    # The resume marker. Stages are "done" only if their artefact was written
    # after this timestamp, so a stale table from an earlier run never counts.
    stamp = HERE / ".run_both_horizons.stamp"
    if a.resume and stamp.is_file():
        started = stamp.stat().st_mtime
        print(f"Resuming: skipping stages already produced since "
              f"{time.strftime('%H:%M:%S', time.localtime(started))}")
    else:
        started = None
        if not a.dry_run:
            stamp.write_text(time.strftime("%Y-%m-%d %H:%M:%S"), encoding="utf-8")

    results = []
    for h in horizons:
        for name, script in stages:
            results.append(_run(name, script, h, a.dry_run, started))

    if a.dry_run:
        return 0

    failed = [r for r in results if r[1] != 0]
    print(f"\n{'=' * 74}\n  SUMMARY\n{'=' * 74}")
    for label, rc, dt in results:
        print(f"  {'ok  ' if rc == 0 else 'FAIL'}  {label:<30} {dt:>8,.1f}s")
    total = sum(r[2] for r in results)
    print(f"\n  {len(results) - len(failed)}/{len(results)} succeeded "
          f"in {total / 60:,.1f} min")
    if failed:
        # Non-zero exit so a caller (or a human scrolling past) cannot read a
        # partially failed suite as a completed one.
        print(f"\n  FAILED: {', '.join(r[0] for r in failed)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
