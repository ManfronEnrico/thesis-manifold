#!/usr/bin/env python3
"""
Read back what a scenario run actually did. Makes no API calls.

WHY: the run log is only useful if it can be interrogated without writing
throwaway code each time. This is the auditing surface -- given a results
directory it answers, from the stored evidence rather than from assertion:

  - what exactly was each arm asked?
  - did the LLM call the tool, and with which arguments?
  - what code did Arm B write?
  - what did Arm C search for, and might it have retrieved the answer?
  - where did the money and time go?

Usage:
    python inspect_runs.py                        # summary of the default results dir
    python inspect_runs.py --dir path/to/results
    python inspect_runs.py --run A_dedicated__CSD_HARBOE__rep0   # one run in full
    python inspect_runs.py --code                 # every code block Arm B wrote
    python inspect_runs.py --leakage              # Arm C retrieval audit
    python inspect_runs.py --prompts              # the prompt each arm received
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def _default_dir():
    from PATHS import THESIS_RESULTS_SRQ4_DIR
    return THESIS_RESULTS_SRQ4_DIR


def _load(d: Path):
    raw = d / "raw_responses"
    if not raw.is_dir():
        return []
    out = []
    for f in sorted(raw.glob("*.json")):
        try:
            out.append((f.stem, json.loads(f.read_text(encoding="utf-8"))))
        except Exception as e:
            print(f"  ! unreadable {f.name}: {e}")
    return out


def _rule(t):
    print("\n" + "=" * 76)
    print(t)
    print("=" * 76)


def summary(runs):
    _rule("RUNS")
    if not runs:
        print("  no cached responses found")
        return
    print(f"{'run':46s} {'outcome':11s} {'forecast':>13s} {'cost':>8s}")
    print("-" * 82)
    for name, d in runs:
        tr = d.get("trace") or {}
        fc = d.get("forecast")
        # forecast is not stored at top level for every arm; fall back to the
        # value the run row carried.
        fcs = f"{fc:,.0f}" if isinstance(fc, (int, float)) else "-"
        print(f"{name:46s} {str(tr.get('arm','?')):11s} {fcs:>13s} "
              f"${d.get('cost_usd_est') or 0:>7.4f}")

    tot = sum(d.get("cost_usd_est") or 0 for _, d in runs)
    ti = sum(d.get("tokens_in") or 0 for _, d in runs)
    to = sum(d.get("tokens_out") or 0 for _, d in runs)
    tr_ = sum(d.get("tokens_reasoning") or 0 for _, d in runs)
    print("-" * 82)
    print(f"{len(runs)} runs   tokens in={ti:,} out={to:,} "
          f"(reasoning={tr_:,}, {100*tr_/max(to,1):.0f}% of output)   "
          f"est=${tot:.4f}")


def show_prompts(runs):
    _rule("PROMPTS -- exactly what each arm was asked")
    seen = set()
    for name, d in runs:
        arm = (d.get("trace") or {}).get("arm", "?")
        if arm in seen:
            continue
        seen.add(arm)
        print(f"\n--- {arm} (from {name}) ---")
        p = d.get("prompt")
        if not p:
            print("  (no prompt stored)")
            continue
        # Arm B embeds the full CSV; elide the middle so the instruction stays legible.
        if len(p) > 1200:
            print(p[:600] + f"\n  ... [{len(p)-1100} chars of data elided] ...\n" + p[-500:])
        else:
            print(p)


def show_tool_calls(runs):
    _rule("TOOL CALLS -- how Arm A reached the trained model")
    any_ = False
    for name, d in runs:
        det = d.get("detail") or {}
        for tc in det.get("tool_calls") or []:
            any_ = True
            match = tc.get("args_match_request")
            flag = "" if match else "   <-- MISMATCH: LLM queried a different series"
            print(f"\n{name}")
            print(f"  requested : {tc.get('requested_category')} / {tc.get('requested_brand')}")
            print(f"  LLM asked : {tc.get('llm_arg_category')} / {tc.get('llm_arg_brand')}{flag}")
            out = tc.get("tool_output") or {}
            if out.get("status") == "ok":
                print(f"  returned  : {out.get('forecast_units'):,.0f} units, "
                      f"90% [{out['interval_90'][0]:,.0f} - {out['interval_90'][1]:,.0f}], "
                      f"{out.get('confidence_tier')} confidence")
                print(f"  provenance: model={out.get('model')} "
                      f"month={out.get('forecast_month')} "
                      f"trained_through={out.get('trained_through')}")
                print(f"  interval  : {out.get('interval_method')}")
            else:
                print(f"  returned  : {out}")
    if not any_:
        print("  no tool calls recorded (Arm A not in this run set)")


def show_code(runs):
    _rule("GENERATED CODE -- what Arm B actually wrote")
    any_ = False
    for name, d in runs:
        blocks = ((d.get("detail") or {}).get("code_blocks")) or []
        if not blocks:
            continue
        any_ = True
        print(f"\n--- {name}: {len(blocks)} block(s) ---")
        for i, b in enumerate(blocks, 1):
            code = (b.get("code") or "").strip()
            print(f"\n  [block {i}] status={b.get('status')}")
            for line in code.splitlines()[:40]:
                print("    " + line)
            if len(code.splitlines()) > 40:
                print(f"    ... ({len(code.splitlines())-40} more lines)")
    if not any_:
        print("  no code blocks recorded (Arm B not in this run set)")


def show_leakage(runs):
    _rule("LEAKAGE AUDIT -- Arm C retrieval risk")
    print("The held-out months are in the past, so a published figure may exist.")
    print("Runs flagged below cite the target month and should be read before use.\n")
    any_ = False
    for name, d in runs:
        tr = d.get("trace") or {}
        if tr.get("arm") != "C_nodata":
            continue
        any_ = True
        susp = tr.get("retrieval_suspected")
        print(f"{name}")
        print(f"  target month        : {tr.get('target_month')}")
        print(f"  used web search     : {tr.get('used_web')}")
        print(f"  retrieval_suspected : {susp}"
              + ("   <-- INSPECT the answer text" if susp else ""))
        qs = ((d.get("detail") or {}).get("web_queries")) or []
        if qs:
            print(f"  queries             : {[q for q in qs if q][:5]}")
    if not any_:
        print("  no Arm C runs in this set")


def show_one(runs, key):
    hits = [(n, d) for n, d in runs if key in n]
    if not hits:
        print(f"no run matching {key!r}")
        return
    for name, d in hits:
        _rule(f"RUN: {name}")
        print(json.dumps(d, indent=2, default=str)[:12000])


def main():
    ap = argparse.ArgumentParser(description="Inspect SRQ4 scenario run logs")
    ap.add_argument("--dir", default=None, help="results dir (default: SRQ4 results dir)")
    ap.add_argument("--run", default=None, help="dump one run in full (substring match)")
    ap.add_argument("--prompts", action="store_true")
    ap.add_argument("--tools", action="store_true")
    ap.add_argument("--code", action="store_true")
    ap.add_argument("--leakage", action="store_true")
    ap.add_argument("--all", action="store_true", help="every section")
    a = ap.parse_args()

    d = Path(a.dir) if a.dir else _default_dir()
    print(f"results dir: {d}")
    runs = _load(d)
    if not runs:
        print("No cached responses. Run the experiment first, or pass --dir.")
        return 1

    if a.run:
        show_one(runs, a.run)
        return 0

    summary(runs)
    if a.prompts or a.all:
        show_prompts(runs)
    if a.tools or a.all:
        show_tool_calls(runs)
    if a.code or a.all:
        show_code(runs)
    if a.leakage or a.all:
        show_leakage(runs)
    if not any([a.prompts, a.tools, a.code, a.leakage, a.all]):
        print("\n(--prompts / --tools / --code / --leakage / --all for detail)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
