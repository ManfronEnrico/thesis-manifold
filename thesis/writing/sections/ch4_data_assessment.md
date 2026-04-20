# Chapter 4 — Data Assessment
> Status: PROSE DRAFT — written from live Nielsen query results 2026-04-12
> Author: Claude Code (Sonnet 4.6) — requires human review before finalisation
> Word count target: ~10 standard CBS pages (~22,750 chars excl. spaces)
> Note: Section 4.3 (Indeks Danmark) based on documented data model; CSVs pending download.

---

## 4.1 Overview and Data Strategy

The empirical work of this thesis rests on two primary datasets: the Nielsen/Prometheus CSD scanner panel and the Indeks Danmark consumer survey. Both datasets were identified as the most appropriate sources for the research questions in Chapter 3, and this chapter presents the results of a systematic data quality assessment conducted on both sources prior to any modelling activity. For the Nielsen dataset, the assessment is grounded in live queries executed against the confirmed Microsoft Fabric data warehouse connection; for the Indeks Danmark dataset, the assessment is grounded in the documented data model, as the raw CSV files remain pending local download at the time of writing.

The two datasets serve complementary analytical roles. The Nielsen panel captures the observed outcomes of retail demand: it records what was sold, in what volume, through which retail channel, and in which time period. The Indeks Danmark survey captures the demand-side drivers behind those outcomes: it records who is buying, what motivates their category and brand choices, and how those attitudes are distributed across the Danish population. Together, the two sources enable a richer feature matrix than either source could provide alone, which is the empirical basis for the enrichment design evaluated in SRQ3.

The analytical strategy adopted in this chapter follows a sequential progression. First, each dataset is assessed on its own terms: schema structure, coverage, null rates, value distributions, and data quality flags. Second, the two datasets are considered jointly from a feature engineering perspective, with explicit attention to the temporal resolution mismatch that constrains the enrichment design. Third, the train, validation, and test split is specified and locked as a design decision, to be applied identically across all five forecasting models evaluated in Chapter 6. Fourth, the key risks arising from the data assessment are documented, together with their mitigations, to bound the scope of the empirical findings in Chapters 6 through 8.

---

## 4.2 Nielsen CSD Dataset

### 4.2.1 Source and Access

The Nielsen/Prometheus CSD dataset is provided by Manifold AI through its Prometheus reporting platform, which stores the data in a Microsoft Fabric data warehouse hosted on Microsoft Azure. Access is established through a Service Principal authentication flow using an Entra ID client credential, implemented in the `ai_research_framework/data/nielsen_connector.py` module. The connection uses the ODBC Driver 18 for SQL Server and encodes the Entra ID access token as a UTF-16-LE byte struct, as required by the pyodbc SQL_COPT_SS_ACCESS_TOKEN attribute (value 1256). The connection was confirmed operational on 12 April 2026, with all four views returning data.

The dataset covers the Carbonated Soft Drinks (CSD) product category in the Danish retail market. It follows a star schema comprising three dimension views and one fact view, all in the `dbo` schema of the `Nielsen_clean` database. Manifold AI has filtered the data to the CSD category scope; the full Prometheus platform covers a broader range of FMCG categories, but the four views used in this thesis are scoped to CSD by design.

### 4.2.2 Schema

The star schema is organised as follows. The market dimension view (`csd_clean_dim_market_v`) contains 28 rows, each representing a distinct Danish retail market or market aggregate, with columns for `market_id` and `market_description`. The period dimension view (`csd_clean_dim_period_v`) contains 42 rows, each representing one calendar month, with columns for `period_id`, `period_year`, `period_month`, and `date_key`. The product dimension view (`csd_clean_dim_product_v`) contains 2,057 rows representing individual SKUs, with 18 columns capturing brand, manufacturer, packaging format, flavour type, price category, and a set of binary flags for organic, private label, and regular versus light variants. The fact view (`csd_clean_facts_v`) contains 2,535,464 rows at the grain of market times product times period, with ten columns: the three foreign keys and seven sales metrics.

A technical note on period ordering is warranted. The `period_id` values in the period dimension are not monotonically sequential with calendar time; sorting by `period_id` alone does not produce a chronological sequence. All time-series operations in this thesis sort by the composite key `(period_year, period_month)` to ensure correct temporal ordering.

### 4.2.3 Coverage

The 28 markets in the dimension cover the full landscape of Danish grocery retail, from national chains to convenience and online channels. The primary analysis market for this thesis is DVH EXCL. HD (market_id 1256338), which aggregates Danish grocery retail excluding hard discount formats and represents the market definition adopted in Manifold AI's standard reporting. Additional markets include individual retailers (MENY, NETTO, REMA 1000, ALDI, BILKA, KVICKLY, SUPERBRUGSEN, SPAR, FØTEX), cooperative groupings (COOP, SALLING GROUP, DAGROFA), convenience channels (7-ELEVEN, CIRCLE K, GASOLINE/7-ELEVEN), and the online retailer NEMLIG.COM. All 28 markets are present in both the dimension and the fact table, with zero null values.

The 42 temporal periods span from October 2022 through March 2026, providing three and a half years of monthly data. The coverage within this range is complete: 2023 and 2024 are represented by all twelve calendar months, as is 2025; 2022 is represented by October through December only, and 2026 by January through March. This yields 42 fully populated periods with no missing months in the 2023, 2024, and 2025 calendar years, which constitute the primary training window.

The product dimension contains 2,057 SKUs representing 144 distinct brands and 114 distinct manufacturers. The category is structured by packaging format (plastic, can, glass, and other materials), flavour type (cola, orange, tonic, citrus or grape, lemon or lime, ginger beer, exotic, and other flavours), price category (branded and budget), organic status, private label status, and a regular versus light distinction. Corporate attribution is captured through the `corporation_ru_1` column, which assigns each SKU to one of seven corporate groups: Carlsberg, Royal Unibrew, Harboe, private label excluding Carlsberg, Vestfyn, third-party suppliers, and Aqua d'Or. The product dimension is complete: all 2,057 rows have zero null values across all 18 columns.

A product dimension mismatch was identified during the assessment: the facts table contains 8,522 distinct `product_id` values, while the product dimension contains 2,057 rows. The most probable explanation is that the `csd_clean_dim_product_v` view is scoped to the active product catalogue relevant to Manifold AI's current reporting, while the facts table retains the full transaction history including discontinued and out-of-scope SKUs. Joining the facts table to the product dimension on `product_id` is therefore the correct scoping mechanism and is applied throughout the modelling pipeline.

### 4.2.4 Data Quality Assessment

**Null rates.** The core sales metrics (`sales_value`, `sales_in_liters`, `sales_units`) have zero null values across all 2,535,464 rows. This confirms that every market-product-period combination recorded in the facts table has a valid sales observation, which is a prerequisite for reliable time-series modelling. The promotional metrics (`sales_value_any_promo`, `sales_in_liters_any_promo`, `sales_units_any_promo`) have a null rate of 39.48 per cent (1,001,078 rows). This null pattern is consistent with the interpretation that a null indicates the absence of promotional activity in that observation, rather than a missing data problem; the three promotional columns are null for the same set of rows, which rules out random data loss. The `weighted_distribution` column has a null rate of 15.42 per cent (391,035 rows), reflecting the fact that Nielsen does not track distribution for every product-market-period combination, typically in cases where the product has very limited or no shelf presence. Both null patterns are addressed in the preprocessing pipeline: promotional nulls are imputed as zero, and distribution nulls are imputed using the median distribution value for the same brand and market combination.

**Value distributions.** The core sales metrics exhibit a pronounced right-skew consistent with the aggregation structure of the data. The DVH composite markets (DVH EXCL. HD, DVH/CONVENIENCE INCL. HD) have very high absolute sales values, while individual retailer rows have much lower values. The mean `sales_units` is 66,495 but the standard deviation is 822,234, reflecting the extreme heterogeneity in scale across market types. A log transformation of sales targets is applied to all gradient-boosted and linear models before training to reduce the influence of scale heterogeneity on model estimation.

**Negative values.** A small proportion of rows contain negative values in the sales metrics: the minimum `sales_value` is negative 20,431 DKK, the minimum `sales_in_liters` is negative 4,293, and the minimum `sales_units` is negative 900. Negative values in scanner panel data represent return adjustments and correction entries, which are standard in retail data collection. The count of negative rows is small relative to the 2.5 million total rows. These values are clipped to zero in the preprocessing pipeline, as negative sales are not a meaningful input for demand forecasting models.

**Zero-sales rows.** Of the 2,535,464 fact rows, 52,919 (2.09 per cent) have `sales_units` equal to zero. This proportion is low and is consistent with the product-market-period combinations where a SKU was listed but not sold in a given period. Zero-sales observations are retained in the dataset and are flagged as true zeros, distinct from the negative correction entries described above. For ARIMA and Prophet, which are fitted on individual brand-level time series, periods with zero sales at the brand level are imputed using the preceding period value if isolated, or excluded if they form a gap of more than two consecutive months.

**Promotional activity.** Of the 2,535,464 rows, 890,269 (35.11 per cent) have a non-null, positive `sales_units_any_promo` value, indicating that promotional sales occurred. This proportion is substantial and confirms that promotional uplift is a meaningful feature engineering input for the CSD category. The promotional share varies considerably across brands and retailers, consistent with the known promotional intensity differences between branded and private-label CSD products.

**weighted_distribution.** This metric ranges from zero to one with a mean of 0.26 and a standard deviation of 0.35. The low mean reflects the fact that most product-market-period combinations have limited distribution coverage; for niche or regional brands, distribution at the national market level is typically below 0.10. For the top five brands in DVH EXCL. HD, distribution values are consistently high (above 0.80), confirming that distribution is not a limiting factor for the core modelling scope.

### 4.2.5 Forecasting Suitability

The assessment confirms that the Nielsen dataset is suitable for all five forecasting models planned in this thesis. The core sales metrics are complete, the time horizon of 42 monthly periods exceeds the minimum of 24 required for stable ARIMA parameter identification, and the three seasonal cycles embedded in the training window are sufficient for both additive decomposition models and gradient-boosted tree models to learn annual seasonality patterns.

Of the 28 markets, the DVH EXCL. HD aggregate market has the most complete brand-level time series. An analysis of brand-level coverage within DVH EXCL. HD shows that the five highest-volume brands (HARBOE, COCA COLA, PEPSI, FAXE KONDI, and FANTA) each have observations across all 42 periods, with no missing months. Jolly, Tuborg Squash, Schweppes, Hancock, and Fever Tree also have full 42-period coverage. These brands represent the primary forecasting targets in the model benchmark chapter. Of the 144 brands in the full catalogue, 779 brand-times-market series have observations in all 42 periods; the remaining series have shorter coverage due to market entry, exit, or intermittent distribution, and are excluded from the benchmark evaluation to ensure that model comparisons are not confounded by time-series length differences.

The broad distribution of time-series lengths across brand-market combinations, ranging from 1 to 42 periods, is relevant for the generalisation claims of the evaluation. The benchmark results reported in Chapter 6 apply specifically to the subset of fully observed series (42 periods) in the DVH EXCL. HD market. The applicability of those results to shorter, more intermittent series is a direction for future research rather than a claim of this thesis.

---

## 4.3 Indeks Danmark Consumer Survey

### 4.3.1 Source and Access

The Indeks Danmark dataset is an annual consumer survey covering the Danish adult population. It is provided in three CSV files: a main data file containing respondent-level observations, a codebook file mapping variable codes to labels and descriptions, and a metadata file documenting survey methodology and variable classifications. The main data file contains 20,134 rows and 6,364 columns; the codebook contains 6,364 rows and 11 columns; and the metadata file contains 29,185 rows and 3 columns. The dataset has been received by the research team. The CSV files require local download from a shared drive before they can be integrated into the preprocessing pipeline; this step is documented as a pending item in the project status log.

Access to the Indeks Danmark dataset is subject to a confidentiality arrangement with Manifold AI. The data is used solely within the local research environment and is not transmitted to external systems. The dataset contains survey weights and demographic variables, which are treated as sensitive data under the project's data governance policy.

### 4.3.2 Data Structure

The survey covers a broad range of consumer attitudes, behaviours, and sociodemographic characteristics relevant to the Danish market. Variables pertinent to the CSD category include product category usage frequency, brand preference intensity, retail channel shopping frequency, health consciousness indicators, price sensitivity measures, and lifestyle segment identifiers. The dataset is cross-sectional, capturing consumer attitudes at a single point in time, which has a direct methodological consequence for the enrichment design: Indeks Danmark signals cannot be used as dynamic time-varying predictors in the forecasting models. They are instead used as static enrichment features that capture structural differences in consumer demand profiles across the retailer segments covered by the Nielsen panel, as described in Section 4.4.

The estimated RAM requirement for the main data file is approximately 970 megabytes, which represents a significant share of the 8-gigabyte budget. Loading the full 6,364-column matrix in memory simultaneously with the Nielsen training data and a fitted gradient-boosted model is not feasible within the constraint. The preprocessing pipeline therefore implements a two-stage approach: in the first stage, a subset of CSD-relevant variables is selected from the main data file using the codebook, and a reduced variable matrix is cached to disk; in the second stage, only the reduced matrix is loaded during model training. This approach ensures that the combined memory footprint remains within the 8-gigabyte budget, consistent with the architectural design documented in Chapter 5.

### 4.3.3 Variable Selection and Consumer Segmentation

The 6,364 variables in the Indeks Danmark main file cover the full range of consumer survey content, the majority of which is not relevant to CSD demand forecasting. The variable selection step filters the codebook to identify variables related to carbonated beverage consumption, soft drink brand preferences, grocery retail channel usage, health and sustainability attitudes, and price sensitivity. The target is a reduced set of approximately 50 to 100 variables that capture the dimensions most directly predictive of CSD demand variation across consumer segments.

From the reduced variable set, a consumer segmentation is derived through a two-step dimensionality reduction and clustering procedure. Principal component analysis reduces the selected variables to a set of principal components explaining at least 80 per cent of the total variance; typically, between 10 and 15 components are required to reach this threshold for consumer survey data. K-means clustering is then applied to the component scores, with the number of clusters determined by the elbow criterion applied to within-cluster sum of squares across a range of 2 to 8 clusters. Prior work on consumer segmentation in retail contexts has identified 4 to 6 segments as the empirically optimal range for national consumer panels of this scale (Kasem et al., 2023; Stylianou and Pantelidou, 2025), and the segmentation in this thesis targets that range.

Each resulting consumer segment is characterised by its centroid profile on the principal components, which is then interpreted in terms of the original variable labels to produce a managerially meaningful description. The segment profiles are the basis for the retailer mapping step described in Section 4.4.

### 4.3.4 Retailer Mapping

The Indeks Danmark survey includes variables on retail channel and retailer shopping frequency, which enable a probabilistic assignment of consumer segments to Nielsen market segments. For each Nielsen market in the analysis scope, the share of each consumer segment is estimated from the survey's channel shopping frequency variables, weighted by the survey's population weights. The result is a retailer-level demand profile vector that summarises the consumer segment composition of the shopper base for each retail channel.

This mapping is a proxy construction rather than a direct linkage. There is no row-level correspondence between individual survey respondents and individual retail transactions; the mapping is based on aggregated segment profiles and channel-level shopping frequency distributions. The measurement error introduced by this proxy is acknowledged as a limitation in Chapter 3 and its potential effect on the SRQ3 enrichment evaluation is discussed in Chapter 8. The absence of a direct individual-level linkage means that the true predictive value of consumer survey data for CSD demand forecasting may be understated by the enrichment evaluation, as the proxy mapping introduces noise that a direct linkage would not.

---

## 4.4 Feature Engineering

### 4.4.1 Time-Series Features

For all five forecasting models, the preprocessing pipeline constructs a set of time-series features derived from the Nielsen facts table. The features are computed at the brand-times-market granularity used in the benchmark evaluation. Autoregressive features include lagged values of `sales_units` at lags of one, two, three, four, eight, and thirteen months, capturing short-term autocorrelation, medium-term trend, and the seasonal pattern at roughly one quarter. Rolling statistics include the four-month rolling mean and standard deviation, and the thirteen-month rolling mean, which approximates a trailing annual average. Calendar features include month of year, quarter, and a binary indicator for Danish public holidays, which fall within specific calendar months and have documented effects on CSD purchasing patterns in the Scandinavian market.

Promotional features include the `sales_units_any_promo` variable (imputed to zero where null) and the ratio of promotional to total sales, which captures promotional intensity. The `weighted_distribution` variable is included as a feature after imputation, capturing the availability dimension of demand. These features are applied to LightGBM, XGBoost, and Ridge Regression; ARIMA and Prophet are fitted as univariate models without the full feature set, consistent with their specification as statistical baselines.

| Feature | Description | Models |
|---|---|---|
| `lag_1` to `lag_4` | Sales at t-1, t-2, t-3, t-4 months | LightGBM, XGBoost, Ridge |
| `lag_8`, `lag_13` | Medium-term lags | LightGBM, XGBoost, Ridge |
| `rolling_mean_4m` | 4-month rolling average | LightGBM, XGBoost, Ridge |
| `rolling_std_4m` | 4-month rolling standard deviation | LightGBM, XGBoost, Ridge |
| `rolling_mean_13m` | 13-month rolling average | LightGBM, XGBoost, Ridge |
| `month` | Calendar month (1–12) | All |
| `quarter` | Calendar quarter | All |
| `is_danish_holiday_month` | Danish public holiday in this month | All |
| `promo_sales_units` | Units sold under promotion (0 if no promo) | LightGBM, XGBoost, Ridge |
| `promo_intensity` | Ratio of promo to total units | LightGBM, XGBoost, Ridge |
| `weighted_distribution` | Distribution level 0–1 (imputed) | LightGBM, XGBoost, Ridge |

### 4.4.2 Consumer Signal Features

The Indeks Danmark enrichment introduces three additional features at the retailer level, derived from the segmentation and mapping procedure described in Section 4.3. The `consumer_demand_index` is a composite score reflecting the CSD demand propensity of the primary consumer segment for each retailer, normalised to a zero-to-one scale. The `segment_id` is the categorical identifier of the dominant consumer segment for each retailer. The `trend_direction` captures whether the consumer demand index for the relevant segment changed positively, neutrally, or negatively in the most recent survey wave compared to a reference period, providing a directional enrichment signal.

These three features are static within the training window: because the Indeks Danmark survey is cross-sectional, they do not vary across time periods. Their contribution to model performance is therefore limited to capturing cross-retailer structural differences in demand levels and is not expected to improve the modelling of within-retailer temporal variation. This limitation is central to the ablation evaluation design described in Chapter 8.

| Feature | Description | Source |
|---|---|---|
| `consumer_demand_index` | Retailer-level CSD demand propensity index | Indeks Danmark |
| `segment_id` | Dominant consumer segment for this retailer | Indeks Danmark |
| `trend_direction` | Directional demand signal (up, flat, down) | Indeks Danmark |

---

## 4.5 Train, Validation, and Test Split

The temporal split is defined by calendar date and locked as a pre-specified design decision, applied identically across all five forecasting models. No random shuffling is applied at any stage; the strict temporal split is required to preserve the autocorrelation structure of the time series and to prevent information leakage from future observations into the training or validation windows.

The 42 monthly periods, sorted chronologically from October 2022 through March 2026, are divided as follows. The training set comprises 29 periods from October 2022 through February 2025, representing 69 per cent of the available data. The validation set comprises 6 periods from March 2025 through August 2025, representing 14 per cent. The test set comprises 7 periods from September 2025 through March 2026, representing 17 per cent.

The training window of 29 months satisfies the ARIMA minimum requirement of 24 periods for stable parameter identification and provides two complete seasonal cycles, which is the minimum required for Prophet's automatic seasonality detection. For LightGBM and XGBoost, the 29-month training window is generous relative to the feature matrix dimension, which is bounded by the number of autoregressive lags and rolling statistics constructed from the training history. The validation set of 6 months is used exclusively for model selection and hyperparameter optimisation; it does not inform any final performance estimates. The test set of 7 months is held out until the final evaluation reported in Chapter 8 and is used for all performance metrics reported in the thesis.

The choice of September 2025 as the test set start date is deliberate. It places the test window in the most recent data available, which includes the period most relevant to Manifold AI's operational planning horizon. It also ensures that the test set covers at least one full seasonal cycle of the autumn and winter months, in which promotional activity in the Danish CSD category tends to be elevated.

---

## 4.6 Key Risks and Mitigations

The data assessment has identified five risks relevant to the empirical chapters. Each risk is documented with its estimated likelihood, its potential impact on the research findings, and the mitigation strategy adopted in this thesis.

**Promotional null imputation.** The 39.48 per cent null rate in the promotional columns requires a deliberate imputation decision. Imputing nulls as zero assumes that a null indicates the absence of promotional activity, which is consistent with the structure of scanner panel data collection. However, if a subset of nulls reflects genuine data collection gaps rather than true absence of promotions, the imputation would introduce systematic downward bias in the promotional feature. The risk is judged as low, because the three promotional columns are null for exactly the same rows, which is more consistent with a structural absence pattern than with random data loss.

**weighted_distribution imputation.** The 15.42 per cent null rate in the distribution column requires imputation before use as a feature. The median imputation strategy adopted here preserves the central tendency for each brand-market combination but ignores time variation in distribution. For brands with rapidly changing distribution in the null periods, this imputation may understate the predictive value of the distribution signal. The risk is judged as moderate for niche brands and low for the top five brands, which have near-complete distribution coverage.

**Consumer-to-retailer segment mapping accuracy.** The proxy mapping of Indeks Danmark consumer segments to Nielsen retailer segments introduces measurement error that cannot be directly quantified without a ground-truth linkage. The magnitude of this error depends on the correlation between the survey's channel shopping frequency variables and the actual demographic composition of each retailer's shopper base. If the correlation is weak, the enrichment features will carry little predictive information and the ablation evaluation will show minimal enrichment value, which is a valid empirical finding rather than a modelling failure. The risk is judged as moderate.

**Indeks Danmark CSV download delay.** The consumer enrichment evaluation (SRQ3) cannot proceed until the Indeks Danmark CSV files are available locally. If the download is delayed beyond the empirical work schedule, the SRQ3 evaluation will be conducted after the SRQ1 and SRQ2 evaluations and will not affect the model benchmark or synthesis module chapters. The risk is judged as low in terms of the overall thesis schedule, as SRQ3 is designed to be modular and does not block the completion of Chapters 6 or 7.

**Scope boundary for generalisability.** All findings in Chapters 6 through 8 are bounded to the brand-times-DVH EXCL. HD scope, the 42-period window, and the fully observed series filter. The performance of the five forecasting models on shorter or more intermittent series, on other Danish retail markets, or on other FMCG categories is not evaluated in this thesis. This is not a risk to the internal validity of the findings but is a bound on their external validity, and it is documented explicitly in Chapter 8.

---

## References cited in this chapter

- Kasem, M. S., Hamada, M., and Taj-Eddin, I. (2023). Customer profiling, segmentation, and sales prediction using AI in direct marketing. *Neural Computing and Applications*. https://doi.org/10.1007/s00521-023-09339-6
- Stylianou, T., and Pantelidou, A. (2025). A machine learning approach to consumer behavior in supermarket analytics. *Decision Analytics Journal*, *16*, Article 100600. https://doi.org/10.1016/j.dajour.2025.100600
