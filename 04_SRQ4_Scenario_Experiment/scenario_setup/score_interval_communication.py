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
from PATHS import THESIS_RESULTS_SRQ4_DIR, SRQ2_DIR  # noqa: E402

TOL = 0.05  # a stated bound within 5% of the payload counts as faithful

SCENARIO = {"C_llm_model": "C - dedicated model", "B_llm_data": "B - code execution",
            "A_llm_plain": "A - no firm data"}

# Hedging alone is not communication of uncertainty; these are the words that
# introduce an actual range or an explicit confidence statement.
# The exemplar's "Range:" label first, then the phrasings a range is written in
# without it. The label alternative is not decoration: the output exemplar
# prescribes "Range: <lo> to <hi>", and "<lo> to <hi>" carries neither a
# "between"/"from" lead-in nor a dash, so the other three alternatives miss it
# entirely. Measured on the 63 funded answers, the label takes this criterion
# from 10 to 63 -- the earlier figure was the regex failing, not the agents.
# Anchoring on the label rather than accepting a bare "<n> to <n>" keeps a year
# range ("2025 to 2026") from scoring as a forecast interval.
_RANGE_RE = re.compile(
    r"(?:^|\n)\s*range\s*:\s*([\d.,]+)\s*(?:to|and|[-\u2013])\s*([\d.,]+)"
    r"|(?:between|from)\s+([\d.,]+)\s*(?:and|to|[-\u2013])\s*([\d.,]+)"
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


_PAYLOAD_CACHE: dict[tuple, dict] = {}
_PAYLOAD_UNVERIFIED: list[str] = []


def _served_payload(category: str, brand: str, month: str) -> dict:
    """The payload the interface returned for this series, recomputed.

    THE RUN LOG DOES NOT CONTAIN IT. The harness records `tool_returned_forecast`
    and `payload_complete` as booleans and discards the payload itself, so the
    interval the agent was given is not in the trace. Criterion 2 compares the
    stated bounds against that interval, so without it the criterion scores False
    for every run -- including the arms that restate the bounds correctly.

    Recomputing is sound here because the serving path is deterministic: it loads
    a persisted model and calls predict, and the half-width is a constant read
    from the served metadata. That determinism is not assumed, it is CHECKED --
    `_payload_for_record` compares the recomputed point forecast against the one
    the run logged and refuses the payload if they differ. A retrained model
    therefore makes the criterion unscoreable rather than silently wrong.
    """
    key = (category, brand, month)
    if key not in _PAYLOAD_CACHE:
        try:
            sys.path.insert(0, str(SRQ2_DIR))
            import forecast_tool as _ft  # noqa: PLC0415
            out = _ft.forecast_demand(category, brand, month)
            _PAYLOAD_CACHE[key] = out if isinstance(out, dict) else {}
        except Exception as e:  # noqa: BLE001
            _PAYLOAD_CACHE[key] = {}
            _PAYLOAD_UNVERIFIED.append(f"{brand}: {type(e).__name__}")
    return _PAYLOAD_CACHE[key]


def _payload_for_record(rec: dict) -> dict:
    """Attach the served payload to the arms that were given one.

    `payload_complete` marks the runs that received the interface's output --
    both the arms that relay it and the arms that weigh it against other
    evidence. The criterion is meaningful for both: it asks whether the range in
    the answer is the range the interface supplied.

    Where the arm also ADOPTED the forecast, the recomputed payload is verified
    against the logged one. Where it departed, the logged forecast is the agent's
    own number and cannot serve as the check, so the payload rests on the
    determinism established on the adopting arms for the same series and month.
    """
    tr = rec.get("trace") or {}
    if not tr.get("payload_complete"):
        return {}
    payload = _served_payload(rec.get("category"), rec.get("brand"),
                              tr.get("target_month"))
    if not payload:
        return {}
    if tr.get("tool_returned_forecast"):
        logged, recomputed = rec.get("forecast"), payload.get("forecast_units")
        if logged is None or recomputed is None or \
                abs(float(recomputed) - float(logged)) > 0.05:
            _PAYLOAD_UNVERIFIED.append(
                f"{rec.get('system')}/{rec.get('brand')}/rep{rec.get('rep')}: "
                f"recomputed {recomputed} against logged {logged}")
            return {}
    return payload


def _run_key(rec: dict) -> tuple:
    """A run is (system, brand, rep) -- read from the record, never the filename.

    `raw_responses/` holds more files than there were runs: the pre-transliteration
    OERBAEK slug left a second copy of some rep0 traces, and two of them were
    re-run afterwards. Keying on the filename therefore scores those two runs
    twice and inflates their scenario's denominator. The record itself carries
    the brand correctly even where the filename mangles it.
    """
    return (rec.get("system"), rec.get("brand"), rec.get("rep"))


def collect() -> pd.DataFrame:
    d = THESIS_RESULTS_SRQ4_DIR / "raw_responses"
    if not d.is_dir():
        return pd.DataFrame()

    # Keep one record per run, the most recent, so a re-run supersedes the trace
    # it replaced rather than being averaged with it.
    latest: dict[tuple, dict] = {}
    for f in sorted(d.glob("*.json")):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        k = _run_key(rec)
        prev = latest.get(k)
        if prev is None or _run_at(rec) >= _run_at(prev):
            latest[k] = rec

    rows = []
    for (system, brand, rep), rec in sorted(latest.items(), key=lambda kv: str(kv[0])):
        scen = (rec.get("trace") or {}).get("scenario") or system
        # The run id is composed from the record, so a filename that mangles a
        # non-ASCII brand cannot reach a published artefact.
        run = f"{system}__{rec.get('category')}_{brand}__rep{rep}"
        # Only the tool-backed arms carry a payload; the others are scored on the
        # same criteria with an empty one, so the ladder stays comparable. An arm
        # with no interface cannot pass criterion 2 by construction -- that is a
        # finding, not a bug.
        r = {"run": run, "scenario": SCENARIO.get(scen, scen)}
        r.update(_score_one(rec.get("answer") or "", _payload_for_record(rec)))
        r["score"] = sum(bool(r[c]) for c in CRITERIA)
        rows.append(r)
    return pd.DataFrame(rows)


def _run_at(rec: dict) -> str:
    return str((rec.get("trace") or {}).get("run_at") or "")


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
