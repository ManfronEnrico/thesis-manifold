---
aliases:
learning_text_title: "A data-driven and context-aware approach for demand forecasting in the beverage industry"
learning_text_venue: International Journal of Logistics Research and Applications
learning_text_doi: 10.1080/13675567.2025.2566806
learning_text_apa7: "Ma, B. J., Jackson, I., Huang, M., Villegas, S., & Macias-Aguayo, J. (2025). A data-driven and context-aware approach for demand forecasting in the beverage industry. *International Journal of Logistics Research and Applications*. Advance online publication. https://doi.org/10.1080/13675567.2025.2566806"
learning_list_authors:
  - Ma, B. J.
  - Jackson, I.
  - Huang, M.
  - Villegas, S.
  - Macias-Aguayo, J.
learning_list_topic:
  - Beverage Industry Forecasting
  - Cluster-Then-Forecast
  - SKU Segmentation
  - Exogenous Features
  - XGBoost
  - ARIMA
  - Demand Pattern Heterogeneity
  - FMCG
learning_list_srq:
  - SRQ1
  - SRQ2
  - SRQ3
learning_list_chapter:
  - Ch.2
  - Ch.3
  - Ch.6
learning_number_release_year: 2025
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

Using 156 weeks of shipment data from North America's largest private-label beverage manufacturer, Ma et al. demonstrate that a cluster-then-forecast framework — segmenting 880 SKUs by volume, volatility, and intermittency into four clusters and assigning tailored models (ARIMA, ETS, XGBoost, TiDE, N-BEATS, Croston, CPFR) — consistently outperforms any single universal forecasting model, and that ML models enriched with exogenous features (holidays, temperature) significantly outperform statistical baselines for stable high-volume SKUs.

## Core Ideas
- No single forecasting model dominates across all demand patterns — the "no-free-lunch" principle applies at the SKU level in beverage FMCG, making cluster-specific model assignment a methodological necessity rather than a convenience; a universal model either overfits erratic SKUs or underfits stable high-volume ones
- K-means segmentation on three interpretable demand features (volume=mean, volatility=CoV, intermittency=zero-demand frequency) yields four operationally meaningful clusters: stable high-volume (3% of SKUs, 63% of volume), stable low-volume, erratic-intermittent, and lumpy — resource allocation follows the concentration of volume, not item count
- Exogenous features (holiday calendars, temperature data aggregated by state) materially improve ML model accuracy for stable high-volume SKUs — temperature drives weather-sensitive beverage consumption patterns in ways that historical sales alone cannot capture; this is the mechanism for context-awareness in the framework
- Lumpy demand (prolonged zeros punctuated by large irregular spikes) is beyond the reliable capability of any statistical or ML model — CPFR (qualitative collaborative planning) is the recommended approach, highlighting that algorithmic forecasting has practical domain limits that managerial judgement must fill

## Methods
- Dataset: 156 weeks (April 2022–March 2025) of outbound shipment data from largest North American private-label beverage manufacturer; 880 parent SKUs, ~650 customers, 12,000 ship-to locations, 49 plants
- Exogenous features: US public holiday calendars (2022–2024); NOAA temperature data (weekly min/max/mean by state)
- SKU segmentation: K-means on CoV, ADI, demand frequency; optimal K=3 via Elbow Method + Silhouette Score; refined to 4 clusters via segmented regression breakpoint at 50,000 units/week on Cluster 1 volume distribution
- Models evaluated per cluster: ETS (auto-AIC selection), ARIMA (Hyndman-Khandakar), XGBoost (regularised gradient boosting), TiDE (transformer dense encoder), N-BEATS (residual decomposition neural net), Croston (intermittent demand)
- Validation: rolling-origin evaluation, fixed 13-week forecast horizon (matching company's tactical planning cycle); hyperparameter tuning via randomised search with 5-fold CV for ML/DL models
- Implementation: Python 3.11, scikit-learn, statsmodels, xgboost, darts

## Key findings — cite these
- For stable high-volume SKUs (Cluster A): ML models with exogenous features significantly outperform statistical baselines — XGBoost with holiday/temperature features achieves best accuracy
- For stable low-volume SKUs (Cluster B): N-BEATS adds value over ARIMA/ETS; signal-to-noise is higher, reducing the advantage of classical statistical decomposition
- For erratic-intermittent SKUs (Cluster C): Croston method remains competitive with more complex alternatives; ML models do not consistently outperform
- For lumpy SKUs (Cluster D): all algorithmic models are unreliable; CPFR (qualitative) is the operationally sound recommendation
- Volume concentration (3% of SKUs = 63% of demand) means that accurate forecasting of Cluster A alone materially improves overall supply chain performance — cluster-then-forecast enables prioritised resource allocation

## Direct quotes — copy verbatim, include page/section
> "No single model performs best across all demand types." (Section 6, Conclusion, p. 25)

> "For stable and high-volume SKUs, machine learning models enhanced with exogenous features such as holidays and temperature significantly outperform traditional baselines." (Section 6, Conclusion, p. 25)

> "Stable SKUs account for only 3% of items, they contribute 63% of volume — a sharp imbalance that calls for targeted resource allocation." (Section 2, p. 3)

> "Our approach is predicated on the idea that no single model is optimal across all demand types, consistent with the no-free-lunch theorem in predictive modelling." (Section 3.4, p. 9)

> "This clustering also enables a more targeted use of endogenous and exogenous factors, which can help improve the accuracy and explainability of the predictions." (Section 2, p. 4)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): Directly and domain-specifically relevant — provides a beverage FMCG model benchmark comparing ARIMA, ETS, XGBoost (analogous to LightGBM), and DL models on data structurally similar to Nielsen CSD (3 years, weekly, single beverage manufacturer); confirms no-free-lunch; the thesis's model set (ARIMA, Prophet, LightGBM, Ridge) is validated as appropriate for the stable high-volume CSD segment — the primary segment in the Nielsen data
- **SRQ2** (multi-agent coordination and recommendations): Relevant — the cluster-then-forecast architecture is a form of multi-model coordination where different models are assigned to different SKU segments and their outputs are aggregated for supply chain decisions; directly analogous to the synthesis module's task of combining heterogeneous model outputs into a unified recommendation
- **SRQ3** (contextual information improving AI capabilities): Directly relevant — exogenous features (holidays, temperature) significantly improved ML accuracy for stable high-volume SKUs; Indeks Danmark consumer survey signals are the thesis's analog (consumer sentiment, purchase frequency, price sensitivity); this paper provides the most direct empirical precedent for the external signal enrichment design — cite as the mechanism validation for SRQ3

## Where this goes in our thesis
- **Ch.2, Section 2.X (Demand Forecasting in Beverage FMCG)**: Cite as the closest domain match in the corpus — a peer-reviewed 2025 study from MIT CTL using 3 years of beverage data with exogenous enrichment; establishes the state of the art in the exact application domain of the thesis
- **Ch.3, Section 3.X (Model Selection and Exogenous Features Rationale)**: Cite when justifying (i) the multi-model benchmark approach as state-of-practice, (ii) the inclusion of Indeks Danmark as a contextual enrichment feature analogous to temperature/holiday signals, and (iii) the focus on stable high-volume SKUs as the operationally critical forecasting target
- **Ch.6, Section 6.X (Model Benchmark Interpretation)**: Cite when interpreting why LightGBM/XGBoost with external features outperforms ARIMA in the stable CSD segment — Ma et al. (2025) provides a direct peer-reviewed parallel finding in the same beverage domain
- **Ch.7, Section 7.X (Synthesis Module Design)**: Cite the cluster-then-forecast architecture as a modular precedent for the synthesis layer's multi-model aggregation design

## What this paper does NOT cover (gap it leaves)

The paper produces cluster-specific forecast outputs but does not address how these outputs are synthesised into natural-language managerial recommendations, how an LLM orchestrates model selection and result interpretation, or how the system operates under a hard RAM constraint — all three of which are the core contributions of this thesis. Additionally, the thesis operates in a monthly aggregated CSD retail context with ~36 observations rather than 156 weekly observations, raising the boundary condition of whether ML exogenous enrichment remains effective at lower temporal resolution.

## Strength
- MIT Center for Transportation and Logistics affiliation — highest credibility; International Journal of Logistics Research and Applications (Taylor & Francis, peer-reviewed)
- Published October 2025 — most recent paper in the corpus; demonstrates the thesis topic is at the current research frontier
- Domain alignment is the strongest of any paper in the corpus: beverage industry + cluster-then-forecast + exogenous features + model comparison including ARIMA and XGBoost; directly citable as a 2025 state-of-the-art baseline for the thesis
- 156 weeks of real company data (not Kaggle/synthetic) and a 13-week rolling-origin validation protocol provide high ecological validity

## Weaknesses
- Uses XGBoost rather than LightGBM — close functional analogue but not identical; LightGBM's advantages (speed, memory efficiency, native categorical handling) are not evaluated in this paper
- US private-label bottled water market structure differs from Danish CSD retail scanner data — different promotional patterns, retail concentration, and consumer behaviour dynamics
- Weekly granularity vs. the thesis's monthly aggregation level — some cluster-specific findings (particularly for TiDE and N-BEATS which require more data) may not transfer
- Computational budget and RAM profiling are not reported — cannot be used to support the 8GB RAM constraint justification

## My critical assessment

Ma et al. (2025) are highly relevant as they provide recent, domain-specific evidence that demand forecasting in FMCG settings benefits from explicitly modelling heterogeneity through a cluster-then-forecast framework. This directly aligns with the thesis’ view that no single model is universally optimal and that multiple specialized models should be orchestrated within a broader decision-support system. The paper’s key contribution—demonstrating that model performance depends on demand characteristics and that exogenous features (e.g., temperature, holidays) significantly enhance ML forecasts—supports both the thesis’ multi-model design and its integration of contextual signals. However, the approach remains limited to the forecasting stage, producing segmented numerical outputs without addressing how these are synthesized into actionable decisions or validated for reliability. It also lacks a unifying reasoning layer to reconcile outputs across segments or handle cases where algorithmic methods fail (e.g., lumpy demand). The thesis extends this work by embedding such heterogeneous forecasts within an LLM-based synthesis and validation framework, enabling interpretable, confidence-scored recommendations under practical system constraints.
# Manual Assessment
---


---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
- [[Makridakis et al. (2022) - M5 Accuracy Competition: Results, Findings, and Conclusions]]
## Link References
- https://doi.org/10.1080/13675567.2025.2566806
## Physical References
+
## Other References
-
