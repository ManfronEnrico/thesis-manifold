#!/usr/bin/env python3
"""
SRQ4 Tier 2 — decision-support prompt battery (25 prompts, 5 families).

Scaffolding only: prompt schema, deterministic ground-truth builders, per-family
correctness evaluators, TAR@N aggregation, judge stub. NO API calls in this module
except run-time execution (delegated to srq4_experiment.run_system_a/b) and the
judge (stub, disabled). Everything here is testable offline against the local
feature matrices: `python scripts/srq4_tier2.py --selftest` costs $0.

Prompt spec (JSON list, thesis/data/_08_results_srq4/tier2_prompts.json):
  {"id": "P01", "family": "point|interval|comparison|ranking|seasonality",
   "category": "CSD", "brands": ["HARBOE"], "params": {...}, "text": "..."}
Families / ground truth (all computed from the held-out test month or history):
  point       -> actual units of the first test month           -> APE
  interval    -> same actual                                    -> covered? + rel. width
  comparison  -> which of 2 brands sells more in test month     -> exact match
  ranking     -> top-k brands by test-month units among a set   -> overlap@k
  seasonality -> is month A historically above month B?          -> exact match (yes/no)
"""
import argparse, importlib.util, json, re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("srq4", ROOT / "scripts" / "srq4_experiment.py")
srq4 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(srq4)

FAMILIES = ("point", "interval", "comparison", "ranking", "seasonality")
PROMPTS_FILE = ROOT / "thesis/data/_08_results_srq4/tier2_prompts.json"


# ---------------------------------------------------------------------------
# data access
# ---------------------------------------------------------------------------
def _matrix(category):
    slug, tag, sub = srq4.CAT_FILE[category]
    return pd.read_parquet(ROOT / f"thesis/data/{tag}/{sub}/{slug}_feature_matrix.parquet")


def _test_actual(category, brand):
    _, actual = srq4._brand_history(category, brand)
    return actual


# ---------------------------------------------------------------------------
# ground truth builders (deterministic, from local data only)
# ---------------------------------------------------------------------------
def gt_point(spec):
    return {"actual": _test_actual(spec["category"], spec["brands"][0])}


def gt_interval(spec):
    return {"actual": _test_actual(spec["category"], spec["brands"][0])}


def gt_comparison(spec):
    a, b = spec["brands"][:2]
    va, vb = _test_actual(spec["category"], a), _test_actual(spec["category"], b)
    if va is None or vb is None:
        return {"winner": None}
    return {"winner": a if va > vb else b, "values": {a: va, b: vb}}


def gt_ranking(spec):
    k = spec.get("params", {}).get("k", 3)
    vals = {b: _test_actual(spec["category"], b) for b in spec["brands"]}
    vals = {b: v for b, v in vals.items() if v is not None}
    top = sorted(vals, key=vals.get, reverse=True)[:k]
    return {"top_k": top, "k": k, "values": vals}


def gt_seasonality(spec):
    m_hi = spec["params"]["month_a"]; m_lo = spec["params"]["month_b"]
    fm = _matrix(spec["category"]).dropna(subset=["sales_units"])
    if spec.get("brands"):
        fm = fm[fm.brand.str.upper() == spec["brands"][0].upper()]
    mu = fm.groupby("period_month").sales_units.mean()
    if m_hi not in mu.index or m_lo not in mu.index:
        return {"answer": None}
    return {"answer": "yes" if mu[m_hi] > mu[m_lo] else "no",
            "mean_a": float(mu[m_hi]), "mean_b": float(mu[m_lo])}


GT_BUILDERS = {"point": gt_point, "interval": gt_interval, "comparison": gt_comparison,
               "ranking": gt_ranking, "seasonality": gt_seasonality}


# ---------------------------------------------------------------------------
# answer parsing (sentinel-first, free-text fallback)
# ---------------------------------------------------------------------------
def _nums(text):
    out = []
    for tok in re.findall(r"[\d][\d,\.]*", (text or "").replace(" ", "")):
        try:
            out.append(float(tok.replace(",", "")))
        except ValueError:
            pass
    return out


def parse_point(answer, forecast=None):
    return forecast if forecast is not None else (max(_nums(answer)) if _nums(answer) else None)


def parse_interval(answer):
    m = re.search(r"ANSWER=([\d\.,]+)\s*[;|-]\s*([\d\.,]+)", answer or "")
    if m:
        lo, hi = (float(x.replace(",", "")) for x in m.groups())
        return sorted((lo, hi))
    ns = sorted(_nums(answer))
    return [ns[0], ns[-1]] if len(ns) >= 2 else None


def parse_choice(answer, options):
    up = (answer or "").upper()
    hits = [o for o in options if o.upper() in up]
    if len(hits) == 1:
        return hits[0]
    if hits:  # last mentioned wins (final answer usually at the end)
        return max(hits, key=lambda o: up.rfind(o.upper()))
    return None


def parse_ranklist(answer, options):
    up = (answer or "").upper()
    found = [(up.find(o.upper()), o) for o in options if o.upper() in up]
    return [o for _, o in sorted(found)] or None


def parse_yesno(answer):
    up = (answer or "").strip().upper()
    m = re.search(r"ANSWER=(YES|NO)", up)
    if m:
        return m.group(1).lower()
    for w, v in (("YES", "yes"), ("NO", "no")):
        if re.search(rf"\b{w}\b", up):
            return v
    return None


# ---------------------------------------------------------------------------
# per-family correctness evaluators -> dict(score in [0,1], detail)
# ---------------------------------------------------------------------------
def eval_point(gt, answer, forecast=None):
    yhat = parse_point(answer, forecast)
    if yhat is None or not gt.get("actual"):
        return {"ok": None, "ape": None}
    ape = abs(yhat - gt["actual"]) / gt["actual"] * 100
    return {"ok": ape <= 30, "ape": round(ape, 2), "parsed": yhat}


def eval_interval(gt, answer, forecast=None):
    iv = parse_interval(answer)
    if iv is None or not gt.get("actual"):
        return {"ok": None, "covered": None}
    lo, hi = iv
    covered = lo <= gt["actual"] <= hi
    width = (hi - lo) / gt["actual"] * 100
    return {"ok": covered, "covered": covered, "rel_width_pct": round(width, 1), "parsed": iv}


def eval_comparison(gt, answer, forecast=None, options=()):
    pick = parse_choice(answer, options or list(gt.get("values", {})))
    if pick is None or gt.get("winner") is None:
        return {"ok": None}
    return {"ok": pick.upper() == gt["winner"].upper(), "parsed": pick}


def eval_ranking(gt, answer, forecast=None, options=()):
    lst = parse_ranklist(answer, options or list(gt.get("values", {})))
    if not lst or not gt.get("top_k"):
        return {"ok": None, "overlap": None}
    k = gt["k"]
    ov = len(set(x.upper() for x in lst[:k]) & set(x.upper() for x in gt["top_k"])) / k
    return {"ok": ov >= 2 / 3, "overlap": round(ov, 2), "parsed": lst[:k]}


def eval_seasonality(gt, answer, forecast=None):
    ans = parse_yesno(answer)
    if ans is None or gt.get("answer") is None:
        return {"ok": None}
    return {"ok": ans == gt["answer"], "parsed": ans}


EVALUATORS = {"point": eval_point, "interval": eval_interval, "comparison": eval_comparison,
              "ranking": eval_ranking, "seasonality": eval_seasonality}


# ---------------------------------------------------------------------------
# judge stub (quality/faithfulness only — correctness stays deterministic)
# ---------------------------------------------------------------------------
def judge_answer(prompt_text, answer, gt):
    """LLM-as-judge (separate model, GPT-4o) for faithfulness/clarity. DISABLED in
    Fase 1 — implemented after the 25-prompt review. Never used for correctness."""
    raise NotImplementedError("judge disabled until prompt review checkpoint")


# ---------------------------------------------------------------------------
# selftest — $0, no API
# ---------------------------------------------------------------------------
def selftest():
    print("== parsing ==")
    assert parse_point("about 26,083,132 units", None) == 26083132.0
    assert parse_interval("range ANSWER=100-200 done") == [100.0, 200.0]
    assert parse_interval("between 22,326,008 and 30,472,519 units") == [22326008.0, 30472519.0]
    assert parse_choice("PEPSI will outsell it", ["PEPSI", "FAXE KONDI"]) == "PEPSI"
    assert parse_yesno("ANSWER=YES because December peaks") == "yes"
    assert parse_ranklist("1. HARBOE 2. PEPSI 3. FANTA", ["PEPSI", "FANTA", "HARBOE", "COCA COLA"]) == ["HARBOE", "PEPSI", "FANTA"]
    print("   ok")

    print("== evaluators (synthetic) ==")
    assert eval_point({"actual": 100.0}, "ANSWER 105")["ok"] is True
    assert eval_point({"actual": 100.0}, "1,000,000")["ok"] is False
    assert eval_interval({"actual": 100.0}, "90 to 120")["covered"] is True
    assert eval_comparison({"winner": "A", "values": {"A": 2, "B": 1}}, "A wins", options=["A", "B"])["ok"] is True
    assert eval_seasonality({"answer": "yes"}, "Yes, clearly")["ok"] is True
    print("   ok")

    print("== ground truth su dati reali (CSD) ==")
    g1 = gt_point({"category": "CSD", "brands": ["HARBOE"]})
    print(f"   point HARBOE: actual={g1['actual']:,.0f}")
    g2 = gt_comparison({"category": "CSD", "brands": ["PEPSI", "FAXE KONDI"]})
    print(f"   comparison PEPSI vs FAXE KONDI: winner={g2['winner']} values={ {k: f'{v:,.0f}' for k, v in g2['values'].items()} }")
    g3 = gt_ranking({"category": "CSD", "brands": ["HARBOE", "PEPSI", "FANTA", "COCA COLA", "FAXE KONDI"], "params": {"k": 3}})
    print(f"   ranking top-3: {g3['top_k']}")
    g4 = gt_seasonality({"category": "CSD", "brands": [], "params": {"month_a": 12, "month_b": 2}})
    print(f"   seasonality dic>feb: {g4['answer']} (dic={g4['mean_a']:,.0f} feb={g4['mean_b']:,.0f})")
    assert g1["actual"] and g2["winner"] and len(g3["top_k"]) == 3 and g4["answer"]
    print("SELFTEST PASS — zero API, zero dollari")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    else:
        print("Tier 2 runner arrives after the 25-prompt review checkpoint. Use --selftest.")


if __name__ == "__main__":
    main()
