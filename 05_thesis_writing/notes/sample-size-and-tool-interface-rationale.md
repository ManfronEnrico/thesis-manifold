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
| Raw facts (all markets) | 9,080,538 | every SKU × market × period |
| Scoped to `DVH EXCL. HD` parent | **37,999** | one market, positive sales only |
| Aggregated to brand × month | **3,917** | SKU → brand rollup (DEC-GRAIN) |
| Calendar-filled | **6,160** | 140 brands × 44 months, gaps included |
| MIN_PERIODS filter | 2,552 | short series dropped |

> Earlier drafts showed "196,657 → 3,975". Both were wrong: 196,657 matched no
> measured scope, and 3,975 is the *region-child* aggregate, so the funnel silently
> mixed two market scopes. Corrected above (F15).

Two separate reductions, and they should be described differently:

1. **9,080,538 → 37,999 is market scoping.** Selecting one market from 86 (and dropping
   zero-sales rows). Not attrition — the other markets are alternative views, including
   the 9 children that partition this same parent.
2. **37,999 → 3,917 is the product→brand rollup.** SKU-level observations collapse to
   brand-level; 140 brands × 44 months caps at 6,160 cells. This is **definitional, not
   attrition** — it is the unit of analysis DEC-GRAIN specifies.

Note the calendar-fill step *raises* the count (3,917 → 6,160) by inserting explicit
zero rows for months where a brand recorded no sales. Say this explicitly in Ch4; a
funnel that goes down, down, then up looks like an error otherwise.

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
