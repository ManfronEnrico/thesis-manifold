---
aliases:
learning_text_title: "M5 accuracy competition: Results, findings, and conclusions"
learning_text_venue: International Journal of Forecasting
learning_text_doi: 10.1016/j.ijforecast.2021.11.013
learning_text_apa7: "Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*, *38*(4), 1346–1364. https://doi.org/10.1016/j.ijforecast.2021.11.013"
learning_list_authors:
  - Makridakis, S.
  - Spiliotis, E.
  - Assimakopoulos, V.
learning_list_topic:
  - Retail Sales Forecasting
  - LightGBM
  - Hierarchical Forecasting
  - Exogenous Variables
  - Machine Learning Forecasting
  - Forecasting Competitions
  - Cross-Learning
learning_list_srq:
  - SRQ1
  - SRQ2
  - SRQ3
learning_list_chapter:
  - Ch.2
  - Ch.3
  - Ch.6
learning_number_release_year: 2022
note_list_type: Regular_Note
note_list_status: complete
note_list_relevance: High
note_list_read_depth: full
tags:
learning_date_read_date: 2026-03-22
cssclasses:
---

# AI Assessment
---
## In one sentence

The M5 competition, conducted on 42,840 hierarchical Walmart retail sales series, establishes that LightGBM — used by all top 50 competitors — dominates statistical benchmarks by 14–20% in WRMSSE, that exogenous/explanatory variables significantly improve retail forecasting accuracy, and that cross-learning across many correlated series is the mechanism enabling ML's superiority in this domain — a direct reversal of M4's finding that pure ML underperformed.

## Core Ideas
- LightGBM's dominance in hierarchical retail sales forecasting is empirically definitive in M5 — used by all top 50 competitors; the top 5 methods achieved 20%+ improvement over the best statistical benchmark — but this dominance is domain-specific: it depends on having many correlated series, promotional/calendar exogenous signals, and sufficient data for cross-learning
- The M4-to-M5 reversal is explained by data structure: M4 had diverse, mostly univariate series with no exogenous variables; M5 had hierarchical retail data with many correlated products, stores, and calendar events — precisely the conditions where LightGBM's ability to process numerous correlated series and exogenous variables pays off
- Exogenous/explanatory variables were explicitly confirmed as important for improving forecasting accuracy in M5 — promotional events, calendar indicators, and product metadata were among the key external signals leveraged by top methods
- Combining remained valuable even on top of LightGBM — the simple combination of the five best level-specific methods (COMB) improved over the single winning submission by up to 8.9%, confirming that ensemble aggregation is complementary to strong base models

## Methods
- 42,840 hierarchical time series: unit sales of 3,049 Walmart products across stores and states (USA), 12 aggregation levels
- Daily sales data; 28-day forecast horizon
- Performance metric: Weighted RMSSE (WRMSSE) — revenue-weighted, scale-independent, handles intermittent demand with zeros
- Kaggle platform competition: March–June 2020; reproducibility verified by organisers (≤2% WRMSSE deviation required)
- Models: predominantly LightGBM-based pipelines with exogenous calendar and promotional features; deep learning alternatives (DeepAR, N-BEATS) also represented

## Key findings — cite these
- LightGBM was used by all top 50 competitors — the first M competition where all top-performing methods were ML-based
- Top 50 methods achieved >14% better WRMSSE than the most accurate statistical benchmark; top 5 achieved >20%
- Exogenous/explanatory variables were key — promotional events, calendar variables, and hierarchical metadata contributed substantially to top-method accuracy
- Combining the five best level-specific methods (COMB) improved over the winning team by up to 8.9% at the most aggregated level — ensemble combination still adds value over single best ML model
- Cross-learning (global model trained across all series simultaneously) was identified as an essential driver of LightGBM's performance

## Direct quotes — copy verbatim, include page/section
> "LightGBM is a decision tree-based ML approach with reportedly superior forecasting performance compared with all other alternatives and it was used in practice by all of the top 50 competitors." (Section 1, p. 1347)

> "The 50 top-performing methods achieved more than 14% better performance compared with the most accurate statistical benchmark and more than 20% better for the top five." (Section 6, p. 1361)

> "Exogenous/explanatory variables were important for improving the forecasting accuracy of time series methods." (Section 6, p. 1362)

> "It was demonstrated that LightGBM can be used to effectively process numerous correlated series and exogenous/explanatory variables, and reduce the forecast error." (Section 6, p. 1361)

> "M5 is the first M competition in which all of the top-performing methods were both ML methods and better than all of the statistical benchmarks and their combinations." (Section 6, p. 1361)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): Directly and foundationally relevant — M5 provides the strongest empirical justification for including LightGBM in the thesis benchmark model set; the retail domain specificity (hierarchical sales, promotional patterns, correlated series) maps closely to the Nielsen CSD scanner data context; cite to justify why LightGBM is the primary ML candidate in Ch.6
- **SRQ2** (multi-agent coordination and recommendations): Relevant — M5 confirms that combining remains beneficial even over strong individual ML models; the synthesis module's multi-model aggregation is supported by the empirical evidence that COMB improved over the winning single submission by up to 8.9%
- **SRQ3** (contextual information improving AI capabilities): Directly relevant — M5 explicitly confirms that exogenous/explanatory variables improved retail forecasting accuracy; this is the strongest empirical precedent for including Indeks Danmark consumer survey signals as contextual enrichment in the thesis forecasting pipeline; cite in Ch.3 and Ch.6 when justifying the external signal enrichment design

## Where this goes in our thesis
- **Ch.2, Section 2.X (ML for Retail Forecasting)**: Cite alongside M4 to establish the ML-vs-statistical narrative — M4 showed pure ML underperformed general time series; M5 showed ML dominates retail hierarchical sales; the thesis sits in the M5 domain (retail scanner data), making LightGBM the evidence-based default ML choice
- **Ch.3, Section 3.X (Model Selection Rationale)**: Cite as primary empirical justification for selecting LightGBM as the thesis's main gradient boosting candidate — not a design choice but an evidence-based selection
- **Ch.6, Section 6.X (Model Benchmark Interpretation)**: Cite when interpreting benchmark results — if LightGBM outperforms ARIMA/Prophet in the thesis benchmark, M5 is the context that explains why; if it underperforms (due to data scarcity), M5 explains the boundary conditions (cross-learning requires many series)
- **Ch.3/Ch.7, Exogenous Variables Section**: Cite when justifying the Indeks Danmark enrichment design — M5 is the empirical precedent that exogenous signals improve retail forecasting accuracy in exactly this type of dataset

## What this paper does NOT cover (gap it leaves)

M5 uses daily Walmart data with thousands of products and stores — cross-learning is feasible at this scale; the thesis operates on ~36 monthly Nielsen CSD observations across a much smaller product-retailer matrix, where LightGBM's cross-learning advantage may not materialise, and statistical methods (ARIMA, Prophet) may remain competitive; this scale-dependent boundary condition is a genuine contribution the thesis can make to the M5 finding.

## Strength
- International Journal of Forecasting (ABS 3); the authoritative empirical benchmark for retail ML forecasting — citing M5 for LightGBM justification in a retail thesis is both necessary and sufficient as primary evidence
- Domain alignment with the thesis is the strongest of any competition paper: hierarchical retail sales data with promotional events and exogenous calendar variables is structurally analogous to Nielsen CSD scanner data
- M5 result on exogenous variables (Section 6 conclusion) is a citable empirical precedent specifically for the Indeks Danmark enrichment contribution

## Weaknesses
- Daily granularity and thousands of Walmart products enable cross-learning that may not transfer to the thesis's monthly CSD data across ~28 retailers — the sample size boundary condition is unexplored in M5
- Exogenous variables in M5 are promotional/calendar indicators (internal to retail operations), not external consumer sentiment surveys — the Indeks Danmark enrichment is a step beyond M5's exogenous variable scope and may not perform equivalently
- Deep learning alternatives (DeepAR, N-BEATS) are noted as competitive but not elaborated — more recent methods (Chronos, TFT) would require citing M5 as historical context rather than current state of the art

## My critical assessment
Makridakis et al. (2022) are directly relevant to this thesis as they provide domain-specific evidence that machine learning—particularly LightGBM—can outperform statistical methods in retail forecasting when leveraging hierarchical structure and exogenous variables. This finding supports the thesis’ use of ML models as core predictive components within a broader decision-support pipeline, especially given the structural similarity between M5 data and retail scanner datasets. The paper’s key contribution—demonstrating the effectiveness of cross-learning across correlated series and the integration of external signals—underpins the thesis’ incorporation of heterogeneous data inputs and contextual enrichment. However, M5 remains focused on large-scale forecasting accuracy and assumes data abundance, leaving unaddressed how such models perform under data scarcity and computational constraints typical of applied settings. It also does not consider how forecast outputs are transformed into actionable recommendations or validated within a reasoning framework. The thesis extends this work by situating ML forecasting within a resource-constrained, multi-agent system where outputs are calibrated, interpreted, and critically validated through an LLM-based synthesis layer.

# Manual Assessment
---


---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
- [[Makridakis et al. (2020) - The M4 Competition: 100,000 Time Series and 61 Forecasting Methods]]
## Link References
- https://doi.org/10.1016/j.ijforecast.2021.11.013
- https://github.com/Mcompetitions/M5-methods
## Physical References
+
## Other References
-
