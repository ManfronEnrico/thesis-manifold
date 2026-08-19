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

WHAT MUST STAY CONSTANT
-----------------------
The single variable under test is HOW the agent produces a forecast. Everything
the scenarios are asked must therefore be as close to identical as their differing
capabilities permit:

  - same brand, same category, same TARGET MONTH (named explicitly, never
    "next month" -- see below)
  - same requested output shape (a number, plus a range where the scenario can give
    one)
  - same sentinel convention, so parsing is not a scenario-specific advantage

Where the prompts necessarily differ, the difference IS the treatment:
  Scenario C is told a forecasting tool exists and not to compute by hand.
  Scenario B is told to write and run its own code.
  Scenario A is told it has no internal data.

WHY THE TARGET MONTH IS ALWAYS NAMED
------------------------------------
The held-out period is in the past relative to the run date. "Next month" means
different things to different scenarios: scenarios B and C infer it from the data they
are given, while scenario A -- which has no data -- anchors on the wall-clock date and
would answer about a completely different month than it is scored on. Naming the
month makes the scenarios comparable rather than merely different.

Run `python prompts.py` to print every prompt with a worked example.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Scenario C -- dedicated-model tool
# ---------------------------------------------------------------------------
# The tool schema is part of the prompt in every sense that matters: it is the
# entire surface through which the LLM can reach the trained model. It exposes
# two strings and nothing else -- no features, no model object, no data.
FORECAST_TOOL_SCHEMA = {
    "type": "function",
    "name": "forecast_demand",
    "description": (
        "Return next-month demand forecast for a brand from the dedicated "
        "pre-trained model (point, 90% interval, confidence tier). Use for "
        "any forecast question; do not compute yourself."
    ),
    "parameters": {
        "type": "object",
        "properties": {"category": {"type": "string"}, "brand": {"type": "string"}},
        "required": ["category", "brand"],
        "additionalProperties": False,
    },
}

# NOTE FOR THE WRITE-UP: "do not compute yourself" is a deliberate constraint,
# not an oversight. Scenario C tests whether a TOOL-USING agent beats a code-writing
# one; without the instruction the model may ignore the tool and hand-compute,
# which would collapse Scenario C into Scenario B. It should be disclosed as part of the
# treatment, because a reviewer may reasonably read it as tilting the scenario.
SCENARIO_C_TASK = (
    "What will {brand} sell in {target} in the {category} category? "
    "Give the number, range and confidence."
)

# ---------------------------------------------------------------------------
# Scenario B -- code-as-action
# ---------------------------------------------------------------------------
# The history is injected as CSV rather than a file upload so that exactly what
# the model received is recorded in the prompt log, byte for byte.
SCENARIO_B_TASK = (
    "Forecast sales_units for {brand} in {category} for {target}, "
    "the month immediately after the history above."
)

SCENARIO_B_PROMPT = (
    "Here is the monthly sales history for brand {brand} in the {category} "
    "category as CSV:\n\n{csv}\n\n{task}\n\n"
    "Write and run Python code to produce the forecast. pandas, numpy, "
    "scipy, scikit-learn and statsmodels are available.\n\n"
    "IMPORTANT: your FINAL message must contain the single line "
    "{sentinel}=<number> with a plain number (no commas, no units), "
    "followed by one line naming your method and a range. Do not end your "
    "reply with code -- end it with that line."
)

# ---------------------------------------------------------------------------
# Scenario A -- no firm data
# ---------------------------------------------------------------------------
# The second paragraph is a LEAKAGE MITIGATION, not a stylistic preference. The
# target month is historical, so a published figure may exist. Instructing
# estimation-over-retrieval reduces that risk; it does not eliminate it, which is
# why every Scenario A run also records `retrieval_suspected` and `used_web` for
# inspection. Documented as a limitation: any residual retrieval makes Scenario A look
# BETTER, which shrinks the measured value of data access -- conservative with
# respect to the thesis claim.
SCENARIO_A_TASK = (
    "Estimate how many units the brand {brand} sold in the {category} category "
    "in Danish retail in {target}. You have no access to internal sales data.\n\n"
    "Do NOT search for or report an already-published figure for that specific "
    "month. Reason from general market knowledge -- category size, the brand's "
    "share, seasonality -- to produce your own estimate."
)

# Shared across scenarios B and C so that answer parsing is not a scenario-specific
# advantage. Scenario C does not need it: its number comes from the tool, not prose.
SENTINEL = "FORECAST"
SENTINEL_INSTRUCTION = (
    "\n\nEnd your reply with the single line {sentinel}=<number> "
    "(a plain number, no commas or units)."
)


def scenario_c_prompt(brand: str, category: str, target: str) -> str:
    return SCENARIO_C_TASK.format(brand=brand, category=category, target=target)


def scenario_b_prompt(brand: str, category: str, target: str, csv: str,
                 sentinel: str = SENTINEL) -> str:
    task = SCENARIO_B_TASK.format(brand=brand, category=category, target=target)
    return SCENARIO_B_PROMPT.format(brand=brand, category=category, csv=csv,
                               task=task, sentinel=sentinel)


def scenario_a_prompt(brand: str, category: str, target: str,
                 sentinel: str = SENTINEL) -> str:
    task = SCENARIO_A_TASK.format(brand=brand, category=category, target=target)
    return task + SENTINEL_INSTRUCTION.format(sentinel=sentinel)


def _demo():
    """Print every prompt with a worked example, for eyeballing before a paid run."""
    import json
    b, c, t = "HARBOE", "CSD", "2026-01"
    csv = "period_year,period_month,sales_units,promo_intensity\n2022,10,4472796.26,\n... (39 rows)"
    print("=" * 78)
    print("SCENARIO A -- plain LLM (no firm data)")
    print("=" * 78)
    print(scenario_a_prompt(b, c, t))
    print("\n" + "=" * 78)
    print("SCENARIO B -- LLM + data & code execution")
    print("=" * 78)
    print(scenario_b_prompt(b, c, t, csv))
    print("\n" + "=" * 78)
    print("SCENARIO C -- LLM + trained model")
    print("=" * 78)
    print("\n[tool schema the LLM sees]")
    print(json.dumps(FORECAST_TOOL_SCHEMA, indent=2))
    print("\n[prompt]")
    print(scenario_c_prompt(b, c, t))
    print("\n" + "=" * 78)
    print("Held constant: brand, category, target month, requested output shape,")
    print("sentinel convention. The differences above ARE the treatment.")
    print("=" * 78)


if __name__ == "__main__":
    _demo()
