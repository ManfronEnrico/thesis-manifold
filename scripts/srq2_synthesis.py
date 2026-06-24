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
Output: thesis/data/_06_results_srq2/{synthesis.csv, synthesis_summary.md}
"""
import json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
RES5 = ROOT / "thesis" / "data" / "_05_results_srq1"
OUT = ROOT / "thesis" / "data" / "_06_results_srq2"; OUT.mkdir(parents=True, exist_ok=True)
SEED = 42
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "holiday_month", "promo_intensity", "weighted_distribution"]
# Ch6 §6.5.6 selected (model fixed to the ladder; granularity per category)
SELECTED = {"CSD": ("csd", "_03_engineered_dvhexclhd", "CSD"),
            "danskvand": ("danskvand", "_04_engineered_bychain", "danskvand"),
            "energidrikke": ("energidrikke", "_03_engineered_dvhexclhd", "energidrikke"),
            "RTD": ("rtd", "_03_engineered_dvhexclhd", "RTD")}
params = json.loads((RES5 / "tuned_params.json").read_text())


def _models(ds_tag, cat):
    pk = "bychain" if "bychain" in ds_tag else "brand"
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


rows = []
for cat, (slug, ds_tag, sub) in SELECTED.items():
    fm = pd.read_parquet(ROOT / f"thesis/data/{ds_tag}/{sub}/{slug}_feature_matrix.parquet")
    keys = ["brand", "chain"] if "chain" in fm.columns else ["brand"]
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr, va, te = (d[d.split == s] for s in ("train", "val", "test"))
    if len(tr) < 30 or len(te) == 0:
        continue
    mods = _models(ds_tag, cat)
    # fit on train; val for weights+calibration
    val_wmape, val_res, te_pred = {}, {}, {}
    for name, m in mods.items():
        m.fit(tr[FEATURES].fillna(0.0), tr["log_sales_units"].values)
        pv = np.expm1(m.predict(va[FEATURES].fillna(0.0)))
        yv = np.expm1(va["log_sales_units"].values)
        val_wmape[name] = np.abs(yv - np.clip(pv, 0, None)).sum() / max(yv.sum(), 1e-9)
        val_res[name] = np.abs(va["log_sales_units"].values - m.predict(va[FEATURES].fillna(0.0)))
        te_pred[name] = np.clip(np.expm1(m.predict(te[FEATURES].fillna(0.0))), 0, None)
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
(OUT / "synthesis_summary.md").write_text("\n".join(lines) + "\n")
print("Saved synthesis.csv + synthesis_summary.md")
for cat in SELECTED:
    s = df[df.category == cat]
    if len(s):
        print(f"  {cat:13s} n={len(s):4d} meanConf={s.confidence.mean():4.1f} "
              f"coverage={100*s.in_interval.mean():4.1f}% tiers={dict(s.tier.value_counts())}")
