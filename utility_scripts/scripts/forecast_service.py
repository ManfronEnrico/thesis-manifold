#!/usr/bin/env python3
"""
Forecast service — the dedicated-model layer behind System A's `forecast_demand` tool.

This is the thesis's alternative to code-as-action: instead of an LLM writing
forecasting code at runtime, a pre-trained model answers via a structured call.
Per category it trains the selected tuned XGBoost (Ch6 §6.5.6 configuration) on all
observed data, then produces a one-step-ahead (next month) forecast for every series
with a split-conformal 90% interval and a confidence tier.

Two entry points:
  - build_service()        : train + write 03_thesis_modelling/model_serving/system_a_forecast/forecasts.csv
  - forecast_demand(...)   : the callable the agent tool wraps (reads the lookup)

Self-contained, reproducible (seed=42). No Prometheus/Nika/LLM dependency.
Usage: .venv/bin/python scripts/forecast_service.py        # builds the lookup
"""
import json, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import (
    THESIS_RESULTS_SRQ1_DIR, THESIS_MODELLING_SERVING_SYSTEM_A_DIR,
    get_category_engineered_bymonth_dir, get_category_engineered_bychain_dir,
)

warnings.filterwarnings("ignore")
RES5 = THESIS_RESULTS_SRQ1_DIR
OUT = THESIS_MODELLING_SERVING_SYSTEM_A_DIR; OUT.mkdir(parents=True, exist_ok=True)
SEED = 42
LAGS = (1, 2, 3, 4, 8, 13); HOL = {3, 6, 12}
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "holiday_month", "promo_intensity", "weighted_distribution"]
# Ch6 §6.5.6 selected (model = tuned XGBoost; granularity per category)
# Tag values ("bymonth"/"bychain") select the PATHS.py helper, not a literal path segment.
SELECTED = {"CSD": ("csd", "bymonth", "CSD", ["brand"]),
            "danskvand": ("danskvand", "bychain", "danskvand", ["brand", "chain"]),
            "energidrikke": ("energidrikke", "bymonth", "energidrikke", ["brand"]),
            "RTD": ("rtd", "bymonth", "RTD", ["brand"])}


def _tier(score):
    return "High" if score >= 70 else ("Moderate" if score >= 40 else "Low")


def build_service():
    from xgboost import XGBRegressor
    params = json.loads((RES5 / "tuned_params.json").read_text())
    rows = []
    for cat, (slug, ds_tag, sub, keys) in SELECTED.items():
        pk = "bychain" if "chain" in keys else "brand"
        eng_dir = get_category_engineered_bychain_dir(sub) if ds_tag == "bychain" else get_category_engineered_bymonth_dir(sub)
        fm = pd.read_parquet(eng_dir / f"{slug}_feature_matrix.parquet")
        d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
        if len(d) < 30:
            continue
        m = XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params.get(f"{pk}/{cat}/XGBoost", {}))
        m.fit(d[FEATURES].fillna(0.0), d["log_sales_units"].values)
        # conformal half-width on the held-out test residuals (log space), 90%
        te = fm[fm.split == "test"].dropna(subset=["log_sales_units", "lag_1", "lag_13"])
        q90 = float(np.quantile(np.abs(te["log_sales_units"].values - m.predict(te[FEATURES].fillna(0.0))), 0.90)) if len(te) else 0.5

        full = fm.copy().sort_values(keys + ["period_index"])
        for kv, g in full.groupby(keys):
            g = g.sort_values("period_index")
            obs = g.dropna(subset=["sales_units"])
            if len(obs) < 13:
                continue
            hist = g["sales_units"].values  # grid-ordered (may include NaN gaps)
            last_idx = int(g["period_index"].max())
            # next-period calendar
            lm = int(g.iloc[-1]["period_month"]); nm = lm % 12 + 1
            # build next-step feature row from the most recent values
            def lag(k):
                v = g["sales_units"].values
                return v[-k] if len(v) >= k and not np.isnan(v[-k]) else np.nan
            past = obs["sales_units"].values
            feat = {f"lag_{k}": lag(k) for k in LAGS}
            feat["rolling_mean_4"] = np.nanmean(past[-4:]) if len(past) else np.nan
            feat["rolling_std_4"] = np.nanstd(past[-4:]) if len(past) >= 2 else np.nan
            feat["rolling_mean_13"] = np.nanmean(past[-13:]) if len(past) else np.nan
            feat["month"] = nm; feat["quarter"] = (nm - 1) // 3 + 1; feat["holiday_month"] = int(nm in HOL)
            feat["promo_intensity"] = float(obs.iloc[-1].get("promo_intensity", 0) or 0)
            feat["weighted_distribution"] = float(obs.iloc[-1].get("weighted_distribution", np.nan))
            X = pd.DataFrame([{f: feat.get(f, np.nan) for f in FEATURES}]).fillna(0.0)
            yhat = float(np.clip(np.expm1(m.predict(X)[0]), 0, None))
            lo, hi = float(np.expm1(np.log(max(yhat, 1e-9)) - q90)), float(np.expm1(np.log(max(yhat, 1e-9)) + q90))
            rel = (hi - lo) / max(yhat, 1e-9)
            conf = float(np.clip(100 * (0.5 * (1 / (1 + rel)) + 0.5 * (1 - min(q90, 1))), 0, 100))
            kv_t = kv if isinstance(kv, tuple) else (kv,)
            brand = kv_t[0]
            chain = kv_t[1] if len(kv_t) > 1 else ""
            rows.append(dict(category=cat, brand=brand, chain=chain,
                             forecast_month=f"month_{nm:02d}", forecast=round(yhat, 1),
                             lower90=round(lo, 1), upper90=round(hi, 1),
                             confidence=round(conf, 1), tier=_tier(conf), model="XGBoost(tuned)"))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "forecasts.csv", index=False)
    print(f"Built forecast lookup: {len(df)} series across {df.category.nunique()} categories")
    for cat in SELECTED:
        s = df[df.category == cat]
        if len(s):
            print(f"  {cat:13s} {len(s):4d} forecasts  tiers={dict(s.tier.value_counts())}")
    return df


def forecast_demand(category: str, brand: str, chain: str | None = None) -> dict:
    """Structured forecast for one (category, brand[, chain]) — what the agent tool returns."""
    df = pd.read_csv(OUT / "forecasts.csv")
    q = df[(df.category.str.lower() == category.lower()) & (df.brand.str.upper() == brand.upper())]
    if chain:
        q = q[q.chain.str.upper() == chain.upper()]
    if not len(q):
        return {"status": "not_found", "message": f"No forecast for {category}/{brand}" + (f"/{chain}" if chain else "")}
    r = q.iloc[0]
    chain_val = r.chain if (isinstance(r.chain, str) and r.chain.strip()) else None
    return {"status": "ok", "category": r.category, "brand": r.brand, "chain": chain_val,
            "forecast_units": r.forecast, "interval_90": [r.lower90, r.upper90],
            "confidence": r.confidence, "tier": r.tier, "model": r.model,
            "horizon": "next month"}


if __name__ == "__main__":
    build_service()
    # smoke demo
    import pprint
    pprint.pprint(forecast_demand("CSD", "HARBOE"))
