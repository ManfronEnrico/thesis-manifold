---
name: sample-size-and-tool-interface-rationale
description: RULE - Why 44-month series and ~2.5k rows are adequate for this thesis, and how the LLM reaches a forecast without handling feature vectors. Write-up material for Ch4/Ch5/Ch7/Ch10.
category: reference
applies-to: [ch4-data, ch5-design, ch6-benchmark, ch7-interface, ch8-evaluation, ch10-limitations]
triggers: [writing Ch4 data adequacy, defending sample size, describing the tool interface, writing limitations]
created: 2026_08_11-16_21
updated: 2026_08_11-16_21
---

# Sample Size & Tool Interface — Write-Up Rationale

Captured 2026-08-11 from an investigation session. These points are **not obvious from the
code** and will be asked at defence. Full measurements in
`plans/P0036_2026-08-11_16-08_csd-fixes-before-mirror/findings.md`.

---

## 1. The dataset facts (CSD, at DVH EXCL. HD)

| Quantity | Value |
|----------|-------|
| Periods available | **44 months** (hard ceiling) |
| Brands | 144 |
| Brands at all 44 months | **51** |
| Brand-month rows (>0) | 3,917 |
| Rows @ MIN_PERIODS>=24 | 3,392 (85 brands) |
| Current feature matrix | 2,552 rows / 58 brands |
| FAXE KONDI | 44/44 months, 118M units, 4th by volume |

**44 months is invariant.** It does not change with market scope, MIN_PERIODS, or brand
selection. Every sample-size argument below reduces to this number.

---

## 2. Why the 196k → 2,552 funnel is not data loss

Anticipated examiner question: *"You started with 9 million rows and modelled 2,552?"*

| Stage | Rows |
|-------|------|
| Raw facts (all markets) | 9,080,538 |
| Scoped to DVH EXCL. HD | 196,657 |
| Aggregated to brand × month | 3,975 |
| Calendar-filled | 6,160 |
| MIN_PERIODS filter | 2,552 |

The large drop is the **product→brand rollup**. 196k rows are SKU-level observations;
144 brands × 44 months caps at ~6,336 cells. The reduction is **definitional, not
attrition** — it is the unit of analysis DEC-GRAIN specifies. Say this explicitly in Ch4;
it looks alarming otherwise.

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

## Related

- `plans/P0036_2026-08-11_16-08_csd-fixes-before-mirror/findings.md` — F3–F7, measurements
- `01_thesis_research/research-questions/research-questions.md` — RQ v4 (canonical)
- `00_thesis_context/thesis-topic/project-overview.md` — ⚠️ SUPERSEDED (v2 RQs) + has an
  unresolved merge conflict at lines 2–8
