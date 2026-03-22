---
title: "An information-sharing and cost-aware custom loss machine learning framework for 3PL supply chain forecasting"
authors: Gabellini, M., Calabrese, F., Galizia, F. G., Ronchi, M., & Regattieri, A.
year: 2025
venue: Computers & Industrial Engineering
doi: 10.1016/j.cie.2025.111573
apa7: >
  Gabellini, M., Calabrese, F., Galizia, F. G., Ronchi, M., & Regattieri, A. (2025). An
  information-sharing and cost-aware custom loss machine learning framework for 3PL supply chain
  forecasting. *Computers & Industrial Engineering*. https://doi.org/10.1016/j.cie.2025.111573
read_date: 2026-03-21
read_depth: full
---

## In one sentence

A CatBoost-based forecasting framework for third-party logistics (3PL) truck space reservation that improves both accuracy and cost efficiency by combining multivariate information sharing with a custom asymmetric loss function that penalises under- and overestimation differently.

## Method

CatBoost as primary ML model (handles complex data relationships, categorical variables). Custom asymmetric loss function reflecting unequal costs of over- vs. underestimation. Real-world 3PL case study in food sector logistics. Benchmarked against traditional statistical models and alternative ML configurations. Validated on multiple time series within a single case study.

## Key findings — cite these

- Custom asymmetric loss function **significantly reduces cost-related forecast errors** vs. symmetric loss baselines, particularly in imbalanced cost scenarios (truck saturation vs. non-saturation)
- CatBoost with multivariate information sharing **substantially outperforms traditional statistical models** in forecast accuracy
- Gain comes at a cost: **CatBoost training time is higher** than both statistical and simpler ML benchmarks
- Incorporating information-sharing data (pallet overlapping dynamics) into ML models directly improves space utilization forecasts — not possible with pure univariate approaches
- Framework validated on a single case study — **generalisability across 3PL segments is an open limitation**

## Direct quotes — copy verbatim, include page/section

> "Models which penalize over- and underestimation equally are misaligned with the operational realities of 3PL forecasting, where space optimization critically depends on recognizing the asymmetric nature of forecast error costs." (Section 1)

> "The proposed framework leverages Machine learning models for the first time to explicitly learn pallet overlapping possibilities and to differentially balance the consequences of overestimating and underestimating the reserved truck space." (Section 1)

> "The results demonstrate that the proposed approach significantly benefits forecast accuracy and cost efficiency." (Section 6)

## Where this goes in my thesis

- **Ch.2, Section 2.X (Supply chain / FMCG demand forecasting)**: Cite as evidence that ML forecasting frameworks in logistics benefit from asymmetric cost-aware loss functions — directly relevant to our SRQ1 model selection, where forecast errors have asymmetric business consequences (stockout vs. overstock)
- **Ch.5 (Framework Design)**: The asymmetric cost framing supports designing our Synthesis Agent's confidence scoring to weight under-forecasting more heavily than over-forecasting in FMCG retail contexts
- **Ch.6 (Model Benchmark / SRQ1)**: CatBoost benchmark result is a comparator — note that we use LightGBM (similar gradient boosting family) rather than CatBoost; cite to justify gradient boosting inclusion
- **Ch.9 (Limitations)**: Single case study limitation mirrors our own — cite to contextualise our single-dataset validation constraint

## What this paper does NOT cover (gap it leaves)

The framework is single-agent, single-model (CatBoost), and focused on physical logistics (truck space) with no LLM orchestration or consumer signal enrichment — it does not address how heterogeneous data signals (e.g., consumer sentiment surveys) can be synthesised by a multi-agent system into confidence-scored managerial recommendations, which is the core contribution of SRQ2 and SRQ3.

## My critical assessment

- Strength / novelty
    
- Introduces a custom asymmetric loss function that aligns forecast penalties with real-world cost asymmetries (underestimation vs. overestimation).
    
- Uses multivariate information sharing to capture pallet-overlap dynamics — improves accuracy over univariate or standard statistical models.
    
- Demonstrates that gradient-boosted ML models (CatBoost) can directly optimize business-relevant cost metrics, not just prediction accuracy.
    

- Technical contribution / insights
    

- Shows that penalizing forecast errors symmetrically is suboptimal in operational contexts like 3PL logistics.
    
- CatBoost effectively handles categorical variables and complex feature interactions, making it suitable for operationally rich datasets.
    
- Validates the approach on multiple time series within a real-world case study, providing applied evidence.
    

- Limitations / gaps
    

- Single case study — generalizability across other 3PL segments or FMCG contexts remains untested.
    
- Single-agent, single-model focus — no orchestration of multiple models or agents.
    
- No integration of heterogeneous signals (e.g., consumer surveys, external forecasts), which is critical for the multi-agent, confidence-scored synthesis approach in your thesis.
    
- Computational cost: CatBoost training time is higher than simpler models — could be a bottleneck for real-time deployment.
    

- Relevance to thesis
    

- Supports SRQ1: justifies the inclusion of gradient boosting models and asymmetric cost considerations in forecasting.
    
- Supports SRQ2/Framework Design: motivates weighting under-forecasting more heavily in the Synthesis Agent’s confidence scoring.
    
- Provides a realistic operational precedent for aligning model loss functions with business KPIs.
    

- Takeaway
    

- Strong example of domain-aware ML design where accuracy alone is insufficient.
    

Demonstrates the value of embedding business logic into model objectives, a principle your multi-agent system extends to heterogeneous, confidence-scored recommendations.**