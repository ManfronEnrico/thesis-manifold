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

    What will {brand} sell in the {category} category in Danish retail in
    {target}? Give the number, a range, and how confident you are.

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
USER_QUESTION = (
    "What will {brand} sell in the {category} category in Danish retail in "
    "{target}? Give the number, a range, and how confident you are."
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


def user_question(brand: str, category: str, target: str) -> str:
    """The question every scenario is asked, before capability notes."""
    return USER_QUESTION.format(brand=brand, category=category, target=target)


def scenario_a_prompt(brand: str, category: str, target: str,
                      sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target) + SCENARIO_A_NOTE
            + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_b_prompt(brand: str, category: str, target: str, csv: str,
                      sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target)
            + SCENARIO_B_NOTE.format(csv=csv)
            + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_c_prompt(brand: str, category: str, target: str,
                      sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target) + SCENARIO_C_NOTE
            + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


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
    print("shape, the sentinel. Only the capability envelope differs.")
    print("=" * 78)


if __name__ == "__main__":
    _demo()
