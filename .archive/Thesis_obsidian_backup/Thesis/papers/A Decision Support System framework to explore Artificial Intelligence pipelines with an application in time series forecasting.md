---
title: "DSS4EX: A Decision Support System framework to explore Artificial Intelligence pipelines with an application in time series forecasting"
authors: Rinaldi, G., Theodorakos, K., Crema Garcia, F., Agudelo, O. M., & De Moor, B.
year: 2025
venue: Expert Systems With Applications, 269, 126421
doi: 10.1016/j.eswa.2025.126421
apa7: >
  Rinaldi, G., Theodorakos, K., Crema Garcia, F., Agudelo, O. M., & De Moor, B. (2025).
  DSS4EX: A decision support system framework to explore artificial intelligence pipelines
  with an application in time series forecasting. *Expert Systems With Applications*, *269*, 126421.
  https://doi.org/10.1016/j.eswa.2025.126421
read_date: 2026-03-21
read_depth: full
---

## In one sentence

DSS4EX proposes a human-in-the-loop Decision Support System framework that makes complex AI forecasting pipelines transparent and explorable for non-expert users — a proof-of-concept demonstrated on electricity demand forecasting with a DR-DNN pipeline.

## Method

Framework design (architecture-level contribution, not empirical ML benchmark). Prototype software demo built around a Decomposition-Residuals Deep Neural Network (DR-DNN) applied to electricity demand forecasting (34,360 hourly timesteps, 7 variables, 2017–2021). GUI-based interactive pipeline exploration with expert-driven in-system suggestions.

## Key findings — cite these

- DSS4EX uniquely targets **non-expert user comprehension** of AI pipelines, not just decision output — distinguishing it from RapidMiner, KNIME, IBM SPSS
- Human-in-the-loop design delivers **context-specific expert suggestions directly in the GUI**, reducing information overload for non-technical users
- Framework is currently **prototype phase** — not validated at scale or on production data
- DSS frameworks for time series forecasting have been applied since the 1980s but increasingly focus on AI transparency (XAI) and human-computer interaction

## Direct quotes — copy verbatim, include page/section

> "DSS4EX is specifically designed to explore and understand complex AI pipelines. Unlike traditional DSS, which primarily focuses on aiding decision-making, DSS4EX emphasizes the exploration and comprehension of AI methods." (Section 1)

> "This interactive approach enhances user engagement and comprehension, promoting informed decision-making. The DSS4EX framework makes complex models more transparent and accessible, bridging the gap between advanced AI models and user understanding." (Abstract)

> "In DSS4EX, this approach also enables the system to offer insights from past expert decisions, suggesting improvements or adjustments to enhance the configuration process." (Section 1)

## Where this goes in my thesis

- **Ch.2, Section 2.X (Decision Support Systems / AI-assisted BI)**: Cite as a recent DSS framework explicitly bridging AI forecasting pipelines and non-expert business users — directly analogous to our system's goal of translating predictive outputs into managerial recommendations (SRQ2)
- **Ch.5 (Framework Design)**: DSS4EX's human-in-the-loop architecture and expert-guidance layer are design precedents for our Synthesis Agent's recommendation interface; cite when justifying the "actionable recommendation" output layer
- **Ch.2 / Ch.9 (Related Work)**: Positions our work relative to DSS literature — we extend the DSS4EX concept by adding multi-agent orchestration, lightweight ML benchmarking, and consumer signal enrichment
- **Ch.8 (Evaluation / SRQ4)**: DSS4EX vs. traditional descriptive BI framing supports our comparative baseline argument

## What this paper does NOT cover (gap it leaves)

DSS4EX is a single-agent, single-pipeline framework applied to a clean energy dataset — it does not address **multi-agent coordination across heterogeneous data sources** (scanner + consumer survey), **resource-constrained deployment**, or **confidence-scored synthesis** of competing model outputs, which are the core contributions of this thesis.

## My critical assessment

- Provides a **strong conceptual foundation** for your thesis by showing that DSS systems are evolving from “decision output tools” to **AI pipeline interpretation tools**, which aligns directly with your goal of making forecasting outputs understandable for managers
- Validates your **human-in-the-loop design choice**, demonstrating that expert guidance embedded in the system improves usability and trust for non-technical users — exactly what your Synthesis Agent is doing
- Strengthens your argument that **interpretability and usability are as important as accuracy** in real-world decision support systems, not just model performance
- However, the contribution is **primarily conceptual and prototype-level**, with no large-scale or production validation — meaning its claims about effectiveness remain unproven
- The paper operates in a **single-model, single-pipeline setting**, so it does not address the complexity of multi-agent orchestration, ensemble forecasting, or heterogeneous data integration central to your thesis
- It also lacks any notion of **confidence scoring or uncertainty-aware recommendations**, which is a key innovation in your framework
- **Bottom line:** useful as a _positioning and design justification paper_ (why DSS should be interpretable and human-centered), but not as a technical foundation for your multi-agent, resource-constrained, ensemble-based system