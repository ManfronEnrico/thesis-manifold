# Comments — Data Assessment

Extracted 2026-09-05 from `MSc. Data Science - 175888 and 176171 - Master Thesis.docx`.
43 comment(s) in 43 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [131](#c131) | Data Assessment | FORMATTING |  | FORMATTING: Could use a subtitle for the chapter... |
| [133](#c133) | Overview and Data Strategy | ACADEMIC |  | ACADEMIC: Reading through the thesis from front to back i noticed that we kind o... |
| [134](#c134) | Overview and Data Strategy | INCORRECT |  | INCORRECT: This is not the reason it was scoped out. The fact table did exist, b... |
| [135](#c135) | Overview and Data Strategy | CONTEXT |  | CONTEXT: CSD is true, but the other categories were assessed for the pooled vs. ... |
| [136](#c136) | Overview and Data Strategy | VERIFY |  | VERIFY: The survey-type claim is a bit dodgy to me. This MUST be grounded in the... |
| [137](#c137) | Overview and Data Strategy | OUTDATED |  | OUTDATED: Not really true. We changed it to a proportial split, which is thus no... |
| [139](#c139) | Source, Type, and Access | FORMATTING |  | FORMATTING: Not really sure why randomly start to bold regular sentence words. W... |
| [140](#c140) | Source, Type, and Access | CONTEXT |  | CONTEXT: We never signed an NDA, not sure if we MUST supply this with our thesis... |
| [142](#c142) | Schema and Structure | APPENDIX |  | VERIFICATION & APPENDIX: Double check claims, and also we need a reference to th... |
| [143](#c143) | Schema and Structure | OUTDATED, APPENDIX |  | OUTDATED & VERIFICATION & APPENDIX: This must be updated. Also this table might ... |
| [145](#c145) | Schema and Structure | VERIFY |  | VERIFY... |
| [146](#c146) | Schema and Structure | OUTDATED |  | OUTDATED: We have an updated reasoning in the code for the period selection, wri... |
| [148](#c148) | Overall Suitability | VERIFY |  | VALIDATE: Not sure if that is actually still the case. Also again, perhaps we ad... |
| [149](#c149) | Overall Suitability | VERIFY, OUTDATED |  | OUTDATED & VERIFY: Again monthly updated database changes on re-pull.... |
| [151](#c151) | Precise Suitability | SOURCE |  | SOURCE... |
| [152](#c152) | Precise Suitability | OUTDATED, CONTEXT |  | CONTEXT & OUTDATED & VERIFICATION: Justification WHY as zero rather than null. A... |
| [153](#c153) | Precise Suitability | OUTDATED |  | OUTDATED & VERIFICATION... |
| [154](#c154) | Precise Suitability | VERIFY, OUTDATED |  | OUTDATED & VERIFY: I believe here we said that we cant be sure about it, or whet... |
| [156](#c156) | Forecasting Suitability | VERIFY, SOURCE, OUTDATED |  | OUTDATED & VERIFY & SOURCE... |
| [157](#c157) | Forecasting Suitability | VERIFY, SOURCE, OUTDATED |  | OUTDATED & VERIFY & SOURCE... |
| [159](#c159) | CSD - Worked Category (EDA and Parameters) | CONTEXT |  | METADATA & CONTEXT & VERIFICATION: Remove metadata „Brian …“. Justify why CSD, i... |
| [161](#c161) | Scope and Filtering | VERIFY, PROSE |  | VERIFY & PROSE & METADATA... |
| [163](#c163) | Stationarity | VERIFY, PROSE |  | VERIFY & PROSE & METADATA... |
| [165](#c165) | Seasonality | VERIFY, PROSE |  | VERIFY & PROSE & METADATA... |
| [167](#c167) | Autocorrelation and Lag Structure | VERIFY, PROSE |  | VERIFY & PROSE & METADATA... |
| [169](#c169) | Parameter Summary | VERIFY, PROSE, APPENDIX |  | VERIFY & PROSE & METADATA & Appendix: Againa a good candidate for a full appendi... |
| [172](#c172) | Per-category EDA - danskvand, energidrikke, R | VERIFY, PROSE |  | VERIFY & PROSE & METADATA: Here it referes to §4.6., which I assume is a metadat... |
| [173](#c173) | Per-category EDA - danskvand, energidrikke, R | VERIFY, APPENDIX |  | VERIFY & APPENDIX: Whole table verification and candidate for appendix or pretti... |
| [175](#c175) | Per-category EDA - danskvand, energidrikke, R | VERIFY |  | VERIFY... |
| [177](#c177) | Feature Engineering (forecasting substrate) | VERIFY, UPDATE |  | VERIFY & UPDATE: As we are thinking about including exogenous features (holiday ... |
| [179](#c179) | Feature Engineering (forecasting substrate) |  |  | VERIFICATION... |
| [180](#c180) | Feature Engineering (forecasting substrate) | VERIFY, SOURCE |  | VERIFY & SOURCE... |
| [181](#c181) | Feature Engineering (forecasting substrate) | SOURCE |  | SOURCE... |
| [183](#c183) | Train, Validation, and Test Split | INCORRECT |  | INCORRECT: Dynamic Train/Test/Val sets based on percentage cutoff.... |
| [184](#c184) | Train, Validation, and Test Split | SOURCE |  | SOURCE... |
| [185](#c185) | Train, Validation, and Test Split | INCORRECT |  | INCORRECT: Not locked... |
| [187](#c187) | Train, Validation, and Test Split | INCORRECT |  | INCORRECT... |
| [188](#c188) | Train, Validation, and Test Split | VERIFY |  | VERIFY... |
| [189](#c189) | Train, Validation, and Test Split | SOURCE |  | SOURCE... |
| [190](#c190) | Train, Validation, and Test Split | METACOMMENT |  | METACOMMENT... |
| [191](#c191) | Train, Validation, and Test Split | INCORRECT |  | INCORRECT... |
| [193](#c193) | Key Risks and Mitigations | VERIFY, PROSE |  | VERIFY & PROSE... |
| [194](#c194) | Key Risks and Mitigations | SOURCE |  | SOURCE: So far only one singular source in chapter 4. Needs more as can be seen ... |

---

<a id="c131"></a>

## [131] Brian Rohde -- Data Assessment  `FORMATTING`

- **Section:** Data Assessment
- **Date:** 2026-09-05T18:53:00
- **On:** “COULD USE A SUBTITLE”

FORMATTING: Could use a subtitle for the chapter

<a id="c133"></a>

## [133] Brian Rohde -- Data Assessment  `ACADEMIC`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:07:00
- **On:** “This thesis draws on one secondary data source in the sense of Saunders et al. (2023): data”

ACADEMIC: Reading through the thesis from front to back i noticed that we kind of repeat the same or similar information multiple times in different chapters.


I am not 100% positive if that is proper academic rigour, and supposed to be like that (e.g. allowing a reader to have some context in each chapter, while having the deep dive in the dedicated chapter), or if that is AI slop, a point for optimization. 


We might want to look at the thesis of my friend Max for reference (Graded 12/12). To see if they wrote in a similar fashion

<a id="c134"></a>

## [134] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:09:00
- **On:** “A fifth category, beer (totalbeer), was scoped out because its facts table is absent from the source data (the data do not exist at source, not a size or memory constraint); this is recorded as a data limitation rather than an analytical choice”

INCORRECT: This is not the reason it was scoped out.  The fact table did exist, but it was way too large for our laptops and internet connections to fetch, so we excluded it. So ist not a data limitation but an analytical choice, directly in conflict with your claim

<a id="c135"></a>

## [135] Brian Rohde -- Data Assessment  `CONTEXT`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:10:00
- **On:** “CSD is the worked category, assessed in full (Section 4.3); the other three are processed through the identical pipeline as parallel proofs of concept.”

CONTEXT: CSD is true, but the other categories were assessed for  the pooled vs. Specialized and potentially also the overall model performance (SRQ1 i believe). 


So just a bit more to-verify context neceassry

<a id="c136"></a>

## [136] Brian Rohde -- Data Assessment  `VERIFY`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:12:00
- **On:** “survey-type, structured, commercial secondary data”

VERIFY: The survey-type claim is a bit dodgy to me. This MUST be grounded in the metadata provided by nielsen. If not we cant claim it. I hardly believe it would be exclusively survey data, maybe not even at all, or more realistically a mix. But we cant outright claim with no evidence.

<a id="c137"></a>

## [137] Brian Rohde -- Data Assessment  `OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:13:00
- **On:** “The train, validation, and test split is then specified as a locked, pre-registered design decision applied identically across the forecasting models”

OUTDATED: Not really true. We changed it to a proportial split, which is thus not locked in and will move upon dataset update relatively speaking in absolute cutoff points.

<a id="c139"></a>

## [139] Brian Rohde -- Data Assessment  `FORMATTING`

- **Section:** Data Assessment > Overview and Data Strategy > Source, Type, and Access
- **Date:** 2026-09-03T13:15:00
- **On:** “is survey secondary data (a continuously maintained commercial scanner panel), structured (organised in a star schema), and quantitative”

FORMATTING: Not really sure why randomly start to bold regular sentence words. We should stay consistent, either propogate same formatting rules to the other chapters, or retain the bolding only for numbered lists, or headers.

<a id="c140"></a>

## [140] Brian Rohde -- Data Assessment  `CONTEXT`

- **Section:** Data Assessment > Overview and Data Strategy > Source, Type, and Access
- **Date:** 2026-09-03T13:15:00
- **On:** “confidentiality agreement with Manifold AI”

CONTEXT: We never signed an NDA, not sure if we MUST supply this with our thesis if we claim it to exist here.

<a id="c142"></a>

## [142] Brian Rohde -- Data Assessment  `APPENDIX`

- **Section:** Data Assessment > Overview and Data Strategy > Schema and Structure
- **Date:** 2026-09-03T13:26:00
- **On:** “Each category follows a star schema: dimension tables for market, period, and product, linked to a facts table at the grain of market × product × period. The facts table records the core sales metrics (sales value, sales in litres, sales units), their promotional variants (the same metrics under promotion), and a weighted-distribution metric that proxies product availability. The product dimension captures brand, manufacturer, packaging format, flavour or type, price tier, and corporate attribution.”

VERIFICATION & APPENDIX: Double check claims, and also we need a reference to the to-be generated data model.

<a id="c143"></a>

## [143] Brian Rohde -- Data Assessment  `OUTDATED * APPENDIX`

- **Section:** Data Assessment > Overview and Data Strategy > Schema and Structure
- **Date:** 2026-09-03T13:28:00
- **On:** “RTD | 37 | 93 | 0 ⚠️ | 42 | 589 | 511 | 2,193 | 44,449”

OUTDATED & VERIFICATION & APPENDIX: This must be updated. Also this table might be a good candidate to move into the appendix. Or at the least eh lengthy definitions and description.

<a id="c145"></a>

## [145] Brian Rohde -- Data Assessment  `VERIFY`

- **Section:** Data Assessment > Overview and Data Strategy > Schema and Structure
- **Date:** 2026-09-05T16:54:00
- **On:** “Per-category training structure, filtered to DVH EXCL. HD scope (2026-06-27)”

VERIFY

<a id="c146"></a>

## [146] Brian Rohde -- Data Assessment  `OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Schema and Structure
- **Date:** 2026-09-03T13:29:00
- **On:** “RTD have only 37–39 monthly periods, so a ≥40-observation filter retains zero brands for them; a single global threshold of ≥30 is therefore adopted across all categories (CSD 77, danskvand 24, energidrikke 27, RTD 42 brands), which is both feasible and consistent - preferable to the inherited mixed rule (40 for CSD, 30 for the rest). The bold column (≥30) is the retained set used downstream.”

OUTDATED: We have an updated reasoning in the code for the period selection, writing notes, or plans.

<a id="c148"></a>

## [148] Brian Rohde -- Data Assessment  `VERIFY`

- **Section:** Data Assessment > Overview and Data Strategy > Overall Suitability
- **Date:** 2026-09-03T13:30:00
- **On:** “the promotional variants and the weighted-distribution proxy serve as exogenous predictors.”

VALIDATE: Not sure if that is actually still the case. Also again, perhaps we add the holiday calendar enrichment

<a id="c149"></a>

## [149] Brian Rohde -- Data Assessment  `VERIFY * OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Overall Suitability
- **Date:** 2026-09-03T13:32:00
- **On:** “The temporal span is 37–42 months (CSD 42, energidrikke 39, danskvand and RTD 37), with complete intermediate calendar years constituting the primary training window. In-scope brand counts are 136 (CSD), 49 (danskvand), 64 (energidrikke), and 93 (RTD); in-scope SKU counts are 7,668, 453, 577, and 511 respectively (Table 4.1). After the ≥30-month retention filter, 77 / 24 / 27 / 42 brands remain for benchmarking, with 3,077 / 885 / 1,007 / 1,543 observed brand-month rows.”

OUTDATED & VERIFY: Again monthly updated database changes on re-pull.

<a id="c151"></a>

## [151] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Overview and Data Strategy > Precise Suitability
- **Date:** 2026-09-03T13:33:00
- **On:** “Nielsen is an established commercial panel provider whose continued operation depends on data credibility; its scanner data are therefore treated as reliable, while recognising that, as with any provider, definitions and collection conventions are fixed by Nielsen rather than by the researcher.”

SOURCE

<a id="c152"></a>

## [152] Brian Rohde -- Data Assessment  `OUTDATED * CONTEXT`

- **Section:** Data Assessment > Overview and Data Strategy > Precise Suitability
- **Date:** 2026-09-03T13:35:00
- **On:** “it is fully populated (0.00% null), with the absence of promotional activity encoded as a zero rather than a null”

CONTEXT & OUTDATED & VERIFICATION: Justification WHY as zero rather than null. Actually I believe our current code does the exact opposite, where we assigned zero meaning, and null genuinely absent (e.g. unrecorded). Please verify

<a id="c153"></a>

## [153] Brian Rohde -- Data Assessment  `OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Precise Suitability
- **Date:** 2026-09-03T13:35:00
- **On:** “Weighted-distribution nulls: negligible across all categories - 0.019% (CSD), 0.016% (danskvand), 0.093% (energidrikke), 0.000% (RTD).”

OUTDATED & VERIFICATION

<a id="c154"></a>

## [154] Brian Rohde -- Data Assessment  `VERIFY * OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Precise Suitability
- **Date:** 2026-09-03T13:36:00
- **On:** “Negative and zero values: negatives are return/correction adjustments standard in scanner data and are clipped to zero - they are rare (CSD 58 rows, 0.031%; danskvand 14, 0.057%; energidrikke 16, 0.032%; RTD 10, 0.022%).”

OUTDATED & VERIFY: I believe here we said that we cant be sure about it, or whether negative numbers are a measurement error or actually returns, so we floored negative numbers to 0.

<a id="c156"></a>

## [156] Brian Rohde -- Data Assessment  `VERIFY * SOURCE * OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Forecasting Suitability
- **Date:** 2026-09-03T13:37:00
- **On:** “37–42-month span exceeds the ARIMA minimum of roughly 24 periods for stable parameter identification and contains enough annual cycles for seasonality to be learned by both decomposition and gradient-boosted models.”

OUTDATED & VERIFY & SOURCE

<a id="c157"></a>

## [157] Brian Rohde -- Data Assessment  `VERIFY * SOURCE * OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Forecasting Suitability
- **Date:** 2026-09-03T13:37:00
- **On:** “by the ≥30-month filter (77 / 24 / 27 / 42 brands for CSD / danskvand / energidrikke / RTD), so that model comparisons are not confounded by very short series;”

OUTDATED & VERIFY & SOURCE

<a id="c159"></a>

## [159] Brian Rohde -- Data Assessment  `CONTEXT`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters)
- **Date:** 2026-09-03T13:39:00
- **On:** “CSD is the worked category. The structural counts and the stationarity, seasonality, and autocorrelation statistics below are recomputed locally under the DVH EXCL. HD scope (2026-06-23); the few items still taken from Brian’s all-markets audit are flagged. The other three categories are processed through the identical pipeline; per-category EDA replication under the corrected scope is pending (Section 4.6).”

METADATA & CONTEXT & VERIFICATION:


Remove metadata „Brian …“. Justify why CSD, if it even is, the worked category.

<a id="c161"></a>

## [161] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Scope and Filtering
- **Date:** 2026-09-03T13:39:00
- **On:** “Scope and FilteringMarket scope: DVH EXCL. HD (single Nielsen market level; see header). 187,907 facts rows fall in scope.Span: 42 monthly periods (Oct 2022–Mar 2026) on Nielsen’s 4-4-5 week calendar. (Period identifiers are not calendar-monotonic, so the span is taken from the documented window, not raw min/max.)Brands: 136 total; the adopted filter MIN_PERIODS ≥ 30 (≥30 non-zero monthly observations) retains 77 brands and 3,077 brand-month rows (of 3,789 total). A ≥40 filter would retain only 57 and is infeasible for the other three categories (37–39 periods → zero brands), so ≥30 is applied globally (Table 4.1). These figures are recomputed locally under DVH EXCL. HD and supersede Brian’s all-markets values (143 → 62 brands; 4,040 rows), inflated by the market double-count.Aggregation grain: brand × month, positive sales only; weighted distribution averaged rather than summed (correct for an ACV metric).”

VERIFY & PROSE & METADATA

<a id="c163"></a>

## [163] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Stationarity
- **Date:** 2026-09-03T13:40:00
- **On:** “StationarityADF test (aggregate monthly total, n = 42, DVH EXCL. HD): the level series is non-stationary in both raw (p = 0.360) and log form (p = 0.421); it becomes stationary only after first differencing (p < 0.001) - i.e. the series is difference-stationary, I(1). This revises Brian’s all-markets finding that the log level was stationary (p = 0.028): that does not hold at the corrected scope. (ADF power is limited at n = 42.)Treatment: a natural-log transform is applied to “sales_units” to stabilise variance; non-stationarity in the mean is handled by differencing for ARIMA and by lagged/rolling features for the tree models (which do not require a stationary level). NaN is preserved for non-positive/missing values rather than imputed.”

VERIFY & PROSE & METADATA

<a id="c165"></a>

## [165] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Seasonality
- **Date:** 2026-09-03T13:40:00
- **On:** “SeasonalityPeak months (share of annual units, DVH EXCL. HD): December (12.8%), March (10.9%), June (8.9%); September is next at 8.5%.Peak-month indicator: PEAK_MONTHS - months whose mean “sales_units” exceeds the category’s overall mean by more than 10%, measured per category. For CSD this gives {3, 6, 9, 12}. Renamed from HOLIDAY_MONTHS (2026-08-18). No holiday calendar is an input to the pipeline, so the former name asserted a cause the computation never established. The evidence often contradicts it: CSD’s peaks are the quarter-end months, consistent with retail trade loading rather than holidays.Now verified per category, resolving the open question: CSD {3, 6, 9, 12}; Danskvand {6, 7, 8, 9} (summer - bottled water); Energidrikke {3, 6, 9} (quarter-ends, no December peak); RTD {5, 6, 12}. Four distinct seasonal profiles, each commercially plausible for its category.The earlier {3, 6, 12} came from a top-quartile rule on monthly totals, which is confounded by how many brands were active in a month. The current rule uses means, which is not - the panel is unbalanced by construction. September enters CSD’s set under the corrected rule.”

VERIFY & PROSE & METADATA

<a id="c167"></a>

## [167] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Autocorrelation and Lag Structure
- **Date:** 2026-09-03T13:40:00
- **On:** “Autocorrelation and Lag StructureLag set: LAGS = (1, 2, 3, 4, 8, 13) and ROLLING_WINDOWS = (4, 13) (4-month and ~annual cycles on the Nielsen calendar).Autocorrelation (recomputed, DVH EXCL. HD): for the top brand by units (HARBOE, n = 42) the log-series ACF is +0.26 (lag 1), +0.47 (lag 3), and ≈0 (lag 13) - a strong quarterly (lag-3) signal but a weak annual (lag-13) one for this brand. Lag structure is clearly brand-dependent, so a single global lag set is a simplification; per-brand optimisation is out of scope. This revises Brian’s Coca-Cola example (lag-1 = −0.399), which was computed on the inflated all-markets series. Method note: the per-category figures in §4.3.6 (CSD lag-1 +0.78) use a pooled, brand-demeaned log series across all retained brands, whereas the HARBOE figures here are a single-brand series; the pooled estimate is larger because demeaning removes between-brand level differences and leaves the common short-horizon dynamics. Both are reported; the qualitative conclusion (positive short-horizon, near-zero annual carry) is robust to the method.Promotional intensity: strongly correlated with sales units, confirmed under DVH EXCL. HD at r = 0.937 (n = 2,442 promo-bearing brand-month rows), closely matching Brian’s all-markets value (r = 0.941); the relationship is robust to market scope. For energidrikke the promotional signal is even stronger (r = 0.988); danskvand and RTD carry no promotional data (promo-zero).”

VERIFY & PROSE & METADATA

<a id="c169"></a>

## [169] Brian Rohde -- Data Assessment  `VERIFY * PROSE * APPENDIX`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Parameter Summary
- **Date:** 2026-09-03T13:42:00
- **On:** “Parameter Summary”

VERIFY & PROSE & METADATA & Appendix:


Againa a good candidate for a full appendix table and only retaining a prettier / smaller / reduced table in prose, or just referencing the appendix figure and discussing the most crucial findings in prose.

<a id="c172"></a>

## [172] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Per-category EDA - danskvand, energidrikke, RTD
- **Date:** 2026-09-03T13:43:00
- **On:** “The three proof-of-concept categories were taken through the identical pipeline and their EDA recomputed under the corrected DVH EXCL. HD scope, closing the gap previously flagged in §4.6.”

VERIFY & PROSE & METADATA:


Here it referes to §4.6., which I assume is a metadata reference to some of our past plan / task metadata files. 


Especially because the actual section 4.6. in this report comes later (currently in 4.3.6.

<a id="c173"></a>

## [173] Brian Rohde -- Data Assessment  `VERIFY * APPENDIX`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Per-category EDA - danskvand, energidrikke, RTD
- **Date:** 2026-09-03T13:44:00
- **On:** “RTD | none (promo-zero) | December | BREEZER | p = 0.000 | stationary in level | +0.82 / +0.58”

VERIFY & APPENDIX:


Whole table verification and candidate for appendix or prettier / smaller table

<a id="c175"></a>

## [175] Brian Rohde -- Data Assessment  `VERIFY`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Per-category EDA - danskvand, energidrikke, RTD
- **Date:** 2026-09-03T17:13:00
- **On:** “Three of the four category-level series are difference-stationary (I(1)); RTD is already stationary in log level. All show strong positive short-horizon autocorrelation (lag-1 +0.55…+0.82), supporting the shared lag/rolling feature set, with near-zero lag-13 carry. Seasonality is category-appropriate (water peaks in summer, the others in autumn/spring). danskvand and RTD carry no promotional signal - the unmeasured-variable limitation already noted. MIN_PERIODS and LAGS transfer reasonably across categories. PEAK_MONTHS does not and is no longer treated as a transferable default: it is derived per category, and the four profiles differ materially (water peaks in summer, Energidrikke has no December peak). Per-series lag structure is brand-dependent and not separately optimised (a stated scope bound).”

VERIFY

<a id="c177"></a>

## [177] Brian Rohde -- Data Assessment  `VERIFY * UPDATE`

- **Section:** Data Assessment > Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:13:00
- **On:** “The feature matrix contains 22 columns: 14 modelling features per observation”

VERIFY & UPDATE: As we are thinking about including exogenous features (holiday calendar)

<a id="c179"></a>

## [179] Brian Rohde -- Data Assessment

- **Section:** Data Assessment > Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:23:00
- **On:** “Table 4 - Feature Engineering Overview”

VERIFICATION

<a id="c180"></a>

## [180] Brian Rohde -- Data Assessment  `VERIFY * SOURCE`

- **Section:** Data Assessment > Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:23:00
- **On:** “log_”sales_units” is the modelling target (the models predict log sales and exponentiate back), not an input feature - using it as a predictor would be trivial leakage; and weighted_distribution is the fourteenth input feature, while the raw promo_units column is carried through the matrix but is not itself a model input (only its derived “promo_intensity” is)”

VERIFY & SOURCE

<a id="c181"></a>

## [181] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:26:00
- **On:** “so the tree models handle NaN natively and the linear model receives a zero-fill at fit time.”

SOURCE

<a id="c183"></a>

## [183] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:27:00
- **On:** “calendar date and locked as a pre-specified design decision, applied identically across the forecasting models and across categories”

INCORRECT: Dynamic Train/Test/Val sets based on percentage cutoff.

<a id="c184"></a>

## [184] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:28:00
- **On:** “ARIMA minimum (~24 periods) and to contain at least two seasonal cycles for Prophet”

SOURCE

<a id="c185"></a>

## [185] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:28:00
- **On:** “The per-category boundaries, taken from the locked split files (<cat>_split_dates.json),”

INCORRECT: Not locked

<a id="c187"></a>

## [187] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:32:00
- **On:** “(locked, pre-registered)”

INCORRECT

<a id="c188"></a>

## [188] Brian Rohde -- Data Assessment  `VERIFY`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:32:00
- **On:** “CSD, the longest series, takes a 12-month test window covering a full annual cycle; the three shorter categories take an 8-month test window (a ≥40-month series would be needed for a 12-month test under the same rule)”

VERIFY

<a id="c189"></a>

## [189] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:33:00
- **On:** “ARIMA minimum (~24 periods; danskvand and RTD at 23 are marginally below”

SOURCE

<a id="c190"></a>

## [190] Brian Rohde -- Data Assessment  `METACOMMENT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:33:00
- **On:** “are flagged as a thin-data caveat in §4.6)”

METACOMMENT

<a id="c191"></a>

## [191] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:33:00
- **On:** “All test windows end in March 2026”

INCORRECT

<a id="c193"></a>

## [193] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > Key Risks and Mitigations
- **Date:** 2026-09-03T17:34:00
- **On:** “Figures verified (resolved). All structural, data-quality, and EDA figures in this chapter are recomputed locally from the data/raw parquets under the DVH EXCL. HD scope (2026-06-27), superseding the earlier P0023 audit values; no placeholders remain. Residual dependence is only on Brian’s final harmonised pipeline, against which the local figures are expected to reconcile.Market scope (resolved). Confirmed locally that the inherited “All Markets” aggregation double-counts (6.16× inflation for CSD; 14–17× for the other three categories, which expose 86 market levels). Resolved by scoping all four categories to the single DVH EXCL. HD market level; feature matrices regenerated accordingly (2026-06-23) under DVH EXCL. HD + MIN_PERIODS=30.Per-category EDA (resolved). All four categories now have a dedicated EDA recomputed under DVH EXCL. HD (§4.3.6): stationarity (three of four series I(1), RTD stationary in level), short-horizon autocorrelation (lag-1 +0.55…+0.82), seasonality, and promo correlation. MIN_PERIODS and LAGS transfer reasonably across categories; PEAK_MONTHS is derived per category rather than inherited, since the four seasonal profiles differ materially. Per-brand lag optimisation remains a stated scope bound.Thin training windows (danskvand, RTD). Both have only 23 training months, marginally below the ~24-period ARIMA rule of thumb, and danskvand has just 24 retained brands. Mitigation: these three categories are framed as parallel proofs of concept rather than primary evidence; CSD (42 periods, 77 brands) is the worked category carrying the main claims, and t […791 more characters — see the chapter file…] cibility is limited to processed features, code, and protocol.Generalisability bound. Findings are bounded to the DVH EXCL. HD scope, the available period window, and the fully observed series filter; applicability to other markets, intermittent series, or non-beverage categories is future research.”

VERIFY & PROSE

<a id="c194"></a>

## [194] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Key Risks and Mitigations
- **Date:** 2026-09-03T17:35:00
- **On:** “research”

SOURCE: So far only one singular source in chapter 4. Needs more as can be seen in the previous comments
