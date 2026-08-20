---
pid: P0040
created: 2026-08-20 00:00:00
updated: 2026-08-20 00:00:00
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
