# Comments — Model Benchmark & Selection

Extracted 2026-09-05 from `MSc. Data Science - 175888 and 176171 - Master Thesis.docx`.
49 comment(s) in 49 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [233](#c233) | Model Benchmark & Selection | FORMATTING |  | FORMATTING: Could use a subtitle for the chapter... |
| [235](#c235) | Rationale for model selection | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [238](#c238) | Simple benchmarks | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [241](#c241) | ARIMA | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [243](#c243) | Prophet (Meta) | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [245](#c245) | LightGBM | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [247](#c247) | XGBoost | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [249](#c249) | Ridge regression | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [252](#c252) | Grain and data split | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [254](#c254) | Feature engineering | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [256](#c256) | Execution protocol | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [259](#c259) | Validation scheme | OUTDATED |  | OUTDATED... |
| [261](#c261) | Hyperparameter optimisation | VERIFY, SOURCE |  | VERIFY, SOURCES... |
| [263](#c263) | Evaluation metrics | VERIFY |  | VERIFY... |
| [265](#c265) | Why WMAPE is the primary metric | VERIFY, SOURCE, PROSE |  | VERIFY, PROSE, SOURCE... |
| [267](#c267) | Scorability, and what is excluded from what | VERIFY, SOURCE, TABLE-REFERENCE, PROSE |  | VERIFY, SOURCES, PROSE, TABLE REFERENCE... |
| [270](#c270) | Targets | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |
| [272](#c272) | Demand-pattern categorisation | VERIFY, SOURCE, TABLE-REFERENCE, PROSE |  | VERIFY, SOURCES, PROSE, TABLE REFERENCE... |
| [274](#c274) | Demand-pattern categorisation | NAMING |  | NAMING... |
| [277](#c277) | Results |  |  | META COMMENT... |
| [279](#c279) | Tabular-model benchmark | VERIFY, TABLE-REFERENCE |  | VERIFY & TABLE REFERENCE... |
| [281](#c281) | Tabular-model benchmark | VERIFY |  | VERIFY... |
| [282](#c282) | Tabular-model benchmark | VERIFY, SOURCE, METACOMMENT |  | VERIFY, METACOMMENT, SOURCE... |
| [283](#c283) | Tabular-model benchmark | VERIFY, SOURCE |  | VERIFY & SOURCE... |
| [285](#c285) | The simple benchmarks, and where they win | METACOMMENT, PROSE |  | METACOMMENT, PROSE... |
| [287](#c287) | The simple benchmarks, and where they win | VERIFY, NAMING |  | NAMING & VERIFY: Also wth is „Best tuned ML“?! Which one does it refer to? It do... |
| [288](#c288) | The simple benchmarks, and where they win | VERIFY, PROSE |  | VERIFY, PROSE... |
| [289](#c289) | The simple benchmarks, and where they win | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCE, PROSE... |
| [291](#c291) | Scaled error (MASE) | VERIFY, PROSE |  | VERIFY & PROSE... |
| [293](#c293) | Scaled error (MASE) | NAMING |  | NAMING... |
| [294](#c294) | Scaled error (MASE) | VERIFY |  | VERIFY... |
| [296](#c296) | Pooled versus per-category training | VERIFY, TABLE-REFERENCE |  | VERIFY, TABLE REFERENCE... |
| [297](#c297) | Pooled versus per-category training | VERIFY, FORMATTING |  | VERIFY, FORMATTING... |
| [299](#c299) | Pooled versus per-category training | NAMING |  | NAMING... |
| [300](#c300) | Pooled versus per-category training | VERIFY |  | VERIFY... |
| [301](#c301) | Pooled versus per-category training | VERIFY |  | VERIFY... |
| [303](#c303) | Results by demand pattern | PROSE, FORMATTING |  | PROSE, METACOMMENTS, FORMATTING... |
| [305](#c305) | Operational profile | VERIFY |  | VERIFY... |
| [307](#c307) | Prediction-interval calibration | VERIFY, PROSE, MATH |  | VERIFY, PROSE, MATH... |
| [308](#c308) | Prediction-interval calibration | VERIFY |  | VERIFY... |
| [310](#c310) | Remaining gaps | VERIFY, PROSE |  | VERIFY, PROSE... |
| [312](#c312) | Forecast stability across seeds | VERIFY, METACOMMENT, PROSE |  | METACOMMENT, PROSE, VERIFY... |
| [313](#c313) | Forecast stability across seeds | METACOMMENT, WATERMARK, ACADEMIC |  | WATERMARK, METACOMMENT, ACADEMIC... |
| [314](#c314) | Forecast stability across seeds | VERIFY, TABLE-REFERENCE |  | VERIFY, TABLE REFERENCE... |
| [316](#c316) | Forecast stability across seeds | VERIFY, METACOMMENT, NAMING |  | METACOMMENT, VERIFY, NAMING... |
| [317](#c317) | Forecast stability across seeds | WATERMARK, ACADEMIC |  | ACADEMIC, WATERMARK... |
| [319](#c319) | Model selection decision | VERIFY, PROSE |  | PROSE, VERIFY... |
| [322](#c322) | Connection to SRQs | VERIFY, NAMING, FORMATTING |  | NAMING, VERIFY, FORMATTING... |
| [323](#c323) | Outstanding decisions | VERIFY, METACOMMENT |  | VERIFY, METACOMMENT... |

---

<a id="c233"></a>

## [233] Brian Rohde -- Model Benchmark & Selection  `FORMATTING`

- **Section:** Model Benchmark & Selection
- **Date:** 2026-09-05T18:53:00
- **On:** “COULD USE A SUBTITLE”

FORMATTING: Could use a subtitle for the chapter

<a id="c235"></a>

## [235] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Rationale for model selection
- **Date:** 2026-09-05T15:22:00
- **On:** “Rationale for model selectionFive model families span the inductive-bias spectrum: classical statistical (ARIMA, Prophet), gradient boosting (LightGBM, XGBoost), regularised linear (Ridge), plus four parameter-free benchmarks (mean, naive, seasonal-naive, drift)Selection criteria: (a) established empirical performance on retail/FMCG panels; fit within the ≤8 GB sequential RAM budget; (c) interpretability sufficient for the SRQ4 scenario comparison; (d) diversity of inductive biasThe benchmark rung is required, not decorative. Hyndman & Athanasopoulos (2021, §5.2) define the four simple methods as benchmarks against which “any forecasting methods we develop will be compared … to ensure that the new method is better than these simple alternatives”. A forecasting result reported without them is unbenchmarkedEmpirical weight for that requirement comes from M4: of six pure machine-learning entries, none beat the statistical combination benchmark and only one beat Naïve2 (Makridakis et al., 2018, p. 803)NOT included, and why: deep sequence models (LSTM/N-BEATS) - RAM footprint incompatible with the ≤8 GB constraint, and infeasible under the HPO time budget on ~30 monthly observations per series”

VERIFY, SOURCES, PROSE

<a id="c238"></a>

## [238] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Model descriptions > Simple benchmarks
- **Date:** 2026-09-05T15:24:00
- **On:** “Four parameter-free methods, defined as in Hyndman & Athanasopoulos (2021, §5.2):Method | Forecast for horizon h || Mean | ŷ(T+h) = ȳ || Naive | ŷ(T+h) = y(T) || Seasonal naive | ŷ(T+h) = y(T+h−m(k+1)), with m the seasonal period and k = ⌊(h−1)/m⌋ || Drift | ŷ(T+h) = y(T) + h · (y(T) − y(1)) / (T−1) || Table 8 - Simple Benchmark Evaluation ParametersSeasonal naive is the decisive one for this panel. Monthly beverage demand has strong annual seasonality, which seasonal naive exploits with zero parameters. It is the direct test of whether a tuned model has learned seasonality or merely fitted it”

VERIFY, SOURCES, PROSE

<a id="c241"></a>

## [241] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Model descriptions > ARIMA
- **Date:** 2026-09-05T15:24:00
- **On:** “ARIMAClassical univariate time-series model in the Box–Jenkins frameworkRole: statistical baseline representing established traditional forecastingImplementation: statsmodels SARIMAX(order=(1,1,1)) on log sales, fitted per brand. A fixed order, not a search - pmdarima/auto_arima was unavailable in the environment. This is a stated limitation: ARIMA is not order-optimised, so its numbers are a floor for the family rather than its best achievable performanceRAM: ~0.5 MB measured; negligibleLimitation: assumes stationarity; univariate, so no promotional or calendar inputs”

VERIFY, SOURCES, PROSE

<a id="c243"></a>

## [243] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Model descriptions > Prophet (Meta)
- **Date:** 2026-09-05T15:24:00
- **On:** “Prophet (Meta)Additive decomposable model, y(t) = g(t) + s(t) + h(t) + ε - trend, seasonality, holidays (Taylor & Letham, 2018, p. 38, Eq. 1)Designed for forecasting at scale by analysts with domain rather than statistical expertise, targeting “piecewise trends, multiple seasonality, floating holidays” (pp. 37–38)No holiday calendar is supplied in this thesis, and none of the multi-seasonality machinery applies at month grainRAM: ~50–100 MB; acceptable”

VERIFY, SOURCES, PROSE

<a id="c245"></a>

## [245] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Model descriptions > LightGBM
- **Date:** 2026-09-05T15:25:00
- **On:** “LightGBMGradient boosting with leaf-wise tree growth and GOSS samplingRole: primary ML candidateRAM: ~18.7 MB measuredHPO: Optuna TPE, 100 trials, 4-fold expanding-window CV (§6.3.4)”

VERIFY, SOURCES, PROSE

<a id="c247"></a>

## [247] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Model descriptions > XGBoost
- **Date:** 2026-09-05T15:25:00
- **On:** “GBoostGradient boosting with level-wise growth and L1/L2 regularisationRole: ML alternative with a different regularisation strategyIdentical feature set to LightGBM for a controlled comparisonRAM: ~0.2 MB measuredHPO: identical protocol”

VERIFY, SOURCES, PROSE

<a id="c249"></a>

## [249] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Model descriptions > Ridge regression
- **Date:** 2026-09-05T15:25:00
- **On:** “Ridge regressionL2-regularised linear regression: minimises the penalised residual sum of squares, equivalently RSS subject to Σβ² ≤ t (Hastie et al., 2009, pp. 61–62, Eq. 3.41–3.42)Role: linear baseline - establishes whether non-linear models earn their complexityRAM: ~1.5 MB measured”

VERIFY, SOURCES, PROSE

<a id="c252"></a>

## [252] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Experimental setup > Grain and data split
- **Date:** 2026-09-05T15:25:00
- **On:** “Grain and data splitGrain: brand × month (DEC-GRAIN). The chain and region grains were evaluated and dropped; they are reported as a limitation and future work, not as a live dimensionTemporal train/validation/test split, no shufflingHorizon H = 3 monthsTest-set sizes: CSD 665 rows, RTD 372, energidrikke 308, danskvand 174”

VERIFY, SOURCES, PROSE

<a id="c254"></a>

## [254] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Experimental setup > Feature engineering
- **Date:** 2026-09-05T15:25:00
- **On:** “Feature engineeringLags: t−1, t−2, t−3, t−4, t−8, t−13 monthsRolling statistics: 4-month and 13-month mean; 4-month standard deviationCalendar: month, quarter, and a binary peak_month flag derived from the category’s own seasonal profile (months whose mean units exceed the category mean by more than 10%). No holiday calendar is used - the flag is measured from the sales distribution, not from calendar datesPromotional: “promo_intensity” (promotional share of units, clipped to [0,1], lagged one period). Available for CSD and energidrikke only - Nielsen reports no promotional measure for danskvand or RTD, so the feature is omitted rather than zero-filled, since a constant zero would assert that no promotion ranMissing lag values for short histories are left as NaN (handled natively by the tree models); Ridge receives a zero-fill at fit time”

VERIFY, SOURCES, PROSE

<a id="c256"></a>

## [256] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Experimental setup > Execution protocol
- **Date:** 2026-09-05T15:25:00
- **On:** “Execution protocolSequential execution: load → fit → predict → unload → gc.collect()Memory profiling via tracemalloc at each stage; peak RAM recorded per modelFixed seed (42) throughout; seed sensitivity is measured separately (§6.5)”

VERIFY, SOURCES, PROSE

<a id="c259"></a>

## [259] Brian Rohde -- Model Benchmark & Selection  `OUTDATED`

- **Section:** Model Benchmark & Selection > Experimental setup > Validation scheme
- **Date:** 2026-09-05T15:26:00
- **On:** “Validation schemeHyperparameters are selected by 4-fold expanding-window (rolling-origin) cross-validation, splitting on distinct periods rather than rows - the rows are brand-months, so a row-wise split would place the same month in training and validation for different brands. The training window grows forward and validation is the block immediately following it, so no model ever sees a period later than the one it predicts. The test split is untouched throughout.Rolling-origin evaluation successively advances the forecast origin instead of relying on a single split, which is vulnerable to “corruption by occurrences unique to that origin” (Tashman, 2000, p. 439). Because each fold refits from scratch, this is recalibration rather than mere updating - Tashman’s preferred procedure (p. 440).”

OUTDATED

<a id="c261"></a>

## [261] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE`

- **Section:** Model Benchmark & Selection > Experimental setup > Hyperparameter optimisation
- **Date:** 2026-09-05T15:26:00
- **On:** “Hyperparameter optimisationOptuna’s TPE sampler, 100 trials per model × category × objective. TPE models the configuration density conditional on performance, splitting observed trials into densities l(x) below and g(x) above a quantile threshold (Bergstra et al., 2011, p. 2549). Optuna supplies the define-by-run interface, sampling and pruning infrastructure (Akiba et al., 2019, p. 2623).The trial budget is justified empirically, not by convention. No trial-count convention exists in the HPO literature; the requirement scales with search-space dimensionality. The tuner therefore records the running best CV score per trial and reports the trial after which improvement becomes negligible. Measured plateaus range from 3 to 87 trials with a median near 16, so 100 trials comfortably contains the converged region for every configuration.”

VERIFY, SOURCES

<a id="c263"></a>

## [263] Brian Rohde -- Model Benchmark & Selection  `VERIFY`

- **Section:** Model Benchmark & Selection > Evaluation metrics
- **Date:** 2026-09-05T15:27:00
- **On:** “Metric | Definition | Rationale || WMAPE | Σ|y−ŷ| / Σ|y| × 100 | Primary. Volume-weighted, defined at zero actuals, and consistent for the median (see below) || Median APE | median(|y−ŷ|/y) over y > 0 | Robust per-series view; undefined where y = 0 || MASE | mean(|y−ŷ|) / in-sample MAE of the naive forecast, per series | Scale-free, defined at zero, and absolutely interpretable: < 1 beats a naive forecast || Coverage (80 / 90% PI) | share of actuals inside the interval | Calibration signal for SRQ2 || Median relative interval width | interval width ÷ actual | Reported beside coverage - see below || Peak RAM (MB) | tracemalloc peak | The operational constraint || Inference latency (ms) | wall-clock prediction time | Agent responsiveness || Plain mean MAPE is not reported. It is undefined against a zero actual and diverges to meaningless magnitudes near zero - on this panel it reaches 10¹³ - because percentage errors are “infinite or undefined if Yₜ = 0 … and have an extremely skewed distribution when any value of Yₜ is close to zero” (Hyndman & Koehler, 2006, p. 683).”

VERIFY

<a id="c265"></a>

## [265] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Evaluation metrics > Why WMAPE is the primary metric
- **Date:** 2026-09-05T15:28:00
- **On:** “Why WMAPE is the primary metricThe choice is not conventional but theoretical. A scoring function determines which functional of the predictive distribution an optimal forecast reports (Gneiting, 2011):absolute-error loss is minimised by the median (p. 746);pointwise absolute percentage error is minimised by the (−1)-median - a density reweighted by y⁻¹ - which biases forecasts systematically downward (pp. 746, 752);WMAPE aggregates absolute errors before dividing by total volume, so minimising it over a fixed evaluation sample is equivalent to minimising MAE, and is therefore consistent for the standard median.This predicts, rather than merely describes, the WMAPE/median-APE divergence reported throughout this chapter. The two metrics estimate different functionals, so agreement was never to be expected. It also explains why tuning against median APE costs 8–13 pp of WMAPE while buying only 2–3 pp of median APE: that objective targets the (−1)-median and underforecasts, which WMAPE penalises directly.”

VERIFY, PROSE, SOURCE

<a id="c267"></a>

## [267] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * TABLE-REFERENCE * PROSE`

- **Section:** Model Benchmark & Selection > Evaluation metrics > Scorability, and what is excluded from what
- **Date:** 2026-09-05T15:28:00
- **On:** “Between 14% and 29% of test rows per category have a zero actual, where APE is undefined. Two distinct decisions follow, and they are not the same rule:Rule | Applies to | Basis || Exclude zero-actual rows | Median APE and MAPE only | Mathematical - APE is undefined there || (nothing else) | - | - || Table 9 - Exclud Zero-Actual Rows DecisionWMAPE and MASE are computed on every row. Both are defined at zero actuals, so neither requires an exclusion, and none is applied.Irregular series are handled by categorisation rather than removal - see §6.4.4.”

VERIFY, SOURCES, PROSE, TABLE REFERENCE

<a id="c270"></a>

## [270] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Evaluation metrics > Targets
- **Date:** 2026-09-05T15:28:00
- **On:** “TargetsAccuracy target: none imported from the literature. Earlier drafts carried a ≤15% WMAPE target attributed to Ceran et al. (2024). Source-level verification (2026-08-25) found no such benchmark in that paper: the authors explicitly reject MAPE because their panel contains too many zero-demand observations for a percentage error to be well defined, and report WRMSSE, RMSE and MAE instead. The target is therefore withdrawn, and no claim that an external accuracy target is met or approached should be written anywhere in the thesisWhat replaces it: the simple benchmarks of §6.2.0, scored on this thesis’s own test rows (§6.5.2). This is the stricter test and needs no cross-study metric alignment - a target borrowed from a daily product-store study with a 15-day horizon was never comparable to brand × month at H=3 in any caseCalibration target: ≥85% empirical coverage for a nominal 90% interval - and interval width must be reported alongside, since an arbitrarily wide interval attains perfect coverage while carrying no decision-relevant information”

VERIFY, SOURCES, PROSE

<a id="c272"></a>

## [272] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * TABLE-REFERENCE * PROSE`

- **Section:** Model Benchmark & Selection > Evaluation metrics > Demand-pattern categorisation
- **Date:** 2026-09-05T15:29:00
- **On:** “Demand-pattern categorisationBrand-level demand on this panel ranges from steady weekly sellers to series with long gaps and highly variable order sizes. Reporting a single pooled accuracy figure across that range obscures more than it conveys, and thresholding the difficult series away would reproduce exactly the practice the metric literature objects to.Each brand is therefore classified using the scheme of Syntetos, Boylan and Croston (2005, p. 495), on two measured quantities with derived cut-offs:p - average inter-demand interval (periods per non-zero demand)CV² - squared coefficient of variation of non-zero demand sizes | CV² ≤ 0.49 | CV² > 0.49 || p ≤ 1.32 | smooth | erratic || p > 1.32 | intermittent | lumpy || Table 10 - NO IDEAThe thresholds are not tuned to this data: they mark where the relative accuracy ordering of Croston’s method, the Syntetos–Boylan Approximation and simple exponential smoothing changes. Classification uses train and validation periods only - deriving classes from test rows and then reporting test accuracy per class would leak.Category | smooth | erratic | intermittent | lumpy || CSD | 44 | 32 | 5 | 14 || RTD | 32 | 20 | 2 | 8 || energidrikke | 16 | 18 | 2 | 8 || danskvand | 16 | 9 | 3 | 1 || Table 11 - Category Resulting Distribution (230 brands)This categorises; it does not exclude. Accuracy is reported per class, so weak performance on lumpy series appears as a stated limitation rather than as an absence. That is the response Syntetos and Boylan’s own work recommends - their contribution is estimators for such series, not advice to discard them.”

VERIFY, SOURCES, PROSE, TABLE REFERENCE

<a id="c274"></a>

## [274] Brian Rohde -- Model Benchmark & Selection  `NAMING`

- **Section:** Model Benchmark & Selection > Evaluation metrics > Demand-pattern categorisation
- **Date:** 2026-09-05T16:08:00
- **On:** “Table 10 - NO IDEA”

NAMING

<a id="c277"></a>

## [277] Brian Rohde -- Model Benchmark & Selection

- **Section:** Model Benchmark & Selection > Results
- **Date:** 2026-09-05T15:38:00
- **On:** “All results are on the locked brand × month grain (DEC-GRAIN). The alternative brand × chain representation, and the granularity comparison built on it, were removed from the project by P0035 and no longer appear in this chapter.”

META COMMENT

<a id="c279"></a>

## [279] Brian Rohde -- Model Benchmark & Selection  `VERIFY * TABLE-REFERENCE`

- **Section:** Model Benchmark & Selection > Results > Tabular-model benchmark
- **Date:** 2026-09-05T15:52:00
- **On:** “Both gradient-boosted models were tuned with Optuna (TPE, 100 trials) against an expanding-window cross-validation objective, then scored once on the untouched test split. Because WMAPE and median APE are minimised by different functionals (§6.4.1), each model was tuned twice - once per objective - and both results are reported. cv_metrics.csv.”

VERIFY & TABLE REFERENCE

<a id="c281"></a>

## [281] Brian Rohde -- Model Benchmark & Selection  `VERIFY`

- **Section:** Model Benchmark & Selection > Results > Tabular-model benchmark
- **Date:** 2026-09-05T15:53:00
- **On:** “Table 12 - Performance Overview - Tuned WMAPE adn medMAPE”

VERIFY

<a id="c282"></a>

## [282] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * METACOMMENT`

- **Section:** Model Benchmark & Selection > Results > Tabular-model benchmark
- **Date:** 2026-09-05T15:54:00
- **On:** “The two objectives select different models and produce different rankings. Tuning for median APE improves that metric and degrades WMAPE, as the theory in §6.4.1 predicts: absolute-error loss is minimised by the median, while a pointwise percentage error is minimised by a lower functional. On energidrikke the effect is large - LightGBM tuned for medMAPE reaches 29.8% test WMAPE against 16.5% when tuned for WMAPE. A single “best model” number is therefore meaningless without naming the objective it was tuned against, which is why both are carried here.”

VERIFY, METACOMMENT, SOURCE

<a id="c283"></a>

## [283] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE`

- **Section:** Model Benchmark & Selection > Results > Tabular-model benchmark
- **Date:** 2026-09-05T15:54:00
- **On:** “Validation-to-test movement is substantial and is not hidden. energidrikke tunes to 10.6% in cross-validation and lands at 13.0–16.5% on test; RTD moves the other way on LightGBM. The gap is consistent with the selection bias documented in §6.3.5 - this protocol is not nested, so the cross-validation figure is an optimistically biased estimate of generalisation, to an unquantifiable degree (Cawley & Talbot, 2010).”

VERIFY & SOURCE

<a id="c285"></a>

## [285] Brian Rohde -- Model Benchmark & Selection  `METACOMMENT * PROSE`

- **Section:** Model Benchmark & Selection > Results > The simple benchmarks, and where they win
- **Date:** 2026-09-05T16:02:00
- **On:** “The four benchmarks of §6.2.0 were run on the same test rows. stat_baselines.csv.”

METACOMMENT, PROSE

<a id="c287"></a>

## [287] Brian Rohde -- Model Benchmark & Selection  `VERIFY * NAMING`

- **Section:** Model Benchmark & Selection > Results > The simple benchmarks, and where they win
- **Date:** 2026-09-05T16:07:00
- **On:** “Table 13 - Four Categories x 5 Model Performance”

NAMING & VERIFY:


Also wth is „Best tuned ML“?! Which one does it refer to? It doesnt seem like its jsut a focus column from the named approaches / models.

<a id="c288"></a>

## [288] Brian Rohde -- Model Benchmark & Selection  `VERIFY * PROSE`

- **Section:** Model Benchmark & Selection > Results > The simple benchmarks, and where they win
- **Date:** 2026-09-05T16:09:00
- **On:** “Two categories are not won by the tuned models, and this is the most important result in the section.On RTD, seasonal naive beats every tuned configuration - 27.3% against 31.8–36.1%. The most irregular category is the one where a method with no parameters wins.On danskvand, a plain Ridge regression reaches 10.9%, roughly half the tuned gradient-boosted error. danskvand is also the smallest panel (29 series, 174 test rows), where a high-capacity model has least to learn from.This is precisely the outcome the benchmark rung exists to detect. Hyndman and Athanasopoulos (2021, §5.2) recommend the simple methods as a standard against which any new method must justify itself; here they are not a formality but a live constraint, and reporting a headline ML number without them would have concealed that the thesis’s approach is beaten outright on half the categories.”

VERIFY, PROSE

<a id="c289"></a>

## [289] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Results > The simple benchmarks, and where they win
- **Date:** 2026-09-05T16:09:00
- **On:** “Prophet is applied outside its design regime and its numbers should not be read as a defect of the method. Taylor and Letham (2018) target daily business series with multiple seasonalities and holiday effects; at month grain, weekly seasonality does not exist, no holiday calendar is supplied, and yearly seasonality reduces to about twelve observations. Fitting a linear trend on log-transformed short series lets the trend extrapolate to extreme values on back-transformation, producing the 105.7% and 972.4% figures. This is a limitation of the application, not of Prophet, and is reported as such.Ridge requires clipping to be reportable. Unclipped, its energidrikke WMAPE is 2.8×10¹³ and its RTD WMAPE 2459%, because back-transformed linear extrapolation diverges. The clipped variant is what appears above; the raw values are retained in stat_baselines.csv because the instability is itself informative about linear models on this panel.”

VERIFY, SOURCE, PROSE

<a id="c291"></a>

## [291] Brian Rohde -- Model Benchmark & Selection  `VERIFY * PROSE`

- **Section:** Model Benchmark & Selection > Results > Scaled error (MASE)
- **Date:** 2026-09-05T16:10:00
- **On:** “WMAPE compares models within a category but says nothing about whether a category is forecastable at all. MASE answers that directly: below 1 beats the in-sample naive forecast. mase.csv.Category | Naive MASE | Seasonal-naive MASE | Naive median ASE || CSD | 0.95 | 1.63 | 0.39 || danskvand | 0.99 | 1.60 | 0.52 || energidrikke | 0.67 | 2.02 | 0.05 || RTD | 6.54 | 14.02 | 0.18 || Table 14 - Categories: MASE ComparisonRTD’s mean MASE of 6.54 against a median ASE of 0.18 is a distributional finding, not an accuracy one. The typical RTD series is forecast better than naive; the mean is carried by a small number of cells with very large scaled errors. Reporting only the mean would describe RTD as catastrophically unforecastable, and only the median would conceal that a few series are. Both are reported for this reason.Seasonal naive scores worse than naive on MASE in every category while winning on WMAPE for RTD - the two metrics weight differently (volume versus per-series scale), and the disagreement is surfaced rather than resolved by picking one.Pooled versus per-category trainingWhether one model trained across all four categories beats four category-specific models is SRQ1’s central design question. Both arms use the same 12-feature intersection, the same tuning protocol, and are scored on identical test rows, so they differ only in which rows they were trained on. pooled_summary.md.Category | LightGBM pooled → per-cat | XGBoost pooled → per-cat || CSD | 17.5% → 16.3% (per-cat better by 1.2 pp) | 16.6% → 15.3% (per-cat by 1.3) || danskvand | 21.4% → 23.7% (pooling wins 2.2  […54,758 more characters — see the chapter file…] , and calendar and seasonality signals (month, quarter, and a binary peak-month indicator derived from each category’s own observed seasonal profile); these complement the models’ autoregressive features (lagged sales and rolling statistics) derived from the historical sales series itself.↩︎Appendix”

VERIFY & PROSE

<a id="c293"></a>

## [293] Brian Rohde -- Model Benchmark & Selection  `NAMING`

- **Section:** Model Benchmark & Selection > Results > Scaled error (MASE)
- **Date:** 2026-09-05T16:10:00
- **On:** “Table 14 - Categories: MASE Comparison”

NAMING

<a id="c294"></a>

## [294] Brian Rohde -- Model Benchmark & Selection  `VERIFY`

- **Section:** Model Benchmark & Selection > Results > Scaled error (MASE)
- **Date:** 2026-09-05T16:11:00
- **On:** “RTD’s mean MASE of 6.54 against a median ASE of 0.18 is a distributional finding, not an accuracy one. The typical RTD series is forecast better than naive; the mean is carried by a small number of cells with very large scaled errors. Reporting only the mean would describe RTD as catastrophically unforecastable, and only the median would conceal that a few series are. Both are reported for this reason.Seasonal naive scores worse than naive on MASE in every category while winning on WMAPE for RTD - the two metrics weight differently (volume versus per-series scale), and the disagreement is surfaced rather than resolved by picking one.”

VERIFY

<a id="c296"></a>

## [296] Brian Rohde -- Model Benchmark & Selection  `VERIFY * TABLE-REFERENCE`

- **Section:** Model Benchmark & Selection > Results > Pooled versus per-category training
- **Date:** 2026-09-05T16:11:00
- **On:** “Whether one model trained across all four categories beats four category-specific models is SRQ1’s central design question. Both arms use the same 12-feature intersection, the same tuning protocol, and are scored on identical test rows, so they differ only in which rows they were trained on. pooled_summary.md.”

VERIFY, TABLE REFERENCE

<a id="c297"></a>

## [297] Brian Rohde -- Model Benchmark & Selection  `VERIFY * FORMATTING`

- **Section:** Model Benchmark & Selection > Results > Pooled versus per-category training
- **Date:** 2026-09-05T16:12:00
- **On:** “RTD | 35.8% → 35.1% (per-cat by 0.7) | 37.0% → 35.5% (per-cat by 1.5)”

VERIFY, FORMATTING

<a id="c299"></a>

## [299] Brian Rohde -- Model Benchmark & Selection  `NAMING`

- **Section:** Model Benchmark & Selection > Results > Pooled versus per-category training
- **Date:** 2026-09-05T16:12:00
- **On:** “Table 15 - Pooled vs Per Category Performance Differences”

NAMING

<a id="c300"></a>

## [300] Brian Rohde -- Model Benchmark & Selection  `VERIFY`

- **Section:** Model Benchmark & Selection > Results > Pooled versus per-category training
- **Date:** 2026-09-05T16:13:00
- **On:** “The answer is conditional, and the condition is data volume. Pooling wins on the two smallest panels (danskvand 174 test rows, energidrikke 308) and loses on the two largest (CSD 665, RTD 372). This is the expected transfer-learning trade-off: a small category borrows strength from the others, while a large one is diluted by them. The pattern holds for both model families, which is what makes it a finding rather than noise - though §6.5.9 shows the magnitudes here sit within seed noise, so the direction is the claim, not the pp values.”

VERIFY

<a id="c301"></a>

## [301] Brian Rohde -- Model Benchmark & Selection  `VERIFY`

- **Section:** Model Benchmark & Selection > Results > Pooled versus per-category training
- **Date:** 2026-09-05T16:14:00
- **On:** “Per-brand, the aggregate conceals wide disagreement. Broken out by demand class (pooled_perbrand_summary.md), pooling helps between 44% and 64% of brands depending on class and model - close to a coin flip everywhere. The aggregate deltas above are small differences between two distributions that overlap heavily.”

VERIFY

<a id="c303"></a>

## [303] Brian Rohde -- Model Benchmark & Selection  `PROSE * FORMATTING`

- **Section:** Model Benchmark & Selection > Results > Results by demand pattern
- **Date:** 2026-09-05T16:15:00
- **On:** “Using the Syntetos–Boylan–Croston partition of §6.4.4, the 230 brands divide into 108 smooth, 79 erratic, 12 intermittent and 31 lumpy. Nothing is excluded; irregular series are reported rather than filtered.The most informative fact here is an absence: 15 of the 31 lumpy brands have no test signal at all - their entire test window is zero. Pooling deltas for the lumpy class are computed on the 16 that remain, and any per-brand percentage statistic for the other 15 would be undefined. This is a property of the data that a volume threshold would have hidden by removing the brands quietly; the categorisation makes it visible and countable.For the classes with signal, pooling win-rates run 46–55% (smooth), 51–64% (erratic) and 44–56% (intermittent). No demand class shows a decisive pooling effect.”

PROSE, METACOMMENTS, FORMATTING

<a id="c305"></a>

## [305] Brian Rohde -- Model Benchmark & Selection  `VERIFY`

- **Section:** Model Benchmark & Selection > Results > Operational profile
- **Date:** 2026-09-05T16:16:00
- **On:** “Peak RAM on the largest matrix is in single-digit megabytes for every model - Ridge 5.5, LightGBM 8.0, XGBoost 0.1, ARIMA 0.3 MB - against the 8 GB sequential budget of SRQ1. The memory constraint is non-binding by three orders of magnitude at this data scale, which is a real answer to the research question and not a missing measurement: the constraint that motivated the question does not bite here.Latency is likewise immaterial: XGBoost fits in 0.97 s and predicts in 9.3 ms; LightGBM fits in 2.04 s and predicts in 15.9 ms. profiling.csv.”

VERIFY

<a id="c307"></a>

## [307] Brian Rohde -- Model Benchmark & Selection  `VERIFY * PROSE * MATH`

- **Section:** Model Benchmark & Selection > Results > Prediction-interval calibration
- **Date:** 2026-09-05T16:18:00
- **On:** “A split-conformal wrapper on the tuned model, calibrated on validation residuals in log space, gives the following on the untouched test split. calibration.csv.Category | Nominal | Empirical coverage | Median relative width | n calib || CSD | 90% | 89.6% | 3.3× | 665 || RTD | 90% | 89.0% | 3.1× | 372 || danskvand | 90% | 87.4% | 16.8× | 174 || energidrikke | 90% | 93.5% | 8.9× | 264 || CSD | 80% | 78.6% | 1.9× | 665 || RTD | 80% | 76.1% | 1.7× | 372 || danskvand | 80% | 70.7% | 3.5× | 174 || energidrikke | 80% | 82.5% | 3.3× | 264 || The half-width is the ⌈(n+1)(1−α)⌉/n empirical quantile of the calibration residuals - Algorithm 2 of Lei et al. (2018) - not the nominal (1−α) quantile. The finite-sample correction is what supports the distribution-free guarantee at finite n.”

VERIFY, PROSE, MATH

<a id="c308"></a>

## [308] Brian Rohde -- Model Benchmark & Selection  `VERIFY`

- **Section:** Model Benchmark & Selection > Results > Prediction-interval calibration
- **Date:** 2026-09-05T16:23:00
- **On:** “Coverage alone is the wrong success criterion, and this table shows why. An arbitrarily wide interval attains perfect coverage while carrying no decision-relevant information. danskvand meets its 90% coverage target only with intervals spanning roughly seventeen times the quantity being forecast, which no planner can act on. For danskvand and energidrikke, width - not coverage - is the binding constraint, and both are reported as limitations rather than averaged into a “well-calibrated” claim. At the 80% level danskvand additionally undercovers, at 70.7%.”

VERIFY

<a id="c310"></a>

## [310] Brian Rohde -- Model Benchmark & Selection  `VERIFY * PROSE`

- **Section:** Model Benchmark & Selection > Results > Remaining gaps
- **Date:** 2026-09-05T16:23:00
- **On:** “Remaining gapsThe ≤15% accuracy target has been withdrawn, not scored. Verification found the benchmark does not exist in the cited source (§6.4.3). Accuracy is therefore assessed against the simple benchmarks of §6.5.2 alone, on which two of four categories are beaten outright.The tuning protocol is not nested, so every cross-validation figure above is optimistically biased by an unquantified amount (§6.3.5).ARIMA and Prophet use a fixed specification per series rather than a per-series order search, on cost grounds. Their figures are a competent baseline, not the best attainable from those families.fig4_ram_budget is stale and contradicts §6.5.6.”

VERIFY, PROSE

<a id="c312"></a>

## [312] Brian Rohde -- Model Benchmark & Selection  `VERIFY * METACOMMENT * PROSE`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:23:00
- **On:** “Chapter 2 motivates evaluating the modelling substrate on accuracy, computational efficiency and stability, and SRQ1’s scope names stability as its fourth axis. This section supplies that measurement, which had not previously been made.Stability is measured as the coefficient of variation of the forecast for each (brand, month) cell across five random seeds, with data, splits, features and protocol held identical. Only the seed varies, driving Optuna’s sampler and the models’ own stochastic elements.”

METACOMMENT, PROSE, VERIFY

<a id="c313"></a>

## [313] Brian Rohde -- Model Benchmark & Selection  `METACOMMENT * WATERMARK * ACADEMIC`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:24:00
- **On:** “Two findings, and both matter more than the accuracy tables suggest.”

WATERMARK, METACOMMENT, ACADEMIC

<a id="c314"></a>

## [314] Brian Rohde -- Model Benchmark & Selection  `VERIFY * TABLE-REFERENCE`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:26:00
- **On:** “First, aggregate stability flatters the system by roughly three times. Aggregate WMAPE moves by about 4.7% of its own level across seeds, while the typical individual forecast moves by about 13%, and the ninetieth-percentile cell by 30–73%. Per-cell movements partly cancel within a volume-weighted sum, so a planner reading one brand’s number experiences considerably more run-to-run variability than a headline metric implies. Both figures are therefore reported; quoting only the aggregate would understate instability threefold.”

VERIFY, TABLE REFERENCE

<a id="c316"></a>

## [316] Brian Rohde -- Model Benchmark & Selection  `VERIFY * METACOMMENT * NAMING`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:27:00
- **On:** “Table 16 - Seed Stabiltiy across Models and Categories”

METACOMMENT, VERIFY, NAMING

<a id="c317"></a>

## [317] Brian Rohde -- Model Benchmark & Selection  `WATERMARK * ACADEMIC`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:26:00
- **On:** “Every input is identical; only the random seed differs. A per-category statement of which gradient-boosting model is best is therefore not a finding - it reports the outcome of one seed. §6.6 states the conclusion this supports instead.”

ACADEMIC, WATERMARK

<a id="c319"></a>

## [319] Brian Rohde -- Model Benchmark & Selection  `VERIFY * PROSE`

- **Section:** Model Benchmark & Selection > Model selection decision
- **Date:** 2026-09-05T16:28:00
- **On:** “The choice between LightGBM and XGBoost is not supported by this data. A five-seed sweep with every input held identical shows the winning model changes with the seed in all four categories (§6.5.7). Naming a winner per category would be reporting one seed’s outcome as a findingThe defensible claim is that the two are statistically indistinguishable here, the between-seed spread exceeding the between-model difference. This is a weaker headline but a true one, and it is useful: a practitioner deciding what to deploy can choose on operational grounds - training time, memory, tooling - rather than accuracyWhat the benchmark does support is the gap between families: both gradient boosters clearly beat Ridge and ARIMA on most categories, and clearly lose to seasonal naive on RTD. Those differences exceed the seed noise; the LightGBM-vs-XGBoost one does notThe served model carries its own track record. The forecast tool returns the selected model’s measured accuracy (WMAPE and median APE), both simple baselines for that category, and a conformal interval - so the consuming agent receives the forecast’s reliability alongside the forecastMetric disagreement is surfaced, not hidden. Where WMAPE and median APE rank models differently, the payload flags it rather than silently reporting oneEnsemble combination is evaluated as a separate scenario, not folded into this chapter’s selection. M4’s evidence that combinations outperform single models (Makridakis et al., 2018) motivates it, and treating it as its own rung is what makes the contribution measurable rather than assumed”

PROSE, VERIFY

<a id="c322"></a>

## [322] Brian Rohde -- Model Benchmark & Selection  `VERIFY * NAMING * FORMATTING`

- **Section:** Model Benchmark & Selection > Connection to SRQs
- **Date:** 2026-09-05T16:29:00
- **On:** “Table 17 - Modelling Contribution to Sub-Research Questions”

NAMING, VERIFY, FORMATTING

<a id="c323"></a>

## [323] Brian Rohde -- Model Benchmark & Selection  `VERIFY * METACOMMENT`

- **Section:** Model Benchmark & Selection > Outstanding decisions
- **Date:** 2026-09-05T19:31:00
- **On:** “decisions”

VERIFY, METACOMMENT
