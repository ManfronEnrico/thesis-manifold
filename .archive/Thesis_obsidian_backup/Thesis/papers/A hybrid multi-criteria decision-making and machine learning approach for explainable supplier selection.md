
authors: (see ScienceDirect, 2024)

year: 2024

venue: Internet of Things (Elsevier) / ScienceDirect

doi: 10.1016/j.iot.2024.XXXXX

apa7: >

  (Authors). (2024). A hybrid multi-criteria decision-making and machine

  learning approach for explainable supplier selection. *Internet of Things*.

  https://www.sciencedirect.com/science/article/pii/S2949863524000177

read_date: 2026-03-17

read_depth: full

---

  

## In one sentence

  

A hybrid framework that keeps MCDM (specifically AHP) (MCDM (Multi-Criteria Decision Making)) as the core decision mechanism while using ML to reduce input dimensionality achieves performance comparable to pure ML approaches in supplier selection, while delivering end-to-end explainability that purely data-driven methods cannot provide.

  

## Method

  

Two real-world case studies (oil & gas, aerospace manufacturing). ML used upstream to reduce the number of selection criteria and/or supplier candidates; AHP applied downstream as the final ranking and selection mechanism. Comparative evaluation against standard interpretable ML approaches across performance, explainability, and applicability criteria.

  

## Key findings — cite these

  

- Hybrid ML + MCDM achieves **comparable performance** to ML-only approaches while retaining full explainability

- ML component reduces problem complexity (feature/alternative dimensionality) before MCDM takes over — the two stages are not additive but organic

- Explainability identified as the primary adoption barrier for AI in supply chains: "opaque logic can be considered counter-cultural within supply chains such as manufacturing, where there is strong preference for control over all processes" (Section 1)

- AHP retained at decision core ensures familiarity for non-technical stakeholders — a design principle with direct transfer to managerial recommendation systems

  

## Direct quotes — copy verbatim, include page/section

  

> "A hybrid supplier selection framework that combines interpretable data-driven AI techniques with multi-criteria decision-making (MCDM) approaches: the former aims to reduce the complexity of the supplier selection problem, while the latter ensures familiarity to supply chain stakeholders by retaining MCDM at the heart of the supplier selection process." (Abstract)

  

> "Lack of interpretability and explainability is a significant barrier to adoption of intelligent approaches, as it hinders trust and acceptance of produced solutions and decisions." (Section 1)

  

> "Successful hybridisation in the case of supplier selection needs to be 'organic' and ensure uniqueness and superiority to other hybridisations." (Section 1, citing Chai and Ngai)

  

## Where this goes in my thesis

  

- **Ch.2, Section 2.4**: Core reference for the MCDM-ML hybrid design pattern — establishes academic precedent for keeping a structured decision method (here AHP, in the thesis a confidence-weighted synthesis) at the centre while ML handles complexity reduction

- **Ch.5 (Framework Design)**: Justifies the Synthesis Agent architecture — the thesis's inverse-MAPE ensemble weighting + confidence score mirrors the "ML reduces complexity, MCDM decides" pattern; cite as the closest structural analogue in the literature

- **Ch.9 (Discussion)**: The explainability argument directly supports the thesis's design choice to produce natural language recommendations rather than raw model outputs — same rationale (stakeholder adoption)

  

## What this paper does NOT cover (gap it leaves)

  

The framework operates on static, structured procurement data with human-in-the-loop MCDM execution; it does not address automated, real-time multi-agent orchestration, probabilistic forecasting under RAM constraints, or the synthesis of heterogeneous time-series model outputs into a confidence-scored recommendation. The hybrid pattern is validated in industrial supply chain contexts, not in retail demand forecasting with LLM-generated outputs.

  

## My critical assessment

  

Hybrid ML + MCDM = “Use ML to predict, use MCDM to decide which prediction or model is best according to multiple business criteria”

eg: 

  

|   |   |   |   |
|---|---|---|---|
|Model|Accuracy|Computation cost|Inventory risk|
|ARIMA|0.88|Low|High|
|LightGBM|0.93|Medium|Medium|
|Prophet|0.90|Medium|Low|

  

 Its main contribution is the validation of a design pattern in which ML supports but does not replace the decision core, which is directly relevant to the thesis’s Synthesis Agent architecture, where confidence-weighted aggregation mirrors the “ML reduces complexity, MCDM decides” principle.

However,  is limited to static, structured supply chain data with human-in-the-loop decision making; it does not address automated, real-time orchestration of multiple agents, resource-constrained environments, or probabilistic forecasting using heterogeneous models, which are central to the thesis. 

  

valuable for design justification and explainability rationale, it cannot be directly used as evidence of system performance or effectiveness in the retail forecasting domain.

  

|   |   |   |
|---|---|---|
|Aspect|Paper ML+MCDM|Thesis Agentic AI|
|Input|Static, structured|Dynamic, multi-source data|
|Decision making|Human-in-the-loop|Fully automated, multi-agent orchestration|
|Timing|Batch, offline|Real-time / online|
|Task complexity|Single task (supplier selection)|Multi-step, multi-model, probabilistic|
|Resource awareness|Not considered|RAM/compute limits managed|
|Explainability|AHP human-friendly|Confidence + natural language explanation, automated|

  
**