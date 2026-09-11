#!/usr/bin/env python3
"""
SRQ1 prediction-interval calibration — split conformal (SRQ2 confidence signal).

For each category, the tuned point model THAT CATEGORY ACTUALLY SERVES is
wrapped in a split-conformal
interval: fit on train, calibrate the interval half-width on the validation
residuals (in log space) at a nominal level, then measure EMPIRICAL coverage on
test (fraction of actuals inside the interval). A well-calibrated interval has
empirical coverage ≈ nominal. Provides the raw confidence signal Ch6/SRQ2 needs.

Self-contained, reproducible (seed=42). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_calibration.py
Output: 04_thesis_results/srq1/{calibration.csv, calibration.md}
"""
import json, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

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
# The active horizon, and the paths that follow from it. ONE source, so the
# matrix read and the results written can never describe different horizons
# (P0049 F24). Set SRQ1_HORIZON=1 to run the secondary horizon.
from _horizon import HORIZON, matrix_path, results_root, banner  # noqa: E402,F401
from _features import FEATURES as _FEATURES, resolve as _resolve_feats, describe as _describe_feats  # noqa: E402,F401
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


RES = _SRQ1Out(results_root())
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
CATS = {"CSD": "csd", "Danskvand": "danskvand", "Energidrikke": "energidrikke", "RTD": "rtd"}
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
# The modelling feature set, defined once in srq1/_features.py. Eleven copies of
# this literal existed and had already drifted -- srq1_pooled.py was missing
# promo_intensity, silently confounding the pooled-vs-per-category comparison
# (P0049 F31). Holiday and intermittency columns are conditional; resolve()
# intersects against the matrix, so a category lacking one simply omits it.
FEATURES = list(_FEATURES)

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

NOMINAL = [0.80, 0.90]


def served_model(cat: str) -> str:
    """Which estimator THIS category actually serves.

    The interval must be calibrated on the residuals of the model that is
    served, not on a different one that happens to be the more common choice.
    `train_and_persist.best_model_for()` selects on the CROSS-VALIDATION score
    -- deliberately, because selecting on test is selection on the evaluation
    set -- and on that basis Energidrikke and RTD serve LightGBM while CSD and
    Danskvand serve XGBoost.

    Until 2026-09-11 this script fitted XGBRegressor unconditionally, so half
    the published calibration table described a model that is not served
    (P0053 F12, raised by Enrico). Read the fact rather than assume it: the
    persisted metadata records it, so a future change of selection propagates
    here without a code change.

    Falls back to XGBoost only when no metadata exists, which is the state
    before `train_and_persist.py` has ever run.
    """
    meta_path = RES / "models" / cat / "metadata.json"
    if not meta_path.is_file():
        print(f"  [warn] {cat}: no served metadata; defaulting to XGBoost")
        return "XGBoost"
    name = str(json.loads(meta_path.read_text()).get("model", ""))
    # The metadata string carries a suffix, e.g. "LightGBM(tuned)".
    return "LightGBM" if "lightgbm" in name.lower() else "XGBoost"


def make_estimator(cat: str, kind: str):
    """A fresh, unfitted estimator of the served kind, with that kind's params.

    n_jobs is pinned to 1 for BOTH families. The SRQ1 constraint exists because
    an unpinned thread count makes the timing figures unreproducible, and it
    would be no less true of LightGBM than of XGBoost.
    """
    tuned = params.get(f"brand/{cat}/{kind}", {})
    if kind == "LightGBM":
        return LGBMRegressor(random_state=SEED, n_jobs=1, verbose=-1, **tuned)
    return XGBRegressor(random_state=SEED, verbosity=0, n_jobs=XGB_N_JOBS, **tuned)


params = json.loads((RES / "tuned_params.json").read_text())
rows = []
for cat, slug in CATS.items():
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(matrix_path(cat, slug))
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr, va, te = (d[d.split == s] for s in ("train", "val", "test"))
    if len(tr) < 30 or len(va) == 0 or len(te) == 0:
        continue
    kind = served_model(cat)
    m = make_estimator(cat, kind)
    print(f"  {cat}: calibrating the served model -- {kind}")
    m.fit(tr[available_features(fm)].fillna(0.0), tr["log_sales_units"].values)
    # calibration residuals on validation (log space)
    res = np.abs(va["log_sales_units"].values - m.predict(va[available_features(fm)].fillna(0.0)))
    pred_te = m.predict(te[available_features(fm)].fillna(0.0))
    ytrue = np.expm1(te["log_sales_units"].values)
    for nom in NOMINAL:
        # FINITE-SAMPLE QUANTILE, not the nominal one. Lei et al. (2018) Algorithm 2
        # takes the ceil((n+1)(1-alpha))/n empirical quantile of the calibration
        # residuals, NOT the (1-alpha) quantile. The correction is what buys the
        # distribution-free guarantee P(Y in C) >= 1-alpha at FINITE n; using the
        # plain nominal quantile undercovers slightly and forfeits the theorem the
        # method is cited for. The gap is small here (+0.3 to +1.0pp of quantile
        # level at our calibration sizes) but it is the difference between "a
        # conformal-style interval" and "Lei et al. Algorithm 2".
        n_cal = len(res)
        level = min(np.ceil((n_cal + 1) * nom) / n_cal, 1.0)
        q = np.quantile(res, level)  # symmetric half-width in log space
        lo = np.expm1(pred_te - q); hi = np.expm1(pred_te + q)
        cov = float(np.mean((ytrue >= lo) & (ytrue <= hi)) * 100)
        # median relative interval width (robust; mean explodes on low-volume rows)
        width = float(np.median((hi - lo) / np.maximum(ytrue, 1e-9)))
        rows.append(dict(category=cat, nominal=int(nom * 100), empirical_coverage=round(cov, 1),
                         mean_rel_width=round(width, 2), n_test=len(te),
                         n_calib=n_cal, quantile_level=round(level, 4)))
        print(f"  {cat:13s} nominal={int(nom*100)}%  empirical={cov:5.1f}%  rel_width={width:.2f}")

df = pd.DataFrame(rows)
df.to_csv(RES / "calibration.csv", index=False)


def _cell(cat, nom, col):
    r = df[(df.category == cat) & (df.nominal == nom)]
    return None if r.empty else float(r.iloc[0][col])


# Values interpolated into the prose below, so a re-run cannot leave a stale
# figure in the caption (generated-artefact-provenance rule).
_dv80 = _cell("Danskvand", 80, "empirical_coverage")
# Which models were fitted, computed from the served metadata rather than
# asserted. The title said "tuned XGBoost" while two categories served
# LightGBM (P0053 F12).
_kinds = sorted({served_model(c) for c in CATS})
_served_desc = (f"tuned {_kinds[0]}" if len(_kinds) == 1
                else "tuned " + " / ".join(_kinds) + ", per served model")

_wide = {c: _cell(c, 90, "mean_rel_width") for c in ("Danskvand", "Energidrikke")
         if (_cell(c, 90, "empirical_coverage") or 100) < 88
         and _cell(c, 90, "mean_rel_width") is not None}
_dv_line = (
    f"The danskvand row ({_dv80:.1f}% against a nominal 80%) is what that gap "
    "looks like in practice." if _dv80 is not None and _dv80 < 80 else
    f"The danskvand row ({_dv80:.1f}% at a nominal 80%) shows the empirical "
    "coverage staying close to nominal here." if _dv80 is not None else
    "The danskvand row shows what that gap looks like in practice.")
_width_line = (
    f"{' and '.join(_wide)} reach acceptable coverage at 90% only with "
    f"intervals spanning {min(_wide.values()):.0f}-{max(_wide.values()):.0f}x "
    "the actual, which no planner can act on. Report "
    f"{'those' if len(_wide) > 1 else 'that one'} as a limitation rather than "
    "averaging into a well-calibrated claim."
    if _wide else
    "No category needs an unusably wide interval to reach 90% coverage.")

lines = [f"# SRQ1 prediction-interval calibration — split conformal "
         f"({_served_desc}, brand×month)", "",
         "Half-width calibrated on validation residuals (log space); empirical coverage "
         "measured on test. Well-calibrated => empirical ≈ nominal.", "",
         "**Read coverage and width together.** Coverage alone is not a success "
         "criterion: an arbitrarily wide interval attains perfect coverage while "
         "carrying no decision-relevant information. `Mean rel. width` is the "
         "interval width as a multiple of the actual value, so 3.0 means the "
         "interval spans about three times the quantity being forecast.", "",
         "| Category | Nominal | Empirical coverage | Mean rel. width | n_test |",
         "|---|---|---|---|---|"]
for _, x in df.iterrows():
    flag = "" if x['mean_rel_width'] < 5 else "  **<- too wide to act on**"
    lines.append(f"| {x['category']} | {x['nominal']}% | {x['empirical_coverage']}% | "
                 f"{x['mean_rel_width']}{flag} | {int(x['n_test'])} |")
lines += ["", "Coverage near nominal indicates the conformal interval is a usable confidence "
          "signal for the agentic layer (SRQ2); systematic over/under-coverage flags residual "
          "heteroskedasticity (interval width is global, not per-series).", "",
          "## What the guarantee does and does not cover", "",
          "The half-width is the `ceil((n+1)(1-alpha))/n` empirical quantile of the "
          "calibration residuals, i.e. Algorithm 2 of Lei et al. (2018), whose "
          "distribution-free finite-sample guarantee is **marginal** coverage "
          "`P(Y in C(X)) >= 1-alpha` -- an average over cells, NOT a per-brand or "
          "per-month promise (Lei et al., 2018, Remark 3).", "",
          "**That guarantee assumes exchangeability, which monthly brand demand "
          "violates.** Barber et al. (2023) show unweighted split conformal can lose "
          "coverage materially under temporal drift, and bound the loss by a weighted "
          "sum of total-variation distances rather than eliminating it. So the "
          "coverage numbers above are an **empirical measurement**, not a theoretical "
          "entitlement -- which is exactly why they are measured on a held-out test "
          "period instead of assumed. " + _dv_line, "",
          "**Width is the binding constraint here, not coverage.** " + _width_line]
(RES / "calibration.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
print("Saved calibration.csv + calibration.md")
