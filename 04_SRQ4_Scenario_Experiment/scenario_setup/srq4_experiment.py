#!/usr/bin/env python3

"""
SRQ4 experiment harness — does model availability improve an LLM's forecasts?

Three scenarios forming an INFORMATION LADDER (B-DEC-5, 2026-08-19). Each adds one
thing to the scenario below it, so the two increments can be attributed separately:

  A_plain   no firm data; web search only. Not a null condition -- it finds
            annual reports and market commentary and answers confidently.
  B_data    the brand history in a hosted Code Interpreter sandbox; the LLM
            writes and runs its own forecasting code.
  C_model   the same data behind a `forecast_demand` tool backed by the
            pre-trained XGBoost. The LLM writes no code.

  A -> B  measures what DATA ACCESS buys.
  B -> C  measures what MODEL INTEGRATION adds on top -- the thesis contribution.

A two-scenario B-vs-C design conflates these, and a reviewer could then argue the
whole effect is just data access.

All scenarios run the SAME model, temperature and reasoning effort: the design
isolates how the forecast is produced, so any other difference would measure LLM
quality instead of the intervention.

Outcomes are classified (ok / code_error / no_forecast / timeout / implausible)
rather than averaged. Failures are findings: "code-as-action failed 12% of the
time" says more about production readiness than a small accuracy gap.

Keys are read from 03_thesis_modelling/.env, falling back to the repo-root .env:
  OPENAI_API_KEY    project key   -- inference (all scenarios)
  OPENAI_ADMIN_KEY  admin key     -- billing reconciliation (optional)
The two scopes are disjoint; the project key returns 403 on the costs endpoint.

Usage:
  python 03_thesis_modelling/scenario_setup/srq4_experiment.py --demo
  python 03_thesis_modelling/scenario_setup/srq4_experiment.py --demo --scenarios A,B
  python 03_thesis_modelling/scenario_setup/srq4_experiment.py --full --repeats 5

RESULT CACHE
------------
Runs cost money, so a completed run is treated as a cache entry keyed by
(prompt schema, category, brand, scenario, repeat).

    default     fill only the gaps. Re-running an identical command sends
                nothing and costs nothing. This is how a block is extended:
                ask for 10 repeats when 6 exist, and only 4 are sent.
    --append    add repeats ALONGSIDE the cached ones, numbered past the
                highest already stored. Use to deliberately grow n.
    --refresh   re-run cached cells and replace them. Spends again on work
                already paid for; use only when a run is suspect.

Only rows carrying the CURRENT prompt schema id count as cache hits. Change any
prompt string and the id changes, so older rows stop matching automatically and
answers to different questions are never pooled. A failed run is not a cache
hit either -- it is retried.
"""
import argparse, json, os, re, sys, time, warnings
from pathlib import Path
import numpy as np
import pandas as pd

def _find_repo_root() -> Path:
    """Walk up from this file to the repo root (anchored on .env.example).

    Replaces a hard-coded parents[N] hop, which silently points at the wrong
    directory whenever a script moves between folder depths -- as happened in
    the 2026-09-06 restructure.
    """
    _start = Path(__file__).resolve().parent
    for _cand in (_start, *_start.parents):
        if any((_cand / _a).exists() for _a in (".env.example", ".env", "PATHS.py")):
            return _cand
    raise FileNotFoundError(f"Could not find project root above {_start}")


sys.path.insert(0, str(_find_repo_root()))
from PATHS import THESIS_RESULTS_SRQ1_DIR, THESIS_RESULTS_SRQ4_DIR, get_category_engineered_bymonth_dir, SRQ2_DIR

warnings.filterwarnings("ignore")

# The modelling feature set lives with the training code that defines it.
sys.path.insert(0, str(_find_repo_root() / "01_SRQ1_Model_Training"
                       / "02_thesis_modelling" / "model_training" / "srq1"))
from _features import FEATURES as _FEATURES, resolve as _resolve_feats, describe as _describe_feats  # noqa: E402,F401
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = _find_repo_root()

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
#   thesis_manifold_openai_prompts       -> OPENAI_API_KEY   (project key: inference)
#   thesis_manifold_openai_prompts_admin -> OPENAI_ADMIN_KEY (admin key: billing)
# The two scopes are disjoint -- the project key returns 403 on
# /v1/organization/costs and the admin key returns 403 on /v1/models -- so both
# are required: one to run the experiment, one to price it.
#
# Both spellings are accepted, `openai` included and omitted. The dashboard
# label carries the `openai` segment; an earlier version of this mapping did
# not, so every run required OPENAI_API_KEY to be exported by hand and the
# .env was silently ignored. Listing both spellings is cheaper than a rename
# that would break whichever copy of the file is not edited. First match wins.
for _src, _dst in (("thesis_manifold_openai_prompts", "OPENAI_API_KEY"),
                   ("thesis_manifold_prompts", "OPENAI_API_KEY"),
                   ("thesis_manifold_openai_prompts_admin", "OPENAI_ADMIN_KEY"),
                   ("thesis_manifold_prompts_admin", "OPENAI_ADMIN_KEY")):
    if os.environ.get(_src) and not os.environ.get(_dst):
        os.environ[_dst] = os.environ[_src]

import importlib.util

# Prompts live in prompts.py, never inline here: they are the experimental
# instrument and must be inspectable and diffable on their own.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompts as P

# Rows written before prompt-schema tracking existed. They were produced by the
# v2 question (units named, no recommendation request, no output exemplar), so
# they are NOT poolable with current runs and must not be silently treated as
# though they were. Tagging them explicitly is what keeps that decision visible
# in the data rather than resting on someone's memory of when a file was
# written.
LEGACY_SCHEMA = "v2-units-no-recommendation"


# Scenario C's tool comes from the serving interface. Loaded by explicit path
# because 03_thesis_modelling/ has no __init__.py, so it is not an importable
# package. Serving loads persisted models; nothing here trains.
# P0046 2026-09-06: was ROOT/"model_serving_interface"/"scenario_c_forecast",
# a path removed in the SRQ restructure -- Scenario C would have raised
# FileNotFoundError at import. The tool now lives in the SRQ2 tier, resolved
# through PATHS rather than a relative guess.
_FT_PATH = SRQ2_DIR / "forecast_tool.py"
if not _FT_PATH.is_file():
    raise FileNotFoundError(
        f"Scenario C's forecast tool is missing: {_FT_PATH}")
_spec = importlib.util.spec_from_file_location("forecast_tool", _FT_PATH)
_ft = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_ft)

# ---------------------------------------------------------------------------
# Model + pricing (DEC-LLM 2026-07-12, confirmed B-DEC-1 2026-08-19)
# ---------------------------------------------------------------------------
# All three scenarios MUST run the same model: the design isolates a single variable
# (how the forecast is produced), so a model that differs between scenarios measures
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
# the decoding control across scenarios; that is not available on a reasoning model.
#
# This does NOT break the comparison -- all three scenarios are equally uncontrolled,
# so decoding is held constant across scenarios in the only sense the API permits.
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
# container_id -- so this is necessarily an estimate. Scenario B alone incurs it.
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
# The third tuple element is a DIRECTORY NAME and must match the case on disk:
# Danskvand/ and Energidrikke/ are capitalised. Windows resolves either spelling,
# so lowercase keys worked here and silently found nothing on Linux -- the same
# defect fixed across the SRQ1 scripts on 2026-09-09. Two of four categories were
# dropped with no error.
CAT_FILE = {"CSD": ("csd", "bymonth", "CSD"),
            "Danskvand": ("danskvand", "bymonth", "Danskvand"),
            "Energidrikke": ("energidrikke", "bymonth", "Energidrikke"),
            "RTD": ("rtd", "bymonth", "RTD")}


def _engineered_dir(tag, sub):
    return get_category_engineered_bymonth_dir(sub)


# The forecast horizon this experiment scores, in months. ONE constant, used
# both to select the feature matrix and to pick the scored month out of the
# held-out window, because those two must not be able to disagree.
#
# WHY THIS EXISTS (2026-09-07, fixing the scoring half of F22). The horizon
# used to be a hardcoded "_h3" in three read_parquet() calls, while the scored
# actual was test.iloc[0] -- the FIRST held-out month, i.e. the month straight
# after the training cutoff. That is one month ahead by construction, whichever
# matrix is read. So the experiment reported three-month-ahead accuracy while
# measuring one-month-ahead accuracy, independently of the feature-side defect
# in engineer_features(). Fixing only the features would have left this intact.
#
# The scored month is now test.iloc[HORIZON - 1]: standing at the cutoff and
# forecasting HORIZON months out lands on the HORIZON-th held-out month.
#
# H=3 is the primary reported horizon: a quarter is the period in which
# marketing budgets are authorised, so it is the first horizon at which a
# campaign decision is actually taken. Set to 1 to reproduce the H=1 task.
HORIZON = 3

# Held-out months needed before a brand can be scored at this horizon. A brand
# whose test window is shorter has no observation at the target month at all.
_MIN_TEST_MONTHS = HORIZON


def _matrix_path(slug, tag, sub):
    """The feature matrix for the horizon being scored.

    Derived from HORIZON rather than written out, so the matrix and the scored
    offset cannot drift apart -- the failure this whole constant exists to stop.
    """
    return _engineered_dir(tag, sub) / f"{slug}_feature_matrix_h{HORIZON}.parquet"


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
# The modelling feature set, defined once in srq1/_features.py. Eleven copies of
# this literal existed and had already drifted -- srq1_pooled.py was missing
# promo_intensity, silently confounding the pooled-vs-per-category comparison
# (P0049 F31). Holiday and intermittency columns are conditional; resolve()
# intersects against the matrix, so a category lacking one simply omits it.
FEATURES = list(_FEATURES)

def available_features(fm, wanted=None):
	"""Return the wanted features that this matrix actually contains.

	DEC-DISCOVER-COLUMNS: categories differ in capability, not just in values.
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
    """Monthly observed series for a brand (train+val), the held-out actual, and
    the target month that actual belongs to.

    The target month is returned EXPLICITLY rather than left to each scenario to infer
    from "next month". Scenario A has no data and would otherwise anchor on the
    current wall-clock date, scoring a different month than scenarios B and C --
    which would make the scenarios incomparable rather than merely different.

    THE SCORED MONTH IS test.iloc[HORIZON - 1], NOT test.iloc[0]. The history
    ends at the training cutoff; forecasting HORIZON months past that cutoff
    lands on the HORIZON-th held-out month. Taking the first one would score a
    one-month-ahead forecast no matter which matrix was read -- see HORIZON.

    The intervening months (test.iloc[0 : HORIZON-1]) are given to NOBODY: they
    are held out of `fit` as well, because a forecaster standing at the cutoff
    has not observed them either. This is what makes the task genuinely
    HORIZON-months-ahead rather than a one-month forecast with a later label.

    LEAKAGE BOUNDARY: `fit` is train+val only. No test row is ever included,
    verified by `_assert_no_leakage` below."""
    slug, tag, sub = CAT_FILE[category]
    fm = pd.read_parquet(_matrix_path(slug, tag, sub))
    g = fm[(fm.brand.str.upper() == brand.upper())].sort_values("period_index")
    test = g[g.split == "test"].dropna(subset=["sales_units"])
    # Short window -> no observation at the target month. Return None rather
    # than silently scoring a nearer month, which would mix horizons across
    # brands within one reported figure.
    scored = test.iloc[HORIZON - 1] if len(test) >= _MIN_TEST_MONTHS else None
    actual = float(scored["sales_units"]) if scored is not None else None
    target = (f"{int(scored['period_year'])}-{int(scored['period_month']):02d}"
              if scored is not None else None)
    cols = ["period_year", "period_month", "sales_units"] + [
        c for c in ("promo_intensity", "weighted_distribution") if c in g.columns]
    fit = g[g.split.isin(["train", "val"])].dropna(subset=["sales_units"])[cols]
    _assert_no_leakage(fit, test, category, brand)
    return fit, actual, target


def _assert_no_leakage(fit, test, category, brand):
    """Hard-fail if the held-out month reached the data a scenario is given.

    A silent leak here would not produce an error -- it would produce an
    impressively accurate Scenario B, which is exactly the result the thesis is
    trying to measure. Cheap to check, catastrophic to miss.

    Checks the SCORED month (test.iloc[HORIZON-1]). The "history ends before the
    target" test below is what additionally proves the HORIZON-1 intervening
    months stayed out of `fit` -- at H=3 a history ending one month before the
    target would be a two-month-ahead forecast reported as three."""
    if len(test) < _MIN_TEST_MONTHS or not len(fit):
        return
    t = test.iloc[HORIZON - 1]
    clash = fit[(fit.period_year == t["period_year"])
                & (fit.period_month == t["period_month"])]
    if len(clash):
        raise AssertionError(
            f"LEAKAGE: {category}/{brand} target "
            f"{int(t['period_year'])}-{int(t['period_month']):02d} present in the "
            f"history handed to the agent")
    last = fit.sort_values(["period_year", "period_month"]).iloc[-1]
    if (last["period_year"], last["period_month"]) >= (t["period_year"], t["period_month"]):
        raise AssertionError(
            f"LEAKAGE: {category}/{brand} history ends "
            f"{int(last['period_year'])}-{int(last['period_month']):02d}, "
            f"at or after the target month")

    # The gap must be EXACTLY the horizon. The check above only proves the
    # history ends before the target, which at H=3 would also pass for a history
    # ending one month before it -- a two-month-ahead forecast reported as
    # three. Understating the gap is a leak; overstating it silently makes the
    # task harder than reported. Both are wrong, so this is an equality.
    gap = ((int(t["period_year"]) - int(last["period_year"])) * 12
           + int(t["period_month"]) - int(last["period_month"]))
    if gap != HORIZON:
        raise AssertionError(
            f"HORIZON MISMATCH: {category}/{brand} history ends "
            f"{int(last['period_year'])}-{int(last['period_month']):02d} and the "
            f"scored month is {int(t['period_year'])}-{int(t['period_month']):02d} "
            f"-- a gap of {gap} month(s), but HORIZON={HORIZON}. The forecast "
            f"would be reported at a horizon it was not made at.")


# The fields that make a Scenario C payload what SRQ2 claims it is: a forecast
# PLUS its measured reliability. Without them C is a forecast in a wrapper, and
# the B->C comparison measures nothing.
_PAYLOAD_REQUIRED = ("forecast_units", "interval_90", "confidence_tier",
                     "historical_wmape", "months_ahead")


def _payload_complete(out) -> bool:
    """True if the tool returned everything Scenario C depends on.

    WHY THIS IS CHECKED PER CALL (P0049). `forecast_tool` reads its track record
    inside a try/except, so a misplaced results directory made it return a valid
    payload with the `historical_*` fields simply ABSENT (F21). Scenario C then
    ran without the very evidence that distinguishes it from Scenario B, every
    run logged `outcome: ok`, and nothing in the results said otherwise.

    The harness already verifies the LLM queried the right series
    (`args_match_request`). This verifies the answer it got back was complete.
    Both are cheap; both failures are invisible without them.
    """
    if not isinstance(out, dict) or out.get("status") != "ok":
        return False
    return all(out.get(k) is not None for k in _PAYLOAD_REQUIRED)


def _eval_forecast(category, brand, month=None):
    """Scenario C's tool: delegate to the serving interface.

    This used to duplicate the whole training + calibration path and refit the
    model on EVERY tool call -- ~1.1 s of identical work per call, and a second
    copy of logic that had already drifted (its conformal calibration was
    in-sample, making intervals 3.9x too narrow, long after the same bug was
    fixed in forecast_service.py).

    Training now happens once in model_training/train_and_persist.py; serving
    loads the persisted booster. One implementation, one place to fix, and
    Scenario C's measured latency stops including training time that a real
    deployment would never pay."""
    return _ft.forecast_demand(category, brand, month)


# ---------------------------------------------------------------------------
# Shared OpenAI plumbing
# ---------------------------------------------------------------------------
# All three scenarios go through _usage() so token accounting is identical across
# them. Any per-scenario difference in how cost is measured would confound the cost
# comparison, which B-DEC-6 promoted to a primary outcome.
# The engine classes exist because scenarios D and E can fail in ways A-C
# cannot, and every one of them is a DIFFERENT statement about the result:
#   engine_unavailable  the machine had no Prometheus -- says nothing about it
#   warehouse_access    the run read live data instead of the snapshot, so it
#                       is not comparable to Scenario B and is excluded
#                       (DEC-D-SNAPSHOT, measured rather than enforced -- F45)
#   no_evidence         no tool call was observed, so the run is unverifiable;
#                       treated as a failure, never as a silent pass (F21)
#   no_code             D produced an answer without running code, which is
#                       Scenario A's behaviour wearing D's label
FAILURE_CLASSES = ("ok", "code_error", "no_forecast", "timeout", "implausible",
                   "engine_unavailable", "warehouse_access", "no_evidence",
                   "no_code")


def _client():
    from openai import OpenAI
    return OpenAI()


def _usage(r, containers=0):
    """Extract the token counts every scenario reports. `reasoning_tokens` is broken
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
        # Engine-side outcomes are their OWN classes, never `code_error`.
        # `code_error` means the scenario attempted its task and the code
        # failed; these mean it never got to attempt it, or attempted it
        # against the wrong data. Pooling them would let a missing engine or a
        # stray warehouse query read as evidence about forecasting quality.
        if "engine unavailable" in error:
            return "engine_unavailable"
        if "engine_verdict=warehouse_access" in error:
            return "warehouse_access"
        if "engine_verdict=no_evidence" in error:
            return "no_evidence"
        if "engine_verdict=no_code" in error:
            return "no_code"
        if "engine_verdict=no_forecast" in error:
            return "no_forecast"
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


def _trace(scenario, extra=None):
    """Provenance recorded per run (SRQ2 traceability). Every free parameter that
    changes cost or behaviour is captured, so a result can be tied to exactly the
    configuration that produced it."""
    t = {"scenario": scenario, "model": MODEL, "temperature": TEMPERATURE,
         "decoding": DECODING_NOTE, "reasoning_effort": REASONING_EFFORT,
         # The PROMPT REGISTRY entry (Dong et al., 2024 name execution traces,
         # tool-call spans and prompt registries as the artefacts an agent needs
         # to be auditable; ch2 §2.5). schema_id() hashes every prompt string
         # sent to the model -- the question, all three capability notes, the
         # exemplar, the sentinel and the tool schema -- while excluding the
         # per-run substitutions logged separately.
         #
         # Without it a results table cannot be tied to the prompt version that
         # produced it, so two runs whose prompts differ are indistinguishable
         # after the fact. It existed in prompts.py and was never recorded.
         "prompt_schema_id": P.schema_id(),
         "run_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if extra:
        t.update(extra)
    return t


def _cache_response(scenario, category, brand, rep, payload, out_dir=None):
    """Persist the full raw response for retrospective inspection.

    Paid, non-deterministic runs cannot be reproduced after the fact: the same
    prompt will not return the same reasoning or the same generated code. Anything
    not written down at run time is gone. Stored per run as JSON, including the
    code Scenario B wrote and the reasoning summaries -- these are qualitative
    evidence for the write-up, not debug output."""
    base = Path(out_dir) if out_dir else THESIS_RESULTS_SRQ4_DIR
    d = base / "raw_responses"
    d.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", f"{category}_{brand}")
    f = d / f"{scenario}__{safe}__rep{rep}.json"
    f.write_text(json.dumps(payload, indent=2, default=str),
                 encoding="utf-8", newline="\n")
    return str(f)


def _response_detail(r):
    """Pull the inspectable parts out of a Responses API object: the code the
    model wrote, any reasoning summary it exposed, and web-search queries."""
    detail = {"code_blocks": [], "reasoning": [], "web_queries": [], "item_types": []}
    for it in getattr(r, "output", []) or []:
        detail["item_types"].append(it.type)
        if it.type == "code_interpreter_call":
            detail["code_blocks"].append({"code": getattr(it, "code", None),
                                          "container_id": getattr(it, "container_id", None),
                                          "status": getattr(it, "status", None)})
        elif it.type == "reasoning":
            for s in (getattr(it, "summary", None) or []):
                detail["reasoning"].append(getattr(s, "text", str(s)))
        elif it.type.startswith("web_search"):
            act = getattr(it, "action", None)
            detail["web_queries"].append(getattr(act, "query", None) if act else None)
    return detail


def _result(scenario, text, err, t0, u, forecast, containers=0, hit_limit=False, trace_extra=None):
    """Uniform result record. One shape across all three scenarios so the results
    writer never has to branch on which scenario produced a row."""
    return {"answer": text or (err or "(no output)"),
            "latency_s": round(time.perf_counter() - t0, 2),
            "tokens_in": u["tokens_in"], "tokens_out": u["tokens_out"],
            "tokens_cached_in": u["tokens_cached_in"],
            "tokens_reasoning": u["tokens_reasoning"],
            "containers": containers,
            "cost_usd_est": _cost_usd(u["tokens_in"], u["tokens_out"],
                                      u["tokens_cached_in"], containers),
            "forecast": forecast, "error": err, "hit_limit": hit_limit,
            "trace": _trace(scenario, trace_extra)}


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
# Scenario C -- dedicated-model tool (the thesis artefact)
# ---------------------------------------------------------------------------
def run_scenario_c(category, brand, question=None):
    """The LLM calls `forecast_demand`, backed by the pre-trained XGBoost. It
    writes no code; the number comes from the dedicated model."""
    c = _client()
    tools = [P.FORECAST_TOOL_SCHEMA]
    _, _, target = _brand_history(category, brand)
    task = question or P.scenario_c_prompt(brand, category, target)
    msgs = [{"role": "user", "content": task}]
    t0 = time.perf_counter()
    tot = dict(_EMPTY_USAGE)
    tool_forecast = None
    err = None
    hit_limit = True
    text = ""
    details = []
    tool_outputs = []
    tool_calls = []
    try:
        for _ in range(4):
            r = c.responses.create(model=MODEL,
                                   reasoning={"effort": REASONING_EFFORT,
                                          "summary": "auto"},
                                   tools=tools, input=msgs)
            u = _usage(r)
            for k in tot:
                tot[k] += u[k]
            details.append(_response_detail(r))
            calls = [it for it in r.output if it.type == "function_call"]
            if calls:
                for call in calls:
                    args = json.loads(call.arguments or "{}")
                    # The scored month is passed EXPLICITLY. Omitting it makes
                    # the tool fall back to the first held-out month, which at
                    # HORIZON>1 is not the month the run is scored on -- the
                    # forecast would be one month ahead while the actual it is
                    # compared against is HORIZON months ahead. The prompt
                    # already names this month to the model for the same reason.
                    out = _eval_forecast(args.get("category", category),
                                         args.get("brand", brand),
                                         target)
                    # Log the arguments the MODEL chose alongside what it was
                    # asked about. A mismatch means the LLM queried a different
                    # series than the one being scored -- silent otherwise, and
                    # it would corrupt the accuracy number.
                    tool_calls.append({
                        "requested_category": category, "requested_brand": brand,
                        "llm_arg_category": args.get("category"),
                        "llm_arg_brand": args.get("brand"),
                        "args_match_request": (
                            str(args.get("category", "")).upper() == str(category).upper()
                            and str(args.get("brand", "")).upper() == str(brand).upper()),
                        # Did the payload actually carry the evidence that makes
                        # this Scenario C? Recorded per call, because the answer
                        # can differ between calls and an aggregate would hide it.
                        "payload_complete": _payload_complete(out),
                        "months_ahead": out.get("months_ahead"),
                        "tool_output": out})
                    # The tool output is authoritative: whatever the LLM then says
                    # in prose, the dedicated model's number is what Scenario C is
                    # credited with.
                    tool_outputs.append(out)
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
    res = _result("C_model", text, err, t0, tot, forecast,
                   containers=0, hit_limit=hit_limit,
                   trace_extra={"tool": "forecast_demand", "wrote_code": False,
                                "target_month": target,
                                "tool_returned_forecast": tool_forecast is not None,
                                # Promoted to the trace, not left in the nested
                                # tool_calls list: a run that served forecasts
                                # WITHOUT their track record is not a valid
                                # Scenario C, and that has to be visible in the
                                # results table rather than found by reading logs
                                # (F21). False here invalidates the B->C claim.
                                "payload_complete": bool(tool_calls) and all(
                                    c.get("payload_complete") for c in tool_calls)})
    # Flatten the per-round details into the same shape the other two scenarios
    # use, so inspect_runs.py and any later analysis can read one structure
    # rather than branching on which scenario wrote the file. `rounds` is kept
    # for the per-turn breakdown.
    flat = {"code_blocks": [], "reasoning": [], "web_queries": [], "item_types": []}
    for rd in details:
        for k in flat:
            flat[k].extend(rd.get(k) or [])
    res["detail"] = {**flat, "rounds": details, "tool_outputs": tool_outputs,
                     "tool_calls": tool_calls, "tool_schema": tools}
    res["prompt"] = task
    return res


# ---------------------------------------------------------------------------
# Scenario B -- code-as-action (the LLM writes and runs its own forecasting code)
# ---------------------------------------------------------------------------
def run_scenario_b(category, brand, question=None, sentinel="FORECAST"):
    """The LLM gets the brand history and must write + run its own code in the
    hosted Code Interpreter sandbox.

    Code Interpreter, not the hosted shell (B-DEC-6): a shell would grant
    arbitrary terminal access that scenarios A and C do not have -- a second variable
    moving -- and would let the model work around its own failures, suppressing
    the failure taxonomy that is itself part of the result.

    Each call creates a fresh container (`container: auto`), so no state carries
    between observations."""
    c = _client()
    fit, _, target = _brand_history(category, brand)
    csv = fit.to_csv(index=False)
    # Name the target month rather than saying "next month": scenarios A, B and C must
    # all be scored on the SAME month, and only the data tells us which one it is.
    prompt = (question if question
              else P.scenario_b_prompt(brand, category, target, csv, sentinel))
    t0 = time.perf_counter()
    err = None
    text = ""
    ncalls = 0
    detail = {}
    u = dict(_EMPTY_USAGE)
    try:
        r = c.responses.create(model=MODEL,
                               reasoning={"effort": REASONING_EFFORT,
                                          "summary": "auto"},
                               tools=[{"type": "code_interpreter",
                                       "container": {"type": "auto"}}],
                               input=prompt)
        ncalls = sum(1 for it in r.output if it.type == "code_interpreter_call")
        u = _usage(r, containers=1)
        text = r.output_text
        detail = _response_detail(r)
    except Exception as e:
        err = str(e)[:300]

    forecast, via_sentinel = _parse_sentinel(text, sentinel)
    containers = 0 if err else 1
    res = _result("B_data", text, err, t0, u, forecast,
                   containers=containers,
                   trace_extra={"tool": "code_interpreter", "wrote_code": True,
                                "target_month": target, "history_months": len(fit),
                                "history_ends": (f"{int(fit.period_year.iloc[-1])}-"
                                                 f"{int(fit.period_month.iloc[-1]):02d}"
                                                 if len(fit) else None),
                                "code_calls": ncalls, "via_sentinel": via_sentinel})
    res["detail"] = detail
    res["prompt"] = prompt
    return res


# ---------------------------------------------------------------------------
# Scenario A -- no firm data (the floor, and the first rung of the ladder)
# ---------------------------------------------------------------------------
def run_scenario_a(category, brand, question=None):
    """The LLM answers with no access to the Nielsen data at all.

    NOT a null condition (B-DEC-5). With web search it will find annual reports,
    market commentary and category coverage, and return a confident number. How
    wrong that number is -- and how confidently wrong -- is the finding, and it
    answers the practitioner question "why not just ask ChatGPT?".

    Documented limitation: because this scenario can browse, it is not a clean
    no-information floor. It may encounter genuinely relevant public data. That
    UNDERSTATES the measured value of data access (C->B), so the bias runs
    conservative with respect to our own claim."""
    c = _client()
    _, _, target = _brand_history(category, brand)
    # The target month is in the PAST relative to wall-clock time (the held-out
    # period runs 2026-01..2026-07 and this is being run later). Two consequences,
    # both handled here:
    #   1. "next month" would anchor on today's date and score a DIFFERENT month
    #      than scenarios B and C -- so the month is named explicitly.
    #   2. The figure may be publicly reported by now, so the scenario is instructed to
    #      ESTIMATE rather than retrieve. This is a mitigation, not a guarantee;
    #      `retrieval_suspected` below flags runs to inspect, and the limitation
    #      is documented in the write-up.
    prompt = question if question else P.scenario_a_prompt(brand, category, target)
    t0 = time.perf_counter()
    err = None
    text = ""
    u = dict(_EMPTY_USAGE)
    detail = {}
    used_web = False
    try:
        r = c.responses.create(model=MODEL,
                               reasoning={"effort": REASONING_EFFORT,
                                          "summary": "auto"},
                               tools=[{"type": "web_search"}],
                               input=prompt)
        u = _usage(r, containers=0)
        used_web = any(it.type.startswith("web_search") for it in r.output)
        text = r.output_text
        detail = _response_detail(r)
    except Exception as e:
        err = str(e)[:300]

    forecast, via_sentinel = _parse_sentinel(text)
    # If the answer cites the target month itself, the scenario may have retrieved the
    # figure rather than estimated it. Flagged, not dropped -- the decision to
    # exclude a run belongs in analysis, on inspected evidence.
    retrieval_suspected = bool(target and target in (text or ""))
    res = _result("A_plain", text, err, t0, u, forecast, containers=0,
                   trace_extra={"tool": "web_search", "wrote_code": False,
                                "used_web": used_web, "via_sentinel": via_sentinel,
                                "target_month": target,
                                "retrieval_suspected": retrieval_suspected})
    res["detail"] = detail
    res["prompt"] = prompt
    return res




# ---------------------------------------------------------------------------
# Scenarios D and E -- the ladder's second half, on the Prometheus orchestrator
# ---------------------------------------------------------------------------
# D is B and E is C, run through the production agent instead of a bare API
# loop. That makes D->E the SAME intervention as B->C, measured twice on
# different orchestrators: agreement is a materially stronger claim than either
# pair alone, and disagreement is itself a finding about how much the result
# depends on the surrounding system.
#
# Everything vendor-shaped lives in prometheus_bridge, which runs the engine in
# ITS OWN interpreter (the two environments are disjoint -- see that module).
# Importing it is allowed to fail: an assessor with scenarios A-C, the shipped
# per-brand CSVs and an OpenAI key must still be able to run the harness, and
# they will not have Prometheus.
try:
    import prometheus_bridge as PB
except Exception as _e:                                     # noqa: BLE001
    PB = None
    _PB_ERR = f"{type(_e).__name__}: {str(_e)[:200]}"
else:
    _PB_ERR = None


def _engine_unavailable(scenario, why, t0, target):
    """A recorded outcome, not a crash.

    `engine_unavailable` is deliberately NOT one of the failure classes: those
    describe how a scenario failed at its task, and this describes a machine
    that could not attempt it. Pooling the two would let a missing engine read
    as evidence about Prometheus.
    """
    return _result(scenario, "", f"engine unavailable: {why}", t0,
                   dict(_EMPTY_USAGE), None, containers=0,
                   trace_extra={"tool": "prometheus", "wrote_code": False,
                                "target_month": target,
                                "engine_available": False})


def _run_engine_scenario(scenario, category, brand, user_prompt, coder_context,
                         require_code, target, extra_trace=None,
                         expect_calls=True):
    """Shared body for D and E: dispatch, classify from evidence, build a result.

    One function for both, so the two scenarios cannot drift in how they are
    measured -- the same reason A, B and C all go through `_result` and
    `_usage`. What differs between D and E is the prompt pair and whether code
    execution is required; everything about scoring is identical.
    """
    t0 = time.perf_counter()
    if PB is None:
        return _engine_unavailable(scenario, _PB_ERR or "bridge import failed",
                                   t0, target)
    ok, why = PB.engine_available()
    if not ok:
        return _engine_unavailable(scenario, why, t0, target)

    r = PB.call_engine(user_prompt, coder_context, MODEL)
    text = r.get("answer") or ""
    calls = r.get("calls") or []
    verdict, ev = PB.classify_engine_run(calls, text, r.get("error"), require_code,
                                         expect_calls=expect_calls)

    # Token usage is reported only if the engine surfaced it. When it did not,
    # the cost estimate would be a fabricated zero -- so `usage_reported` is
    # traced and the reported figure comes from the billing endpoint, exactly as
    # Scenario B's container charge already does.
    u = dict(_EMPTY_USAGE)
    u.update({k: v for k, v in (r.get("usage") or {}).items() if k in u})

    forecast, via_sentinel = _parse_sentinel(text)
    fp = r.get("fingerprint") or {}
    trace = {"tool": "prometheus",
             "wrote_code": bool(ev.get("code_calls")),
             "target_month": target,
             "engine_available": True,
             "orchestrator": "prometheus_graph_engine",
             "via_sentinel": via_sentinel,
             # THE DEC-D-SNAPSHOT CHECK. The SQL tools cannot be removed without
             # forking the vendor (F45), so compliance is measured rather than
             # configured: a non-empty list means this run read the live
             # warehouse instead of the snapshot, and it is excluded.
             "sql_calls": ev.get("sql_calls"),
             "code_calls": ev.get("code_calls"),
             "tool_calls": ev.get("all_calls"),
             "engine_verdict": verdict,
             "usage_reported": bool(r.get("usage_reported")),
             "sandbox_killed": r.get("sandbox_killed"),
             "coder_reasoning_effort": fp.get("coder_reasoning_effort"),
             "coder_request_limit": fp.get("coder_request_limit"),
             "vendor_coder_model": fp.get("vendor_coder_model")}
    if extra_trace:
        trace.update(extra_trace)

    # A verdict that is not `ok` is surfaced as the run's error, so it reaches
    # the results table rather than living only in the trace. `_classify` then
    # maps it into the failure taxonomy the write-up reports.
    err = r.get("error")
    if not err and verdict != "ok":
        err = f"engine_verdict={verdict}"

    res = _result(scenario, text, err, t0, u, forecast, containers=0,
                  trace_extra=trace)
    # `code_blocks` carries the SAME shape Scenario B writes, so a reader can
    # audit D's method the way B's can be audited without knowing which
    # orchestrator produced it. Until 2026-09-11 this was hardcoded [] and D's
    # source was discarded, leaving `item_types` (four copies of the string
    # "execute_code") as the only record of what D actually did.
    res["detail"] = {"code_blocks": [{"code": c, "container_id": None,
                                      "status": "completed"}
                                     for c in (r.get("code_written") or [])],
                     "reasoning": [], "web_queries": [],
                     "item_types": list(ev.get("all_calls") or []),
                     "engine_stdout": r.get("stdout_log"),
                     "engine_evidence": ev}
    res["prompt"] = user_prompt
    res["coder_context"] = coder_context
    return res


def run_scenario_d(category, brand, question=None):
    """D -- Prometheus writes and runs its own forecasting code (B's task).

    The series reaching the coder is the SAME one Scenario B is handed, from
    `_brand_history()`, so the two arms differ in orchestrator alone.
    """
    fit, _, target = _brand_history(category, brand)
    csv = fit.to_csv(index=False)
    user = question or P.scenario_d_prompt(brand, category, target)
    coder = P.scenario_d_coder(brand, category, target, csv)
    return _run_engine_scenario(
        "D_prometheus", category, brand, user, coder,
        require_code=True, target=target,
        extra_trace={"history_months": len(fit),
                     "history_ends": (f"{int(fit.period_year.iloc[-1])}-"
                                      f"{int(fit.period_month.iloc[-1]):02d}"
                                      if len(fit) else None)})


def run_scenario_e(category, brand, question=None):
    """E -- Prometheus reports the dedicated model's forecast (C's task).

    The payload comes from the SAME call Scenario C makes, so E's number and C's
    number have identical origin and D->E is comparable to B->C.

    The payload is computed here and injected rather than the engine calling the
    tool: the trained booster needs xgboost, which is absent from the engine's
    interpreter and must not be added to a vendor environment this thesis does
    not control.
    """
    _, _, target = _brand_history(category, brand)
    out = _eval_forecast(category, brand, target)
    complete = _payload_complete(out)
    user = question or P.scenario_e_prompt(brand, category, target)
    coder = P.scenario_e_coder(brand, category, target,
                               json.dumps(out, indent=2, default=str))
    res = _run_engine_scenario(
        "E_prometheus_model", category, brand, user, coder,
        require_code=False, target=target,
        # E is HANDED its forecast, so it should make no tool call at all.
        # Requiring one classified a correct run as `no_evidence` (2026-09-11).
        # E's evidence is `payload_complete`, asserted in the parent below.
        expect_calls=False,
        # Same check that guards Scenario C (F21): a payload served without its
        # track record is not Scenario E, and that must be visible in the
        # results table rather than found by reading logs.
        extra_trace={"tool": "forecast_demand+prometheus",
                     "payload_complete": complete,
                     "tool_returned_forecast": out.get("forecast_units") is not None,
                     "months_ahead": out.get("months_ahead")})
    # The dedicated model's number is authoritative for E, exactly as it is for
    # C: whatever the agent then writes in prose, E is credited with the model's
    # forecast. Falling back to the parsed number would silently score a
    # hand-computed figure as if the model had produced it.
    if out.get("forecast_units") is not None:
        res["forecast"] = out["forecast_units"]
    res["detail"]["tool_outputs"] = [out]
    return res


def run_scenario_f(category, brand, question=None, sentinel="FORECAST"):
    """F -- the history AND the trained model's forecast AND a code sandbox.

    What a production deployment would actually have: the dedicated model is
    available, and so is everything else. C -> F therefore measures what adding
    code back ON TOP of the model does, which is the question C alone cannot
    answer.

    DEC-COMBINED-INPUT (Brian, 2026-09-11): the payload is presented as ONE
    INPUT AMONG SEVERAL, never as a starting point to revise. An agent handed a
    number and told it may keep it will almost always keep it, which would
    measure deference rather than integration. Whether F defers to the model,
    overrides it, or blends the two IS the measurement.

    UNLIKE C AND E, F's forecast is NOT overridden with the model's number. C
    and E are scored on the model's output because reporting it faithfully is
    their whole task; F is scored on what it actually says, because disagreeing
    with the model is a legitimate outcome here. `model_forecast` is traced
    alongside, so the two can be compared afterwards.
    """
    c = _client()
    fit, _, target = _brand_history(category, brand)
    csv = fit.to_csv(index=False)
    out = _eval_forecast(category, brand, target)
    complete = _payload_complete(out)
    prompt = (question if question else P.scenario_f_prompt(
        brand, category, target, csv,
        json.dumps(out, indent=2, default=str), sentinel))
    t0 = time.perf_counter()
    err = None
    text = ""
    ncalls = 0
    detail = {}
    u = dict(_EMPTY_USAGE)
    try:
        r = c.responses.create(model=MODEL,
                               reasoning={"effort": REASONING_EFFORT,
                                          "summary": "auto"},
                               tools=[{"type": "code_interpreter",
                                       "container": {"type": "auto"}}],
                               input=prompt)
        ncalls = sum(1 for it in r.output if it.type == "code_interpreter_call")
        u = _usage(r, containers=1)
        text = r.output_text
        detail = _response_detail(r)
    except Exception as e:
        err = str(e)[:300]

    forecast, via_sentinel = _parse_sentinel(text, sentinel)
    mfc = out.get("forecast_units")
    res = _result("F_data_model", text, err, t0, u, forecast,
                  containers=0 if err else 1,
                  trace_extra={"tool": "code_interpreter+forecast_demand",
                               "wrote_code": bool(ncalls),
                               "target_month": target,
                               "history_months": len(fit),
                               "history_ends": (f"{int(fit.period_year.iloc[-1])}-"
                                                f"{int(fit.period_month.iloc[-1]):02d}"
                                                if len(fit) else None),
                               "code_calls": ncalls,
                               "payload_complete": complete,
                               "months_ahead": out.get("months_ahead"),
                               # What the model said, so deference vs override
                               # is measurable rather than inferred from prose.
                               "model_forecast": mfc,
                               "deviates_from_model": (
                                   None if (forecast is None or mfc in (None, 0))
                                   else abs(forecast - mfc) / abs(mfc) > 0.01),
                               "via_sentinel": via_sentinel})
    res["detail"] = detail
    res["detail"]["tool_outputs"] = [out]
    res["prompt"] = prompt
    return res


def run_scenario_g(category, brand, question=None):
    """G -- F's capability envelope, on the Prometheus orchestrator.

    D -> E -> G repeats B -> C -> F on production, so the two ladders can be
    compared rung for rung. As in F, the answer is NOT overridden with the
    model's number.
    """
    fit, _, target = _brand_history(category, brand)
    csv = fit.to_csv(index=False)
    out = _eval_forecast(category, brand, target)
    complete = _payload_complete(out)
    payload = json.dumps(out, indent=2, default=str)
    user = question or P.scenario_g_prompt(brand, category, target)
    coder = P.scenario_g_coder(brand, category, target, csv, payload)
    mfc = out.get("forecast_units")
    res = _run_engine_scenario(
        "G_prometheus_data_model", category, brand, user, coder,
        # Code is AVAILABLE but not required: G may legitimately decide the
        # model's forecast needs no further analysis, and failing it for that
        # would presuppose the answer. `code_calls` is traced either way.
        require_code=False, target=target,
        extra_trace={"tool": "prometheus+forecast_demand",
                     "payload_complete": complete,
                     "months_ahead": out.get("months_ahead"),
                     "history_months": len(fit),
                     "model_forecast": mfc})
    fc = res.get("forecast")
    res["trace"]["deviates_from_model"] = (
        None if (fc is None or mfc in (None, 0))
        else abs(fc - mfc) / abs(mfc) > 0.01)
    res["detail"]["tool_outputs"] = [out]
    return res


# Ordered as the information ladder, weakest first:
#   A -> B  adds the firm's data and code execution
#   B -> C  adds the trained forecasting model
#   D -> E  repeats that pair on the Prometheus orchestrator
#
# D and E are listed here so --scenarios selects them by letter like the rest.
# They no-op cleanly (outcome `engine_unavailable`) on a machine without the
# engine, so an assessor running A-C is unaffected by their presence.
SCENARIOS = (("A_plain", run_scenario_a),
             ("B_data", run_scenario_b),
             ("C_model", run_scenario_c),
             ("D_prometheus", run_scenario_d),
             ("E_prometheus_model", run_scenario_e),
             ("F_data_model", run_scenario_f),
             ("G_prometheus_data_model", run_scenario_g))


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


def _eligible_brands(cat):
    """Brands with a held-out actual AT THE SCORED MONTH, ordered by volume.

    Requires at least HORIZON held-out months, not merely one: a brand with a
    shorter window has nothing to score at this horizon, and including it would
    put a brand into the sample that every run then skips."""
    slug, tag, sub = CAT_FILE[cat]
    fm = pd.read_parquet(_matrix_path(slug, tag, sub))
    te = fm[fm.split == "test"].dropna(subset=["sales_units"])
    has_test = {str(b).upper() for b, g in te.groupby("brand")
                if len(g) >= _MIN_TEST_MONTHS}
    vol = (fm.dropna(subset=["sales_units"]).groupby("brand").sales_units.sum()
           .sort_values(ascending=False))
    return [b for b in vol.index if str(b).upper() in has_test]


def _scorable_brands(cat):
    """Eligible brands whose held-out test window has NO zero actuals.

    APE divides by the actual, so a zero month is not a hard score -- it is
    undefined. Measured 2026-08-20, the lowest-volume eligible brand in
    danskvand (SIRMA) and energidrikke (GLACEAU) has an ALL-zero test window,
    and CSD's (DOCTOR POLIDORIS) reads [0, 1, 1, 0, 0, 2]. Selecting those
    brands would produce divide-by-zero cells rather than measurements.

    History length is NOT the discriminator -- every brand in a category shares
    the same split geometry and ~22-26 fit rows. Sparsity is.

    Scoping the experiment to brands with continuous recent sales is also the
    honest population for a demand forecast; intermittent/zero-inflated series
    are a different forecasting problem, and one worth naming as a limitation
    rather than silently averaging over.

    The whole test window must be non-zero, not merely the scored month. Only
    the scored month enters the APE denominator, so the weaker rule would be
    enough to keep the arithmetic defined -- but it would let the eligible
    population change with HORIZON, and the H=1 and H=3 results would then be
    measured on different sets of brands. Holding the population fixed keeps the
    two horizons comparable, at the cost of a few brands that could technically
    have been scored."""
    slug, tag, sub = CAT_FILE[cat]
    fm = pd.read_parquet(_matrix_path(slug, tag, sub))
    te = fm[fm.split == "test"].dropna(subset=["sales_units"])
    keep = {str(b).upper() for b, g in te.groupby("brand") if (g.sales_units > 0).all()}
    return [b for b in _eligible_brands(cat) if str(b).upper() in keep]


def _stratified_brands(cat, k=3):
    """Highest / median / lowest-volume brand among the SCORABLE ones.

    Volume-ranked top-N evaluates every scenario on the largest, most stable,
    most data-rich series -- exactly where a trained model should look best. It
    does not bias the A/B/C/D/E comparison (all scenarios see identical brands)
    but it cannot answer whether the advantage survives on a thin, volatile
    brand. Sampling across the volume range can.

    Stratifying over `_scorable_brands` rather than raw volume rank keeps that
    range coverage while guaranteeing every selected cell yields a defined APE."""
    pool = _scorable_brands(cat)
    if not pool:
        raise SystemExit(
            f"{cat}: no brand has a fully non-zero test window; cannot stratify. "
            f"Inspect with --list-brands.")
    if len(pool) <= k:
        return pool
    if k == 3:
        idx = [0, len(pool) // 2, len(pool) - 1]
    else:
        # Even spacing across the volume range, endpoints always included.
        idx = sorted({round(i * (len(pool) - 1) / (k - 1)) for i in range(k)})
    return [pool[i] for i in idx]


def _select_brands(per_cat=(4, 4, 4, 3), categories=None, brands=None,
                   strategy="volume"):
    """Which (category, brand) pairs to run.

    Three ways to choose, in order of precedence:

      brands=["HARBOE", "PEPSI"]  exactly those, matched case-insensitively
      strategy="stratified"       highest/median/lowest volume per category,
                                  drawn only from brands with a scorable
                                  (fully non-zero) test window
      categories=["CSD"]          top-N within only those categories
      per_cat=(4, 4, 4, 3)        top-N per category, all categories

    Naming brands explicitly matters for cost. `per_cat` always counts from the
    highest-volume brand down, so a partial re-run repeats brands already
    measured -- an attempt to collect only Coca Cola's Scenario A on 2026-08-19
    re-ran HARBOE first and exhausted the credit balance before reaching it."""
    cats = list(categories) if categories else list(CAT_FILE)
    for c in cats:
        if c not in CAT_FILE:
            raise SystemExit(f"unknown category {c!r}; expected some of {sorted(CAT_FILE)}")

    if brands:
        wanted = {b.strip().upper() for b in brands}
        picks, seen = [], set()
        for cat in cats:
            for b in _eligible_brands(cat):
                if str(b).upper() in wanted:
                    picks.append((cat, b))
                    seen.add(str(b).upper())
        missing = wanted - seen
        if missing:
            # Fail rather than silently run a subset: a typo would otherwise
            # produce a smaller experiment than the one written down.
            raise SystemExit(
                f"no held-out rows for brand(s) {sorted(missing)} in "
                f"categor{'y' if len(cats) == 1 else 'ies'} {cats}. "
                f"Use --list-brands to see what is available.")
        return picks

    picks = []
    if strategy == "stratified":
        # per_cat's first entry sets the per-category count (default 3).
        k = per_cat[0] if per_cat else 3
        for cat in cats:
            picks += [(cat, b) for b in _stratified_brands(cat, k)]
        return picks

    for cat, k in zip(cats, per_cat):
        picks += [(cat, b) for b in _eligible_brands(cat)[:k]]
    return picks


def run_full(repeats=5, brands_per_cat=(4, 4, 4, 3), scenarios=None, out_dir=None,
             budget_usd=None, categories=None, brands=None, rep_offset=0,
             dry_run=False, strategy="volume", mode="resume"):
    """Run the experiment and write runs.csv + summary.md.

    Checkpoints after every brand: a crash 40 runs in should not cost the
    completed runs, and a paid experiment is not worth re-running for want of a
    flush."""
    OUT = Path(out_dir) if out_dir else THESIS_RESULTS_SRQ4_DIR
    OUT.mkdir(parents=True, exist_ok=True)
    scenarios = scenarios or SCENARIOS
    pairs = _select_brands(brands_per_cat, categories, brands, strategy)
    t_start = time.time()
    schema = P.schema_id()
    n_req = len(pairs) * repeats * len(scenarios)

    todo, skipped, base = _plan_runs(pairs, scenarios, repeats, rep_offset,
                                     OUT, schema, mode)

    print(f"SRQ4: {len(pairs)} brands x {repeats} repeats x {len(scenarios)} scenarios "
          f"= {n_req} requested, model={MODEL}")
    print("      " + ", ".join(f"{c}/{b}" for c, b in pairs))
    print(f"      prompt schema: {schema}")
    print(f"      cache mode:    {mode}")
    if mode == "resume" and skipped:
        print(f"      CACHED:        {skipped} run(s) already complete at this "
              f"schema -- not re-sent")
    if mode == "append" and base != rep_offset:
        print(f"      appending:     repeat numbering starts at {base}")
    elif rep_offset:
        print(f"      repeat numbering starts at {rep_offset}")
    print(f"      TO RUN:        {len(todo)} run(s)")
    if budget_usd:
        print(f"      budget cap:    ${budget_usd:.2f} (estimated spend; stops mid-run)")
    print()

    if not todo:
        print("Nothing to run: every requested cell is already cached at this "
              "prompt schema. Use --refresh to re-run them, or --append to add "
              "repeats alongside them.")
        df = _load_runs(OUT)
        if len(df):
            _write_summary(df[df.schema == schema] if "schema" in df.columns else df,
                           OUT, repeats, pairs, t_start)
        return df

    if dry_run:
        # Per-run estimates from measured 2026-08-19 runs. Rough by design --
        # the point is to catch "this costs 4x what I expected" before spending.
        # Costed over what will ACTUALLY be sent, so the cache saving is visible.
        # A/B/C are measured (2026-08-19). D and E are NOT yet measured -- no
        # engine run has been costed. The placeholders are deliberately the
        # nearest measured analogue (D~B, E~C) plus a margin for the engine's
        # nested-agent loop, and they are flagged in the output rather than
        # presented as measurements. Replace with measured values after the
        # first smoke run; a made-up number that looks measured is the exact
        # failure the provenance rule exists to stop.
        est = {"A_plain": 0.4243, "B_data": 0.2664, "C_model": 0.0068,
               # D/E MEASURED 2026-09-11 on CSD/HARBOE (billed $1.83 for the
               # five-arm run, reconciled against the org costs endpoint).
               "D_prometheus": 0.55, "E_prometheus_model": 0.21,
               # F/G are ESTIMATES: F from B (same sandbox, a longer prompt),
               # G from D (same engine, a longer coder brief). Neither has run.
               "F_data_model": 0.30, "G_prometheus_data_model": 0.60}
        _unmeasured = {"F_data_model", "G_prometheus_data_model"}
        by_scen = {}
        for _, _, sysname, _, _ in todo:
            by_scen[sysname] = by_scen.get(sysname, 0) + 1
        total = sum(n * est.get(k, 0.2) for k, n in by_scen.items())
        print("DRY RUN -- nothing was sent.")
        _has_unmeasured = bool(set(by_scen) & _unmeasured)
        print(f"  {len(todo)} calls to send, estimated ${total:.2f}"
              + (" (A/B/C measured; D/E estimated, see below)"
                 if _has_unmeasured else " (from measured per-run costs)"))
        for k, n in sorted(by_scen.items()):
            mark = "  (ESTIMATE NOT MEASURED)" if k in _unmeasured else ""
            print(f"    {k:20s} {n:3d} runs x ${est.get(k, 0.2):.4f} "
                  f"= ${n * est.get(k, 0.2):6.2f}{mark}")
        if skipped:
            print(f"  {skipped} cached run(s) skipped -- not re-sent.")
        return None

    rows = []
    spent = 0.0
    stopped = False
    _hist = {}
    # One flat pass over the planned cells. The plan already excludes anything
    # cached, so the loop never has to reason about what has been paid for.
    for cat, brand, sysname, fn, rep in todo:
        if True:
            if (cat, brand) not in _hist:
                _, a, t = _brand_history(cat, brand)
                _hist[(cat, brand)] = (a, t)
            actual, target = _hist[(cat, brand)]
            if not actual:
                print(f"  skip {cat}/{brand}: no held-out actual")
                continue
            if True:
                try:
                    r = fn(cat, brand)
                except Exception as e:
                    r = {"forecast": None, "latency_s": None, "tokens_in": 0,
                         "tokens_out": 0, "tokens_cached_in": 0, "tokens_reasoning": 0,
                         "containers": 0, "cost_usd_est": 0.0, "answer": str(e)[:200],
                         "error": str(e)[:300], "hit_limit": False, "trace": {}}
                # Persist the raw response before anything else touches it: a
                # paid, non-deterministic run cannot be reproduced later, so
                # whatever is not written down now is lost.
                fc = r.get("forecast")
                cls = _classify(fc, r.get("hit_limit"), r.get("error"), actual)
                # Cache AFTER classifying, so the stored payload carries the
                # outcome too. Each file is then self-contained: readable without
                # joining against runs.csv.
                try:
                    _cache_response(sysname, cat, brand, rep,
                                    {"category": cat, "brand": brand, "rep": rep,
                                     "system": sysname,
                                     "actual": actual, "target_month": target,
                                     "forecast": fc, "outcome": cls,
                                     "ape": (abs(fc - actual) / actual * 100
                                             if cls == "ok" and actual else None),
                                     "latency_s": r.get("latency_s"),
                                     "answer": r.get("answer"), "prompt": r.get("prompt"),
                                     "trace": r.get("trace"), "detail": r.get("detail"),
                                     "tokens_in": r.get("tokens_in"),
                                     "tokens_out": r.get("tokens_out"),
                                     "tokens_reasoning": r.get("tokens_reasoning"),
                                     "cost_usd_est": r.get("cost_usd_est"),
                                     "error": r.get("error")},
                                    out_dir=OUT)
                except Exception as e:
                    print(f"    ! could not cache response: {str(e)[:120]}")
                # APE is computed only for runs that produced a usable number.
                # Failures are counted as a CLASS, never folded into the mean --
                # one implausible answer would otherwise destroy it (P0038 F72).
                ape = (abs(fc - actual) / actual * 100) if cls == "ok" else None
                rows.append(dict(
                    schema=schema,
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
                spent += r.get("cost_usd_est") or 0.0
                print(f"  {cat:12s} {str(brand)[:16]:16s} {sysname:13s} rep{rep} "
                      f"{cls:12s} fc={fc} ape={ape if ape is None else round(ape, 1)} "
                      f"lat={r.get('latency_s')} est=${r.get('cost_usd_est') or 0:.4f} "
                      f"cum=${spent:.2f}")
                # Hard budget stop. Estimated cost per run varies by an order of
                # magnitude between scenarios and brands, so a pre-run projection is
                # not a safeguard -- this is. Partial results are already on
                # disk from the per-brand checkpoint.
                if budget_usd and spent >= budget_usd:
                    print(f"\n!! BUDGET STOP: estimated spend ${spent:.2f} reached the "
                          f"${budget_usd:.2f} cap after {len(rows)} runs.")
                    print("   Partial results saved. Raise --budget to continue.")
                    stopped = True
                    break
            if stopped:
                break
        if stopped:
            break
        # Checkpoint as we go: a crash 40 runs in must not cost the completed
        # runs, and a paid experiment is not worth re-running for want of a flush.
        if len(rows) % 5 == 0:
            _merge_runs(rows, OUT)

    # Summarise everything on disk, not just this block: the appendix and the
    # summary must describe the whole experiment, not the most recent slice.
    df = _merge_runs(rows, OUT)
    _write_summary(df, OUT, repeats, pairs, t_start)
    return df


# ---------------------------------------------------------------------------
# Result cache: never pay twice for the same run
# ---------------------------------------------------------------------------
# Runs are expensive and are executed in blocks across sessions. Three things
# follow, and all three are handled here rather than left to the operator:
#
#   1. A completed run is a CACHE ENTRY. Re-running the same configuration
#      should cost nothing by default.
#   2. Whether an entry counts as "the same run" depends on the PROMPT. Answers
#      to different questions cannot be pooled, so every row records the prompt
#      schema id and only rows sharing the current id are reusable.
#   3. Extending an experiment means filling the gap between what exists and
#      what is now asked for -- not repeating the whole block.
#
# The unit of caching is a CELL: (schema, category, brand, scenario, rep).

CACHE_KEYS = ["schema", "category", "brand", "system", "rep"]


def _load_runs(OUT):
    f = OUT / "runs.csv"
    if not f.is_file():
        return pd.DataFrame()
    try:
        df = pd.read_csv(f)
    except Exception:
        return pd.DataFrame()
    # Rows written before schema tracking existed are tagged with the schema
    # that was live when they were produced, rather than being silently treated
    # as current. Backfilling them as "unknown" would make them look poolable
    # with runs they cannot be pooled with.
    if len(df) and "schema" not in df.columns:
        df["schema"] = LEGACY_SCHEMA
    return df


def _cached_cells(OUT, schema):
    """Which (category, brand, system, rep) cells already exist at THIS schema."""
    df = _load_runs(OUT)
    if not len(df) or "schema" not in df.columns:
        return set()
    d = df[df.schema == schema]
    if not len(d):
        return set()
    cols = ["category", "brand", "system", "rep"]
    if not all(c in d.columns for c in cols):
        return set()
    # A failed run is not a usable cache entry: it should be retried, not
    # counted as done. Only `ok` rows suppress a re-run.
    if "outcome" in d.columns:
        d = d[d.outcome == "ok"]
    return {tuple(r) for r in d[cols].astype(object).values}


def _plan_runs(pairs, scenarios, repeats, rep_offset, OUT, schema, mode):
    """Decide which cells to execute, and report what the cache covers.

    Returns (todo, n_skipped) where todo is a list of (cat, brand, sysname, fn, rep).

    mode:
      "resume"  -- default. Execute only cells absent from the cache at this
                   schema. Re-running an identical config sends nothing.
      "refresh" -- execute every requested cell and replace the cached rows.
      "append"  -- execute every requested cell at repeat numbers past the
                   highest already stored, adding to the cache instead of
                   matching against it.
    """
    cached = _cached_cells(OUT, schema) if mode != "refresh" else set()

    base = rep_offset
    if mode == "append":
        df = _load_runs(OUT)
        if len(df) and "rep" in df.columns and "schema" in df.columns:
            d = df[df.schema == schema]
            if len(d):
                base = max(rep_offset, int(d.rep.max()) + 1)

    todo, skipped = [], 0
    for cat, brand in pairs:
        for sysname, fn in scenarios:
            for rep in range(base, base + repeats):
                if mode == "resume" and (cat, brand, sysname, rep) in cached:
                    skipped += 1
                    continue
                todo.append((cat, brand, sysname, fn, rep))
    return todo, skipped, base


def _merge_runs(new_rows, OUT):
    """Merge this batch into runs.csv rather than replacing the file.

    Blocks run days apart and repeats are added later, so a writer that replaced
    the file would destroy results that were already paid for.

    A row is identified by (schema, category, brand, system, rep). A re-run of
    the same cell REPLACES its row -- retrying a failure should correct it, not
    duplicate it -- while every other row on disk survives untouched. Rows at a
    different schema are never touched: they answer a different question and are
    kept for the record, not for pooling."""
    new = pd.DataFrame(new_rows)
    f = OUT / "runs.csv"
    old = _load_runs(OUT)
    if len(old) and all(k in old.columns for k in CACHE_KEYS) \
            and all(k in new.columns for k in CACHE_KEYS):
        old_idx = pd.MultiIndex.from_frame(old[CACHE_KEYS].astype(str))
        new_idx = pd.MultiIndex.from_frame(new[CACHE_KEYS].astype(str))
        old = old[~old_idx.isin(new_idx)]
        combined = pd.concat([old, new], ignore_index=True)
    else:
        combined = pd.concat([old, new], ignore_index=True) if len(old) else new
    combined.to_csv(f, index=False)
    return combined


def _write_summary(df, OUT, repeats, brands, t_start):
    """Aggregate per scenario and write summary.md.

    Reports the failure taxonomy alongside accuracy: a scenario that answers 60% of
    the time with great accuracy is not better than one that always answers, and
    a table showing only mean APE would hide that."""
    arm_names = [a for a, _ in SCENARIOS if a in set(df.system)]
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

    hdr = {"C_model": "A — dedicated model",
           "B_data": "B — code-as-action",
           "A_plain": "C — no firm data"}
    lines = [
        "# SRQ4 — does model availability improve an LLM's forecasts?", "",
        f"{len(brands)} brands x {repeats} repeats x {len(arm_names)} scenarios. "
        f"Model `{MODEL}`, reasoning effort `{REASONING_EFFORT}`. "
        f"Decoding: {DECODING_NOTE}. "
        "Forecasting the held-out test month from train+val.", "",
        "The scenarios are an information ladder: **A -> B** measures what data access buys, "
        "**B -> C** measures what model integration adds on top.", "",
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
        "Failures are reported as classes, not averaged away. An scenario that answers "
        "60% of the time is not comparable to one that always answers, and a single "
        "implausible value destroys a mean.", "",
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
    ap = argparse.ArgumentParser(description="SRQ4 experiment: three-scenario information ladder")
    ap.add_argument("--demo", action="store_true",
                    help="one brand through all three scenarios, no repeats -- the smoke test")
    ap.add_argument("--full", action="store_true", help="the full experiment")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--brands-per-cat", type=int, nargs="+", default=[4, 4, 4, 3],
                    help="top-N brands per category, in --categories order")
    ap.add_argument("--brands", nargs="+", default=None,
                    help="run EXACTLY these brands (case-insensitive). Overrides "
                         "--brands-per-cat. Use this for partial re-runs: "
                         "--brands-per-cat always counts from the top brand down, "
                         "so it repeats work already paid for.")
    ap.add_argument("--categories", nargs="+", default=None,
                    help="restrict to these categories (default: all four)")
    ap.add_argument("--rep-offset", type=int, default=0,
                    help="start repeat numbering here, to ADD repeats to an "
                         "existing run. runs.csv is merged, not replaced, so "
                         "earlier blocks survive; a cell with the same "
                         "(category, brand, scenario, rep) is replaced rather "
                         "than duplicated. Use this to scale up once the real "
                         "per-run cost is known -- but only if the PROMPT is "
                         "unchanged, since answers to different questions "
                         "cannot be pooled.")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and its estimated cost; send nothing")
    cache = ap.add_mutually_exclusive_group()
    cache.add_argument("--refresh", action="store_true",
                       help="re-run cells that are already cached at this prompt "
                            "schema, replacing their rows. Use when a run is "
                            "suspect, not to extend one -- it SPENDS again on "
                            "work already paid for.")
    cache.add_argument("--append", action="store_true",
                       help="add these repeats ALONGSIDE the cached ones, "
                            "numbering them past the highest already stored, "
                            "rather than treating a matching cell as done. Use "
                            "to deliberately grow n. Without it (the default), "
                            "an identical request costs nothing.")
    ap.add_argument("--brand-strategy", choices=["volume", "stratified"],
                    default="volume",
                    help="volume: top-N by units (default). stratified: "
                         "highest/median/lowest volume among brands with a "
                         "fully non-zero test window, so every cell yields a "
                         "defined APE. Use --brands-per-cat N to set the count "
                         "(default 3 when stratified).")
    ap.add_argument("--list-brands", action="store_true",
                    help="list eligible brands per category and exit")
    ap.add_argument("--scenarios", default="A,B,C",
                    help="comma-separated subset of A (plain LLM), "
                         "B (data + code), C (trained model)")
    ap.add_argument("--category", default="CSD")
    ap.add_argument("--brand", default="HARBOE")
    ap.add_argument("--out", default=None, help="output dir (default: SRQ4 results dir)")
    ap.add_argument("--budget", type=float, default=None,
                    help="stop once estimated spend reaches this many USD")
    a = ap.parse_args()

    if a.list_brands:
        for cat in (a.categories or list(CAT_FILE)):
            bs = _eligible_brands(cat)
            scorable = {str(b).upper() for b in _scorable_brands(cat)}
            print(f"\n{cat} -- {len(bs)} brands with held-out test rows, "
                  f"{len(scorable)} of them scorable "
                  "(highest volume first; * = no zero in the test window):")
            for i, b in enumerate(bs, 1):
                mark = "*" if str(b).upper() in scorable else " "
                print(f"  {i:3d}. {mark} {b}")
            print(f"  stratified pick: "
                  f"{', '.join(str(x) for x in _stratified_brands(cat))}")
        return

    want = {s.strip().upper() for s in a.scenarios.split(",") if s.strip()}
    scenarios = tuple((n, f) for n, f in SCENARIOS if n[0] in want)
    if not scenarios:
        raise SystemExit(f"--scenarios {a.scenarios!r} selected nothing; "
                         "expected some of A,B,C,D,E")

    if a.full:
        run_full(a.repeats, tuple(a.brands_per_cat), scenarios, a.out, a.budget,
                 categories=a.categories, brands=a.brands,
                 rep_offset=a.rep_offset, dry_run=a.dry_run,
                 strategy=a.brand_strategy,
                 mode=("refresh" if a.refresh else "append" if a.append else "resume"))
        return

    # Demo: one brand, one repeat, every selected scenario. This is the smoke test --
    # it reveals what a run costs and how long it takes before committing to the
    # full schedule.
    t_start = time.time()
    _, actual, target = _brand_history(a.category, a.brand)
    print(f"=== SRQ4 demo: {a.brand} / {a.category} ===")
    print(f"    model={MODEL} reasoning={REASONING_EFFORT} ({DECODING_NOTE})")
    print(f"    held-out actual = {actual:,.0f}\n")
    est = 0.0
    for name, fn in scenarios:
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
