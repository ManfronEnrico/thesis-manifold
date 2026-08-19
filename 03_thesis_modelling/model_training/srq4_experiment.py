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

Keys are read from 03_thesis_modelling/.env, falling back to the repo-root .env.
ANTHROPIC_API_KEY is needed by both systems; E2B_API_KEY only by System B.
Reproducible. No live RU warehouse access required.
Usage: python 03_thesis_modelling/model_training/srq4_experiment.py --demo
"""
import argparse, json, os, re, sys, time, warnings
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_SRQ1_DIR, THESIS_RESULTS_SRQ4_DIR, get_category_engineered_bymonth_dir

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[2]

# Keys are read from the modelling-layer .env first, then the repo-root .env.
# Both are gitignored. setdefault means an already-exported environment variable
# always wins, and the first file to define a key wins over the second.
# Neither file is required to exist: a missing key surfaces at the point of use
# as an SDK auth error naming the key, which is more useful than a
# FileNotFoundError on import that blocks even the parts needing no credentials.
for _env in (ROOT / ".env", REPO_ROOT / ".env"):
    if not _env.is_file():
        continue
    for line in _env.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, _, v = line.partition("=")
            # An empty value is a placeholder, not a credential. Setting it would
            # shadow a real exported variable and turn a clear auth error into a
            # confusing one -- the repo-root .env declares an empty
            # ANTHROPIC_API_KEY exactly like this.
            if v.strip():
                os.environ.setdefault(k.strip(), v.strip())

import importlib.util
# forecast_service.py lives in model_serving/, not beside this file: the P0028
# restructure split train-vs-serve and this path was never updated. Loaded by
# explicit path because 03_thesis_modelling/ has no __init__.py, so it is not
# an importable package.
_FS_PATH = ROOT / "model_serving" / "system_a_forecast" / "forecast_service.py"
if not _FS_PATH.is_file():
    raise FileNotFoundError(f"System A's backing service is missing: {_FS_PATH}")
_spec = importlib.util.spec_from_file_location("fs", _FS_PATH)
fs = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(fs)

MODEL = "claude-sonnet-4-6"
# USD per 1M tokens. MUST be updated together with MODEL above -- the cost
# column in every SRQ4 result table is computed from these two constants, so a
# vendor switch without updating them reports the old vendor's prices against
# the new vendor's token counts (P0039 F7).
PRICE_IN_PER_M, PRICE_OUT_PER_M = 3.00, 15.00  # claude-sonnet-4-6 (verified 2026-07-01)


def _cost_usd(tok_in, tok_out):
    return round((tok_in or 0) * PRICE_IN_PER_M / 1e6 + (tok_out or 0) * PRICE_OUT_PER_M / 1e6, 4)
# GRAIN (P0035, 2026-08-01): DEC-GRAIN (2026-07-12) locked the thesis to
# brand x month. danskvand was previously pinned to the 'bychain' grain here;
# its data directory is deleted, so it now reads brand x month like every other
# category. Tag kept in the tuple shape so a future grain can be reintroduced.
# Tag value "bymonth" selects the PATHS.py helper, not a literal path segment.
CAT_FILE = {"CSD": ("csd", "bymonth", "CSD"),
            "danskvand": ("danskvand", "bymonth", "danskvand"),
            "energidrikke": ("energidrikke", "bymonth", "energidrikke"),
            "RTD": ("rtd", "bymonth", "RTD")}


def _engineered_dir(tag, sub):
    return get_category_engineered_bymonth_dir(sub)


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



def _brand_history(category, brand):
    """Monthly observed series for a brand (train+val), and the test actual (next month)."""
    slug, tag, sub = CAT_FILE[category]
    fm = pd.read_parquet(_engineered_dir(tag, sub) / f"{slug}_feature_matrix_h3.parquet")
    g = fm[(fm.brand.str.upper() == brand.upper())].sort_values("period_index")
    test = g[g.split == "test"].dropna(subset=["sales_units"])
    actual = float(test.iloc[0]["sales_units"]) if len(test) else None
    cols = ["period_year", "period_month", "sales_units"] + [
        c for c in ("promo_intensity", "weighted_distribution") if c in g.columns]
    fit = g[g.split.isin(["train", "val"])].dropna(subset=["sales_units"])[cols]
    return fit, actual


def _eval_forecast(category, brand):
    """System A's tool, EVALUATION mode: train tuned XGBoost on train+val only and
    predict the FIRST test month — same target/data as System B, for a fair comparison."""
    import json as _json
    from xgboost import XGBRegressor
    slug, tag, sub = CAT_FILE[category]
    params = _json.loads((THESIS_RESULTS_SRQ1_DIR / "tuned_params.json").read_text())
    pk = "brand"
    fm = pd.read_parquet(_engineered_dir(tag, sub) / f"{slug}_feature_matrix_h3.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"])
    trval = d[d.split.isin(["train", "val"])]
    m = XGBRegressor(random_state=42, verbosity=0, n_jobs=-1, **params.get(f"{pk}/{category}/XGBoost", {}))
    m.fit(trval[available_features(fm)].fillna(0.0), trval["log_sales_units"].values)
    te = d[d.split == "test"]
    res = np.abs(d[d.split == "val"]["log_sales_units"].values - m.predict(d[d.split == "val"][available_features(fm)].fillna(0.0)))
    q90 = float(np.quantile(res, 0.90)) if len(res) else 0.5
    row = te[te.brand.str.upper() == brand.upper()].sort_values("period_index").head(1)
    if not len(row):
        return {"status": "not_found", "brand": brand}
    yhat = float(np.clip(np.expm1(m.predict(row[available_features(fm)].fillna(0.0))[0]), 0, None))
    lo, hi = float(np.expm1(np.log(max(yhat, 1e-9)) - q90)), float(np.expm1(np.log(max(yhat, 1e-9)) + q90))
    return {"status": "ok", "category": category, "brand": brand,
            "forecast_units": round(yhat, 1), "interval_90": [round(lo, 1), round(hi, 1)],
            "model": "XGBoost(tuned)", "horizon": "next (held-out) month"}


# ---------------------------------------------------------------------------
# System A — dedicated-model tool (Claude function-calling)
# ---------------------------------------------------------------------------
def run_system_a(category, brand, question=None):
    import anthropic
    c = anthropic.Anthropic()
    tools = [{
        "name": "forecast_demand",
        "description": "Return next-month demand forecast for a brand from the dedicated pre-trained model (point, 90% interval, confidence tier). Use for any forecast question; do not compute yourself.",
        "input_schema": {"type": "object", "properties": {
            "category": {"type": "string"}, "brand": {"type": "string"}},
            "required": ["category", "brand"]},
    }]
    msgs = [{"role": "user", "content": question or f"What will {brand} sell next month in the {category} category? Give the number, range and confidence."}]
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
def run_system_b(category, brand, question=None, sentinel="FORECAST"):
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
        "description": "Run Python in a sandbox where `df` is the brand's monthly history (period_year, period_month, sales_units and, when available, promo_intensity and weighted_distribution). Available: pandas, numpy, scipy, scikit-learn, statsmodels. Use them to answer the forecasting question. print() your result.",
        "input_schema": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]},
    }]
    task = question or f"Forecast next month's sales_units for {brand} in {category}."
    msgs = [{"role": "user", "content": f"{task} Write and run your own forecasting code on `df` in the sandbox. When done, run one final cell that prints exactly `{sentinel}=<number>`, then give a one-line summary with a range."}]
    t0 = time.perf_counter(); tok_in = tok_out = 0; printed = None
    for _ in range(8):
        r = c.messages.create(model=MODEL, max_tokens=1500, temperature=0, tools=tools, messages=msgs)
        tok_in += r.usage.input_tokens; tok_out += r.usage.output_tokens
        if r.stop_reason == "tool_use":
            tu = next(b for b in r.content if b.type == "tool_use")
            ex = sbx.run_code(tu.input.get("code", ""))
            out = (ex.logs.stdout and "".join(ex.logs.stdout)) or (ex.error and str(ex.error)) or "(no output)"
            mm = re.findall(rf"{sentinel}=([\d\.,]+)", out)
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


def _tar(vals, tol=0.01):
    """Total agreement rate (Atil et al., 2025): largest fraction of the N repeated
    answers that agree with each other within `tol` relative tolerance."""
    v = [float(x) for x in vals if x is not None and not (isinstance(x, float) and np.isnan(x))]
    if not v:
        return np.nan
    best = 0
    for x in v:
        n = sum(1 for y in v if abs(y - x) <= tol * max(abs(x), 1e-9))
        best = max(best, n)
    return best / len(v)


def _select_brands(per_cat=(4, 4, 4, 3)):
    """Top brands by volume that have a held-out test actual, balanced across categories."""
    picks = []
    for (cat, (slug, tag, sub)), k in zip(CAT_FILE.items(), per_cat):
        fm = pd.read_parquet(_engineered_dir(tag, sub) / f"{slug}_feature_matrix_h3.parquet")
        has_test = set(fm[fm.split == "test"].dropna(subset=["sales_units"]).brand.str.upper())
        vol = (fm.dropna(subset=["sales_units"]).groupby("brand").sales_units.sum().sort_values(ascending=False))
        chosen = [b for b in vol.index if str(b).upper() in has_test][:k]
        picks += [(cat, b) for b in chosen]
    return picks


def run_full(repeats=5):
    OUT = THESIS_RESULTS_SRQ4_DIR; OUT.mkdir(parents=True, exist_ok=True)
    brands = _select_brands()
    print(f"Running SRQ4 full experiment: {len(brands)} brands x {repeats} repeats x 2 systems\n")
    rows = []
    for cat, brand in brands:
        _, actual = _brand_history(cat, brand)
        if not actual:
            continue
        for sysname, fn in [("A_dedicated", run_system_a), ("B_codeaction", run_system_b)]:
            for rep in range(repeats):
                try:
                    r = fn(cat, brand)
                except Exception as e:
                    r = {"forecast": None, "latency_s": None, "tokens_in": None, "tokens_out": None, "answer": str(e)[:100]}
                ape = (abs(r["forecast"] - actual) / actual * 100) if r.get("forecast") else None
                rows.append(dict(category=cat, brand=brand, system=sysname, rep=rep, actual=actual,
                                 forecast=r.get("forecast"), ape=ape, latency_s=r.get("latency_s"),
                                 tokens_in=r.get("tokens_in") or 0, tokens_out=r.get("tokens_out") or 0,
                                 tokens=(r.get("tokens_in") or 0) + (r.get("tokens_out") or 0),
                                 cost_usd=_cost_usd(r.get("tokens_in"), r.get("tokens_out"))))
                print(f"  {cat:12s} {str(brand)[:16]:16s} {sysname:13s} rep{rep} "
                      f"fc={r.get('forecast')} ape={ape if ape is None else round(ape,1)} "
                      f"lat={r.get('latency_s')} tok={(r.get('tokens_in') or 0)+(r.get('tokens_out') or 0)}")
        pd.DataFrame(rows).to_csv(OUT / "runs.csv", index=False)  # checkpoint after each brand

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "runs.csv", index=False)
    # aggregate the 5 SRQ4 metrics per system
    lines = ["# SRQ4 experiment — dedicated-model tool (A) vs code-as-action (B)", "",
             f"{len(brands)} brands x {repeats} repeats x 2 systems, claude-sonnet-4-6 temp 0, "
             "forecasting the held-out test month from train+val. Metrics:", "",
             "| Metric | System A (dedicated) | System B (code-as-action) |", "|---|---|---|"]
    agg = {}
    for sysname in ["A_dedicated", "B_codeaction"]:
        s = df[df.system == sysname]
        ok = s.dropna(subset=["forecast"])
        # consistency: per-brand coefficient of variation of the repeated forecasts
        cv = ok.groupby("brand").forecast.apply(lambda x: x.std() / x.mean() if x.mean() else np.nan)
        # replicability: fraction of brands whose repeated forecasts are all (near-)identical
        rep_ok = ok.groupby("brand").forecast.apply(lambda x: (x.max() - x.min()) / max(x.mean(), 1e-9) < 0.01)
        tar = ok.groupby("brand").forecast.apply(lambda x: _tar(list(x)))
        agg[sysname] = dict(
            correctness=ok.ape.mean(), consistency=cv.mean() * 100,
            replicability=rep_ok.mean() * 100 if len(rep_ok) else np.nan,
            tar=tar.mean(),
            tokens=s.tokens.mean(), latency=s.latency_s.mean(),
            cost=s.cost_usd.mean(), total_cost=s.cost_usd.sum(),
            failures=int(s.forecast.isna().sum()))
    A, B = agg["A_dedicated"], agg["B_codeaction"]
    lines += [
        f"| Correctness — mean APE (lower=better) | {A['correctness']:.1f}% | {B['correctness']:.1f}% |",
        f"| Consistency — mean CV across repeats (lower=better) | {A['consistency']:.1f}% | {B['consistency']:.1f}% |",
        f"| Replicability — % brands identical across repeats | {A['replicability']:.0f}% | {B['replicability']:.0f}% |",
        f"| Replicability — TAR@N, 1% tol (Atil et al., 2025) | {A['tar']:.2f} | {B['tar']:.2f} |",
        f"| Cost — mean tokens/answer (lower=better) | {A['tokens']:.0f} | {B['tokens']:.0f} |",
        f"| Cost — mean USD/answer | ${A['cost']:.4f} | ${B['cost']:.4f} |",
        f"| Cost — total USD this run | ${A['total_cost']:.2f} | ${B['total_cost']:.2f} |",
        f"| Latency — mean seconds (lower=better) | {A['latency']:.1f} | {B['latency']:.1f} |",
        f"| Failures (no answer) | {A['failures']} | {B['failures']} |", ""]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("\n" + "\n".join(lines))
    print(f"\nSaved runs.csv + summary.md in {OUT}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--demo", action="store_true")
    ap.add_argument("--full", action="store_true"); ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--category", default="CSD"); ap.add_argument("--brand", default="HARBOE")
    a = ap.parse_args()
    if a.full:
        run_full(a.repeats); return
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
