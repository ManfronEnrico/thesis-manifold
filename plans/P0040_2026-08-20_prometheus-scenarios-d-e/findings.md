---
pid: P0040
created: 2026-08-20 00:00:00
updated: 2026-08-21 00:00:00
---

# P0040 — Findings

## F1 — An integration blueprint already exists, but predates engine access

`.archive/thesis_agents_preintegration/system_a_oracle/` holds
`forecast_demand_tool.py`, a README and a persona doc describing registration of a
`forecast_demand` tool with the Graph Engine.

It names specifics that would be hard to invent: the decorator `@data_agent.tool`;
imports from `data_agents.agents.base_agents`, `data_agents.types.agent_deps_types`;
`ProjectDeps(agent_name=..., tool_names=[..., "forecast_demand"])`; pydantic_ai's
`RunContext`; deployment by copying to `graph-engine/data_agents/projects/oracle/`
and registering in `langgraph.json`; engine `.env` needing `OPENAI_API_KEY` +
`E2B_API_KEY`.

**Provenance is uncertain and Brian believes it predates access** — likely written
without sight of the shipped engine. Its README concedes it was never run.
**Status: hypothesis, pending task 1.** The value if it holds is large: the
expensive unknown (the tool API) would already be answered.

One detail worth preserving whatever else changes — the tool's return string ends:

> `Source: dedicated {model} model (not generated code).`

The SRQ4 contrast is already surfaced to the agent in its own words.

## F2 — Three specific staleness points in the blueprint

Independent of whether the API matches:

1. Resolves `forecast_service.py` via `parents[3] / "scripts"` — a pre-P0028 path
   that no longer exists. Must become a `PATHS.py` import.
2. Accepts a `chain` parameter and reads `_07_forecast_service/` — the chain grain
   was deleted per DEC-GRAIN.
3. Describes "~50 prompts" and "System A / System B" — superseded by 1 prompt x N
   repeats and the reversed scenario lettering.

None are hard fixes.

## F3 — A single Prometheus scenario would have confounded engine with tool

The initial proposal (one scenario D: Prometheus + tool) would have moved two
variables at once relative to C. Brian's split into `D_prometheus` (plain) and
`E_prometheus_model` (tooled) isolates the tool within one engine.

Second benefit, not obvious at first: **D->E and B->C are the same intervention on
two different orchestrators.** Directional agreement is a much stronger claim than
a single comparison, and it turns D/E's non-reproducibility from a weakness into a
two-tier design where a reproducible core and an ecological validation corroborate
each other.

## F4 — The warehouse-vs-snapshot concern is largely theoretical within August

Initially flagged as a leakage and comparability risk: if D/E read the live Royal
Unibrew warehouse while A-C read the local Nielsen snapshot, inputs differ and the
live source might expose the held-out target month.

**Brian's correction:** the warehouse is refreshed roughly **monthly, not daily**. A
re-poll on 2026-08-19 returned data through **July 2026 — the same cutoff as the
local snapshot.** Within August the two sources are the same snapshot.

Residual risks, both manageable:

- The equivalence is a **timing coincidence, not a guarantee**. It expires at the
  next warehouse refresh. Re-verify if the run slips past August.
- Pointing at the local snapshot (`data_credentials.json`, `type: file`) makes
  identical-input an *enforced property*. Preferred where supported.

Record which source each run used in its trace either way.

## F5 — Prometheus rescues the RAM-budget argument rather than undermining it

Brian's worry was that plugging in a ~500 MB engine invalidates the
compute-constraint chapter.

The opposite. `generate_figures.py::fig4_ram_budget` is currently **fabricated** —
hardcoded literals including a 512 MB "active ML model" — against a **measured 3-4
MB** for the served model. Indefensible as it stands.

The real structure is stronger:

| Component | Footprint |
|-----------|-----------|
| Trained model, served | 3-4 MB (measured) |
| Agent runtime / graph engine | hundreds of MB (to measure, task 9) |

The claim becomes *"the model is the cheap part; the agent runtime is where the
budget goes"* — which is both true and more interesting than the invented version.
Task 9 turns the thesis's weakest figure into a genuine measurement.

## F6 — P0037's Prometheus exclusion has expired

P0037 lists under Out of scope: *"Prometheus/Graph Engine integration (SRQ3 is an
assessment, pending NDA)."* Access has landed. This is an argument for a **new
plan** (P0040) rather than reopening P0037's scope, whose remaining tasks (2, 6, 8,
9) are unrelated serving-interface cleanup.

## F7 — Access alone does not reconvert SRQ3

An earlier claim of mine, **corrected**: I said obtaining Prometheus makes SRQ3
"stop being an assessment and start being a real integration."
`srq3-integration-readiness.md` frames SRQ3 as an assessment **by design**, not
solely because access was blocked. Whether to reframe it is a scope decision for
Brian and Enrico. Recorded so the assumption is not silently inherited.

## F8 — RESOLVED: the RQ commits to per-CATEGORY vs pooled, not per-brand

Raised by Brian as a possible next modelling iteration, with a recollection that
pooled-vs-individual was an actual research-question commitment. **Verified against
the RQ documents 2026-08-20. The recollection is half right, and the wrong half
changes the cost.**

**Committed — and named in the SRQ1 headline question itself:**

> "the best trade-off between accuracy, memory efficiency, and **category
> specialization** for FMCG demand forecasting under computational constraints"

`srq1-models-efficiency.md:32` glosses it explicitly as a v4 addition: *"category
specialization added as a third trade-off dimension alongside accuracy and memory
-- i.e. does a per-category model beat a single pooled model?"* Scope item 5 (:40)
and the literature-selection criteria (:51) repeat it.

**Not committed:** pooled vs **per-brand**. Every hit says *category*. The per-brand
framing appears only in a P0039 aside noting CSD has the most brands. Nothing in
the RQ documents obliges it.

The distinction matters for effort:

| Reading | Meaning | Work |
|---------|---------|------|
| per-category vs pooled (**committed**) | 4 category models vs 1 model over all four | one extra training run + comparison |
| per-brand vs pooled (not committed) | ~85 brand models per category | much larger |

Per-category is already the default, so only the **pooled** side needs building.

### Consequence 1 — the ensemble stays deferred

Confirming the commitment does **not** rescue the ensemble. They are different axes:
category specialization asks *what scope of data one model is fit on*; the ensemble
asks *whether to combine several model families*. The RQ commits to the first and is
silent on the second. **Ensemble remains genuinely deferrable.**

### Consequence 2 — this is a results gap, not a nice-to-have

SRQ1 names a three-way trade-off. `tuned_metrics.csv` reports accuracy and memory
and **nothing pooled**. The thesis currently asks a question in its own SRQ1 heading
that its results do not answer. Unlike a missing ensemble, an examiner reading SRQ1
will look for this specifically. Treat as a real gap when sequencing the remaining
month.

### Incidental — the five-category error reaches the RQ documents too

`srq1-models-efficiency.md:40` still reads "across the **five** categories." That is
the same contradiction `check_chapter_facts.py` finds in the chapter drafts, but the
script only scans `05_thesis_writing/sections-drafts/` and therefore misses it.
Consider extending its scan path to `01_thesis_research/research-questions/`.

## F9 — Brands are NOT mutually exclusive across categories; `OTHER BRAND` is a trap

Measured 2026-08-20 from the four `*_feature_matrix_h3.parquet` files.

| Category | Brands | Rows | Cols |
|----------|--------|------|------|
| CSD | 95 | 4,370 | 51 |
| danskvand | 29 | 1,189 | 33 |
| energidrikke | 44 | 1,892 | 51 |
| RTD | 62 | 2,542 | 49 |

Union of brand names = **213**, sum = **230**, so **17 names recur**. Most are
genuine multi-category brands (HARBOE, FEVER TREE, SAN PELLEGRINO, SAN BENEDETTO,
AQUA D'OR — CSD and danskvand share 11).

**But `OTHER BRAND` appears in danskvand, energidrikke and RTD, and it is not a
brand — it is a residual bucket whose contents differ per category.**

**Consequence for pooling: the series key must be `(category, brand)`, never
`brand`.** Pooling on name alone would merge HARBOE's CSD and danskvand series and
collapse three unrelated residual aggregates into one. This is the same class of
defect P0027 found in `engineer_features.py` (grouping by `brand` only, conflating
across `market_id`).

## F10 — Feature intersection is 33 of 51 columns, and the gap is one coherent family

| | Count |
|---|---|
| Columns present in all 4 categories | **33** |
| Union across categories | 51 |
| Missing from at least one | 18 |

The 18 are almost entirely one family: `baseline_*`, `promo_*`, and the
`weighted_distribution_*` promo/feature/display variants.

**They are missing for a substantive reason, not an arbitrary one: danskvand and
RTD have no promo signal** (the promo-zero finding from P0036). `promo_intensity`
and `promo_units` exist only in CSD and energidrikke; the rest exist in all but
danskvand.

### Recommendation — intersect, do not union-with-NaN

| Option | Consequence |
|--------|-------------|
| **Intersection (33 cols)** | Loses promo for CSD/energidrikke only — danskvand/RTD never had it |
| Union + NaN | Two categories carry a structurally all-missing block. Trees tolerate NaN, but here "missing" means *structurally absent*, not *unobserved* — the model can learn `NaN => danskvand`, turning the pooled model into a disguised category indicator |

The decisive argument is **experimental, not statistical**: the comparison must be
pooled-vs-per-category with *one* variable moving. If the pooled model sees a
different feature set than the per-category models, two things change at once. Run
**both sides on the same 33 columns.**

For the write-up: the intersection is a *consequence* of promo absence in two
categories — a finding, not an arbitrary restriction.

## F11 — SRQ4 brand selection is CSD-weighted; 3 per category is the fair basis

Brian's observation. CSD has 95 brands against danskvand's 29, and runs to date drew
top-N by volume weighted toward CSD. A result generalised from a
predominantly-CSD sample is a CSD finding presented as a general one.

**At least 3 brands per category (12 pairs) is the defensible minimum.** The
`--brands` and `--categories` flags added 2026-08-19 already express this; no new
code needed. Independent of the pooled question and worth fixing regardless.

## F12 — REVISED: the ensemble becomes cheap once pooled exists

F8 concluded the ensemble stays deferred because it is a different axis from
category specialization. That reasoning was correct about the RQ but missed the
implementation coupling.

Building the pooled path requires code that fits one model across multiple category
datasets on a common feature set — schema alignment, a shared eval harness,
comparable metrics. **An ensemble over model families reuses all of that
infrastructure.**

Revised sequencing:

1. **Pooled comparison** — closes a named SRQ1 gap. Build it.
2. **Ensemble** — still not RQ-obligated, but its marginal cost drops sharply once
   (1) lands, and it beats the single best model in 3 of 4 categories.

So: deferred **until pooled lands**, then reassess with real numbers — not deferred
indefinitely. If time is tight at that point it can be dropped without loss, since
the RQ does not ask for it.

## F13 — VERIFIED: the archived blueprint's API is correct (tasks 1-2 closed)

Engine extracted to `Z:\_dev-ssd\prometheus\prometheus-graph-engine\graph-engine`.
Inspected 2026-08-20. **F1's hypothesis holds.** Every element the blueprint named
exists in the shipped engine:

| Blueprint claim | Shipped engine |
|-----------------|----------------|
| `langgraph.json` graph registry | present; 21 agents registered |
| `data_agents/projects/<name>/<name>.py:<name>_graph` | exactly the pattern |
| `ProjectDeps(agent_name, company_name, data, tool_names, ...)` | exact |
| `@data_agent.tool` decorator | exact |
| pydantic_ai `RunContext[CodeExecutorDeps]` | exact |
| `create_quantitative_research_graph(deps)` | exact |
| E2B code execution | `data_agents.tools.code_executor.execute_code` |

The engine is **LangGraph + pydantic_ai**, as Brian expected.

`prometheus.py` also shows the engine already runs **`main_agent_model="gpt-5.5"`
and `coder_model="gpt-5.5"`** — the same family as scenarios A-C. That is a
material comparability win nobody planned: D/E will not differ from A-C by base
model.

### A current, working tool example exists

`data_agents/projects/prometheus/tools/weekly_report_tool.py` is a live tool in the
shipped project, not an archived guess. It is the template to copy for
`forecast_demand` — same decorator, same `RunContext[CodeExecutorDeps]` signature,
same docstring-as-agent-instruction convention.

Note its import: `from data_agents.graphs.quantitative_research_graph import
quantitative_data_agent as data_agent`. The blueprint imported from
`data_agents.agents.base_agents` instead. **Follow the shipped file, not the
blueprint**, on this detail.

### Registration path for E_prometheus_model

1. Add `forecast_demand_tool.py` under `projects/<oracle>/tools/`
2. Import it in the project module (import triggers registration)
3. Add `"forecast_demand"` to `ProjectDeps.tool_names`
4. Register the graph in `langgraph.json`

`D_prometheus` needs none of this — it is the shipped project as-is.

## F14 — Data access is warehouse-only in the shipped config (task 3)

`data_agents/projects/prometheus/data/data_credentials.json` declares
`"type": "database"` against the RU Azure SQL warehouse, with `RU_SERVER_STRING`,
`RU_CLIENT_ID`, `RU_CLIENT_SECRET`, `RU_TENANT_ID`, plus `E2B_API_KEY` and
`PROMETHEUS_TEMPLATE_ID`.

**This contradicts the assumption in DEC-PROMETHEUS-DATA that a local-snapshot mode
was readily available.** The archived blueprint's `"type": "file"` may be a
supported loader variant (`load_data_sources` should reveal this) or may have been
aspirational. **Not yet verified — do not treat local-snapshot mode as available.**

Consequence: if only warehouse access works, F4's monthly-refresh argument becomes
load-bearing rather than a convenience. It still holds for August (both sources at
July 2026), but the equivalence must be re-verified before each run rather than
enforced structurally.

Next check: read `data_agents/utils/load_data.py::load_data_sources` for supported
`type` values.

## F15 — CORRECTION: SRQ4 brand selection was never CSD-only by default

F11 attributed the CSD-heavy runs to the selector. **Wrong.** Reading
`_select_brands`, the default `per_cat=(4, 4, 4, 3)` already draws top-N *per
category across all four*. The CSD-heavy runs came from Brian passing
`--categories CSD` during testing, not from a biased default.

The real, remaining methodological question is **volume-ranking**, not category
balance: `_eligible_brands` sorts by total `sales_units` descending, so every
scenario is evaluated on the largest, most stable, data-richest series. That does
not bias the *comparison* (all scenarios see identical brands) but it does limit
generalization — it cannot answer whether C's advantage survives on thin, volatile
brands. Stratified or random sampling would; volume-ranking will not.

F11's "3 per category" recommendation is therefore near-moot; the default is
already 4/4/4/3.

## F16 — CORRECTION: SHAP importance already exists, and clears the promo confound

I recommended "check feature importance for promo before committing to pooling."
**It was already on disk:** `04_thesis_results/srq1/shap_importance.csv`, produced
by `03_thesis_modelling/model_training/srq1/srq1_shap.py`, covering all four
categories. Brian was right that this belongs to model training/evaluation and
right to ask why it was not consulted.

Measured `mean_abs_shap`, top features:

| Category | 1st | 2nd | `promo_intensity` |
|----------|-----|-----|-------------------|
| CSD | lag_1 (1.319) | weighted_distribution (1.146) | **0.100** (7th, 7.6% of lag_1) |
| energidrikke | lag_1 (1.428) | weighted_distribution (1.150) | **not in top 8** |
| danskvand | lag_1 (1.344) | weighted_distribution (0.607) | n/a (no promo) |
| RTD | lag_1 (1.464) | weighted_distribution (0.760) | n/a (no promo) |

**Verdict: the intersection is safe.** Promo is a minor contributor even where it
exists. Dropping it costs CSD little and energidrikke almost nothing. The confound
I flagged is real in principle but small in this data.

Structure is strikingly consistent across all four categories — `lag_1` then
`weighted_distribution` dominate everywhere — which is itself a mild prior *in
favour* of pooling working.

### Two caveats on this artifact

1. **It is stale.** `holiday_month` appears in the CSD and RTD rows — the
   pre-rename name (now `peak_month`). So `shap_importance.csv` predates that
   rename and probably the 2026-08-19 re-tuning. **Regenerate before citing.**
2. **Correlation matrices are per-category only**, produced in the EDA layer
   (`pre_csd_1.5_eda.py`, the CSD notebook), not in `srq1/`. There is no
   cross-category correlation view, which is what pooling would actually want.
   Cheap to produce and worth doing alongside the pooled run.

## F17 — What "NaN => danskvand" would actually cost (answering Brian's question)

Concretely: pool all four categories with all 51 columns and every danskvand row
has `promo_intensity = NaN`. XGBoost learns a default direction per split, so it
can split on *is-NaN* — and that split separates danskvand from CSD/energidrikke
perfectly.

The pooled model then contains a hidden category indicator, letting it learn
per-category behaviour internally. **It partly becomes four models wearing one
coat.**

This is **not a correctness bug** — predictions would be fine, possibly good. It is
a **construct validity** problem specific to this experiment: the question is
"does one pooled model match four specialized ones?", and if the pooled model can
reconstruct the specialization from missingness, a good score no longer
distinguishes "cross-category learning helped" from "the model rebuilt the
specialization internally."

With the 33-column intersection the shortcut does not exist, so the measurement
answers the question asked. This is the same reasoning as running both sides on
identical features: keep one variable moving.

## F18 — `type: "file"` IS a supported value, but it changes less than hoped (task 3 closed)

Read `data_agents/utils/load_data.py::load_data_sources` and
`data_agents/types/data_types.py` on 2026-08-20.

**`type` is a declared enum:**

```python
type: Literal["file", "database", "url", "api"]
```

So `"file"` is legal and the archived blueprint's `type: "file"` was **not
invented** — it is a real supported value. F14's caution is partly relieved.

**But `load_data_sources` never branches on `type`.** It reads the JSON and passes
`source_data.get("type")` straight into `EnhancedDataSource`; the only consumer is
`get_data_source_type()`, which stringifies it. Grep across `data_agents/` and
`core/` finds no `if type == "file"` dispatch anywhere.

**What this means:** `type` is **descriptive metadata handed to the agent**, not a
loader switch. It tells the LLM what kind of source it is dealing with; it does not
cause the engine to load a parquet file. The actual mechanism is
`DataSource.extract_all_env_vars()` -> `passed_envs` -> the E2B sandbox
(`code_executor.py:64-67`), i.e. **credentials are forwarded to the sandbox and the
agent's generated code does the reading.**

### Consequence for D/E

Pointing Prometheus at the local Nielsen snapshot is **not a config-file change**.
Options, in ascending cost:

1. **Warehouse, as shipped.** Zero engine changes. Relies on F4's monthly-refresh
   equivalence, which is a timing property to re-verify per run, not a guarantee.
2. **Declare a `file` source and make the snapshot reachable inside the sandbox.**
   Needs the parquet to exist in the E2B template or be uploaded per run, plus
   `data_model.md` / `data_summary.md` describing it so the coder writes correct
   code against it. Real work, not a one-line edit.
3. **Bypass for `E_prometheus_model` only** — the `forecast_demand` tool reads the
   local persisted models directly, exactly as `C_model` does, and never touches
   the warehouse. **This already works with no engine change**, because the tool
   runs in-process, not in the sandbox.

Note what (3) implies: in `E_prometheus_model` the *forecast* is guaranteed to come
from the same local models as `C_model`, regardless of what the warehouse holds.
Only `D_prometheus`, which must query data to write its own code, depends on
warehouse state. That narrows the comparability exposure to a single scenario.

**Recommendation: option 1 for now**, with the August equivalence recorded in each
run trace, and option 2 only if the run slips past the next warehouse refresh.

## F19 — Credentials: only two are missing

`data_credentials.json` requires `RU_SERVER_STRING`, `RU_CLIENT_ID`,
`RU_CLIENT_SECRET`, `RU_TENANT_ID`, `E2B_API_KEY`, `PROMETHEUS_TEMPLATE_ID`.

**Brian holds the four RU warehouse credentials. Missing: `E2B_API_KEY` and
`PROMETHEUS_TEMPLATE_ID`** — both to request from Enrico.

`PROMETHEUS_TEMPLATE_ID` is the E2B sandbox template. The archived blueprint flagged
"E2B template id to confirm" as its known unknown back then; it is still the open
item now. The engine also does an Azure SQL token swap
(`security/token_swap.py`, `swap_credentials_for_tokens`) before handing env vars to
the sandbox, so the RU credentials must be the kind that swap succeeds for.

## F20 — Stratified brand sampling answers the generalization question within budget

Brian's proposal, in response to F15's volume-ranking concern: instead of top-N by
volume, take **highest / median / lowest volume brand per category**.

**This is strictly better than top-N at the same cost.** 3 brands x 4 categories =
12 pairs, versus the current default's 15, so it is actually *cheaper* while
covering the volume range rather than only its top.

Why it matters: `C_model`'s advantage is currently measured only on the largest,
most data-rich, most stable series — precisely where a trained model should do
best. A reviewer asking "does this hold for a thin, volatile brand?" cannot be
answered from volume-ranked runs. Stratified sampling answers it directly, and if
C's advantage *narrows* at the low end that is a finding worth reporting, not a
failure.

Implementation: a `--brand-strategy {volume,stratified}` flag selecting from
`_eligible_brands()`, which is already volume-sorted -- so median and lowest are
just index arithmetic on an existing list. Cheap.

Caveat to check when picking the "lowest" brand: it must still have a held-out test
actual (`_eligible_brands` already enforces this) and enough history that the
per-category model was actually fit on it. The lowest-volume eligible brand may sit
near MIN_PERIODS; verify before locking the selection.

## F21 — Pooled EDA: Brian is right, no new per-category EDA is needed

Brian's question, and his lean, both correct. The four categories each already have
a full EDA (stationarity, missingness, distribution, ACF/PACF). Pooling consumes
their **cleaned, engineered outputs** -- it introduces no new raw data and no new
cleaning decisions, so re-running per-category EDA would re-derive what already
exists.

What pooling *does* introduce is **cross-category structure**, which no existing
artifact covers. Three things are worth producing, and only these:

1. **Cross-category correlation matrix** on the 33 shared columns -- does
   `weighted_distribution` relate to `log_sales_units` the same way in each
   category, or do relationships invert? An inversion is an argument *against*
   pooling and should be known before the run, not after.
2. **Scale comparability.** CSD's brand-months and danskvand's differ in magnitude;
   pooling raw `sales_units` across them lets the large category dominate the loss.
   The target is already `log_sales_units`, which largely handles this -- confirm
   rather than assume.
3. **Per-category residual breakdown of the pooled model.** The headline pooled
   metric can look fine while one category is badly served. This is where the
   pooled-vs-per-category answer actually lives.

So: no full EDA, one correlation matrix plus two checks.

## F22 — Stratified sampling: "lowest volume" is UNUSABLE; use lowest-with-signal

Brian's caveat confirmed, and the real problem is worse than short history. Every
brand in a category shares the same split geometry (CSD 32/7/7, danskvand 29/6/6,
energidrikke 30/6/7, RTD 29/6/6) and the same ~22-26 fit rows, so **history length
is not the discriminator**. Sparsity is:

| Category | lowest-volume brand | nonzero months | test actuals |
|----------|--------------------|----------------|--------------|
| CSD | DOCTOR POLIDORIS | 23/46 | `[0, 1, 1, 0, 0, 2]` |
| danskvand | SIRMA | 20/41 | `[0, 0, 0, 0, 0, 0]` |
| energidrikke | GLACEAU | 17/43 | `[0, 0, 0, 0, 0, 0]` |
| RTD | SKAERSOEGAARD | 38/41 | `[0, 1, 2, 3, 8, 6]` |

**Two of four have an all-zero test window.** APE is undefined against a zero
actual, so those brands cannot be scored at all — the SRQ4 metric would be a
divide-by-zero, not a hard number. Even the two that are non-zero sit at 1-8 units
where a single unit swings APE by 100%.

The medians are not much better: energidrikke's EASIS has test actuals
`[5, 0, 1, 0, 0, 12]`, danskvand's KIRVI decays `[811, ..., 19, 4]`.

**Revised recommendation: stratify on *scorable* brands, not on raw volume rank.**
Filter eligibility to brands whose **test window is entirely non-zero** (or at
minimum has no zeros), then take highest / median / lowest *of that filtered list*.
This keeps Brian's range-coverage intent — which is right and worth keeping — while
guaranteeing every selected cell yields a defined APE.

Report the filter honestly: the experiment measures forecast quality on brands with
continuous recent sales, which is the population a demand forecast is actually for.
Intermittent/zero-inflated series are a different forecasting problem (and a real
limitation to state).

**Do not lock the selection until this filter is implemented and its output
eyeballed.**

## F23 — SHAP regenerated: intersection CONFIRMED safe, and a stale citation caught

Root cause of the staleness found: **`shap` was absent from `requirements.txt`** and
not installed. The script could not run in a clean environment -- same class as the
`optuna`/`joblib` gaps. Added as `shap==0.52.0`.

Re-ran `srq1_shap.py` 2026-08-20 (local compute, no API cost). `peak_month` now
present, `holiday_month` gone -- the artifact is current.

| Feature | Old (2026-07-10) | New |
|---------|------------------|-----|
| CSD `promo_intensity` | 0.100 (7th) | **0.041 (11th)** |
| energidrikke `promo_intensity` | outside top 8 | **0.051 (10th)** |
| CSD `weighted_distribution` | **1.146 (2nd)** | **absent** |

**Promo halved** -- dropping it for the 33-column intersection costs even less than
the stale file implied. F16's provisional verdict is now **confirmed**.

**More consequential: `weighted_distribution` was the #2 feature and no longer
exists** (the 2026-08-18/19 weighted_dist drop). Any prose citing it as a leading
predictor is wrong. This is exactly the failure mode `check_chapter_facts.py`
exists for, and the SHAP artifact was invisible to it.

Current structure is **near-purely autoregressive** and near-identical across all
four categories: `lag_1` 2.06-3.84, everything else below 0.45. That similarity is
itself a mild prior in favour of pooling.

## F24 — Cross-category checks pass; nothing blocks pooling

Both pre-run checks from F21, computed on the 33 shared columns.

**(1) No sign inversions.** Every feature correlates with `log_sales_units` in the
same direction in all four categories -- the `INVERTS` column is empty throughout.
Distribution features are the strongest and are strikingly stable:

| Feature | CSD | danskvand | energidrikke | RTD |
|---------|-----|-----------|--------------|-----|
| `numeric_distribution` | 0.683 | 0.730 | 0.706 | 0.802 |
| `weighted_distribution_reach` | 0.698 | 0.755 | 0.688 | 0.767 |
| `weighted_dist` | 0.674 | 0.670 | 0.709 | 0.663 |
| `lag_1` | 0.445 | 0.516 | 0.493 | 0.458 |

Spreads of 0.04-0.12 with consistent sign. **This is a genuine argument *for*
pooling** -- the categories share structure, so a pooled model has something real to
learn across them.

Worth noting for the write-up: distribution correlates with sales *more strongly
than lag_1* in every category, yet SHAP ranks `lag_1` far above everything (F23).
Correlation is marginal, SHAP is conditional -- once lags are in the model,
distribution adds little. Not a contradiction, but a reviewer may ask.

**(2) Scale is comparable on the log target.**

| Category | raw median | log mean | log sd | log range |
|----------|-----------|----------|--------|-----------|
| CSD | 1,602 | 6.89 | 4.31 | 0.00-15.93 |
| danskvand | 1,952 | 7.34 | 4.28 | 0.00-15.16 |
| energidrikke | 2,723 | 6.87 | 4.78 | 0.00-15.09 |
| RTD | 303 | 5.66 | 3.72 | 0.00-14.65 |

Means within 1.7 log units, sds within 1.1, near-identical ranges. **The log
transform does the job** -- no category will dominate the pooled loss. RTD sits
lowest and should be watched in the per-category residual breakdown (check 3, which
runs after the pooled model exists).

Confirmed rather than assumed, as F21 required.

## F25 — Stratified selection IMPLEMENTED and verified

`--brand-strategy {volume,stratified}` added to `srq4_experiment.py`
(`_scorable_brands`, `_stratified_brands`). `--list-brands` now marks scorable
brands with `*` and prints the stratified pick per category.

**Scorable counts** (fully non-zero test window): CSD 76/95, danskvand 21/29,
energidrikke 27/44, RTD 44/62. So 40% of nominally-eligible brands would have
produced undefined APE cells.

**Selected 12 pairs, all verified zero-free:**

| Category | highest | median | lowest |
|----------|---------|--------|--------|
| CSD | HARBOE (237M) | NIKOLINE (301k) | VOELKEL (460) |
| danskvand | HARBOE (73.6M) | PERRIER (224k) | THY (15.6k) |
| energidrikke | RED BULL (95.5M) | STATE VITAMIN (954k) | MANA ENERGY (5.8k) |
| RTD | BREEZER (37.8M) | FUNKIN (76.7k) | AERIS (439) |

Volume spans **237,169,352 down to 439 units** -- five orders of magnitude, which
is real range coverage rather than the top of the distribution only. Minimum test
actual across all 12 is 1.0 (MANA ENERGY), so every cell yields a defined APE.

**Cost** (`--dry-run`, measured per-run rates): 12 brands x 5 repeats x 3 scenarios
= 180 runs, **$41.85**. Within the $50 ceiling but tight; 3 repeats is ~$25.
`A_plain` dominates at $25.46 of the total -- it is the most expensive scenario per
run despite having no tools, because reasoning tokens bill at the output rate.

## F26 — Why `weighted_dist` was dropped (answering Brian's question)

Recorded in `user-docs/handovers/2026-08-19_preprocessing-pipeline-handover-enrico.md`
section 2.5, commit `f4779a7`:

> **Not** because it leaks -- it was tested and cleared (structural and nearly
> static, corr(t, t-1) = 0.976). Dropped because it does not improve accuracy:
> worse in **3 of 4** categories. The column stays in the matrix for EDA.

So it was an **empirical accuracy decision, not a leakage fix** -- a distinction
worth preserving in the write-up, since "dropped for leakage" and "dropped because
it did not help" are very different claims about the modelling process.

This explains the F23 SHAP shift: the old artifact ranked `weighted_distribution`
#2 at 1.146 because the model still *had* it. It is absent now because it is no
longer an input. The column remains in the feature matrix, which is why F24's
correlation analysis can still measure it (0.66-0.71 with `log_sales_units`) -- a
strong *marginal* correlate that nonetheless did not improve out-of-sample
accuracy once lags were present.

## F27 — E2B credentials: no substitute exists (answering Brian's question)

Brian asked whether an own OpenAI key could stand in if Manifold cannot supply
`E2B_API_KEY` and `PROMETHEUS_TEMPLATE_ID`.

**No -- they are different services.** OpenAI supplies the model; E2B supplies the
sandbox the engine executes generated code in. `code_executor.py` calls the E2B SDK
directly with its own key. An OpenAI key cannot authenticate to E2B any more than
it could to Azure.

`PROMETHEUS_TEMPLATE_ID` is a *specific pre-built sandbox image* carrying the ODBC
driver and libraries Prometheus's generated code expects. Even with a personal E2B
account, a default sandbox would lack them and warehouse queries would fail inside
the sandbox rather than at connection time.

**Impact if unavailable, per scenario:**

| Scenario | Needs E2B? | Fallback |
|----------|-----------|----------|
| `D_prometheus` | **yes** -- code-as-action *is* sandbox execution | none; D cannot run |
| `E_prometheus_model` | **no** -- `forecast_demand` runs in-process | runs without E2B, provided the agent routes to the tool |

**This is a real risk to the thesis contribution and should be raised with Enrico
early**, because losing D loses the D->E comparison, which is the reason for
integrating Prometheus at all. E alone would show the tooled engine works but not
what the tool *adds*.

Partial mitigations, in preference order:

1. **Enrico supplies both.** Cleanest; his account already carries the E2B billing.
2. **Own E2B account + Manifold's template id.** The template is the harder half;
   a personal key with the right template may suffice.
3. **Report `E_prometheus_model` only**, and lean on `B->C` for the tool effect,
   stating explicitly that the production-engine replication covers the tooled arm
   only. Weaker, but not worthless.

## F28 — High SHAP + worse test accuracy is not a contradiction (answering Brian)

Brian: *"if it is an accuracy decision, why did it have such high feature
importance then? Is that not contradictory?"* Good challenge -- and the numbers say
the answer is **not** the easy one (redundancy with lags).

Measured on CSD (n=4,275 rows with all three present):

| Quantity | Value |
|----------|-------|
| corr(`weighted_dist`, `log_sales_units`) | 0.673 |
| corr(`lag_1`, `log_sales_units`) | 0.445 |
| corr(`weighted_dist`, `lag_1`) | 0.437 |
| **partial** corr(`weighted_dist`, target \| `lag_1`) | **0.594** |

The partial correlation barely falls below the raw one, so `weighted_dist` carries
information `lag_1` does not. **It is not redundant.** Yet removing it improved
test accuracy in 3 of 4 categories.

### The resolution: the two metrics measure different things

- **SHAP** measures how much the fitted model *used* a feature, on data it was fit
  around. Give a model a strong correlate and it will lean on it. High SHAP means
  "relied upon", not "helped generalize."
- **Test WMAPE** measures whether that reliance paid off on unseen months.

A feature can rank high on the first and *negative* on the second when its
relationship is stable in-sample but shifts out-of-sample.

That is the likely mechanism here. `weighted_dist` is nearly static --
corr(t, t-1) = 0.976, per the handover. It is a slow-moving structural property,
close to a brand-identity fingerprint. A tree can use it to identify *which brand
it is looking at* and recall that brand's typical level. This works well until
distribution shifts in the test window, at which point the memorized level is
wrong.

**So the drop is evidence-consistent, not contradictory.** Had `weighted_dist`
been merely redundant with the lags, removing it would have been roughly neutral.
That removal actively *helped* indicates it was contributing harm -- the signature
of a feature the model over-relies on.

### Write-up value

This is a genuine methodological point worth a paragraph: **feature importance is
not feature selection.** The thesis has a concrete, measured instance -- a feature
ranked #2 by SHAP whose removal improved accuracy in 3 of 4 categories -- which is
more persuasive than citing the principle abstractly. It also justifies why model
selection here was driven by held-out error rather than importance ranking.

## F29 — E2B is LESS of a blocker than F27 said (correcting F27)

Two code facts, both read 2026-08-20, materially soften F27.

**1. `PROMETHEUS_TEMPLATE_ID` is optional.** In
`data_types.py::extract_all_env_vars`, `template_id` initialises to `None` and is
only set if the key is present. `code_executor.py:121-124` then calls:

```python
code_interpreter = await AsyncSandbox.create(
    template, envs={...}, timeout=600)
```

`AsyncSandbox.create(None, ...)` is legal -- it yields E2B's **default base
sandbox**. Omitting the template does not raise; it changes which image runs.

**This is very likely Enrico's forgotten bypass.** He recalls hitting the same
problem and working around it. Dropping the template key is the obvious
workaround and requires remembering nothing. Worth telling him -- it may jog the
memory.

**2. An E2B key is self-serve.** E2B is an ordinary SaaS vendor (e2b.dev), free
tier available, nothing NDA-covered. Enrico's key is a convenience, not a
dependency.

### Revised risk

| Piece | F27 said | Actually |
|-------|----------|----------|
| `E2B_API_KEY` | blocker if Manifold cannot supply | **self-serve** |
| `PROMETHEUS_TEMPLATE_ID` | "the harder half" | **optional; falls back to default sandbox** |

**`D_prometheus` is not blocked.** The residual risk is narrower: the default
sandbox likely lacks the ODBC driver the custom template preinstalls, so warehouse
queries would fail *inside* execution. Mitigations: run D against a local snapshot
instead, or rebuild the template from the engine's Docker config
(a `Dockerfile` exists at the engine root -- unverified whether it is the sandbox
image or the service image).

F27's option 3 (report E only) drops from "likely fallback" to "last resort."

## F30 — Budget ceiling raised; run A last

Brian, 2026-08-20: Enrico has **up to 2,000 DKK** (~$290) available, well above the
earlier $50 self-imposed ceiling, and considers it worth spending if it improves
the thesis.

The full stratified design at 5 repeats is **$41.85** -- now comfortable rather
than tight.

**Brian's sequencing, adopted:** run `B_data` and `C_model` (plus D/E once
credentialled) first to shake out the harness, and re-run `A_plain` **last**, once
the design is locked. `A_plain` is $25.46 of the $41.85 -- 61% of the total despite
using no tools, because reasoning tokens bill at the output rate. Spending it on a
configuration that later changes is the single most wasteful failure mode
available, and this ordering eliminates it.

`--scenarios B_data,C_model` and `--brand-strategy stratified` already express this;
no new code needed.

## F31 — The sandbox template ships WITH the engine; nothing needs porting

F29 speculated about rebuilding the template from Docker config. It is better than
that: **the engine ships its own E2B template build system**, and the Prometheus
recipe is in it.

- `data_agents/sandboxes/build_template.py` -- E2B `AsyncTemplate` builder
- `data_agents/sandboxes/templates/prometheus.yaml` -- **the exact recipe**
- `data_agents/sandboxes/README.md` -- usage

`prometheus.yaml` in full: base image `e2bdev/code-interpreter:latest`, 4096 MB,
1 CPU, then

1. `unixodbc`, `unixodbc-dev`, `odbcinst`, Microsoft's apt key, and **`msodbcsql18`**
   -- the ODBC driver F29 worried about
2. `statsmodels prophet lightgbm xgboost catboost shap optuna polars`
3. `pandas>=2.0.0`
4. `dask[complete]>=2023.4.0 pyarrow`
5. `pyodbc sqlalchemy`

Build with:

```bash
cd graph-engine/data_agents/sandboxes
python build_template.py --config templates/prometheus.yaml
```

The alias it registers (`template_name: prometheus`) becomes the value for
`PROMETHEUS_TEMPLATE_ID`. **So the "missing" template id is not a secret to obtain
from Enrico -- it is a build artifact of a recipe already in hand.** Building it
against Brian's own E2B account produces a functionally identical sandbox.

### Answering "couldn't we port our warehouse script onto it?"

Brian asked whether the repo's existing warehouse-access code could be ported into
the sandbox. **Not needed, and it would be the wrong shape.** The sandbox does not
run a fixed script -- it runs whatever code the LLM writes at inference time
(`code_executor.execute_code`). What it needs is the *environment* (ODBC driver +
`pyodbc`/`sqlalchemy`), which `prometheus.yaml` installs, plus credentials, which
the engine already injects via `extract_all_env_vars` -> `swap_credentials_for_tokens`.

Porting a fixed query script would also **defeat `D_prometheus`'s purpose**: D is
the code-as-action scenario. Its entire measurement is whether the LLM can write
working forecasting code itself. Handing it a prepared script would convert D into
a third tool-using scenario and destroy the D->E contrast.

### Revised blocker status -- now clear

| Piece | Status |
|-------|--------|
| `E2B_API_KEY` | **HELD** -- Brian's own key, `thesis_manifold_e2b_sandbox` in `.env`, $5 loaded |
| `PROMETHEUS_TEMPLATE_ID` | **buildable from `prometheus.yaml`**; no longer needs Enrico |
| RU warehouse credentials | **HELD** -- all four present in `.env` |

Nothing external is outstanding for `D_prometheus`. Remaining unknowns are
operational (does the build succeed, does the token swap work with these
credentials), not access-related.

## F32 — E2B cost discipline before scaling

Brian loaded **$5** and asked to measure per-run cost before scaling.

E2B bills **sandbox runtime**, not tokens -- a separate axis from the OpenAI spend
already tracked in `srq4_experiment.py`. The existing cost logging captures LLM
tokens only, so **E2B cost is currently invisible to the harness.**

Two properties from the code that bear on spend:

- `AsyncSandbox.create(..., timeout=600)` -- 10-minute sandbox lifetime per
  creation.
- Sandboxes are **reused** across calls within a run via
  `ctx.deps.state["code_interpreter_id"]` (`code_executor.py:99-118`), so cost
  scales with distinct sandbox creations, not with tool calls.

`prometheus.yaml` requests 4096 MB / 1 CPU, above the default -- so per-second cost
is higher than a stock sandbox.

**Before any scaled run:** execute exactly one `D_prometheus` call, then read actual
usage from the E2B dashboard and record dollars-per-run here. Do not extrapolate
from the OpenAI figures -- they measure a different resource. The $5 is enough for
a meaningful pilot but would not cover 60 D-runs at an unmeasured rate.

Also worth noting: the template build itself consumes E2B resources (it runs
`apt-get` and five `pip install` layers). Build once, reuse the alias.

## F33 — CORRECTION to F31: there is no repo warehouse code to port

F31 answered "couldn't we port our warehouse script?" on design grounds (a fixed
script would defeat `D_prometheus`'s code-as-action premise). That reasoning stands,
but it implied such a script exists. **It does not.**

A repo-wide search for `pyodbc|sqlalchemy|azure.*sql|RU_SERVER|ODBC` returned only
`.venv` library noise -- zero first-party hits. The four `RU_*` credentials sit in
`.env` but **no code in the repository consumes them.** Nielsen data arrives as
parquet by some route outside this repo.

Corrected picture:

| | Reality |
|---|---|
| Repo warehouse-access code | **none exists** |
| `RU_*` credentials | present in `.env`, unused by any repo code |
| Sandbox warehouse access | **entirely engine-side** -- `prometheus.yaml` installs `msodbcsql18` + `pyodbc`/`sqlalchemy`, the engine injects credentials via `swap_credentials_for_tokens`, the LLM writes the query at inference time |

This *simplifies* D rather than complicating it: Brian contributes credentials and
nothing else. There is no integration surface to build on the thesis side.

## F34 — `utility_scripts/scripts/` still shadows canonical scripts

Noticed while confirming F33. `utility_scripts/scripts/` contains `srq1_shap.py`,
`srq1_calibration.py`, `srq1_baselines_stat.py`, `generate_figures.py` and
`srq2_agent.py` -- duplicates of files that also live under `03_thesis_modelling/`.

P0035 F6 already established `03_thesis_modelling/` as the canonical tree and
flagged these as stale shadows; they were not removed.

**Concrete risk, now realised in this session:** the SHAP regeneration (F23) ran
`03_thesis_modelling/model_training/srq1/srq1_shap.py`. Running the
`utility_scripts/` copy instead would execute possibly-different code and overwrite
the same output artifact, silently. The same hazard applies to `generate_figures.py`,
which is already slated for the `fig4_ram_budget` fix (F5).

Cleanup, not a blocker -- but it should be resolved before the writing phase, since
"which script produced this figure?" becomes unanswerable otherwise.

## F35 — CORRECTION to F33: warehouse code DOES exist (Brian was right)

F33 claimed no repo warehouse-access code exists. **Wrong** — my search excluded the
path it lives in. Brian corrected it:
`02_thesis_data/_00_raw/nielsen/scripts/nielsen_connector.py`.

It is a real, complete Microsoft Fabric connector: `ClientSecretCredential`
(Entra ID service principal) -> token packed UTF-16-LE into a `struct` ->
`pyodbc.connect(..., attrs_before={1256: token_struct})` against
`ODBC Driver 18 for SQL Server`. Siblings `save_all_datasets.py` and
`audit_datasets.py` use it. This is how the parquet snapshots are produced.

**This is materially useful, for two reasons F33 missed:**

1. **It proves the RU credentials are the right kind.** F19 flagged uncertainty
   about whether they would survive the engine's Azure token swap. `nielsen_connector`
   performs the *same* service-principal flow (`ClientSecretCredential` ->
   `database.windows.net/.default`) that `security/token_swap.py` does. If the
   connector works today, the swap should too. **Run
   `nielsen_connector.test_connection()` as a free pre-flight** before spending on D.
2. **It documents the schema** — `csd_clean_facts_v`, `csd_clean_dim_market_v`,
   `csd_clean_dim_period_v`, `csd_clean_dim_product_v`. If `D_prometheus` needs a
   local-snapshot fallback (F18 option 2), these view names and the loader are the
   starting point.

Note its stale docstring: `from thesis.data.nielsen.scripts...` is a pre-P0028
import path, and `parents[4]` is the fixed-index pattern P0035 replaced. It resolves
correctly by luck of current depth — worth fixing when next touched.

**F31's design answer still stands**: do not port a fixed query script *into the
sandbox*, because `D_prometheus` must write its own code. The connector's value is
credential validation and schema reference, not transplantation.

## F36 — Shadow scripts verified stale and retired

Per Brian's instruction: verify before archiving, port anything unique, then retire.

| File | Counterpart | Verdict |
|------|-------------|---------|
| `srq1_shap.py` | canonical 119 lines vs 67 | stale |
| `srq1_calibration.py` | canonical 124 vs 72 | stale |
| `srq1_baselines_stat.py` | canonical 129 vs 112 | stale |
| `generate_figures.py` | `04_thesis_results/` | **byte-identical** |
| `srq2_agent.py` | none | already archived elsewhere |

**Nothing needed porting.** Every line unique to the utility copies is a superseded
pattern, not unique work: `parents[2]` root lookup (P0035 replaced it),
`holiday_month` (renamed `peak_month`), `weighted_distribution` (dropped in
`f4779a7`), `{slug}_feature_matrix.parquet` (pre-H=3 filename), and the
`np.log`/`np.expm1` mismatch (fixed in `5f2e9b7`). Running them would have produced
results against dropped features and superseded matrices, or crashed on the path.

Moved to `utility_scripts/scripts/.archive/shadow_scripts_2026-08/` with a README
recording the per-file verification. `README.md:128` pointed at the utility copy of
`generate_figures.py` and was repointed to `04_thesis_results/`.

`generate_figures.py` was archived *despite* being identical, because the canonical
copy still needs the `fig4_ram_budget` fix (F5) — leaving two copies invites fixing
one and citing the other.

## F37 — E2B cost discipline before scaling (documented per Brian's request)

E2B bills **sandbox runtime**, a different resource from the OpenAI tokens
`srq4_experiment.py` already logs. **E2B spend is invisible to the harness.** Do not
extrapolate from OpenAI figures.

Facts from the engine that govern spend:

- `AsyncSandbox.create(..., timeout=600)` — 10-minute lifetime per creation
  (`code_executor.py:121`).
- Sandboxes are **reused** within a run via
  `ctx.deps.state["code_interpreter_id"]` (`code_executor.py:99-118`), so cost
  tracks distinct *creations*, not tool calls.
- `prometheus.yaml` requests **4096 MB / 1 CPU**, above default — higher per-second
  rate than a stock sandbox.
- The **template build itself consumes resources** (`apt-get` + five `pip install`
  layers). Build once, reuse the alias; `skip_cache: true` in the yaml forces a
  full rebuild every time, so flip it to `false` after the first successful build.

### Required procedure before any scaled D/E run

1. Build the template **once** from `prometheus.yaml`.
2. Run **exactly one** `D_prometheus` call.
3. Read actual usage from the E2B dashboard; record dollars-per-run in this file.
4. Only then decide the repeat count.

Budget held: **$5** on Brian's own key (`thesis_manifold_e2b_sandbox`), loaded
2026-08-20. Enough for a pilot; would not survive 60 unmeasured D-runs.

**Pre-flight that costs nothing:** run `nielsen_connector.test_connection()` (F35)
to confirm the RU credentials still authenticate before spending any E2B time on a
run that would fail at the same step.

## F38 — MEASURED: E2B cost is negligible; the template build IS required

Ran `measure_e2b_cost.py` against the **default** sandbox (no template, no build
spend), 2026-08-20.

### Timing

| Phase | Seconds |
|-------|---------|
| sandbox create | 1.68 |
| code execute | 1.22 (0.58 in-sandbox) |
| kill | 0.19 |
| **billable wall clock** | **3.08** |

At E2B's small-sandbox rate (order $0.00003/s), that is **~$0.0001 per lifecycle**.
Even assuming a sandbox is held for the full `timeout=600` window across a
multi-turn D run, 60 runs lands **under $1**. Brian's $5 is ample.

**E2B is not a budget constraint.** The OpenAI spend ($41.85 for the full
stratified design) remains the only cost that matters. F32/F37's caution was
warranted as a discipline but the answer is: negligible.

Planning figure: use the **600s timeout**, not the 3.08s probe. A real D run holds
the sandbox open while the LLM reasons between tool calls; the probe measured a
fast synchronous workload.

### The decisive finding: the base image is bare

```
pandas 2.2.3
MISSING pyodbc
MISSING sqlalchemy
MISSING statsmodels
MISSING xgboost
MISSING prophet
```

**All five absent.** This settles F29's open question -- the `prometheus` template
is **required**, not optional-in-practice.

The reason matters more than warehouse access. `D_prometheus` is the
*code-as-action* scenario: its entire measurement is whether the LLM can write
working forecasting code. Without `statsmodels` or `prophet` it cannot fit a real
forecasting model at all, and would be reduced to numpy arithmetic.

**Running D on the default sandbox would silently handicap it**, inflating the
D->E gap in the thesis's own favour. That is the worst class of confound available
here -- one that flatters the contribution. The template must be built before any
D run is scored.

Cost of learning this: a few hundredths of a cent, versus a full template build.
The cheap-first sequencing paid off.

### Next actions

1. Build the template: `python build_template.py --config templates/prometheus.yaml`
   from `graph-engine/data_agents/sandboxes/`. Requires `E2B_API_KEY` in that
   directory's environment.
2. Set `skip_cache: false` in `prometheus.yaml` **after** the first successful
   build, so retries do not pay full rebuild cost.
3. Re-run `measure_e2b_cost.py --template prometheus` to confirm the five packages
   are present and to get the real per-run figure for the 4 GB box.

### Pin caveat still open

`requirements.txt` now installs `e2b-code-interpreter==2.9.1`; the engine's
`pyproject.toml` declares `2.0.0`. The probe worked at 2.9.1, but the probe only
uses `AsyncSandbox.create/run_code/kill`. **The engine exercises more of the API
and may require 2.0.0** -- verify before the D/E runs rather than assuming.

## F39 — Template build: the exact command, and why it failed the first time

`build_template.py` calls bare `load_dotenv()`, which reads `.env` from the
**current working directory**. The engine ships only `.env.example`, so the first
attempt raised `e2b.exceptions.AuthenticationException: API key is required`.

**Working sequence** (PowerShell), verified shape 2026-08-20 -- reads the key
straight from the thesis `.env` without printing it or writing it anywhere new:

```powershell
cd Z:\_dev-ssd\prometheus\prometheus-graph-engine\graph-engine\data_agents\sandboxes
$env:E2B_API_KEY = (Select-String -Path Z:\_dev-ssd\thesis-manifold\.env -Pattern '^thesis_manifold_e2b_sandbox=(.+)$').Matches.Groups[1].Value
python build_template.py --config templates/prometheus.yaml
```

Confirm without exposing the value:

```powershell
$env:E2B_API_KEY.Length    # expect 44
```

The variable lasts for that shell session only.

**Expect several minutes.** `skip_cache: true`, 4096 MB, 1 CPU, and the pip layer
includes `prophet`, which compiles Stan. Do not interrupt.

**After the first successful build, set `skip_cache: false`** in `prometheus.yaml`
so retries do not pay a full rebuild.

Then verify:

```powershell
cd Z:\_dev-ssd\thesis-manifold
.venv\Scripts\python.exe 03_thesis_modelling\scenario_setup\measure_e2b_cost.py --template prometheus
```

If any of the five packages still report MISSING, a build layer silently failed --
catch that **before** scoring a D run, per F38.

**Status 2026-08-20: not yet run.** Brian will execute tomorrow.

### The template alias is per-account, not a shared secret

`template_name: prometheus` registers under **Brian's own E2B account**. So
`PROMETHEUS_TEMPLATE_ID=prometheus` resolves for Brian and not for Enrico, who must
build from the same yaml against his own key. Worth stating in any handover: this
was never a credential to obtain from Manifold.

### `.env` in the engine tree is acceptable

Brian, 2026-08-20: the engine arrived as a **zip**, not a clone. Nothing is pushed
back, so writing a `.env` there carries no leak risk to Manifold's repository. It
would only matter if code is returned to them, at which point the file is deleted.
The shell-variable approach above is still marginally cleaner, but either is fine.

## F40 — The thesis venv's `e2b` is fine for building, a problem for running

The build resolved `e2b` from `Z:\_dev-ssd\thesis-manifold\.venv` because Brian's
venv stayed active across the `cd`. **Harmless for task 3b** -- template building
touches only the E2B template API, which 2.9.1 serves.

**It becomes a real problem at task 4.** Running the engine needs the engine's own
dependency set, and the versions do not match:

| Package | engine `pyproject.toml` | thesis `.venv` |
|---------|------------------------|----------------|
| `e2b_code_interpreter` | **2.0.0** | **2.9.1** |
| `pydantic-ai` | 1.73.0 | not installed |
| `langgraph` | >=0.2.74 | not installed |

The engine's shipped `.venv` is unusable -- it is a **Linux venv whose interpreter
path points at `/home/niks/miniconda3/bin/python3`**, i.e. built on the developer's
machine and not portable to Brian's Windows box.

**Task 4 needs a decision, and it should be made deliberately rather than by
whichever interpreter happens to be active:**

1. **Separate environment for the engine** (`uv sync --frozen` against its
   `pyproject.toml` + `uv.lock`, both of which ship). Cleanest -- keeps the
   engine's pins away from the thesis pins, and the lockfile means exact
   reproduction. Preferred.
2. **Install engine deps into the thesis venv.** Would force
   `e2b-code-interpreter` down to 2.0.0, which the A-C harness also imports.
   Risks breaking `B_data` to fix D/E. Not recommended.

Note the engine targets **python-version 3.11** in `langgraph.json` while Brian's
environment is 3.14.2 -- another argument for option 1.

## F41 — E2B billing is runtime-only; an idle template costs nothing

Brian asked whether a built template bills continuously even with no conversation.
**No.** Two separate meters:

| Thing | Billed |
|-------|--------|
| Template (the built image) | storage only -- negligible or free |
| Sandbox (a running instance) | **per second, only while alive** |

No conversation means no sandbox means no runtime charge. `skip_cache` affects only
what a *rebuild* costs, not standing cost.

What does bill, and is worth watching, is a sandbox left open: the engine creates
with `timeout=600`, so an abandoned sandbox bills for up to 10 minutes after its
last use. `measure_e2b_cost.py` explicitly kills its sandbox in a `finally` block
for that reason. At ~$0.0001 per 3-second lifecycle (F38) even the pathological
case is cents.

## F42 — Template built and verified; the first build died with its log poller

Built 2026-08-21. **Template alias `prometheus` resolves**, so nothing in the
engine's config needs rewiring — `prometheus.yaml`'s alias is what
`AsyncSandbox.create` accepts. Generated id, recorded for reference:
`fxe7gzkqjupdhbx4uvpr`.

Verified by probe (`measure_e2b_cost.py --template prometheus`):

```
HAVE pyodbc / sqlalchemy / statsmodels / xgboost / prophet
```

All five present, against **all five missing** on the base image (F38). The
handicap risk that made this build mandatory is closed: `D_prometheus` can now fit
a real forecasting model rather than failing for want of a library.

### The first attempt failed client-side, not server-side

Attempt 1 registered the template, uploaded, began uncompressing 33 layers off a
1.1 GB base — then raised `asyncio.exceptions.CancelledError` inside
`pyqwest/middleware/retry/_async.py`, surfaced as `KeyboardInterrupt`.

**The build did not survive the disconnect.** Probing the generated id returned:

```
404: tag 'default' does not exist for template 'fxe7gzkqjupdhbx4uvpr'
```

i.e. the template *record* existed with **no build tagged `default`**. Worth
recording because the intuition "server-side builds continue regardless" is what
one would assume, and it is wrong here — checking cost a fraction of a cent and
avoided paying for a duplicate build.

Attempt 2 succeeded, run from the **thesis venv** rather than system python
(3.14.2, `pythoncore-3.14-64`, every frame of both tracebacks). The interpreter
change is the only difference, so python 3.14 + `pyqwest`'s async retry transport
is the probable cause, though a transient network fault is not excluded. If a
future rebuild is needed, use the venv.

### The per-run cost figure from F38 is superseded

| | Base image (F38) | `prometheus` template |
|---|---|---|
| Create | 1.68s | 2.88s |
| Execute | ~1.4s | **33.22s** |
| Lifecycle | 3.08s | **36.31s** |

**~12x, on an identical workload.** This is import cost, not compute —
`prophet`/`statsmodels` pull in `cmdstanpy` and `scipy` on first import. It is paid
**once per sandbox**, and the engine reuses one sandbox per conversation
(`ctx.deps.state["code_interpreter_id"]`, F37), so a D/E run pays it once, not per
tool call.

Budget impact is still negligible — 60 D-runs at ~36s is ~36 sandbox-minutes,
under a dollar of the $5. But **the "~$0.0001 per run" figure quoted in F41 and the
Enrico handover was measured on the bare image and no longer holds.** The honest
figure is roughly an order of magnitude higher and still immaterial next to the
~$42 OpenAI side.

### The real risk this introduces: a cold-start timeout confound

A 28-second first import is long enough to collide with a **per-execution**
timeout. `AsyncSandbox.create(..., timeout=600)` bounds the sandbox *lifetime*,
which is not the same thing as a limit on a single `run_code` call.

If the engine's executor caps individual executions below ~30s, `D_prometheus`'s
first tool call fails on cold start and the trace reads as *"the LLM wrote code
that did not work"* — when it is really a startup timeout. That would depress D and
**inflate D -> E in our favour**: the same class of confound the template build was
undertaken to remove (F38), re-entering by a different door.

**Check `code_executor.py` for a per-call timeout during task 4, before any scored
D run.** If one exists and is tight, either raise it or warm the sandbox with a
throwaway import before the measured turn — and say which was done in the
methodology.

## F43 — Engine environment: separate venv, python 3.13, both hard pins satisfied

DEC-ENGINE-ENV (Brian, 2026-08-21): the engine gets **its own environment**, not a
downgraded thesis venv. `e2b_code_interpreter==2.0.0` is a hard `==` in the engine's
`pyproject.toml`, and `B_data` imports the same package at 2.9.1 — so satisfying the
engine inside the thesis venv would mean breaking a *working* scenario to enable an
unbuilt one. Two environments is the cheaper trade, and it keeps A–C reproducible
exactly as they are today, which is the premise of the two-tier reproducibility
argument.

Built with `uv sync --frozen --python 3.13` **in place** at
`graph-engine/.venv` (Brian's call). Nothing recoverable was lost: the shipped
`.venv` was a Linux venv (`home = /home/niks/miniconda3/bin`) unusable on Windows,
and it is fully reconstructible from the shipped `uv.lock`.

Verified after sync:

| | Value |
|---|---|
| python | **3.13.13** |
| `e2b_code_interpreter` | **2.0.0** ✓ pinned |
| `pydantic_ai` | **1.73.0** ✓ pinned |
| `langgraph` | 1.0.6 |

### Two corrections to F40

1. **The engine requires `>=3.12`, not 3.11.** F40 carried 3.11 from the archived
   blueprint. It is a floor, not a pin — 3.14.2 also satisfies it, so the python
   version was never itself the blocker. The `==` pins are.
2. **3.13 was chosen deliberately over 3.14**, for two reasons: the shipped Linux
   `.venv` records `version_info = 3.13.2`, so 3.13 is the version the engine is
   known to run on at Manifold; and python 3.14 + `pyqwest`'s async retry transport
   is the stack that killed the template build's log poller (F42). Matching
   Enrico's minor version removes a variable rather than adding one.

3.13.13 was already installed locally — no download needed.

## F44 — Pooling costs ONE feature, not eighteen: F8's framing was too pessimistic

Measured 2026-08-21 against the four `*_feature_matrix_h3.parquet` schemas.

F8 reasoned about pooling from the **feature matrices** (33 of 51 columns common).
But the models never consume the matrix — `srq1_benchmark_tuned.py::FEATURES` is
**13 columns**, all lag / rolling / calendar plus `promo_intensity`.

| Category | Model features present | Missing |
|----------|------------------------|---------|
| CSD | 13/13 | -- |
| energidrikke | 13/13 | -- |
| danskvand | 12/13 | `promo_intensity` |
| RTD | 12/13 | `promo_intensity` |

**Intersection: 12 of 13. The sole casualty is `promo_intensity`** — ranked
**11th of 13** by regenerated SHAP in CSD (0.041), and absent by construction in
danskvand and RTD (Nielsen reports no promotion there; the pipeline omits rather
than zero-fills, per DEC-DISCOVER-COLUMNS).

### Three consequences

1. **The comparison is nearly free of handicap.** A pooled model gives up one
   low-importance feature, not a whole promo family. Any accuracy gap is therefore
   attributable to pooling itself rather than to a crippled feature set — which is
   what makes the comparison worth running at all.
2. **The construct-validity worry in the design-rationale note dissolves.** That
   note argued against union-with-NaN because a tree could split on *is-NaN* and
   silently rebuild a category indicator. With `promo_intensity` simply dropped,
   there are no NaNs to split on. The argument stays valid as written — it just no
   longer describes a live risk.
3. **`05_thesis_writing/notes/prometheus-scenarios-design-rationale.md` overstates
   the cost of pooling** in its "feature intersection is a finding" section, which
   is built on 33/51. The matrix figure is not wrong, but it is not the number that
   governs the model. Correct that section when the pooled run produces numbers.

`available_features()` already implements the intersection per-category, so the
pooled path needs no new column-handling logic — only `(category, brand)` as the
series key (brand names are not unique across categories) and `promo_intensity`
excluded from `FEATURES`.

## F45 — The cold-start timeout confound does not exist; checked rather than assumed

F42 flagged a risk: the `prometheus` template's ~28s first-import cost could collide
with a **per-execution** timeout (a different limit from
`AsyncSandbox.create(..., timeout=600)`, which bounds sandbox *lifetime*). If one
existed and were tight, `D_prometheus`'s first tool call would fail on cold start,
the trace would read as *"the LLM wrote code that did not work"*, and D -> E would
inflate in our favour.

**Checked. No such cap.** `code_executor.py` has exactly two timeout-relevant lines:

```
124:  AsyncSandbox.create(template, envs={...}, timeout=600)   # lifetime
129:  execution = await code_interpreter.run_code(code)        # no timeout arg
```

`run_code` is called with **no timeout argument**, so the SDK default governs:
`e2b_code_interpreter/constants.py::DEFAULT_TIMEOUT = 300` seconds — ~10x headroom
over the 28s cold start.

Closed on both fronts (no engine-side cap, generous SDK default). **No warm-up turn
is needed and none should be added** — a warm-up would be an undocumented deviation
between D/E and A/B/C for no measurement benefit.

Worth keeping in the write-up as an example of the verification discipline: the risk
was real in kind, cost one grep to rule out, and would have biased the headline
D -> E number had it held.

## F46 — Engine environment complete and verified

`uv sync --frozen --python 3.13` finished exit 0. Full dependency set resolved
(~200 packages). Verified in the engine venv:

| Package | Version | Note |
|---------|---------|------|
| python | 3.13.13 | matches Enrico's 3.13.2 |
| `e2b_code_interpreter` | **2.0.0** | hard `==` pin satisfied |
| `pydantic_ai` | **1.73.0** | hard `==` pin satisfied |
| `langgraph` | 1.0.6 | |
| `openai` | 2.30.0 | |
| `pandas` | 2.3.3 | |
| `matplotlib` | 3.10.8 | |
| `logfire` | 4.19.0 | |

A `pywin32.pth` / `ModuleNotFoundError: pywin32_bootstrap` warning appeared **during**
the install and **resolved on completion** — a partially-unpacked `pywin32` mid-sync,
not a defect. Interpreter now starts clean. Do not chase it if seen again mid-install.

The thesis venv is untouched and keeps `e2b-code-interpreter==2.9.1` for `B_data`,
which was the entire point of DEC-ENGINE-ENV (F43).

## F47 — Engine credentials: shell env vars, no file in the vendor tree

Brian asked whether there is an alternative to writing keys into the engine
directory. **There is, and it is better.** Verified rather than assumed — every
`load_dotenv()` call in the engine uses the default `override=False`:

```
config/loader.py:42                         load_dotenv(dotenv_path=... / ".env")
data_agents/tools/fetch_weather_data.py:12  load_dotenv()
data_agents/sandboxes/build_template.py:10  load_dotenv()
```

No `override=True` anywhere, so **variables already in the environment win** over
any `.env` file. Exporting them in the shell before launch is sufficient:

```powershell
$env:OPENAI_API_KEY = (Select-String -Path Z:\_dev-ssd\thesis-manifold\.env -Pattern '^OPENAI_API_KEY=(.+)$').Matches.Groups[1].Value
$env:E2B_API_KEY    = (Select-String -Path Z:\_dev-ssd\thesis-manifold\.env -Pattern '^thesis_manifold_e2b_sandbox=(.+)$').Matches.Groups[1].Value
```

Same indirection `measure_e2b_cost.py` uses, and the pattern that made the template
build work. Preferred because: one source of truth for keys; the vendor tree stays
byte-identical to the delivered zip (diffable); and no stray `git add` can catch
them. Cost: the vars live only in that shell session.

**Correction to an earlier claim in this session:** the engine does *not* read
`graph-engine/.env`. `config/loader.py:42` resolves `parent.parent.parent`, which is
`prometheus-graph-engine/` — one level ABOVE the repo dir. A file dropped in
`graph-engine/` would have been silently ignored. Shell vars sidestep the ambiguity.

## F48 — Pooled-vs-per-category: harness built, smoke test shows a real signal

`03_thesis_modelling/model_training/srq1/srq1_pooled.py`, written 2026-08-21. Closes
the SRQ1 gap in F8: the thesis names category specialization in its own headline
question and `tuned_metrics.csv` has no pooled row.

### Design: per-category scoring, not pooled-vs-pooled aggregate

A single pooled WMAPE across all four categories is dominated by CSD's volume, and
comparing it against four separate per-category numbers compares different
populations. Instead: **train one pooled model, score it separately on each
category's test rows**, against a per-category model on those SAME rows. The
evaluation population is identical on both sides; only the training rows differ.

Two further controls so exactly one variable moves:

- **Both arms use the same 12 features.** The per-category arm is RE-TRAINED here
  rather than read from `tuned_metrics.csv` — that file's models had 13 features
  (incl. `promo_intensity`), so reusing it would confound "pooling" with "one fewer
  feature".
- **Same tuning protocol** (`_fit_tuned` mirrors `srq1_benchmark_tuned.py::tune`):
  Optuna TPE, seed 42, tune on val by WMAPE, refit best on train+val.

### The (category, brand) key was necessary, not defensive

Measured at runtime: **16 brand names span more than one category** (AQUA D'OR,
EASIS, FEVER TREE, FREM, HANCOCK, HARBOE, ...). Pooling on `brand` alone would have
silently merged unrelated series. The script audits and prints this before training.

### Row counts

| | train | test |
|---|---|---|
| pooled | 4009 | 1519 |
| CSD | 1805 | 665 |
| danskvand | 464 | 174 |
| energidrikke | 748 | 308 |
| RTD | 992 | 372 |

### Smoke test (2 trials — under-tuned, indicative only)

| Category | LightGBM delta | XGBoost delta |
|----------|---------------|---------------|
| CSD | +1.9pp per-cat better | +0.8pp per-cat better |
| danskvand | **-20.9pp pooled better** | -3.2pp pooled better |
| energidrikke | -7.0pp pooled better | +0.3pp per-cat better |
| RTD | +1.1pp per-cat better | +0.8pp per-cat better |

**The pattern is coherent: pooling helps the data-poor categories and slightly hurts
the data-rich one.** danskvand has 464 training rows and gains most from borrowing;
CSD has 1805 and loses a little. That is textbook transfer behaviour, which is
evidence the harness is measuring something real rather than noise.

**Do not cite these numbers.** At 2 trials the per-category danskvand result swings
41.6% -> 22.0% between models, which is a tuning artifact. The 30-trial run (matching
`tuned_metrics.csv`) supersedes them.

## F49 — RESULT: pooling wins on data-poor categories, loses on data-rich ones

30 trials, matching `tuned_metrics.csv`. Supersedes the 2-trial smoke test in F48.
Written to `04_thesis_results/srq1/{pooled_metrics.csv, pooled_params.json,
pooled_summary.md}`.

**Sorted by training rows** (delta = pooled WMAPE - per-category WMAPE; positive
means the specialised model is more accurate):

| Category | train rows | LightGBM | XGBoost | Winner |
|----------|-----------:|---------:|--------:|--------|
| CSD | 1805 | +1.2pp | +1.3pp | per-category |
| RTD | 992 | +0.7pp | +1.5pp | per-category |
| energidrikke | 748 | -1.6pp | -1.4pp | **pooled** |
| danskvand | 464 | -2.2pp | -2.5pp | **pooled** |

### Why this is a defensible finding and not noise

**The sign flips exactly once, at the same place, for both model families.** Two
independent gradient-boosting implementations, tuned separately, agree on all four
categories and on magnitude to within ~0.8pp. An artifact of one algorithm's
inductive bias would not replicate like this.

The ordering is also mechanistically sensible: pooling trades **specialisation** for
**sample size**. Below roughly 750-1000 training rows the borrowed signal outweighs
the lost specificity; above it, the reverse. danskvand (464 rows) gains most,
CSD (1805) loses most.

### Tuning mattered — do not cite the smoke test

Per-category danskvand moved 41.6% / 22.0% (2 trials) -> 23.7% / 21.5% (30 trials).
The smoke test's dramatic -20.9pp was a tuning artifact; the true effect is roughly
a tenth that size. This is itself worth a sentence in the methodology: under-tuned
baselines inflate apparent gains, and the direction of that bias favours whatever
arm happens to tune faster.

### What to claim in the write-up

SRQ1's third leg — *"does a per-category model beat a single pooled model?"* — now
has an answer, and it is **conditional rather than binary**:

> Neither strategy dominates. Specialisation pays only where a category has enough
> history to support it; below that threshold a pooled model borrowing cross-category
> structure is more accurate. On this dataset the crossover sits between roughly 750
> and 1000 brand-month training observations.

That is a more useful result for a practitioner than either "pooled wins" or
"per-category wins", because it converts the modelling choice into a measurable
precondition. It also gives the memory-efficiency leg of SRQ1 a sharper edge: one
pooled model is ~1/4 the artifact count, and for two of four categories it is also
*more accurate* — so for those the trade-off is not a trade-off at all.

### Caveats to state

1. **Effect sizes are small** (0.7-2.5pp). Report them as directional, not decisive.
2. **No confidence intervals.** Single split, single seed. A seed sweep would firm
   this up cheaply (no API spend) and is the obvious next step if a reviewer presses.
3. **The crossover is interpolated from four points.** "Between 750 and 1000 rows" is
   the honest phrasing; a precise threshold is not supported.
4. **RTD's WMAPE is ~35% in both arms** — the pooling question is secondary to the
   fact that neither model forecasts RTD well.

## F50 — WMAPE and median MAPE disagree about who wins; F49 holds only on WMAPE

Surfaced when reading the full `pooled_summary.md` table rather than the WMAPE
console line. **This qualifies F49 and must not be omitted from the write-up.**

| Model | Category | WMAPE winner | medMAPE winner | Agree? |
|-------|----------|--------------|----------------|--------|
| LightGBM | CSD | per-cat (16.3 vs 17.5) | per-cat (37.0 vs 40.3) | yes |
| LightGBM | danskvand | pooled (21.4 vs 23.7) | pooled (37.3 vs 47.4) | yes |
| LightGBM | energidrikke | pooled (12.1 vs 13.7) | pooled (50.3 vs 57.8) | yes |
| LightGBM | RTD | per-cat (35.1 vs 35.8) | **per-cat by 11.6pp** (43.4 vs 55.0) | yes, but magnitude differs wildly |
| XGBoost | CSD | per-cat (15.3 vs 16.6) | pooled (34.8 vs 35.5) | **NO** |
| XGBoost | danskvand | pooled (18.9 vs 21.5) | pooled (32.4 vs 39.1) | yes |
| XGBoost | energidrikke | pooled (12.5 vs 13.9) | **per-cat by 11.2pp** (39.7 vs 50.9) | **NO** |

### Why, and why it is not a bug

**WMAPE is volume-weighted; median MAPE is not.** WMAPE divides summed absolute
error by summed actuals, so high-volume brands dominate it. Median MAPE gives every
brand-month equal weight, so it reflects the typical brand rather than the big ones.

The disagreement therefore says: **the pooled model tends to help large series and
hurt small ones *within* a category.** That is the same "borrow from the data-rich"
mechanism as the cross-category result in F49, operating one level down — pooling
lets a thin brand inherit the shape of a fat one, which flatters the volume-weighted
metric and can damage the per-brand typical case.

### Consequence for the claim

F49's finding is **metric-conditional**, and stating it as unconditional would
overclaim:

- On **WMAPE**, the crossover story is clean: sign flips once, both algorithms agree.
- On **median MAPE**, two of eight cells flip, and in the two largest disagreements
  (LightGBM RTD, XGBoost energidrikke) the gap is >11pp — far larger than any WMAPE
  delta in the entire table (max 2.5pp).

**Recommended framing:** report WMAPE as the headline (it is the operational metric —
the business cares about total units mis-forecast), state the median-MAPE
disagreement explicitly, and interpret it as evidence about *who* pooling helps
rather than as a contradiction. A reviewer who finds this unaided will read it as a
cherry-picked metric; stated openly it is an additional finding.

### Note on effect-size asymmetry

Every WMAPE delta is <= 2.5pp while median-MAPE deltas reach 11.6pp. This means the
pooled-vs-per-category choice is **nearly irrelevant for total-volume accuracy and
quite consequential for typical-brand accuracy.** That is arguably the more
practically useful sentence in the whole comparison, and it is invisible if only
WMAPE is reported.

### Open item

A per-brand breakdown (delta as a function of that brand's own training rows) would
test the "helps large, hurts small" explanation directly rather than inferring it
from two aggregate metrics. Cheap, no API spend, and it would convert an
interpretation into a measurement. Not run yet.

## F51 — Per-brand test of F50: XGBoost supports the mechanism, LightGBM does not

`srq1_pooled_perbrand.py`, 30 trials, 2026-08-22. Written to
`04_thesis_results/srq1/{pooled_perbrand.csv, pooled_perbrand_summary.md}`.

F50 *inferred* from a WMAPE/median-MAPE disagreement that pooling must be helping
large series and hurting small ones within a category. This tested that directly by
scoring every brand separately and relating each brand's delta to its own size.

**The script's console verdict ("SUPPORTS F50" for both models) is too generous and
should not be quoted.** Its threshold was `r > 0.1`, which passed a correlation of
+0.137 sitting on top of a completely flat tercile table. Reading the tables rather
than the summary statistic gives a split result.

### XGBoost: supports the mechanism, cleanly

Monotone on every measure.

| Tercile | median delta | pooling win-rate |
|---------|-------------:|-----------------:|
| small | -6.9pp | 38/56 (68%) |
| medium | -1.0pp | 33/56 (59%) |
| large | -0.3pp | 30/56 (54%) |

corr(delta, log volume) = **+0.252**. It also holds *within all four categories* —
the "small" column is negative in every XGBoost row of the per-category table
(-7.6 CSD, -27.9 danskvand, -7.1 energidrikke, -7.7 RTD).

### LightGBM: null result, not a weak positive

| Tercile | median delta | pooling win-rate |
|---------|-------------:|-----------------:|
| small | +2.0pp | 26/56 (46%) |
| medium | +2.9pp | 25/56 (45%) |
| large | +2.2pp | 26/56 (46%) |

Flat, not monotone. Win-rate is indistinguishable across terciles. corr(delta,
log train rows) = **-0.014** — essentially zero.

### Why the tercile table is the more trustworthy view

Medians and means diverge sharply (LightGBM small: median +2.0 vs mean -3.9), so a
handful of extreme brands is moving the averages and, with them, the correlation.
The win-rate column is the most robust statistic in the table because it is immune
to outlier magnitude — and it is flat for LightGBM and monotone for XGBoost.

### Two further problems with the simple story

1. **The medium tercile misbehaves for LightGBM**: +10.1 (CSD), +9.1 (danskvand),
   +7.5 (RTD). If size drove the benefit, medium should sit *between* small and
   large, not exceed both. It does not, in three of four categories.
2. **124 of 460 rows (27%) were unscorable** — zero actuals in the test window,
   where APE is undefined rather than large. Consistent with the ~40% figure from
   SRQ4 brand selection. All statistics here therefore describe the
   continuously-selling subset only, which must be stated.

### What this means for the write-up

**Weaken the F50 claim.** The "pooling helps small brands" mechanism is
**supported for XGBoost and unsupported for LightGBM**, so it cannot be presented
as the general explanation for the metric disagreement. Honest phrasings:

> A per-brand breakdown supports this mechanism for XGBoost (pooling wins for 68% of
> small brands against 54% of large ones, monotone across terciles) but not for
> LightGBM, where the effect is flat across the volume range. The metric
> disagreement is therefore real but its cause is not uniform across model families.

This is a less tidy result than F50 anticipated, and it is the one the data
supports. Note the contrast with F49, whose strength was precisely that both
algorithms agreed — here they do not, which is itself informative: the
*category-level* crossover replicates across model families, the *brand-level*
mechanism does not.

### Cheap follow-up if this matters

A seed sweep would establish whether LightGBM's null is stable or an artifact of one
seed. No API spend. Worth doing only if the brand-level mechanism ends up load-bearing
in the prose; the category-level result in F49 does not depend on it.

## F52 — Seasonal-naive beats the tuned models on RTD; the ML advantage is not uniform

Four benchmarks added to `srq1_baselines_stat.py` 2026-08-22 (naive, seasonal-naive,
drift, Ridge), on Brian's instruction and because their absence is conspicuous:
Hyndman & Athanasopoulos §5.2 defines the first three as *the* standard benchmark
set, and the M-competitions score every entrant against them.

**They immediately produced an uncomfortable and important result.**

| Category | SeasonalNaive WMAPE | tuned GBM WMAPE | verdict |
|----------|--------------------:|----------------:|---------|
| CSD | **19.2%** | 15.3-17.5% | GBM ahead by 2-4pp |
| RTD | **27.3%** | 35.1-37.0% | **seasonal-naive WINS by ~8pp** |
| energidrikke | 23.8% | 12.1-13.9% | GBM ahead by ~10pp |
| danskvand | 35.9% | 18.9-23.7% | GBM ahead by ~12pp |

**On RTD a zero-parameter benchmark beats every tuned model in the thesis.** On CSD
the tuned models lead by only 2-4pp after 30 Optuna trials per model.

### This must be reported, not buried

It is precisely the M4 finding (Makridakis et al. 2018) reproduced on this dataset:
sophisticated methods frequently fail to beat simple benchmarks. Discovering it now
is far better than an examiner discovering it, and the benchmark's absence would
have been the first thing questioned.

Three honest readings, all of which should appear:

1. **The ML advantage is real but category-dependent** -- large on energidrikke and
   danskvand, marginal on CSD, negative on RTD. The thesis should claim a
   conditional advantage, not a general one.
2. **RTD needs a direct answer.** Both arms sit near 35% WMAPE and the free
   benchmark beats them. The defensible statement is that RTD is the hardest
   category and the tabular approach does not help there -- a finding about the
   limits of the method, not a failure to hide.
3. **It corroborates F49 rather than undermining it.** The categories where pooling
   helped (danskvand, energidrikke) are the same ones where ML most clearly beats
   seasonal-naive. Coherent: those categories have learnable structure; RTD has
   less. Two independent analyses agreeing on which categories are tractable is
   worth stating.

### The metric split repeats here

On **medMAPE** seasonal-naive is poor (CSD 54.7%, RTD 89.4%, energidrikke 95.9%),
because its strength is volume-weighted WMAPE. **Seasonal-naive is good on big
brands and bad on typical ones** -- structurally the same finding as F50/F51 for
pooling. Worth reporting as a pattern across analyses, but it does not erase the RTD
result: WMAPE is the operational metric and RTD is where it loses.

## F53 — The Ridge arm's first run was broken; bug and fix recorded

The Ridge baseline's first run reported **WMAPE = inf% (CSD, RTD)** and
**345,856,990% (energidrikke)**. These are not accuracy results.

**Cause.** Ridge predicts in log space and the result is inverted with `expm1`
without bounding. One extrapolated prediction becomes astronomically large after
exponentiation, and a single such series destroys a volume-weighted sum. That the
medMAPE values were plausible (62-88%) confirmed a few exploded series rather than a
wholly broken fit -- the median is robust to exactly the failure the mean is not.

Contributing factor: a per-brand Ridge fits ~24 rows against 13 standardised
features, which is close to singular. The L2 penalty shrinks coefficients but does
not bound the **prediction** when a test row sits outside the training envelope.

**Fix.** Clamp in log space *before* inverting, bounded by that series' own observed
history widened 3x. Justified as a forecasting constraint rather than a fudge: a
monthly demand forecast three times the largest month ever observed for that brand
is an extrapolation failure a practitioner would reject. Applied identically to
every brand, and **the clip count is now reported per category** so the write-up can
state how often the bound bound rather than hiding it.

**Methodological point worth a sentence in the thesis:** this is a second concrete
instance of WMAPE's sensitivity to single diverged series, alongside CSD Prophet
(P0038 F72, 60% of the category figure from one brand). It is the reason
`stat_baselines.md` leads with medMAPE for the per-series statistical arm, and it is
evidence for the general claim rather than an isolated nuisance.

## F54 — The feature matrix is engineered for TREES; a linear model needs logged inputs

The single most consequential finding of this session's baseline work, and it
supersedes the diagnosis in F53.

### What happened

Pooled Ridge (built to fix F53's clipping) came back **worse**: 182-301% WMAPE, with
`alpha=1000.0` -- the top of the grid -- selected in all eight cells. Hitting a grid
ceiling everywhere is a signal that tuning is compensating for something it cannot
fix, so the alpha sweep was widened and instrumented rather than simply extended.

**Log-space RMSE was flat at ~3.92 across SEVEN orders of magnitude of alpha**
(1e-4 to 1e3), and medMAPE was pinned at 99.6% -- the model predicted ~zero for
essentially every brand. Regularisation was irrelevant; the specification was wrong.

### The cause

**The features are in raw units; the target is logged.**

`lag_1`, `lag_2`, `rolling_mean_4` etc. are raw `sales_units`. The target
`log_sales_units` is `log1p(sales_units)` (verified numerically, not assumed).
Fitting `log(y) ~ b*(raw lags)` asserts an **additive** relationship where the true
one is **multiplicative**.

**Trees are immune** -- they split on rank order, so any monotone transform of a
feature is equivalent. That is why LightGBM and XGBoost perform well on exactly the
same columns, and why the defect went unnoticed: no tree-based model could have
revealed it.

### The fix and its effect

Log the volume-valued features (`lag_*`, `rolling_*`); leave calendar features and
`promo_intensity` alone, as they are not volumes.

| | log-space RMSE | WMAPE | medMAPE |
|---|---:|---:|---:|
| CSD, raw features | 3.92 | 1705% | 99.6% |
| CSD, logged features | **0.93** | **22.6%** | **29.5%** |

Full result after the fix:

| Regime | CSD | danskvand | energidrikke | RTD |
|--------|----:|----------:|-------------:|----:|
| Ridge within-category | 22.8% | 21.5% | 22.1% | 56.3% |
| Ridge all-categories | 25.1% | 24.0% | 19.9% | 52.0% |
| tuned GBM (reference) | 15.3-17.5% | 18.9-23.7% | 12.1-13.9% | 35.1-37.0% |

**Ridge is now a legitimate baseline**, within ~5-8pp of tuned gradient boosting on
three of four categories. The earlier per-brand figures (19.4-47.3% WMAPE with heavy
clipping) were accidentally reasonable for the wrong reason: with ~24 rows the model
could not move far from the mean, so the misspecification was masked.

### Why this matters beyond Ridge

1. **The Ridge -> GBM comparison is now meaningful.** It was measuring "linear model
   with wrong functional form" vs "trees", which is not the nonlinearity premium.
   With logged inputs the ~5-8pp remaining gap is a defensible estimate of what
   nonlinearity buys.
2. **It is a real limitation of the feature matrix worth one sentence in the
   thesis.** The engineered features encode a modelling assumption -- tree-based
   learners -- that was never stated. Any future linear or neural model on this
   matrix inherits the same trap.
3. **F53's diagnosis was incomplete.** The clipping bound was a symptom fix; the
   explosion happened *because* the misspecified model extrapolated wildly. With
   logged features the pooled clip rate is 81/1519 (~5%) rather than ~1 per series.

### Consequence for the write-up

The per-brand Ridge row in `stat_baselines.csv` is **still misspecified** -- the fix
lives in `srq1_ridge_pooled.py`, not in `srq1_baselines_stat.py`. Either port `_prep`
into the per-brand arm or drop that row and cite the pooled figures. **Do not report
the per-brand Ridge numbers as they stand.**

RTD remains the hard category in every arm (Ridge 52-56%, GBM 35-37%,
seasonal-naive 27.3% WMAPE), which corroborates F52.

## F55 — DEC-ENSEMBLE-SCENARIO: the ensemble becomes its own rung, not a change to C

Brian, 2026-08-22, resolving task 12. **His framing is better than the one this plan
proposed** and the reasoning is worth preserving.

The objection to exposing pooled+specialised inside `C_model` was that it changes
what C *is*: from "the trained model this thesis built, served" to "an ensemble",
making `B -> C` ambiguous. Brian's answer removes the objection entirely -- **make it
a separate scenario**. C stays exactly as specified; the ensemble gets its own rung
and its own measurement.

The structural argument is the strongest part: the thesis already runs
specialised-vs-pooled at the **data/model** layer (F49). Running the same contrast at
the **serving** layer asks the same question one level up. That is a coherent design
rather than a bolt-on, and it makes the pooled/specialised theme a through-line
across two research questions instead of a one-off SRQ1 result.

| Scenario | Serves |
|----------|--------|
| `C_model` | specialised model: one prediction + interval + accuracy context |
| `F_ensemble` | pooled AND specialised, each with WMAPE + medMAPE, plus their agreement |

`C -> F` isolates exactly one variable: **does exposing model disagreement improve
the agent's forecast?** Publishable either way -- a null result says a single
well-calibrated estimate suffices, which is itself a useful interface finding.

Note F needs running against only ONE orchestrator. The question concerns the
interface, not the engine, so no Prometheus twin is required.

### Cost and sequencing

~$8-10 at 5 repeats, against the ~$42 five-scenario baseline. **Sequence it last** --
after B/C/D/E are locked and A_plain has run. An un-started scenario can be dropped
for free if time or budget tightens; a half-integrated ensemble inside C would
contaminate the cleanest comparison in the thesis.

## F56 — What the serving payload should and should not carry

Resolving Brian's follow-up: should the tool serve every model's prediction (tuned,
seasonal-naive, naive) with WMAPE and medMAPE for each?

**Statistics: yes. Predictions: no** -- except the pooled/specialised pair, which is
what `F_ensemble` exists to test.

### Why more statistics help

"Your model: 33.6% WMAPE / 36.6% medMAPE. Best benchmark: 27.3% / 89.4%" is true,
compact, and actionable: it tells the agent *this category is hard, and the model's
edge is on typical brands rather than on volume*. Nothing in it requires a judgement
the agent cannot make.

**Both metrics, not one.** F52/F50/F51 all found the same volume-weighted vs
per-series split, and reporting only WMAPE would hand the agent the flattering half.

### Why more point predictions do NOT help

Seasonal-naive's RTD figure (27.3% WMAPE) comes from being accurate on **large**
brands; its medMAPE is 89.4%, i.e. it is badly wrong about typical ones. Handing the
agent "seasonal-naive says 4.1M units" gives it no way to know whether *this
particular brand* is one seasonal-naive handles well -- that depends on the brand's
volume rank, which is not in the payload and which the agent cannot infer.

The result is a plausible-looking number carrying a good-looking headline statistic
and no basis for weighting it. That is not more context; it is an invitation to
average two estimates that should not be averaged. **A prediction the recipient
cannot weight is noise wearing the costume of information.**

The pooled/specialised pair is the deliberate exception: both are general-purpose
models with comparable coverage across all brands, so their *disagreement* carries
information in a way "the naive benchmark disagrees" does not.

### The metric-choice asymmetry already in the payload

`_track_record` selects the best baseline by **medMAPE**. For RTD that picks Naive
(44.1% medMAPE) and reports `improvement_vs_baseline_pp = 7.4`. Had it selected by
WMAPE it would pick SeasonalNaive (27.3%) and the model would be **losing by 6.3pp**.

Same data, opposite story, decided by which yardstick chooses the opponent. The
medMAPE choice is defensible (WMAPE is outlier-fragile for per-series baselines --
Prophet's 972% proves it), but it is the framing that flatters the artefact.
**Disclose the choice in the methodology rather than letting it pass as neutral**,
and consider reporting both baselines.

## F57 — Per-brand Ridge after the F54 fix: improved, still not citable

The logged-feature fix was ported into `srq1_baselines_stat.py::run_ridge`
(2026-08-22) so the per-brand arm no longer carries the misspecification. Results
improved substantially:

| Category | before fix | **after fix** | medMAPE | clipped |
|----------|-----------:|--------------:|--------:|--------:|
| CSD | 19.5% | **19.4%** | 43.5% | 59/665 (9%) |
| danskvand | 22.2% | **10.9%** | 40.6% | 9/174 (5%) |
| energidrikke | 19.4% | **18.3%** | 81.5% | 46/308 (15%) |
| RTD | 47.3% | **40.5%** | 56.1% | 44/372 (12%) |

### The danskvand number is not trustworthy, and should not be reported

**10.9% WMAPE beats every tuned GBM (18.9-23.7%).** A regularised linear model
beating tuned gradient boosting is not impossible on small data, but this specific
number should not be cited, for a mechanical reason:

**The extrapolation bound truncates LARGE predictions.** Truncating over-forecasts
mechanically improves a volume-weighted metric. With 5-15% of predictions clipped,
the bound is load-bearing rather than a guardrail, so an unknown share of the
improvement is the clip, not the model.

The medMAPE column corroborates: danskvand Ridge is **40.6% medMAPE** against the
GBM's ~35-39%. Strong on volume-weighted error, mediocre per-brand -- precisely the
signature of a few large predictions being clipped into place.

### What to cite instead

**Cite the pooled Ridge figures from `ridge_pooled.csv`** (21.5-25.1% within
category, clip rate ~1-5%), not the per-brand ones. Two reasons:

1. The per-brand arm remains structurally under-determined: ~24 rows against 13
   features is near-singular regardless of feature scaling. The F54 fix addressed
   functional form, not sample size.
2. The pooled arm matches the GBMs' fitting regime, so Ridge -> GBM isolates
   nonlinearity rather than confounding it with how much data each model saw.

**The per-brand Ridge row is retained in `stat_baselines.csv` for completeness and
because the clip counts are now reported, but the write-up should use the pooled
figures and say why.** Reporting the flattering 10.9% without the clip rate beside
it would be the kind of number that does not survive a question.

### Cross-check with the wider pattern

RTD is the hard category in every arm without exception:

| Method | RTD WMAPE |
|--------|----------:|
| SeasonalNaive | **27.3%** |
| tuned GBM | 35.1-37.0% |
| Ridge (per-brand) | 40.5% |
| Ridge (pooled) | 52.0-56.3% |
| ARIMA | 53.3% |
| Prophet | 66.8% |

**A zero-parameter benchmark leads the entire table on RTD.** That corroborates F52
from a second direction and makes the RTD limitation impossible to attribute to any
single method's weakness -- it is a property of the category.

## F58 — Tuning upgrade: expanding-window CV, 100 trials, dual objective

`srq1_benchmark_cv.py`, built 2026-08-22 on Brian's instruction. Addresses the three
gaps in `srq1_benchmark_tuned.py`. **The old script's protocol was correct** -- no
leakage, proper three-way split, seeded, TPE, data-driven selection -- but its
*budget* was under-powered.

| Gap | Old | New |
|-----|-----|-----|
| Validation | single split | **expanding-window CV, 4 folds** |
| Trials | 30, unjustified | **100, with convergence curve saved** |
| Objective | WMAPE only | **tuned twice: WMAPE and medMAPE** |
| Stability | none | plateau trial reported per study |

### Expanding-window folds verified

danskvand: train grows 203 -> 319 -> 435 -> 551 rows while validation stays a fixed
forward block. Training never includes a month later than the one being predicted.

**K-fold CV would be invalid here** and this must be said in the methodology:
shuffling rows lets a model train on 2026-06 and predict 2026-03, which is not a
forecast. Splits are on distinct PERIODS, not rows -- rows are brand-months, so a
row-wise split would place the same month in both train and validation for
different brands.

The test split is untouched throughout; CV happens strictly inside train+val.

### The trial budget is justified EMPIRICALLY, not by convention

**There is no citable "correct" number of trials.** An earlier claim in this session
that "convention is 50-200" was practitioner folklore with no source, and citing it
would invite a question with no good answer.

Instead `cv_convergence.csv` records the running best CV score per trial, and
`plateau_trial` reports where improvement fell below 0.1% relative. The write-up can
then state *"the objective plateaued after N trials, indicating the budget was
sufficient"* -- an empirical argument that can be shown in a figure, which is
stronger than an appeal to convention.

### Dual objective answers the "why WMAPE?" question with data

Each configuration is tuned twice. If the selected model is the same under both
objectives, the choice of objective did not matter and that is reportable. If it
differs, the magnitude is measured rather than speculated about. Either outcome
converts an implicit choice into a stated, evidenced one.

## F59 — Citation discipline: what is safe to cite and what is not

Brian requires an academic source at every best-practice claim. **Some of what this
session asserted cannot be sourced, and that must not be papered over.**

### Safe to cite (verify details independently before submission)

| Claim | Source |
|-------|--------|
| naive / seasonal-naive / drift are the standard benchmarks | Hyndman & Athanasopoulos, *FPP3*, §5.2 |
| simple methods frequently beat complex ones | Makridakis et al., M4 competition (2018, 2020) |
| TPE sampler | Bergstra, Bardenet, Bengio & Kegl (2011), NeurIPS |
| random > grid search for HPO | Bergstra & Bengio (2012), *JMLR* 13 |
| Optuna design | Akiba et al. (2019), KDD |
| rolling-origin / time-series CV | Hyndman & Athanasopoulos §5.10; Tashman (2000), *IJF* 16(4) |
| regularised linear models as tabular baseline | Hastie, Tibshirani & Friedman, *ESL* ch. 3 |

### NOT citable -- do not put a reference next to these

- **"50-200 trials is the convention."** Stated earlier this session; it is folklore.
  The required budget depends on the search space. Use the convergence evidence.
- **"3x the observed maximum" as an extrapolation bound.** Invented for this project.
  See F60.
- **The `confidence` index in `forecast_tool.py`.** 0.5/0.5 weights and 70/40 tier
  cutoffs are arbitrary. Describe as a heuristic; never imply a calibrated
  probability.

**All citations above are LEADS TO VERIFY, not verified references.** Page numbers,
exact titles and whether a specific claim appears where stated must be checked
against the actual sources before submission.

## F60 — The extrapolation clip is not academically sound as a headline result

Brian asked directly whether clipping is defensible and whether reporting a clipped
model's error conflates performance. **He is right that it does.**

### Defensible

- Constraining forecasts to a plausible range is normal in deployed systems.
- Applied uniformly across brands, not tuned per series.
- The bound is data-derived (that series' own history), not a fixed constant.

### Not defensible

- **The 3x multiplier is arbitrary.** 2x or 5x yields different numbers. A result
  that moves with an unjustified constant is not a measurement of the model.
- **It is a post-hoc repair** of a misspecified model, not a modelling decision made
  in advance.
- **It changes the estimand.** "Ridge + this clipping rule" is a different estimator
  from "Ridge". Reporting the former as the latter conflates the two, exactly as
  Brian said.

### Ranked options for the write-up

1. **Cite pooled Ridge only** (`ridge_pooled.csv`), where the fit is well-determined
   and clipping is nearly inert (1-5%). **Recommended.**
2. **Report clipped AND unclipped**, letting the unclipped `inf%` stand as evidence
   that per-brand Ridge is unusable at ~24 rows. Honest, and a genuine finding.
3. Report clipped with the clip rate as a stated limitation. Survivable but weakest.

**Do not use option 3 as the primary presentation.**

## F61 — Live contamination in the payload: exclude, do not annotate

The per-brand Ridge row leaked into `forecast_tool.py` as CSD's "best baseline"
(43.5% medMAPE) via `stat_baselines.csv`. Now excluded from the baseline pool.

**More context would NOT have fixed this.** An agent told "Ridge scores 43.5% but 9%
of its predictions were clipped" still cannot recover Ridge's true error -- nobody
can, which is the whole problem. Unreliable numbers must be excluded, not annotated.

**Worth stating as an SRQ2 interface principle:** *an interface should not serve a
number it cannot vouch for, however much caveat text accompanies it.* Caveats
transfer responsibility to a consumer who lacks the information to discharge it.

## F62 — Per-brand context for weighting predictions: the cheap version is viable

Brian asked twice whether the per-brand information needed to weight competing
predictions could simply be supplied. **Technically yes; the full version is not
worth building, but a reduced version is.**

### Why the full version fails

Per-tercile x per-method x per-category accuracy slices 230 brands into ~24 cells.
danskvand's small tercile would hold ~10 brands. Those estimates are too noisy to
guide a decision -- the context would look authoritative and mislead.

It also turns the tool into an expert system that reasons about model selection and
reports its reasoning to an LLM which re-reasons about it. That is a substantial
build and squarely an SRQ2 design question.

### The cheap version worth doing

Include **the brand's own volume tercile** and **the served model's accuracy within
that tercile**. One number, adequately powered (~56 brands per tercile when pooled
across categories), directly relevant:

> "This brand is in the smallest volume tercile; the model's median error on small
> brands is 48%."

Honest, actionable, and no per-method estimates invented from ten observations. It
strengthens the SRQ2 uncertainty story at low cost.

**Status: proposed, not built.** Added as task 14.

## F63 — CORRECTION to F57: danskvand's Ridge result is real; clipping is per-category

DEC-RIDGE-BOTH (Brian, 2026-08-22) required publishing clipped AND unclipped Ridge
rather than dropping the per-brand arm. Doing so **refuted the suspicion recorded in
F57**, which is the point of having run it.

| Category | unclipped WMAPE | clipped WMAPE | difference | clips |
|----------|----------------:|--------------:|-----------:|------:|
| CSD | 19.9% | 19.4% | 0.5pp | 59/665 |
| **danskvand** | **10.9%** | **10.9%** | **none** | 9/174 |
| energidrikke | 2.8e13% | 18.3% | catastrophic | 46/308 |
| RTD | 2458.9% | 40.5% | catastrophic | 44/372 |

### What F57 got wrong

F57 claimed danskvand's 10.9% "should not be reported" because the extrapolation
bound was truncating over-forecasts and mechanically flattering a volume-weighted
metric. **The unclipped figure is identical to the clipped one.** The 9 clips that
occurred did not touch the volume-weighted total. So per-brand Ridge genuinely
achieves 10.9% WMAPE on danskvand, beating every tuned GBM (18.9-23.7%).

The reasoning in F57 was sound a priori -- clipping *can* do exactly that, and the
high clip counts elsewhere prove it -- but **the check should have been run before
the claim was made, not after.** A clip *count* does not establish that clipping
changed the *result*; only comparing the two does.

CSD is likewise nearly clip-independent (0.5pp).

### What F57 got right

energidrikke and RTD are unusable without the bound. 2.8e13% is not an accuracy
figure; it is a model that failed completely on at least one series and then had that
failure amplified by `expm1`. There the clipped number genuinely is "Ridge + our
arbitrary constant" rather than "Ridge".

### The corrected finding, which is better than either previous version

**Per-brand Ridge is legitimate on CSD and danskvand and unusable on energidrikke and
RTD.** That is more informative than "Ridge works" or "Ridge is broken", and it has a
mechanical explanation: with ~24 rows against 13 features the fit is near-singular,
so whether it produces a sane extrapolation is essentially a property of how
well-conditioned that particular category's design matrix happens to be.

### How to report it

Publish the table above **exactly as it stands**, both columns. Then:

- For CSD and danskvand, cite the figures -- the clipped and unclipped agree, so the
  bound is demonstrably inert and the numbers describe Ridge.
- For energidrikke and RTD, report the unclipped figures as **evidence that the
  method fails at this sample size**, not as accuracy measurements. State that the
  clipped variants are shown only for completeness and are not comparable to the
  other models.
- Keep citing the POOLED Ridge (`ridge_pooled.csv`) for the nonlinearity-premium
  argument, since it is well-conditioned in every category.

**Brian's judgement was better than the recommendation it overrode.** Dropping the
per-brand arm (F60 option 1, which this assistant recommended) would have concealed
both a genuine result and a genuine failure mode.

## F64 — Implausible error rates are now served as "n/a", not as numbers

Brian, 2026-08-22, on whether `2.8e13%` should reach the LLM: *"I could imagine that
with missing context a 2.8x10^13% could bias / confuse the LLM, but perhaps a 'n/a'
when the numbers are irrational being sent in the payload would make it better."*

**Correct, and for a sharper reason than confusion.** A figure that large is not an
extreme measurement -- it is a **failure indicator wearing a number's clothes**. An
agent shown it either ignores it (harmless) or attempts to reason about it (harmful),
and it has no way to tell which case it is in. Serving `"n/a (model failed on this
category)"` preserves the information that the method failed while removing the false
quantity.

Implemented in `forecast_tool.py::_metric`: any value above **300%**, or non-finite,
is replaced with an explicit `"n/a"` plus a reason. Improvement deltas are computed
only when both operands survive, so no arithmetic is performed on a non-number.

**300% is a display threshold, not an analysis parameter.** A forecast wrong by 3x is
already useless, so nothing above it carries decision-relevant signal. The RAW
figures remain in `stat_baselines.csv` and the thesis reports them in full (F63) --
this governs only what the serving interface hands an agent. Recorded in the P0041
register as one of ours, never to be cited.

**A finding surfaced while testing it:** on energidrikke the tuned model **loses to
Drift by 12.8pp on median MAPE** while winning by 3.4pp on WMAPE. Another instance of
the volume-weighted vs per-series split, now visible in the payload rather than
hidden by reporting one metric.

## F65 — CV results: the objective choice matters, and the budget IS adequate

`srq1_benchmark_cv.py --trials 100 --folds 4`, completed 2026-08-22. 16 studies.

### The objective choice is consequential and asymmetric

Tuning for medMAPE instead of WMAPE changes the result materially:

| Category | Model | tuned for WMAPE | tuned for medMAPE |
|----------|-------|-----------------|-------------------|
| CSD | LightGBM | **14.5%** / 33.2% | 22.8% / **30.4%** |
| CSD | XGBoost | **15.2%** / 31.8% | 20.5% / **28.8%** |
| energidrikke | LightGBM | **16.5%** / 34.7% | 29.8% / 39.1% |
| RTD | LightGBM | **31.8%** / 38.1% | 40.1% / **34.6%** |

**Tuning for medMAPE costs 8-13pp of WMAPE and buys 2-3pp of medMAPE.** The trade is
strongly unfavourable, so WMAPE-tuning is close to dominant -- and on energidrikke
LightGBM, medMAPE-tuning is worse on BOTH metrics (29.8/39.1 vs 16.5/34.7), which
means the medMAPE objective found a genuinely worse configuration.

**This converts an implicit choice into an evidenced one**, which was the point of
running it. The write-up can now state that WMAPE was chosen as the tuning objective
and that the alternative was measured and costs more than it returns.

### The trial budget is adequate -- but the first plateau metric said otherwise and was WRONG

Initial output reported `plateau@99, 93, 89, 96...`, implying 100 trials was
insufficient. **That was a defect in the metric, not a finding.**

`_plateau` used a **0.1% relative** tolerance. On a score of ~17 that is 0.017pp, so a
study still drifting by 0.2pp registered as "not converged". Measuring the actual
gains gives the opposite picture:

| Category | Model | total gain | gain in last 25 trials | share |
|----------|-------|-----------:|-----------------------:|------:|
| CSD | LightGBM | 4.17pp | 0.16pp | 3.8% |
| CSD | XGBoost | 0.64pp | 0.19pp | 29.1% |
| danskvand | LightGBM | 32.71pp | **0.00pp** | 0.0% |
| danskvand | XGBoost | 3.13pp | **0.00pp** | 0.0% |
| energidrikke | LightGBM | 12.06pp | 0.06pp | 0.5% |
| energidrikke | XGBoost | 1.56pp | **0.00pp** | 0.0% |
| RTD | LightGBM | 7.89pp | 0.23pp | 2.9% |
| RTD | XGBoost | 3.16pp | 0.22pp | 7.0% |

**The last 25 trials contribute 0-7% of total improvement in six of eight studies, and
exactly zero in three.** Absolute gains are 0.00-0.23pp -- far below anything that
would change a reported result.

CSD XGBoost's 29.1% is the apparent exception, but on a total gain of 0.64pp it
represents 0.19pp of movement. Not meaningful.

**Fixed:** `_plateau` now uses an absolute 0.5pp tolerance, and `_gain_tail` reports
the share of improvement in the final 25 trials. The claim to write:

> The search budget was 100 trials per configuration. Improvement was effectively
> exhausted well before the budget was reached -- the final 25 trials contributed
> under 7% of total improvement in six of eight studies and none at all in three --
> indicating the budget was sufficient for this search space.

**Methodological note worth carrying into the thesis:** a convergence *criterion*
must be expressed in units where the question makes sense. A relative tolerance on an
error percentage answers "is the number still moving?" when the question is "would
more search change the conclusion?" The first version measured the wrong thing and
would have led to spending compute on a non-problem.

### CV supersedes the single-split numbers

| | single split | CV-tuned |
|---|---:|---:|
| CSD LightGBM | 15.6% | 14.5% |
| RTD LightGBM | 35.1% | 31.8% |

Not badly wrong, but superseded. **Cite `cv_metrics.csv`, not `tuned_metrics.csv`,**
and note that the serving payload's `_track_record` still reads the latter -- it
should be repointed once the CV numbers are final.

## F66 — Chapter audit: ch6 passes the fact-checker and is wrong throughout

Full audit at `05_thesis_writing/notes/2026_08_22-21_00-chapter-staleness-audit.md`.

`check_chapter_facts.py` reports **42 ERROR / 6 CHECK** across the drafts. Ch1 fell
from 46 items to 1 after the 2026-08-22 rewrite (the remaining item is a benign
mention of totalbeer while explaining its exclusion).

### The important finding is what the tool CANNOT see

**`ch6-model-benchmark.md` scores ZERO errors and contradicts every current results
file.** The checker matches known-stale *phrases*; it has no rule for a *number that
used to be right*. Ch6 is almost entirely numbers.

| Category | ch6 claims (XGBoost) | current (cv_metrics.csv) | drift |
|----------|---------------------:|-------------------------:|------:|
| CSD | 16.5% | 15.2% | -1.3pp |
| danskvand | 23.8% | 20.9% | -2.9pp |
| energidrikke | 11.4% | 13.0% | +1.6pp |
| RTD | 31.0% | **36.1%** | **+5.1pp** |

Every figure is wrong, RTD by 5pp. The ARIMA comparison table is equally stale
(CSD 24.2% vs 21.8% current), so every "ML wins by Npp" margin in the verdict column
is computed from two wrong numbers.

Ch6 is also **missing** the entire 2026-08-22 body of work: the three simple
benchmarks, seasonal-naive beating every tuned model on RTD, the pooled-vs-per-category
result (SRQ1's third named axis), Ridge, the CV protocol, and the dual-objective
finding.

**Generalisable lesson worth carrying:** a zero-error automated check is not evidence
of currency. Number-level rules should be added so a regenerated results file flags the
chapters citing the old values. Until then every chapter number is unverified unless
traced by hand.

### Ch6's prose contradicts its own figure

Ch6 lines 190-192 state peak RAM is "orders of magnitude under the 8 GB budget" --
**true and measured** (3-4 MB). But `generate_figures.py::fig4_ram_budget` is entirely
hardcoded with a literal 512 MB "active ML model". Fix the figure to match the prose.

### Ch8 needs a rewrite, not edits

11 errors, all pointing one way: it describes a judge-scored two-arm comparison
(GPT-4o, N=50, claude-sonnet-4-6, "E2B not configured"). The design is a five-scenario
capability ladder with programmatic measures on gpt-5.5. The chapter's *structure*
assumes the old design, so line-by-line patching will not work.

Blocked on the D/E runs regardless.

### Recommended order

1. **Ch6 numbers** -- best value per hour; structure is sound, values are stale.
2. **`fig4_ram_budget`** -- a fabricated figure contradicting its own chapter.
3. **Ch8 rewrite** -- largest, blocked on D/E results.
4. **Ch3 methodology** -- 10 errors, and where the judge protocol is *specified*.
5. **Ch9/Ch10** -- mostly follow.

## F67 — Corrected plateau numbers: budget confirmed adequate, claim now precise

Re-run after fixing `_plateau` (F65). Accuracy figures identical -- the run is
deterministic, so only the diagnostic changed.

| | broken metric (0.1% relative) | **corrected (0.5pp absolute)** |
|---|---|---|
| CSD LightGBM / wmape | 99 | **11** |
| danskvand LightGBM / wmape | 73 | **10** |
| energidrikke LightGBM / wmape | 96 | **3** |
| RTD XGBoost / wmape | 89 | **16** |

Median plateau across the WMAPE-tuned arm: **~16 trials**. The `gain_in_last_25_pct`
column corroborates independently: **0.0% in five of eight studies**, under 8% in
seven.

### Two studies genuinely run longer, and the claim should say so

- danskvand XGBoost / medmape -- plateau@87, 13.9% of gain in the last 25 trials
- CSD XGBoost / wmape -- plateau@15 but 29.1% of gain late (on a total gain of only
  0.64pp, so 0.19pp of movement -- not material)

**The precise claim, which is stronger than a uniform one because the table visibly
supports it:**

> The search budget was 100 trials per configuration. In most studies the
> cross-validated objective plateaued well before that -- median ~16 trials, with no
> improvement at all in the final quarter of the search for five of eight -- and the
> budget accommodates the slower studies with margin.

Do NOT claim every study plateaued early. Two did not, the table shows it, and
overstating would invite exactly the question the evidence otherwise answers.

### Lesson worth one methodology sentence

This is the second time in one session that a diagnostic, rather than the underlying
result, was the thing at fault (see also F63, where a clip *count* was mistaken for
evidence that clipping changed the *result*). Both times the fix was to measure the
quantity the question is actually about -- absolute improvement rather than relative
drift; clipped-vs-unclipped output rather than clip frequency.
