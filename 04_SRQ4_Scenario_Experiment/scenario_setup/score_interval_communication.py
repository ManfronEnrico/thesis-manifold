#!/usr/bin/env python
"""Score whether an agent COMMUNICATED forecast uncertainty, not just whether the
forecast was accurate.

WHY THIS EXISTS
---------------
Chapter 2 builds its decision-support argument on Goodwin, Onkal and Thomson
(2010), who gave participants a newsvendor task under asymmetric shortage and
surplus costs. Supplying 50% or 95% prediction intervals alongside the point
forecast did not improve decisions; it made them worse. Correct discrimination
between the two cost regimes fell from roughly 84% under point forecasts to 44%
under 95% intervals, because participants anchored on the interval midpoint
instead of shifting toward the expensive side of the loss function.

The chapter draws the right conclusion: a bare numeric range is not
self-interpreting, and the interpretive step between the interval and the
decision is where the value lies -- which is exactly what an agentic layer is
positioned to supply.

But SRQ4 scores absolute percentage error. It measures whether the number was
right, never whether the agent made the uncertainty usable. The literature
review therefore argues for a capability the evaluation is silent on.

This module closes that gap WITHOUT new API spend. Every scenario-C run already
logs the tool payload (`forecast_units`, `interval_90`, `confidence`,
`confidence_tier`) and the answer text, so communication can be scored
retrospectively against runs already paid for.

WHAT IT DOES NOT CLAIM
----------------------
This measures whether the artefact COMMUNICATED the interval. It does NOT show
that human decisions improved -- that would require Goodwin's own design, with
participants and ethics approval, and is out of scope. State the boundary
explicitly wherever these numbers are used.

WHY NO LLM JUDGE
----------------
Every check here is deterministic and rule-based: numeric extraction and
matching against the payload the tool actually returned. A judge would add
non-determinism and its own bias controls (Gu et al., 2025; Ye et al., 2024) to
a question arithmetic already answers. This is the same reasoning that keeps
correctness on APE rather than on a rubric.

THE FOUR CRITERIA
-----------------
  1. states_interval   -- is a range reported at all
  2. interval_faithful -- do the stated bounds match the tool payload (5% tol)
  3. states_confidence -- is the confidence level or tier reported
  4. gives_recommendation -- is a course of action proposed, not merely a number

Criterion 2 is the ANAH principle of Chapter 2.5 applied to the interval: a
generated statement is assessable only against an explicitly retrieved source.
It is the same check `args_match_request` performs for the point forecast, and
catches an agent that reports a plausible but invented range.

ON THE RECOMMENDATION CRITERION
-------------------------------
This criterion is scoreable only because the shared question asks for a
recommendation. It briefly did not: an earlier version of the question asked
only for a number, a range and a confidence, and scoring a recommendation
against it measured compliance with an instruction never given -- a finding
about the prompt rather than about the scenario. The question was changed
(identically for all three scenarios, so no factor varies between them) rather
than the criterion quietly dropped, because Goodwin's result makes the
interpretive step the part that carries the decision value.

Runs logged BEFORE that prompt change cannot be scored on this criterion, and
must not be pooled with runs asked the newer question.

EVERY FIGURE HERE IS COMPUTED, NOT INFERRED
-------------------------------------------
Each criterion is a regular-expression extraction followed by a numeric
comparison against the payload the tool returned. Percentages are counts divided
by the number of scored answers. Nothing in this module asks a language model to
judge anything, and re-running it on the same inputs returns the same numbers.

Usage
-----
    python 03_thesis_modelling/scenario_setup/score_interval_communication.py

Reads:  04_thesis_results/srq4/raw_responses/*.json
Writes: 04_thesis_results/srq4/interval_communication.csv
        04_thesis_results/srq4/interval_communication.md
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_SRQ4_DIR  # noqa: E402

TOL = 0.05  # a stated bound within 5% of the payload counts as faithful

SCENARIO = {"C_model": "C - dedicated model", "B_data": "B - code execution",
            "A_plain": "A - no firm data"}

# Hedging alone is not communication of uncertainty; these are the words that
# introduce an actual range or an explicit confidence statement.
_RANGE_RE = re.compile(
    r"(?:between|from)\s+([\d.,]+)\s*(?:and|to|[-\u2013])\s*([\d.,]+)"
    r"|([\d.,]+)\s*[-\u2013]\s*([\d.,]+)"
    r"|\u00b1\s*([\d.,]+)", re.I)
_CONF_RE = re.compile(
    r"\b(90\s*%|confidence|interval|uncertain|prediction interval"
    r"|high confidence|medium confidence|low confidence)\b", re.I)
# Matches the exemplar's "Recommendation:" label first, then falls back to the
# verbs a recommendation is actually phrased with, so an answer that gives advice
# without adopting the label still scores.
_REC_RE = re.compile(
    r"(^|\n)\s*recommendation\s*:"
    r"|\b(recommend|advise|suggest|should|plan (?:for|against)|order|stock"
    r"|hold cover|increase|decrease|reduce|maintain)\b", re.I)


def _nums(s: str) -> list[float]:
    out = []
    for m in _RANGE_RE.finditer(s or ""):
        for g in m.groups():
            if g:
                try:
                    out.append(float(g.replace(",", "")))
                except ValueError:
                    pass
    return out


def _score_one(answer: str, payload: dict) -> dict:
    """Four deterministic checks against the tool payload."""
    a = answer or ""
    iv = payload.get("interval_90") or []
    lo, hi = (iv + [None, None])[:2]

    stated = _nums(a)
    states_interval = len(stated) >= 2

    # Faithful if BOTH bounds appear within tolerance. An agent that states only
    # one bound, or invents a range, fails -- which is the point.
    faithful = False
    if states_interval and lo is not None and hi is not None:
        got_lo = any(abs(v - lo) <= abs(lo) * TOL for v in stated)
        got_hi = any(abs(v - hi) <= abs(hi) * TOL for v in stated)
        faithful = got_lo and got_hi

    return {
        "states_interval": states_interval,
        "interval_faithful": faithful,
        "states_confidence": bool(_CONF_RE.search(a)),
        "gives_recommendation": bool(_REC_RE.search(a)),
    }


CRITERIA = ["states_interval", "interval_faithful", "states_confidence",
            "gives_recommendation"]
LABEL = {"states_interval": "States a range",
         "interval_faithful": "Range matches the tool output",
         "states_confidence": "States confidence",
         "gives_recommendation": "Proposes a course of action"}


def collect() -> pd.DataFrame:
    rows = []
    d = THESIS_RESULTS_SRQ4_DIR / "raw_responses"
    if not d.is_dir():
        return pd.DataFrame()
    for f in sorted(d.glob("*.json")):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        scen = (rec.get("trace") or {}).get("scenario") or f.stem.split("__")[0]
        answer = rec.get("answer") or ""
        # Only scenario C has a tool payload; A and B are scored on the same
        # criteria with an empty payload, so the ladder stays comparable. A
        # cannot pass criterion 2 by construction -- that is a finding, not a bug.
        payload = {}
        for tc in (rec.get("tool_calls") or []):
            payload = tc.get("tool_output") or {}
            break
        r = {"run": f.stem, "scenario": SCENARIO.get(scen, scen)}
        r.update(_score_one(answer, payload))
        r["score"] = sum(bool(r[c]) for c in CRITERIA)
        rows.append(r)
    return pd.DataFrame(rows)


def main() -> None:
    df = collect()
    if df.empty:
        print("No logged responses found -- run the experiment first.")
        return

    out = THESIS_RESULTS_SRQ4_DIR / "interval_communication.csv"
    df.to_csv(out, index=False, encoding="utf-8")

    scenarios = sorted(df.scenario.unique())
    hdr = {s_: f"{s_} (n={len(df[df.scenario == s_])})" for s_ in scenarios}
    rows = []
    for c in CRITERIA:
        r = {"Criterion": LABEL[c]}
        for s_ in scenarios:
            d = df[df.scenario == s_]
            r[hdr[s_]] = (f"{d[c].sum():.0f} of {len(d)} ({d[c].mean()*100:.0f})"
                          if len(d) else "")
        rows.append(r)
    r = {"Criterion": f"Mean criteria met (of {len(CRITERIA)})"}
    for s_ in scenarios:
        d = df[df.scenario == s_]
        r[hdr[s_]] = f"{d.score.mean():.2f}" if len(d) else ""
    rows.append(r)
    tbl = pd.DataFrame(rows)

    md = [
        "**Communication of forecast uncertainty by scenario.** Number of answers "
        "meeting each criterion, with the percentage in parentheses, scored "
        "against the payload the forecasting tool returned. n denotes the number "
        "of answers scored.", "",
        tbl.to_markdown(index=False), "",
        "*Note.* Goodwin, Onkal and Thomson (2010) show that a prediction interval "
        "presented as a bare numeric range does not improve decisions and can "
        "degrade them, because the interpretive step from interval to decision is "
        "left to the reader. These criteria record whether that step was supplied: "
        "whether a range was stated, whether the stated range corresponds to the "
        "one the model produced, whether the associated confidence was "
        "reported, and whether a course of action was proposed. Each is "
        "evaluated by direct comparison of the numbers in the "
        "answer against the numbers the tool returned, with a five per cent "
        "tolerance; no judgement is involved. A scenario without access to the "
        "forecasting tool cannot satisfy the second criterion, which requires a "
        "retrieved source against which a stated range can be checked.", "",
        "*These measures concern what the system communicated. Whether such "
        "communication improves the decisions of human planners is not examined "
        "in this thesis, and would require a controlled decision experiment with "
        "human participants.*", "",
        f"_Scored over {len(df)} logged responses._",
    ]
    (THESIS_RESULTS_SRQ4_DIR / "interval_communication.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8", newline="\n")

    print("\n".join(md))
    print(f"\nSaved {out.name} + interval_communication.md")


if __name__ == "__main__":
    main()
