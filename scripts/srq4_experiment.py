#!/usr/bin/env python3
"""
SRQ4 experiment harness — dedicated-model tool (System A) vs code-as-action (System B).

The single variable under test: HOW the agent produces a forecast.
- System A (Oracle): Claude calls a `forecast_demand` tool backed by the pre-trained
  XGBoost model (scripts/forecast_service.py). No code written.
- System B (Prometheus-style): Claude is given the brand's monthly history in an E2B
  sandbox and must WRITE + RUN its own forecasting code to answer (code-as-action).

Both use the same model (claude-sonnet-4-6, temp 0) and the same prompts. We record
the numeric forecast, token cost, and latency; correctness is scored against the
held-out actual; consistency is the spread over repeated runs.

Keys from .env (ANTHROPIC_API_KEY, E2B_API_KEY). Reproducible. No live RU warehouse.
Usage: .venv/bin/python scripts/srq4_experiment.py --demo   # one prompt through A and B
"""
import argparse, json, os, re, time, warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
for line in (ROOT / ".env").read_text().splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, _, v = line.partition("="); os.environ.setdefault(k.strip(), v.strip())

import importlib.util
_spec = importlib.util.spec_from_file_location("fs", ROOT / "scripts" / "forecast_service.py")
fs = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(fs)

MODEL = "claude-sonnet-4-6"
CAT_FILE = {"CSD": ("csd", "_03_engineered_dvhexclhd", "CSD"),
            "danskvand": ("danskvand", "_04_engineered_bychain", "danskvand"),
            "energidrikke": ("energidrikke", "_03_engineered_dvhexclhd", "energidrikke"),
            "RTD": ("rtd", "_03_engineered_dvhexclhd", "RTD")}


FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "holiday_month", "promo_intensity", "weighted_distribution"]


def _brand_history(category, brand):
    """Monthly observed series for a brand (train+val), and the test actual (next month)."""
    slug, tag, sub = CAT_FILE[category]
    fm = pd.read_parquet(ROOT / f"thesis/data/{tag}/{sub}/{slug}_feature_matrix.parquet")
    g = fm[(fm.brand.str.upper() == brand.upper())].sort_values("period_index")
    test = g[g.split == "test"].dropna(subset=["sales_units"])
    actual = float(test.iloc[0]["sales_units"]) if len(test) else None
    fit = g[g.split.isin(["train", "val"])].dropna(subset=["sales_units"])[["period_year", "period_month", "sales_units"]]
    return fit, actual


def _eval_forecast(category, brand):
    """System A's tool, EVALUATION mode: train tuned XGBoost on train+val only and
    predict the FIRST test month — same target/data as System B, for a fair comparison."""
    import json as _json
    from xgboost import XGBRegressor
    slug, tag, sub = CAT_FILE[category]
    params = _json.loads((ROOT / "thesis/data/_05_results_srq1/tuned_params.json").read_text())
    pk = "bychain" if "chain" in tag else "brand"
    fm = pd.read_parquet(ROOT / f"thesis/data/{tag}/{sub}/{slug}_feature_matrix.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"])
    trval = d[d.split.isin(["train", "val"])]
    m = XGBRegressor(random_state=42, verbosity=0, n_jobs=-1, **params.get(f"{pk}/{category}/XGBoost", {}))
    m.fit(trval[FEATURES].fillna(0.0), trval["log_sales_units"].values)
    te = d[d.split == "test"]
    res = np.abs(d[d.split == "val"]["log_sales_units"].values - m.predict(d[d.split == "val"][FEATURES].fillna(0.0)))
    q90 = float(np.quantile(res, 0.90)) if len(res) else 0.5
    row = te[te.brand.str.upper() == brand.upper()].sort_values("period_index").head(1)
    if not len(row):
        return {"status": "not_found", "brand": brand}
    yhat = float(np.clip(np.expm1(m.predict(row[FEATURES].fillna(0.0))[0]), 0, None))
    lo, hi = float(np.expm1(np.log(max(yhat, 1e-9)) - q90)), float(np.expm1(np.log(max(yhat, 1e-9)) + q90))
    return {"status": "ok", "category": category, "brand": brand,
            "forecast_units": round(yhat, 1), "interval_90": [round(lo, 1), round(hi, 1)],
            "model": "XGBoost(tuned)", "horizon": "next (held-out) month"}


# ---------------------------------------------------------------------------
# System A — dedicated-model tool (Claude function-calling)
# ---------------------------------------------------------------------------
def run_system_a(category, brand):
    import anthropic
    c = anthropic.Anthropic()
    tools = [{
        "name": "forecast_demand",
        "description": "Return next-month demand forecast for a brand from the dedicated pre-trained model (point, 90% interval, confidence tier). Use for any forecast question; do not compute yourself.",
        "input_schema": {"type": "object", "properties": {
            "category": {"type": "string"}, "brand": {"type": "string"}},
            "required": ["category", "brand"]},
    }]
    msgs = [{"role": "user", "content": f"What will {brand} sell next month in the {category} category? Give the number, range and confidence."}]
    t0 = time.perf_counter(); tok_in = tok_out = 0; tool_forecast = None
    for _ in range(4):
        r = c.messages.create(model=MODEL, max_tokens=500, temperature=0, tools=tools, messages=msgs)
        tok_in += r.usage.input_tokens; tok_out += r.usage.output_tokens
        if r.stop_reason == "tool_use":
            tu = next(b for b in r.content if b.type == "tool_use")
            out = _eval_forecast(tu.input.get("category", category), tu.input.get("brand", brand))
            tool_forecast = out.get("forecast_units")  # authoritative model forecast
            msgs += [{"role": "assistant", "content": r.content},
                     {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tu.id, "content": json.dumps(out, default=str)}]}]
            continue
        text = "".join(b.text for b in r.content if b.type == "text")
        return {"answer": text, "latency_s": round(time.perf_counter() - t0, 2),
                "tokens_in": tok_in, "tokens_out": tok_out, "forecast": tool_forecast}
    return {"answer": "(no final answer)", "latency_s": round(time.perf_counter() - t0, 2),
            "tokens_in": tok_in, "tokens_out": tok_out, "forecast": tool_forecast}


# ---------------------------------------------------------------------------
# System B — code-as-action (Claude writes + runs code in E2B sandbox)
# ---------------------------------------------------------------------------
def run_system_b(category, brand):
    import anthropic
    from e2b_code_interpreter import Sandbox
    fit, _ = _brand_history(category, brand)
    sbx = Sandbox.create()
    # give the code-as-action agent a fair toolkit (statsmodels is not preinstalled)
    sbx.run_code("import subprocess,sys; subprocess.run([sys.executable,'-m','pip','install','-q','statsmodels'])")
    # pre-load the brand's monthly history into the sandbox as `df` (mirrors Prometheus run_sql)
    csv = fit.to_csv(index=False)
    sbx.run_code("import pandas as pd, io\n_csv='''" + csv + "'''\ndf=pd.read_csv(io.StringIO(_csv))\nprint('df loaded', df.shape)")
    c = anthropic.Anthropic()
    tools = [{
        "name": "run_python",
        "description": "Run Python in a sandbox where `df` (columns period_year, period_month, sales_units) is the brand's monthly history. Available: pandas, numpy, scipy, scikit-learn, statsmodels. Use them to FORECAST next month's sales_units. print() your result.",
        "input_schema": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]},
    }]
    msgs = [{"role": "user", "content": f"Forecast next month's sales_units for {brand} in {category}. Write and run your own forecasting code on `df` in the sandbox. When done, run one final cell that prints exactly `FORECAST=<number>` (the point forecast in units), then give a one-line summary with a range."}]
    t0 = time.perf_counter(); tok_in = tok_out = 0; printed = None
    for _ in range(8):
        r = c.messages.create(model=MODEL, max_tokens=1500, temperature=0, tools=tools, messages=msgs)
        tok_in += r.usage.input_tokens; tok_out += r.usage.output_tokens
        if r.stop_reason == "tool_use":
            tu = next(b for b in r.content if b.type == "tool_use")
            ex = sbx.run_code(tu.input.get("code", ""))
            out = (ex.logs.stdout and "".join(ex.logs.stdout)) or (ex.error and str(ex.error)) or "(no output)"
            mm = re.findall(r"FORECAST=([\d\.,]+)", out)
            if mm:
                try: printed = float(mm[-1].replace(",", ""))
                except Exception: pass
            msgs += [{"role": "assistant", "content": r.content},
                     {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tu.id, "content": out[:3000]}]}]
            continue
        text = "".join(b.text for b in r.content if b.type == "text")
        sbx.kill()
        return {"answer": text, "latency_s": round(time.perf_counter() - t0, 2),
                "tokens_in": tok_in, "tokens_out": tok_out, "forecast": printed if printed is not None else _extract_number(text)}
    sbx.kill()
    return {"answer": "(loop limit)", "latency_s": round(time.perf_counter() - t0, 2),
            "tokens_in": tok_in, "tokens_out": tok_out, "forecast": printed}


def _extract_number(text):
    nums = re.findall(r"[\d][\d,\.]{2,}", text.replace(" ", ""))
    vals = []
    for n in nums:
        try: vals.append(float(n.replace(",", "")))
        except Exception: pass
    return max(vals) if vals else None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--demo", action="store_true")
    ap.add_argument("--category", default="CSD"); ap.add_argument("--brand", default="HARBOE")
    a = ap.parse_args()
    _, actual = _brand_history(a.category, a.brand)
    print(f"=== SRQ4 demo: {a.brand} / {a.category} (actual next month = {actual:,.0f}) ===\n")
    print(">>> System A (dedicated-model tool)")
    A = run_system_a(a.category, a.brand)
    print(f"  forecast={A['forecast']}  latency={A['latency_s']}s  tokens={A['tokens_in']}+{A['tokens_out']}")
    print(f"  answer: {A['answer'][:240]}\n")
    print(">>> System B (code-as-action)")
    B = run_system_b(a.category, a.brand)
    print(f"  forecast={B['forecast']}  latency={B['latency_s']}s  tokens={B['tokens_in']}+{B['tokens_out']}")
    print(f"  answer: {B['answer'][:240]}")
    if actual and A['forecast'] and B['forecast']:
        print(f"\n  APE  System A = {abs(A['forecast']-actual)/actual*100:.1f}%   System B = {abs(B['forecast']-actual)/actual*100:.1f}%")


if __name__ == "__main__":
    main()
