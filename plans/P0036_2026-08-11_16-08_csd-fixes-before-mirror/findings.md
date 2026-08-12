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
