#!/usr/bin/env python3
"""
Pre-flight check for the SRQ4 experiment. Costs nothing; makes no paid API calls
unless --live is passed.

WHY: a paid, non-deterministic run that fails 40 observations in has wasted both
money and the runs already completed. Every failure mode found so far --
missing credentials, a stale module path, an unsupported decoding parameter, an
arm scored on the wrong month -- was detectable before spending anything.

Checks, in order of what they would cost you to discover late:

  1. Credentials resolve, and the two key scopes are actually distinct
  2. The pinned model exists on this account
  3. Feature matrices load for every category
  4. LEAKAGE: the held-out month never appears in the data an arm receives
  5. Every arm is scored on the same target month
  6. The forecast tool returns a complete payload
  7. (--live) one real call per arm, to confirm the API contract still holds

Usage:
    python 03_thesis_modelling/scenario_setup/verify_setup.py
    python 03_thesis_modelling/scenario_setup/verify_setup.py --live   # ~$0.30
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load_harness():
    spec = importlib.util.spec_from_file_location("srq4", HERE / "srq4_experiment.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Checks:
    """Collects results so a single failure does not hide the ones after it --
    seeing every problem at once is the point of a pre-flight."""

    def __init__(self):
        self.rows = []

    def add(self, ok, name, detail=""):
        self.rows.append((ok, name, detail))
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}" + (f"\n         {detail}" if detail else ""))
        return ok

    def run(self, name, fn):
        try:
            ok, detail = fn()
            return self.add(ok, name, detail)
        except Exception as e:
            return self.add(False, name, f"{type(e).__name__}: {e}")

    @property
    def failed(self):
        return [r for r in self.rows if not r[0]]


def main():
    ap = argparse.ArgumentParser(description="SRQ4 pre-flight verification")
    ap.add_argument("--live", action="store_true",
                    help="also make one real API call per arm (~$0.30)")
    ap.add_argument("--category", default="CSD")
    ap.add_argument("--brand", default="HARBOE")
    a = ap.parse_args()

    print("=" * 74)
    print("SRQ4 PRE-FLIGHT")
    print("=" * 74)

    c = Checks()

    print("\n-- credentials ---------------------------------------------------")
    m = _load_harness()

    def keys():
        proj = os.environ.get("OPENAI_API_KEY")
        adm = os.environ.get("OPENAI_ADMIN_KEY")
        if not proj:
            return False, "OPENAI_API_KEY absent. Needed by every arm."
        if not adm:
            return True, ("OPENAI_ADMIN_KEY absent -- runs will work, but cost "
                          "cannot be reconciled against actual billing.")
        return True, f"project key {len(proj)} chars, admin key {len(adm)} chars"
    c.run("credentials resolve", keys)

    def scopes():
        # The two keys must NOT be interchangeable. If the project key could read
        # billing, it would mean an over-scoped key is in use.
        import json as _j, urllib.request
        proj = os.environ.get("OPENAI_API_KEY")
        adm = os.environ.get("OPENAI_ADMIN_KEY")
        if not (proj and adm):
            return True, "skipped (admin key absent)"

        def status(key, url):
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
            try:
                urllib.request.urlopen(req, timeout=20)
                return 200
            except Exception as e:
                return getattr(e, "code", 0)
        import time
        start = int(time.time()) - 3600
        p_models = status(proj, "https://api.openai.com/v1/models")
        p_costs = status(proj, f"https://api.openai.com/v1/organization/costs?start_time={start}")
        a_costs = status(adm, f"https://api.openai.com/v1/organization/costs?start_time={start}")
        ok = p_models == 200 and p_costs == 403 and a_costs == 200
        return ok, (f"project: models={p_models} costs={p_costs} | "
                    f"admin: costs={a_costs} (expect 200/403/200)")
    c.run("key scopes are disjoint", scopes)

    print("\n-- configuration -------------------------------------------------")

    def model():
        from openai import OpenAI
        OpenAI().models.retrieve(m.MODEL)
        return True, f"{m.MODEL} reachable"
    c.run("pinned model exists", model)

    def snapshot():
        # A floating alias silently re-points mid-study; a dated snapshot cannot.
        dated = any(ch.isdigit() for ch in m.MODEL.split("-")[-1])
        return dated, (f"{m.MODEL} is a dated snapshot" if dated
                       else f"{m.MODEL} looks like a floating alias -- pin a dated snapshot")
    c.run("model is a dated snapshot", snapshot)

    def decoding():
        # Recorded rather than assumed: the harness must not claim a control the
        # API refuses to accept.
        if m.TEMPERATURE is not None:
            return False, ("TEMPERATURE is set, but this model line rejects it. "
                           "The write-up would claim a control that was never applied.")
        return True, f"temperature not settable; recorded as: {m.DECODING_NOTE}"
    c.run("decoding claim matches reality", decoding)

    print("\n-- data ----------------------------------------------------------")

    def matrices():
        import pandas as pd
        missing = []
        for cat, (slug, tag, sub) in m.CAT_FILE.items():
            f = m._engineered_dir(tag, sub) / f"{slug}_feature_matrix_h3.parquet"
            if not f.is_file():
                missing.append(f"{cat}: {f.name}")
        return (not missing), ("all 4 categories load" if not missing
                               else "missing: " + "; ".join(missing))
    c.run("feature matrices present", matrices)

    def leakage():
        # The check that matters most: a leak does not raise, it just makes Arm B
        # look brilliant -- the exact quantity under measurement.
        problems, checked = [], 0
        for cat in m.CAT_FILE:
            for br in [b for cc, b in m._select_brands((2, 2, 2, 2)) if cc == cat][:2]:
                try:
                    fit, actual, target = m._brand_history(cat, br)
                    checked += 1
                    if actual is None:
                        problems.append(f"{cat}/{br}: no held-out actual")
                        continue
                    if (fit.sales_units == actual).any():
                        problems.append(f"{cat}/{br}: held-out VALUE present in history")
                    ty, tm = int(target[:4]), int(target[5:7])
                    last = fit.sort_values(["period_year", "period_month"]).iloc[-1]
                    if (int(last.period_year), int(last.period_month)) >= (ty, tm):
                        problems.append(f"{cat}/{br}: history reaches the target month")
                except AssertionError as e:
                    problems.append(str(e)[:120])
        return (not problems), (f"{checked} brand-series clean, target month absent "
                                f"from every history" if not problems
                                else "; ".join(problems[:4]))
    c.run("LEAKAGE: target month excluded from arm data", leakage)

    def same_month():
        # Arms scored on different months are incomparable, not merely different.
        _, _, t = m._brand_history(a.category, a.brand)
        tool = m._eval_forecast(a.category, a.brand)
        ok = tool.get("forecast_month") == t
        return ok, (f"history target={t}, tool forecast_month={tool.get('forecast_month')}")
    c.run("all arms target the same month", same_month)

    print("\n-- tool contract -------------------------------------------------")

    def tool_payload():
        need = {"forecast_units", "interval_90", "confidence_tier",
                "forecast_month", "trained_through", "interval_method", "model"}
        out = m._eval_forecast(a.category, a.brand)
        missing = need - set(out)
        return (not missing), (f"complete: {out['forecast_units']:,.0f} units, "
                               f"{out['confidence_tier']} confidence, "
                               f"trained through {out['trained_through']}"
                               if not missing else f"missing fields: {sorted(missing)}")
    c.run("forecast tool returns a full payload", tool_payload)

    def prompts_module():
        sys.path.insert(0, str(HERE))
        import prompts as P
        _, _, t = m._brand_history(a.category, a.brand)
        pa = P.arm_a_prompt(a.brand, a.category, t)
        pc = P.arm_c_prompt(a.brand, a.category, t)
        # Every arm must name the month; "next month" is what broke Arm C before.
        ok = t in pa and t in pc and "next month" not in pc.lower()
        return ok, f"target {t} named in every arm prompt"
    c.run("prompts name the target month", prompts_module)

    if a.live:
        print("\n-- live API (paid) -----------------------------------------------")
        for name, fn in m.ARMS:
            def call(name=name, fn=fn):
                r = fn(a.category, a.brand)
                if r.get("error"):
                    return False, r["error"][:200]
                cls = m._classify(r.get("forecast"), r.get("hit_limit"),
                                  r.get("error"), None)
                return cls == "ok", (f"forecast={r.get('forecast')} "
                                     f"latency={r.get('latency_s')}s "
                                     f"est=${r.get('cost_usd_est') or 0:.4f} "
                                     f"outcome={cls}")
            c.run(f"{name} completes", call)

    print("\n" + "=" * 74)
    if c.failed:
        print(f"NOT READY -- {len(c.failed)} check(s) failed:")
        for _, n, d in c.failed:
            print(f"  - {n}: {d}")
        print("=" * 74)
        return 1
    print(f"READY -- all {len(c.rows)} checks passed.")
    if not a.live:
        print("Re-run with --live to confirm the API contract (~$0.30).")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
