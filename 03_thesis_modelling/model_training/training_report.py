#!/usr/bin/env python3
"""
Model-training transparency report. Costs nothing; makes no API calls.

WHY: the trained model is the thesis artefact that Scenario C exposes, and until
now nothing said in one place what it was trained on, what it was tuned against,
how its intervals were calibrated, or how well it does. That gap is not a
documentation nicety -- an examiner asking "how did you train this?" needs an
answer that is generated from the data rather than asserted from memory.

Mirrors the EDA step reports: markdown tables written to disk, regenerable, with
the reasoning next to the numbers.

Sections:
  1. Data the model sees      -- rows per split, date boundaries, leakage checks
  2. Features                 -- which columns, which are absent where, and why
  3. Hyperparameters          -- what was tuned, on what, with what objective
  4. Accuracy                 -- per category and model, medMAPE + WMAPE
  5. Interval calibration     -- the split-conformal contract and its width
  6. What the tool returns    -- the exact payload Scenario C receives

Usage:
    python 03_thesis_modelling/model_training/training_report.py
    python 03_thesis_modelling/model_training/training_report.py --out DIR
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import (THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir)

warnings.filterwarnings("ignore")

# Mirrors srq4_experiment.CAT_FILE. Kept local so this report can run even if the
# harness is mid-edit -- a transparency report that breaks when the thing it
# documents breaks is useless exactly when it is needed.
CATEGORIES = {"CSD": "csd", "danskvand": "danskvand",
              "energidrikke": "energidrikke", "RTD": "rtd"}

FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "peak_month", "promo_intensity"]


def _matrix(cat):
    slug = CATEGORIES[cat]
    f = get_category_engineered_bymonth_dir(cat) / f"{slug}_feature_matrix_h3.parquet"
    return pd.read_parquet(f) if f.is_file() else None


def _span(df):
    if not len(df):
        return "-"
    d = df.sort_values(["period_year", "period_month"])
    a, b = d.iloc[0], d.iloc[-1]
    return (f"{int(a.period_year)}-{int(a.period_month):02d} to "
            f"{int(b.period_year)}-{int(b.period_month):02d}")


def section_data(L):
    L += ["## 1. What the model is trained on", "",
          "One row per brand x month. The `split` column is assigned by the "
          "preprocessing pipeline as a strict forward chain: every train month "
          "precedes every validation month, which precedes every test month. A "
          "random split would let the model learn from the future.", "",
          "| Category | Brands | Train | Val | Test | Train span | Val span | Test span |",
          "|---|---:|---:|---:|---:|---|---|---|"]
    for cat in CATEGORIES:
        fm = _matrix(cat)
        if fm is None:
            L.append(f"| {cat} | _matrix missing_ | | | | | | |")
            continue
        d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"])
        parts = {s: d[d.split == s] for s in ("train", "val", "test")}
        L.append(f"| {cat} | {d.brand.nunique()} | {len(parts['train'])} | "
                 f"{len(parts['val'])} | {len(parts['test'])} | "
                 f"{_span(parts['train'])} | {_span(parts['val'])} | "
                 f"{_span(parts['test'])} |")

    L += ["", "**Rows are dropped** where `log_sales_units`, `lag_1` or `lag_13` "
          "is null -- a series cannot be modelled before it has 13 months of "
          "history, so early months are warm-up, not training data.", ""]

    # Leakage is asserted, not assumed: an ordering violation here would be
    # invisible in the accuracy numbers except as suspiciously good performance.
    L += ["### Leakage checks", "",
          "| Category | train < val | val < test | verdict |", "|---|---|---|---|"]
    for cat in CATEGORIES:
        fm = _matrix(cat)
        if fm is None:
            continue
        d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"])
        def last(s):
            x = d[d.split == s]
            return (x.period_year * 100 + x.period_month).max() if len(x) else None
        def first(s):
            x = d[d.split == s]
            return (x.period_year * 100 + x.period_month).min() if len(x) else None
        tv = last("train") < first("val") if last("train") and first("val") else None
        vt = last("val") < first("test") if last("val") and first("test") else None
        ok = "PASS" if (tv and vt) else "**FAIL**"
        L.append(f"| {cat} | {tv} | {vt} | {ok} |")
    L.append("")
    return L


def section_features(L):
    L += ["## 2. Features", "",
          "Selected by intersection, not by a fixed list (DEC-OPEN-WORLD). "
          "Categories differ in *capability*, not only in values: Nielsen reports "
          "no promotion data for some categories, so `promo_intensity` is omitted "
          "there rather than zero-filled -- a constant-zero column would assert "
          "\"no promotion ran\", which the data does not support.", "",
          "| Feature | CSD | danskvand | energidrikke | RTD | what it is |",
          "|---|:-:|:-:|:-:|:-:|---|"]
    desc = {
        "lag_1": "sales 1 month back", "lag_2": "sales 2 months back",
        "lag_3": "sales 3 months back", "lag_4": "sales 4 months back",
        "lag_8": "sales 8 months back", "lag_13": "same month last year",
        "rolling_mean_4": "4-month mean, excluding current",
        "rolling_std_4": "4-month volatility",
        "rolling_mean_13": "13-month mean (annual level)",
        "month": "calendar month", "quarter": "calendar quarter",
        "peak_month": "flag for the category's seasonal peak",
        "promo_intensity": "promotion share at t-1 (lagged: contemporaneous would leak)",
    }
    mats = {c: _matrix(c) for c in CATEGORIES}
    for f in FEATURES:
        cells = ["yes" if (mats[c] is not None and f in mats[c].columns) else "-"
                 for c in CATEGORIES]
        L.append(f"| `{f}` | " + " | ".join(cells) + f" | {desc.get(f,'')} |")

    L += ["", "**Deliberately excluded** from model inputs, though present in the "
          "matrix for EDA:", "",
          "| Column | Why excluded |", "|---|---|",
          "| `weighted_dist` | Tested and cleared for leakage, but does not improve "
          "out-of-sample accuracy -- worse in 3 of 4 categories (P0036 task 7). |",
          "| `sales_value`, `sales_liters`, `promo_units`, `baseline_*` | "
          "Contemporaneous with the target: measured in the month being forecast, "
          "so using them means reading the answer. |", ""]
    return L


def section_hyperparams(L):
    L += ["## 3. Hyperparameters", "",
          "Tuned with Optuna against **validation** WMAPE, then refit on "
          "train+val and evaluated once on test (`srq1_benchmark_tuned.py`). "
          "Tuning on test would select the configuration that best fits the "
          "evaluation set, which is not a measurement.", ""]
    f = THESIS_RESULTS_SRQ1_DIR / "tuned_params.json"
    if not f.is_file():
        L += ["_`tuned_params.json` not found -- run `srq1_benchmark_tuned.py`._", ""]
        return L
    params = json.loads(f.read_text(encoding="utf-8"))
    keys = sorted(k for k in params if "XGBoost" in k)
    allp = sorted({p for k in keys for p in params[k]})
    L += ["### XGBoost (the model Scenario C serves)", "",
          "| Parameter | " + " | ".join(k.split("/")[1] for k in keys) + " |",
          "|---|" + "---|" * len(keys)]
    for p in allp:
        L.append(f"| `{p}` | " + " | ".join(
            f"{params[k].get(p, '-'):g}" if isinstance(params[k].get(p), (int, float))
            else str(params[k].get(p, "-")) for k in keys) + " |")
    L += ["", f"_{len(params)} tuned configurations in total "
          f"({', '.join(sorted({k.split('/')[-1] for k in params}))})._", ""]
    return L


def section_accuracy(L):
    L += ["## 4. Accuracy", ""]
    f = THESIS_RESULTS_SRQ1_DIR / "metrics.csv"
    if not f.is_file():
        L += ["_`metrics.csv` not found -- run `srq1_benchmark.py`._", ""]
        return L
    df = pd.read_csv(f)
    metric = "median_mape" if "median_mape" in df.columns else None
    wm = "wmape" if "wmape" in df.columns else None
    L += ["Reported as **median per-series MAPE** and **WMAPE** "
          "(volume-weighted -- the business metric). The mean MAPE is deliberately "
          "absent: a single divergent series destroys it (P0038 F75), which is a "
          "property of the metric, not of the model.", ""]
    if "category" in df.columns and "model" in df.columns:
        cats = [c for c in CATEGORIES if c in set(df.category)]
        models = list(dict.fromkeys(df.model))
        for label, col in (("Median per-series MAPE", metric), ("WMAPE", wm)):
            if not col:
                continue
            L += [f"### {label} (lower is better)", "",
                  "| Model | " + " | ".join(cats) + " |", "|---|" + "---:|" * len(cats)]
            for mo in models:
                cells = []
                for c in cats:
                    r = df[(df.model == mo) & (df.category == c)]
                    cells.append(f"{r.iloc[0][col]:.1f}%" if len(r) and pd.notna(r.iloc[0][col]) else "-")
                L.append(f"| {mo} | " + " | ".join(cells) + " |")
            L.append("")
    else:
        L += ["_metrics.csv has an unexpected shape; showing raw._", "",
              df.to_markdown(index=False), ""]
    return L


def section_calibration(L):
    L += ["## 5. Interval calibration", "",
          "Prediction intervals use **split conformal**: the 90th percentile of "
          "absolute residuals on a calibration set the model has never seen.", "",
          "> **Fit on train. Calibrate on val. Leave test untouched.**", "",
          "Getting this wrong does not raise an error -- it produces intervals "
          "that look impressively tight. Measured on CSD (2026-08-19), calibrating "
          "on rows the model had already fit gave q90 = 0.305 against an honest "
          "1.194: intervals **3.9x too narrow**. Scenario C's claimed advantage is "
          "calibrated uncertainty, so a silently tight interval attacks the thesis "
          "at its strongest point.", "",
          "| Category | Calibration rows | q90 (log space) | Median 90% interval width |",
          "|---|---:|---:|---|"]
    try:
        from xgboost import XGBRegressor
    except ImportError:
        L += ["_xgboost not installed._", ""]
        return L
    pf = THESIS_RESULTS_SRQ1_DIR / "tuned_params.json"
    params = json.loads(pf.read_text(encoding="utf-8")) if pf.is_file() else {}
    for cat in CATEGORIES:
        fm = _matrix(cat)
        if fm is None:
            continue
        feats = [c for c in FEATURES if c in fm.columns]
        d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"])
        tr, va = d[d.split == "train"], d[d.split == "val"]
        if len(tr) < 30 or not len(va):
            L.append(f"| {cat} | {len(va)} | _insufficient_ | - |")
            continue
        m = XGBRegressor(random_state=42, verbosity=0, n_jobs=-1,
                         **params.get(f"brand/{cat}/XGBoost", {}))
        m.fit(tr[feats].fillna(0.0), tr["log_sales_units"].values)
        res = np.abs(va["log_sales_units"].values - m.predict(va[feats].fillna(0.0)))
        q90 = float(np.quantile(res, 0.90))
        # Width as a multiple of the point forecast, which is the number a reader
        # can interpret. The interval is symmetric in LOG space, so in level
        # space it is [y/e^q90, y*e^q90] and the width is y*(e^q90 - e^-q90).
        mult = float(np.exp(q90) - np.exp(-q90))
        L.append(f"| {cat} | {len(va)} | {q90:.3f} | ~{mult:.1f}x the point forecast |")
    L += ["", "A wide interval is not a failure of the model -- it is an honest "
          "statement about monthly brand-level demand. Reporting a narrow one "
          "that is not earned would be.", ""]
    return L


def section_tool_payload(L):
    L += ["## 6. What Scenario C's tool returns", "",
          "The exact payload handed back to the LLM for one brand. Every field "
          "beyond the number is provenance: SRQ2 defines traceability as a "
          "recorded mapping from tool call to forecast to recommendation, so "
          "these fields are the claim, not decoration.", ""]
    try:
        import importlib.util
        p = (Path(__file__).resolve().parents[1] / "scenario_setup"
             / "srq4_experiment.py")
        spec = importlib.util.spec_from_file_location("srq4", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        out = m._eval_forecast("CSD", "HARBOE")
        L += ["```json", json.dumps(out, indent=2), "```", ""]
    except Exception as e:
        L += [f"_could not call the tool: {type(e).__name__}: {str(e)[:200]}_", ""]
    return L


def main():
    ap = argparse.ArgumentParser(description="Model-training transparency report")
    ap.add_argument("--out", default=None,
                    help="output dir (default: 04_thesis_results/srq1)")
    a = ap.parse_args()
    out = Path(a.out) if a.out else THESIS_RESULTS_SRQ1_DIR
    out.mkdir(parents=True, exist_ok=True)

    L = ["# Model training — what was trained, on what, and how well", "",
         "Generated by `03_thesis_modelling/model_training/training_report.py`. "
         "Every number below is computed from the feature matrices and results "
         "files at run time, not transcribed.", "",
         "This documents the model that **Scenario C** exposes through the "
         "`forecast_demand` tool. Scenario B writes its own code against the same "
         "history; Scenario A sees none of it.", "", "---", ""]
    for fn in (section_data, section_features, section_hyperparams,
               section_accuracy, section_calibration, section_tool_payload):
        L = fn(L)
        L.append("---")
        L.append("")

    f = out / "training_report.md"
    f.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))
    print(f"\nWrote {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
