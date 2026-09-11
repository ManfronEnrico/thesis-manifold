"""Second pass: can ANY scheme beat pooled without undercovering?

Pass 1 showed size-bucketing fails (only 1-4 brands per category exceed 1M
units/month, so the large bucket has 0-28 calibration rows and falls back to
pooled) and that per-brand normalisation undercovers badly (69-80% vs a 90%
target) because a brand's mean validation residual is itself estimated from ~7
rows and is far too noisy a divisor.

Tested here:
  - pooled                  the shipped scheme, as baseline
  - volatility-scaled       divide by the brand's own coefficient of variation
                            in the CALIBRATION window -- a stable statistic,
                            unlike its mean residual
  - two-bucket              split at the MEDIAN brand size, so both halves are
                            populated by construction
  - pooled_95               the shipped scheme at a 95th percentile, to show
                            what buying coverage costs in width

Honest accounting: a scheme only "wins" if it holds coverage near 90% AND is
narrower. Undercovering to look narrow is not a win.
"""
import json, sys
import numpy as np, pandas as pd

sys.path.insert(0, r"Z:\_dev-ssd\thesis-manifold")
sys.path.insert(0, r"Z:\_dev-ssd\thesis-manifold\04_SRQ4_Scenario_Experiment\scenario_setup")
import srq4_experiment as E

MODELS = r"Z:\_dev-ssd\thesis-manifold\05_thesis_results\05_model_benchmark\models"
DIRS = {"CSD": "CSD", "Danskvand": "danskvand",
        "Energidrikke": "energidrikke", "RTD": "RTD"}


def _make(name, params, seed):
    if name.startswith("XGBoost"):
        import xgboost as xgb
        return xgb.XGBRegressor(**params, random_state=seed)
    import lightgbm as lgb
    return lgb.LGBMRegressor(**params, random_state=seed, verbose=-1)


rows = []
for cat, d in DIRS.items():
    meta = json.load(open(f"{MODELS}/{d}/metadata.json", encoding="utf-8"))
    feats, params, seed = meta["features"], meta["hyperparameters"], meta["seed"]
    slug, tag, sub = E.CAT_FILE[cat]
    fm = pd.read_parquet(E._matrix_path(slug, tag, sub))
    tr = fm[fm.split == "train"].dropna(subset=["sales_units"])
    va = fm[fm.split == "val"].dropna(subset=["sales_units"]).copy()
    te = fm[fm.split == "test"].dropna(subset=["sales_units"]).copy()
    if not len(va) or not len(te):
        continue

    m_cal = _make(meta["model"], params, seed)
    m_cal.fit(tr[feats].fillna(0.0), tr["log_sales_units"].values)
    va["resid"] = np.abs(va["log_sales_units"].values
                         - m_cal.predict(va[feats].fillna(0.0)))

    trval = pd.concat([tr, va]).sort_values("period_index")
    m_srv = _make(meta["model"], params, seed)
    m_srv.fit(trval[feats].fillna(0.0), trval["log_sales_units"].values)
    pred = m_srv.predict(te[feats].fillna(0.0))
    act = te.sales_units.values

    # Brand statistics from the CALIBRATION window only.
    g = va.groupby("brand").sales_units
    cv = (g.std() / g.mean().clip(lower=1e-9)).fillna(1.0).clip(0.1, 3.0)
    bmean = va.groupby("brand").sales_units.mean()
    med = float(bmean.median())

    q_pooled = float(np.quantile(va.resid, 0.90))
    q_p95 = float(np.quantile(va.resid, 0.95))

    va["cv"] = va.brand.map(cv).fillna(1.0)
    q_vol = float(np.quantile(va.resid / va["cv"], 0.90))
    te_cv = te.brand.map(cv).fillna(1.0).values

    va["half"] = (va.brand.map(bmean) >= med).map({True: "upper", False: "lower"})
    q_half = {h: float(np.quantile(s.resid, 0.90))
              for h, s in va.groupby("half") if len(s) >= 30}
    te_half = (te.brand.map(bmean).fillna(0) >= med).map({True: "upper", False: "lower"})
    q_two = te_half.map(q_half).fillna(q_pooled).values

    big = (te.brand.map(bmean).fillna(0) >= med).values   # upper half of brands
    for name, q in {"pooled (SHIPPED)": np.full(len(te), q_pooled),
                    "pooled @95th": np.full(len(te), q_p95),
                    "volatility-scaled": q_vol * te_cv,
                    "two-bucket (median split)": q_two}.items():
        lo, hi = np.expm1(pred - q), np.expm1(pred + q)
        cov = (act >= lo) & (act <= hi)
        width = (hi - lo) / np.maximum(np.expm1(pred), 1)
        rows.append({"category": cat, "scheme": name,
                     "cov_%": round(cov.mean() * 100, 1),
                     "width_x": round(float(np.median(width)), 1),
                     "cov_upper_%": round(float(cov[big].mean() * 100), 1),
                     "width_upper_x": round(float(np.median(width[big])), 1)})

df = pd.DataFrame(rows)
pd.set_option("display.width", 200)
print("\nTEST-SET. 'upper' = the larger half of brands by calibration-window volume.")
print("A scheme wins only if coverage stays near 90% AND width falls.\n")
for cat in DIRS:
    s = df[df.category == cat]
    if len(s):
        print(s.to_string(index=False)); print()
