#!/usr/bin/env python3
"""
SRQ4 experiment harness — does model availability improve an LLM's forecasts?

Three arms forming an INFORMATION LADDER (B-DEC-5, 2026-08-19). Each adds one
thing to the arm below it, so the two increments can be attributed separately:

  C_nodata      no firm data; web search only. Not a null condition -- it finds
                annual reports and market commentary and answers confidently.
  B_codeaction  the brand history in a hosted Code Interpreter sandbox; the LLM
                writes and runs its own forecasting code.
  A_dedicated   the same data behind a `forecast_demand` tool backed by the
                pre-trained XGBoost. The LLM writes no code.

  C -> B  measures what DATA ACCESS buys.
  B -> A  measures what MODEL INTEGRATION adds on top -- the thesis contribution.

A two-arm A-vs-B design conflates these, and a reviewer could then argue the
whole effect is just data access.

All arms run the SAME model, temperature and reasoning effort: the design
isolates how the forecast is produced, so any other difference would measure LLM
quality instead of the intervention.

Outcomes are classified (ok / code_error / no_forecast / timeout / implausible)
rather than averaged. Failures are findings: "code-as-action failed 12% of the
time" says more about production readiness than a small accuracy gap.

Keys are read from 03_thesis_modelling/.env, falling back to the repo-root .env:
  OPENAI_API_KEY    project key   -- inference (all arms)
  OPENAI_ADMIN_KEY  admin key     -- billing reconciliation (optional)
The two scopes are disjoint; the project key returns 403 on the costs endpoint.

Usage:
  python 03_thesis_modelling/model_training/srq4_experiment.py --demo
  python 03_thesis_modelling/model_training/srq4_experiment.py --demo --arms A,B
  python 03_thesis_modelling/model_training/srq4_experiment.py --full --repeats 5
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

# The .env stores these under their OpenAI dashboard labels rather than the
# names the SDK and the costs endpoint expect. Map them, without clobbering a
# value already exported in the real environment.
#   thesis_manifold_prompts       -> OPENAI_API_KEY   (project key: inference)
#   thesis_manifold_prompts_admin -> OPENAI_ADMIN_KEY (admin key: billing)
# The two scopes are disjoint -- the project key returns 403 on
# /v1/organization/costs and the admin key returns 403 on /v1/models -- so both
# are required: one to run the experiment, one to price it.
for _src, _dst in (("thesis_manifold_prompts", "OPENAI_API_KEY"),
                   ("thesis_manifold_prompts_admin", "OPENAI_ADMIN_KEY")):
    if os.environ.get(_src) and not os.environ.get(_dst):
        os.environ[_dst] = os.environ[_src]

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

# ---------------------------------------------------------------------------
# Model + pricing (DEC-LLM 2026-07-12, confirmed B-DEC-1 2026-08-19)
# ---------------------------------------------------------------------------
# All three arms MUST run the same model: the design isolates a single variable
# (how the forecast is produced), so a model that differs between arms measures
# LLM quality instead of the intervention.
#
# Pinned to the DATED SNAPSHOT, not the floating "gpt-5.5" alias -- an alias
# silently re-points and would break reproducibility mid-study.
MODEL = "gpt-5.5-2026-04-23"

# Free parameters that change cost and behaviour and default silently. Frozen
# here so they are reported rather than inherited (B-DEC-1).
REASONING_EFFORT = "medium"   # API default; stated explicitly because reasoning
                              # tokens are billed at the OUTPUT rate and in
                              # testing were the majority of output.

# DECODING IS NOT CONTROLLABLE ON THIS MODEL (verified 2026-08-19).
# gpt-5.5 rejects BOTH `temperature` and `top_p` with HTTP 400
# ("Unsupported parameter"). The original protocol specified temperature 0 as
# the decoding control across arms; that is not available on a reasoning model.
#
# This does NOT break the comparison -- all three arms are equally uncontrolled,
# so decoding is held constant across arms in the only sense the API permits.
# What it changes is the WRITE-UP: run-to-run consistency is a purely measured
# outcome, and cannot be described as "despite temperature 0". Reporting
# temperature 0 in the methodology would be false.
TEMPERATURE = None            # not settable; recorded as such in every trace
DECODING_NOTE = "temperature/top_p unsupported by the model; defaults used"

# USD per 1M tokens. Verified against actual billing 2026-08-19: the output rate
# backs out at ~$30.4/1M from /v1/organization/costs, matching the published $30.
# These drive the per-run ESTIMATE only; the reported figure is reconciled
# against the billing export (see fetch_billed_cost).
PRICE_IN_PER_M, PRICE_OUT_PER_M = 5.00, 30.00
PRICE_CACHED_IN_PER_M = 0.50

# Code Interpreter container, 1 GB tier (the default when no memory_limit is
# given). Published per 20-minute session, billed by the minute with a 5-minute
# minimum. The API does NOT report container duration or charge -- only a
# container_id -- so this is necessarily an estimate. Arm B alone incurs it.
PRICE_CONTAINER_SESSION = 0.03


def _cost_usd(tok_in, tok_out, cached_in=0, containers=0):
    """Per-run cost ESTIMATE in USD.

    Token cost is exact; the container component is not, because the Responses
    API exposes no duration or charge for code_interpreter. Reconcile against
    fetch_billed_cost() before reporting any total."""
    billable_in = max((tok_in or 0) - (cached_in or 0), 0)
    return round(
        billable_in * PRICE_IN_PER_M / 1e6
        + (cached_in or 0) * PRICE_CACHED_IN_PER_M / 1e6
        + (tok_out or 0) * PRICE_OUT_PER_M / 1e6
        + (containers or 0) * PRICE_CONTAINER_SESSION,
        6,
    )


def fetch_billed_cost(start_time, end_time=None):
    """Actual billed USD from the org costs endpoint, grouped by line item.

    Requires an ADMIN-scoped key (OPENAI_ADMIN_KEY); the project key returns 403.
    This is the ground truth that _cost_usd only estimates -- in particular it is
    the only way to see the code_interpreter container charge."""
    import urllib.request
    key = os.environ.get("OPENAI_ADMIN_KEY")
    if not key:
        return None
    url = (f"https://api.openai.com/v1/organization/costs"
           f"?start_time={int(start_time)}&limit=31&group_by=line_item")
    if end_time:
        url += f"&end_time={int(end_time)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    items = {}
    for bucket in data.get("data", []):
        for res in bucket.get("results", []):
            items[res.get("line_item") or "unknown"] = round(
                items.get(res.get("line_item") or "unknown", 0.0)
                + res["amount"]["value"], 6)
    return {"total_usd": round(sum(items.values()), 6), "line_items": items}


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
# Shared OpenAI plumbing
# ---------------------------------------------------------------------------
# All three arms go through _usage() so token accounting is identical across
# them. Any per-arm difference in how cost is measured would confound the cost
# comparison, which B-DEC-6 promoted to a primary outcome.
FAILURE_CLASSES = ("ok", "code_error", "no_forecast", "timeout", "implausible")


def _client():
    from openai import OpenAI
    return OpenAI()


def _usage(r, containers=0):
    """Extract the token counts every arm reports. `reasoning_tokens` is broken
    out because it is billed at the OUTPUT rate while being invisible in the
    answer -- in testing it was the majority of output tokens."""
    u = r.usage
    cached = getattr(getattr(u, "input_tokens_details", None), "cached_tokens", 0) or 0
    reasoning = getattr(getattr(u, "output_tokens_details", None), "reasoning_tokens", 0) or 0
    return {
        "tokens_in": u.input_tokens,
        "tokens_out": u.output_tokens,
        "tokens_cached_in": cached,
        "tokens_reasoning": reasoning,
        "containers": containers,
        "cost_usd_est": _cost_usd(u.input_tokens, u.output_tokens, cached, containers),
    }


def _classify(forecast, hit_limit=False, error=None, actual=None):
    """Assign a failure class. These are FINDINGS, not noise (P0039 task 3):
    "code-as-action failed 12% of the time" is a stronger statement about
    production readiness than a small accuracy gap."""
    if error:
        return "code_error"
    if hit_limit:
        return "timeout"
    if forecast is None:
        return "no_forecast"
    # `implausible` exists because of P0038 F72: Prophet forecast 101M against a
    # 301k actual. Averaged in, one such answer destroys a mean; recorded as a
    # class, it is a result.
    if actual and (forecast > actual * 20 or forecast < actual / 20):
        return "implausible"
    return "ok"


def _trace(arm, extra=None):
    """Provenance recorded per run (SRQ2 traceability). Every free parameter that
    changes cost or behaviour is captured, so a result can be tied to exactly the
    configuration that produced it."""
    t = {"arm": arm, "model": MODEL, "temperature": TEMPERATURE,
         "decoding": DECODING_NOTE, "reasoning_effort": REASONING_EFFORT,
         "run_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if extra:
        t.update(extra)
    return t


def _result(arm, text, err, t0, u, forecast, containers=0, hit_limit=False, trace_extra=None):
    """Uniform result record. One shape across all three arms so the results
    writer never has to branch on which arm produced a row."""
    return {"answer": text or (err or "(no output)"),
            "latency_s": round(time.perf_counter() - t0, 2),
            "tokens_in": u["tokens_in"], "tokens_out": u["tokens_out"],
            "tokens_cached_in": u["tokens_cached_in"],
            "tokens_reasoning": u["tokens_reasoning"],
            "containers": containers,
            "cost_usd_est": _cost_usd(u["tokens_in"], u["tokens_out"],
                                      u["tokens_cached_in"], containers),
            "forecast": forecast, "error": err, "hit_limit": hit_limit,
            "trace": _trace(arm, trace_extra)}


_EMPTY_USAGE = {"tokens_in": 0, "tokens_out": 0, "tokens_cached_in": 0, "tokens_reasoning": 0}


def _parse_sentinel(text, sentinel="FORECAST"):
    """Return (value, via_sentinel). Prefers the sentinel line; falls back to a
    bare number so a non-compliant-but-correct answer is not scored as a
    failure. The flag is recorded so prompt non-compliance stays distinguishable
    from forecasting failure."""
    mm = re.findall(rf"{sentinel}\s*=\s*([\d\.,]+)", text or "")
    if mm:
        try:
            return float(mm[-1].replace(",", "")), True
        except Exception:
            pass
    return _extract_number(text or ""), False


# ---------------------------------------------------------------------------
# Arm A -- dedicated-model tool (the thesis artefact)
# ---------------------------------------------------------------------------
def run_system_a(category, brand, question=None):
    """The LLM calls `forecast_demand`, backed by the pre-trained XGBoost. It
    writes no code; the number comes from the dedicated model."""
    c = _client()
    tools = [{
        "type": "function",
        "name": "forecast_demand",
        "description": ("Return next-month demand forecast for a brand from the dedicated "
                        "pre-trained model (point, 90% interval, confidence tier). Use for "
                        "any forecast question; do not compute yourself."),
        "parameters": {"type": "object",
                       "properties": {"category": {"type": "string"},
                                      "brand": {"type": "string"}},
                       "required": ["category", "brand"], "additionalProperties": False},
    }]
    task = question or (f"What will {brand} sell next month in the {category} category? "
                        "Give the number, range and confidence.")
    msgs = [{"role": "user", "content": task}]
    t0 = time.perf_counter()
    tot = dict(_EMPTY_USAGE)
    tool_forecast = None
    err = None
    hit_limit = True
    text = ""
    try:
        for _ in range(4):
            r = c.responses.create(model=MODEL,
                                   reasoning={"effort": REASONING_EFFORT},
                                   tools=tools, input=msgs)
            u = _usage(r)
            for k in tot:
                tot[k] += u[k]
            calls = [it for it in r.output if it.type == "function_call"]
            if calls:
                for call in calls:
                    args = json.loads(call.arguments or "{}")
                    out = _eval_forecast(args.get("category", category),
                                         args.get("brand", brand))
                    # The tool output is authoritative: whatever the LLM then says
                    # in prose, the dedicated model's number is what Arm A is
                    # credited with.
                    if out.get("forecast_units") is not None:
                        tool_forecast = out["forecast_units"]
                    msgs += [{"type": "function_call", "call_id": call.call_id,
                              "name": call.name, "arguments": call.arguments},
                             {"type": "function_call_output", "call_id": call.call_id,
                              "output": json.dumps(out, default=str)}]
                continue
            text = r.output_text
            hit_limit = False
            break
    except Exception as e:
        err = str(e)[:300]

    forecast = tool_forecast if tool_forecast is not None else _extract_number(text)
    return _result("A_dedicated", text, err, t0, tot, forecast,
                   containers=0, hit_limit=hit_limit,
                   trace_extra={"tool": "forecast_demand", "wrote_code": False,
                                "tool_returned_forecast": tool_forecast is not None})


# ---------------------------------------------------------------------------
# Arm B -- code-as-action (the LLM writes and runs its own forecasting code)
# ---------------------------------------------------------------------------
def run_system_b(category, brand, question=None, sentinel="FORECAST"):
    """The LLM gets the brand history and must write + run its own code in the
    hosted Code Interpreter sandbox.

    Code Interpreter, not the hosted shell (B-DEC-6): a shell would grant
    arbitrary terminal access that arms A and C do not have -- a second variable
    moving -- and would let the model work around its own failures, suppressing
    the failure taxonomy that is itself part of the result.

    Each call creates a fresh container (`container: auto`), so no state carries
    between observations."""
    c = _client()
    fit, _ = _brand_history(category, brand)
    csv = fit.to_csv(index=False)
    task = question or f"Forecast next month's sales_units for {brand} in {category}."
    prompt = (
        f"Here is the monthly sales history for brand {brand} in the {category} "
        f"category as CSV:\n\n{csv}\n\n{task}\n\n"
        "Write and run Python code to produce the forecast. pandas, numpy, "
        "scipy, scikit-learn and statsmodels are available.\n\n"
        f"IMPORTANT: your FINAL message must contain the single line "
        f"{sentinel}=<number> with a plain number (no commas, no units), "
        "followed by one line naming your method and a range. Do not end your "
        "reply with code -- end it with that line."
    )
    t0 = time.perf_counter()
    err = None
    text = ""
    ncalls = 0
    u = dict(_EMPTY_USAGE)
    try:
        r = c.responses.create(model=MODEL,
                               reasoning={"effort": REASONING_EFFORT},
                               tools=[{"type": "code_interpreter",
                                       "container": {"type": "auto"}}],
                               input=prompt)
        ncalls = sum(1 for it in r.output if it.type == "code_interpreter_call")
        u = _usage(r, containers=1)
        text = r.output_text
    except Exception as e:
        err = str(e)[:300]

    forecast, via_sentinel = _parse_sentinel(text, sentinel)
    containers = 0 if err else 1
    return _result("B_codeaction", text, err, t0, u, forecast,
                   containers=containers,
                   trace_extra={"tool": "code_interpreter", "wrote_code": True,
                                "code_calls": ncalls, "via_sentinel": via_sentinel})


# ---------------------------------------------------------------------------
# Arm C -- no firm data (the floor, and the first rung of the ladder)
# ---------------------------------------------------------------------------
def run_system_c(category, brand, question=None):
    """The LLM answers with no access to the Nielsen data at all.

    NOT a null condition (B-DEC-5). With web search it will find annual reports,
    market commentary and category coverage, and return a confident number. How
    wrong that number is -- and how confidently wrong -- is the finding, and it
    answers the practitioner question "why not just ask ChatGPT?".

    Documented limitation: because this arm can browse, it is not a clean
    no-information floor. It may encounter genuinely relevant public data. That
    UNDERSTATES the measured value of data access (C->B), so the bias runs
    conservative with respect to our own claim."""
    c = _client()
    task = question or (f"What will the brand {brand} sell next month in the {category} "
                        "category in Danish retail, in units? You have no access to "
                        "internal sales data. Give your best single numeric estimate.")
    prompt = (task + "\n\nEnd your reply with the single line FORECAST=<number> "
              "(a plain number, no commas or units).")
    t0 = time.perf_counter()
    err = None
    text = ""
    u = dict(_EMPTY_USAGE)
    used_web = False
    try:
        r = c.responses.create(model=MODEL,
                               reasoning={"effort": REASONING_EFFORT},
                               tools=[{"type": "web_search"}],
                               input=prompt)
        u = _usage(r, containers=0)
        used_web = any(it.type.startswith("web_search") for it in r.output)
        text = r.output_text
    except Exception as e:
        err = str(e)[:300]

    forecast, via_sentinel = _parse_sentinel(text)
    return _result("C_nodata", text, err, t0, u, forecast, containers=0,
                   trace_extra={"tool": "web_search", "wrote_code": False,
                                "used_web": used_web, "via_sentinel": via_sentinel})


# Arm order is the information ladder (B-DEC-5): C -> B measures what data access
# buys, B -> A measures what model integration adds on top.
ARMS = (("A_dedicated", run_system_a),
        ("B_codeaction", run_system_b),
        ("C_nodata", run_system_c))


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


def run_full(repeats=5, brands_per_cat=(4, 4, 4, 3), arms=None, out_dir=None):
    """Run the experiment and write runs.csv + summary.md.

    Checkpoints after every brand: a crash 40 runs in should not cost the
    completed runs, and a paid experiment is not worth re-running for want of a
    flush."""
    OUT = Path(out_dir) if out_dir else THESIS_RESULTS_SRQ4_DIR
    OUT.mkdir(parents=True, exist_ok=True)
    arms = arms or ARMS
    brands = _select_brands(brands_per_cat)
    t_start = time.time()
    n_total = len(brands) * repeats * len(arms)
    print(f"SRQ4: {len(brands)} brands x {repeats} repeats x {len(arms)} arms "
          f"= {n_total} runs, model={MODEL}\n")

    rows = []
    for cat, brand in brands:
        _, actual = _brand_history(cat, brand)
        if not actual:
            print(f"  skip {cat}/{brand}: no held-out actual")
            continue
        for sysname, fn in arms:
            for rep in range(repeats):
                try:
                    r = fn(cat, brand)
                except Exception as e:
                    r = {"forecast": None, "latency_s": None, "tokens_in": 0,
                         "tokens_out": 0, "tokens_cached_in": 0, "tokens_reasoning": 0,
                         "containers": 0, "cost_usd_est": 0.0, "answer": str(e)[:200],
                         "error": str(e)[:300], "hit_limit": False, "trace": {}}
                fc = r.get("forecast")
                cls = _classify(fc, r.get("hit_limit"), r.get("error"), actual)
                # APE is computed only for runs that produced a usable number.
                # Failures are counted as a CLASS, never folded into the mean --
                # one implausible answer would otherwise destroy it (P0038 F72).
                ape = (abs(fc - actual) / actual * 100) if cls == "ok" else None
                rows.append(dict(
                    category=cat, brand=brand, system=sysname, rep=rep,
                    actual=actual, forecast=fc, ape=ape, outcome=cls,
                    latency_s=r.get("latency_s"),
                    tokens_in=r.get("tokens_in") or 0, tokens_out=r.get("tokens_out") or 0,
                    tokens_cached_in=r.get("tokens_cached_in") or 0,
                    tokens_reasoning=r.get("tokens_reasoning") or 0,
                    tokens=(r.get("tokens_in") or 0) + (r.get("tokens_out") or 0),
                    containers=r.get("containers") or 0,
                    cost_usd_est=r.get("cost_usd_est") or 0.0,
                    error=r.get("error"),
                    trace=json.dumps(r.get("trace") or {}, default=str),
                    answer=(r.get("answer") or "")[:2000]))
                print(f"  {cat:12s} {str(brand)[:16]:16s} {sysname:13s} rep{rep} "
                      f"{cls:12s} fc={fc} ape={ape if ape is None else round(ape, 1)} "
                      f"lat={r.get('latency_s')} est=${r.get('cost_usd_est') or 0:.4f}")
        pd.DataFrame(rows).to_csv(OUT / "runs.csv", index=False)  # checkpoint per brand

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "runs.csv", index=False)
    _write_summary(df, OUT, repeats, brands, t_start)
    return df


def _write_summary(df, OUT, repeats, brands, t_start):
    """Aggregate per arm and write summary.md.

    Reports the failure taxonomy alongside accuracy: an arm that answers 60% of
    the time with great accuracy is not better than one that always answers, and
    a table showing only mean APE would hide that."""
    arm_names = [a for a, _ in ARMS if a in set(df.system)]
    agg = {}
    for sysname in arm_names:
        s = df[df.system == sysname]
        ok = s[s.outcome == "ok"]
        cv = ok.groupby("brand").forecast.apply(
            lambda x: x.std() / x.mean() if len(x) > 1 and x.mean() else np.nan)
        rep_ok = ok.groupby("brand").forecast.apply(
            lambda x: (x.max() - x.min()) / max(x.mean(), 1e-9) < 0.01)
        tar = ok.groupby("brand").forecast.apply(lambda x: _tar(list(x)))
        agg[sysname] = dict(
            n=len(s), n_ok=len(ok),
            # medMAPE alongside the mean: P0038 F75 removed mean MAPE from the
            # SRQ1 table because a single divergent series destroyed it.
            ape_mean=ok.ape.mean() if len(ok) else np.nan,
            ape_med=ok.ape.median() if len(ok) else np.nan,
            consistency=cv.mean() * 100 if len(cv) else np.nan,
            replicability=rep_ok.mean() * 100 if len(rep_ok) else np.nan,
            tar=tar.mean() if len(tar) else np.nan,
            tokens=s.tokens.mean(), reasoning=s.tokens_reasoning.mean(),
            latency=s.latency_s.mean(),
            cost=s.cost_usd_est.mean(), total_cost=s.cost_usd_est.sum(),
            **{f"cls_{c}": int((s.outcome == c).sum()) for c in FAILURE_CLASSES})

    def row(label, key, fmt="{:.1f}", pct=""):
        cells = []
        for a in arm_names:
            v = agg[a][key]
            cells.append("n/a" if v is None or (isinstance(v, float) and np.isnan(v))
                         else fmt.format(v) + pct)
        return f"| {label} | " + " | ".join(cells) + " |"

    hdr = {"A_dedicated": "A — dedicated model",
           "B_codeaction": "B — code-as-action",
           "C_nodata": "C — no firm data"}
    lines = [
        "# SRQ4 — does model availability improve an LLM's forecasts?", "",
        f"{len(brands)} brands x {repeats} repeats x {len(arm_names)} arms. "
        f"Model `{MODEL}`, reasoning effort `{REASONING_EFFORT}`. "
        f"Decoding: {DECODING_NOTE}. "
        "Forecasting the held-out test month from train+val.", "",
        "The arms are an information ladder: **C -> B** measures what data access buys, "
        "**B -> A** measures what model integration adds on top.", "",
        "| Metric | " + " | ".join(hdr.get(a, a) for a in arm_names) + " |",
        "|---|" + "---|" * len(arm_names),
        row("Runs", "n", "{:.0f}"),
        row("Usable answers", "n_ok", "{:.0f}"),
        row("**Correctness** — median APE (lower=better)", "ape_med", "{:.1f}", "%"),
        row("Correctness — mean APE", "ape_mean", "{:.1f}", "%"),
        row("**Consistency** — mean CV across repeats", "consistency", "{:.1f}", "%"),
        row("Replicability — % brands identical", "replicability", "{:.0f}", "%"),
        row("Replicability — TAR@N, 1% tol (Atil et al., 2025)", "tar", "{:.2f}"),
        row("Cost — mean tokens/answer", "tokens", "{:.0f}"),
        row("Cost — mean reasoning tokens (billed as output)", "reasoning", "{:.0f}"),
        row("Cost — mean USD/answer (est.)", "cost", "${:.4f}"),
        row("Cost — total USD this run (est.)", "total_cost", "${:.2f}"),
        row("Latency — mean seconds", "latency", "{:.1f}"),
        "",
        "## Outcome taxonomy",
        "",
        "Failures are reported as classes, not averaged away. An arm that answers "
        "60% of the time is not comparable to one that always answers, and a single "
        "implausible value destroys a mean (P0038 F72).", "",
        "| Outcome | " + " | ".join(hdr.get(a, a) for a in arm_names) + " |",
        "|---|" + "---|" * len(arm_names),
    ]
    for c in FAILURE_CLASSES:
        lines.append(row(c, f"cls_{c}", "{:.0f}"))

    est_total = float(df.cost_usd_est.sum())
    lines += ["", "## Cost reconciliation", "",
              f"Estimated from token counts: **${est_total:.4f}**.", ""]
    billed = None
    try:
        billed = fetch_billed_cost(t_start)
    except Exception as e:
        lines.append(f"Billing lookup failed: `{str(e)[:150]}`")
    if billed:
        lines += [f"Actually billed over the run window: **${billed['total_usd']:.4f}**.", "",
                  "The estimate excludes the Code Interpreter container charge, which the "
                  "API does not report per response — only the billing endpoint sees it. "
                  "Report the billed figure.", "",
                  "| Line item | USD |", "|---|---|"]
        for k, v in sorted(billed["line_items"].items(), key=lambda x: -x[1]):
            lines.append(f"| {k} | ${v:.6f} |")
    elif billed is None:
        lines.append("_No `OPENAI_ADMIN_KEY` set, so billed cost could not be read. "
                     "The figure above is a token-only estimate and excludes container "
                     "charges._")

    (OUT / "summary.md").write_text("\n".join(lines) + "\n",
                                    encoding="utf-8", newline="\n")
    print("\n" + "\n".join(lines))
    print(f"\nSaved runs.csv + summary.md in {OUT}")


def main():
    ap = argparse.ArgumentParser(description="SRQ4 experiment: three-arm information ladder")
    ap.add_argument("--demo", action="store_true",
                    help="one brand through all three arms, no repeats -- the smoke test")
    ap.add_argument("--full", action="store_true", help="the full experiment")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--brands-per-cat", type=int, nargs=4, default=[4, 4, 4, 3],
                    help="brands drawn per category, in CAT_FILE order")
    ap.add_argument("--arms", default="A,B,C",
                    help="comma-separated subset of A,B,C")
    ap.add_argument("--category", default="CSD")
    ap.add_argument("--brand", default="HARBOE")
    ap.add_argument("--out", default=None, help="output dir (default: SRQ4 results dir)")
    a = ap.parse_args()

    want = {s.strip().upper() for s in a.arms.split(",") if s.strip()}
    arms = tuple((n, f) for n, f in ARMS if n[0] in want)
    if not arms:
        raise SystemExit(f"--arms {a.arms!r} selected no arms; expected some of A,B,C")

    if a.full:
        run_full(a.repeats, tuple(a.brands_per_cat), arms, a.out)
        return

    # Demo: one brand, one repeat, every selected arm. This is the smoke test --
    # it reveals what a run costs and how long it takes before committing to the
    # full schedule.
    t_start = time.time()
    _, actual = _brand_history(a.category, a.brand)
    print(f"=== SRQ4 demo: {a.brand} / {a.category} ===")
    print(f"    model={MODEL} reasoning={REASONING_EFFORT} ({DECODING_NOTE})")
    print(f"    held-out actual = {actual:,.0f}\n")
    est = 0.0
    for name, fn in arms:
        print(f">>> {name}")
        r = fn(a.category, a.brand)
        cls = _classify(r.get("forecast"), r.get("hit_limit"), r.get("error"), actual)
        fc = r.get("forecast")
        ape = f"{abs(fc - actual) / actual * 100:.1f}%" if (cls == "ok" and actual) else "n/a"
        est += r.get("cost_usd_est") or 0.0
        print(f"    outcome={cls}  forecast={fc}  APE={ape}  latency={r['latency_s']}s")
        print(f"    tokens in={r['tokens_in']} out={r['tokens_out']} "
              f"(reasoning={r['tokens_reasoning']})  est=${r.get('cost_usd_est') or 0:.4f}")
        print(f"    trace={json.dumps(r.get('trace') or {}, default=str)}")
        print(f"    answer: {(r.get('answer') or '')[:300]}\n")
    print(f"--- estimated token cost for this demo: ${est:.4f}")
    try:
        billed = fetch_billed_cost(t_start)
        if billed:
            print(f"--- billed (incl. container): ${billed['total_usd']:.4f}")
            for k, v in sorted(billed["line_items"].items(), key=lambda x: -x[1]):
                print(f"      {k:48s} ${v:.6f}")
        else:
            print("--- no OPENAI_ADMIN_KEY: billed cost unavailable")
    except Exception as e:
        print(f"--- billing lookup failed: {str(e)[:150]}")


if __name__ == "__main__":
    main()
