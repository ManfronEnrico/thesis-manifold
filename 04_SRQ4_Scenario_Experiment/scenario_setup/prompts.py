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
# v6 (2026-09-12) REBUILT THESE FROM SHARED PARTS. WHY.
#
# Every note used to be written by hand, so comparable arms drifted apart in
# wording while nobody noticed. Measured on v5:
#
#   * B told the model which five libraries were available; D did not.
#   * D's coder brief asked for "the point forecast, a 90% interval and how
#     confident you are"; B's note asked for none of that -- yet BOTH are
#     scored on interval communication. D was instructed to produce an interval
#     and B was left to volunteer one.
#   * D's brief prescribed the mechanics ("paste the CSV into io.StringIO");
#     B's did not.
#   * E glossed every field of the model payload; C, which receives the same
#     fields through the tool response, got no gloss.
#
# Each difference is small. Together they mean B->D and C->E did not isolate
# the orchestrator: wording travelled with it. The shared user question exists
# precisely to stop that, and the capability notes had quietly undone it.
#
# So the notes below are COMPOSED, not written. One data block, one model
# block, one warehouse instruction, assembled per arm. A difference between two
# arms is now visible as a different component, not as a turn of phrase.
#
# WHAT IS ALLOWED TO DIFFER, AND NOTHING ELSE:
#
#   1. WHICH capability an arm has -- data, model, both. That is the treatment.
#   2. The warehouse instruction, for D/E/G ONLY. Those arms run on Prometheus,
#      whose nested coder has `run_sql`, `inspect_schema`, `distinct_values`
#      and `sample_rows` registered at module scope in the vendor tree
#      (prometheus_coder.py:327). The tools cannot be removed by configuration.
#      B/C/F have no such tools, so the sentence would be meaningless there --
#      including it would be adding words to describe a capability the arm does
#      not have.
#   3. A short conversational-agent note for D/E/G, because Prometheus is two
#      agents and the coder never sees the user's message.
#
# WHAT IS NO LONGER ALLOWED TO DIFFER: the library list, the deliverable, the
# mechanics, and any gloss on the data.

# --- the data block, used verbatim by B, D, F and G -------------------------
#
# WHY THE SCHEMA DICTIONARY IS INCLUDED
# A production Prometheus queries a live star schema and can read its column
# documentation. The dictionary is that documentation, unedited. Without it the
# agent is handed 32 unexplained columns and must guess what
# `total_weighted_distribution_points_tdp_reach` means -- a handicap no
# production agent faces, and one that would make a poor result unattributable
# between "could not model it" and "could not read it".
#
# WHY NO GLOSS ON THE DATA ITSELF
# The dictionary is the warehouse's own text. We add nothing: no hint that
# distribution matters, no warning about the sparsity, no suggested method.
# Working out which of 32 columns carries signal IS the task being measured.
DATA_BLOCK = """

Here is the brand's monthly sales history, as it comes out of the sales data warehouse after joining the fact and dimension tables and aggregating to brand-month:

{csv}

The warehouse's own column documentation:

{schema}
"""

# --- the model block, used verbatim by C, E, F and G ------------------------
#
# No gloss on the fields (changed in v6). v5 explained `forecast_units`,
# `interval_90`, `confidence_tier` and `historical_wmape` to E but not to C,
# which is an asymmetry between two arms that are supposed to differ only in
# orchestrator. Removed rather than duplicated: the payload names its own
# fields, and reading it is part of what is being measured.
MODEL_BLOCK = """

A forecast from a dedicated model trained on the company's internal sales history is available:

{payload}
"""

# The tool-shaped variant, for C -- which reaches the same model through a
# typed tool call rather than being handed the payload. "Do not compute it
# yourself" is what separates this from the data arms; without it the model may
# ignore the tool and hand-compute, collapsing C into B.
MODEL_TOOL_BLOCK = """

A `forecast_demand` tool is available, backed by a dedicated model trained on the company's internal sales history. Use it to answer; do not compute the forecast yourself."""

# --- the deliverable, identical in every arm that runs code ------------------
#
# v5 asked D for an interval and confidence and asked B for neither, while
# scoring both on interval communication. One string now, so that cannot recur.
ANALYSIS_TASK = """
Write and run Python code on this history to produce a forecast for {target}. pandas, numpy, scipy, scikit-learn and statsmodels are available. Report the point forecast, a 90% interval and how confident you are. End your reply with the answer, not with code."""

# The same deliverable where the model's forecast is also present. It does NOT
# say which evidence to prefer -- see DEC-COMBINED-INPUT below.
ANALYSIS_TASK_WITH_MODEL = """
You have the history, the model's forecast, and a Python environment. pandas, numpy, scipy, scikit-learn and statsmodels are available. Weigh the evidence as you see fit and produce your own forecast for {target}. Report the point forecast, a 90% interval and how confident you are. End your reply with the answer, not with code."""

# --- the warehouse instruction, D/E/G ONLY ----------------------------------
#
# An INSTRUCTION, not an enforcement. The SQL tools stay registered and cannot
# be removed without forking the vendor (F45). Compliance is MEASURED per run
# via `sql_calls` in the trace, and a run that queries anyway is classified
# `warehouse_access` and excluded, not quietly kept. That is stronger evidence
# than a filtered tool list, because it is observed per run rather than
# configured once and trusted. The limitations say exactly this.
NO_WAREHOUSE = """
Do not query the data warehouse. The material below has already been retrieved and is the authoritative input; a warehouse query would answer a different question from the one being asked.
"""

# --- the conversational-agent note, D/E/G ONLY ------------------------------
#
# Prometheus is two agents: a conversational one whose only data verb is
# `invoke_prometheus_coder`, and a nested coder owning the data tools. This
# reaches the conversational agent; the blocks above reach the coder through
# `extra_coder_guardrails`, the vendor's documented eval seam. Kept minimal --
# it routes the request, it does not restate the task, because restating it
# would be wording that exists in D/E/G and not in B/C/F.
ENGINE_NOTE = """

Use the analysis engine to answer this. The material it needs has already been retrieved; it does not need to query the data warehouse. End your reply with the answer, not with code."""

# --- Scenario A -------------------------------------------------------------
# States the absence of internal data as a fact, without telling the model how
# to behave: an instruction would be a second variable, and the retrieval test
# (see the header) showed there is nothing to retrieve anyway.
SCENARIO_A_NOTE = (
    "\n\nYou have no access to the company's internal sales data. "
    "Produce your best estimate."
)

# --- assembled per arm ------------------------------------------------------
# Read these as the composition they are. Any two arms that share a capability
# share the exact string that expresses it.
SCENARIO_B_NOTE = DATA_BLOCK + ANALYSIS_TASK
SCENARIO_C_NOTE = MODEL_TOOL_BLOCK
SCENARIO_D_NOTE = ENGINE_NOTE
SCENARIO_D_CODER = NO_WAREHOUSE + DATA_BLOCK + ANALYSIS_TASK
SCENARIO_E_NOTE = ENGINE_NOTE
SCENARIO_E_CODER = (NO_WAREHOUSE + MODEL_BLOCK
                    + "\nPresent this to the category planner with a "
                      "recommendation for {target}.")
SCENARIO_F_NOTE = DATA_BLOCK + MODEL_BLOCK + ANALYSIS_TASK_WITH_MODEL
SCENARIO_G_NOTE = ENGINE_NOTE
SCENARIO_G_CODER = (NO_WAREHOUSE + DATA_BLOCK + MODEL_BLOCK
                    + ANALYSIS_TASK_WITH_MODEL)

# ---------------------------------------------------------------------------
# Scenarios F and G -- the combined arm
# ---------------------------------------------------------------------------
# F and G hold the history, a code sandbox AND the trained model's forecast at
# the same time. This is what a production deployment would actually do.
#
# WHY THEY ARE A SIXTH AND SEVENTH RUNG, NOT A REDEFINITION OF C AND E
# C and E stay exactly as they are -- the trained model alone, the artefact as
# Chapter 6 specifies it. F and G sit ABOVE them, so the ladder still
# attributes cleanly:
#
#     A -> B   what data access buys
#     B -> C   what the trained model adds          (the thesis contribution)
#     C -> F   what adding code back ON TOP of the model does
#     D -> E -> G  the same three rungs on the production orchestrator
#
# THE FRAMING DECISION (DEC-COMBINED-INPUT, Brian, 2026-09-11)
# The model's forecast is presented as ONE INPUT AMONG SEVERAL, not as a
# starting point to revise. The alternative -- "here is the model's number,
# override it if you disagree" -- answers a weaker question, because an agent
# handed a number and told it may keep it will almost always keep it. That
# measures deference, not integration.
#
# F and G are also the arms that most resemble production: the agent holds
# data, code-as-action and a trained model at once and must reason ACROSS all
# three to reach one recommendation. Whether it trusts its own analysis or the
# served model -- and whether that choice is stable from run to run -- is the
# measurement, traced as `deviates_from_model`.

# The tool schema is Scenario C's prompt in every sense that matters: it is the
# entire surface through which the LLM reaches the trained model. Two strings,
# and nothing else -- no features, no model object, no data.
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
#   v4  2026-09-10  adds scenarios D and E (the Prometheus orchestrator). The
#                   A/B/C strings are BYTE-IDENTICAL to v3 -- question, exemplar
#                   and sentinel unchanged -- so A-C ask exactly what they did.
#                   The id changes anyway, because the registry it hashes is now
#                   larger, and v3 and v4 rows are deliberately NOT pooled: a v3
#                   row came from a harness that had no D or E. See P0049 F44 --
#                   add D/E BEFORE the funded set, never after, or every paid
#                   row stops matching and is re-sent.
SCHEMA_VERSION = "v6-shared-composition"


def schema_id() -> str:
    """Short stable hash of every prompt string sent to the model.

    Covers the question, all three capability notes, the exemplar, the sentinel
    instruction and the tool schema. Excludes per-run substitutions (brand,
    category, month, CSV) -- those vary by design and are logged per run."""
    import hashlib
    import json as _json
    parts = [SCHEMA_VERSION, USER_QUESTION, OUTPUT_EXEMPLAR, SENTINEL,
             SENTINEL_INSTRUCTION, SCENARIO_A_NOTE, SCENARIO_B_NOTE,
             SCENARIO_C_NOTE, SCENARIO_D_NOTE, SCENARIO_D_CODER,
             SCENARIO_E_NOTE, SCENARIO_E_CODER,
             SCENARIO_F_NOTE, SCENARIO_G_NOTE, SCENARIO_G_CODER,
             _json.dumps(FORECAST_TOOL_SCHEMA, sort_keys=True)]
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
                      schema: str, sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target)
            + SCENARIO_B_NOTE.format(csv=csv, schema=schema, target=target)
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_c_prompt(brand: str, category: str, target: str,
                      sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target) + SCENARIO_C_NOTE
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))



def scenario_d_prompt(brand: str, category: str, target: str,
                      sentinel: str = SENTINEL) -> str:
    """The user-facing half of D. The CSV goes to the coder, not here."""
    return (user_question(brand, category, target) + SCENARIO_D_NOTE
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_d_coder(brand: str, category: str, target: str, csv: str,
                     schema: str) -> str:
    """The coder-side brief for D.

    Carries the SAME composed block Scenario B receives -- same data, same
    schema, same deliverable -- so B->D isolates the orchestrator.
    """
    return SCENARIO_D_CODER.format(brand=brand, category=category,
                                   target=target, csv=csv, schema=schema)


def scenario_e_prompt(brand: str, category: str, target: str,
                      sentinel: str = SENTINEL) -> str:
    return (user_question(brand, category, target) + SCENARIO_E_NOTE
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_e_coder(brand: str, category: str, target: str, payload: str) -> str:
    """The coder-side brief for E, carrying the trained model's payload."""
    return SCENARIO_E_CODER.format(brand=brand, category=category,
                                   target=target, payload=payload)


def scenario_f_prompt(brand: str, category: str, target: str, csv: str,
                      payload: str, schema: str,
                      sentinel: str = SENTINEL) -> str:
    """F -- history AND the model's forecast AND a sandbox, one LLM.

    Everything is in the single user message, as Scenario B's CSV already is:
    F has no nested coder to brief.
    """
    return (user_question(brand, category, target)
            + SCENARIO_F_NOTE.format(csv=csv, payload=payload,
                                     schema=schema, target=target)
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_g_prompt(brand: str, category: str, target: str,
                      sentinel: str = SENTINEL) -> str:
    """The user-facing half of G. The CSV and payload go to the coder."""
    return (user_question(brand, category, target) + SCENARIO_G_NOTE
            + OUTPUT_EXEMPLAR + SENTINEL_INSTRUCTION.format(sentinel=sentinel))


def scenario_g_coder(brand: str, category: str, target: str, csv: str,
                     payload: str, schema: str) -> str:
    """The coder-side brief for G: the same blocks D and E receive."""
    return SCENARIO_G_CODER.format(brand=brand, category=category,
                                   target=target, csv=csv, payload=payload,
                                   schema=schema)


def _demo():
    """Print every prompt with a worked example, for eyeballing before a paid run.

    Renders all SEVEN arms. The v5 version showed three, which is how the
    wording drift between B and D survived: the arms that had diverged were
    never printed side by side.
    """
    import json
    b, c, t = "FAXE KONDI", "CSD", "2026-06"
    csv = ("period_year,period_month,n_skus_observed,sales_value,...\n"
           "2022,10,12,9861.23,...\n... (39 rows x 32 columns) ...")
    schema = ("table_name,column_name,data_type,unit,null_meaning,description\n"
              "csd_clean_facts,sales_units,double,units,,Total sales out of "
              "store...\n... (70 rows) ...")
    payload = ('{"forecast_units": 1234567, "interval_90": [1.0e6, 1.5e6], '
               '"confidence_tier": "Medium", "historical_wmape": 0.184}')

    print("=" * 78)
    print("THE SHARED QUESTION (identical in all seven arms)")
    print("=" * 78)
    print(user_question(b, c, t))

    arms = [
        ("A_llm_plain      -- no firm data", scenario_a_prompt(b, c, t)),
        ("B_llm_data       -- data + code", scenario_b_prompt(b, c, t, csv, schema)),
        ("C_llm_model      -- typed tool", scenario_c_prompt(b, c, t)),
        ("D_prometheus_data     [user]", scenario_d_prompt(b, c, t)),
        ("D_prometheus_data     [coder]", scenario_d_coder(b, c, t, csv, schema)),
        ("E_prometheus_model    [user]", scenario_e_prompt(b, c, t)),
        ("E_prometheus_model    [coder]", scenario_e_coder(b, c, t, payload)),
        ("F_llm_data_model -- data + code + model",
         scenario_f_prompt(b, c, t, csv, payload, schema)),
        ("G_prometheus_data_model [user]", scenario_g_prompt(b, c, t)),
        ("G_prometheus_data_model [coder]",
         scenario_g_coder(b, c, t, csv, payload, schema)),
    ]
    for name, text in arms:
        print("\n" + "=" * 78)
        print(name)
        print("=" * 78)
        print(text)

    print("\n" + "=" * 78)
    print("Scenario C also receives this tool schema:")
    print("=" * 78)
    print(json.dumps(FORECAST_TOOL_SCHEMA, indent=2))

    print("\n" + "=" * 78)
    print("SHARED-COMPONENT CHECK -- comparable arms must be byte-identical")
    print("=" * 78)
    pairs = [
        ("B data block", "D coder data block",
         DATA_BLOCK in SCENARIO_B_NOTE and DATA_BLOCK in SCENARIO_D_CODER),
        ("B deliverable", "D deliverable",
         ANALYSIS_TASK in SCENARIO_B_NOTE and ANALYSIS_TASK in SCENARIO_D_CODER),
        ("F data block", "G coder data block",
         DATA_BLOCK in SCENARIO_F_NOTE and DATA_BLOCK in SCENARIO_G_CODER),
        ("F deliverable", "G deliverable",
         ANALYSIS_TASK_WITH_MODEL in SCENARIO_F_NOTE
         and ANALYSIS_TASK_WITH_MODEL in SCENARIO_G_CODER),
        ("E model block", "G model block",
         MODEL_BLOCK in SCENARIO_E_CODER and MODEL_BLOCK in SCENARIO_G_CODER),
    ]
    for left, right, ok in pairs:
        print(f"  [{'OK ' if ok else 'BAD'}] {left} == {right}")
    print(f"  [{'OK ' if NO_WAREHOUSE not in SCENARIO_B_NOTE else 'BAD'}] "
          "warehouse instruction absent from B (it has no SQL tools)")
    print(f"  [{'OK ' if NO_WAREHOUSE in SCENARIO_D_CODER else 'BAD'}] "
          "warehouse instruction present in D (it does)")

    print("\n" + "=" * 78)
    print("Held constant: the question, the target month, the output shape, the")
    print("exemplar, the sentinel, the data, the schema dictionary and the")
    print("deliverable. Only the capability envelope differs.")
    print("=" * 78)
    print(f"\nSCHEMA: {schema_id()}")
    print("Runs may only be pooled with other runs carrying this same id.")
    print("=" * 78)


if __name__ == "__main__":
    _demo()
