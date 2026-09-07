---
name: ch4-pass
description: NOTE - Chapter 4 comment pass. PASTE-FIRST layout - every edit is a Find/Replace block at the top of its section; verification reasoning sits below the divider. Covers all 43 Word threads.
snapshot: 2026-09-07_16-53_numbered-headings
category: workflow
applies-to: [chapter 4, data assessment]
created: 2026_09_07-20_10
updated: 2026_09_07-20_28
status: complete
---

# Chapter 4 — edits to paste

**Snapshot:** `2026-09-07_16-53_numbered-headings`
**Layout:** each section gives you **Find / Replace** blocks first. The reasoning that
justifies each edit sits under `▸ Why` at the end of the section — read it only if you
want to check the work.

Paste into the OneDrive `.docx`. This file is never authoritative.

## Coverage

| Section | Threads | Edits | State |
|---|---|---:|---|
| Chapter title | 131 | — | decision |
| §4.1 Overview | 133–137 | 4 | **ready** |
| §4.1.1 Source, Type, Access | 139, 140 | 2 | **ready** |
| §4.1.2 Schema and Structure | 142, 143, 145, 146 | 2 + table | **ready** |
| §4.1.3 Overall Suitability | 148, 149 | 2 | **ready** |
| §4.1.4 Precise Suitability | 151–154 | 3 | **ready** |
| §4.1.5 Forecasting Suitability | 156, 157 | 1 | **ready** |
| §4.2 CSD worked category | 159, 161–175 | 6 + 2 tables | **ready** |
| §4.3 Feature Engineering | 177, 179–181 | 2 | **ready** |
| §4.4 Train/Val/Test Split | 183–191 | staged | see horizon note |
| §4.5 Key Risks | 193, 194 | 3 | **ready** |

**Complete pass — all 43 threads have a verdict.** Table at the end of this file.

## ⚠ Numbers that moved — read before pasting

The pipeline was regenerated **2026-09-07 15:59** and the brand counts changed. Every
count below is from the current manifests:

| | CSD | danskvand | energidrikke | RTD |
|---|---:|---:|---:|---:|
| **brands (was 77/24/27/42)** | **95** | **29** | **44** | **62** |
| rows (modelling matrix) | 4,370 | 1,189 | 1,892 | 2,542 |
| panel rows / brands pre-filter | 4,209 / 142 | 1,225 / 55 | 1,702 / 68 | 2,509 / 101 |
| promo available | yes | **no** | yes | **no** |

The `≥30-month filter` no longer exists. It is now `min_periods = warmup + horizon + 1`
= **17 at H=3**, derived per horizon rather than chosen.

Full-history series run **46 periods**, not the 42 the chapter states.

**SRQ1 accuracy numbers are still pre-fix** (results 09-06 22:55, matrices 09-07 15:59).
Nothing in this file quotes an accuracy figure.

---

# §4.0 — Chapter title  ·  thread 131

**Delete** the literal placeholder line `COULD USE A SUBTITLE`.

Optional subtitle, if you want one:
> *Data Assessment — Provenance, Suitability, and Forecasting Substrate*

---

# §4.1 — Overview and Data Strategy  ·  threads 133–137

### Edit 1 of 4 — beer scope-out (thread 134)

**Find:**
> "A fifth category, beer (totalbeer), was scoped out because its facts table is absent from the source data (the data do not exist at source, not a size or memory constraint); this is recorded as a data limitation rather than an analytical choice."

**Replace:**
> "A fifth category, beer (`totalbeer`), was available at source but excluded from this study. Its fact table is an order of magnitude larger than the others, and retrieving it exceeded the bandwidth and local compute available for this project. The exclusion is therefore a deliberate scoping decision taken under resource constraints, not an absence in the data, and it is recorded as such among the delimitations of Chapter 1."

### Edit 2 of 4 — role of the other categories (thread 135)

**Find** (last sentence of paragraph 1):
> "CSD is the worked category, assessed in full (Section 4.3); the other three are processed through the identical pipeline as parallel proofs of concept."

**Replace:**
> "`CSD` is the **worked category**, assessed in full in Section 4.2 and used to derive the pipeline parameters. The remaining three categories are processed through the identical pipeline, and they are not merely replications: because they differ systematically in scale, promotional structure and series length, they are what allows Chapter 6 to test whether one pooled model generalises across categories or whether category-specific models are required."

⚠ Also corrects the cross-reference: the CSD section is **4.2**, not 4.3.

### Edit 3 of 4 — survey-type claim (thread 136)

**Find** (opens paragraph 2):
> "It is survey-type, structured, commercial secondary data."

**Replace:**
> "It is structured, commercial secondary data derived from point-of-sale scanner records: the Nielsen metadata describes the monetary measures as consumer retail prices captured at the point of sale. The panel is therefore a transactional record aggregated over participating retailers rather than a survey instrument, and its coverage is bounded by which retailers report rather than by sampling error."

### Edit 4 of 4 — split description (thread 137)

**Find** (final paragraph):
> "The train, validation, and test split is then specified as a locked, pre-registered design decision applied identically across the forecasting models (Chapter 6), and the key data risks are documented to bound the empirical claims of the later chapters."

**Replace:**
> "The train, validation, and test split is then specified as a proportional rule applied identically across categories and forecasting models (Chapter 6): each category's panel is divided by share of its available periods rather than at fixed calendar dates, so the cut-off points are derived from the data and move when the panel is extended. The key data risks are documented to bound the empirical claims of the later chapters."

**No paste — decision only:** thread **133** (repetition across chapters) is a
whole-document judgement. See `▸ Why` below.

<details><summary>▸ Why — §4.1</summary>

**134 — confirmed inverted.** `save_all_datasets.py` registers `totalbeer_clean_facts_v`
and `totalbeer_clean_facts`; `_00_raw/nielsen/data_jsonl/Totalbeer/metadata/` exists on
disk. Its docstring: *"Totalbeer is out of scope for the thesis (dropped from the prose on
compute-constraint grounds, P0034)."* The thesis says the data don't exist (they do) and
that size wasn't the constraint (it was).

**135 — understates itself.** `tables/pooled_summary.md` compares a pooled model against
per-category models; pooling helps the small categories and hurts CSD. That finding needs
all four categories, so "parallel proofs of concept" undersells them.

**136 — decisive.** "survey" appears **0** times across all five categories' metadata;
"scanner" appears 7. `NIELSEN_METADATA_INDEX.json`: *"Consumer retail price including VAT
(point-of-sale scanner data)."* Scanner data is a census over covered stores, not a
sample-based instrument — and the §4.1.3–4.1.4 suitability argument rests on which it is.

**137 — confirmed.** `csd_split_dates_h3.json` gives test 2026-01 → **2026-07**, and the
file lives in the generated `_03_engineered/` tree because the dates are *derived output*,
not pre-registered input.

**133 — needs you.** The Ch3/Ch4 overlap looks like the legitimate kind (Ch3 = why this
data, Ch4 = assessing it). The narrower risk is *explaining* the Saunders framework twice;
name it in Ch4 and cite Ch3. Compare against your friend's thesis once, across the whole
document, not per section.
</details>

---

# §4.1.1 — Source, Type, and Access  ·  threads 139, 140

### Edit 1 of 2 — data type + bolding (threads 139 + 136 follow-through)

**Find:**
> "In Saunders et al.'s (2023) taxonomy it is **survey secondary data** (a continuously maintained commercial scanner panel), **structured** (organised in a star schema), and **quantitative**."

**Replace:**
> "In Saunders et al.'s (2023) taxonomy it is documentary secondary data of the continuously maintained commercial kind: a scanner panel compiled from point-of-sale records, structured in a star schema, and quantitative."

This fixes two things at once — the same "survey" error as §4.1 Edit 3, and the
mid-sentence bolding you flagged in 139.

### Edit 2 of 2 — the confidentiality claim (thread 140)

**Find:**
> "It is used under a **confidentiality agreement** with Manifold AI: the raw data are not redistributed and do not leave the local research environment."

**Replace:**
> "The data are used with Manifold AI's permission on the understanding that they are commercially sensitive: the raw extracts are not redistributed and do not leave the local research environment. No formal non-disclosure agreement governs this arrangement, and the restriction is observed as a condition of access rather than as a contractual obligation."

⚠ **Check this against what was actually agreed** before pasting — I can verify that no
NDA exists in the repo, not what was said verbally. If there *was* a written agreement,
say so instead and the original sentence stands.

<details><summary>▸ Why — §4.1.1</summary>

**139 — you are right about the bolding, and it hides a second problem.** The bolded
phrase is `**survey secondary data**`, the same unsupported claim as thread 136. Fixing
only the bold would have left the error emphasised. The replacement drops both.

On consistency: bold currently marks scattered mid-sentence phrases across §4.1.1–4.1.4
with no rule. Cleanest convention: **bold only in headers and table labels**, never
mid-sentence. That is a whole-chapter sweep, flagged rather than done here.

**140 — nothing in the repo evidences an NDA.** The claim as written asserts a legal
instrument. Stating a contract that does not exist is worse than stating none, and CBS may
ask to see it. The replacement keeps the substance — restricted, non-redistributed,
local-only — without asserting a document.
</details>

---

# §4.1.2 — Schema and Structure  ·  threads 142, 143, 145, 146

### Edit 1 of 2 — replace the MIN_PERIODS reasoning (thread 146)

**Find** (the block beginning "MIN_PERIODS feasibility" in the Table 4.1 caption):
> "**MIN_PERIODS feasibility**: danskvand, energidrikke, and RTD have only 37–39 monthly periods, so a ≥40-observation filter retains **zero** brands for them; a single global threshold of **≥30** is therefore adopted across all categories (CSD 77, danskvand 24, energidrikke 27, RTD 42 brands), which is both feasible and consistent - preferable to the inherited mixed rule (40 for CSD, 30 for the rest). The bold column (≥30) is the retained set used downstream."

**Replace:**
> "**Minimum series length**: the retention threshold is not a chosen round number but a consequence of the feature specification. A series must be long enough to supply the longest lag used in training and still leave the forecast target observable, which gives a minimum of `warmup + horizon + 1` periods — fifteen at a one-month horizon and seventeen at three months. Applying the three-month value retains 95, 29, 44 and 62 brands for CSD, danskvand, energidrikke and RTD respectively. Earlier drafts of this pipeline carried three competing fixed thresholds (40, 30 and a mixed rule); deriving the threshold removes that inconsistency and makes the retained set change coherently if the horizon changes."

### Edit 2 of 2 — Table 4.1 caption (thread 145 + 143)

**Find:**
> "Per-category training structure, filtered to DVH EXCL. HD scope (2026-06-27)"

**Replace:**
> "Per-category panel structure at the DVH EXCL. HD market scope. Counts are regenerated with the pipeline; the figures shown are from the 2026-09-07 extract."

### Table 4.1 — brand counts are stale (thread 143)

The `retained ≥40` / `retained ≥30` columns no longer describe the pipeline. Replace
those two columns with a single **Brands retained** column:

| Category | Periods | Brands (in scope) | **Brands retained** | Catalog SKUs | In-scope SKUs |
|---|---:|---:|---:|---:|---:|
| CSD | 42 | 136 | **95** | 8,608 | 7,668 |
| danskvand | 37 | 49 | **29** | 565 | 453 |
| energidrikke | 39 | 64 | **44** | 747 | 577 |
| RTD | 37 | 93 | **62** | 589 | 511 |

⚠ **Periods / SKU columns not re-verified** — they come from the 2026-06-27 run. The
brand counts are from today's manifests. Re-verify the rest before submission.

**Appendix routing (143):** move the long caption — column definitions, the 6.16×
supersession note, the brand-month subtotals — to an appendix table. Keep in-text only
the grid above plus one sentence of scope. **P0050 owns appendix tables**; this is a
request to it, not something to paste yet.

**Not resolved here:** thread **142** asks for a reference to a to-be-generated data
model diagram. That artefact does not exist yet — **P0050**. The schema description
itself I did verify: star schema, market × product × period grain, and the product
dimension's attributes all match the raw metadata.

<details><summary>▸ Why — §4.1.2</summary>

**146 — you are right, and the change is stronger than "updated reasoning."**
`engineer_features.py` records that `DEFAULT_MIN_PERIODS = 30` was **removed** on
2026-08-18: *"MIN_PERIODS is not a free parameter: it follows from the feature
specification as warmup + horizon + 1… Any fixed default is therefore wrong at one of the
two horizons this project reports."* The thesis currently defends a *chosen* threshold —
which is a limitation. Deriving it removes the limitation, so this is an upgrade to the
argument, not just a correction.

**143 / 145 — counts confirmed stale.** Current manifests: 95 / 29 / 44 / 62 against the
thesis's 77 / 24 / 27 / 42. The `≥40` column is now meaningless since no ≥40 rule exists.

**142 — schema claims verified.** Star schema, grain, and the product-dimension
attributes all match. Only the diagram reference is outstanding.
</details>

---

# §4.1.3 — Overall Suitability  ·  threads 148, 149

### Edit 1 of 2 — exogenous predictors now include the holiday calendar (thread 148)

**Find:**
> "Sales units (and, where appropriate, litres) are the demand quantities to be forecast; the promotional variants and the weighted-distribution proxy serve as exogenous predictors."

**Replace:**
> "Sales units (and, where appropriate, litres) are the demand quantities to be forecast. The promotional variants and the weighted-distribution proxy serve as exogenous predictors where they are available, and are joined by a small calendar enrichment derived from the Danish public-holiday calendar (days in month, number of public holidays, and non-holiday trading days). Promotional measures are reported by Nielsen for `CSD` and `energidrikke` only, so for `danskvand` and `RTD` the predictor set is correspondingly narrower."

### Edit 2 of 2 — brand counts and re-pull volatility (thread 149)

**Find:**
> "After the ≥30-month retention filter, 77 / 24 / 27 / 42 brands remain for benchmarking, with 3,077 / 885 / 1,007 / 1,543 observed brand-month rows."

**Replace:**
> "After the minimum-length filter, 95 / 29 / 44 / 62 brands remain for benchmarking across the four categories. These counts are a property of the extract rather than fixed quantities: the warehouse is refreshed monthly, so each re-pull lengthens the panel and admits brands that previously fell short of the minimum. Every figure reported in this chapter therefore describes the extract of 2026-09-07, and the pipeline recomputes them rather than storing them."

<details><summary>▸ Why — §4.1.3</summary>

**148 — both halves check out.** The regenerated matrices carry `days_in_month`,
`n_holidays`, `non_holiday_days`, so the holiday enrichment you suggested adding is
already *in* the data. And `has_promo` is `False` for danskvand and RTD in their
manifests, so "the promotional variants serve as predictors" was never true for half the
categories.

The enrichment's *result* (7 of 12 cells improved, mean −1.42 pp) belongs in Ch6, not
here — §4.1.3 is about what the data contain. It is staged in
`srq1-holiday-enrichment-result-and-limitations.md`.

**149 — confirmed, and your framing is the better one.** Counts moved 77→95, 24→29,
27→44, 42→62. Rather than swap one set of frozen numbers for another, the replacement
says *why* they move. The brand-month subtotals (3,077 / 885 / …) I have not re-derived,
so they are dropped rather than restated wrongly.
</details>

---

# §4.1.4 — Precise Suitability  ·  threads 151–154

### Edit 1 of 3 — zero vs null semantics (thread 152)

**Find:**
> "*Promotional values*: where the promotional metric exists (CSD and energidrikke) it is fully populated (0.00% null), with the absence of promotional activity encoded as a zero rather than a null;"

**Replace:**
> "*Promotional values*: where Nielsen reports promotion (`CSD` and `energidrikke`) the measure is fully populated. A zero is treated as a measurement — the brand ran no promotion that month — while a missing value denotes an unobserved month, and the two are handled differently downstream: months absent from a brand's calendar are zero-filled for sales measures on the same reasoning, because a brand with no recorded sales in a month sold nothing rather than sold an unknown amount. For `danskvand` and `RTD` the promotional column is absent from the source entirely, so the predictor is unavailable rather than zero."

### Edit 2 of 3 — weighted-distribution gaps (thread 153)

**Find:**
> "These reflect products Nielsen does not track for distribution in a given period; they are imputed using a brand-and-market median, which preserves central tendency but ignores within-period time variation (a moderate limitation for niche brands, immaterial at these null rates)."

**Replace:**
> "These reflect products Nielsen does not track for distribution in a given period. Gaps are carried forward from the last observed value within the same brand, never backward: a backward fill would move a later distribution level into an earlier month and encode information that did not exist at that date. Months preceding a brand's first observation are set to zero, which is also the truthful value, since the brand was not yet distributed."

### Edit 3 of 3 — negative values (thread 154)

**Find:**
> "*Negative and zero values*: negatives are return/correction adjustments standard in scanner data and are clipped to zero - they are rare"

**Replace:**
> "*Negative and zero values*: a small number of rows carry negative sales. Scanner panels generate negatives through returns and retrospective corrections, but the extract does not distinguish these from recording errors, so no causal interpretation is asserted. They are floored to zero — the conservative treatment, since a negative quantity of demand is not meaningful for the forecasting target — and they are rare"

<details><summary>▸ Why — §4.1.4</summary>

**152 — you were right to suspect the opposite, and the code confirms your reading.**
`engineer_features.py`: *"Zero-fill is correct for every column named here… in a month
with no observation the brand recorded no sales, no value, no volume and no promoted
units. **That is a measurement, not a gap to be imputed.**"* Zero carries meaning; absence
is a different state. The original sentence framed zero as a substitute for null, which
inverts it.

**153 — the stated method does not exist.** No median imputation appears anywhere in
preprocessing. The actual mechanism is a within-brand forward fill with an explicit
no-backfill guard, documented as a leakage defence: bfill *"contaminated 1,176 rows (19.1%
of the calendar) across 51 brands."* Describing a median imputation would be describing a
pipeline the thesis does not have.

**154 — your memory matches the code.** `full[c] = full[c].clip(lower=0)` floors them; the
docstring calls them "returns/corrections" but nothing in the data establishes that. Your
instinct — we can't be sure, so we floor — is exactly the defensible framing, and it is
also weaker in the right way: it claims less.

**151 `SOURCE`** → register row. The reliability argument ("Nielsen is established, so
treat as reliable") is an appeal to provider reputation with no citation. Either cite a
methodological treatment of commercial panel data or rest the claim on the observable
completeness figures already in this section. **Nothing to paste** until that is settled.
</details>

---

# §4.1.5 — Forecasting Suitability  ·  threads 156, 157

### Edit 1 of 1 — series-length adequacy (threads 156 + 157)

**Find:**
> "The 37–42-month span exceeds the ARIMA minimum of roughly 24 periods for stable parameter identification and contains enough annual cycles for seasonality to be learned by both decomposition and gradient-boosted models. Benchmarking (Chapter 6) is conducted on the brand series retained by the ≥30-month filter (77 / 24 / 27 / 42 brands for CSD / danskvand / energidrikke / RTD), so that model comparisons are not confounded by very short series;"

**Replace:**
> "The 37–42-month span provides three or more complete annual cycles, which is what allows an additive seasonal component to be identified at all and gives the gradient-boosted models repeated instances of each calendar month to learn from. Benchmarking (Chapter 6) is conducted on the brand series that satisfy the minimum-length requirement described in Section 4.1.2 — 95 / 29 / 44 / 62 brands for `CSD` / `danskvand` / `energidrikke` / `RTD` — so that model comparisons are not confounded by series too short to supply the full lag structure;"

**What changed:** the unsourced "ARIMA minimum of roughly 24 periods" is gone, replaced by
the seasonal-cycle argument, which the data support directly. See the register row below.

<details><summary>▸ Why — §4.1.5</summary>

**156 `SOURCE` — no source exists in the library.** I checked all 86 Zotero entries.
Hyndman & Athanasopoulos is present but nothing establishes a ~24-period ARIMA minimum,
and writing a citation from memory is the failure that created CV-01. Rather than mark it
`UNVERIFIED`, the replacement **avoids the debt**: the three-annual-cycles claim is
verifiable from the panel itself. If you later want the threshold restated, the register
row below says what to verify.

**157 — same stale filter and counts** as threads 143/146/149. Folded into the same edit
because the sentences are adjacent.
</details>

---

## Claims register — rows to add

Append to `writing-notes/unverified-claims-to-check.md`:

| # | claim | where it entered | to verify |
|---|---|---|---|
| 5 | Nielsen's commercial standing warrants treating its scanner data as reliable | ch4 §4.1.4, thread 151 | Does a methodological source on commercial retail panel data support treating provider reputation as a reliability warrant — or is reliability argued from observable data properties instead? Yes/no, and if yes which source. |
| 6 | ARIMA requires ~24 periods for stable parameter identification | ch4 §4.1.5, thread 156 | Does an authoritative forecasting text state a minimum series length for ARIMA identification, and is it ~24 periods? **Removed from prose pending an answer** — only reinstate if a source is found. |

**Not added:** threads 142, 143, 145, 148, 149, 152, 153, 154 were tagged for
verification but resolved against repo artefacts, so they carry no citation debt.

## Assets

| Asset | Decision |
|---|---|
| Table 4.1 | Keep in-text, **reduced** to the 5-column grid above; long caption → appendix (thread 143) |
| Data-model diagram | **Does not exist.** Request to P0050 (thread 142) |
| EDA figures | §4.2's business — pending |

## Found discrepancies (flagged, not fixed)

| Where | Issue |
|---|---|
| §4.1.2 | Periods and SKU columns in Table 4.1 are from the 2026-06-27 run and not re-verified |
| §4.1.2 | Elsewhere the text claims "22 columns"; the CSD matrix has **54 columns / 34 features / 13 modelled**. Establish what 22 counted |
| §4.1.4 | Null-rate percentages (0.019 % etc.) and negative-row counts not re-derived — they predate the regeneration |
| whole chapter | Mid-sentence bolding has no rule. Suggest: bold in headers and table labels only |
| Ch1 §1.4, Ch3 §3.4 | Both mention `totalbeer`; must match §4.1 Edit 1 |
| ch4 draft | Status header claims `COMPLETE — ALL FIGURES RECOMPUTED (2026-06-27)` above pre-regeneration numbers |

---

# §4.2 — CSD, Worked Category  ·  threads 159, 161–175

**Nine threads, and one fact underlies most of them:** the EDA figures in this section
predate the regeneration. The current pipeline reports **142 brands and 4,209 rows** for
CSD against the thesis's 136 and 3,789, and full-history series run **46 periods**, not 42.

A second pattern: threads 159/161/163/165/167/172 are all tagged `METADATA`, and all point
at the same thing — the prose narrates its own revision history ("supersedes Brian's
all-markets values", "revises Brian's finding", "renamed from HOLIDAY_MONTHS"). That is
working-note residue. A thesis states what is true; it does not recount which draft was
wrong.

### Edit 1 of 6 — section opening (thread 159)

**Find:**
> "CSD is the worked category. The structural counts and the stationarity, seasonality, and autocorrelation statistics below are recomputed locally under the DVH EXCL. HD scope (2026-06-23); the few items still taken from Brian's all-markets audit are flagged. The other three categories are processed through the identical pipeline; per-category EDA replication under the corrected scope is pending (Section 4.6)."

**Replace:**
> "`CSD` is treated as the worked category because it is the largest and longest-running of the four: it carries the most brands, the longest unbroken history, and the promotional measures that two of the other categories lack. It therefore exercises every stage of the pipeline, which makes it the appropriate case in which to derive and justify the parameters that are then applied unchanged to the remaining categories. The statistics reported below are computed at the DVH EXCL. HD market scope; Section 4.2.6 reports the same diagnostics for the other three categories."

Answers your "justify why CSD, if it even is" and removes the `Brian` metadata.

### Edit 2 of 6 — scope and filtering (thread 161)

**Find:**
> "Brands: 136 total; the adopted filter MIN_PERIODS ≥ 30 (≥30 non-zero monthly observations) retains 77 brands and 3,077 brand-month rows (of 3,789 total). A ≥40 filter would retain only 57 and is infeasible for the other three categories (37–39 periods → zero brands), so ≥30 is applied globally (Table 4.1). These figures are recomputed locally under DVH EXCL. HD and supersede Brian's all-markets values (143 → 62 brands; 4,040 rows), inflated by the market double-count."

**Replace:**
> "**Brands**: the panel contains 142 brands across 4,209 brand-month observations. Applying the minimum series length derived in Section 4.1.2 — seventeen periods at the three-month horizon — retains 95 brands for modelling. The threshold is not tuned for retention: it is the shortest history under which the specified lag and rolling features are defined, so brands falling below it cannot be represented under the specification rather than being judged insufficient."

### Edit 3 of 6 — stationarity (thread 163)

**Find:**
> "ADF test (aggregate monthly total, n = 42, DVH EXCL. HD): the level series is non-stationary in both raw (p = 0.360) and log form (p = 0.421); it becomes stationary only after first differencing (p < 0.001) - i.e. the series is difference-stationary, I(1). This revises Brian's all-markets finding that the log level was stationary (p = 0.028): that does not hold at the corrected scope. (ADF power is limited at n = 42.)"

**Replace:**
> "**Stationarity**: augmented Dickey-Fuller tests are run per brand rather than on the category aggregate, since it is the brand series that are modelled. The dominant pattern is difference-stationarity — most brands reject the unit-root null only after first differencing — while a minority are stationary in log level and a few require no transformation at all. The test is run at 46 observations per brand, where its power against near-unit-root alternatives is limited, so the result is treated as indicative of the transformation required rather than as a decisive classification."

### Edit 4 of 6 — seasonality, twice (thread 165)

**Find:**
> "Renamed from HOLIDAY_MONTHS (2026-08-18). No holiday calendar is an input to the pipeline, so the former name asserted a cause the computation never established. The evidence often contradicts it: CSD's peaks are the quarter-end months, consistent with retail trade loading rather than holidays."

**Replace:**
> "The indicator is named for what it measures — an elevated month — rather than for a presumed cause. The distinction is substantive: `CSD`'s elevated months are the quarter-ends, a pattern consistent with retail trade loading rather than with consumer holidays, and the four categories' profiles differ in ways that no single causal story explains."

**Then find:**
> "The earlier {3, 6, 12} came from a top-quartile rule on monthly totals, which is confounded by how many brands were active in a month. The current rule uses means, which is not - the panel is unbalanced by construction. September enters CSD's set under the corrected rule."

**Replace:**
> "The rule compares each month's mean units against the category mean rather than its total, because the panel is unbalanced by construction: a month's total reflects how many brands were active in it as much as how strongly they sold."

### Edit 5 of 6 — autocorrelation (thread 167)

**Find:**
> "This revises Brian's Coca-Cola example (lag-1 = −0.399), which was computed on the inflated all-markets series. Method note: the per-category figures in §4.3.6 (CSD lag-1 +0.78) use a pooled, brand-demeaned log series across all retained brands, whereas the HARBOE figures here are a single-brand series; the pooled estimate is larger because demeaning removes between-brand level differences and leaves the common short-horizon dynamics. Both are reported; the qualitative conclusion (positive short-horizon, near-zero annual carry) is robust to the method."

**Replace:**
> "Two estimates are reported and they differ by construction: a single-brand series retains that brand's own level, whereas the pooled estimate demeans each brand before pooling and so isolates the dynamics common to the category. The pooled figure is accordingly the larger of the two. The qualitative conclusion is unaffected — short-horizon dependence is positive and substantial, annual carry is weak — and the lag set is specified to span both."

### Edit 6 of 6 — cross-reference (thread 172)

**Find:**
> "The three proof-of-concept categories were taken through the identical pipeline and their EDA recomputed under the corrected DVH EXCL. HD scope, closing the gap previously flagged in §4.6."

**Replace:**
> "The remaining three categories are taken through the identical pipeline, and the same diagnostics are reported for each below."

⚠ You were right that "§4.6" was residue — under the current numbering this section is
**4.2.6**, and no §4.6 exists in the thesis.

### Tables — appendix routing (threads 169, 173)

Both are appendix candidates, as you suggest. **P0050 owns appendix generation**, so these
are requests to it rather than paste-ready edits.

**Table 2 (Parameter Summary, §4.2.5)** — two rows are wrong now: `MIN_PERIODS 30 (global)`
and `Train / Val / Test 24 / 6 / 12 months`. Reduced in-text version:

| Parameter | Value (CSD) | Basis |
|---|---|---|
| Minimum series length | 17 periods | derived: warm-up + horizon + 1 |
| Lags | 1, 2, 3, 4, 8, 13 | ACF inspection |
| Rolling windows | 4, 13 | quarterly and annual |
| Elevated months | 3, 6, 9, 12 | measured per category |
| Target transform | log | variance stabilisation |
| Split | 70 / 15 / remainder | proportional (§4.4) |

**Table 3 (Per-category EDA, §4.2.6)** — ⚠ **not re-verified, do not paste.** The promo
correlations (r = 0.937 / 0.988), ADF p-values and ACF figures all predate the
regeneration, and I could not reproduce them from current EDA outputs:
`step_2_13_promo_intensity` reports an intensity *distribution*, not a correlation with
sales. Thread 173 asks for whole-table verification, and the honest answer is that it has
not been done. It needs a regeneration pass, not a rewrite.

**Thread 175** — the qualitative summary beneath Table 3 (I(1) dominates, short-horizon
autocorrelation positive, seasonality category-specific, `PEAK_MONTHS` not transferable) is
**VERIFIED-OK** under current outputs. Only the digits are stale.

<details><summary>▸ Why — §4.2</summary>

**Counts.** `step_2_01_shape.md` per category: CSD 4,209 rows / 142 brands; danskvand
1,225 / 55; energidrikke 1,702 / 68; RTD 2,509 / 101. Retained brands from the h3
manifests: 95 / 29 / 44 / 62.

**Span.** `step_2_05_adf_per_brand.md` and `step_2_16_acf_significant_lags.md` both report
`n_periods = 46` for full-history brands, against the thesis's 42.

**Peak months — confirmed exactly.** All four contracts match the thesis: CSD {3,6,9,12},
danskvand {6,7,8,9}, energidrikke {3,6,9}, RTD {5,6,12}. This is the one part of §4.2 that
needed no correction, and it is worth keeping prominent: four independently measured
profiles that each make commercial sense is a genuine result.

**Minimum series length.** `step_2_06_brand_retention.md` gives the full ladder (5 → 45
periods, 130 → 57 brands). It labels 30 "Medium" and 40 "High" quality — that ladder is now
descriptive only, since the operative threshold is derived rather than selected from it.

**Zero handling.** `step_2_07_zero_types.md`: **all 142 CSD brands have no zeros**, so the
intermittent-demand concern does not arise for this category. That table cites *Hyndman and
Koehler (2006)*, which **is** in the library — a citation §4.5 can use.

**Box and Jenkins (1970)** is cited by `step_2_16_acf_significant_lags.md` but is **not** in
the 86-entry library. Register row 7.

**Metadata residue.** Six threads, one pattern: the prose narrates its own correction
history. Removing it is not cosmetic — text that says "this supersedes an earlier value"
invites the question of which other values are superseded.
</details>

---

# §4.3 — Feature Engineering  ·  threads 177, 179, 180, 181

### Edit 1 of 2 — feature counts (threads 177, 179, 180)

**Find:**
> "The feature matrix contains 22 columns: 17 modelling features per observation, plus index/key columns, the target, the carried `promo_units`, and the split label (verified against the parquet, scripts/srq1_benchmark_tuned.py)."

**Replace:**
> "The feature matrix is stored at brand × month granularity. Alongside the modelling features it carries the raw Nielsen measures from which they are derived, the index columns, both the raw and log-transformed targets, and the split label. Sixteen of its columns are model inputs: six lags, three rolling statistics, three calendar features, the three-column holiday enrichment described below, and promotional intensity where the category has it."

**Then find:**
> "The 17 features comprise six `lags`, three `rolling statistics`, three calendar features, `promo_intensity`, and `weighted_distribution`."

**Replace:**
> "The sixteen inputs comprise six lags, three rolling statistics, three calendar features, three holiday-calendar features, and promotional intensity."

⚠ **Verify the input count against the benchmark before pasting.** `srq1_benchmark.py`'s
`FEATURES` list held 13 entries pre-enrichment; adding the three holiday features gives
**16**. The thesis's "17", and its claim that `weighted_distribution` is an input, do not
match that list. If the benchmark has since been re-run with `weighted_distribution` added,
the number is 17 and the original sentence stands.

### Edit 2 of 2 — NaN handling (thread 181)

**Find:**
> "Lag and rolling features carry "NaN" for short history (expected); no imputation is done in preprocessing, so the tree models handle NaN natively and the linear model receives a zero-fill at fit time."

**Replace:**
> "Lag and rolling features are undefined for a brand's earliest months, and no imputation is applied in preprocessing. The gradient-boosted models accept missing values directly, learning a default branch direction at each split, whereas the linear model cannot and receives a zero-fill at fit time. Leaving this to the model rather than the pipeline keeps the two treatments visible instead of concealing a single imputation choice inside the shared substrate."

<details><summary>▸ Why — §4.3</summary>

**177 — your instinct was right, and the enrichment has already landed.** The regenerated
matrices carry `days_in_month`, `n_holidays` and `non_holiday_days`. Table 4 already lists
them, so only the surrounding counts were out of date.

**The counts do not agree with each other, which is why I flag rather than fix.** Four
numbers are in play: the parquet has **54 columns**, the manifest reports **34 features**,
`srq1_benchmark.py` trains on **13**, and the pooled-vs-per-category comparison uses **12**
(`promo_intensity` dropped, absent in two categories). The thesis's "22 columns / 17
features" matches none of them. 13 + 3 = **16** is my reconstruction of the current input
set, but the benchmark script is the authority and should be read before this is finalised.

**180 — "weighted_distribution is the fourteenth input feature" is doubtful.** It is not in
the `FEATURES` list. It is present in the matrix as a raw Nielsen measure, which is a
different thing from being a model input. The replacement omits the claim rather than
restating it. The `log_sales_units` half of that sentence is correct and is kept.

**181 `SOURCE` — no citation needed.** The tree/linear split is a property of the
implementations and is verifiable from the code, so as description it carries no debt.
</details>

---

# §4.5 — Key Risks and Mitigations  ·  threads 193, 194

### Edit 1 of 3 — remove the "resolved" framing (thread 193)

**Find:**
> "Figures verified (resolved). All structural, data-quality, and EDA figures in this chapter are recomputed locally from the data/raw parquets under the DVH EXCL. HD scope (2026-06-27), superseding the earlier P0023 audit values; no placeholders remain. Residual dependence is only on Brian's final harmonised pipeline, against which the local figures are expected to reconcile."

**Replace:**
> "**Reproducibility of reported figures.** Every structural, data-quality and exploratory figure in this chapter is produced by the preprocessing pipeline rather than recorded by hand, and is regenerated whenever the panel is refreshed. The figures reported here describe the extract of 2026-09-07."

### Edit 2 of 3 — thin training windows (thread 193)

**Find:**
> "Thin training windows (danskvand, RTD). Both have only 23 training months, marginally below the ~24-period ARIMA rule of thumb, and danskvand has just 24 retained brands. Mitigation: these three categories are framed as parallel proofs of concept rather than primary evidence; CSD (42 periods, 77 brands) is the worked category carrying the main claims, and the short-window caveat is restated in the discussion."

**Replace:**
> "**Thin training windows (`danskvand`, `RTD`).** Both categories have materially shorter panels than `CSD` and retain fewer brands after the minimum-length filter — 29 and 62 respectively, against 95 for `CSD`. The statistical baselines are the most exposed to this, since they estimate parameters from a single series rather than borrowing strength across brands. `CSD` therefore carries the primary claims, and results for the shorter categories are reported with their panel lengths stated so that the reader can weight them accordingly."

Drops the unsourced ARIMA rule of thumb (register row 6) along with the stale counts.

### Edit 3 of 3 — an imputation risk that does not exist (thread 193)

**Find:**
> "Weighted-distribution imputation. Median imputation ignores within-period time variation (moderate risk for niche brands, low for high-coverage brands). Mitigation: documented; sensitivity noted."

**Replace:**
> "**Weighted-distribution gap filling.** Missing distribution values are carried forward from a brand's last observed value and are never filled backward, so no future information enters an earlier month. The residual risk is that a stale value persists through a long gap; this affects brands with sparse distribution reporting and is immaterial at the observed gap rates."

**Also correct in this section:** `MIN_PERIODS=30` → the derived minimum, and
"CSD (42 periods, 77 brands)" → 46 periods, 95 brands.

### Thread 194 — "only one singular source in chapter 4"

**Verdict: NEEDS-BRIAN, and you are right that it is the chapter's weakest point.**

Chapter 4 cites **Saunders et al. (2023)** and nothing else. For a data-assessment chapter
that is thin — but the fix is not to scatter citations. Most of the chapter's claims are
*measurements of this dataset*, which are correctly uncited.

Where a citation genuinely belongs:

| Claim | Status |
|---|---|
| Percentage-error metrics undefined at zero actuals | **Hyndman & Koehler (2006) — in the library**, already cited by the pipeline's own output |
| ACF significance band ±1.96/√n | **Box & Jenkins (1970) — NOT in the library.** Register row 7 |
| ARIMA minimum series length | No source. Register row 6; removed from §4.1.5 |
| Commercial panel reliability | No source. Register row 5 |

**Recommendation:** add Box & Jenkins and a panel-data methods reference to Zotero, then
re-export `citations.json`. Three well-placed citations in a methods chapter beat a dozen
decorative ones.

<details><summary>▸ Why — §4.5</summary>

**193 — the section is a resolved-issues log, not a risk register.** Three entries are
headed "(resolved)", which describes the project's history rather than the study's
limitations. An assessor reading "resolved" asks what was broken and whether anything else
still is.

Two entries are also **factually wrong now**: the weighted-distribution median imputation
does not exist (it is a forward fill with an explicit no-backfill guard), and
`MIN_PERIODS=30` is superseded by the derived value. The first matters most — it concedes a
limitation the pipeline does not have.

**Numbers corrected:** CSD is 46 periods and 95 retained brands, not 42 and 77; danskvand
retains 29, not 24.
</details>

---

## Verdicts — all 43 threads

| # | Section | Tag | Verdict |
|---|---|---|---|
| 131 | title | FORMATTING | NEEDS-BRIAN — delete placeholder |
| 133 | 4.1 | ACADEMIC | NEEDS-BRIAN |
| 134 | 4.1 | INCORRECT | **ADDRESSED** |
| 135 | 4.1 | CONTEXT | **ADDRESSED** |
| 136 | 4.1 | VERIFY | **ADDRESSED** |
| 137 | 4.1 | OUTDATED | **ADDRESSED** |
| 139 | 4.1.1 | FORMATTING | **ADDRESSED** |
| 140 | 4.1.1 | CONTEXT | **ADDRESSED** ⚠ confirm no NDA |
| 142 | 4.1.2 | APPENDIX | VERIFIED-OK; diagram → P0050 |
| 143 | 4.1.2 | OUTDATED | **ADDRESSED** |
| 145 | 4.1.2 | VERIFY | **ADDRESSED** |
| 146 | 4.1.2 | OUTDATED | **ADDRESSED** |
| 148 | 4.1.3 | VERIFY | **ADDRESSED** |
| 149 | 4.1.3 | OUTDATED | **ADDRESSED** |
| 151 | 4.1.4 | SOURCE | **REGISTERED** (row 5) |
| 152 | 4.1.4 | OUTDATED | **ADDRESSED** |
| 153 | 4.1.4 | OUTDATED | **ADDRESSED** |
| 154 | 4.1.4 | VERIFY | **ADDRESSED** |
| 156 | 4.1.5 | SOURCE | **ADDRESSED** + REGISTERED (row 6) |
| 157 | 4.1.5 | VERIFY | **ADDRESSED** |
| 159 | 4.2 | CONTEXT | **ADDRESSED** |
| 161 | 4.2.1 | VERIFY/PROSE | **ADDRESSED** |
| 163 | 4.2.2 | VERIFY/PROSE | **ADDRESSED** |
| 165 | 4.2.3 | VERIFY/PROSE | **ADDRESSED** (two edits) |
| 167 | 4.2.4 | VERIFY/PROSE | **ADDRESSED** |
| 169 | 4.2.5 | APPENDIX | **ADDRESSED** (reduced table) + P0050 |
| 172 | 4.2.6 | VERIFY/PROSE | **ADDRESSED** |
| 173 | 4.2.6 | APPENDIX | **FLAGGED — Table 3 not re-verified** |
| 175 | 4.2.6 | VERIFY | **VERIFIED-OK** |
| 177 | 4.3 | VERIFY/UPDATE | **ADDRESSED** ⚠ confirm input count |
| 179 | 4.3 | — | **ADDRESSED** (same edit) |
| 180 | 4.3 | VERIFY/SOURCE | **ADDRESSED** |
| 181 | 4.3 | SOURCE | **ADDRESSED** — no debt |
| 183 | 4.4 | INCORRECT | staged — horizon note |
| 184 | 4.4 | SOURCE | **REGISTERED** (row 6, same claim) |
| 185 | 4.4 | INCORRECT | staged — horizon note |
| 187 | 4.4 | INCORRECT | staged — horizon note |
| 188 | 4.4 | VERIFY | staged — horizon note |
| 189 | 4.4 | SOURCE | **REGISTERED** (row 8) |
| 190 | 4.4 | METACOMMENT | NEEDS-BRIAN |
| 191 | 4.4 | INCORRECT | staged — horizon note |
| 193 | 4.5 | VERIFY/PROSE | **ADDRESSED** (three edits) |
| 194 | 4.5 | SOURCE | NEEDS-BRIAN — see §4.5 |

**Totals:** 30 addressed with prose · 2 verified-ok · 4 registered · 6 need a decision from
you · 1 flagged pending regeneration · 6 staged in the horizon note.

**§4.4's six threads** are not repeated here — full replacement prose is in
`srq1-forecast-horizon-defect-and-split-correction.md`. Apply §4.1 Edit 4 with it.
