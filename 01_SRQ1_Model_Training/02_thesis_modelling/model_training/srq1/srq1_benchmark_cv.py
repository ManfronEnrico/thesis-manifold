#!/usr/bin/env python3
"""
SRQ1 — tuned benchmark with expanding-window CV, convergence evidence, and a
dual-objective check.

WHY THIS EXISTS. `srq1_benchmark_tuned.py` is methodologically correct but
under-powered, and an examiner asking "how many trials, and did you cross-validate?"
would get a weak answer. This addresses the three gaps (P0040 F58):

  1. SINGLE VALIDATION SPLIT -> expanding-window time-series CV.
  2. 30 TRIALS, UNJUSTIFIED    -> 100 trials, with the convergence curve SAVED so
                                  the budget is justified by evidence rather than
                                  by an appeal to convention.
  3. WMAPE-ONLY OBJECTIVE      -> tunes under both WMAPE and medMAPE, reporting
                                  whether the choice changes the selected model.

ACADEMIC BASIS (verify each before citing -- see P0040 F59)
-----------------------------------------------------------
* Expanding-window / rolling-origin evaluation for time series:
  Hyndman & Athanasopoulos, *Forecasting: Principles and Practice* 3rd ed., §5.10
  ("Time series cross-validation"); Tashman (2000), *International Journal of
  Forecasting* 16(4), on rolling-origin evaluation. K-fold CV is INVALID here --
  shuffling lets the model train on months after the ones it predicts.
* TPE sampler: Bergstra, Bardenet, Bengio & Kegl (2011), "Algorithms for
  Hyper-Parameter Optimization", NeurIPS.
* Sequential model-based search over random/grid: Bergstra & Bengio (2012),
  "Random Search for Hyper-Parameter Optimization", JMLR 13.
* Optuna / define-by-run + pruning: Akiba et al. (2019), KDD.

**There is no citable "correct" number of trials.** Any source claiming one is
being misread: the requirement depends on the search space. This script therefore
justifies its budget EMPIRICALLY -- `convergence.csv` records the running best
validation score per trial, so the write-up can state the trial at which the score
plateaued. That is a stronger argument than citing a convention.

Self-contained, seed=42. No API spend.
Usage:  .venv/Scripts/python.exe .../srq1_benchmark_cv.py [--trials 100] [--folds 4]
Output: 04_thesis_results/srq1/{cv_metrics.csv, cv_params.json, cv_convergence.csv,
        cv_summary.md}
"""

import argparse
import json
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import optuna
from joblib import Parallel, delayed

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, THESIS_DATA_ENGINEERED_BYMONTH_DIR

warnings.filterwarnings("ignore")
# The active horizon, and the paths that follow from it. ONE source, so the
# matrix read and the results written can never describe different horizons
# (P0049 F24). Set SRQ1_HORIZON=1 to run the secondary horizon.
from _horizon import HORIZON, matrix_path, results_root, banner  # noqa: E402,F401
from _features import FEATURES as _FEATURES, resolve as _resolve_feats, describe as _describe_feats  # noqa: E402,F401
optuna.logging.set_verbosity(optuna.logging.WARNING)

class _SRQ1Out:
    """Routes `OUT / "file.ext"` into figures/, tables/ or models/ by role.

    Added 2026-09-06 (P0046 Phase 3b). The results tier is the tree humans browse
    to pick thesis artefacts, so every SRQ folder has the same three-way shape.
    This preserves each existing call site while filing the output correctly, and
    it resolves READS too, so scripts reading a sibling's output keep working.

    Splitting by role rather than by extension keeps a `.csv` and its rendered
    `.md` twin together -- they are one artefact in two formats.
    """

    _MODELS = {"cv_params.json", "pooled_params.json", "tuned_params.json"}
    _FIGURES = {".png", ".svg", ".pdf"}

    def __init__(self, base):
        self._base = base

    def _sub(self, name):
        if name in self._MODELS:
            return self._base / "models"
        if Path(name).suffix.lower() in self._FIGURES:
            return self._base / "figures"
        return self._base / "tables"

    _PASSTHROUGH = {"figures", "tables", "models"}

    def __truediv__(self, name):
        # A bare subfolder name is already the destination -- pass it straight
        # through, or `RES / "figures"` would be filed as if it were a table.
        if str(name) in self._PASSTHROUGH:
            d = self._base / str(name)
            d.mkdir(parents=True, exist_ok=True)
            return d
        d = self._sub(str(name))
        d.mkdir(parents=True, exist_ok=True)
        return d / str(name)

    def __getattr__(self, attr):
        return getattr(self._base, attr)

    def __fspath__(self):
        return str(self._base)

    def __str__(self):
        return str(self._base)


OUT = _SRQ1Out(results_root())
SEED = 42

# ---------------------------------------------------------------------------
# XGB_N_JOBS: reproducibility, not performance. READ BEFORE CHANGING.
#
# XGBoost's histogram builder sums gradient statistics per thread and reduces
# them in completion order. Floating-point addition is not associative, so a
# different THREAD COUNT gives a different sum, a different split, and a
# different tree -- with the seed, the data and every hyperparameter identical.
# `random_state` fixes the subsample/colsample draw; it does NOT fix the order
# of a parallel reduction.
#
# Measured on danskvand brand-month, seed 42, all else held constant
# (2026-09-06):
#     n_jobs=1  -> WMAPE 34.648708   (repeatable across runs)
#     n_jobs=2  -> WMAPE 34.946778
#     n_jobs=4  -> WMAPE 35.397904
#     n_jobs=8  -> WMAPE 37.297544   (== n_jobs=-1 on this 8-core machine)
#
# A 2.65pp spread from thread count alone. That is larger than most of the
# holiday-enrichment effects reported in appendix table 94, so with n_jobs=-1
# a reader on a different machine could not reproduce the sign of a finding.
# This is what caused the XGBoost-only drift when srq1_benchmark.py was re-run
# on 2026-09-06 against matrices whose new holiday columns no models read
# (P0047 F18).
#
# Fixed to 1 for every ACCURACY number. The cost is wall-clock on a
# single fit, which is seconds here and is not a reported quantity.
#
# DELIBERATELY NOT APPLIED to srq1_profiling.py: that script measures memory
# and latency under realistic multi-core execution, where n_jobs=-1 is the
# thing being measured. It records the core count with its results and says so
# in its output table.
# ---------------------------------------------------------------------------
XGB_N_JOBS = 1
# Directory names are CAPITALISED on disk (Danskvand/, Energidrikke/). On Linux
# the lowercase keys silently matched nothing and two of four categories were
# dropped from every run -- fixed on the HPC, 2026-09-09.
CATS = {"CSD": "csd", "Danskvand": "danskvand",
        "Energidrikke": "energidrikke", "RTD": "rtd"}
# The modelling feature set, defined once in srq1/_features.py. Eleven copies of
# this literal existed and had already drifted -- srq1_pooled.py was missing
# promo_intensity, silently confounding the pooled-vs-per-category comparison
# (P0049 F31). Holiday and intermittency columns are conditional; resolve()
# intersects against the matrix, so a category lacking one simply omits it.
FEATURES = list(_FEATURES)


def _wmape(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    return float(np.abs(y - yhat).sum() / max(y.sum(), 1e-9) * 100)


def _medmape(y, yhat):
    """Median absolute percentage error, computed only where the actual is > 0.

    APE is UNDEFINED against a zero actual, not merely large. Dropping those cells
    is the honest treatment; substituting a large constant would silently penalise
    whichever model happens to be evaluated on sparser series."""
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    m = y > 0
    if not m.any():
        return float("nan")
    return float(np.median(np.abs(y[m] - yhat[m]) / y[m]) * 100)


def mase_denominator(train_df, series_col="brand", y_col="log_sales_units"):
    """Per-series in-sample MAE of the one-step naive forecast (Hyndman & Koehler
    2006, pp. 684-685). This is MASE's scaling factor.

    Computed on RAW units, not the logged target, because MASE is meant to be
    interpreted against the naive model's error in the quantity being forecast.

    Returns {series_key: denominator}. Series whose naive MAE is zero (a perfectly
    flat history) are omitted rather than assigned inf -- MASE is genuinely
    undefined there, and a flat series is not a meaningful benchmark to beat.
    """
    out = {}
    for k, g in train_df.groupby(series_col):
        y = np.expm1(np.asarray(g.sort_values("ym")[y_col], float)) if "ym" in g             else np.expm1(np.asarray(g[y_col], float))
        if len(y) < 2:
            continue
        d = float(np.mean(np.abs(np.diff(y))))
        if d > 0:
            out[k] = d
    return out


def _mase(y, yhat, keys, denom):
    """Mean absolute scaled error.

    WHY THIS METRIC EXISTS HERE. Hyndman & Koehler (2006) propose MASE precisely
    for the situation this dataset is in: comparing accuracy across series of very
    different scales, some of which contain zero actuals. Unlike MAPE it is
    **defined at zero**, so it admits the ~27% of brands that percentage errors
    must exclude -- and Hyndman & Koehler (p. 683) explicitly criticise excluding
    them as "an artificial solution that is impossible to apply in practical
    situations".

    READING IT. MASE < 1 means the model beats a naive one-step forecast on that
    series' own history; MASE > 1 means it does not. That makes it the only metric
    here with an absolute, interpretable threshold rather than a relative one.
    """
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    num, ok = np.abs(y - yhat), np.array([k in denom for k in keys])
    if not ok.any():
        return float("nan")
    d = np.array([denom.get(k, np.nan) for k in keys], float)
    return float(np.mean(num[ok] / d[ok]))


METRICS = {"wmape": _wmape, "medmape": _medmape}


def _load(cat, slug):
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(matrix_path(cat, slug))
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    feats = [c for c in FEATURES if c in fm.columns]
    return d, feats


def _make(model, params):
    if model == "LightGBM":
        from lightgbm import LGBMRegressor
        return LGBMRegressor(random_state=SEED, verbose=-1, **params)
    from xgboost import XGBRegressor
    return XGBRegressor(random_state=SEED, verbosity=0, n_jobs=XGB_N_JOBS, **params)


def _space(trial, model):
    if model == "LightGBM":
        return dict(
            n_estimators=trial.suggest_int("n_estimators", 200, 1200),
            learning_rate=trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
            num_leaves=trial.suggest_int("num_leaves", 15, 128),
            min_child_samples=trial.suggest_int("min_child_samples", 5, 60),
            subsample=trial.suggest_float("subsample", 0.6, 1.0),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
        )
    return dict(
        n_estimators=trial.suggest_int("n_estimators", 200, 1200),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
        max_depth=trial.suggest_int("max_depth", 3, 10),
        min_child_weight=trial.suggest_float("min_child_weight", 1.0, 8.0),
        subsample=trial.suggest_float("subsample", 0.6, 1.0),
        colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
    )


def _folds(d, k):
    """Expanding-window folds over the ORDERED period index (train+val only).

    Each fold trains on everything up to a cut-off and validates on the block
    immediately after it, so the training window grows and the model is never fitted
    on a month later than the one it predicts. This is rolling-origin evaluation
    (Tashman 2000; Hyndman & Athanasopoulos §5.10).

    K-fold CV would be INVALID here: shuffling rows lets a model train on 2026-06
    and predict 2026-03, which is not a forecast. The test split is untouched
    throughout -- CV happens strictly inside train+val.

    Splits on distinct PERIODS, not rows: rows are brand-months, so a row-wise split
    would put the same month in both train and validation for different brands."""
    dev = d[d.split.isin(["train", "val"])].copy()
    periods = np.sort(dev.period_index.unique())
    if len(periods) < (k + 2):
        k = max(1, len(periods) // 3)
    # Reserve the last k blocks as successive validation windows.
    edges = np.array_split(periods[len(periods) // 3:], k)
    out = []
    for e in edges:
        if len(e) == 0:
            continue
        cut = e[0]
        tr = dev[dev.period_index < cut]
        va = dev[dev.period_index.isin(e)]
        if len(tr) >= 30 and len(va) > 0:
            out.append((tr, va))
    return out


def _fit_fold(model, params, tr, va, feats, fn):
    """One fold's fit+score. Factored out so it can run under Parallel --
    the RETURN VALUE is identical to inlining this in a for-loop; only the
    wall-clock changes."""
    m = _make(model, params)
    m.fit(tr[feats].fillna(0.0), tr["log_sales_units"].values)
    pred = np.expm1(m.predict(va[feats].fillna(0.0)))
    s = fn(np.expm1(va["log_sales_units"].values), pred)
    return s if np.isfinite(s) else None


# Fold-level parallelism, XGBoost only. Read before touching.
#
# XGBoost is already hardcoded to n_jobs=XGB_N_JOBS=1 (determinism -- see the
# note by that constant). That pinning is what makes fitting its 4 folds
# under a thread pool SAFE: each thread's fit uses exactly one core, so 4
# threads = 4 cores, no nested oversubscription, and -- because each fold's
# fit is independent of the others and Parallel returns results IN INPUT
# ORDER regardless of completion order -- the returned `scores` list, and
# therefore its mean, is IDENTICAL to the sequential version. This changes
# wall-clock only, never a number.
#
# LightGBM is deliberately EXCLUDED. Its n_jobs is unset (library default,
# multi-threaded per fit), so wrapping ITS folds in an outer thread pool
# would nest thread pools inside thread pools -- real oversubscription risk,
# and LightGBM's own thread-count sensitivity has never been measured the
# way XGBoost's was (see XGB_N_JOBS's docstring table). Pin and measure that
# first; don't fold it into this change.
FOLD_N_JOBS = 4


def tune(model, d, feats, trials, metric_name, folds):
    """Tune by mean CV score across expanding-window folds.

    Records the running best per trial so budget adequacy can be SHOWN."""
    fn = METRICS[metric_name]
    curve = []
    parallel_folds = (model == "XGBoost")

    # Opened ONCE per study, reused across all `trials` calls to objective().
    # A fresh Parallel(...) per trial (the first version of this change) was
    # measured SLOWER than the plain sequential loop -- 2m16s vs 2m5s for 10
    # trials on identical data -- because thread-pool spin-up cost more than
    # the 4 small fold-fits saved. Reusing one pool for the whole study (100
    # trials in production) amortises that cost instead of paying it per
    # trial. `parallel` is None when this study is LightGBM, so `objective`
    # falls through to the sequential branch unconditionally.
    parallel = (Parallel(n_jobs=FOLD_N_JOBS, backend="threading")
                if parallel_folds else None)

    def objective(trial):
        params = _space(trial, model)
        if parallel is not None:
            results = parallel(
                delayed(_fit_fold)(model, params, tr, va, feats, fn)
                for tr, va in folds)
        else:
            results = [_fit_fold(model, params, tr, va, feats, fn)
                       for tr, va in folds]
        scores = [s for s in results if s is not None]
        if not scores:
            return float("inf")
        # MEAN across folds, not best: the best fold would select a configuration
        # that happens to suit one window, which is the overfitting CV exists to
        # prevent.
        return float(np.mean(scores))

    study = optuna.create_study(direction="minimize",
                                sampler=optuna.samplers.TPESampler(seed=SEED))

    def _cb(st, tr):
        curve.append({"trial": tr.number,
                      "value": tr.value if tr.value is not None else float("nan"),
                      "best": st.best_value})
    study.optimize(objective, n_trials=trials, callbacks=[_cb],
                   show_progress_bar=False)

    # Refit the winner on ALL of train+val, evaluate ONCE on the untouched test.
    dev = d[d.split.isin(["train", "val"])]
    te = d[d.split == "test"]
    m = _make(model, study.best_params)
    m.fit(dev[feats].fillna(0.0), dev["log_sales_units"].values)
    pred = np.expm1(m.predict(te[feats].fillna(0.0)))
    yte = np.expm1(te["log_sales_units"].values)
    return (dict(cv_score=study.best_value,
                 test_wmape=_wmape(yte, pred),
                 test_medmape=_medmape(yte, pred),
                 n_test=len(te)),
            study.best_params, curve)


def _plateau(curve, tol_pp=0.5):
    """First trial whose best score is within `tol_pp` PERCENTAGE POINTS of final.

    The empirical justification for the trial budget, replacing a citation to a
    convention that does not exist (P0040 F59).

    IMPORTANT -- an earlier version used a 0.1% RELATIVE tolerance and was
    misleading. On a score of ~17, 0.1% relative is 0.017pp, so a study still
    drifting by 0.2pp registered as "not converged" and the plateau trial came out
    at 99 for six of eight studies. That reading suggested 100 trials was
    insufficient. Measuring the actual gains showed the opposite: the last 25
    trials contributed 0-7% of total improvement, and 0.00pp in three studies.

    An absolute tolerance in the metric's own units is the meaningful test, because
    the question is "would more trials change the reported result?" -- and a 0.2pp
    move in WMAPE would not. `_gain_tail` reports the complementary evidence."""
    if not curve:
        return None
    final = curve[-1]["best"]
    for c in curve:
        if abs(c["best"] - final) <= tol_pp:
            return c["trial"]
    return curve[-1]["trial"]


def _gain_tail(curve, n=25):
    """Share of total improvement occurring in the last `n` trials.

    The honest budget-adequacy statistic: near zero means the search had stopped
    finding anything and additional trials would not change the result."""
    if len(curve) <= n:
        return None
    b = [c["best"] for c in curve]
    total = b[0] - b[-1]
    if total <= 1e-9:
        return 0.0
    return round(100.0 * (b[-n] - b[-1]) / total, 1)


def _write_outputs(rows, params, curves, cats, n_folds, trials):
    """The aggregation + markdown-writing tail. ONE implementation, called by
    both the sequential default path and --merge-partials, so the two paths
    cannot drift into writing outputs differently."""
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "cv_metrics.csv", index=False)
    pd.DataFrame(curves).to_csv(OUT / "cv_convergence.csv", index=False)
    (OUT / "cv_params.json").write_text(json.dumps(params, indent=2),
                                        encoding="utf-8", newline="\n")

    lines = ["# SRQ1 — CV-tuned benchmark", "",
             f"Expanding-window time-series CV ({n_folds} folds), {trials} Optuna",
             "TPE trials per configuration, seed 42. Each configuration is tuned",
             "twice — once for WMAPE, once for median MAPE — to show whether the",
             "objective changes which model is selected.", "",
             "`plateau_trial` = the trial after which the best CV score improved by",
             "<0.1% relative. This is the empirical justification for the trial",
             "budget; there is no citable convention for a trial count.", "",
             "| Category | Model | Tuned for | test WMAPE | test medMAPE | CV score | plateau |",
             "|---|---|---|---|---|---|---|"]
    for _, r in df.iterrows():
        lines.append(f"| {r['category']} | {r['model']} | {r['tuned_for']} | "
                     f"{r['test_wmape']:.1f}% | {r['test_medmape']:.1f}% | "
                     f"{r['cv_score']:.1f} | {r['plateau_trial']} |")
    lines += ["", "## Does the objective change the answer?", "",
              "| Category | Model | WMAPE when tuned for WMAPE | ... for medMAPE | delta |",
              "|---|---|---|---|---|"]
    for cat in cats:
        for model in ("LightGBM", "XGBoost"):
            sel = df[(df.category == cat) & (df.model == model)]
            if len(sel) != 2:
                continue
            w = sel[sel.tuned_for == "wmape"].iloc[0]
            m = sel[sel.tuned_for == "medmape"].iloc[0]
            lines.append(f"| {cat} | {model} | {w['test_wmape']:.1f}% | "
                         f"{m['test_wmape']:.1f}% | "
                         f"{m['test_wmape'] - w['test_wmape']:+.1f}pp |")
    lines.append("")
    (OUT / "cv_summary.md").write_text("\n".join(lines) + "\n",
                                       encoding="utf-8", newline="\n")
    print(f"\nSaved cv_metrics.csv + cv_convergence.csv + cv_params.json + "
          f"cv_summary.md in {OUT}")


# --study support: one (category, model, metric) study per process. Exists so
# --parallel can run several studies concurrently as separate OS processes
# instead of one Python process working through all 16 sequentially.
#
# Each partial file is named uniquely by its (cat, model, metric) triple, so
# 16 concurrent writers can never collide on the same path -- this is the
# fix for the failure mode P0053 already hit once: srq1_benchmark_cv.py's
# --categories flag lets you run a SUBSET, but every invocation overwrites
# the SAME cv_metrics.csv/cv_params.json, so two categories run "in parallel"
# by hand would race and the loser's results would vanish silently. Distinct
# per-study files + an explicit --merge-partials step is what makes 16-way
# concurrency safe: nothing is ever a shared mutable target until the merge,
# and the merge reads back exactly 16 files it can count.
PARTIAL_DIR = Path(OUT) / "partial"


def _partial_path(cat, model, metric):
    return PARTIAL_DIR / f"{cat}__{model}__{metric}.json"


def _run_one_study(cat, slug, model, metric, trials, n_folds):
    d, feats = _load(cat, slug)
    folds = _folds(d, n_folds)
    print(f"\n########## {cat}/{model}/{metric} -- {len(folds)} expanding "
          f"folds, {len(feats)} features, {trials} trials ##########",
          flush=True)
    res, best, curve = tune(model, d, feats, trials, metric, folds)
    pl = _plateau(curve)
    gt = _gain_tail(curve)
    row = dict(category=cat, model=model, tuned_for=metric,
              plateau_trial=pl, gain_in_last_25_pct=gt, **res)
    curve_rows = [{"category": cat, "model": model, "tuned_for": metric, **c}
                 for c in curve]
    print(f"  {model:9s} tuned_for={metric:8s} "
          f"test WMAPE={res['test_wmape']:5.1f}% "
          f"medMAPE={res['test_medmape']:5.1f}%  "
          f"(cv={res['cv_score']:5.1f}, plateau@{pl}, last25={gt}%)",
          flush=True)
    return row, best, curve_rows


def _merge_partials(cats, trials, n_folds):
    """Read every partial/{cat}__{model}__{metric}.json and write the same
    final files the sequential path would have. Fails loudly (not silently)
    if any expected study is missing -- a partial merge that looks complete
    is worse than a merge that refuses to run."""
    expected = [(c, m, met) for c in cats
               for m in ("LightGBM", "XGBoost") for met in ("wmape", "medmape")]
    missing = [f"{c}/{m}/{met}" for c, m, met in expected
              if not _partial_path(c, m, met).is_file()]
    if missing:
        raise SystemExit(f"--merge-partials: missing {len(missing)} of "
                         f"{len(expected)} studies: {missing}")

    rows, params, curves = [], {}, []
    for cat, model, metric in expected:
        d = json.loads(_partial_path(cat, model, metric).read_text(encoding="utf-8"))
        rows.append(d["row"])
        params[f"{cat}/{model}/{metric}"] = d["best_params"]
        curves.extend(d["curve"])
    _write_outputs(rows, params, curves, cats, n_folds, trials)


def _parallel_orchestrate(cats, trials, n_folds):
    """Run all (category, model, metric) studies as subprocesses of THIS
    script, then merge. XGBoost studies run up to 8-way concurrent -- safe
    because XGB_N_JOBS=1 is already pinned, so N processes = N cores, no
    nested oversubscription. LightGBM studies run ONE AT A TIME, exactly the
    existing sequential behaviour: its n_jobs is unset (library default,
    multi-threaded per fit), and pinning/measuring that is a separate,
    not-yet-made decision -- see FOLD_N_JOBS's docstring. Don't parallelize
    what hasn't been measured."""
    PARTIAL_DIR.mkdir(parents=True, exist_ok=True)
    xgb = [(c, "XGBoost", met) for c in cats for met in ("wmape", "medmape")]
    lgb = [(c, "LightGBM", met) for c in cats for met in ("wmape", "medmape")]

    def _cmd(cat, model, metric):
        return [sys.executable, str(_here), "--study", f"{cat}/{model}/{metric}",
               "--trials", str(trials), "--folds", str(n_folds)]

    print(f"--parallel: {len(xgb)} XGBoost studies concurrent, "
          f"{len(lgb)} LightGBM studies sequential", flush=True)
    procs = {(c, m, met): subprocess.Popen(_cmd(c, m, met))
            for c, m, met in xgb}
    failed = []
    for key, p in procs.items():
        if p.wait() != 0:
            failed.append(key)
    for c, m, met in lgb:
        if subprocess.run(_cmd(c, m, met)).returncode != 0:
            failed.append((c, m, met))
    if failed:
        raise SystemExit(f"--parallel: {len(failed)} stud(y/ies) failed: "
                         f"{failed}")
    _merge_partials(list(cats), trials, n_folds)


def main():
    global FOLD_N_JOBS
    ap = argparse.ArgumentParser(description="SRQ1 CV-tuned benchmark")
    ap.add_argument("--trials", type=int, default=100)
    ap.add_argument("--folds", type=int, default=4)
    ap.add_argument("--categories", nargs="+", default=None)
    ap.add_argument("--study", default=None, metavar="CAT/MODEL/METRIC",
                    help="run exactly one study, write partial/<...>.json, "
                         "exit. Used by --parallel; not for direct use.")
    ap.add_argument("--parallel", action="store_true",
                    help="run all studies as concurrent subprocesses of this "
                         "script, then merge (see _parallel_orchestrate).")
    ap.add_argument("--merge-partials", action="store_true",
                    help="skip computation; aggregate partial/*.json written "
                         "by earlier --study runs into the final outputs.")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    cats = {c: CATS[c] for c in (a.categories or CATS)}

    if a.study:
        cat, model, metric = a.study.split("/")
        # This process supplies its own core via --parallel's concurrency,
        # not via threading a single study's folds -- stacking both would
        # oversubscribe. See FOLD_N_JOBS's docstring for the measured
        # per-trial-pool-creation cost this avoids.
        FOLD_N_JOBS = 1
        slug = CATS[cat]
        row, best, curve_rows = _run_one_study(cat, slug, model, metric,
                                               a.trials, a.folds)
        PARTIAL_DIR.mkdir(parents=True, exist_ok=True)
        _partial_path(cat, model, metric).write_text(
            json.dumps({"row": row, "best_params": best, "curve": curve_rows}),
            encoding="utf-8", newline="\n")
        return

    if a.merge_partials:
        _merge_partials(list(cats), a.trials, a.folds)
        return

    if a.parallel:
        _parallel_orchestrate(list(cats), a.trials, a.folds)
        return

    rows, params, curves = [], {}, []

    for cat, slug in cats.items():
        d, feats = _load(cat, slug)
        folds = _folds(d, a.folds)
        print(f"\n########## {cat} -- {len(folds)} expanding folds, "
              f"{len(feats)} features, {a.trials} trials ##########")
        for i, (tr, va) in enumerate(folds, 1):
            print(f"   fold {i}: train={len(tr):5d} rows  val={len(va):4d} rows")

        for model in ("LightGBM", "XGBoost"):
            for metric in ("wmape", "medmape"):
                res, best, curve = tune(model, d, feats, a.trials, metric, folds)
                pl = _plateau(curve)
                gt = _gain_tail(curve)
                rows.append(dict(category=cat, model=model, tuned_for=metric,
                                 plateau_trial=pl, gain_in_last_25_pct=gt, **res))
                params[f"{cat}/{model}/{metric}"] = best
                for c in curve:
                    curves.append({"category": cat, "model": model,
                                   "tuned_for": metric, **c})
                print(f"  {model:9s} tuned_for={metric:8s} "
                      f"test WMAPE={res['test_wmape']:5.1f}% "
                      f"medMAPE={res['test_medmape']:5.1f}%  "
                      f"(cv={res['cv_score']:5.1f}, plateau@{pl}, "
                      f"last25={gt}%)")

    _write_outputs(rows, params, curves, cats, a.folds, a.trials)


if __name__ == "__main__":
    main()
