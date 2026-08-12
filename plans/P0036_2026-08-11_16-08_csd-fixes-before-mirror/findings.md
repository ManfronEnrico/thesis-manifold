---
pid: P0036
created: 2026-08-11 16:08:00
updated: 2026-08-11 16:08:00
---

# P0036 — Findings

All measurements below are from read-only queries against
`02_thesis_data/_01_converted/nielsen/parquet_nielsen/CSD/views/` (9,080,538 fact rows)
and `_02_preprocessing/nielsen/CSD/pipeline_step_outputs/`, run 2026-08-11.

## F1 — Promo exists at the parent market, is identically zero at the region children

Promo column in the raw facts: `sales_value_any_promo` (also `sales_units_any_promo`,
`sales_in_liters_any_promo`, `sales_units_any_tpr`).

| Scope | Fact rows | Non-null promo | Nonzero promo |
|-------|-----------|----------------|---------------|
| Parent `1256338` (DVH EXCL. HD) | 196,657 | 182,467 | **119,010** |
| 9 region children (live filter) | 453,685 | **0** | **0** |

Parent spans 44 periods; max promo value 308,302,433.53.

Nielsen reports promo at rollup/chain level, never at geographic-region level. Exactly
22 markets carry promo — all rollups or chains. The region filter that P0027 introduced
to prevent double-counting also eliminated every promo observation.

**Consequence:** P0032's F10 ("promo is structurally absent") is true only of the chosen
scope. The columns are not dead and must **not** be dropped.

## F2 — "HD" = hard discount (a retail channel), not discounting or promotions

Checked because it was a plausible explanation for the zeros — if the market definition
excluded discounted selling, promo-zero would follow naturally. It does not.

- `nielsen-prometheus_data_model.md:69` — "**DVH EXCL. HD** (Dagligvarehandel excluding
  hard discount)"
- `build_feature_matrix.py:24` — "a clean branded-demand signal excluding **hard discount**"

Decisive: the market list contains sibling *channel* definitions — `DVH EXCL. LIDL`,
`DVH EXCL. DISCOUNT/HD` — and a `DISCOUNT` market that **carries promo**. Excluding
hard-discount *stores* never implied excluding promotional *selling* in the remaining
stores.

## F3 — Parent dominates children at brand×month; no trade-off exists

| Metric | Parent `1256338` | Region children |
|--------|------------------|-----------------|
| Fact rows | 196,657 | 453,685 |
| Distinct brands | **144** | 136 |
| Distinct periods | 44 | 44 |
| Brand-month rows (>0) | **3,917** | 3,641 |
| Brands @ MIN_PERIODS>=24 | **85** | 74 |
| Rows @ MIN_PERIODS>=24 | **3,392** | 3,038 |

Children have more *fact* rows but fewer *brand-month* rows: geographic splitting
fragments each brand-month into thin slices that individually fail MIN_PERIODS.

P0026's headline "10.6× more data" (2.3k → 25.1k) counted the same brand-months nine
times. It was never additional information, and at brand×month it is a net loss.

## F4 — The 196k → 2,552 funnel is arithmetic, not attrition

| Stage | Rows | Brands |
|-------|------|--------|
| Facts @ DVH EXCL. HD | 196,657 | — |
| step_1_aggregate_bymonth | 3,975 | 140 |
| step_2_calendar_filled | 6,160 | 140 |
| step_3_filtered_series | 2,552 | 58 |
| step_4 / step_5 / final matrix | 2,552 | 58 |

The large drop is the **product→brand rollup**: 196k SKU-level rows collapse to
144 brands × 44 periods, capped at ~6,336 cells. Definitional, and exactly what
DEC-GRAIN specifies. Not a defect.

The genuine concern is the next step: MIN_PERIODS culls 140 → 58 brands (59%).

## F5 — Per-brand depth: 44 months is a hard ceiling

| Statistic | Value |
|-----------|-------|
| Periods available | 44 |
| Brands | 144 |
| Median series length | 33 months |
| Brands at all 44 months | **51** |
| Brands at >=40 months | 56 |

Top brands by volume, all at 44/44 months: HARBOE (202M units), COCA COLA (193M),
PEPSI (166M), **FAXE KONDI (118M)**, FANTA (33M).

FAXE KONDI has complete coverage — 44/44 months, no gaps, 4th by volume. An excellent
demo brand.

## F6 — Single-brand training loses 77× the data and gains nothing

Assessed against Brian's proposal to train exclusively on the highest-data brand
(2026-08-11), on the reasoning that the System B demo only needs one brand.

| MIN_PERIODS | Pooled rows (brands) | Single best brand |
|-------------|----------------------|-------------------|
| >=24 | 3,392 (85) | 44 |
| >=30 | 3,152 (76) | 44 |
| >=36 | 2,865 (67) | 44 |

**The premise does not hold.** Selecting the best brand yields no additional data:
51 brands already sit at the 44-month ceiling. MIN_PERIODS filters on *series length*,
so discarding brands cannot lengthen the survivor — what varies across brands is how
many of the 44 months are non-zero, not how much history exists.

Two consequences:

1. **Unfittable models.** 44 rows × ~30 features is more features than observations.
   XGBoost/LightGBM require pooling across brands to work at all.
2. **No statistical power.** ~12 test points produce error bars wide enough to swallow
   any realistic difference between base LLM / LLM+data / LLM+model — precisely the
   comparison the thesis rests on.

**Resolution — separate training scope from evaluation scope:**
train pooled across surviving brands (a global forecasting model, standard practice),
then demo and evaluate on FAXE KONDI. Delivers the intended single-brand demo, keeps
statistical power, and forecasts Faxe Kondi *better* than a single-brand fit would.

## F7 — Sample-size adequacy for the thesis's actual contribution

Binding constraint is **44 months per series**, invariant to market scope. Current split
1450/348/754 (~12 test months per brand).

| Model class | Verdict |
|-------------|---------|
| Statistical per-brand (ARIMA/ETS/Prophet) | Thin but defensible — ~3.5 seasonal cycles; 12 seasonal lags on 44 points is tight. Declare as a limitation. |
| Classical ML pooled (XGBoost/LightGBM) | Adequate at 2,552–3,392 rows × ~30 features. **Must pool.** |
| Deep learning from scratch | **Not viable.** Do not attempt. |
| Pre-trained / foundation models (Chronos, TimesFM, Moirai) | Well-suited — zero-shot on short series is their target regime. |

**Assessment:** adequate. The RQ asks whether pre-trained models improve predictive
recommendations over training from scratch. A low-data regime is the *condition that
makes that question meaningful*, not a defect — a dataset large enough to train deep
models from scratch would weaken the framing. Recommend stating this explicitly in Ch4
as a deliberate design property rather than apologising for it.

## F8 — Defect locations (live code)

| File | Line | Defect |
|------|------|--------|
| `pre_processing_notebook_csd.ipynb` | 426 | `DVH_REGION_IDS` — 9 region ids |
| `pre_processing_notebook_csd.ipynb` | 457 | `isin(DVH_REGION_IDS)` filter |
| `pre_processing_notebook_csd.ipynb` | 725 | `"region_ids"` in findings artifact |
| `_shared_modules/engineer_features.py` | 317-321 | V3 `promo_intensity` leakage (fix uncommitted) |
| `_shared_modules/engineer_features.py` | 232-235 | `make_calendar` bfill pulls future values backward |

The last two are in a **shared module** — they affect all four categories, so they must
be fixed before P0033 mirrors anything.

## F9 — Silent all-zero columns are the underlying process failure

The pipeline shipped three structurally dead columns and the EDA never flagged them.
That is why the market-scope defect survived multiple review passes, including a
dedicated leakage plan (P0032) that stalled on the symptom without diagnosing the cause.

Worth fixing as a class, not an instance: assert loudly on any all-zero/degenerate
feature, not merely on promo. Tracked as task 3.

## F10 — Sample size per SRQ: the arms have different evaluation units

Checked against RQ **v4** (`01_thesis_research/research-questions/research-questions.md`,
canonical, synced 2026-06-17). Conflating these makes the thesis look weaker than it is.

| SRQ | Evaluation unit | Effective n | Exposure to the 44-month limit |
|-----|-----------------|-------------|-------------------------------|
| SRQ1 (models & efficiency) | Held-out forecast accuracy | ~12 test months × brands × 4 categories | **Directly exposed** |
| SRQ2 (tool interface) | Design artefact | n/a | None |
| SRQ3 (integration readiness) | Capability assessment | n/a | None |
| SRQ4 (ML vs code-as-action LLM) | **Prompts** | **~50** | **Largely insulated** |

**SRQ1 is a genuine accuracy claim** and inherits the limitation. Mitigations: (a) it
compares models on *identical* data, so relative ranking is more robust at small n than an
absolute claim — pair with Diebold-Mariano, already in the System A spec; (b) "category
specialization" spans all four categories, multiplying the evidence base.

**SRQ4 is insulated.** v4 metrics are correctness/consistency/replicability (primary) +
cost/latency (secondary) over ~50 prompts, against a **code-as-action LLM** baseline.
Consistency and replicability measure whether the system answers identically twice — a
trained model does so deterministically, an LLM writing fresh code each time may not. That
finding is unthreatened by the 44-month panel.

Correction to an earlier framing in this session: the SRQ4 arms are not "base LLM vs
LLM+data vs LLM+model". v4's comparator is narrower — **dedicated ML integration vs. a
code-as-action LLM that writes and self-corrects its own forecasting code**. The question is
whether dedicated ML is warranted *at all* (Nika's open question, v4 line 36).

## F11 — Tool interface: the LLM never handles feature vectors

Design question raised by Brian 2026-08-11: how does the LLM obtain 44 rows of lag values
from a natural-language question?

**It does not, by design.** The LLM performs two translations only — intent → typed tool
call parameters, and structured output → prose:

```
"What will Faxe Kondi sales be in 4 months?"
  → {"tool":"forecast_demand","brand":"FAXE KONDI","horizon_months":4}
  → [service: history lookup + feature construction + model run, all server-side]
  → {"point_forecast":…, "lower_90":…, "upper_90":…, "confidence":78,
     "source_model":"LightGBM", "data_window":"2022-04..2025-11"}
  → natural-language answer
```

Feature construction stays server-side, versioned and identical on every call. This is the
SRQ2 contribution as already specified ("typed, structured tool call — not raw model
output").

**This is also the hypothesised SRQ4 mechanism:** the code-as-action baseline must load data
and build features itself on every invocation, with no guarantee of doing so identically
twice — exactly the consistency/replicability axis SRQ4 measures. The interface's determinism
is not incidental to the comparison, it *is* the comparison.

## F12 — Repo hygiene issues found while reading the RQs

1. **`00_thesis_context/thesis-topic/project-overview.md` has an unresolved git merge
   conflict** at lines 2-8 (`<<<<<<<< HEAD` / `========` / `>>>>>>>> origin/main`), leaving
   two competing thesis titles in the file. Needs resolving.
2. The same file is marked **SUPERSEDED** (line 4) and carries **v2** RQs, while the
   canonical v4 set lives in `01_thesis_research/research-questions/research-questions.md`.
   It was the file opened when asking about "the current RQ" — a live trap for future
   sessions. Its internal links also still use pre-P0028 `thesis/…` paths.

Neither blocks P0036. Recorded so they are not rediscovered later.

---

## F15 — DEC-SCOPE confirmed, but the plan's supporting numbers were wrong

Measured against the real parquet views before editing (task 3, 2026-08-11). The
decision holds; three of the figures used to justify it do not.

| Metric | Plan claimed | **Measured** | Verdict |
|---|---|---|---|
| Fact rows, region scope | ~453,685 | **243,691** | wrong |
| Fact rows, parent scope | ~196,657 | **37,999** | wrong |
| Brand-month rows, region | 3,641 | **3,975** | wrong |
| Brand-month rows, parent | 3,917 | **3,917** | correct |
| Nonzero promo, parent | 119,010 | **~23,400** | wrong (per-column) |
| Distinct brands, both scopes | 144 | **140** | wrong |
| Panel depth | 44 months | **44** | correct |
| Brands @ MIN_PERIODS>=24, parent | 85 | **85** | correct |

### The argument changes shape

`task_plan.md` framed DEC-SCOPE as a **free win**: more rows *and* the promo feature.
That is false. Parent scope yields **3,917 brand-month rows vs region's 3,975** — it
**costs 1.5%**, it does not gain.

The correct justification, which survives scrutiny:

- **Promo: 0 → ~23,400 nonzero per column.** All 7 promo columns are identically empty
  at region scope. This is the whole case.
- **No brand loss** — 140 distinct brands under both scopes.
- **6.4× less redundancy** — region scope repeats each brand-period across 9 children
  (243,691 / 37,999 = 6.41), inflating fact rows without adding information at the
  brand × month modelling grain.

**Net: costs 1.5% of brand-month rows, buys the entire promo feature family.**

This matters beyond bookkeeping: the "more rows" claim would not have survived a
defence question, since the aggregation arithmetic makes it implausible on its face.

### Also corrected

- **No `len > 0` guard existed to fix.** The plan said to change `len > 0` to `len == 1`;
  `_load_merged()` had **no guard at all**. Added as new code.
- **No SCD market-dim dedup existed to preserve.** The plan said to keep it. The
  line-454 merge has no `.drop_duplicates()` — safe only because `market_id` is unique
  in the dim (verified: 86 rows, 86 distinct). The new `== 1` guard now enforces this
  rather than relying on it.

### Verified post-patch

`_load_merged()` returns 37,999 rows, exactly 1 market (`1256338` = `"DVH EXCL. HD"`),
140 brands, all sales positive, all 7 promo columns populated. Cell parses via `ast.parse`.
Guard confirmed to raise on a simulated 2-market frame.

### Downstream implications

- **Task 6's parity check** must expect 37,999 fact rows / 3,917 brand-month rows —
  not the plan's figures.
- **Ch4's funnel narrative** cites the 196k→2,552 path (see
  `05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md`). The 196,657
  starting figure is wrong; rebuild the funnel from 37,999 once task 6 runs.
- **FAXE KONDI** confirmed at full 44/44 month depth, 118,158,520 units — the System B
  demo brand is intact under parent scope (feeds task 9).

---

## F16 — make_calendar bfill leakage: measured, fixed, and one live copy left behind

Task 5. The defect at `_shared_modules/engineer_features.py:271` was:

```python
.transform(lambda s: s.replace(0, np.nan).ffill().bfill().fillna(0))
```

`ffill` is legitimate — it carries the last *known* value forward, using only past
information. `bfill` fills **leading** gaps (months before a series' first observation)
with that series' **first observed** value: a fact from the future.

### Impact, measured on CSD at parent scope

| | |
|---|---|
| Calendar rows | 6,160 (140 brands × 44 months) |
| Rows changed by dropping `bfill` | **1,176 (19.1%)** |
| Brands affected | **51 of 140** |
| Of affected rows, in a leading gap | **1,176 (100%)** |
| Leaked value: median / max | 0.0025 / **0.157** |

100% in leading gaps is the diagnostic signature — if `bfill` were doing something
benign, affected rows would be scattered through interior gaps instead.

Worked example, `SPIRIT OF SWEDEN`: 2023-04 through 2023-07 all carried `0.157`,
a value first observed **2023-08**.

### Magnitude is small; that is not the argument

Max leaked value 0.157, median 0.0025 — affected brands are low-distribution
newcomers. The case for fixing is **correctness, not effect size**: a feature that
cannot be constructed at forecast time invalidates the evaluation regardless of how
far it moves the metric.

### Fix

`.ffill().bfill().fillna(0)` → `.ffill().fillna(0)`. Leading gaps fill 0, which is
also the truthful value (the brand was not distributed). Unit-tested: leading gaps
→ 0 not the future value; real observations preserved; no cross-group leak;
**trailing gaps still ffill from the past** (confirming no over-correction).

### Why it survived review — the transferable lesson

The docstring documented the **cross-group** leak (handled via `group_keys`) in
detail and was **silent on future leakage**. Reviewers checked the documented risk
and stopped. Docstring now names both, with reasoning for each.

> Documenting one failure mode can create false assurance about a neighbouring one.

### Left behind deliberately — one live copy of the pattern

`utility_scripts/tests/test_agent_system_comprehensive.py:292` reproduces
`.ffill().bfill().fillna(0)` on `price_per_unit`, and asserts the result is correct
("forward/backward filled").

**Not fixed here**, because: it builds its own mock frame, never imports
`engineer_features`, and is a test fixture rather than pipeline code — so it neither
breaks from this change nor affects any result. But it is a **test encoding the
defect as intended behaviour**, and is exactly where someone would look for the
"right" pattern. Worth cleaning up when tests are next touched.

The 7 other matches are all under `.archive/` (dead code, out of scope).

---

## F17 — Fact-table sparsity verified; "196,657" explained; both stale tests archived

Three loose ends closed after Brian challenged an unverified claim.

### 1. Is the facts table sparse? Partly — the claim needed correcting

Stated in conversation that Nielsen "only emits rows where a brand sold something."
**Measured, that is half right.** At parent market `1256338`, before any filter:

| | Rows |
|---|---|
| Total | 196,657 |
| `sales_units > 0` | 182,399 |
| `sales_units == 0` | **14,202** |
| `sales_units` NULL | **14,190** |
| `sales_units < 0` | 56 |

So explicit zeros and nulls **do** exist — absence and zero are not interchangeable.
But the table is genuinely sparse at the grid level: **1,923 SKUs × 44 periods =
84,612 possible cells, 43,559 present — 51.5% populated.**

Accurate statement for Ch4: *Nielsen emits rows sparsely, mostly where a product was
tracked as selling, with some explicit zeros and nulls; about half the possible
SKU-month grid is absent.* This is why `make_calendar` exists.

Does not affect the F16 fix: whatever the reason a month is missing, filling it from
a *later* month still imports future information.

### 2. Where the plan's "196,657" came from

It is the **raw parent-market row count before the `sales_units > 0` filter**. Not
invented, and not a different market scope — measured one pipeline stage earlier than
the 37,999 it was compared against in F15.

F15's verdict stands (the brand-count, promo and brand-month figures were wrong), but
this one figure is now explained rather than simply wrong. The Ch4 funnel now shows
both stages: 9,080,538 → 196,657 → 37,999 → 3,917 → 6,160 → 2,552.

### 3. Both archived tests confirmed stale, for *different* reasons

Brian moved `test_agent_system_comprehensive.py` and `test_builder_integration.py` to
`utility_scripts/tests/.archive/` — both from the superseded "multiple agents write
everything" approach. Verified:

| File | Verdict |
|---|---|
| `test_agent_system_comprehensive.py` | **Ran, but asserted a defect correct.** Self-contained mock; reproduced `.ffill().bfill()` on `price_per_unit:292` and asserted "forward/backward filled" correct |
| `test_builder_integration.py` | **Could not run at all.** Imports `thesis.thesis_production_system.agents.builder`, removed by the P0028 restructure (2026-07-11). Fails at import; `find_spec("thesis")` → `None`. Dead since July |

`README.md` added to `.archive/` recording both, so this is not re-derived.

**The instructive one is the first.** A test that runs green while encoding a bug is
worse than one that cannot run: the broken test announces itself, the passing test
provides false assurance. Same shape as the root cause in F16 — the `make_calendar`
docstring covered cross-group leakage thoroughly and was silent on future leakage,
so reviewers checked the documented risk and stopped. **Partial coverage reading as
full coverage.**

---

## F18 — Funnel step mislabelled; drop-then-refill fabricates 157 observations

Three challenges from Brian, all substantive. Measured rather than argued.

### 1. The 196,657 → 37,999 step was attributed to the wrong cause

Documented as "drops 14,202 zero, 14,190 null, 56 negative." **Wrong.** Measured at
parent market:

| Stage | Rows |
|---|---|
| Parent market, raw | 196,657 |
| After brand/period dim join | **43,559** |
| After `sales_units > 0` | 37,999 |

**~78% of the drop is the dimension join** — fact rows whose `product_id`/`period_id`
has no dimension entry. The `> 0` filter removes only **5,560** rows (5,525 NULL, 28
negative, 7 zero). The zero/null counts previously cited (14,202 / 14,190) were
measured *before* the brand join and do not describe this step.

Funnel corrected to 6 stages: 9,080,538 → 196,657 → 43,559 → 37,999 → 3,917 → 6,160
→ 2,552.

### 2. Drop-then-refill is real for 158 brand-months — and 157 are fabricated

Brian: *"we drop rows where sales_units == 0 or NULL ... but then re-add them with
the calendar fill? How does that make sense?"*

| | Brand-months |
|---|---|
| Present in raw data | 4,075 |
| Survive `> 0` | 3,917 |
| **Lost then re-added as explicit 0** | **158** |
| Dropped SKU row had a selling sibling (no gap) | 1,249 |

~89% of drops are invisible at brand grain — the drop is at SKU grain, the refill at
brand grain, and a sibling variant usually keeps the brand-month alive. The remaining
**158 are a genuine round trip**.

**The real defect is what they were:** **157 NULL-only, 0 zero-only.** NULL = not
measured; 0 = measured, sold nothing. After calendar fill both are `0.0`.

> **157 unmeasured cells are asserted as confirmed zero sales.** 2.5% of the modelled
> frame. Not a chosen modelling assumption — an artifact of drop-then-fill ordering.

Ch10 limitation: the pipeline cannot distinguish "not measured" from "sold nothing."

### 3. "Zero/null/negative are not forecastable targets" — overstated

- **Zeros: the claim was wrong.** A zero is a real observation carrying signal
  (seasonality, decline). The `> 0` filter acts on *raw SKU rows*; the model trains on
  the calendar-filled frame where brand-month zeros are present. `filter_series` counts
  non-zero periods only to judge series *length*, not to drop zeros from training.
- **NULLs: genuinely different**, and the collapse above is the actual problem.
- **Negatives: Brian's seasonal-returns hypothesis is sound but absent here.** 28 rows
  across 9 distinct calendar months, no spike. Moot regardless — `make_calendar`
  applies `clip(lower=0)`.

**Corrected framing:** `> 0` is a **convention inherited from the SQL view**, not a
first-principles derivation. Defensible, but state it as a decision with a rationale.

### 4. SKU → brand: causality was backwards

Attributed the rollup to SKU sparsity. **The driver is the research question** — SRQ1
concerns brand-level demand forecasting for decision support; DEC-GRAIN fixes brand ×
month. Sparsity (51.5% populated at SKU) is a consequence that helps, not the reason.

Stating it backwards invites: *"so you aggregated until the data looked good?"*

All four points written into
`05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md` §2, including a
kind-of-reduction table (deduplication / integrity / convention / definitional /
completion / genuine exclusion) making explicit that **only the MIN_PERIODS step is
true attrition**.

---

## F19 — 153,098 unmapped fact rows; NULL semantics undocumented; filter justified wrongly

Brian challenged four claims from F18. All four were right to challenge; two of my
statements were wrong, one was unfounded, and one uncovered a larger problem.

### 1. ⚠️ The 196,657 → 43,559 step is NOT benign referential integrity

Labelled "unusable — no brand to attribute them to." Measured:

| | |
|---|---|
| Fact rows with `product_id` absent from `dim_product` | **153,098** |
| Distinct unmapped products | **6,306** |
| Their total sales_units | **26,142,834,849** |
| Unmapped rows with **positive** sales | **144,400** |
| `dim_product` coverage of facts' product_ids | **2,103 / 8,229 = 26%** |

Mapped and unmapped ID ranges fully overlap (unmapped 2..127,023; mapped
1..127,020), so this is not a clean category cut.

**Cause unknown.** Candidates: `dim_product` exported with a narrower filter than the
facts; facts spanning products outside CSD; incomplete dimension export.

**This is now a blocking question for Ch4's sample-size claim.** If those products are
in-scope CSD items, the study models a fraction of the available market and the
"9,080,538 → 2,552" funnel is materially misleading. Raised as task 10.

### 2. NULL semantics: unfounded assertion, retracted

Stated "NULL = not measured, 0 = measured, sold nothing" as fact. **No grounding.**
Searched `nielsen-prometheus_data_model.md` for NULL/null/missing/zero/blank/negative:
**zero matches**. It documents `sales_units` only as *"Total number of units sold"*,
examples `0.0, 22639.0`.

Brian: *"this assertion needs to be grounded in the metadata verbatim ... NULL and 0
could mean the same thing."* Correct. Notes now state it as an explicit assumption
under documented uncertainty, not a fact.

### 3. Negatives: clip to zero, framed as a choice under uncertainty

Brian: *"as we dont have the proper dataset justification from the supplier for the
logic of negative sales, we should clip it to zero and raise that limitation."*
Adopted. The metadata is equally silent on negatives. 28 rows, 9 distinct calendar
months, no seasonal spike. `clip(lower=0)` retained, documented as unjustified-by-
supplier rather than derived.

### 4. Why filter SKU rows at all — Brian right, and the real reason found

Brian: *"a 0 entry would not affect [a sum] at all, and an average would be wrongly
poisoned."* Exactly right on both halves:

| Aggregate | Effect of `> 0` filter |
|---|---|
| `sales_units` / `sales_value` / `sales_liters` (SUM) | ≤883 units / ≤12,558 / ≤1,521; **28-33 of 3,917 brand-months differ. Effectively a no-op** |
| **`weighted_dist` (MEAN)** | **1,249 of 3,917 brand-months change, max 0.19** |

The filter's real justification is **aggregation hygiene for the one averaged column**
— including non-selling variants biases a brand's mean distribution toward zero. Not
target validity, and certainly not "inherited from the SQL view," which Brian rightly
called no justification at all: *"provenance is not a reason."*

**Open design option:** filter only for the `weighted_dist` mean, retain all rows for
the sums. Would preserve the NULL/0 distinction instead of laundering it through
drop-and-refill.

### 5. "Selling sibling" clarified (Brian asked directly)

Not a mapping error — both rows carry a valid brand. A sibling is a **different
`product_id` under the same brand name in the same month**: `FAXE KONDI 1.5L PET`
records 0/NULL in March while `FAXE KONDI 0.5L` sells 40,000 that March.

**5,308 of 5,560 dropped SKU rows (95%)** have such a sibling → invisible at brand
grain. Only the remaining 252 remove a brand-month entirely, producing the 158 round
trips in F18.

### 6. SKU → brand causality: F18 had it backwards, and evasively

F18 claimed the rollup was driven purely by the research question, warning that citing
sparsity invites *"so you aggregated until the data looked good?"*

Brian rejected this: *"we actually aggregated until the data was sufficiently
non-sparse to even allow for model training ... Our research question was shaped and
changed to accommodate this sparse dataset."*

He is right, and the honest account is the stronger one. The real sequence is
**bidirectional**: the data could not support SKU-level fitting, so aggregation was a
precondition for training at all; the RQ was then framed at brand level, broad enough
to be answerable and still decision-relevant. Scope following feasibility is ordinary
applied-research practice.

It also yields a concrete Ch10 further-work claim: **finer-grained questions (SKU,
pack size, regional) require a broader and denser dataset than the one licensed here**
— a limitation of the data, not the method.

---

## F20 — Schemas differ across categories; RTD is EMPTY; shared script not viable as-is

Brian: *"A shared engineer feature script makes sense only if each dataset can be
dynamically engineered in the same fashion ... we must verify with .head() of the real
datasets."* Verified. **The premise does not hold.**

### Facts view, per category

| Category | Facts shape | Promo columns | Periods | Coverage |
|---|---|---|---|---|
| CSD | 9,080,538 × 32 | ✅ full | 44 (2022-01..) | 24.0% |
| Danskvand | 1,248,913 × **15** | ❌ **NONE** | 37 (2023-01..) | 45.0% |
| Energidrikke | 3,112,010 × 32 | ✅ (renamed) | 41 (2023-01..) | 26.6% |
| **RTD** | **0 × 0 — EMPTY FILE** | — | 37 | n/a |

### Three blockers for a single shared script

1. **RTD's facts parquet is empty** — zero rows, zero columns. P0033 cannot mirror a
   notebook to RTD; there is no data to process. This is a *missing dataset*, not a
   missing notebook. Must be re-exported or RTD dropped from scope.
2. **Danskvand has no promotional data whatsoever.** 15 columns vs CSD's 32: no
   `sales_units_any_promo`, no `baseline_*`, no `weighted_distribution_*` promo
   variants. `promo_units` / `promo_intensity` / `has_promo` are **not computable**
   for Danskvand. Not a configuration difference — the source lacks the measures.
3. **Energidrikke renames columns**: `weighted_distribution_disp_wo_feat` /
   `_feat_wo_disp` vs CSD's `_disp_w_o_feat` / `_feat_w_o_disp`. A shared script
   matching on exact names silently drops them.

Dimension views differ too: Danskvand and RTD `dim_market` carry 2 columns vs CSD's 6
(no market hierarchy); their `dim_period` carries 4 vs CSD's 9.

### What IS consistent — the shareable core

- `market_id` **1256338 = "DVH EXCL. HD" exists in all four categories** → DEC-SCOPE
  generalises unchanged.
- Join keys `market_id` / `period_id` / `product_id` are `int64` everywhere present.
- Core measures `sales_value` / `sales_in_liters` / `sales_units` /
  `weighted_distribution` exist in all three non-empty categories with identical dtypes.

### Implication — resolves the "shared vs per-notebook" question

Brian framed it as either/or: *"either we should remove the notebook specific
engineering or the shared one."* The evidence supports **neither extreme**:

- A fully shared script **cannot** work — Danskvand would need promo features that do
  not exist, and RTD has nothing at all.
- Fully per-notebook duplicates the leakage-prone logic 3-4× — exactly the multiplication
  P0036 exists to prevent (V3/V4 and the bfill fix each had to be made once, in the
  shared module, precisely because it is shared).

**Recommended: shared *core*, declared per-category capability.** Keep
`make_calendar` / `filter_series` / `engineer_features` / lag construction shared, since
those operate on the post-aggregation frame whose schema IS uniform. Make the
*aggregation* step declare which optional measure families the category has
(promo: yes/no; baseline: yes/no) and skip absent ones rather than assuming CSD's schema.

This also means **P0033's premise needs revisiting**: it assumes mirroring a CSD
template three times. Danskvand's notebook cannot carry promo features, and RTD cannot
be mirrored at all until its data is re-exported.

### dim_product coverage is systematic, not a CSD bug (task 10 input)

24.0% / 45.0% / 26.6% across CSD / Danskvand / Energidrikke. Whatever causes the
unmapped-product gap affects every category, so task 10's answer applies pipeline-wide.

---

## F21 — Task 10 RESOLVED: the 153,098 unmapped rows are Nielsen AGGREGATE rows

The `⚠️` raised in F19 is **cleared**. The `dim_product` join is not losing data — it is
the mechanism that prevents double-counting on the **product** axis, exactly as the
market filter does on the market axis.

### Evidence

| Test | Result | Reading |
|---|---|---|
| Largest unmapped "SKU" | **975,587,575 units** | **12.5× the largest real SKU** (77,781,929). No single product outsells the biggest flagship 12-fold |
| Volume concentration | top 50 ids = **82.5%** of unmapped volume; top 100 = 89.0% | Real SKU volume does not concentrate this way; rollup rows do |
| `dim_product` density in its own id range | **1.66%** (2,103 ids spanning 1..127,020) | A deliberately *filtered* whitelist, not a truncated export |
| `dim_product.category` | single value `'CSD'` | Scoped to the category on purpose |

**Conclusion: the fact table contains Nielsen's precomputed subtotals** (segment,
manufacturer, category totals) alongside individual SKUs. `dim_product` lists only
genuine SKUs. Joining to it selects real products and discards the rollups.

The alarming "96.9% of sales volume at the parent market is unmapped" is the *same
phenomenon* as the 6.16× market double-count — summing rollups together with their
constituents. Both are correctly handled by selecting one level of a hierarchy.

### `product_id` is NOT globally unique — reused across categories

| Pair | Overlapping ids | Same product? |
|---|---|---|
| CSD vs Danskvand | 40 | **No** — id 10 is `FEVER TREE` in CSD, `EGEKILDE` in Danskvand |
| CSD vs Energidrikke | 84 | **No** — id 20 is `FEVER TREE` in CSD, `COCA COLA` in Energidrikke |
| Danskvand vs Energidrikke | 84 | **No** |

**Consequence:** `product_id` is only meaningful *within* a category. Never join
product dimensions across categories, and never pool fact tables on `product_id`. Of
CSD's 6,652 unmapped ids, 495 appear in another category's dimension — those are
coincidental id reuse, not recoverable products.

This is a real trap for P0033 mirroring and for any future pooled model.

### Corrections to earlier findings

- **F19 item 1 overstated the problem.** "26.1bn units, 144,400 rows with positive
  sales — these are not malformed records" was true but drew the wrong inference: they
  are not malformed *because they are legitimate aggregates*, not because they are
  missing products.
- The funnel step `196,657 → 43,559` is **correct as implemented** and should be
  labelled **deduplication (product axis)**, alongside the market-axis deduplication —
  not "⚠️ unresolved".
- Coverage percentages (24.0% / 45.0% / 26.6% across CSD / Danskvand / Energidrikke)
  are **expected**, not defects. They vary because categories have different ratios of
  rollup rows to SKUs.

### Residual check for task 6

The one thing this does *not* prove is that **every** unmapped id is an aggregate. 89%
of unmapped volume sits in the top 100 ids; the long tail of ~6,550 low-volume ids is
unverified. If any are genuine SKUs, they are individually negligible (<0.01% of volume
each), so no result is at risk — but a Ch4 sentence should say "aggregate rows and a
negligible tail" rather than claiming all 6,652 are rollups.

---

## F22 — The Nielsen DB is LIVE and ADDITIVE; RTD was a failed pull, not missing data

Brian challenged the claim that the data is "a static snapshot, not a live feed."
**That claim was wrong.** Verified by connecting to the Fabric warehouse directly
(read-only, `SELECT MAX/MIN/COUNT` only).

### The database is live and 2-4 months ahead of our snapshot

| Category | DB newest | Our snapshot | DB fact rows | Our fact rows |
|---|---|---|---|---|
| CSD | **2026-07** | 2026-05 | 10,311,342 | 9,080,538 |
| Danskvand | **2026-07** | 2026-03 | 1,382,673 | 1,248,913 |
| Energidrikke | **2026-07** | 2026-05 | 3,476,121 | 3,112,010 |
| RTD | **2026-07** | 2026-03 | **2,409,362** | **0** |

All four now reach **2026-07** — one month before today (2026-08-12). The staleness was
**our pull being old**, not a dead database.

### RTD: the view has 2.4M rows in the DB. Our parquet is 0x0.

`rtd_clean_facts_v` = 2,409,362 rows; `rtd_clean_facts` = 9,094,805 rows. The data
exists and always did. **F20's "RTD is a missing dataset" was wrong — the pull failed
for RTD.** A re-pull fixes it; no re-export request to the supplier is needed. Task 12
rescoped accordingly.

### NOT a rolling window — additive. Re-pull is safe.

The decisive question (Brian): does the DB drop old periods as new ones arrive? **No.**

| Category | DB oldest | Our oldest | DB periods | Ours | Gain |
|---|---|---|---|---|---|
| CSD | 2022-10 | 2022-10 ✅ | **46** | 44 | +2 |
| Danskvand | 2023-03 | 2023-03 ✅ | **41** | 37 | **+4** |
| Energidrikke | 2023-01 | 2023-01 ✅ | **43** | 41 | +2 |
| RTD | 2023-03 | 2023-03 ✅ | **41** | 37 | **+4** |

Every oldest period is identical to ours, and all four period sequences are
**contiguous** (no interior gaps). History is preserved; new months append. No pipeline
change is needed to guard against data loss on refresh.

### Consequences

1. **Panel depth grows**: 44 → 46 (CSD), 37 → 41 (Danskvand, RTD), 41 → 43
   (Energidrikke). The two shortest panels gain the most (~11% each).
2. **All four align at the recent end (2026-07) for the first time**, which helps SRQ1's
   cross-category comparison. Start dates still differ, so depth stays uneven.
3. **Every measured figure in F15-F21 is superseded by the re-pull** — 44 months,
   3,917 brand-month rows, 37,999 fact rows, 2,552 matrix rows, the 140/144 brand counts.
   All were correct for the old snapshot. Task 6's parity check must re-measure.
4. **"The data cannot be refreshed" is not a valid limitation.** The refresh path exists
   and works (`save_all_datasets.py --only <CATS> --parallel`, ~3 min, views+metadata).

### Re-pull command (Brian ran this)

```
python 02_thesis_data/_00_raw/nielsen/scripts/save_all_datasets.py \
    --only CSD Danskvand Energidrikke RTD --parallel
```

Explicit `--only` excludes **Totalbeer**, which P0034 dropped on compute grounds; a bare
`--parallel` would pull it.

### Correction to the horizon argument (supersedes part of the §9 note)

I argued a "6-month forecast" was really a 21-month extrapolation because the data ended
2026-05. With data to **2026-07**, a query made in August 2026 for six months ahead is a
genuine **6-step-ahead** forecast. The horizon problem is therefore a *modelling*
question (the model is one-step-ahead — P0037 DEC-HORIZON), **not** a data-staleness
question. The recursive-error-compounding point stands; the "stale snapshot" framing
does not.

---

## F23 — Re-pull verified; three capability tiers, not two; minimum-viable set is 15 columns

Re-pull ran 2026-08-12 16:26–16:40 (Brian). Verified against the JSONL on disk, not
the manifest — **`MANIFEST.json` was NOT rewritten** (still dated 2026-06-30, CSD-only),
so it must not be used to judge a pull. File mtimes and content are the evidence.

### Period coverage — every prediction from F22 held

| Category | Periods | Oldest | Newest | Facts JSONL |
|---|---|---|---|---|
| CSD | **46** (was 44) | 2022-10 *unchanged* | **2026-07** | 10.17 GB |
| Danskvand | **41** (was 37) | 2023-03 *unchanged* | **2026-07** | 0.65 GB |
| Energidrikke | **43** (was 41) | 2023-01 *unchanged* | **2026-07** | 3.77 GB |
| RTD | **41** (was 37) | 2023-03 *unchanged* | **2026-07** | **2.51 GB** |

No oldest period moved and all sequences are contiguous — the additive/non-rolling
finding is confirmed on real data. **RTD went from an empty file to 2.51 GB / 31
columns**, closing F20's false "missing dataset" diagnosis. Totalbeer untouched
(2026-07-10), as intended by the explicit `--only`.

### Danskvand's promo gap is REAL, not a pull artifact

Still **0 promo columns**, 17 missing vs CSD (all `baseline_*` and `*_any_promo`
families). The fresh extract confirms the source genuinely lacks these measures.
**This is what locks the no-shared-module decision.**

### THREE capability tiers, not two

| Category | Cols | Promo cols | Notes |
|---|---|---|---|
| CSD | 32 | **7** | reference schema |
| Energidrikke | 32 | **7** | 2 columns renamed (`_disp_wo_feat` vs `_disp_w_o_feat`) |
| **RTD** | **31** | **6** | has baselines but **lacks `sales_units_any_promo`** |
| Danskvand | 15 | **0** | no promotional measures at all |

RTD is *not* "CSD-like" — it is a third tier. `sales_units_any_promo` is precisely the
column `promo_units` is derived from, so **RTD cannot compute `promo_units` the way CSD
does** even though it has 6 other promo columns. Any per-category adaptation must check
the specific column, not just "does this category have promo".

### MINIMUM VIABLE COMPARISON — 15 columns shared by all four

```
market_id  period_id  product_id
sales_units  sales_value  sales_in_liters
weighted_distribution  weighted_distribution_reach
numeric_distribution  numeric_distribution_reach
total_weighted_distribution_points_tdp_reach
number_of_items_reach  avg_number_of_stores_selling_reach
avg_no_of_items_per_store_reach  universe_number_of_stores
```

The target (`sales_units`) and the core distribution signal survive. Lost: the entire
promo and baseline families.

This answers Brian's two-track design question directly:

| Track | Feature basis | Cross-category comparable? | Poolable? |
|---|---|---|---|
| **Minimum viable** | the 15 shared columns | ✅ yes — genuinely "identical data" | ✅ yes, with the key fix below |
| **Optimal available** | 32 / 32 / 31 / 15 per category | ❌ no | ❌ no — absent features would join as null/0 |

The **delta between tracks measures what the promotional feature family is worth**,
which is a real SRQ1 contribution rather than a workaround for a data gap.

### Pooling requires a key fix (F21)

`product_id` is not globally unique — id 10 is `FEVER TREE` in CSD and `EGEKILDE` in
Danskvand. A pooled dataset must key on **`(category, product_id)`** or drop
`product_id` entirely. Brand names must be checked for cross-category collisions before
pooling on brand.

### Conversion is a separate step — and its command was documented wrong

JSONL → parquet does **not** happen on pull. The converter is
`run_all_conversions.py`, which lives under the **`_01_converted/`** tier, not
`_00_raw/` as the CSD notebook's Step 0 comment claimed (that hardcoded path is stale
and is being removed — paths belong in `PATHS.py`).

`--force` only overrides the mtime guard (skip when parquet is newer than JSONL). It is
**not needed** for a normal refresh: fresh JSONL is newer, so conversion triggers on its
own. Use it only after an interrupted or corrupt write.

---

## F24 — Open design question: how to split shared vs CSD-specific feature engineering

Brian, 2026-08-12, after the "delete the shared module" instruction was deferred
(task 14 — 9 live importers, deleting now breaks all four pipelines).

### The question, in his words

Two candidate designs:

**Option A — two notebook cells per category.** Move the shared code into a notebook
cell marked "shared", followed immediately by a "CSD specific" cell. Copy the shared
cell verbatim into each new category notebook and adapt only the specific cell.

**Option B — filter the CSD-specific parts OUT of the shared module.** Move only the
CSD-specific logic into the CSD notebook, leaving a genuinely-shared module behind.
Easier to adapt the shared engineering later if it needs to change.

Brian's reservation, which is the crux: *"I think the shared was worked out with a focus
on CSD anyways, so we must verify based on the list of shared variables that we can
truly dynamically have as a shared module due to dynamic decision points (e.g. if blank
= filter out, date fill for missing entries etc.)."*

### Why this is not yet answerable — what must be verified first

The module currently exposes: `aggregate_brand_month_from_db`,
`aggregate_brand_month_from_csvs` (both **dead — no live callers**, F19),
`make_calendar`, `filter_series`, `engineer_features`, `apply_split`,
`build_series_index`.

**Each function must be classified against the three capability tiers (F23)** before
either option can be chosen:

| Function | Question to answer |
|---|---|
| `make_calendar` | Grain/gap logic looks category-agnostic — but the ffill-vs-bfill decision (F16) and the NULL/zero policy (F18) are *dynamic decision points*. Are they the same choice for every category, or does Danskvand's total lack of promo change what "blank" means? |
| `filter_series` | MIN_PERIODS is a *parameter*, but is the threshold decision itself category-specific? Panel depths now differ: 46 / 43 / 41 / 41 |
| `engineer_features` | **Most likely CSD-biased.** Builds `promo_units`/`promo_intensity`/`has_promo`, which Danskvand cannot compute at all and RTD cannot compute the same way (no `sales_units_any_promo`) |
| `apply_split` | Train/val/test cutoffs are dates — differing panel start dates mean the split points cannot be shared constants |
| `build_series_index` | Probably genuinely shared; verify |

### Assessment (not a decision — Brian's call)

**Option B looks stronger**, for a reason Brian already identified in the risk noted on
task 14: the V3 and bfill leakage fixes each had to be made **once** *because* the module
was shared. Option A (copy-paste a "shared" cell four times) reinstates exactly the drift
P0027/P0029/P0030 spent real effort untangling — a future leakage fix would need applying
four times, with no mechanism to detect if one copy was missed.

Option B keeps a single point of truth for the logic that genuinely is common, and
isolates only what is provably category-specific.

**But B is only valid if the "shared" remainder is truly category-agnostic**, which is
precisely what Brian says must be verified rather than assumed. The suspicion that the
module was written CSD-first is well-founded: it was authored when CSD was the only
category with a working pipeline.

### Concrete next step (feeds task 12 / task 14)

Before choosing, produce a **function × category capability matrix**: for each of the 5
live functions, list every *dynamic decision point* inside it (missing-value policy, gap
fill, promo derivation, split dates, threshold) and mark whether that decision is the
same across CSD / Energidrikke / RTD / Danskvand.

- Decisions identical everywhere → genuinely shared, keep in the module.
- Decisions that differ → either a parameter (if the *logic* is common) or category-
  specific code (if the logic itself differs).

`engineer_features` is the one already known to differ, since promo derivation is
impossible for Danskvand and different for RTD.

**Recorded, not acted on.** Brian will decide after the matrix exists.
