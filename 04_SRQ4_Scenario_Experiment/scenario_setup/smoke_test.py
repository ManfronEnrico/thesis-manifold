#!/usr/bin/env python3
"""
SRQ4 smoke test — one run per scenario, ~$1, before the ~$40 funded set.

WHY THIS EXISTS
---------------
`verify_setup.py` checks contracts: keys resolve, the model is reachable, the
tool returns a complete payload, the prompts name the target month. It never
sends a request. So it cannot see anything that only appears when a scenario
actually runs -- an LLM querying the wrong series, a scenario answering about the
wrong month, a payload that degrades mid-run, a response the extractor cannot
parse.

Every defect this project has hit in the experiment path has been of one shape:
**something returned LESS rather than failing** (P0049 F21, F25, F31, F32). A
run of n=1 per scenario costs about a dollar and surfaces that class before the
sampling design spends forty.

WHAT IT ASSERTS, AND WHY EACH ONE
---------------------------------
The checks are not a wish-list; each maps to a requirement the thesis makes.

| Check | Source |
|---|---|
| every scenario answered, `outcome == "ok"` | a failed arm is a finding, but a failed SMOKE arm is a blocker |
| one target month across all arms | arms scored on different months are incomparable, not merely different |
| Scenario C's `months_ahead == HORIZON` | the horizon defect (F23) was invisible in exactly this way |
| C's payload complete, with `historical_*` | ch2 §2.5: uncertainty and track record are what make C differ from B |
| interval present and ordered lo < forecast < hi | ch2 §2.5 conformal intervals (Lei et al., 2018); a malformed interval is worse than none |
| `prompt_schema_id` recorded | ch2 §2.5 prompt registry (Dong et al., 2024) |
| a raw response cached per run | ch2 §2.5 execution traces; paid runs are not reproducible after the fact |
| tool-call span logged for C | ch2 §2.5 tool-call spans |
| cost within an order of magnitude of the estimate | a 10x surprise at n=1 is a 400x surprise at n=111 |

USAGE
-----
    python smoke_test.py                 # A, B, C -- one run each, ~$1
    python smoke_test.py --scenarios A,C
    python smoke_test.py --dry-run       # show the plan and the checks, spend nothing

Results go to a `smoke/` subfolder, NEVER the main results directory -- a smoke
run must not be mistaken for, or overwrite, a funded one.

SCENARIOS D AND E ARE NOT COVERED. They are not implemented in the harness
(`SCENARIOS` holds A, B and C only) and require the Prometheus graph engine plus
an E2B template. When they land, add them here first and smoke them before
spending.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_root = next((p for p in HERE.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {HERE}")
sys.path.insert(0, str(_root))
sys.path.insert(0, str(HERE))

# Rough per-run cost from the delivered A/B/C ladder (2026-08-19, $4.92 total):
# A ~$0.49, B ~$0.28, C ~$0.007. An order of magnitude above these is a surprise
# worth stopping for, because it multiplies by 111 in the funded set.
_EXPECTED_USD = {"A_plain": 0.50, "B_data": 0.30, "C_model": 0.01}
_COST_ALARM = 10.0


class Check:
    """One assertion, its verdict and a line explaining it."""

    def __init__(self) -> None:
        self.rows: list[tuple[bool, str, str]] = []

    def run(self, name, fn) -> bool:
        try:
            ok, detail = fn()
        except Exception as e:                      # a check must never crash the run
            ok, detail = False, f"check raised {type(e).__name__}: {str(e)[:110]}"
        self.rows.append((bool(ok), name, str(detail)))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}", flush=True)
        return bool(ok)

    @property
    def failed(self):
        return [r for r in self.rows if not r[0]]


def _interval_ok(payload) -> tuple[bool, str]:
    """The 90% interval must exist, be ordered, and contain the point forecast.

    A reversed or degenerate interval is worse than an absent one: it looks like
    calibrated uncertainty and is not. Chapter 6 measures coverage empirically
    (ch2 §2.5 -- the conformal guarantee is marginal and exchangeability is
    violated by temporal data), which is only meaningful if the interval is
    well-formed in the first place.
    """
    iv, fc = payload.get("interval_90"), payload.get("forecast_units")
    if not isinstance(iv, (list, tuple)) or len(iv) != 2:
        return False, f"interval_90 missing or malformed: {iv!r}"
    lo, hi = float(iv[0]), float(iv[1])
    if not lo < hi:
        return False, f"interval not ordered: lo={lo:,.0f} hi={hi:,.0f}"
    if fc is None or not (lo <= float(fc) <= hi):
        return False, f"forecast {fc} outside [{lo:,.0f}, {hi:,.0f}]"
    width = (hi - lo) / max(float(fc), 1e-9)
    return True, f"[{lo:,.0f}, {hi:,.0f}] around {float(fc):,.0f} (width {width:.1f}x)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--scenarios", default="A,B,C")
    ap.add_argument("--category", default="CSD")
    ap.add_argument("--brand", default=None,
                    help="default: the highest-volume scorable brand in --category")
    ap.add_argument("--budget", type=float, default=3.0,
                    help="hard spend cap in USD; the harness stops at it (default 3)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    import srq4_experiment as E
    import prompts as P

    brand = a.brand or E._scorable_brands(a.category)[0]
    _, actual, target = E._brand_history(a.category, brand)
    out_dir = Path(E.THESIS_RESULTS_SRQ4_DIR) / "smoke"

    print("=" * 74)
    print(f"  SRQ4 SMOKE TEST -- {a.category}/{brand}, target {target}")
    print(f"  scenarios={a.scenarios}  n=1 each  horizon=H{E.HORIZON}")
    print(f"  held-out actual: {actual:,.0f} units")
    print(f"  output -> {out_dir}")
    print("=" * 74)

    if a.dry_run:
        est = sum(_EXPECTED_USD.get(n, 0.0) for n, _ in E.SCENARIOS
                  if n[0] in a.scenarios.upper())
        print(f"\n  [dry] would spend approximately ${est:.2f} and assert:")
        for line in ("every scenario returns outcome == ok",
                     "all arms answer about ONE target month",
                     f"Scenario C months_ahead == {E.HORIZON}",
                     "C payload complete (historical_* present)",
                     "interval ordered and containing the forecast",
                     "prompt_schema_id recorded in every trace",
                     "a raw response cached per run",
                     "tool-call span logged for C",
                     "cost within 10x of the estimate"):
            print(f"        - {line}")
        return 0

    # --repeats 1 is what makes this a smoke test. --budget is a hard stop: if
    # a pricing change or a runaway loop pushes spend past the cap, the harness
    # halts rather than discovering it on the invoice.
    cmd = [sys.executable, str(HERE / "srq4_experiment.py"),
           "--scenarios", a.scenarios, "--categories", a.category,
           "--brands", brand, "--repeats", "1",
           "--budget", str(a.budget), "--out", str(out_dir)]
    print(f"\n  $ {' '.join(cmd[1:])}\n", flush=True)
    t0 = time.perf_counter()
    r = subprocess.run(cmd)
    dt = time.perf_counter() - t0
    if r.returncode != 0:
        print(f"\n  harness exited {r.returncode} after {dt:,.0f}s -- nothing to check")
        return 2

    runs_f = out_dir / "runs.csv"
    if not runs_f.is_file():
        print(f"\n  no runs.csv at {runs_f} -- the harness wrote nothing")
        return 2

    import pandas as pd
    runs = pd.read_csv(runs_f)
    traces = [json.loads(t) if isinstance(t, str) else {} for t in runs.get("trace", [])]

    print(f"\n{'=' * 74}\n  CHECKS ({dt:,.0f}s elapsed)\n{'=' * 74}")
    c = Check()

    c.run("every scenario answered", lambda: (
        len(runs) > 0 and (runs["outcome"] == "ok").all(),
        f"{int((runs['outcome'] == 'ok').sum())}/{len(runs)} ok"
        + ("" if (runs["outcome"] == "ok").all()
           else f"; failed: {runs[runs.outcome != 'ok'].outcome.tolist()}")))

    def one_month():
        # Arms scored on different months are incomparable, not merely different
        # -- and Scenario A, which has no data, would otherwise anchor on the
        # wall-clock date.
        months = sorted({str(m) for m in runs.get("target_month", []) if str(m) != "nan"})
        return len(months) == 1 and months[0] == target, \
            f"target_month across arms: {months} (expected [{target}])"
    c.run("all arms answer about ONE target month", one_month)

    def horizon_ok():
        cm = runs[runs.system.astype(str).str.startswith("C")]
        if not len(cm):
            return True, "Scenario C not in this run; skipped"
        ahead = [t.get("months_ahead") for t in traces
                 if str(t.get("scenario", "")).startswith("C")]
        payload = [t.get("payload_complete") for t in traces
                   if str(t.get("scenario", "")).startswith("C")]
        return (all(x == E.HORIZON for x in ahead if x is not None)
                and all(bool(x) for x in payload)), \
            f"months_ahead={ahead} (expected {E.HORIZON}), payload_complete={payload}"
    c.run(f"Scenario C forecasts at H={E.HORIZON} with a complete payload", horizon_ok)

    def interval():
        f = out_dir / "raw_responses"
        outs = []
        for p in sorted(f.glob("C_model__*.json")) if f.is_dir() else []:
            d = json.loads(p.read_text(encoding="utf-8"))
            outs += (d.get("detail") or {}).get("tool_outputs") or []
        if not outs:
            return True, "no Scenario C tool output in this run; skipped"
        return _interval_ok(outs[0])
    c.run("90% interval is well-formed", interval)

    c.run("prompt registry recorded (ch2 2.5)", lambda: (
        bool(traces) and all(t.get("prompt_schema_id") == P.schema_id() for t in traces),
        f"{ {t.get('prompt_schema_id') for t in traces} } vs prompts.schema_id()={P.schema_id()}"))

    def cached():
        d = out_dir / "raw_responses"
        n = len(list(d.glob("*.json"))) if d.is_dir() else 0
        return n >= len(runs), f"{n} raw response(s) cached for {len(runs)} run(s)"
    c.run("execution trace cached per run (ch2 2.5)", cached)

    def spans():
        d = out_dir / "raw_responses"
        for p in sorted(d.glob("C_model__*.json")) if d.is_dir() else []:
            calls = (json.loads(p.read_text(encoding="utf-8")).get("detail") or {}).get("tool_calls") or []
            if calls:
                k = calls[0]
                return bool(k.get("args_match_request")), \
                    (f"{len(calls)} span(s); args_match_request="
                     f"{k.get('args_match_request')}, months_ahead={k.get('months_ahead')}")
        return True, "no Scenario C in this run; skipped"
    c.run("tool-call span logged (ch2 2.5)", spans)

    def cost():
        if "cost_usd_est" not in runs.columns:
            return True, "no cost column; skipped"
        over = []
        for _, r_ in runs.iterrows():
            exp = _EXPECTED_USD.get(str(r_["system"]))
            got = float(r_["cost_usd_est"] or 0)
            if exp and got > exp * _COST_ALARM:
                over.append(f"{r_['system']} ${got:.3f} vs ~${exp:.2f}")
        total = float(runs["cost_usd_est"].fillna(0).sum())
        return not over, (f"total ${total:.3f}" if not over
                          else f"total ${total:.3f}; unexpected: {'; '.join(over)}")
    c.run("cost within an order of magnitude", cost)

    print(f"\n{'=' * 74}")
    if c.failed:
        print(f"  NOT READY -- {len(c.failed)} check(s) failed:")
        for _, n, d in c.failed:
            print(f"    - {n}: {d}")
        print("\n  Do NOT start the funded runs until these pass.")
        print("=" * 74)
        return 1
    print(f"  READY -- all {len(c.rows)} checks passed. The funded set can start.")
    print(f"  Smoke output is in {out_dir}; it is NOT part of the results.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
