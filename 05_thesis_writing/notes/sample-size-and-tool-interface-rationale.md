---
name: sample-size-and-tool-interface-rationale
description: RULE - Why 44-month series and ~2.5k rows are adequate for this thesis, how the LLM reaches a forecast without handling feature vectors, and the three leakage defects found and fixed. Write-up material for Ch4/Ch5/Ch7/Ch10.
category: reference
applies-to: [ch4-data, ch5-design, ch6-benchmark, ch7-interface, ch8-evaluation, ch10-limitations]
triggers: [writing Ch4 data adequacy, defending sample size, describing the tool interface, writing limitations, defending leakage control, justifying market scope]
created: 2026_08_11-16_21
updated: 2026_08_11-21_55
---

# Sample Size & Tool Interface — Write-Up Rationale

Captured 2026-08-11 from an investigation session. These points are **not obvious from the
code** and will be asked at defence. Full measurements in
`plans/P0036_2026-08-11_16-08_csd-fixes-before-mirror/findings.md`.

---

## 1. The dataset facts (CSD, at DVH EXCL. HD)

> **Figures corrected 2026-08-11** against the parquet views (P0036 F15). Earlier
> values in this note were partly wrong and partly mixed two different market
> scopes. Use these.

| Quantity | Value |
|----------|-------|
| Periods available | **44 months** (hard ceiling) |
| Brands | **140** |
| Brands at all 44 months | **51** |
| Brand-month rows (>0) | **3,917** |
| Rows @ MIN_PERIODS>=24 | 3,392 (**85** brands) |
| Current feature matrix | 2,552 rows / 58 brands |
| FAXE KONDI | 44/44 months, 118,158,520 units |

**44 months is invariant.** It does not change with market scope, MIN_PERIODS, or brand
selection. Every sample-size argument below reduces to this number.

**Market scope is DEC-SCOPE: the `DVH EXCL. HD` parent (`market_id` 1256338)**, not its
9 regional children. The children were used until 2026-08-11. The switch is worth one
sentence in Ch4 because it is the reason promotional features exist at all:

| | Parent (used) | Region children (prior) |
|---|---|---|
| Nonzero promo, per column | **~23,400** | **0** |
| Distinct brands | 140 | 140 |
| Brand-month rows | 3,917 | 3,975 |
| Fact rows | 37,999 | 243,691 |

The honest framing: parent scope **costs 1.5% of brand-month rows and buys the entire
promotional feature family**. Do *not* claim it gains rows — the 9 children are a
partition of the same universe, so their fact-row count is ~6.4× inflated by repetition,
and an examiner can see that from the aggregation arithmetic.

---

## 2. Why the 9M → 2,552 funnel is not data loss

Anticipated examiner question: *"You started with 9 million rows and modelled 2,552?"*

| Stage | Rows | What happens |
|-------|------|--------------|
| Raw facts (all markets) | 9,080,538 | every SKU × market × period present |
| Scoped to `DVH EXCL. HD` parent | **196,657** | one market of 86 |
| Joined to brand + period dims | **43,559** | SKUs with no brand mapping drop out |
| Positive sales only | **37,999** | drops 5,525 NULL, 28 negative, 7 zero |
| Aggregated to brand × month | **3,917** | SKU → brand rollup (DEC-GRAIN) |
| Calendar-filled | **6,160** | 140 brands × 44 months, gaps made explicit |
| MIN_PERIODS filter | 2,552 | short series dropped |

> Two corrections (F15, F18). Earlier drafts collapsed the scoping steps and showed
> "196,657 → 3,975" — 3,975 is the *region-child* aggregate, so the funnel mixed two
> market scopes. A later draft then attributed the 196,657 → 37,999 drop to
> zero/null/negative sales; that is wrong. **~78% of that drop is the brand/period
> join** (196,657 → 43,559), not the sales filter. The `> 0` filter removes only
> 5,560 rows.

### The five reductions are five *different kinds* of operation

Conflating them is what makes the funnel look alarming. Only one is genuine loss:

| Step | Kind | Why it is defensible |
|------|------|----------------------|
| 9.08M → 196,657 | **Deduplication** | The 86 markets are overlapping *views* of one universe (channel totals, size tiers, 9 regions, EAST/WEST and national rollups). One carton sold in Copenhagen appears in the KBH row, the DVH parent, the EAST rollup, a size tier and the national total. Summing them is the 6.16× double-count P0027 found. Picking one lens is not loss |
| 196,657 → 43,559 | **Deduplication (product axis)** | Discards Nielsen's precomputed subtotal rows (segment / manufacturer / category totals), keeping only genuine SKUs. Same logic as the market step, one axis over. See below |
| 43,559 → 37,999 | **Aggregation hygiene** | 5,525 NULL, 28 negative, 7 zero at SKU grain. Near-no-op for sums; materially changes the one *averaged* column. See below |
| 37,999 → 3,917 | **Definitional** | Unit of analysis changes from SKU to brand. Nothing discarded; observations are *summed*. 1,923 SKUs → 140 brands |
| 3,917 → 6,160 | **Completion (+57%)** | Adds explicit rows for real absences. The only step that goes *up* |
| 6,160 → 2,552 | **Genuine exclusion** | Series too short to model. **The only step that is true attrition** |

### The product-dimension join is a second deduplication, not data loss (F21)

`dim_product` lists **2,103 of the 8,229 `product_id`s** in the facts (26%). At first
reading that looks alarming — the unmapped rows carry **96.9% of sales volume at the
modelled market**. Investigated, and the explanation is the same one that justifies the
market filter:

**The fact table contains Nielsen's precomputed subtotals alongside individual SKUs.**
`dim_product` is a whitelist of genuine products; joining to it discards the rollups.

| Test | Result |
|---|---|
| Largest "unmapped SKU" | **975,587,575 units — 12.5× the largest real SKU** (77.8M) |
| Volume concentration | top 50 unmapped ids = **82.5%** of unmapped volume |
| `dim_product` density in its id range | **1.66%** — a filtered whitelist, not a truncated export |
| `dim_product.category` | single value `'CSD'` |

No individual product outsells the biggest brand's flagship twelvefold, and real SKU
volume does not concentrate into 50 ids. These are segment, manufacturer and category
totals.

**So the funnel has two deduplication steps, on two axes:** the market filter removes
rollups across geography/channel; the product join removes rollups across the product
hierarchy. Both prevent the same error — summing a total together with its parts.
This is the 6.16× double-count pattern P0027 found, in a second guise.

**Ch4 phrasing:** *"aggregate rows and a negligible unverified tail"* — 89% of unmapped
volume sits in the top 100 ids; the remaining ~6,550 low-volume ids were not
individually inspected, but each is <0.01% of volume, so no result depends on them.

### ⚠️ `product_id` is NOT globally unique — never pool across categories

| Pair | Overlapping ids | Same product? |
|---|---|---|
| CSD vs Danskvand | 40 | **No** — id 10 = `FEVER TREE` (CSD) / `EGEKILDE` (Danskvand) |
| CSD vs Energidrikke | 84 | **No** — id 20 = `FEVER TREE` (CSD) / `COCA COLA` (Energidrikke) |
| Danskvand vs Energidrikke | 84 | **No** |

`product_id` is meaningful only **within** a category. Never join product dimensions
across categories and never pool fact tables on `product_id` — a trap for any
cross-category or pooled model.

### Why brand, not SKU — two honest reasons, in order

An earlier draft claimed the rollup was driven *purely* by the research question, and
warned that citing sparsity invites *"so you aggregated until the data looked good?"*
**Brian rejected that framing, correctly**: it is evasive, and the honest account is
stronger.

The real sequence was **bidirectional**, and should be written as such:

1. **The data could not support SKU-level forecasting.** At SKU grain the panel is
   51.5% populated and most SKUs have too few periods to fit. Brand-level aggregation
   was a *precondition for training a model at all*.
2. **The research question was then shaped to match.** SRQ1 was framed at brand-level
   demand — broad enough to be answerable with the available data, and still
   decision-relevant, since the System B user asks "how will Faxe Kondi sell next
   month," not about the 1.5L PET variant.

This is ordinary applied-research practice: scope follows feasibility. Stating it
plainly is more defensible than implying the grain was chosen on purity grounds and
the sparsity fit was a happy accident. It also sets up a **concrete further-work
claim** for Ch10: *finer-grained questions (SKU, pack size, regional) require a
broader and denser dataset than the one licensed here* — which is a limitation of the
data, not of the method.

### Caveat: drop-then-refill, and the NULL/zero collapse (measured, F18)

The pipeline drops rows at SKU grain, then re-adds brand-months as explicit zeros
during calendar fill. That sounds circular; measured, it mostly is not — but where it
is, it fabricates observations:

| | Count |
|---|---|
| Brand-months present in raw data | 4,075 |
| Brand-months surviving the `> 0` filter | 3,917 |
| **Brand-months lost, then re-added as explicit 0** | **158** |
| Dropped SKU rows | 5,560 |
| ...where a **sibling SKU** of the same brand sold that month | **5,308 (95%)** |
| ...where no sibling sold (→ the lost brand-months) | 252 |

**"Sibling" = a different `product_id` under the same brand name, same month.** It is
*not* a mapping error: both rows carry a valid brand. Concretely — `FAXE KONDI 1.5L
PET` records 0 or NULL units in March while `FAXE KONDI 0.5L` sells 40,000 that same
March. Dropping the first changes nothing, because the brand-month survives on the
second and the sum is unaffected.

95% of dropped SKU rows are that case: **invisible at brand grain**. Only the 252 rows
where *no* variant sold remove a brand-month entirely, producing the 158 round trips.

Of those 158, **157 were NULL-only** and **none were zero-only**. After calendar fill
they are written as `0.0`.

### What NULL means: unknown, and the metadata does not say

**Do not claim NULL means "not measured."** The supplier metadata
(`02_thesis_data/_00_raw/nielsen/description/nielsen-prometheus_data_model.md`) was
searched for `NULL` / `null` / `missing` / `zero` / `blank` / `negative`: **zero
matches**. It documents `sales_units` only as *"Total number of units sold"* with
example values `0.0, 22639.0`. **There is no documented null semantics.**

So NULL could mean not-measured, not-stocked, a suppressed low-volume cell, or a
data-entry artifact — and it could mean the same thing as `0`. **We cannot tell.**

Write it as a stated assumption, not a fact:

> Nielsen's data model does not document the semantics of missing values. Absent
> supplier guidance, unmeasured and zero-valued cells are treated identically
> (as zero units sold) for modelling. Whether NULL and 0 encode distinct real-world
> states in the source system is unknown, and if they do, the pipeline does not
> preserve that distinction.

That is honest, checkable, and does not overclaim. **157 cells (2.5% of the modelled
frame)** are affected — small, but the assumption should be visible rather than buried.

### Negatives: clip to zero, and state it as an unjustified choice

Returns/corrections could carry signal (e.g. post-campaign returns clustering). Two
findings:

- **No seasonal pattern here.** 28 negative rows spread across 9 distinct calendar
  months, no spike. The hypothesis is sound in general; this data does not exhibit it.
- **The metadata does not explain negatives either.** Same search, no matches.

`make_calendar` applies `clip(lower=0)`, so negatives become 0 regardless of the
filter. **Keep that**, because without supplier documentation there is no principled
alternative — but record it as a choice made under uncertainty, not a derivation.

Ch10 sentence: *negative sales values, presumed accounting corrections but not
documented as such by the supplier, are clipped to zero; returns dynamics and
zero-inflation are therefore outside the modelled target.*

### Why filter SKU rows at all, if brands are summed?

Brian's challenge: a `0` row contributes nothing to a `SUM`, so why filter? **Measured
— he is right for the sums, and the real reason is elsewhere.**

| Aggregate | Effect of the `> 0` filter |
|---|---|
| `sales_units` (sum) | max diff **883 units** across 3,917 brand-months, 28 rows differ |
| `sales_value` (sum) | max diff 12,558, 33 rows differ |
| `sales_liters` (sum) | max diff 1,521, 28 rows differ |
| **`weighted_dist` (MEAN)** | **1,249 of 3,917 brand-months change, up to 0.19** |

For sums the filter is effectively a **no-op** — as predicted. Its real effect is on
`weighted_dist`, the one column aggregated with `.mean()`: including zero/NULL SKU rows
**drags the average distribution down**, exactly the "averages would be wrongly
poisoned" concern.

So the correct justification is **aggregation hygiene for the averaged column**, not
target validity:

> SKU rows without positive sales are excluded before aggregation. For summed
> measures this is immaterial. It matters for `weighted_distribution`, which is
> averaged across SKUs: including non-selling variants would bias a brand's mean
> distribution toward zero.

The previous justification — "a convention inherited from the SQL view" — was
correctly rejected by Brian as no justification at all. Provenance is not a reason.

Its **second** effect is the 158 brand-months above: dropping every SKU row for a
brand-month removes the brand-month entirely, which the calendar fill then re-creates
as a zero. **Alternative worth considering:** filter only for the `weighted_dist` mean
and retain all rows for the sums. This would preserve the NULL/0 distinction rather
than laundering it through drop-and-refill.

---

## 3. Why pooled training helps a single-brand forecast

Anticipated question — and one that is genuinely counter-intuitive: *"If you only ever ask
about Faxe Kondi, and Faxe Kondi only has 44 months, why train on 85 brands?"*

**The model does not learn "Faxe Kondi's history." It learns a function:**

```
(lag_1, lag_2, lag_12, month, weighted_dist, promo_intensity, …) → next month's units
```

That function has ~30 parameters. Faxe Kondi supplies 44 examples of the mapping; the
other 84 brands supply ~3,350 more examples **of the same mapping**. December behaves like
December for Coca Cola, Pepsi and Harboe too; "sales dipped last month and distribution is
falling → expect a further dip" is a property of Danish CSD demand, not of one brand.

At prediction time the model is fed **Faxe Kondi's own 44 rows** of lag values. The
prediction is driven entirely by Faxe Kondi's data. Pooling buys a *better-estimated
function* to apply to it. Fitting 30 parameters on 44 observations memorises noise;
fitting them on 3,392 estimates the real seasonal and autoregressive structure.

**Honest boundary:** pooling helps with *shared* structure (seasonality, promo response,
autoregressive decay). It cannot recover brand-specific idiosyncrasy — for that, 44 points
is all the evidence that exists. State this in Ch10.

### Single-brand training was considered and rejected on measurement

| | Pooled (MIN_PERIODS>=24) | Single best brand |
|---|---|---|
| Training rows | **3,392** | **44** |

Selecting the highest-data brand yields **no additional data** — 51 brands already sit at
the 44-month ceiling. MIN_PERIODS filters *series length*, so discarding brands cannot
lengthen the survivor. 44 rows × ~30 features is more features than observations
(unfittable for XGBoost/LightGBM). ~12 test points also destroys the statistical power
SRQ4 depends on.

**Design rule: separate training scope from evaluation scope.** Train pooled across
surviving brands (a global forecasting model — standard practice); demo and evaluate on
Faxe Kondi. Delivers the single-brand demo *and* keeps the power.

---

## 4. Sample-size adequacy by model class

| Model class | Verdict |
|-------------|---------|
| Statistical per-brand (ARIMA/ETS/Prophet) | Thin but defensible — ~3.5 seasonal cycles; 12 seasonal lags on 44 points is tight. **Declare as a limitation.** |
| Classical ML pooled (LightGBM/XGBoost/Ridge) | Adequate at 2,552–3,392 rows × ~30 features. **Must pool.** |
| Deep learning from scratch | **Not viable** — and already excluded on RAM grounds, so no conflict. |
| Pre-trained / foundation models (Chronos, TimesFM, Moirai) | Well-suited; zero-shot on short series is their target regime. |

**Framing for Ch4/Ch10:** a low-data regime is the *condition that makes the research
question meaningful*, not a defect. The thesis asks whether lightweight/pre-trained
approaches beat training from scratch under constraints. A dataset large enough to train
deep models from scratch would weaken the framing. State it as a deliberate design
property — do not apologise for it.

---

## 5. Sample size per SRQ — they are not the same n

**This is the key distinction.** Different SRQs have different evaluation units, and
conflating them makes the thesis look weaker than it is.

| SRQ | Evaluation unit | Effective n | Exposure to the 44-month limit |
|-----|-----------------|-------------|-------------------------------|
| **SRQ1** (models & efficiency) | Forecast accuracy on held-out months | ~12 test months/brand × brands × 4 categories | **Directly exposed** |
| **SRQ2** (tool interface) | Interface design artefact | n/a — design contribution | None |
| **SRQ3** (integration readiness) | Capability assessment | n/a — assessment | None |
| **SRQ4** (ML vs code-as-action LLM) | **Prompts** | **~50 prompt set** | **Largely insulated** |

### SRQ1 — the one arm that does inherit the limitation

SRQ1 is a genuine forecasting-accuracy claim and must be defended as such. Two mitigations:

1. The comparison is **between models on identical data** (Ridge/ARIMA/Prophet/LightGBM/
   XGBoost). Relative ranking under identical conditions is more robust at small n than an
   absolute accuracy claim. Pair with **Diebold-Mariano** significance testing (already in
   the System A spec).
2. "Category specialization" runs the comparison across **all four categories**, multiplying
   the evidence base beyond any single category's test points.

### SRQ4 — insulated by design

Per RQ v4 (2026-06-17), SRQ4's metrics are **correctness, consistency, replicability**
(primary) + **cost, latency** (secondary), over a **~50-prompt set**, against a
**code-as-action LLM** baseline.

*Consistency* and *replicability* barely depend on forecast accuracy — they measure whether
the system returns the same answer twice. A trained model does so deterministically; an LLM
writing fresh forecasting code each time may not. **That result is unthreatened by the
44-month panel**, and is plausibly the strongest finding available.

---

## 6. How the LLM reaches a forecast (SRQ2 mechanics)

Anticipated question: *"The user asks a natural-language question — how does the LLM get
44 rows of lag values?"*

**It does not, and must not.** Having the LLM assemble feature vectors would be fragile and
would defeat the traceability requirement.

```
User: "What will Faxe Kondi sales be in 4 months?"
   │
   ▼  LLM decomposes intent → typed tool call (NOT feature vectors)
{"tool": "forecast_demand", "brand": "FAXE KONDI", "horizon_months": 4}
   │
   ▼  Forecast service, server-side:
      • looks up FAXE KONDI history from the feature matrix
      • constructs lag / rolling / calendar features itself
      • runs the trained model
   │
   ▼  Returns typed, calibrated output
{"point_forecast": 2847000, "lower_90": 2510000, "upper_90": 3184000,
 "confidence": 78, "source_model": "LightGBM",
 "data_window": "2022-04..2025-11"}
   │
   ▼  LLM renders structured output → natural language
```

**The LLM's responsibility is exactly two translations:** intent → parameters, and
structured output → prose. It never sees a lag value. Feature construction stays
server-side, where it is versioned, testable and identical on every call.

This *is* the SRQ2 contribution — "a typed, structured tool call, not raw model output,"
carrying point forecast, calibrated 90% interval, confidence score, source attribution and
traceability metadata.

**Why this is also the SRQ4 advantage:** the code-as-action baseline must load data and
construct features itself on every invocation, with no guarantee of doing it identically
twice. That is precisely the *consistency* and *replicability* axis SRQ4 measures — the
tool interface's determinism is not incidental, it is the hypothesised mechanism of
improvement.

---

## 7. Leakage control — three defects found and fixed (Ch4 + Ch10)

**This is a methodological strength worth claiming explicitly, not an embarrassment to
bury.** Three distinct target-leakage defects were found by audit and fixed before any
reported result. Each is a different *kind* of leakage, which is what makes the set
worth a paragraph in Ch4 and a limitations note in Ch10.

| # | Defect | Kind | Why it is leakage |
|---|--------|------|-------------------|
| V3 | `promo_intensity` computed from `sales_units_t` | **Target leakage** | The target's own denominator. Unconstructible at forecast time — you cannot know this month's units before forecasting them |
| — | bare `shift(1)` on a frame sorted by (brand, date) | **Cross-series leakage** | Carries the last row of brand A into the first row of brand B. Fixed with `groupby(group_keys).shift(1)` |
| — | `make_calendar` chained `.ffill().bfill()` | **Future leakage within a series** | `bfill` fills *leading* gaps — months before a brand's first observation — with its first observed value, i.e. a fact from the future |

### Why gap-filling is needed at all (state this before the bfill example)

Nielsen's fact table is **sparse**: at the parent market the SKU × month grid is only
**51.5% populated** (1,923 SKUs × 44 months = 84,612 possible; 43,559 present). Most
absent cells are products not tracked that month. Nielsen *does* also emit explicit
zeros and nulls (14,202 and 14,190 rows at parent scope), so absence and zero are not
interchangeable — but roughly half the grid is simply missing.

The model needs an evenly-spaced series per brand, so the pipeline builds the full
140 × 44 calendar and fills the holes. **Sales** gaps fill with 0 (no recorded sales
= none sold). **Distribution** gaps are where the leakage crept in.

### The bfill case, with numbers (good Ch4 example)

Measured on CSD at parent scope: the `bfill` contaminated **1,176 rows — 19.1% of the
calendar — across 51 of 140 brands**, and **100% of affected rows were leading gaps**,
which is the diagnostic signature of future leakage.

Worked example, brand `SPIRIT OF SWEDEN`:

| Month | Sales | Raw dist | With `bfill` (old) | `ffill` only (fixed) |
|-------|-------|----------|--------------------|----------------------|
| 2023-04 | 0 | — | **0.157** | 0.000 |
| 2023-05 | 0 | — | **0.157** | 0.000 |
| 2023-06 | 0 | — | **0.157** | 0.000 |
| 2023-07 | 0 | — | **0.157** | 0.000 |
| 2023-08 | 35,819 | 0.157 | 0.157 | 0.157 |

Four months before the brand existed in distribution carried a value first observed in
August. Fixed: leading gaps fill `0`, which is also the *truthful* value — the brand was
not distributed. Trailing gaps still `ffill`, which is legitimate because it uses only
past information.

**The magnitude was small (max 0.157) but that is not the argument.** Frame it as
correctness, not effect size: a feature that cannot be constructed at forecast time
invalidates the evaluation regardless of how much it moves the metric. An examiner who
finds this unfixed will discount every number in Ch6; an examiner who sees it found,
measured and fixed reads it as evidence of a controlled pipeline.

### Why these survived earlier review — the transferable lesson

The `make_calendar` docstring documented the *cross-series* risk carefully and was
**silent on future leakage**. Reviewers checked the documented risk and moved on. The
docstring now names both, with the reasoning for each.

Generalisable point for Ch10: **documenting one failure mode can create false assurance
about a neighbouring one.** Leakage audits should enumerate leakage *kinds*
(target / cross-series / future / train-test contamination), not spot-check individual
lines.

### Related structural safeguard

The same audit added a **market fan-out guard**: a `market_description` join resolving to
more than one `market_id` silently multiplies every `SUM()`. This produced a 6.16×
double-count in an earlier iteration (P0027). The pipeline now asserts exactly one market
survives filtering — `== 1`, not `> 0`, because `> 0` passes the fan-out case unchanged.

---

## Related

- `plans/P0036_2026-08-11_16-08_csd-fixes-before-mirror/findings.md` — F3–F7, measurements
- `01_thesis_research/research-questions/research-questions.md` — RQ v4 (canonical)
- `00_thesis_context/thesis-topic/project-overview.md` — ⚠️ SUPERSEDED (v2 RQs) + has an
  unresolved merge conflict at lines 2–8

---

## 8. Cross-category asymmetry — the four datasets are not equivalent (Ch4 + Ch6 + Ch10)

Verified 2026-08-11 against the parquet views (F20). **SRQ1 compares model ranking "on
identical data." The data is not identical, and one category has none.**

| Category | Facts rows | Cols | Promo measures | Periods | From |
|---|---|---|---|---|---|
| CSD | 9,080,538 | 32 | ✅ full | **44** | 2022-01 |
| Danskvand | 1,248,913 | **15** | ❌ **none** | 37 | 2023-01 |
| Energidrikke | 3,112,010 | 32 | ✅ (renamed) | 41 | 2023-01 |
| **RTD** | **0** | **0** | — | 37 | — |

Three facts that must reach the write-up:

1. **RTD's fact table is empty.** Not "not yet processed" — the parquet is 0×0. Either
   it is re-exported or RTD leaves scope. Any claim of *four* categories is currently
   unsupported for one of them.
2. **Danskvand has no promotional data at all.** Not a config gap: the source lacks the
   measures. `promo_units` / `promo_intensity` / `has_promo` cannot exist there. So a
   cross-category model comparison either drops promo features everywhere (weakening
   CSD and Energidrikke) or compares models on **different feature sets** — which
   changes what SRQ1's "relative model ranking on identical data" can claim.
3. **Panel depth differs**: 44 / 41 / 37 months. Any "44 months" statement is
   CSD-specific.

**What is consistent, and worth stating positively:** `market_id 1256338` (`DVH EXCL.
HD`) exists in all four categories, so DEC-SCOPE is not a CSD-only choice; and the join
keys plus core measures (`sales_units`, `sales_value`, `sales_in_liters`,
`weighted_distribution`) are identical in name and dtype wherever present.

**Ch6 framing:** report per-category feature availability in the results table rather
than implying a uniform design. **Ch10:** the promotional-feature asymmetry limits
cross-category generalisation of any promo-driven finding.

---

## 9. Product-range features — recoverable signal, and the deployment problem (Ch4/Ch5/Ch10)

`dim_product` carries 20+ attributes (manufacturer, packaging, size_variants, variant,
subbrand, organic, private_label, price_category…). The brand-month rollup currently
keeps **two**: `product_id` and `brand`. Everything else is discarded rather than
aggregated.

Raw SKU attributes genuinely cannot survive the rollup — FAXE KONDI spans 7 sizes and 3
packaging types across 144 SKUs, so there is no single "the size" for a brand-month.
But **brand-month aggregates of them can**, and they carry signal:

| Candidate feature | r with `sales_units` |
|---|---|
| **`n_skus_active`** (distinct products on shelf that month) | **0.848** |
| `n_sizes` | 0.658 |
| `n_packaging` | 0.469 |
| *(existing `weighted_dist`)* | *0.756* |
| *(existing `lag_1`)* | *0.585* |

`n_skus_active` outperforms every current feature. It measures range expansion and
delisting — a real commercial dynamic the model is presently blind to.

**Two caveats before claiming this** (task 11): it may be a size proxy (large brands
have more SKUs *and* more sales — needs a **within-brand** correlation), and it requires
`shift(1)` like `promo_intensity`, since the current month's SKU count is not known when
forecasting the current month.

### The deployment question (raised by Brian) — and why it is an SRQ2 opportunity

*"It is unrealistic that a marketing manager knows or voices the listings by heart."*
Correct — but the feature does not need to be user-supplied. `n_skus_active` is a
property of **the brand's own history**, already in the feature matrix, so the forecast
service derives it server-side exactly as it derives `lag_1`. This is the same
separation described in §6: the LLM never handles feature vectors.

Three tiers:

| Tier | When | Source |
|---|---|---|
| 1. **Auto-derive** (default) | Always | Last known value from history, like the lags |
| 2. **User override** (optional) | Manager *does* know a planned change | Optional typed tool parameter |
| 3. **Training average** | Cold-start brand only | Category mean |

Tier 2 converts a limitation into a **capability**: *"what happens to Faxe Kondi if we
delist the 1.5L?"* is precisely the forecast-informed decision support the main RQ
describes, and it is only expressible because feature construction is server-side and
typed.

**Honest limitation for Ch10:** at a 6-month horizon the auto-derived value is the last
observed SKU count carried forward six months, and its accuracy degrades with horizon.
Options: hold constant and document, forecast it as a secondary series, or restrict it
to short horizons. Measure the degradation before choosing — this is a real constraint
on long-horizon queries regardless of which option is taken.
