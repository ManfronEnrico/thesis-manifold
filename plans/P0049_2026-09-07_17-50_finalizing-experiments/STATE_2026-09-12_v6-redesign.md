---
name: state-2026-09-12-v6-redesign
description: STATE - The 2026-09-12 input and prompt redesign. What the scenarios now receive, why the prompt schema went v5 -> v6, what that invalidates, and where the funded run stands. Read this before LAUNCH_THE_FUNDED_RUN.md, which it partly supersedes.
pid: P0049
created: 2026_09_12-20_10
updated: 2026_09_12-20_10
status: in_progress
---

# 2026-09-12 — the v6 redesign

> **This supersedes parts of `LAUNCH_THE_FUNDED_RUN.md`.** That file still has
> the right command and the right three brands, but its **cost table and schema
> id are from v5** and are now wrong. Read this first.

Two changes landed together, because both alter every data arm and a schema id
cannot be bumped twice for one run.

---

## 1. THE DATA — the scenarios were being starved

**Found by Brian**, inspecting the input CSV.

The data arms were receiving **four columns**, sliced off the *engineered*
feature matrix. The warehouse holds **32**. Three separate defects, all in the
same direction:

| | |
|---|---|
| **Withheld 28 columns** | a production Prometheus joins the star schema and holds all of them. Withholding made *"the agent found no signal"* **unfalsifiable** — it was never given the signal to find. |
| **Leaked a pipeline feature** | one of the four, `promo_intensity`, is an **engineered** shifted ratio. So the payload simultaneously starved the agent of raw data and handed it a piece of the pipeline under measurement. |
| **Silently dropped a column** | the slice asked for `weighted_distribution`; the matrix calls it `weighted_dist`. No error. The dominant failure mode on this project, again. |

### The boundary, and why it is there

Brian's framing, which is now the methodology:

> Prometheus in production reaches a **live star schema**. It would join,
> filter and aggregate to brand-month itself — that is table stakes. The
> **EDA, cleaning, feature engineering and tuning are the proprietary
> pipeline**, and they are what SRQ4 measures. So the agents get the data at
> exactly the point between those two things.

**post-join, post-market-filter, post-brand-month-aggregation;
pre-cleaning, pre-imputation, pre-feature-engineering.**

That frame **existed nowhere on disk** — `_01_converted` holds un-joined views,
`_03_engineered` holds a frame carrying the human choices. So it had to be
built.

### New: `build_agent_inputs.py`

Writes to `SRQ4_AGENT_INPUTS_DIR` (new PATHS constant), per category:

```
agent_inputs/CSD/HARBOE_brand_month.csv     39 rows x 33 cols
                 7-UP_brand_month.csv
                 OERBAEK_brand_month.csv
                 schema_dictionary.csv       70 rows, 4 tables
                 manifest.json               every choice, declared
```

**Three declared human choices**, all in the manifest:

- **Market** `DVH EXCL. HD` — Nielsen's own recommended universe, the same one
  the models train on. A one-id assertion guards the 6.16x fan-out defect.
- **SKU → brand** — `dim_product` is **UPC-only**; there are no brand-level
  rows, so brand-month cannot be reached any other way. Worth one limitations
  sentence: it embeds one aggregation decision before the agent sees anything.
- **Sum vs mean** — volume sums, distribution averages, following the `unit`
  field of the warehouse's own metadata.

**Nulls are preserved, never zero-filled.** A zero asserts "measured, and it
was zero", which the warehouse does not say. The sparsity varies enormously by
brand (HARBOE 3 columns with nulls, ØRBÆK 7, three of them 100% empty) and
handling it is exactly the judgement being measured.

### THE LEAKAGE CUT IS IN THE GENERATOR, NOT THE HARNESS

**Brian's call, and it is the right one.** The warehouse runs to 2026-07;
validation ends **2025-12**. An untruncated extract would hand the agent the
month it is asked to forecast.

The cut is applied **at write time**, so the file on disk cannot leak. A file
that is safe only if every reader remembers to truncate it leaks the first time
someone opens it for another purpose. The boundary is **read** from
`csd_split_dates_h3.json`, never recomputed — no second implementation to
drift. The harness re-asserts it independently on every run.

Result: **39 visible months (2022-10 .. 2025-12), 7 withheld**, all three
brands.

---

## 2. THE PROMPTS — comparable arms had drifted apart

**Also found by Brian.** The capability notes were hand-written per arm, so
arms that are supposed to differ *only in orchestrator* also differed in
wording:

- B named the five libraries; **D did not**.
- D's coder brief asked for *"the point forecast, a 90% interval and how
  confident you are"*; **B's asked for none of that** — yet both are scored on
  interval communication.
- D prescribed mechanics (`io.StringIO`); B did not.
- E glossed every payload field; **C, which receives the same fields, got no
  gloss**.

Individually trivial. Together they mean **B→D and C→E did not isolate the
orchestrator** — wording travelled with it, which is the exact confound the
shared user question exists to remove.

### v6: notes are COMPOSED, not written

`DATA_BLOCK`, `MODEL_BLOCK`, `MODEL_TOOL_BLOCK`, `ANALYSIS_TASK`,
`ANALYSIS_TASK_WITH_MODEL`, `NO_WAREHOUSE`, `ENGINE_NOTE` — assembled per arm.
A difference between two arms is now a **different component**, not a turn of
phrase.

**What is still allowed to differ, and nothing else:**

1. Which capability the arm has. That is the treatment.
2. The warehouse instruction, **D/E/G only** — their nested coder has the SQL
   tools registered at module scope in the vendor tree
   (`prometheus_coder.py:327`, verified 2026-09-12). B/C/F have no such tools,
   so the sentence would describe a capability they lack.
3. A short conversational-agent note for D/E/G, because Prometheus is two
   agents and the coder never sees the user message.

**No gloss on C or E** (Brian: *"neither does"*) — minimal input, the agent
reasons for itself.

`python prompts.py` now renders **all seven arms** and runs a
**shared-component check** that asserts the pairs are byte-identical. The v5
demo printed three arms, which is how the drift survived.

### On not forking Prometheus

Brian pushed back on "a fork forfeits ecological validity", correctly — that
argument is weak on its own. The load-bearing reason to keep the SQL tools
registered is different: **compliance is measured per run via `sql_calls`**,
which is stronger evidence than a filtered tool list because it is observed
rather than configured and trusted. A run that queries anyway is classified
`warehouse_access` and excluded, not quietly kept.

---

## What this invalidates

| | |
|---|---|
| **Schema id** | `v5-seven-scenarios+d22fe7cdc30e` → **`v6-shared-composition+af04a42a478b`** |
| **Every v5 row** | no longer pools. Correct: they were asked a different question over different data. |
| **The v5 cost table** | wrong. See the measurements below. |
| **`LAUNCH_THE_FUNDED_RUN.md`** | command and brands still right; cost and schema id stale. |

---

## Cost, measured on the v6 smoke (2026-09-12)

Balance before the run: **$44.41**. First five runs:

| arm | v6 actual | v5 estimate | ratio |
|---|---|---|---|
| A_llm_plain | 0.4108 | 0.6432 | 0.64x |
| B_llm_data | 0.2718 | 0.2243 | 1.21x |
| C_llm_model | 0.0092 | 0.0090 | 1.03x |
| **D_prometheus_data** | **0.9605** | 0.5190 | **1.85x** |
| E_prometheus_model | 0.2077 | 0.2021 | 1.03x |

**D is the one that moved.** 103,662 input and 14,740 output tokens on a single
run — the nested coder iterating over a 32-column frame. Since output is 6x the
input price, the combined arms F and G are the ones to watch.

Update the dry-run table from the completed smoke before funding anything.

---

## State at this moment

- Pre-flight **13/13**. The leakage check now covers **all three funded
  brands** rather than one — it used to sample top-2-by-volume, which after the
  data change verified only 1 of the 3 that actually run.
- All six harness scripts compile.
- The v6 smoke (21 runs, 1 repeat x 3 brands x 7 arms) is **running**.
- Two writing notes added:
  `ch9_discussion/ad-hoc-data-science-vs-a-trained-pipeline.md` and
  `ch8_experiment/the-agent-input-contract.md`.

## Next

1. Finish the smoke; read actual F and G costs.
2. Refresh the dry-run estimate table with v6 measurements.
3. Re-cost the funded run and compare against the $44.41 baseline.
4. Then decide repeats vs brands for the funded set — the cache supports both
   (`--append` for repeats, more brands needs no flag at all).
