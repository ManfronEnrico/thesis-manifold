#!/usr/bin/env python3
"""
Scenario C's tool interface — SRQ2's structured tool/action contract.

THIS MODULE SERVES. IT NEVER TRAINS.

Models are fitted once by `model_training/train_and_persist.py` and written to
04_thesis_results/srq1/models/. This loads them. That boundary matters for three
reasons, all of which were live defects before it existed:

  1. Three separate copies of the training logic had drifted apart, and the
     conformal-calibration fix (intervals were 3.9x too narrow) landed in one of
     them while the other two kept the bug.
  2. `srq4_experiment._eval_forecast` refit the model on EVERY tool call --
     ~1.1 s of identical work per call, inflating Scenario C's measured latency
     with training time that a real deployment would never pay.
  3. `srq2_synthesis.py` retrained on import.

WHAT SRQ2 ASKS, AND WHERE IT IS ANSWERED HERE
---------------------------------------------
  reliability  -- the number the agent reports is the number the model produced;
                  `forecast_demand` returns it, and the caller records it, so
                  prose cannot silently diverge from the source value.
  uncertainty  -- every forecast travels with a split-conformal 90% interval and
                  a confidence tier, never as a bare point estimate.
  traceability -- every call is appended to forecast_log.jsonl with the model
                  file, its training cutoff, the calibration split, the feature
                  count and a UTC timestamp.

Usage:
    from forecast_tool import forecast_demand
    forecast_demand("CSD", "HARBOE")            # next held-out month
    forecast_demand("CSD", "HARBOE", "2026-06") # a specific test month
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir

MODELS_DIR = THESIS_RESULTS_SRQ1_DIR / "models"
LOG_FILE = Path(__file__).resolve().parent / "forecast_log.jsonl"

CATEGORIES = {"CSD": "csd", "danskvand": "danskvand",
              "energidrikke": "energidrikke", "RTD": "rtd"}

# Loaded models, keyed by category. Populated on first use and reused for the
# life of the process: loading a booster is cheap, but doing it per call would
# reintroduce the latency this module exists to remove.
_CACHE: dict[str, tuple] = {}


def _tier(score: float) -> str:
    return "High" if score >= 70 else ("Moderate" if score >= 40 else "Low")


def _load(category: str):
    """Load the persisted booster + metadata for a category."""
    if category in _CACHE:
        return _CACHE[category]
    meta_f = MODELS_DIR / f"{category}_metadata.json"
    if not meta_f.is_file():
        raise FileNotFoundError(
            f"No persisted model for {category}. Run "
            f"model_training/train_and_persist.py first. Expected {meta_f}")
    meta = json.loads(meta_f.read_text(encoding="utf-8"))
    from xgboost import XGBRegressor
    m = XGBRegressor()
    m.load_model(str(MODELS_DIR / meta["model_file"]))
    _CACHE[category] = (m, meta)
    return _CACHE[category]


def _log(record: dict) -> None:
    """Append one line to the forecast log.

    JSONL, not CSV: a CSV needs the whole file rewritten to add a row (which is
    why the previous forecasts.csv carried a single stale timestamp for every
    row and never recorded a served forecast at all). One JSON object per line
    appends in O(1), survives partial writes, and carries nested provenance that
    a flat CSV cannot."""
    try:
        with LOG_FILE.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(record, default=str) + "\n")
    except Exception as e:  # logging must never break serving
        print(f"  ! forecast log write failed: {str(e)[:120]}")


def forecast_demand(category: str, brand: str, month: str | None = None) -> dict:
    """Return the structured forecast payload for one (category, brand).

    `month` selects a specific held-out month ("2026-06"); omitted, the first
    test month is used. Requesting a month outside the test split is refused --
    the model was trained through the validation period, so a train or
    validation month is not a forecast, it is recall.
    """
    t0 = time.perf_counter()
    if category not in CATEGORIES:
        return {"status": "unknown_category", "category": category,
                "known": sorted(CATEGORIES)}

    m, meta = _load(category)
    feats = meta["features"]
    q90 = meta["q90_log"]

    slug = CATEGORIES[category]
    fm = pd.read_parquet(
        get_category_engineered_bymonth_dir(category) / f"{slug}_feature_matrix_h3.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"])
    te = d[d.split == "test"].copy()
    te["ym"] = (te.period_year.astype(int).astype(str) + "-"
                + te.period_month.astype(int).map("{:02d}".format))

    rows = te[te.brand.str.upper() == brand.upper()].sort_values("period_index")
    if not len(rows):
        return {"status": "not_found", "category": category, "brand": brand,
                "message": f"No held-out row for {brand} in {category}"}

    if month:
        # Refusing rather than silently substituting: a caller asking for a
        # non-test month is making an error the result would otherwise hide.
        if month not in set(te.ym):
            return {"status": "month_not_held_out", "category": category,
                    "brand": brand, "requested_month": month,
                    "available_months": meta.get("test_months", []),
                    "message": (f"{month} is not in the test split. The model was "
                                f"trained through {meta['trained_through']}, so a "
                                "forecast for an earlier month would be recall, "
                                "not prediction.")}
        rows = rows[rows.ym == month]
        if not len(rows):
            return {"status": "not_found", "category": category, "brand": brand,
                    "requested_month": month,
                    "message": f"No row for {brand} in {month}"}

    row = rows.head(1)
    yhat = float(np.clip(np.expm1(m.predict(row[feats].fillna(0.0))[0]), 0, None))
    lo = float(np.expm1(np.log(max(yhat, 1e-9)) - q90))
    hi = float(np.expm1(np.log(max(yhat, 1e-9)) + q90))
    rel = (hi - lo) / max(yhat, 1e-9)
    conf = float(np.clip(100 * (0.5 * (1 / (1 + rel)) + 0.5 * (1 - min(q90, 1))), 0, 100))

    out = {
        "status": "ok",
        "category": category,
        "brand": brand,
        "forecast_month": row.iloc[0]["ym"],
        "forecast_units": round(yhat, 1),
        "interval_90": [round(lo, 1), round(hi, 1)],
        "confidence": round(conf, 1),
        "confidence_tier": _tier(conf),
        # Provenance travels with every forecast (SRQ2 traceability).
        "model": meta["model"],
        "model_file": meta["model_file"],
        "trained_on": meta["trained_on"],
        "trained_through": meta["trained_through"],
        "calibrated_on": meta["calibrated_on"],
        "calibrated_through": meta["calibrated_through"],
        "n_calibration_rows": meta["n_calibration_rows"],
        "interval_method": meta["interval_method"],
        "n_features": meta["n_features"],
        "serve_seconds": round(time.perf_counter() - t0, 4),
        "served_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    _log(out)
    return out


def _demo():
    import argparse
    ap = argparse.ArgumentParser(description="Scenario C forecast tool")
    ap.add_argument("--category", default="CSD")
    ap.add_argument("--brand", default="HARBOE")
    ap.add_argument("--month", default=None)
    a = ap.parse_args()
    print(json.dumps(forecast_demand(a.category, a.brand, a.month), indent=2))
    print(f"\nlogged to {LOG_FILE}")


if __name__ == "__main__":
    _demo()
