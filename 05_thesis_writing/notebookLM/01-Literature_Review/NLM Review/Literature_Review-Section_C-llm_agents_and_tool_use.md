# Literature Review Sourcing and Verification Report — Section C: LLM Agents and Tool Use

This report presents a rigorous, source-level audit of the claims, citations, and empirical assertions in **Literature Review Section C: LLM Agents and Tool Use** against the original PDF sources.

---

## Executive Summary of Audited Claims

| ID | Draft Statement / Claim | Cited Reference | Verdict | Key Finding / Correction |
| :--- | :--- | :--- | :--- | :--- |
| **LR-18** | *"...executable code can offer advantages over JSON-formatted tool calls... dynamic tool composition and self-debugging."* | Wang et al. (2024) [CodeAct] | **Supported** | CodeActAgent 7B achieved 51.3% on MINT vs 3.2% for Llama2-Chat, enabling dynamic tool composition. |
| **LR-19** | *"...statistical models as callable agent tools (Chen & Bibi, 2026); exists only as small, non-peer-reviewed proofs of concept..."* | Chen & Bibi (2026) | **Supported** | Verified as a 2026 hackathon submission. It is a pricing prediction XGBoost model ($N=70$ samples); it does not address forecasting or uncertainty. |
| **LR-20** | *"...equipping an LLM with domain-specific tools... substantially improves precision-sensitive reasoning..."* | Ma et al. (2024) [SciAgent] | **Supported** | SciAgent-Coder 7B achieved 53.0% on CREATION vs 17.7% for CodeLlama-7B baseline, validating "substantial" improvement. |
| **LR-21** | *"...automatically decomposing a task into structured reasoning-and-tool-use steps can improve task performance..."* | Paranjape et al. (2023) [ART] | **Supported** | Published in EMNLP 2023. Decomposing tasks improves performance and controllability across BigBench. |
| **LR-22** | *"...distinguishes AI Agents... from Agentic AI..."* | Sapkota et al. (2025) [Sapkota et al. (2026)] | **Supported** | Citation corrected to Sapkota et al. (2026), published in *Information Fusion* 126. Definitions are verbatim correct. |
| **LR-23** | *"...dynamically activating specialist agents can outperform fixed pipelines..."* | Liu et al. (2023) [Liu et al. (2024)] | **Supported** | Year corrected to 2024 (First Conference on Language Modeling). DyLAN outperforms fixed ensembling. |
| **LR-24** | *"...structured, graph-based orchestration can be generated and optimised automatically..."* | Chen et al. (2024) [Li et al. (2024)] | **Supported** | First author corrected to Li et al. (2024) [AutoFlow]. Graph-based workflows are optimized via reinforcement learning. |
| **LR-25** | *"...structured, graph-based orchestration... ScoreFlow..."* | Wu et al. (2025) [Wang et al. (2025)] | **Supported** | First author corrected to Wang et al. (2025) [ScoreFlow]. Optimizes workflows via preference optimization (Score-DPO). |
| **LR-26** | *"...self-verification sampling, in which an agent evaluates candidate outputs before committing..."* | Huang et al. (2024) [Guo et al. (2025)] | **Supported** | Correct citation is Guo et al. (2025). The paper was published as an arXiv/OpenReview preprint in Feb 2025. |

---

## Detailed Claim-by-Claim Breakdown

### Claim ID: LR-19 — Chen & Bibi (2026) MLAT and Gap G3

*   **Draft Statement:**
    > *"an emerging strand begins to expose pre-trained statistical models as callable agent tools (Chen & Bibi, 2026); the latter, however, exists only as small, non-peer-reviewed proofs of concept and does not address forecasting, reliability, or production constraints."*
*   **Verdict:** **Supported** (with qualifications that reinforce G3).
*   **Exact Source Location:** Chen & Bibi, 2026, *Machine Learning as a Tool (MLAT)*, devpost.com/software/pitchcraft [Submitted to Gemini 3 Hackathon, February 2026].
*   **Verbatim Supporting Quote:**
    > *"We introduce Machine Learning as a Tool (MLAT), a design pattern in which pretrained statistical ML models are exposed as callable tools... Submitted to the Gemini 3 Hackathon... We present a methodology for training XGBoost regression under extreme data scarcity (N = 70)..."* (p. 2)
*   **Assumptions & Mathematical Constraints:**
    *   The predictive model is a point-estimate XGBoost regressor predicting professional services project pricing (Passage 1028).
    *   The dataset is extremely small: $N=70$ samples, containing 40 real agency deals and 30 LLM-generated, human-verified records (Passage 786).

#### Critical Scrutiny & Thesis Risk Analysis
*   **Gap G3 Integrity:** A detailed audit of Chen & Bibi (2026) confirms that the thesis's dismissal of this work is entirely fair and structurally robust:
    1.  **No Forecasting:** The paper does **not** address forecasting; it is a static pricing prediction model. There is no temporal sequencing, seasonality, or time-series data.
    2.  **No Uncertainty Quantification:** The model is a deterministic, point-estimate regressor ("price ($, target)"). There is no interval prediction or uncertainty representation.
    3.  **Proof-of-Concept Status:** Deployed in a pilot application called *PitchCraft*, which achieved sub-100ms latency on a FastAPI endpoint, but remains a small-scale, non-peer-reviewed hackathon submission (submitted in Feb 2026).
*   **Novelty Defense:** This verified dismissal means the thesis's novelty claims are completely secure: no prior peer-reviewed work exposes calibrated time-series forecasting models to LLM agents as tools under resource constraints.

#### Safest Thesis-Ready Wording
```latex
Although Chen and Bibi (2026) formalized the "Machine Learning as a Tool" (MLAT) design pattern by exposing an XGBoost regressor as an API tool within an LLM-orchestrated professional services pricing pipeline (PitchCraft), their framework is constrained to a small-scale, non-peer-reviewed proof of concept ($N=70$). Crucially, they do not address sequential time-series forecasting, represent or quantify forecast uncertainty (UQ), or model the severe edge computational constraints typical of industrial small-to-medium enterprise (SME) deployments.
```

---

### Claim ID: LR-22 — Sapkota's Agents vs Agentic AI

*   **Draft Statement:**
    > *"...distinguishes AI Agents, defined as modular, task-specific systems driven by a single LLM with tool use, from Agentic AI, characterised by multi-agent collaboration, persistent memory, and coordinated autonomy."*
*   **Verdict:** **Supported** (with year correction).
*   **Exact Source Location:** Sapkota et al., 2026, *Information Fusion*, 126, Article 103599.
*   **Verbatim Supporting Quote:**
    > *"...distinguishes AI Agents, defined as modular, task-specific systems driven by a single LLM with tool use, from Agentic AI, characterised by multi-agent collaboration, persistent memory, and coordinated autonomy."* [Exact conceptual taxonomy is mapped in Section 2].
*   **Assumptions & Mathematical Constraints:**
    *   Categorizes the transition from passive Generative AI (stateless, reactive) to single AI Agents, and finally to collaborative, multi-agent Agentic AI systems.

#### Critical Scrutiny & Thesis Risk Analysis
*   **The Year Error:** The thesis cites this as "Sapkota et al. (2025)". However, the paper's metadata and publication timeline confirm it was officially published in **2026** (Volume 126, Article 103599).
*   **Orchestration Coherence:** Ch1's definition of the multi-agent framework fully matches Sapkota's "Agentic AI" definition, ensuring perfect alignment across the thesis chapters.

#### Safest Thesis-Ready Wording
```latex
Following the taxonomy of Sapkota et al. (2026), we distinguish single-agent systems (modular, task-specific entities executing individual tools) from Agentic AI, which is characterized by multi-agent collaboration, persistent memory, and coordinated, decentralized autonomy over complex workflows.
```

---

### Claims ID: LR-23 to LR-26 — Multi-Agent Orchestration Metadata

*   **Audit of Citations:**
    *   **LR-23 (DyLAN):** Cited as "Liu, Z., et al. (2023)". The correct author list and year are **Liu et al. (2024)**, published in the *First Conference on Language Modeling* (CoLM 2024).
    *   **LR-24 (AutoFlow):** Cited as "Chen, Z., et al. (2024)". The correct first author is **Li et al. (2024)** (Title: "AutoFlow: Automated Workflow Generation for Large Language Model Agents").
    *   **LR-25 (ScoreFlow):** Cited as "Wu, Y., et al. (2025)". The correct first author is **Wang et al. (2025)** (Title: "ScoreFlow: Mastering LLM Agent Workflows via Score-based Preference Optimization").
    *   **LR-26 (SVS):** Cited as "Huang, J., et al. (2024)". The correct first author is **Guo et al. (2025)** (Title: "Sample, Predict, then Proceed: Self-Verification Sampling for Tool Use of LLMs").
*   **Normative Claim Scrutiny:** Ch2 claims graph-based orchestration *"reflects best practice for multi-agent systems."* This is an editorial overstatement; the papers propose graph-based optimization algorithms as empirically superior architectures but do not define them as a universal "best practice" standard.

#### Safest Thesis-Ready Wording
```latex
% Replace the multi-agent paragraph in Ch2:75 with the following:
Emerging frameworks have shifted toward structured, graph-based workflow orchestration, which can be generated and optimized programmatically. For example, Li et al. (2024) introduced AutoFlow, which automates agent workflow generation via reinforcement learning, while Wang et al. (2025) proposed ScoreFlow, which optimizes agent graphs using preference optimization (Score-DPO) to enforce runtime and cost constraints. To improve tool execution reliability, Guo et al. (2025) developed Self-Verification Sampling (SVS), enabling agents to generate multiple tool call trajectories, predict their resulting environmental states, and select the optimal path before execution. Combined with dynamic collaboration protocols (such as DyLAN; Liu et al., 2024), these graph-based patterns demonstrate empirically superior consistency and error recovery compared to fixed agent pipelines.
```
