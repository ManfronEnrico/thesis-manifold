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
  track record -- and with this model's MEASURED held-out accuracy on BOTH metrics,
                  plus the best classical baseline under EACH metric, so a caller can
                  judge whether to trust the number rather than inferring trust from
                  interval width alone. Both metrics are carried because they
                  disagree: on RTD the served model beats the best medMAPE baseline
                  by 7.4pp while LOSING to the best WMAPE baseline by 6.3pp.
                  The interval and the track record answer different questions:
                  "how uncertain is THIS forecast" vs "how accurate is this MODEL".

                  NOTE on `confidence`: it is a heuristic index combining relative
                  interval width and the conformal quantile, with hand-chosen 0.5/0.5
                  weights and 70/40 tier cutoffs. It is NOT a calibrated probability
                  and has no literature definition. Because both its terms derive
                  from the per-category q90, it varies little within a category.
                  Report it as an ordinal hint; let `historical_*` carry the
                  reliability claim.
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


# Held-out accuracy per (category, model), read once from the SRQ1 results.
# WHY THIS IS IN THE PAYLOAD: the conformal interval says how uncertain THIS
# forecast is; it says nothing about how accurate this model has been. Those are
# different questions, and an agent reasoning about whether to trust a number
# needs both. Without a track record the only reliability signal is `confidence`,
# which is a heuristic index (see _tier) rather than a measured error rate.
#
# Static lookup, not a computation: these are the numbers already reported in the
# thesis, so the tool cannot disagree with the results chapter.
_TRACK: dict | None = None


# Above this, a reported error rate is a failure indicator rather than a
# measurement. Ridge on energidrikke scored 2.8e13% WMAPE unclipped -- a model that
# collapsed on one series and had the failure amplified by expm1 (P0040 F63).
#
# WHY IT MUST NOT BE SERVED (Brian, 2026-08-22): an LLM shown "2.8e13%" either
# ignores it (harmless) or tries to reason about it (harmful), and it has no way to
# tell which case it is in. A number that large is not informative-but-extreme; it
# is a different KIND of thing from an error rate, wearing the same clothes.
# Substituting an explicit "n/a" plus a reason preserves the information that the
# method failed while removing the false quantity.
#
# 300% is chosen as "worse than any usable forecast" -- a forecast wrong by 3x is
# already useless, so nothing above it carries decision-relevant signal. It is a
# display threshold, not an analysis parameter: the RAW figures stay in
# stat_baselines.csv and the thesis reports them (F63). This only governs what the
# serving interface hands an agent.
_IMPLAUSIBLE_ERROR_PCT = 300.0


def _metric(value: float) -> float | str:
    """Return a finite, plausible error rate, or 'n/a (model failed)'."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "n/a (not available)"
    if not (v == v) or v in (float("inf"), float("-inf")):
        return "n/a (undefined)"
    if v > _IMPLAUSIBLE_ERROR_PCT:
        return "n/a (model failed on this category)"
    return round(v, 1)


def _norm_model(name: str) -> str:
    """Reconcile model names across artifacts.

    The persisted metadata records `XGBoost(tuned)` while tuned_metrics.csv records
    `XGBoost`. An exact-match join therefore silently returned nothing, and because
    the payload merges an empty dict, the historical_* fields simply vanished with
    no error -- a failure mode indistinguishable from success. Normalising both
    sides is the fix; this function is the single place that knows about the
    discrepancy."""
    n = str(name).strip()
    for suffix in ("(tuned)", "(Tuned)", "_tuned", " tuned"):
        if n.endswith(suffix):
            n = n[: -len(suffix)]
    return n.strip()


def _track_record(category: str, model_name: str) -> dict:
    """Held-out test accuracy for this model, plus the best classical baseline.

    Returns {} rather than raising if the results files are absent -- serving must
    not break because an analysis artifact moved."""
    global _TRACK
    if _TRACK is None:
        _TRACK = {"tuned": {}, "base": {}}
        # Prefer the CV-tuned results; fall back to the single-split ones.
        #
        # cv_metrics.csv comes from expanding-window time-series cross-validation
        # over 100 Optuna trials and SUPERSEDES tuned_metrics.csv, which used a
        # single validation split at 30 trials (P0040 F65). The numbers moved --
        # CSD LightGBM 15.6% -> 14.5%, RTD 35.1% -> 31.8% -- so serving the old
        # file would report a track record the thesis no longer claims.
        #
        # cv_metrics.csv has a `tuned_for` column (wmape | medmape): the SAME model
        # tuned for medMAPE scores 8-13pp worse on WMAPE. Only the wmape-tuned rows
        # are served, matching the models that are actually persisted and served.
        loaded_from = None
        for fname, wcol, mcol in (
            ("cv_metrics.csv", "test_wmape", "test_medmape"),
            ("tuned_metrics.csv", "test_wmape", "test_median"),
        ):
            try:
                tm = pd.read_csv(THESIS_RESULTS_SRQ1_DIR / fname)
            except Exception:
                continue
            if "tuned_for" in tm.columns:
                tm = tm[tm["tuned_for"] == "wmape"]
            if not len(tm):
                continue
            for _, r in tm.iterrows():
                # NOTE: tuned_metrics.csv's test_mape (MEAN APE) is unusable -- it
                # reaches 9.3e10 because APE divides by actuals and the panel
                # contains genuine zeros. Neither file's mean-APE column is read.
                _TRACK["tuned"][(str(r["category"]), _norm_model(str(r["model"])))] = {
                    "wmape": float(r[wcol]),
                    "median_mape": float(r[mcol]),
                }
            loaded_from = fname
            break

        if loaded_from is None:
            # Loud, not silent. A swallowed exception here previously made a failed
            # lookup indistinguishable from "no data": the payload simply omitted
            # historical_* and looked fine.
            print("  ! track record: neither cv_metrics.csv nor tuned_metrics.csv "
                  "could be read -- historical_* fields will be absent")
        _TRACK["source"] = loaded_from
        try:
            sb = pd.read_csv(THESIS_RESULTS_SRQ1_DIR / "stat_baselines.csv")
            for cat, g in sb.groupby("category"):
                # BOTH baselines are recorded, deliberately (P0040 F56).
                #
                # "Best" depends entirely on the yardstick, and the two disagree.
                # RTD: best-by-medMAPE is Naive (44.1%), and against it the served
                # model shows +7.4pp. Best-by-WMAPE is SeasonalNaive (27.3%), and
                # against THAT the served model is LOSING by 6.3pp. Same data,
                # opposite story, decided by which metric picks the opponent.
                #
                # Reporting only the medMAPE-selected baseline would hand the caller
                # the framing that flatters the served model. Both are returned so
                # the choice is visible rather than silently made here.
                g = g.dropna(subset=["median_mape", "wmape"])
                # Ridge is excluded from the BASELINE comparison on purpose. Its
                # per-brand fit is under-determined (~24 rows, 13 features) and
                # 5-15% of its predictions hit the extrapolation bound, which
                # truncates over-forecasts and mechanically flatters a
                # volume-weighted metric (P0040 F57). Comparing the served model
                # against a number partly produced by that bound would not be a
                # comparison against a baseline method.
                #
                # The pooled Ridge in ridge_pooled.csv IS sound and belongs in the
                # thesis's nonlinearity-premium argument -- it is simply not a
                # "classical benchmark" for this payload.
                g = g[g["model"] != "Ridge"]
                if not len(g):
                    continue
                bm = g.loc[g["median_mape"].idxmin()]
                bw = g.loc[g["wmape"].idxmin()]
                _TRACK["base"][str(cat)] = {
                    "by_median": {"model": str(bm["model"]),
                                  "wmape": float(bm["wmape"]),
                                  "median_mape": float(bm["median_mape"])},
                    "by_wmape": {"model": str(bw["model"]),
                                 "wmape": float(bw["wmape"]),
                                 "median_mape": float(bw["median_mape"])},
                }
        except Exception as e:
            print(f"  ! track record: stat_baselines.csv unreadable ({str(e)[:80]})")

    out = {}
    t = _TRACK["tuned"].get((category, _norm_model(model_name)))
    if t:
        # BOTH metrics, always. They answer different questions and they disagree:
        # WMAPE is volume-weighted ("how many total units are wrong"), median MAPE
        # weights every brand equally ("how wrong is a typical brand"). Reporting
        # one alone gives a systematically partial picture -- three separate
        # analyses in this project (P0040 F50, F51, F52) found the two diverging.
        out["historical_wmape"] = _metric(t["wmape"])
        out["historical_median_mape"] = _metric(t["median_mape"])

    b = _TRACK["base"].get(category)
    if b:
        bm, bw = b["by_median"], b["by_wmape"]
        out["baseline_best_by_median_mape"] = {
            "model": bm["model"],
            "wmape": _metric(bm["wmape"]),
            "median_mape": _metric(bm["median_mape"]),
        }
        out["baseline_best_by_wmape"] = {
            "model": bw["model"],
            "wmape": _metric(bw["wmape"]),
            "median_mape": _metric(bw["median_mape"]),
        }
        if t:
            # Both comparisons, and they can point in OPPOSITE directions.
            # Positive = the served model is better by that many percentage points.
            # Computed ONLY when both operands survived _metric -- a delta against a
            # failed baseline would be arithmetic on a non-number.
            def _delta(base, model):
                a, b_ = _metric(base), _metric(model)
                if isinstance(a, str) or isinstance(b_, str):
                    return None
                return round(a - b_, 1)

            dm = _delta(bm["median_mape"], t["median_mape"])
            dw = _delta(bw["wmape"], t["wmape"])
            if dm is not None:
                out["improvement_vs_baseline_median_pp"] = dm
            if dw is not None:
                out["improvement_vs_baseline_wmape_pp"] = dw
            if dm is not None and dw is not None and (dm > 0) != (dw > 0):
                # Flagged explicitly so a caller cannot quote the favourable half
                # without seeing that the other half disagrees.
                out["metrics_disagree"] = True

    if out:
        src = _TRACK.get("source") or "unknown"
        proto = ("expanding-window time-series CV, 100 Optuna trials, tuned for WMAPE"
                 if src == "cv_metrics.csv" else
                 "single validation split, 30 Optuna trials")
        out["accuracy_basis"] = (
            f"held-out test split; {proto} (04_thesis_results/srq1/{src}). "
            "WMAPE is volume-weighted; median MAPE weights each brand equally. "
            "Where they disagree, metrics_disagree is set.")
    return out


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
    f = MODELS_DIR / meta["model_file"]
    # The serving model is whichever one SRQ1 selected for this category, which
    # is not always XGBoost -- danskvand serves Ridge. Dispatch on the persisted
    # format rather than assuming a booster: assuming one raised
    # UnicodeDecodeError on a joblib pickle, which is a confusing way to learn
    # that the wrong loader was used.
    if f.suffix == ".json":
        from xgboost import XGBRegressor
        m = XGBRegressor()
        m.load_model(str(f))
    else:
        import joblib
        m = joblib.load(f)
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
    # Apply exactly the transform training applied. The metadata records it, so
    # serving cannot silently diverge from the fitted pipeline -- a linear model
    # fitted on clipped inputs and served unclipped would take log1p of a
    # negative number and return NaN.
    X = row[feats].fillna(0.0)
    if meta.get("clip_negative_features"):
        X = X.clip(lower=0)
    yhat = float(np.clip(np.expm1(m.predict(X)[0]), 0, None))
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
        # Measured track record -- see _track_record. Distinct from the interval:
        # the interval is about this forecast, these are about this model.
        **_track_record(category, meta["model"]),
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
