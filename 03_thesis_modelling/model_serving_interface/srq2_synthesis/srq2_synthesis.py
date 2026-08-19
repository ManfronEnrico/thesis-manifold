#!/usr/bin/env python3
"""
SRQ2 synthesis engine (deterministic core) — multi-model -> confidence-scored output.

Implements the non-LLM part of the Synthesis Agent (Ch7 §7.2): per category, train
the model ladder (Ridge/LightGBM/XGBoost) with tuned configs on the SELECTED
granularity (Ch6 §6.5.6), produce per-series test forecasts, then for each series:
  - inter-model agreement = 1 - std(forecasts)/mean(forecasts)  (relative consensus)
  - inverse-MAPE ensemble point forecast (weights from validation WMAPE)
  - split-conformal 90% interval around the ensemble (calibrated on validation)
  - composite confidence score 0-100 and 3-tier label (High/Moderate/Low)

The LLM recommendation text and LLM-as-Judge (Ch7 §7.6, Ch8 §8.3) need an LLM API
and are NOT run here; this engine produces the structured inputs they consume.

Self-contained, reproducible (seed=42). No Prometheus/Nika/LLM-API dependency.
Usage: .venv/bin/python scripts/srq2_synthesis.py
Output: 04_thesis_results/srq2/{synthesis.csv, synthesis_summary.md}
"""
import json, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor

# Repo root located by searching upward for PATHS.py rather than by a fixed
# parents[N] index: the index silently breaks whenever a script moves a
# directory deeper, which is exactly what happened in the 2026-08-19
# reorganisation (ModuleNotFoundError: No module named 'PATHS').
_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import (
    THESIS_RESULTS_SRQ1_DIR, THESIS_RESULTS_SRQ2_DIR,
    get_category_engineered_bymonth_dir,
)

warnings.filterwarnings("ignore")
RES5 = THESIS_RESULTS_SRQ1_DIR
OUT = THESIS_RESULTS_SRQ2_DIR; OUT.mkdir(parents=True, exist_ok=True)
SEED = 42
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

	DEC-OPEN-WORLD: categories differ in capability, not just in values.
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

# Ch6 §6.5.6 selected (model fixed to the ladder; granularity per category)
# GRAIN (P0035, 2026-08-01): DEC-GRAIN (2026-07-12) locked the thesis to
# brand x month. danskvand was previously pinned to the 'bychain' grain here;
# its data directory is deleted, so it now reads brand x month like every other
# category. Tag kept in the tuple shape so a future grain can be reintroduced.
# Tag value "bymonth" selects the PATHS.py helper, not a literal path segment.
SELECTED = {"CSD": ("csd", "bymonth", "CSD"),
            "danskvand": ("danskvand", "bymonth", "danskvand"),
            "energidrikke": ("energidrikke", "bymonth", "energidrikke"),
            "RTD": ("rtd", "bymonth", "RTD")}
params = json.loads((RES5 / "tuned_params.json").read_text())


def _models(ds_tag, cat):
    pk = "brand"
    return {
        "Ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
        "LightGBM": LGBMRegressor(random_state=SEED, verbose=-1, **params.get(f"{pk}/{cat}/LightGBM", {})),
        "XGBoost": XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params.get(f"{pk}/{cat}/XGBoost", {})),
    }


def confidence(agreement, rel_width, acc_score):
    """0-100 composite: 30% agreement + 40% interval tightness + 30% model accuracy."""
    tight = 1.0 / (1.0 + rel_width)          # narrower interval -> closer to 1
    return float(np.clip(100 * (0.30 * agreement + 0.40 * tight + 0.30 * acc_score), 0, 100))


def tier(score):
    return "High" if score >= 70 else ("Moderate" if score >= 40 else "Low")



def build_synthesis():
    """Train the model ladder and write synthesis.csv + synthesis_summary.md.

    Previously this ran at IMPORT time -- the whole training pass fired the
    moment anything did `import srq2_synthesis`, including a harmless
    inspection or a doc tool. That made the module unusable as a library and
    made any importer silently pay for a full retrain.
    """
    rows = []
    for cat, (slug, ds_tag, sub) in SELECTED.items():
        eng_dir = get_category_engineered_bymonth_dir(sub)
        fm = pd.read_parquet(eng_dir / f"{slug}_feature_matrix_h3.parquet")
        keys = ["brand", "chain"] if "chain" in fm.columns else ["brand"]
        d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
        tr, va, te = (d[d.split == s] for s in ("train", "val", "test"))
        if len(tr) < 30 or len(te) == 0:
            continue
        mods = _models(ds_tag, cat)
        # fit on train; val for weights+calibration
        val_wmape, val_res, te_pred = {}, {}, {}
        for name, m in mods.items():
            m.fit(tr[available_features(fm)].fillna(0.0), tr["log_sales_units"].values)
            pv = np.expm1(m.predict(va[available_features(fm)].fillna(0.0)))
            yv = np.expm1(va["log_sales_units"].values)
            val_wmape[name] = np.abs(yv - np.clip(pv, 0, None)).sum() / max(yv.sum(), 1e-9)
            val_res[name] = np.abs(va["log_sales_units"].values - m.predict(va[available_features(fm)].fillna(0.0)))
            te_pred[name] = np.clip(np.expm1(m.predict(te[available_features(fm)].fillna(0.0))), 0, None)
        # inverse-WMAPE weights
        inv = {k: 1.0 / max(v, 1e-6) for k, v in val_wmape.items()}
        Z = sum(inv.values()); w = {k: inv[k] / Z for k in inv}
        # ensemble conformal half-width (weighted val residuals, 90%)
        q90 = np.quantile(np.concatenate([val_res[k] for k in mods]), 0.90)
        acc_score = float(1.0 - min(val_wmape.values()))  # best model skill, clipped later
        ytrue = np.expm1(te["log_sales_units"].values)
        P = np.vstack([te_pred[k] for k in mods]).T  # rows=series, cols=models
        ens = P @ np.array([w[k] for k in mods])
        for i in range(len(ytrue)):
            fc = P[i]; mean_fc = max(fc.mean(), 1e-9)
            agreement = float(np.clip(1.0 - fc.std() / mean_fc, 0, 1))
            lo, hi = np.expm1(np.log(max(ens[i], 1e-9)) - q90), np.expm1(np.log(max(ens[i], 1e-9)) + q90)
            rel_width = (hi - lo) / max(ens[i], 1e-9)
            sc = confidence(agreement, rel_width, max(acc_score, 0))
            rows.append(dict(category=cat, ensemble=round(float(ens[i]), 1),
                             lower90=round(float(lo), 1), upper90=round(float(hi), 1),
                             agreement=round(agreement, 3), confidence=round(sc, 1), tier=tier(sc),
                             actual=round(float(ytrue[i]), 1),
                             in_interval=bool(lo <= ytrue[i] <= hi)))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "synthesis.csv", index=False)

    # summary
    lines = ["# SRQ2 synthesis engine — deterministic core (Ch7 §7.2)", "",
             "Per-series ensemble forecast (inverse-WMAPE weighted), inter-model agreement, "
             "split-conformal 90% interval, composite confidence (30% agreement + 40% interval "
             "tightness + 30% model accuracy) and 3-tier label. LLM recommendation text + "
             "LLM-as-Judge (Ch7 §7.6 / Ch8 §8.3) need an LLM API and are not run here.", "",
             "| Category | n_series | mean confidence | %High | %Moderate | %Low | interval coverage |",
             "|---|---|---|---|---|---|---|"]
    for cat in SELECTED:
        s = df[df.category == cat]
        if not len(s):
            continue
        cov = 100 * s.in_interval.mean()
        vc = s.tier.value_counts(normalize=True) * 100
        lines.append(f"| {cat} | {len(s)} | {s.confidence.mean():.1f} | {vc.get('High',0):.0f}% | "
                     f"{vc.get('Moderate',0):.0f}% | {vc.get('Low',0):.0f}% | {cov:.1f}% |")
    lines += ["", "Confidence-tier triage lets the agentic layer surface High-confidence forecasts "
              "directly and flag Low-confidence ones for human review (SRQ2 reliability/traceability)."]
    (OUT / "synthesis_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("Saved synthesis.csv + synthesis_summary.md")
    for cat in SELECTED:
        s = df[df.category == cat]
        if len(s):
            print(f"  {cat:13s} n={len(s):4d} meanConf={s.confidence.mean():4.1f} "
                  f"coverage={100*s.in_interval.mean():4.1f}% tiers={dict(s.tier.value_counts())}")


if __name__ == "__main__":
    build_synthesis()
