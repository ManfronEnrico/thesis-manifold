---
aliases:
learning_text_title: "Unlocking Business Potential in FMCG with Predictive Analytics: A Machine Learning Approach"
learning_text_venue: MSc Research Project, MSc in Data Analytics, National College of Ireland
learning_text_doi:
learning_text_apa7: "Sharma, U. (2024). *Unlocking business potential in FMCG with predictive analytics: A machine learning approach* [MSc research project, National College of Ireland]."
learning_list_authors:
  - Sharma, U.
learning_list_topic:
  - FMCG Forecasting
  - ML Model Comparison
  - Random Forest
  - Customer Segmentation
  - K-Means Clustering
  - Sales Prediction
  - Supply Chain Analytics
learning_list_srq:
  - SRQ1
  - SRQ3
learning_list_chapter:
  - Ch.2
  - Ch.6
learning_number_release_year: 2024
note_list_type: Regular_Note
note_list_status: complete
note_list_relevance: Medium
note_list_read_depth: full
tags:
learning_date_read_date: 2026-03-22
cssclasses:
---

# AI Assessment
---

**Relevance note**: Source is an MSc project report (National College of Ireland, 8,706 words), not a peer-reviewed publication — cite only for contextual support of FMCG ML model choices, not as primary academic evidence.

## In one sentence

Across five ML models (Linear Regression, Random Forest, Decision Tree, SVR, KNN) applied to FMCG retail sales data, Random Forest consistently achieves the lowest RMSE and highest R² — corroborating tree ensemble superiority in non-linear retail demand patterns — while K-Means segmentation of retail/transfer/warehouse sales provides customer-type groupings that inform inventory targeting.

## Core Ideas
- Tree ensemble models (Random Forest) outperform linear and instance-based models (LR, KNN) on RMSE and R² for FMCG sales forecasting — the non-linearity and interaction effects in retail demand data favour ensemble approaches over parametric baselines
- Three-domain integrated ML framework: sales forecasting (supervised regression), customer behaviour (unsupervised segmentation), and inventory optimisation (reinforcement learning) — positions ML not as a point-forecast tool but as a pipeline serving multiple operational decisions
- K-Means clustering on retail, transfer, and warehouse sales volumes identifies three distinct customer segments that map to different inventory management strategies — segmentation-derived signals can serve as contextual enrichment for demand forecasting models
- Traditional FMCG forecasting (historical averages, seasonal extrapolation) fails to capture consumer preference heterogeneity and supply chain variability — ML models address this gap but require domain-specific feature engineering around seasonality and promotion cycles

## Methods
- Dataset: FMCG retail sales (domain unspecified — likely synthetic or anonymised; sourced from Kaggle or public repository)
- Five supervised ML models: Linear Regression, Random Forest, Decision Tree, SVR, KNN
- Evaluation metrics: RMSE, R²
- Customer segmentation: K-Means clustering on retail/transfer/warehouse sales volume features; three clusters
- Inventory optimisation: Reinforcement Learning for stock-up/stock-down decisions under seasonal demand uncertainty
- No train/test split methodology, cross-validation, or hyperparameter tuning details provided

## Key findings — cite these
- Random Forest achieves best RMSE and R² across all evaluated ML models for FMCG sales forecasting — consistent with tree ensemble literature in retail demand settings
- K-Means produces three interpretable customer segments differentiated by sales channel mix (retail vs. warehouse vs. transfer) — segments correlate with distinct purchasing frequency and volume patterns
- Reinforcement Learning for inventory control identifies optimal reorder policies under seasonal demand fluctuation — though no quantitative performance comparison against a rule-based baseline is provided
- Simple models (Linear Regression) underperform significantly on FMCG data, confirming that non-linear ensemble approaches are necessary for accurate retail demand modelling

## Direct quotes — copy verbatim, include page/section
> "Random Forest was exclusively identified as the most suitable model within the three performance indicators of RMSE as well as R²." (Abstract)

> "Purchasing data patterns, seasonal buying and other relevant external factors can be used effectively to predict buying patterns and, therefore, better manage the supply chain." (Section 1.1, p. 1)

> "The integration of the three domains – prediction of sales, customer engagement, and operation flows – with the help of more sophisticated machine learning models will lead to improvement in the accuracy of forecast and effectiveness of sales and operations planning." (Section 1.2, p. 3)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): Relevant — provides an FMCG-domain ML model comparison that corroborates the thesis's choice of tree ensemble models (LightGBM, XGBoost) over simpler baselines (Ridge Regression); the Random Forest result supports the hypothesis that non-linear models outperform linear baselines in retail demand data
- **SRQ2** (multi-agent coordination and recommendations): N/A
- **SRQ3** (contextual information improving AI capabilities): Partially relevant — K-Means customer segmentation as a form of contextual enrichment signal is conceptually analogous to how Indeks Danmark consumer segments are used in the thesis; cite to frame segmentation-based enrichment as an established FMCG practice
- **SRQ4** (predictive AI vs. descriptive BI): Partially relevant — framing of traditional FMCG models as inadequate vs. ML alternatives mirrors the thesis's descriptive-to-predictive transition argument

## Where this goes in our thesis
- **Ch.2, Section 2.X (ML for FMCG Forecasting)**: Cite as contextual evidence that tree ensemble models are the prevailing ML choice in FMCG retail demand forecasting — supports the inclusion of LightGBM and XGBoost in the thesis benchmark model set
- **Ch.6, Section 6.X (Model Benchmark Design)**: Cite when justifying the exclusion of SVR and KNN from the thesis benchmark — the FMCG results show these models underperform tree ensembles at no computational advantage, supporting the decision to prioritise ARIMA, Prophet, LightGBM, XGBoost, and Ridge

## What this paper does NOT cover (gap it leaves)

The study uses an undisclosed, likely synthetic FMCG dataset without memory profiling, computational budget constraints, or multi-agent orchestration — it treats ML forecasting as a standalone system and does not address how model outputs feed into a confidence-scored managerial recommendation or how to select models under a hard RAM constraint, which is the specific contribution of this thesis.

## Strength
- FMCG domain alignment and three-model comparison (LR, RF, DT, SVR, KNN) provides a directly citable precedent for tree ensemble superiority in retail demand forecasting
- The three-domain framing (forecasting + segmentation + optimisation) is conceptually aligned with the thesis's multi-component pipeline design

## Weaknesses
- MSc project report — not peer-reviewed; limited methodological rigour (no cross-validation details, no hyperparameter tuning description, no statistical significance testing)
- Dataset is undisclosed and likely synthetic or Kaggle-sourced — generalisation to real Nielsen CSD scanner data is uncertain
- No memory or runtime profiling — cannot support any claim about computational efficiency
- 8,706 words / 19 pages — very short; findings lack depth and quantitative detail needed for primary citation

## My critical assessment

- **Strengths:** Provides FMCG-specific empirical support for the effectiveness of tree-based ensemble models (Random Forest) in capturing non-linear retail demand patterns; also introduces segmentation (K-Means) as a form of contextual enrichment, aligning conceptually with multi-signal forecasting approaches.
- **Weaknesses:** Limited methodological rigour (no clear validation strategy, tuning, or statistical testing) and based on an unspecified, likely non-industrial dataset; as an MSc project, it lacks the robustness and credibility of peer-reviewed research.
- **Relevance to thesis:** Offers domain-aligned, albeit weak, supporting evidence for your inclusion of ensemble models (LightGBM, XGBoost) and the idea of enriching forecasts with additional signals (e.g., consumer survey data).
- **Gap addressed by your work:** Does not address **resource-constrained model selection, multi-model benchmarking, or integration into a multi-agent decision-support system**; your thesis advances this by providing a **rigorous, real-world retail implementation with explicit evaluation of accuracy, efficiency, and decision quality**.
# Manual Assessment
---


---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
-
## Link References
-
## Physical References
+
## Other References
-
