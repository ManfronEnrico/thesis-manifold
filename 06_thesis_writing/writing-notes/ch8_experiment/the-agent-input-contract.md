---
name: the-agent-input-contract
description: NOTE - What data the scenarios receive and why that exact cut is the fair one. Covers the post-join/pre-cleaning boundary, the schema dictionary, the SKU-to-brand aggregation, and the three declared human choices that must be stated in the methodology.
category: reference
applies-to: [ch8_experiment, ch3_methodology, ch10_limitations]
triggers: [what data did the scenarios get, experiment setup, fair comparison, methodology for SRQ4]
created: 2026_09_12-19_35
updated: 2026_09_12-19_35
status: bullets, not prose
---

# The agent input contract

**What changed, 2026-09-12.** Until this date the data-access scenarios
received **four columns** sliced off the engineered feature matrix. They now
receive the **32-column warehouse extract** plus the warehouse's own column
dictionary. Prompt schema v5 to v6. This note records why, because the
methodology chapter has to defend the choice.

---

## The boundary, and why it is where it is

The scenarios are handed data at exactly one point in the pipeline:

> **post-join, post-market-filter, post-brand-month-aggregation;
> pre-cleaning, pre-imputation, pre-feature-engineering**

The reasoning is an argument about what the comparison is *for*:

- Prometheus in production reaches a **live star schema**. Asked this question
  it would join facts to the product, period and market dimensions, filter to a
  market, and aggregate to brand-month. That work is not the contribution; it
  is table stakes, and a production agent does it unaided.
- The **EDA, cleaning, feature engineering, tuning and calibration** *are* the
  contribution. Handing those over would mean measuring nothing.
- So the extract stops precisely between the two.

**That frame existed nowhere on disk.** The converted tier holds un-joined
views; the engineered tier holds a frame that already carries the human
choices. `build_agent_inputs.py` was written to produce the missing state.

### What was wrong with the old four-column payload

Three separate defects, all in the same direction:

1. It withheld 28 warehouse measures a production agent would hold, which made
   "the agent found no signal" **unfalsifiable** -- it was never given the
   signal to find.
2. One of the four columns, `promo_intensity`, is an **engineered feature** (a
   shifted ratio built by the pipeline), so the old payload simultaneously
   withheld raw data and leaked a piece of the pipeline.
3. It asked for a column by a name the matrix does not use, so that column was
   **silently dropped** with no error.

---

## The three declared human choices

Unavoidable, and therefore stated rather than hidden. All three are written
into the generated `manifest.json` beside the data.

| Choice | What was done | Why it is not a modelling decision |
|---|---|---|
| **Market** | `DVH EXCL. HD` | Nielsen's own recommended universe; the same market the models train on. Chosen by the data provider, not by us. |
| **SKU to brand** | sum across SKUs | `dim_product` is **UPC-only** -- there are no brand-level rows -- so brand-month cannot be reached any other way. A production agent faces the identical constraint. |
| **Sum vs mean** | volume sums, distribution averages | Follows the `unit` field of the warehouse's own metadata. Distribution measures are ACV-weighted fractions of category turnover and are documented as **not additive across products**. |

**The SKU aggregation is worth one sentence in the limitations.** It embeds one
modelling decision into the data before the agent sees it: the brand is treated
as the sum of its SKUs, which is the right grain for the question but is still
a choice the agent did not make and could not revisit.

---

## What is deliberately NOT done to the data

- **No zero-filling.** Nulls are preserved as nulls throughout. A zero asserts
  "this was measured and it was zero", a claim the warehouse does not make.
- No outlier handling, no imputation, no smoothing, no derived columns.
- No hint in the prompt that any particular column matters, no warning about
  the sparsity, no suggested method.

Working out which of 32 columns carries signal **is the task being measured.**

---

## The schema dictionary

Every data arm also receives the warehouse's own column documentation: 70 rows
covering four tables, with data type, unit, null meaning and description.

- A production Prometheus can read its warehouse's column docs. Withholding
  them would hand the agent 32 unexplained columns.
- Without it, a poor result is **unattributable**: we could not separate "could
  not model it" from "could not read it".
- It is the warehouse's text, unedited. We add nothing.
- It goes to **all seven arms**, including the model-only ones, so the shared
  context is genuinely shared. An arm without it would differ from its pair in
  a second way.

---

## The leakage boundary is enforced at write time

- Visible window is **train + validation**: 39 months ending 2025-12 for CSD at
  H=3. The test window is never visible to any scenario.
- The cut is applied **in the generator**, not in the harness. A file on disk
  that is safe only if every reader remembers to truncate it will leak the
  first time someone opens it for another purpose.
- The boundary is **read** from the pipeline's persisted split file, never
  recomputed, so there is no second implementation to drift.
- The harness re-checks it independently on every run. Two checks of the same
  boundary, by different code, is the point.

---

## Figures for the methodology chapter

Computed 2026-09-12; recompute before quoting.

| | |
|---|---|
| Columns sent (was 4) | 32 |
| Visible months per brand | 39 (2022-10 .. 2025-12) |
| Months withheld as test | 7 |
| Schema dictionary rows | 70, across 4 tables |
| Mean payload, series + dictionary | ~12,300 tokens per run |
| Added input cost | ~$0.058 per data-arm run |

---

## Related

- [[ad-hoc-data-science-vs-a-trained-pipeline]] -- why the sparsity in this
  data is the point rather than a nuisance
- [[brand-sampling-and-inclusion-criteria]] -- which brands, and why
- `04_SRQ4_Scenario_Experiment/scenario_setup/build_agent_inputs.py` -- the
  generator, whose docstring carries the same reasoning
