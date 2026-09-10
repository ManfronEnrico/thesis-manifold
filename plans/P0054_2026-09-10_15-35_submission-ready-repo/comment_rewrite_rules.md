---
name: comment-rewrite-rules
description: RULE - What to strip and what to keep when rewriting pipeline comments for the submission repository, with worked before/after examples from the actual codebase.
category: reference
applies-to: [P0054 submission export, every shipped .py file]
triggers: [running /submission-export, reviewing a rewritten file]
created: 2026_09_10-15_35
updated: 2026_09_10-15_35
---

# Comment rewrite rules — working repo → submission repo

The assessor reads this code with the thesis open. They want to know **what a
script does and why it does it that way**. They do not want to know that a
decision was made on 18 August, that it was numbered `DEC-HORIZON`, or that it
reversed something a plan called `P0026`.

## The one test

> Would this sentence make sense to a reader who has never seen a previous
> version of this repository, and does not know what a plan, a finding, or a
> DEC-code is?

If it only makes sense as a diff against our history, it is provenance —
delete it. If it explains the code in front of them, it is reasoning — keep it.

This is the same test `prose-insertion-discipline.md` applies to thesis prose.
The code is now a submission artefact too, so it inherits the rule.

---

## Quick reference

| Marker | Found in | Verdict |
|---|---|---|
| `DEC-<NAME>`, `DEC-P0046-<NAME>` | 101 sites | drop the code, keep the reasoning it labels |
| `P00NN`, `P0038 task 3` | 211 sites | drop; keep the fact if it is about the code |
| `F63`, `F7`, `F28/F38` | 134 sites | drop; if the finding matters, state it in words |
| `2026-08-18`, "Measured 2026-08-12" | 185 sites | drop the date; keep "measured across the four categories" |
| "Ported from the notebook", "the notebook hardcoded" | ~15 files | delete the whole clause |
| "previously X", "used to", "REMOVED", "supersedes" | 27 sites | delete — repo history, not code behaviour |
| "Brian", "Enrico", "so we both run" | 12 sites | delete attribution; keep the decision |
| `WHY THIS EXISTS` / `ROUTING` / `CONVENTIONS` banner headers | several docstrings | collapse into plain prose |
| Paths into `plans/`, `writing-notes/`, `.claude/`, `notebookLM/` | 17 sites | delete the reference entirely |

---

## Rule 1 — Keep reasoning, drop provenance

The single most common shape in this codebase is a genuinely good comment
wearing an internal label. Strip the label, keep the comment.

### Example 1 — `pipeline_config.py`, the derived minimum-periods threshold

**Before** (26 lines):

```python
# DEC-MINPERIODS (2026-08-18): the minimum series length is DERIVED from the
# feature specification above, never chosen. A brand-month row is trainable
# only once its lag features are defined, so
#
#     usable_rows(brand) = n_months(brand) - WARMUP_PERIODS - FORECAST_HORIZON
#
# and requiring at least one usable row gives n_months >= 15. A brand below
# that cannot enter the design matrix at all -- it is excluded because it is
# unrepresentable under this feature specification, not because it was judged
# low quality. That distinction is what makes the threshold defensible.
#
# Measured 2026-08-18 across all four categories: this threshold costs 0.0% of
# training rows relative to imposing no threshold, because the brands it drops
# were each contributing zero. The previous hardcoded 40 cost 20.5% (CSD),
# 16.8% (Danskvand), 40.8% (Energidrikke) and 30.2% (RTD).
#
# Because it is derived, it follows the lag structure automatically: MAX_LAG=6
# yields 9, MAX_LAG=3 yields 6. Do not hardcode a replacement.
MIN_PERIODS: int = WARMUP_PERIODS + FORECAST_HORIZON + 1   # = 15
```

**After** (8 lines):

```python
# Minimum series length is derived from the feature spec, not chosen. A row is
# trainable only once its lag features are defined:
#
#     usable_rows(brand) = n_months(brand) - WARMUP_PERIODS - FORECAST_HORIZON
#
# Requiring at least one usable row gives n_months >= 15. A brand below the
# threshold is excluded because it is unrepresentable under this feature
# specification, not because it was judged low quality. Deriving the value
# means it tracks the lag structure automatically.
MIN_PERIODS: int = WARMUP_PERIODS + FORECAST_HORIZON + 1   # = 15
```

**What went and why:**
- `DEC-MINPERIODS (2026-08-18)` — internal label and date
- the 0.0% / 20.5% / 16.8% measurement paragraph — this belongs in the thesis,
  where it is a finding with a method behind it. In a config file it reads as
  a changelog, and it references "the previous hardcoded 40", which is repo
  history.
- "Do not hardcode a replacement" — an instruction to a future collaborator,
  not an explanation to a reader

**What stayed:** the derivation, the formula, and the defensibility argument.
That is the part an assessor would ask about.

---

### Example 2 — `export_holiday_appendix.py`, the file docstring

**Before** (29 lines, four banner headers):

```python
"""
Appendix tables documenting the DK public-holiday enrichment.

WHY THIS EXISTS AS A GENERATOR
------------------------------
Per DEC-P0046-PATHS every artefact that could enter the thesis must be produced
by a script under version control, resolving its output through PATHS.py. A
hand-pasted table of holiday counts would be exactly the undefendable artefact
P0046 exists to eliminate: nobody could say which fetch produced it.

ROUTING (DEC-P0046-ROUTING)
---------------------------
This lives beside its producer -- the holiday fetch, in SRQ1's raw tier, since
the enrichment feeds SRQ1's models -- and writes into the results tier, which
per DEC-P0046-SINGLE-HOME is where artefacts live exactly once. Tier 06
(writing) receives nothing.

CONVENTIONS (F7, matching export_appendix.py)
---------------------------------------------
  - .md and .csv twins from the same DataFrame, so they cannot disagree
  - no hard-coded numbers: every value derives from the cache on disk
  - units in the column headers
  - an <!-- INTERNAL REVIEW --> separator below which nothing is for submission
  - the filename carries the sequence number; the content carries none, because
    numbering inside the document is Word's job

USAGE
    python export_holiday_appendix.py
"""
```

**After** (10 lines):

```python
"""Generate the appendix tables documenting the Danish public-holiday enrichment.

Reads the holiday cache produced by fetch_holidays.py and writes matching .md
and .csv tables from the same DataFrame, so the two cannot disagree. Every
value is computed from the cache rather than typed in, which means the tables
stay correct when the holiday data is re-fetched.

Usage:
    python export_holiday_appendix.py
"""
```

**What went:** the three banner headers, all four DEC codes, the `P0046` and
`F7` references, and the routing paragraph (an assessor does not need our
single-home artefact policy explained). The `<!-- INTERNAL REVIEW -->`
convention goes too — in the submission repo there is no internal half.

**What stayed:** what it reads, what it writes, why the twin-output design
matters, and how to run it.

---

## Rule 2 — Delete change history outright

A comment describing what the code *used to* do has no reader in the submission
repo. There is no earlier version to compare against.

### Example 3 — `srq1_generate_performance_figures.py`, a removed figure

**Before:**

```python
# ---- Fig 2: REMOVED (P0035, 2026-08-01) ----
# Was a brand×month vs brand×chain granularity comparison. DEC-GRAIN (2026-07-12)
# dropped the chain grain, so the comparison has no second term. The historical
# chain-grain numbers are preserved at
# plans/P0035_2026-08-01_grain-artifact-removal/preserved_chain_grain_results/.
```

**After:** *(deleted entirely; figure numbering renumbered so there is no gap)*

An assessor reading a script that generates figures 1 and 3 will wonder where
figure 2 went. Better to have figures 1 and 2. The chain-grain decision itself
belongs in the thesis limitations section, which is where it already lives.

### Example 4 — `step_1_load_and_aggregate.py`, the aggregation spec

**Before** (23 lines):

```python
# Measures are DISCOVERED from the merged frame, not enumerated.
#
# The notebook hardcoded five columns (sales_units, sales_value,
# sales_in_liters, sales_units_any_promo, weighted_distribution). Measured
# 2026-08-12 across the four categories, the fact views actually carry 35
# distinct measure columns -- the whole `baseline_*` family, the
# `numeric_distribution` family, `universe_number_of_stores`,
# `sales_units_any_tpr`, and more. A fixed list silently discards all of them,
# not because anyone judged them uninformative but because the notebook listed
# five and the list was inherited unexamined. That is the same defect class as
# F28/F38: an inherited literal wearing the appearance of a decision.
#
# Column availability also differs BETWEEN categories in ways a fixed list
# cannot express -- and not only by presence. The same measure is spelled
# differently per category:
#     weighted_distribution_disp_w_o_feat   (CSD)
#     weighted_distribution_disp_wo_feat    (Energidrikke, RTD)
#     weighted_distribution_disp_and_feat   (RTD)
# Discovery handles all three without naming any of them.
#
# Related: P0036 task 11 ("recover discarded product-dimension features").
# This removes the step-1 half of that problem -- measures are no longer
# dropped on the way into the panel.
```

**After** (10 lines):

```python
# Measure columns are discovered from the merged frame rather than enumerated.
#
# The four category views carry 35 distinct measure columns between them, and
# availability differs by category. The same measure is also spelled
# differently across categories:
#     weighted_distribution_disp_w_o_feat   (CSD)
#     weighted_distribution_disp_wo_feat    (Energidrikke, RTD)
#     weighted_distribution_disp_and_feat   (RTD)
# A fixed column list cannot express either kind of variation, so it would
# silently drop measures; discovery handles all three spellings without
# naming any of them.
```

**What went:** the notebook's five hardcoded columns (repo history), the
`F28/F38` defect-class aside, the `P0036 task 11` cross-reference, and the
measurement date.

**What stayed:** the design decision, the concrete evidence for it (35 columns,
three spellings), and why the alternative fails. This is the strongest kind of
code comment and it survives the pass nearly intact.

---

## Rule 3 — Delete collaboration and attribution

### Example 5 — `forecast_tool.py`, the implausible-error clip

**Before:**

```python
# Above this, a reported error rate is a failure indicator rather than a
# measurement. Ridge on energidrikke scored 2.8e13% WMAPE unclipped -- a model that
# collapsed on one series and had the failure amplified by expm1 (P0040 F63).
#
# WHY IT MUST NOT BE SERVED (Brian, 2026-08-22): an LLM shown "2.8e13%" either
# ignores it (harmless) or tries to reason about it (harmful), and it has no way to
# tell which case it is in. A number that large is not informative-but-extreme; it
# is a different KIND of thing from an error rate, wearing the same clothes.
# Substituting an explicit "n/a" plus a reason preserves the information that the
# method failed while removing the false quantity.
#
# 300% is chosen as "worse than any usable forecast" -- a forecast wrong by 3x is
# already useless, so nothing above it carries decision-relevant signal. It is a
# display threshold, not an analysis parameter: the RAW figures stay in
# stat_baselines.csv and the thesis reports them (F63). This only governs what the
# serving interface hands an agent.
_IMPLAUSIBLE_ERROR_PCT = 300.0
```

**After:**

```python
# Above this threshold a reported error rate is a failure indicator rather than
# a measurement: Ridge on energidrikke scored 2.8e13% WMAPE, a model that
# collapsed on one series with the failure amplified by the expm1 back-transform.
#
# Serving such a value to an LLM is worse than serving nothing. The agent either
# ignores it or tries to reason about it, and cannot tell which case it is in.
# An explicit "n/a" plus a reason keeps the information that the method failed
# while removing the false quantity.
#
# 300% is "worse than any usable forecast" -- a forecast wrong by 3x already
# carries no decision-relevant signal. This is a display threshold only; the raw
# figures stay in stat_baselines.csv and are reported in full.
_IMPLAUSIBLE_ERROR_PCT = 300.0
```

**What went:** `(P0040 F63)`, `(F63)`, the `WHY IT MUST NOT BE SERVED (Brian,
2026-08-22)` banner with its attribution.

**What stayed:** all three arguments — the observed failure, why serving it
harms an agent, and why 300 specifically. This is a good comment and the rewrite
barely shortens it. The label was the only problem.

---

## Rule 4 — Compress docstrings to master's-student length

A file docstring answers three questions in three to eight lines: what this
script does, what it reads, what it writes. Anything longer is an essay, and the
length itself reads as machine-generated even when every sentence is true.

The banner-header style (`WHY THIS EXISTS`, `ROUTING`, `CONVENTIONS`,
`GRAIN HISTORY`, `DEC-NO-FALLBACK` as a heading) is the clearest tell in this
codebase. Real student code does not have section headers inside a docstring.

**Where reasoning is worth keeping but the docstring is over-long, move it to
the point of use.** A two-line comment above the function that implements a
decision is more useful than the same text 200 lines above it.

### Not every long comment is wrong

`step_2_eda_descriptive.py` has a long docstring explaining the section-runner
mechanism, and that mechanism genuinely needs explaining — it is how the
pipeline handles per-category column variation. Keep it, strip
`DEC-DISCOVER-COLUMNS (P0038, 2026-08-12)` from the heading, and cut it from
banner style into prose.

The judgement is **does the code need this to be understood**, not **is it long**.

---

## Rule 5 — Sever internal path references

17 code sites name a path that will not exist in the submission repo. Each is a
comment or an error message.

| Kind | Before | After |
|---|---|---|
| Comment cross-ref | `# ... preserved at plans/P0035_.../preserved_chain_grain_results/.` | delete the sentence |
| Error message | `"see writing-notes/unverified-claims-to-check.md item 1 before ..."` | reword to name the check, not the file |
| Style reference | `# greyscale palette (see .claude/rules/figure-generation-standards.md)` | `# greyscale tier palette` |
| Root anchor | `"""Anchor on .env.example per DEC-P0046-ANCHOR -- never CLAUDE.md, never cwd..."""` | `"""Find the repo root by searching upward for .env.example."""` |

The root-finder case appears in six files with near-identical wording. It is
also the one place where a `CLAUDE.md` mention is *functional* rather than
decorative — the comment explains why that file is not the anchor. In the
submission repo `CLAUDE.md` does not exist, so the whole clause goes.

---

## What NOT to strip

Being thorough here is how the pass avoids destroying the code's value:

| Keep | Because |
|---|---|
| Every "why this and not the obvious alternative" comment | this is what distinguishes considered code from generated code |
| Concrete measured evidence (35 columns, three spellings, 17 test origins) | it is the justification, and it is checkable |
| Formulas and derivations | an assessor may verify the arithmetic |
| Warnings about correctness traps ("assert == 1, not > 0") | real engineering knowledge |
| Section-divider comments (`# ==== CATEGORIES ====`) | ordinary navigation, not meta |
| Docstrings on functions | keep them; shorten if they run past ~8 lines |
| `Usage:` blocks | an assessor needs to know how to run it |
| SRQ / research-question references | these are thesis vocabulary the assessor shares |

The last row matters. `SRQ1`, `SRQ4`, `Scenario A/B/C`, `H=3`, `WMAPE`,
`DEC-GRAIN`'s *content* — the brand × month grain — are all thesis concepts.
Only the internal *labels* go.

---

## Order of work

Per file, in this order, because each step narrows the next:

1. **File docstring** — usually the largest single win
2. **Module-level comment blocks** — the `# ==== SECTION ====` essays
3. **Inline markers** — the remaining `DEC-`/`P00NN`/`F\d+` hits from the grep inventory
4. **Error and log message strings** — easy to miss; they carry internal paths
5. **Read the file top to bottom** as an assessor would, and cut what still
   reads as a note to a collaborator

Step 5 is not optional. The greps find labels; only reading finds tone.
