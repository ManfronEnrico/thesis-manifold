"""
Run the SRQ1 suite at both reported horizons.
=============================================

DEC-HORIZON (Brian, 2026-09-07) requires H=1 and H=3 both benchmarked. This runs
the suite twice, once per horizon, by setting SRQ1_HORIZON for each child
process. Every script then picks its own input matrix and output directory from
that one value (see srq1/_horizon.py), so:

  * H=3 writes to  05_thesis_results/srq1_model_performance/{tables,figures,models}/
  * H=1 writes to  05_thesis_results/srq1_model_performance/h1/{...}/

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

# name -> script path. Ordered by dependency; see the module docstring.
STAGES: list[tuple[str, Path]] = [
    ("benchmark",       SRQ1 / "srq1_benchmark.py"),
    ("benchmark_cv",    SRQ1 / "srq1_benchmark_cv.py"),
    ("benchmark_tuned", SRQ1 / "srq1_benchmark_tuned.py"),
    ("baselines_stat",  SRQ1 / "srq1_baselines_stat.py"),
    ("calibration",     SRQ1 / "srq1_calibration.py"),
    ("train_persist",   HERE / "train_and_persist.py"),
    ("shap_figures",    SRQ1 / "srq1_generate_shap_figures.py"),
    ("perf_figures",    SRQ1 / "srq1_generate_performance_figures.py"),
]

# Stages deliberately NOT in the default run, and why.
#
#   srq1_profiling.py  -- measures memory/latency at n_jobs=-1 (DEC-DETERMINISM).
#                         It is a resource measurement, not an accuracy result,
#                         and it is horizon-insensitive by design.
#   srq1_stability.py  -- 40 fits; run deliberately, not as part of a suite.
#   srq1_pooled.py     -- a separate modelling question (pooled vs per-category).
#   holiday_ablation*  -- answered already; rerun only if features change.
OPTIONAL = ("profiling", "stability", "pooled")

HORIZONS = (3, 1)  # primary first, so a run interrupted early still has H=3


def _run(name: str, script: Path, horizon: int, dry: bool) -> tuple[str, int, float]:
    env = dict(os.environ, SRQ1_HORIZON=str(horizon))
    label = f"H={horizon} {name}"
    if dry:
        print(f"  [dry] {label:<28} {script.name}")
        return (label, 0, 0.0)

    print(f"\n{'=' * 74}\n  {label}  --  {script.name}\n{'=' * 74}", flush=True)
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, str(script)], env=env, cwd=str(script.parent))
    dt = time.perf_counter() - t0
    print(f"  -> {label} exit={r.returncode} in {dt:,.1f}s", flush=True)
    return (label, r.returncode, dt)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--horizon", type=int, choices=(1, 3), default=None,
                    help="run one horizon only (default: both, H=3 first)")
    ap.add_argument("--only", default=None,
                    help="comma-separated stage names from the ordered list")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan without running anything")
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

    horizons = (a.horizon,) if a.horizon else HORIZONS

    missing = [str(p) for _, p in stages if not p.is_file()]
    if missing:
        print("Cannot start -- script(s) not found:")
        for m in missing:
            print(f"  {m}")
        return 2

    print(f"Plan: {len(stages)} stage(s) x {len(horizons)} horizon(s) "
          f"= {len(stages) * len(horizons)} run(s)")
    print(f"Horizons: {list(horizons)}  (H=3 writes the primary tree; "
          f"H=1 writes h1/)")

    results = []
    for h in horizons:
        for name, script in stages:
            results.append(_run(name, script, h, a.dry_run))

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
