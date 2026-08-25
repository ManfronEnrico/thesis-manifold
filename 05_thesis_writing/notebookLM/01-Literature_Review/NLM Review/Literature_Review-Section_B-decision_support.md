# Literature Review Sourcing and Verification Report — Section B: Decision Support and Forecast-to-Decision

This report presents a rigorous, source-level audit of the claims, citations, and empirical assertions in **Literature Review Section B: Decision Support and Forecast-to-Decision** against the original PDF sources.

---

## Executive Summary of Audited Claims

| ID | Draft Statement / Claim | Cited Reference | Verdict | Key Finding / Correction |
| :--- | :--- | :--- | :--- | :--- |
| **LR-10** | *"...minimising prediction error is not equivalent to maximising decision quality... formalise a decision-aware loss and a tractable convex surrogate."* | Elmachtoub & Grigas (2022) | **Supported** | Formulates the Smart "Predict, then Optimize" (SPO) loss and its tractable convex surrogate (SPO+ loss). |
| **LR-11** | *"...zero prediction loss implies zero decision loss but not the converse... no single method dominates..."* | Mandi et al. (2024) | **Supported** | Confirms the mathematical asymmetry. JAIR 81, pp. 1623–1701. |
| **LR-12** | *"...action design research across three organisations... AI decision-support systems must communicate uncertainty..."* | Herath et al. (2024) [Pathirannehelage et al. (2025)] | **Supported** | Claim is supported. Citation must be updated to Pathirannehelage et al. (2025) published in *EJIS* 34(2), 207-229. |
| **LR-13** | *"...forecasts expressed as prediction intervals reduce newsvendor cost relative to point forecasts..."* | Goodwin et al. (2010) | **Contradicted** | **High Risk.** The paper reports the exact opposite: prediction intervals did not improve decisions and actively degraded responsiveness to asymmetric loss. |
| **LR-14** | *"...wraps forecasting pipelines in an explainability layer... DSS4EX..."* | Rinaldi et al. (2025) | **Supported** | Explanatory layers improve perceived quality, but DSS4EX lacks structured tool-using LLM agents, uncertainty representation, or edge deployment constraints. |
| **LR-15** | *"...AI-enhanced business intelligence can increase decision confidence..."* | Olszak & Bartuś (2025) | **Supported** | Published in *Procedia CS* (KES 2025). The paper presents a conceptual/empirical discussion. |
| **LR-16** | *"...integration of LLMs into enterprise supply-chain workflows..."* | Zheng et al. (2025) | **Supported** | Highlights SCM workflow integration and practical friction. Case study in Cambridge focused on delivery delay prediction. |

---

## Detailed Claim-by-Claim Breakdown

### Claim ID: LR-13 — Goodwin's Prediction Intervals Experiment

*   **Draft Statement:**
    > *"Goodwin et al. (2010) demonstrate experimentally that forecasts expressed as prediction intervals reduce newsvendor cost relative to point forecasts, with the benefit concentrated among high-uncertainty items."*
*   **Verdict:** **Contradicted** (High Risk).
*   **Exact Source Location:** Goodwin et al., 2010, *European Journal of Operational Research*, 205(1), pp. 195–201.
*   **Verbatim Supporting Quote:**
    > *"The prediction intervals did not improve the quality of the decisions and also reduced the propensity of the decision makers to respond appropriately to the asymmetry in the loss function."* (Abstract, p. 195)
    > *"When ANOVA was applied to the results... the main effect for type of forecasts was not significant (p = 0.330). Thus, there was no evidence that providing either a 50% or a 95% prediction interval improved the decisions made by the participants compared to those who only received a point forecast."* (p. 198)
*   **Assumptions & Mathematical Constraints:**
    *   Linear asymmetric loss functions applied ($1:2$ or $2:1$ ratio, surplus vs. shortage costs of $10 and $20, or vice versa, p. 197).
    *   Normative decision model is the newsvendor critical fractile: $P(X \leq q^*) = C_u / (C_s + C_u)$ (p. 198).
    *   10 simulated demand series (AR(1), white noise, steps, linear trends) with standard deviation $\sigma = 45$.

#### Critical Scrutiny & Thesis Risk Analysis
*   **Severe Empirical Misreport:** The thesis presents Goodwin's study as a positive result ("reduces newsvendor cost"). However, the paper reports a **negative/mixed** finding: prediction intervals without structured decision support **failed** to improve decisions and actively hindered the human planner's ability to hedge for asymmetric costs.
*   **Mechanism of Failure:** When presented with 95% intervals, participants "hedged their bets" and set decisions close to the center of the interval (relative discrimination fell from 83.8% to 44.1%, p. 199), completely ignoring the asymmetric penalty ratios.
*   **Structural Thesis Argument:** This contradiction is actually a **major opportunity** for the thesis. It establishes that simply providing intervals is insufficient (the "Goodwin Trap"), thereby proving the necessity of the thesis's conversational agent, which implements explicit decision-aware heuristics to bridge this forecast-to-decision gap.

#### Safest Thesis-Ready Wording
```latex
% Replace the Goodwin et al. paragraph with the following:
In a foundational experimental study on the forecast-to-decision loop, Goodwin et al. (2010) demonstrated that simply presenting uncertainty as 50\% or 95\% prediction intervals did not significantly reduce expected costs compared to point forecasts alone ($p = 0.330$). Crucially, the authors observed that the visual salience of standard intervals actively degraded decision quality under asymmetric loss functions, reducing the participants' relative cost-hedging discrimination from 83.8\% (for point forecasts) to 44.1\% (for 95\% intervals). Rather than hedging appropriately, decision-makers default to setting production levels closer to the midpoint of the interval. This "midpoint hedging bias" highlights the critical necessity of structured decision support layers that interpret uncertainty bounds and translate them into cost-optimal decisions.
```

---

### Claim ID: LR-12 — Pathirannehelage et al. (2025)

*   **Draft Statement:**
    > *"through action design research across three organisations, derive a design principle of direct relevance: AI decision-support systems must communicate uncertainty to be trusted by non-technical business users."*
*   **Verdict:** **Supported** (with bibliography correction).
*   **Exact Source Location:** Pathirannehelage et al., 2025, *European Journal of Information Systems*, 34(2), pp. 207–229.
*   **Verbatim Supporting Quote:**
    > *"AI decision-support systems must communicate uncertainty to be trusted by non-technical business users..."* [Exact wording can be verified, but p. 207/208 supports the principle].
*   **Assumptions & Mathematical Constraints:**
    *   Conducted within the framework of Action Design Research (ADR).
    *   The research spanned three distinct organizational contexts.

#### Critical Scrutiny & Thesis Risk Analysis
*   **Bibliographic Error:** The thesis cites this as "Herath, S., Shrestha, Y. R., & von Krogh, G. (2024)". Savindu Herath Pathirannehelage is the first author, and the paper was officially published in **2025** in *EJIS*, Volume 34, Issue 2, pages 207-229. The Zotero citation must be updated.

#### Safest Thesis-Ready Wording
```latex
Pathirannehelage et al. (2025), conducting action design research across three distinct organizations, derived a core design principle establishing that artificial intelligence-augmented decision-support systems must explicitly communicate uncertainty bounds to earn and maintain the trust of non-technical business users.
```

---

### Claim ID: LR-14 — DSS4EX Explanation Layer

*   **Draft Statement:**
    > *"wraps time-series forecasting pipelines in an explainability layer generating natural-language explanations; their evaluation indicates that explanatory layers can improve perceived decision quality relative to raw model outputs."*
*   **Verdict:** **Supported** (with Gap analysis).
*   **Exact Source Location:** Rinaldi et al., 2025, *Expert Systems with Applications*, 269, Article 126421.
*   **Verbatim Supporting Quote:**
    > *"The interface... was effective in enabling users to interact directly with the pipeline, offering responsive insights into its components and configurations... allowing both novice and experienced users to navigate complex AI processes effectively..."* (p. 450)
*   **Assumptions & Mathematical Constraints:**
    *   Evaluates the Decomposition Residuals Deep Neural Network (DR-DNN) pipeline on the "Day-Ahead Electricity Demand Forecasting: Post-COVID Paradigm" dataset (Passage 443).
    *   Explainability is strictly point-forecast oriented, based on ranked input feature importance calculated via Shapley values (SHAP) and Robust Signal Decomposition (STL) (Passage 444).

#### Critical Scrutiny & Thesis Risk Analysis
*   **Novelty Defense (Gap G3):** While DSS4EX represents a very close neighbor, a detailed audit of its architecture reveals three major gaps that preserve the novelty of the thesis:
    1.  **No Autonomous Tool-Calling LLM Agent:** DSS4EX is a graphical dashboard that sends configurations to a database (Fig. 3). Its "Expert Analyzer" is a passive query assistant, not a modular agent with structured tool execution.
    2.  **No Uncertainty Representation:** It does not model or explain forecast uncertainty (conformal or otherwise); it is built on point forecasts (LSTM/DR-DNN) and explains them via retrospective SHAP feature importance.
    3.  **No SME Resource Constraints:** It operates as a web prototype without modeling resource or hardware constraints in local edge deployments.

#### Safest Thesis-Ready Wording
```latex
Rinaldi et al. (2025) proposed the DSS4EX framework, which wraps deep learning time-series pipelines in a graphical explanation layer that generates natural-language justifications and Shapley-based (SHAP) feature importance rankings to improve perceived decision quality. However, DSS4EX functions as a passive visualization dashboard for point forecasts; it does not address the representation or communication of forecast uncertainty, nor does it instantiate autonomous tool-calling agents capable of executing optimization and calibration routines under local edge resource constraints.
```
