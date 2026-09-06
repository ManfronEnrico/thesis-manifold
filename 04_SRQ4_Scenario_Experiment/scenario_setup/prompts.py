#!/usr/bin/env python3
"""
Every prompt used in the SRQ4 experiment, in one place.

WHY THIS FILE EXISTS
--------------------
Prompts are the experimental instrument. If they live inline in the harness, a
reviewer asking "show me exactly what you asked the model" gets pointed at
source code interleaved with API plumbing, and a change to a prompt looks like a
change to the runner. Here they are inspectable, diffable, and quotable in the
methodology appendix without transcription.

THE SHARED QUESTION
-------------------
All three scenarios are asked the SAME user question, verbatim:

    How many units of {brand} will be sold in the {category} category in
    Danish retail in {target}? Answer in units sold, not currency. Give the
    number, a range, how confident you are, and what you would recommend the
    category planner do about it.

This is deliberate and it is the core of the single-variable design. An earlier
version gave each scenario differently-worded instructions -- Scenario A got a
paragraph about not searching, Scenario B got method guidance, Scenario C got one
bare sentence. Any accuracy difference then partly measured PROMPT WORDING rather
than the mechanism under test. Now the question is identical and only the
*capability envelope* differs:

    Scenario A   the question + no data                     (web search available)
    Scenario B   the question + the brand's history + code  (sandbox)
    Scenario C   the question + a forecasting tool          (trained model)

Each scenario adds one CAPABILITY NOTE explaining what it does and does not
have. These notes are the treatment, and they are kept as short and as parallel
as the differing capabilities allow.

WHY THE TARGET MONTH IS ALWAYS NAMED
------------------------------------
The held-out period is in the past relative to the run date. "Next month" means
different things to different scenarios: B and C infer it from the data they are
given, while A -- which has no data -- anchors on the wall-clock date and would
answer about a completely different month than it is scored on. Naming the month
makes the scenarios comparable rather than merely different.

WHY THE QUESTION ASKS FOR A RECOMMENDATION
------------------------------------------
Goodwin, Onkal and Thomson (2010) found that supplying prediction intervals
alongside a point forecast did not improve newsvendor decisions and actively
degraded them: correct discrimination between asymmetric cost regimes fell from
roughly 84% under point forecasts to 44% under 95% intervals, because
participants anchored on the interval midpoint. Their result locates the value
not in the interval but in the interpretive step from interval to decision --
the step a decision-support layer exists to supply.

An earlier version of this question asked only for a number, a range and a
confidence. That made the interpretive step unobservable: the evaluation could
show whether a forecast was accurate, but not whether the system did the thing
Chapter 2 argues is the point of having an agent at all. The request is added
IDENTICALLY to all three scenarios, so it varies no factor between them.

WHY A ONE-SHOT OUTPUT EXEMPLAR
------------------------------
The answers are scored by programmatic extraction, so the measurement is only
as good as the format the model was asked to produce. A single worked example
fixes the answer shape at minimal token cost and, being identical across
scenarios, cannot advantage any of them. See OUTPUT_EXEMPLAR below for the
full rationale, including why exactly one example rather than several.

ON SCENARIO A AND RETRIEVAL
---------------------------
Scenario A can browse, and the target month is historical, so in principle it
could look the answer up. Tested adversarially 2026-08-19: asked point-blank to
find the Nielsen-reported January 2026 unit sales for a specific brand, the model
searched and returned NOT FOUND -- Nielsen scanner data is a paid commercial
product and brand-level monthly units are not published. Public sources carry
annual-report aggregates ("Danish soft drinks +2.6%"), not the quantity being
forecast.

The prompt therefore no longer contains a "do not search" instruction. It was
doing no work (there is nothing to find), it made A's prompt structurally
different from the others, and relying on instruction-following for a leakage
control would be weaker evidence than the retrieval test. Every run still records
`used_web`, the search queries, and `retrieval_suspected`, so the claim rests on
logged evidence rather than on an instruction.

Run `python prompts.py` to print every prompt with a worked example.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# The shared user question -- identical across all three scenarios
# ---------------------------------------------------------------------------
# "how many UNITS" is not a stylistic choice. The first paid run (2026-08-19)
# asked "what will X sell", and all six Scenario A runs answered in DKK --
# 145,000,000 DKK for Coca Cola against a 3.15M unit actual, scored as a 4500%
# error. Scenarios B and C infer the unit from the data they are handed; A has no
# data, so an ambiguous question let it answer a different question. That made
# A's measured accuracy an artefact of the prompt rather than a property of the
# scenario, which is exactly the confound the shared question exists to remove.
USER_QUESTION = (
    "How many units of {brand} will be sold in the {category} category in "
    "Danish retail in {target}? Answer in units sold, not currency. "
    "Give the number, a range, how confident you are, and what you would "
    "recommend the category planner do about it."
)

# ---------------------------------------------------------------------------
# One-shot output exemplar -- the answer SHAPE, held identical across scenarios
# ---------------------------------------------------------------------------
# WHY A WORKED EXAMPLE, AND WHY EXACTLY ONE
#
# The outputs are scored by programmatic extraction: `_parse_sentinel` reads the
# forecast, and `score_interval_communication.py` reads the interval bounds and
# the confidence back out of the prose to check them against what the tool
# returned. Extraction can only test what the model was actually asked to
# produce. Without a shown format, an answer that reports "roughly 3.4 to 3.9
# million" is scored the same as one that omits the interval entirely -- the
# measurement would then be of our parser's luck rather than of the system.
#
# One exemplar, not several. Brown et al. (2020) show that most of the gain from
# in-context examples arrives with the first, with sharply diminishing returns
# after; and every additional example is tokens paid on every run across all
# three scenarios. One example is also the smallest intervention that fixes the
# format, which matters because the exemplar is prompt content and therefore a
# potential confound: whatever it demonstrates, it demonstrates to A, B and C
# alike, so it cannot advantage one scenario over another.
#
# The exemplar deliberately uses a DIFFERENT category and a DIFFERENT brand from
# any scored cell, and rounded, obviously-illustrative figures. It shows the
# shape of an answer, never a plausible answer to the question being asked.
OUTPUT_EXEMPLAR = (
    "\n\nFormat your answer like this worked example (a different brand and "
    "category, shown only to fix the format):\n\n"
    "  Forecast: 1,250,000 units\n"
    "  Range: 1,050,000 to 1,480,000 units (90% interval)\n"
    "  Confidence: medium -- the brand's history is short and its recent "
    "months are volatile.\n"
    "  Recommendation: plan against the midpoint but hold cover to the upper "
    "bound, since a stockout costs more here than carrying surplus.\n"
    "  FORECAST=1250000"
)

# Shared output contract, so answer parsing is never a scenario-specific
# advantage. Scenario C also gets it, even though its number comes from the tool,
# to keep the instruction identical.
SENTINEL = "FORECAST"
SENTINEL_INSTRUCTION = (
    "\n\nEnd your reply with the single line {sentinel}=<number> "
    "(a plain number, no commas or units)."
)

# ---------------------------------------------------------------------------
# Capability notes -- the treatment
# ---------------------------------------------------------------------------
# Scenario A. States the absence of internal data as a fact, without telling the
# model how to behave: an instruction would be a second variable, and the
# retrieval test above showed there is nothing to retrieve anyway.
SCENARIO_A_NOTE = (
    "\n\nYou have no access to the company's internal sales data. "
    "Produce your best estimate."
)

# Scenario B. Names the tools available, matching what the sandbox actually
# provides, and requires the code to be RUN rather than merely written -- the
# distinction between code-as-action and code-as-text.
SCENARIO_B_NOTE = (
    "\n\nHere is the brand's monthly sales history as CSV:\n\n{csv}\n\n"
    "Write and run Python code on this history to produce the forecast. "
    "pandas, numpy, scipy, scikit-learn and statsmodels are available. "
    "End your reply with the answer, not with code."
)

# Scenario C. Announces the tool without prescribing a method. "Do not compute
# it yourself" is what separates this from Scenario B: without it the model may
# ignore the tool and hand-compute, collapsing C into B. Disclosed in the
# write-up as part of the treatment.
SCENARIO_C_NOTE = (
    "\n\nA `forecast_demand` tool is available, backed by a forecasting model "
    "trained on the company's internal sales history. Use it to answer; do not "
    "compute the forecast yourself."
)

# The tool schema is part of Scenario C's prompt in every sense that matters: it
# is the entire surface through which the LLM can reach the trained model. Two
# strings, and nothing else -- no features, no model object, no data.
FORECAST_TOOL_SCHEMA = {
    "type": "function",
    "name": "forecast_demand",
    "description": (
        "Return the demand forecast for a brand in a category from the "
        "dedicated pre-trained model: point forecast, 90% prediction interval, "
        "confidence tier, and provenance."
    ),
    "parameters": {
        "type": "object",
        "properties": {"category": {"type": "string"}, "brand": {"type": "string"}},
        "required": ["category", "brand"],
        "additionalProperties": False,
    },
}


# ---------------------------------------------------------------------------
# Prompt schema identity
# ---------------------------------------------------------------------------
# WHY THIS EXISTS
#
# Runs may only be pooled if they were asked the SAME question. Repeats are
# added across sessions and days (see the P0042 block design), and the resume
# logic in srq4_experiment.py decides whether a cached run counts as already
# done. Both need "the prompt is unchanged" to be a fact that can be checked,
# not a recollection.
#
# SCHEMA_VERSION is the human-readable name; SCHEMA_ID is a hash over every
# string that actually reaches the model. The hash is what the harness compares,
# so editing any prompt string changes the identity automatically -- there is no
# way to alter a prompt and forget to bump the version.
#
# HISTORY
#   v1  2026-08-19  "what will X sell" -- no unit named. Every Scenario A answer
#                   came back in DKK against a unit actual (~4500% error). The
#                   run is retained under run_2026-08-19_dkk-confound/ and must
#                   never be pooled.
#   v2  2026-08-19  units named explicitly. The 6-run Scenario A pilot.
#   v3  2026-09-03  adds the recommendation request (Goodwin: the interpretive
#                   step from interval to decision is where the decision value
#                   lies) and a one-shot output exemplar fixing the answer shape
#                   for programmatic extraction. Both applied identically to all
#                   three scenarios, so no factor varies between them.
SCHEMA_VERSION = "v3-recommendation-oneshot"


def schema_id() -> str:
    """Short stable hash of every prompt string sent to the model.

    Covers the question, all three capability notes, the exemplar, the sentinel
    instruction and the tool schema. Excludes per-run substitutions (brand,
    category, month, CSV) -- those vary by design and are logged per run."""
    import hashlib
    import json as _json
    parts = [SCHEMA_VERSION, USER_QUESTION, OUTPUT_EXEMPLAR, SENTINEL,
             SENTINEL_INSTRUCTION, SCENARIO_A_NOTE, SCENARIO_B_NOTE,
             SCENARIO_C_NOTE, _json.dumps(FORECAST_TOOL_SCHEMA, sort_keys=True)]
    h = hashlib.sha256("\x00".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{SCHEMA_VERSION}+{h}"


def user_question(brand: str, category: str, target: str) -> str:
    """The question every scenario is asked, before capability notes."""
    return USER_QUESTION.format(brand=brand, category=category, target=target)


def scenario_a_prompt(brand: str, category: str, target: str,
                      sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target) + SCENARIO_A_NOTE
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_b_prompt(brand: str, category: str, target: str, csv: str,
                      sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target)
            + SCENARIO_B_NOTE.format(csv=csv)
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_c_prompt(brand: str, category: str, target: str,
                      sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target) + SCENARIO_C_NOTE
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def _demo():
    """Print every prompt with a worked example, for eyeballing before a paid run."""
    import json
    b, c, t = "FAXE KONDI", "CSD", "2026-06"
    csv = ("period_year,period_month,sales_units,promo_intensity\n"
           "2022,10,4472796.26,\n... (39 rows) ...")
    print("=" * 78)
    print("THE SHARED QUESTION (identical in all three scenarios)")
    print("=" * 78)
    print(user_question(b, c, t))
    for name, p in (("SCENARIO A -- plain LLM, no firm data", scenario_a_prompt(b, c, t)),
                    ("SCENARIO B -- LLM + data & code execution", scenario_b_prompt(b, c, t, csv)),
                    ("SCENARIO C -- LLM + trained model", scenario_c_prompt(b, c, t))):
        print("\n" + "=" * 78)
        print(name)
        print("=" * 78)
        print(p)
    print("\n" + "=" * 78)
    print("SCENARIO C also receives this tool schema:")
    print("=" * 78)
    print(json.dumps(FORECAST_TOOL_SCHEMA, indent=2))
    print("\n" + "=" * 78)
    print("Held constant: the question, the target month, the requested output")
    print("shape, the exemplar, the sentinel. Only the capability envelope differs.")
    print("=" * 78)
    print(f"\nSCHEMA: {schema_id()}")
    print("Runs may only be pooled with other runs carrying this same id.")
    print("=" * 78)


if __name__ == "__main__":
    _demo()
