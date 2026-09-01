#!/usr/bin/env python3
"""
SRQ1 operational profiling — peak RAM + train/predict latency per model.

Measures PROCESS RSS, not tracemalloc, and does so in a fresh subprocess per
model. Both choices are load-bearing:

* tracemalloc sees only Python-level allocations. LightGBM and XGBoost build
  their trees in C++, so their real footprint is invisible to it. The previous
  version of this script reported XGBoost at 0.1 MB peak -- less than Ridge,
  and impossible for a 926-tree depth-7 ensemble. That number was not small;
  it was unmeasured. RSS is what the OS actually charges the process, which is
  what an 8 GB budget is denominated in.
* one subprocess per model, because RSS never returns to baseline in-process:
  allocators retain freed pages, so a sequential in-process loop attributes
  earlier models' retained memory to later ones. A fresh interpreter gives each
  model a clean baseline.

tracemalloc is still reported, as a second column. The gap between the two IS
the native allocation the old table was blind to, and Ch6 should show it rather
than quietly replace one number with another.

Threads matter for the same reason: XGBoost runs n_jobs=-1, so per-thread
native buffers scale with core count. The core count is recorded with the
results or the numbers are not reproducible on another machine.

Supports the thesis's ≤8 GB operational constraint claim (Ch6 §6.4) and SRQ4.
Measures, per model, tracemalloc peak memory and wall-clock for fit and predict
on a representative dataset (CSD brand×month). Tabular models
use the tuned configs; ARIMA is profiled on a single representative brand series.

Self-contained, reproducible (seed=42). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_profiling.py
Output: 04_thesis_results/srq1/{profiling.csv, profiling.md}
"""
import json, os, subprocess, sys, threading, time, tracemalloc, warnings, gc
from pathlib import Path

import psutil
import numpy as np
import pandas as pd

# Repo root located by searching upward for PATHS.py rather than by a fixed
# parents[N] index: the index silently breaks whenever a script moves a
# directory deeper, which is exactly what happened in the 2026-08-19
# reorganisation (ModuleNotFoundError: No module named 'PATHS').
_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir

warnings.filterwarnings("ignore")
RES = THESIS_RESULTS_SRQ1_DIR
SEED = 42
MODELS = ["Ridge", "LightGBM", "XGBoost", "ARIMA(per-series)"]
# weighted_distribution / weighted_dist is deliberately ABSENT (P0036 task 7,
# 2026-08-19).
#
# Note these scripts previously named "weighted_distribution", a column that does
# not exist in the matrix (it is "weighted_dist" after step 1's RENAMES). They
# were therefore already training without it -- silently, since
# available_features() drops unknown names. This makes that state deliberate and
# documented rather than accidental.
#
# It was tested for leakage and CLEARED: never lagged, but structural and nearly
# static -- corr(wd[t], wd[t-1]) = 0.976, corr(wd[t], wd[t+3]) = 0.946, median
# month-on-month change 0.00114 on a 0-1 scale.
#
# It is absent because it does not improve out-of-sample accuracy. LightGBM, 300
# trees, seeds 42/7/2024 (identical -- deterministic):
#
#     category        without    with     lagged
#     CSD              17.20%   18.24%   18.32%
#     Danskvand        33.39%   34.36%   32.89%
#     Energidrikke     17.40%   16.94%   16.86%
#     RTD              31.83%   32.54%   31.26%
#
# Worse in 3 of 4. The column REMAINS in the feature matrix for EDA; this removes
# it only from model inputs. If reintroduced, use the LAGGED form.
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "peak_month", "promo_intensity"]

def available_features(fm, wanted=None):
	"""Return the wanted features that this matrix actually contains.

	DEC-DISCOVER-COLUMNS: categories differ in capability, not just in values.
	Danskvand and RTD carry no `promo_units` (Nielsen does not report promotion
	for them), so the pipeline omits `promo_intensity` for those categories
	rather than zero-filling -- a constant-zero column would assert "no
	promotion ran", which the data does not support.

	Indexing by a fixed list therefore raises KeyError on exactly the categories
	whose capability differs. Selecting by intersection trains each category on
	what it has, and picks up new columns without a code change.

	The order of `wanted` is preserved so feature-importance output stays
	comparable across runs.
	"""
	wanted = FEATURES if wanted is None else wanted
	return [c for c in wanted if c in fm.columns]



def _profile(fn):
    """Time `fn`, reporting BOTH peak RSS delta and tracemalloc peak, in MB.

    RSS is sampled by a poller thread rather than read once at the end: peak
    memory during a fit is transient (XGBoost frees its histogram buffers before
    returning), so a single post-hoc reading measures what survived, not what
    was needed. The budget question is about the high-water mark.

    The 5 ms interval is a deliberate trade: fine enough to catch a sub-second
    Ridge fit, coarse enough that the poller itself is not a measurable load.
    """
    proc = psutil.Process()
    gc.collect()
    base_rss = proc.memory_info().rss
    peak_rss = base_rss
    stop = threading.Event()

    def _poll():
        nonlocal peak_rss
        while not stop.is_set():
            try:
                r = proc.memory_info().rss
            except psutil.Error:
                return
            if r > peak_rss:
                peak_rss = r
            stop.wait(0.005)

    t = threading.Thread(target=_poll, daemon=True)
    tracemalloc.start()
    t.start()
    t0 = time.perf_counter()
    out = fn()
    dt = time.perf_counter() - t0
    stop.set(); t.join(timeout=1.0)
    _, tm_peak = tracemalloc.get_traced_memory(); tracemalloc.stop()

    # One last reading: a fit that peaks after the final poll tick would
    # otherwise be undercounted.
    peak_rss = max(peak_rss, proc.memory_info().rss)
    return out, dt, (peak_rss - base_rss) / 1e6, tm_peak / 1e6


def _run_isolated(model_name):
    """Re-invoke this script in a fresh interpreter to profile ONE model.

    Isolation is not fastidiousness. RSS never falls back to its baseline within
    a process -- CPython's allocator and the native libraries both retain freed
    pages for reuse -- so a sequential in-process loop charges each model with
    whatever its predecessors left resident. Ridge would look enormous simply
    for running after XGBoost. A fresh interpreter is the only way each model
    gets a baseline it owns.

    Returns the row dict parsed from the child's JSON line, or None on failure.
    """
    env = dict(os.environ, SRQ1_PROFILE_ONE=model_name)
    proc = subprocess.run([sys.executable, str(Path(__file__).resolve())],
                          capture_output=True, text=True, env=env)
    for line in proc.stdout.splitlines():
        if line.startswith("__ROW__"):
            return json.loads(line[len("__ROW__"):])
    print(f"  !! {model_name}: no row returned")
    if proc.stderr.strip():
        # Surface the child's traceback; a silent NaN row would otherwise be
        # reported as a measurement.
        print("     " + proc.stderr.strip().splitlines()[-1])
    return None


def main():
    # Parent mode: fan out one subprocess per model, collect their rows, and
    # write the report. Child mode (SRQ1_PROFILE_ONE set): profile that one
    # model, print its row as JSON, exit.
    only = os.environ.get("SRQ1_PROFILE_ONE")
    if not only:
        print(f"Profiling in isolated subprocesses ({os.cpu_count()} logical cores)...")
        rows = [r for r in (_run_isolated(m) for m in MODELS) if r]
        if not rows:
            raise RuntimeError("every subprocess failed -- no measurements to report")
        return _write_report(pd.DataFrame(rows))

    # P0035: was get_category_engineered_bychain_dir; the chain grain and its data
    # directory are gone (DEC-GRAIN 2026-07-12). Profiling now runs on brand x month.
    fm = pd.read_parquet(get_category_engineered_bymonth_dir("CSD") / "csd_feature_matrix_h3.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    trval = d[d.split.isin(["train", "val"])]
    te = d[d.split == "test"]
    Xtr, ytr = trval[available_features(fm)].fillna(0.0), trval["log_sales_units"].values
    Xte = te[available_features(fm)].fillna(0.0)
    params = json.loads((RES / "tuned_params.json").read_text())

    rows = []

    def add(name, builder):
        m, fit_t, fit_mb, fit_tm = _profile(lambda: builder().fit(Xtr, ytr))
        _, pred_t, pred_mb, pred_tm = _profile(lambda: m.predict(Xte))
        # Serialised size is a third, independent witness: it is measured by the
        # filesystem rather than by either profiler, so it cannot share their
        # blind spots. A model that pickles to 40 MB did not train in 0.1 MB.
        try:
            import pickle
            size_mb = len(pickle.dumps(m)) / 1e6
        except Exception:
            size_mb = float("nan")
        row = dict(model=name, fit_s=round(fit_t, 3), predict_ms=round(pred_t * 1000, 1),
                   peak_fit_RSS_MB=round(fit_mb, 1), peak_predict_RSS_MB=round(pred_mb, 2),
                   peak_fit_tracemalloc_MB=round(fit_tm, 1),
                   model_size_MB=round(size_mb, 2),
                   n_train=len(trval), n_features=len(FEATURES))
        rows.append(row)
        print('__ROW__' + json.dumps(row))
        print(f"  {name:10s} fit={fit_t:6.3f}s predict={pred_t*1000:7.1f}ms "
              f"RSS={fit_mb:8.1f}MB tracemalloc={fit_tm:7.1f}MB size={size_mb:6.2f}MB")

    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    if only == "Ridge":
        add("Ridge", lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0)))

    from lightgbm import LGBMRegressor
    if only == "LightGBM":
        add("LightGBM", lambda: LGBMRegressor(random_state=SEED, verbose=-1,
                                              **params["brand/CSD/LightGBM"]))
    from xgboost import XGBRegressor
    if only == "XGBoost":
        add("XGBoost", lambda: XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1,
                                            **params["brand/CSD/XGBoost"]))

    # ARIMA on a single representative brand series (univariate; per-series cost)
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    one = d[d.brand == d.groupby("brand")["sales_units"].sum().idxmax()].sort_values("period_index")
    yfit = np.log(np.maximum(one[one.split.isin(["train", "val"])].sales_units.values, 1.0))
    h = int((one.split == "test").sum())

    def fit_arima():
        return SARIMAX(yfit, order=(1, 1, 1), enforce_stationarity=False,
                       enforce_invertibility=False).fit(disp=False)
    if only != "ARIMA(per-series)":
        return
    r, fit_t, fit_mb, fit_tm = _profile(fit_arima)
    _, pred_t, pred_mb, pred_tm = _profile(lambda: r.forecast(h))
    row = dict(model="ARIMA(per-series)", fit_s=round(fit_t, 3), predict_ms=round(pred_t * 1000, 1),
               peak_fit_RSS_MB=round(fit_mb, 1), peak_predict_RSS_MB=round(pred_mb, 2),
               peak_fit_tracemalloc_MB=round(fit_tm, 1),
               model_size_MB=None,
               n_train=len(yfit), n_features=1)
    rows.append(row)
    print('__ROW__' + json.dumps(row))
    print(f"  {'ARIMA':10s} fit={fit_t:6.3f}s predict={pred_t*1000:7.1f}ms "
          f"RSS={fit_mb:8.1f}MB tracemalloc={fit_tm:7.1f}MB (1 series)")

    return


def _write_report(df):
    df.to_csv(RES / "profiling.csv", index=False)
    n_cores = os.cpu_count()
    total_gb = psutil.virtual_memory().total / 1e9
    # Grain label was "brand x chain" until 2026-09-01. That grain was deleted in
    # P0035 (DEC-GRAIN) and line ~92 has loaded bymonth ever since, so the
    # published table carried a stale label naming a grain that no longer exists.
    lines = ["# SRQ1 operational profiling (CSD brand×month; tuned configs)", "",
             "Peak **process RSS** and wall-clock per model, each measured in isolation. "
             "Supports the ≤8 GB sequential-execution constraint. ARIMA is per-series "
             "(univariate); tabular models train on the full matrix in one fit.", "",
             f"Environment: {n_cores} logical cores, {total_gb:.1f} GB system RAM, "
             f"XGBoost `n_jobs=-1`. Native buffers scale with core count, so these "
             f"figures are machine-dependent and the core count is part of the result.", "",
             "| Model | fit (s) | predict (ms) | peak RSS fit (MB) | peak RSS predict (MB) | tracemalloc fit (MB) | model size (MB) | n_train | n_features |",
             "|---|---|---|---|---|---|---|---|---|"]
    for _, x in df.iterrows():
        lines.append(f"| {x['model']} | {x['fit_s']} | {x['predict_ms']} | {x['peak_fit_RSS_MB']} | "
                     f"{x['peak_predict_RSS_MB']} | {x['peak_fit_tracemalloc_MB']} | "
                     f"{x['model_size_MB']} | {int(x['n_train'])} | {int(x['n_features'])} |")
    lines += ["",
              "**Reading the two memory columns.** RSS is what the operating system charges "
              "the process and is the figure the 8 GB budget is denominated in. tracemalloc "
              "counts Python-object allocations only. The gap between them is native "
              "(C/C++) allocation: LightGBM and XGBoost build their ensembles outside the "
              "Python heap, so tracemalloc is structurally blind to the dominant term for "
              "exactly the two models that allocate most. An earlier version of this table "
              "reported tracemalloc alone and put XGBoost at 0.1 MB -- below Ridge, and "
              "impossible for a 926-tree depth-7 ensemble. That figure was not small, it was "
              "unmeasured. Both columns are kept so the correction is auditable rather than "
              "silent.",
              "",
              "Model size on disk is a third, independent witness, measured by serialisation "
              "rather than by either profiler, and so shares neither one's blind spot."]
    (RES / "profiling.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("Saved profiling.csv + profiling.md")


if __name__ == "__main__":
    main()
