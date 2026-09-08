---
name: srq1-holiday-enrichment-result-and-limitations
description: NOTE - Task 12 write-up for the Danish public-holiday enrichment. Bullet skeleton plus approved prose paragraphs for pasting into the .docx. Covers the split result, the SHAP redistribution test, the reproducibility finding, and five limitations.
category: reference
applies-to: [ch4 §4.3, ch6 §6.3.3, ch6 §6.5, ch9 §9.4, ch9 §9.5]
triggers: [writing up the holiday enrichment, answering the exogenous-data Word threads, reporting SRQ1 feature results]
created: 2026_09_07-10_30
updated: 2026_09_07-15_30
---

# Holiday enrichment — result, limitations, future work

**Prose in this file is exceptional and explicitly approved** (2026-09-07) for pasting
into the OneDrive `.docx`. Per `writing-surface-authority`, the `.docx` remains the
authoritative home: once pasted, edit it there, not here. This file then reverts to
being a bullet/provenance record.

**Every number below is read from a result file.** Sources: appendix tables 94 and 96;
`holiday_ablation_tuned_delta.csv`; plan P0047 findings F16, F18.

---

## PART 1 — BULLET SKELETON

### 1.1 What was built

- Danish public-holiday calendar pulled from the Nager.Date v3 public API, per year,
  cached to `_00_raw/holidays/` with a manifest recording fetch timestamp and SHA-256.
- Three features engineered at brand × month grain: `days_in_month`, `n_holidays`,
  `non_holiday_days` (= `days_in_month` − `n_holidays`).
- Named `non_holiday_days`, **not** `selling_days` or `trading_days`: Danish retail
  trades at weekends and many stores open on public holidays with reduced hours, so this
  is not a count of days on which selling happened. *(Statute name and year unverified —
  see CV-03.)*
- Fetch is wired into the Nielsen refetch **and** available standalone, because a full
  Nielsen re-pull is slow.
- If the API is unavailable the pipeline does not silently substitute: step 3 records
  `holiday_enrichment: false` in the contract and step 4 hard-fails if a contract
  promised enrichment it cannot supply. An unenriched run is *declared*, never quiet.

### 1.2 The headline result — report the split, never the mean

- Helped in **7 of 12** category × model cells; mean **−1.42 pp** WMAPE.
- **Do not quote that mean.** It averages across model families that behave differently,
  and that difference is itself the finding.

| Model | helped | mean Δ | range |
|---|---|---|---|
| Ridge | 3/4 | −2.49 pp | −8.97 … +0.95 |
| LightGBM | 3/4 | −2.45 pp | −5.36 … +0.10 |
| XGBoost | **1/4** | **+0.68 pp** | −0.14 … +1.73 |

| Category | helped | mean Δ |
|---|---|---|
| RTD | 3/3 | −4.82 pp |
| danskvand | 2/3 | −1.27 pp |
| energidrikke | 2/3 | −0.51 pp |
| CSD | **0/3** | **+0.93 pp** |

- Largest single gain: **RTD Ridge, −8.97 pp** (56.30 → 47.33).
- CSD is the only category harmed in every cell — and it is the largest and
  best-predicted category, where the models were already strongest.

### 1.3 The calendar is not a re-encoding of month

- Objection to pre-empt: `month`, `quarter` and `peak_month` are already features, and
  Christmas is always December — so a WMAPE gain alone does not prove new information.
- Test: SHAP attribution before vs after. Pure redistribution would show existing
  calendar features losing what the holiday features gain.
- Result — holiday gain vs calendar loss (% of total attribution, LightGBM):

| Category | holiday features gain | existing calendar loses | net |
|---|---|---|---|
| CSD | 2.37 | 0.60 | **+1.77** |
| RTD | 2.31 | 1.00 | **+1.31** |
| danskvand | 1.21 | 0.26 | **+0.95** |
| energidrikke | 1.88 | −0.36 *(gains)* | **+2.24** |

- New information in all four categories. In energidrikke the existing calendar
  features *gain* attribution, which redistribution cannot produce.
- Strongest substantive argument: **Store Bededag was abolished from 2024**, dropping
  the count 15 → 14 permanently, mid-panel. A structural break `month` cannot represent.
  *(Effect visible in the data, table 91; legislative reference unverified — CV-05.)*

### 1.4 The reproducibility finding (methods contribution)

- Found while regenerating: re-running the benchmark moved **XGBoost rows only** — 4 of
  4 — while all 12 non-XGBoost rows were byte-identical.
- Cause: `n_jobs=-1`. Holding seed, data and hyperparameters fixed and varying only
  thread count: **34.65 / 34.95 / 35.40 / 37.30** WMAPE at 1 / 2 / 4 / 8 threads.
  A **2.65 pp** spread from thread count alone. *(Effect measured; mechanism unverified
  — CV-04.)*
- `random_state` fixes the sampling draw, not the order of a parallel reduction.
- **The spread is larger than most of the holiday effects reported here** — so before
  the fix, a reader on a different machine could not reproduce the sign of several
  findings.
- Two conclusions did not survive: RTD's best model flipped XGBoost → LightGBM (old
  margin 0.43 pp), and 3 of 12 ablation cells changed sign.
- Fixed to `n_jobs=1` for all accuracy measurement. Deliberately **not** applied to
  resource profiling, where multi-core execution is the quantity being measured and the
  core count is reported alongside.

### 1.5 Limitations

1. **External dependency.** Results depend on a third-party API. Mitigated by caching
   with timestamp and hash, but a future re-run may fetch a revised calendar.
2. **`non_holiday_days` is a proxy.** It does not observe opening hours, only the
   absence of a public holiday.
3. **Monthly grain.** A holiday shifts demand across days within a month; monthly
   aggregation absorbs much of that. A null here is not evidence of no holiday effect —
   it is evidence of none *surviving monthly aggregation*.
4. **School holidays excluded** — no free, reliable, municipality-level source found.
   Danish school holidays vary by municipality, so a national approximation would
   introduce error of unknown sign.
5. **Determinism cost.** Single-threaded XGBoost is slower. Acceptable because accuracy
   runs are not latency-bound; noted because it affects re-run time.

### 1.6 Future work

- Weather (temperature especially, for beverages) — plausibly the strongest omitted
  variable.
- Macroeconomic indicators: consumer confidence, disposable income.
- Municipality-level school holidays if a source becomes available.
- Sub-monthly grain, which would let holiday timing act rather than only holiday count.

---

## PART 2 — PROSE, WITH EXACT INSERTION POINTS

**Snapshot this is written against:** `2026-09-07_14-29_holiday-enrichment`.
Re-verify anchors if the `.docx` has been edited since.

**How to read each block:**

- **Anchor** — the exact existing sentence to search for in Word.
- **Action** — REPLACE / INSERT AFTER / APPEND / EDIT-THEN-INSERT.
- **Assets** — what to cite in-text vs. send to the appendix.

---

### P1 — Ch4 §4.3 Feature Engineering (forecasting substrate)

> **File:** `chapters/sections/08-ch4-data-assessment/03-feature-engineering-forecasting-substrate.md`
> **Word comment 177 is anchored on this exact sentence** — your own note,
> *"VERIFY & UPDATE: As we are thinking about including exogenous features (holiday calendar)"*.
> Doing this closes 177.

**⚠ EDIT-THEN-INSERT — the existing counts are wrong and must change first.**

**Anchor (opening sentence of the section):**
> "The feature matrix contains 22 columns: **14 modelling features** per observation, plus index/key columns, the target, the carried promo_units, and the split label"

**Action A — amend the count.** The three holiday features are modelling inputs, so
`14 → 17`. **Do not touch "22 columns" in the same pass** — see the ⚠ discrepancy note
at the end of this block; that number is separately wrong and needs its own check.

**Action B — add a row to Table 4** (Feature Engineering Overview), after the
`month, quarter, peak_month` calendar row:

| Feature | Description | Models |
|---|---|---|
| days_in_month, n_holidays, non_holiday_days | Danish public-holiday calendar (Nager.Date); non_holiday_days = days_in_month − n_holidays | LightGBM, XGBoost, Ridge |

**Action C — INSERT AFTER the paragraph ending** "...only its derived "promo_intensity" is)."
→ paste §2.1 prose below.

**Assets:**
- **In-text:** Table 4 (amended, above).
- **Appendix, cite don't inline:** Table 90 (source provenance), Table 93 (feature
  definitions).
- **No new figure needed.**

---

### P2 — Ch6 §6.5 Results — NEW subsection after §6.5.1

> **File:** `chapters/sections/10-ch6-model-benchmark/05-results/01-tabular-model-benchmark.md`
> **Action:** INSERT a new subsection immediately **after** §6.5.1 "Tabular-model
> benchmark" ends (after the paragraph beginning "**Validation-to-test movement is
> substantial...**") and **before** §6.5.2 "The simple benchmarks, and where they win".

**Suggested heading:** `Holiday enrichment: does an exogenous calendar help?`

Paste §2.2 then §2.3 prose below as one subsection.

**Assets:**
- **In-text — insert as a new numbered table** (will become Table 14; renumber the
  existing 14+ onward). Use the per-model / per-category split, **not** the 12-row grid:

| Model | Helped | Mean Δ WMAPE | Range |
|---|---|---|---|
| Ridge | 3 of 4 | −2.49 pp | −8.97 … +0.95 |
| LightGBM | 3 of 4 | −2.45 pp | −5.36 … +0.10 |
| XGBoost | 1 of 4 | +0.68 pp | −0.14 … +1.73 |

- **Appendix, cite don't inline:** Table 94 (full 12-cell grid — too wide for the body),
  Table 96 (SHAP attribution), Table 91 (annual counts, the Store Bededag evidence),
  Table 92 (monthly matrix).
- **Figure:** none required. If one is wanted later, a diverging bar of the 12 deltas
  grouped by model would carry §2.2's argument — but the table above already does.

---

### P3 — Ch6 §6.3 Experimental setup — the determinism finding

> **File:** `chapters/sections/10-ch6-model-benchmark/03-experimental-setup/03-execution-protocol.md`
> **Action:** APPEND to the end of §6.3.3 "Execution protocol".

Paste §2.4 prose below.

**Why here, not Ch9.** This is a property of *how the experiments were run*, so it
belongs with the protocol that governs every number in Ch6. Ch9 §9.4 gets only the
one-line limitation (P5).

**Assets:**
- **In-text — small table**, the core evidence:

| XGBoost threads | Test WMAPE (danskvand) |
|---|---|
| 1 | 34.65 % |
| 2 | 34.95 % |
| 4 | 35.40 % |
| 8 | 37.30 % |

*Seed, data and hyperparameters identical; only thread count varies.*

- **No appendix table exists for this yet.** If you want one, say so and I will add it
  as Table 100 from the measured series.

---

### P4 — Ch6 §6.5.9 and §6.6 — UNBLOCKED (stability re-run landed)

> **Files:** `05-results/09-forecast-stability-across-seeds.md`, `06-model-selection-decision.md`
> **Status:** the re-run finished 2026-09-07 14:44. **The verdict survives** (F19), so
> the conclusion stays — but four specific edits are required.

**The good news first.** These two sentences were *false* when written and are now
**true**, because thread count is fixed:

> §6.5.9: "Every input is identical; only the random seed differs."
> §6.6: "A five-seed sweep with every input held identical..."

They can stay **provided P3 lands**, which is what records that XGBoost is pinned to one
thread. P3 and P4 must ship together — leaving these sentences without the protocol note
restores the false claim.

**Edit 1 — REPLACE Table 16's per-seed winners** with the new run:

| Category | Winner per seed | |
|---|---|---|
| CSD | XGBoost, XGBoost, LightGBM, LightGBM, LightGBM | flips |
| danskvand | LightGBM ×3, XGBoost, LightGBM | flips |
| energidrikke | LightGBM, XGBoost, XGBoost, LightGBM, LightGBM | flips |
| RTD | XGBoost, LightGBM ×4 | flips |

**All four still flip.** The verdict is unchanged.

**Edit 2 — REPLACE the stability table in §6.5.9** (the median CV / p90 CV / WMAPE
mean / WMAPE sd grid) from the regenerated `stability.csv`. Values moved.

**Edit 3 — ⚠ QUALIFY this sentence in §6.6.** This is the one substantive change:

**Anchor:**
> "**The defensible claim is that the two are statistically indistinguishable here**, the between-seed spread exceeding the between-model difference."

**Action:** REPLACE the clause after the comma. It is **no longer true of all four
categories**:

| Category | Model gap | Max seed sd | |
|---|---|---|---|
| CSD | 0.11 | 0.65 | seed spread wins |
| danskvand | 0.74 | 1.22 | seed spread wins |
| energidrikke | 0.42 | 1.38 | seed spread wins |
| **RTD** | **3.16** | **1.94** | **model gap wins** |

Replacement text:

> **The defensible claim is that the two are statistically indistinguishable here.** In
> CSD, danskvand and energidrikke the between-seed spread exceeds the between-model
> difference outright. On RTD the model gap is the larger of the two — LightGBM averages
> 32.3 per cent against XGBoost's 35.5 — yet the per-seed winner still changes there as
> well, so a per-category winner remains unsupported in all four categories, on
> different grounds in the fourth.

**Edit 4 — fix the cross-reference.** §6.6 cites "(§6.5.7)" for the seed sweep; it is
**§6.5.9**.

**Assets:**
- **In-text:** Table 16 (replaced), the §6.5.9 stability table (replaced).
- **Appendix:** none new required.

### P5 — Ch9 §9.4 Limitations

> **File:** `chapters/sections/13-ch9-discussion/04-limitations.md`
> **Action:** APPEND to the existing bullet list. **This section is bullets, not prose** —
> match it. Do not paste §2.5's paragraphs here.

- **Exogenous calendar dependency:** holiday features come from a third-party API; exact
  reproduction depends on that service. Cached with timestamp and SHA-256, which
  mitigates but does not remove the dependency
- **`non_holiday_days` is a proxy:** observes the absence of a designated public holiday,
  not actual opening hours or trading intensity
- **Monthly aggregation limits holiday effects:** a holiday redistributes demand within a
  month; a null at this grain means no effect *survived aggregation*, not no effect
- **School holidays excluded:** vary by Danish municipality, no free reliable source
  found; a national approximation would add error of unknown sign
- **Determinism costs training time:** XGBoost is restricted to one thread for accuracy
  measurement, which is slower but reproducible

---

### P6 — Ch9 §9.5 Future research directions

> **File:** `chapters/sections/13-ch9-discussion/05-future-research-directions.md`
> **Action:** APPEND to the existing bullet list. Bullets, not prose.

- **Weather as an exogenous driver:** temperature is the most plausible omitted variable
  for beverage demand and the natural next addition after the holiday calendar
- **Macroeconomic indicators:** consumer confidence and disposable income capture demand
  shifts the current feature set cannot observe
- **Municipality-level school holidays**, if a source becomes available
- **Sub-monthly grain:** would let holiday *timing* act rather than only holiday *count*,
  which monthly aggregation currently forecloses

---

## PART 2B — THE PROSE

### §2.1 → goes to P1 (Ch4 §4.3)

The feature set was extended with a Danish public-holiday calendar retrieved from the
Nager.Date public API. The calendar is fetched per year and cached locally alongside a
manifest recording the retrieval timestamp and a SHA-256 digest of the response, so that
any later run can establish exactly which version of the calendar produced a given
result. Three features are derived at the brand-by-month grain: the number of days in
the month, the number of public holidays falling within it, and the difference between
the two. The third is named `non_holiday_days` rather than the more common
`trading_days`, because the latter would assert something the Danish retail calendar does
not support: shops trade at weekends, and many open on public holidays with reduced
hours. The feature therefore counts days not designated as public holidays, which is a
weaker and more defensible claim than counting days on which trade occurred.

Retrieval is wired into the existing Nielsen refresh so that the calendar is updated
whenever the underlying sales data is re-pulled, and is also exposed as a standalone
entry point, since a full Nielsen refresh is slow and the calendar changes independently
of it. Where the API cannot be reached, the pipeline does not substitute a default. The
parameter-derivation step records in its contract whether holiday enrichment is
available, and the feature-engineering step fails if a contract promises enrichment that
cannot be supplied. An unenriched run is therefore an explicitly declared state rather
than a silently different one.

### §2.2 → goes to P2 (Ch6, new subsection), first half

Holiday enrichment was evaluated by an ablation in which each arm was tuned
independently, refit on the combined training and validation data, and scored once on
the held-out test split. Across the twelve category-and-model combinations, the calendar
features improved weighted MAPE in seven. The mean improvement was 1.42 percentage
points, but that average should not be read as the result, because it conceals a
systematic difference between model families that is itself the more informative
finding. The linear model benefited in three of four categories, by an average of 2.49
percentage points, and LightGBM benefited in three of four by an average of 2.45.
XGBoost benefited in only one of four and was worse on average by 0.68 percentage
points. The single largest gain was for RTD under the linear model, where weighted MAPE
fell from 56.30 to 47.33 per cent.

The pattern across categories is similarly uneven. RTD improved under all three models,
by an average of 4.82 percentage points, and danskvand and energidrikke improved under
two of three each. CSD was harmed under all three. CSD is also the largest and
best-predicted category in the study, which suggests the calendar contributes most where
the existing feature set leaves the most unexplained variation, and contributes nothing
where the autoregressive features already perform well. Reported as a single average,
the result would appear to be a modest uniform gain; reported by category and model, it
is a conditional gain whose conditions can be stated.

### §2.3 → goes to P2 (Ch6, new subsection), second half

A gain in accuracy does not by itself establish that the holiday calendar supplied new
information. The feature set already contained month, quarter and a peak-month
indicator, and the major Danish holidays fall in a fixed monthly pattern, so an
improvement could in principle reflect a more convenient encoding of seasonality the
model already had access to. This was tested by comparing SHAP attribution before and
after enrichment. Under pure re-encoding, attribution gained by the holiday features
would be offset by an approximately equal loss from the existing calendar features.

That is not what occurs. The holiday features attract between 1.21 and 2.37 per cent of
total attribution across the four categories, while the existing calendar features lose
between 0.26 and 1.00 per cent — and in energidrikke they gain rather than lose. The net
effect is positive in every category. The calendar therefore carries information the
month-based features do not, which is consistent with the substantive argument for
including it: the abolition of Store Bededag reduced the Danish public-holiday count
from fifteen to fourteen partway through the panel, a permanent structural break that a
month index cannot represent, because the month is unchanged while its holiday content
is not.

### §2.4 → goes to P3 (Ch6 §6.3.3 Execution protocol)

A defect in the execution protocol was identified while regenerating results, and it is
reported here because it affects every figure in this chapter. Re-running the benchmark
on unchanged data produced different figures for XGBoost while leaving every other model
bit-for-bit identical. That asymmetry localised the cause: XGBoost had been configured to
use all available processor cores. Holding the random seed, the data and all
hyperparameters constant and varying only the number of threads, weighted MAPE moved
from 34.65 per cent at one thread to 37.30 at eight — a spread of 2.65 percentage points
attributable to nothing but the degree of parallelism. Setting a random seed does not
prevent this, because the seed governs which observations and features are sampled, not
the order in which partial results computed on separate threads are combined.

The consequence is material rather than cosmetic, because that spread is larger than
most of the feature effects this study set out to measure. Before the configuration was
corrected, two reported conclusions did not survive: the best-performing model for one
category changed, on an original margin of 0.43 percentage points, and three of the
twelve holiday-ablation comparisons reversed direction. All accuracy measurements were
consequently rerun with XGBoost restricted to a single thread, which yields identical
results across repeated runs. Multi-core execution was retained for the
resource-profiling measurements of §6.5.6, where parallel execution is the property
being measured rather than a confound, and the core count is reported alongside those
figures. The wider point is that a result which cannot be reproduced on a different
machine has not been established, and that fixing a random seed is not sufficient to
guarantee that it can be.

---

## PART 3 — Assets summary

| Prose | In-text asset | Appendix (cite, don't inline) |
|---|---|---|
| §2.1 (Ch4) | Table 4, amended with a holiday row | 90 provenance, 93 definitions |
| §2.2 (Ch6) | **New table** — per-model split | 94 full 12-cell grid |
| §2.3 (Ch6) | none | 96 SHAP, 91 annual counts, 92 monthly matrix |
| §2.4 (Ch6) | **New small table** — thread sweep | none yet (Table 100 on request) |
| P5 / P6 (Ch9) | none — bullets | — |

**Renumbering:** the new Ch6 table lands as **Table 14**; existing 14+ shift by one.
Word cross-references update automatically only if they are real field references —
check, because several table callouts in this document are plain text.

---

## PART 4 — Provenance, discrepancies, open items

| Element | Source |
|---|---|
| 7/12, −1.42 pp, per-model and per-category figures | `holiday_ablation_tuned_delta.csv`, appendix 94 |
| SHAP gains and losses | appendix 96 |
| Thread-count WMAPE series | P0047 F18 (reproducible on demand) |
| Store Bededag 15 → 14 | appendix 91 (observed in fetched data) |

### ⚠ Two pre-existing discrepancies found while locating anchors

Neither is caused by the enrichment. Both are flagged, not silently fixed.

1. **"22 columns" is wrong.** The CSD feature matrix has **54 columns**. The thesis
   sentence may be counting something narrower, but as written it does not match the
   parquet it cites. **Do not amend this number as part of the holiday edit** — establish
   what it was meant to count first, or it will be wrong in a new way.
2. **"14 modelling features" vs. the benchmark's 13.** The thesis lists 14 including
   `weighted_distribution`; `srq1_benchmark.py::FEATURES` contains 13 and does **not**
   include it. So either the thesis or the code is wrong about whether
   `weighted_distribution` is a model input. Resolve before amending 14 → 17, since the
   corrected figure depends on which is right (17, or 16).

### Unverified claims — kept out of the prose deliberately

- **CV-03** — statute name and year omitted. The prose asserts only that Danish shops
  trade at weekends and often on public holidays, which you confirmed.
- **CV-04** — §2.4 states the measured effect and describes the cause as an ordering
  issue without citing a mechanism.
- **CV-05** — §2.3 cites the abolition as observed in the data, not as a legislative fact.

**All prose above is safe to paste now.** Verification would let these be sharpened, not
corrected.

### Blocked

**Nothing.** P4 unblocked 2026-09-07 — the stability re-run landed and the verdict
survives (F19). All six blocks are ready to paste.

**One sequencing constraint:** P3 and P4 must ship together. P4 leaves two sentences
standing that claim "every input held identical"; those are only true once P3 records
that XGBoost is pinned to a single thread.
