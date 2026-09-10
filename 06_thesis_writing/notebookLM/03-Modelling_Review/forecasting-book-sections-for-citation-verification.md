# Forecasting Book Sections for Citation Verification

## Purpose

This document identifies sections of Hyndman and Athanasopoulos's *Forecasting: Principles and Practice* (3rd ed.) that may support, qualify, or challenge claims in the current draft of **Chapter 5 — Model Benchmark & Selection**.

The sections were selected from the book's chapter outlines and opening previews. A section's inclusion here means that it is a **candidate source**, not that it has already been confirmed to support the thesis wording. The relevant section PDFs should be supplied to NotebookLM together with the chapter draft so that every claim can be checked against the full source text.

## Short print list

### Essential — print first

#### Chapter 5 — The Forecaster's Toolbox

- 5.2 Some simple forecasting methods
- 5.5 Distributional forecasts and prediction intervals
- 5.6 Forecasting using transformations
- 5.8 Evaluating point forecast accuracy
- 5.9 Evaluating distributional forecast accuracy
- 5.10 Time series cross-validation

#### Chapter 9 — ARIMA Models

- 9.1 Stationarity and differencing
- 9.5 Non-seasonal ARIMA models
- 9.6 Estimation and order selection
- 9.7 ARIMA modelling in fable
- 9.9 Seasonal ARIMA models

#### Chapter 13 — Some Practical Forecasting Issues

- 13.3 Ensuring forecasts stay within limits
- 13.4 Forecast combinations
- 13.7 Very long and very short time series
- 13.8 Forecasting on training and test sets

These 15 sections are the smallest defensible print set. They cover the benchmark definitions, accuracy evaluation, prediction intervals, transformations, temporal validation, ARIMA specification, forecast constraints, combinations, and short-series limitations that are central to the draft.

### Important — print if time permits

#### Chapter 5

- 5.3 Fitted values and residuals
- 5.4 Residual diagnostics

#### Chapter 7 — Time Series Regression Models

- 7.4 Some useful predictors
- 7.5 Selecting predictors
- 7.6 Forecasting with regression

#### Chapter 8 — Exponential Smoothing

- 8.6 Estimation and model selection

#### Chapter 9

- 9.10 ARIMA vs ETS

#### Chapter 11 — Forecasting Hierarchical and Grouped Time Series

- 11.1 Hierarchical and grouped time series
- 11.3 Forecast reconciliation

#### Chapter 12 — Advanced Forecasting Methods

- 12.2 Prophet model
- 12.5 Bootstrapping and bagging

### Less crucial / optional

#### Chapter 2 — Time Series Graphics

- 2.3 Time series patterns
- 2.4 Seasonal plots
- 2.5 Seasonal subseries plots
- 2.7 Lag plots
- 2.8 Autocorrelation

#### Chapter 3 — Time Series Decomposition

- 3.1 Transformations and adjustments
- 3.2 Time series components

#### Chapter 4 — Time Series Features

- 4.1 Some simple statistics
- 4.2 ACF features
- 4.3 STL features

#### Chapter 6 — Judgmental Forecasts

- 6.1 Beware of limitations
- 6.2 Key principles
- 6.7 Judgmental adjustments

#### Chapter 10 — Dynamic Regression Models

- 10.6 Lagged predictors

#### Chapter 13

- 13.9 Dealing with outliers and missing values

## Detailed section-to-claim analysis

| Priority | Book subsection | Draft location | Claim or decision to examine | What NotebookLM should verify |
|---|---|---|---|---|
| Essential | **§5.2 Some simple forecasting methods** | §§5.1, 5.2.1, 5.4.3, 5.5.2 | Mean, naïve, seasonal-naïve, and drift are appropriate benchmarks; their equations; new methods should be compared with simple alternatives. | Verify every equation and whether the authors explicitly recommend these methods as benchmarks. Return the precise supporting passages and locations. |
| Essential | **§5.8 Evaluating point forecast accuracy** | §§5.4–5.5.5 | MAPE is problematic at zero and near-zero actuals; MASE is scale-free; MASE below 1 indicates improvement over its scaling benchmark; metrics may rank forecasts differently. | Verify each property, including the exact denominator used for MASE, and compare it with the thesis implementation. |
| Essential | **§5.10 Time series cross-validation** | §§5.3.1, 5.3.4, 5.3.5, 5.5.1 | Validation must preserve temporal order; training observations precede validation observations; rolling-origin evaluation uses several origins. | Verify terminology and logic. Determine whether the section supports multi-step blocks and period-level panel splits or only the general principle. |
| Essential | **§5.5 Distributional forecasts and prediction intervals** | §§5.4, 5.5.7, 5.6 | Prediction intervals represent forecast uncertainty and nominal coverage has a probabilistic interpretation. | Verify definitions of forecast distributions, prediction intervals, and coverage. Do not attribute conformal finite-sample guarantees to this section unless explicitly discussed. |
| Essential | **§5.9 Evaluating distributional forecast accuracy** | §§5.4, 5.5.7 | Coverage alone is insufficient; useful intervals must also be sufficiently narrow or sharp. | Check whether the section discusses calibration, sharpness, interval width, interval scores, or the coverage–width trade-off. Identify any recommended metric. |
| Essential | **§5.6 Forecasting using transformations** | §§5.2.2–5.2.3, 5.5.2, 5.5.7 | Models fitted on log sales require back-transformation; back-transformed means and medians may differ; bias adjustment may be relevant. | Verify the exact effects of log transformation and back-transformation and whether they help explain the extreme Prophet/Ridge results. |
| Essential | **§9.1 Stationarity and differencing** | §5.2.2 | The draft says that ARIMA “assumes stationarity.” | Check whether this should instead say that an appropriately differenced series is assumed to be stationary. |
| Essential | **§9.5 Non-seasonal ARIMA models** | §5.2.2 | `order=(1,1,1)` is used as the classical univariate ARIMA baseline. | Verify the interpretation of ARIMA(1,1,1). Check whether `SARIMAX` needs clarification when no exogenous predictors or seasonal order are used. |
| Essential | **§9.6 Estimation and order selection** | §§5.2.2, 5.5.8; outstanding decisions | A fixed ARIMA(1,1,1) is not order-optimised and does not represent the family's best achievable performance. | Verify normal order-selection practice, including AICc and the difference between selecting differencing orders and selecting p and q. Assess whether “floor for the family” is defensible wording. |
| Essential | **§9.7 ARIMA modelling in fable** | §§5.2.2, 5.5.8; outstanding decisions | Automatic order selection could provide a stronger ARIMA comparator than the fixed specification. | Identify the automatic-selection procedure and whether it searches seasonal terms. Do not assume another software package implements the identical procedure. |
| Essential | **§9.9 Seasonal ARIMA models** | §§5.2.1–5.2.2, 5.5.2 | The data are monthly and strongly seasonal, but the reported ARIMA has no seasonal order. | Determine whether monthly seasonal data may require seasonal ARIMA terms. Assess whether the model must be labelled **non-seasonal ARIMA** and whether comparison with seasonal naïve is structurally disadvantaged. |
| Essential | **§13.3 Ensuring forecasts stay within limits** | §§5.2.3, 5.5.2 | Ridge forecasts were clipped after back-transformed extrapolations became implausible; sales forecasts should remain non-negative. | Identify recommended methods for positive or bounded forecasts. Determine whether post-hoc clipping is supported or transformation-based constraints are preferable. |
| Essential | **§13.4 Forecast combinations** | §§5.1, 5.6; outstanding decisions | Forecast combinations may outperform individual models and could justify a separate experimental scenario. | Verify the general evidence and recommended combination methods. Check whether simple averaging and combination intervals are discussed. |
| Essential | **§13.7 Very long and very short time series** | §§5.5.2, 5.5.4, 5.5.5, 5.5.8 | Small panels and short brand histories provide complex models with less information and may favour simpler models. | Verify how length, parameter count, randomness, and estimation error affect model suitability. Check whether this supports the proposed explanation for Ridge winning on the smallest panel. |
| Essential | **§13.8 Forecasting on training and test sets** | §§5.3.1, 5.3.4, 5.5.1 | Final performance must be evaluated on untouched test observations, while CV and test results serve different purposes. | Verify the book's recommendations and whether it warns against selecting and evaluating models on the same observations. |
| Important | **§5.3 Fitted values and residuals** | §§5.3–5.5 | In-sample fit should not be treated as genuine forecast performance. | Distinguish residuals, fitted errors, validation errors, and test forecast errors. |
| Important | **§5.4 Residual diagnostics** | §5.2.2; remaining gaps | A competent ARIMA baseline normally involves diagnostic assessment in addition to test accuracy. | Identify recommended residual properties and tests, especially residual autocorrelation and Ljung–Box testing. Determine whether absent diagnostics should be a limitation. |
| Important | **§7.4 Some useful predictors** | §5.3.2 | Calendar variables, seasonal indicators, lags, and promotional intensity are used as predictors. | Match only genuinely equivalent predictor types discussed by the book. |
| Important | **§7.5 Selecting predictors** | §§5.2.6, 5.3.2 | Ridge is a regularised linear baseline and tabular models use a controlled feature set. | Check general predictor-selection and overfitting principles. Do not use this as support for Ridge regularisation unless Ridge is actually discussed. |
| Important | **§7.6 Forecasting with regression** | §§5.3.2, 5.7 | Regression forecasting may require future values or scenarios for calendar and promotional predictors. | Identify which predictors must be known or separately forecast over the three-month horizon. Flag unresolved deployment-time availability. |
| Important | **§8.6 Estimation and model selection** | §§5.1, 5.2, 5.5.2 | The benchmark includes ARIMA and Prophet but omits ETS. | Determine whether ETS is presented as a broad, selectable family suitable for trend/seasonal series and whether omission weakens the claimed model-family coverage. |
| Important | **§9.10 ARIMA vs ETS** | §§5.1–5.2, 5.6 | The draft calls ARIMA the traditional statistical baseline and claims broad inductive-bias coverage. | Verify that ETS and ARIMA are complementary. Assess whether ETS should be included or at least acknowledged as an omitted classical family. |
| Important | **§11.1 Hierarchical and grouped time series** | §§5.3.1, 5.5.4, 5.7 | Sales can be aggregated across brand, category, chain, and region; the thesis fixes brand × month and compares pooled with category-specific training. | Determine whether the data are hierarchical, grouped, or crossed. Clarify that pooled training is not itself forecast reconciliation. |
| Important | **§11.3 Forecast reconciliation** | §§5.5.4, 5.7; limitations | Forecasts across aggregation levels may need to add up coherently, but reconciliation is not evaluated. | Verify coherent forecasting and reconciliation definitions. Use primarily to frame a limitation or future-work opportunity. |
| Important | **§12.2 Prophet model** | §§5.2.3, 5.5.2 | Prophet uses trend, seasonality, and holiday components; the thesis supplies no holiday calendar and applies it at monthly grain. | Verify Prophet's components and applicable seasonal structures. Test the strong claim that Prophet is “outside its design regime”; soften it if the source does not justify that conclusion. |
| Important | **§12.5 Bootstrapping and bagging** | §§5.5.9, 5.6 | Forecast instability across seeds and a possible ensemble scenario raise the question of variance reduction through aggregation. | Determine whether bagging is presented as stabilising or improving forecasts. Do not equate bootstrap variation with random-seed variation without explicit justification. |
| Optional | **§2.3 Time series patterns** | §§5.2.1, 5.3.2 | Annual seasonality is central to monthly beverage demand. | Determine what empirical evidence is required to establish seasonality and whether the draft should point to an earlier plot or diagnostic. |
| Optional | **§§2.4–2.5 Seasonal plots and seasonal subseries plots** | §5.3.2 | `peak_month` is derived from the category's seasonal profile. | Determine whether these plots provide an accepted exploratory basis and check whether calculating the profile on the full sample would leak test information. |
| Optional | **§§2.7–2.8 Lag plots and autocorrelation** | §§5.2.2, 5.3.2 | Lagged features and ARIMA capture temporal dependence. | Check whether these sections support diagnosing relevant lags and annual dependence. They cannot alone justify the exact chosen lag set. |
| Optional | **§3.1 Transformations and adjustments** | §§5.2.2–5.2.3, 5.5.2 | Log sales are modelled and later transformed back to the original scale. | Check variance stabilisation, zero handling, skewness, and retransformation implications. |
| Optional | **§3.2 Time series components** | §§5.2.1, 5.2.3, 5.3.2 | Seasonal naïve and Prophet encode trend and seasonality differently. | Verify foundational definitions only if the chapter needs them. |
| Optional | **§§4.1–4.3 Simple statistics, ACF features, and STL features** | §§5.3.2, 5.4.4 | Series characteristics might explain cross-brand model performance. | Identify useful descriptive features, but do not substitute them for the Syntetos–Boylan demand classification. |
| Optional | **§§6.1, 6.2, 6.7 Judgmental forecasting principles and adjustments** | §§5.6–5.7; later SRQ4 experiment | An LLM interprets and may contextualise or adjust a statistical forecast. | Assess principles for disciplined judgmental adjustment. This is more relevant to the later LLM experiment than the benchmark chapter. |
| Optional | **§10.6 Lagged predictors** | §5.3.2 | Lagged promotion and sales features avoid reliance on unknown contemporaneous inputs. | Distinguish lagged external predictors from autoregressive target features and verify any discussion of delayed effects. |
| Optional | **§13.9 Dealing with outliers and missing values** | §§5.3.2, 5.5.5 | Missing initial lag values are retained for tree models and zero-filled for Ridge. | Check whether the recommended treatment applies. Distinguish missing raw observations from structurally unavailable initial lags. |

## Main issues the source review should resolve

### 1. The reported ARIMA model is non-seasonal

The chapter treats annual seasonality as central to monthly beverage demand but implements `SARIMAX(order=(1,1,1))` without a seasonal order. NotebookLM should determine whether the draft should:

- label this explicitly as a **fixed, non-seasonal ARIMA(1,1,1) baseline**;
- avoid implying it is representative of a tuned ARIMA/SARIMA family;
- describe the comparison with seasonal naïve as potentially disadvantaging ARIMA; and
- strengthen the limitation or rerun the benchmark with seasonal/order selection.

### 2. ETS is absent from the claimed model-family spectrum

The draft claims that its chosen families span the inductive-bias spectrum, but it omits exponential smoothing/ETS. Sections 8.6 and 9.10 should be used to determine whether the claim should be narrowed, ETS should be added, or its omission should be acknowledged explicitly.

### 3. Prophet may be described too strongly

The statement that Prophet was applied “outside its design regime” may be stronger than the cited literature supports. NotebookLM should separate:

- what Prophet was designed to model;
- which inputs and seasonal components were absent here;
- the empirical failure observed in this thesis; and
- the authors' interpretation of why it failed.

The last point should be presented as an inference unless directly supported by a source or diagnostic evidence.

### 4. Clipping and back-transformation need methodological support

The Ridge results are reported only after clipping, while raw predictions diverged after back-transformation. The review should determine whether the book supports clipping, recommends transformation-based constraints instead, and requires explicit reporting of the clipping bounds and procedure.

### 5. Coverage should not stand alone

The chapter already reports interval width alongside coverage. NotebookLM should check whether §5.9 supports this logic and whether a proper interval score would provide a stronger evaluation than separate coverage and relative-width figures.

### 6. Internal section references appear inconsistent

The attached file is Chapter 5, but several references point to Chapter 6 sections, including `§6.3.4`, `§6.4.1`, `§6.5.2`, and `§6.6`. These cross-references should be corrected independently of citation verification.

## NotebookLM verification instructions

Use the thesis chapter and the printed book sections as the only authoritative materials for this task. Review the candidate claims in the table above.

For every thesis statement that could rely on Hyndman and Athanasopoulos:

1. Quote the complete thesis sentence being assessed.
2. Classify it as **supported**, **partially supported**, **unsupported**, or **contradicted**.
3. Identify the exact book section and page shown in the uploaded PDF.
4. Provide a short source excerpt containing the evidence.
5. Explain precisely which part of the thesis sentence is or is not supported.
6. Propose a minimally changed replacement sentence when needed.
7. State when a sentence is the thesis authors' own inference rather than a claim made by the source.
8. Do not infer support from a section title, example, or general topic alone.
9. Do not attribute claims about conformal prediction, WMAPE consistency, Optuna, LightGBM, XGBoost, Ridge regularisation, Prophet's original design intentions, or demand-pattern classification to this book unless the supplied text explicitly covers them.
10. Flag secondary citations: if the book attributes a claim to another study, identify that study so the original source can be checked where necessary.

Return the result as a table with these columns:

| Thesis location | Thesis claim | Verdict | Book section/page | Evidence | Problem | Recommended revision | Original source needed? |
|---|---|---|---|---|---|---|---|

## Citation metadata to verify

The screenshots identify the source as:

> Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts.

The online version shown in the supplied metadata screenshot reports a later update date than the 2021 print version. Citation details and page references must therefore match the exact PDFs used. Section numbers are safer than page numbers when citing the changing online edition, while page numbers should be taken directly from the printed PDF pages supplied to NotebookLM.
