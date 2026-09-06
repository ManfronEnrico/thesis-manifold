# Literature Review Sourcing and Verification Report — Section D: Reliability, Uncertainty, Evaluation

This report presents a rigorous, source-level audit of the claims, citations, and empirical assertions in **Literature Review Section D: Reliability, Uncertainty, Evaluation** against original PDF sources.

---

## Executive Summary of Audited Claims

| ID | Draft Statement / Claim | Cited Reference | Verdict | Key Finding / Correction |
| :--- | :--- | :--- | :--- | :--- |
| **LR-01a** | *"...specification compliance above 98% and median LLM numerical error below 3%..."* | González-Potes et al. (2026) | **Qualified** | Raw process compliance is 58% on average for alkaline. The 98% figure refers to **state specification consistency** ($\Gamma_s \geq 0.98$); median LLM error is verified below 3%. |
| **LR-01b** | *"...reduces CIP process duration by 12–18% and chemical consumption by up to 20%... achieving 100% regulatory compliance"* | "Bürger & Pauli (2024)" | **Contradicted** | **Fabricated Citation & Quote.** The paper does not exist, and the quoted metrics are completely fabricated; they must be purged. |
| **LR-01c** | *"...the authors explicitly note that it does not address predictive forecasting... or SME resource constraints..."* | González-Potes et al. (2026) | **Contradicted** | The authors do not state this themselves. This is an ungrounded thesis-author inference; must be reworded. |
| **LR-01d** | *"...domain matches... and no SME resource constraint is considered."* | González-Potes et al. (2026) | **Supported** | Domain is dairy CIP. Forecasting is absent, and no SME constraints are modeled. |
| **LR-01e** | *"...carefully separates deterministic and generative components."* | González-Potes et al. (2026) | **Supported** | The architecture wraps a deterministic supervisory/HMI panel with a RAG/Ollama conversational layer on top. |
| **LR-27** | *"...patterns including entity substitution, numerical imprecision, and unsupported causal attribution."* | Ji et al. (2024) [ANAH] | **Contradicted** | **Fabricated Categories.** ANAH's taxonomy classifies sentences into: No Hallucination, Contradictory, Unverifiable, and No Fact. |
| **LR-28** | *"...tool-using agents degrade systematically when tool inputs contain structured noise..."* | Wang et al. (2026) [AgentNoiseBench] | **Supported** | Evaluates ambiguous/inconsistent instructions and tool/reformatting noise (Preprint, Feb 2026). |
| **LR-29** | *"...structured traceability mechanisms materially reduce debugging effort..."* | Sapra et al. [Kartik et al. (2025)] | **Qualified** | Correct authors: Kartik et al. (2025). The debugging-effort reduction is conceptually asserted, not empirically measured. |
| **LR-30** | *"...specifying the artifacts — execution traces, tool-call spans, prompt and guardrail registries..."* | Dong et al. (2025) [Dong et al. (2024)] | **Supported** | Year corrected to 2024. AgentOps logs spans (tool, task, LLM, workflow) and integrates guardrails. |
| **LR-31** | *"...post-hoc isotonic-regression calibration can align empirical interval coverage... calibrated regression..."* | Kuleshov et al. (2018) | **Qualified** | Covers calibrated regression via CDF scaling, but does **not** cover conformal prediction. The thesis has no literature source for its conformal method. |
| **LR-32** | *"...confirm isotonic regression as a consistently effective calibration method... including LightGBM and XGBoost..."* | Levi et al. (2022) | **Contradicted** | **High Risk Misattribution.** The paper strictly evaluates neural networks (fully connected & DenseNet); it does **not** evaluate XGBoost or LightGBM. |
| **LR-33** | *"...CLEAR proposes evaluating enterprise agentic systems... correlation with deployment readiness..."* | Mehta (2025) | **Supported** | CLEAR dimensions and empirical correlation metrics are verified. It remains an arXiv preprint. |
| **LR-34** | *"...pairwise comparison tends to be more consistent than absolute scoring..."* | Gu et al. (2024) [Gu et al. (2025)] | **Supported** | Date corrected to 2025 (published October 2025). |
| **LR-35** | *"...position and self-enhancement bias... use a separate model... explicit bias checks."* | Ye et al. (2024) | **Supported** | Verified from paper. It remains an arXiv preprint. |

---

## Detailed Claim-by-Claim Breakdown

### Claim ID: LR-01 — The González-Potes CIP Case Study Audit

*   **Draft Statement:**
    > Ch1: *"...specification compliance above 98% and median LLM numerical error below 3%..."*
    > Bürger note: *"...reduces CIP process duration by 12–18% and chemical consumption by up to 20% relative to experienced human operators, while achieving 100% regulatory compliance."*
    > Ch2: *"...the authors explicitly note that it does not address predictive forecasting over historical tabular data or the resource constraints of small-to-medium enterprise deployments."*
*   **Verdict:**
    *   **LR-01a (Ch1 numbers):** **Qualified**. Raw compliance was only 58% on average for the degraded alkaline stages (CIP 3 was 0% compliant due to sustained low flow/temperature). The 98% figure refers to **state specification consistency ($\Gamma_s \geq 0.98$)**, meaning the rule-based label (WARNING/CRITICAL) matched the actual process conditions 98% of the time (Section 6.1, p. 38). Median LLM numerical error was indeed below 3% (Section 6.4, p. 41).
    *   **LR-01b (Bürger note):** **Contradicted** (Fabricated). The Bürger & Pauli (2024) paper is non-existent. The quoted 12-18% duration and 20% chemical reductions are completely fabricated and must be purged from the repository.
    *   **LR-01c (Attribution):** **Contradicted**. The authors do not state this limitations sentence themselves; it is an ungrounded thesis-author inference.
*   **Exact Source Location:** González-Potes et al., 2026, *AI* (MDPI), 7(1), pp. 305–328.

#### Critical Scrutiny & Thesis Risk Analysis
*   **Fabrication Purge:** The non-existent "Bürger & Pauli" reference and its corresponding quote must be completely removed from `obisdian_paper_analysis` and any other repository files.
*   **ATTRIBUTION Error:** Ch2 claims the authors "explicitly note" gaps in tabular forecasting and SME resource constraints. This is a severe attribution error; the paper's actual limitations (Section 8.2) focus on the lack of process diversity (single CIP site) and the need for formal verification in pharma manufacturing (p. 46).

#### Safest Thesis-Ready Wording
```latex
% Replace the González-Potes paragraph in Ch2:109 with:
González-Potes et al. (2026) implemented a real-time decision-support system for a Clean-in-Place (CIP) batch process at an operational beverage plant, demonstrating that wrapping deterministic rule-based supervisors with a retrieval-augmented generation (RAG) conversational agent (using a locally deployed Qwen 2.5 7B model) achieved a state specification consistency ($\Gamma_s$) above 98\% and a median LLM numerical error below 3\% in summarizing buffered time-series variables. However, their architecture is strictly process-monitoring oriented and does not address predictive time-series forecasting over historical tabular databases, nor does it evaluate the severe hardware or cost constraints of small-to-medium enterprise (SME) edge deployments.
```

---

### Claim ID: LR-27 — Ji's ANAH Hallucination Taxonomy

*   **Draft Statement:**
    > *"Ji et al. (2024) establish a systematic taxonomy of LLM hallucination … classifying factual errors into identifiable patterns including entity substitution, numerical imprecision, and unsupported causal attribution."*
*   **Verdict:** **Contradicted** (Fabricated Categories).
*   **Exact Source Location:** Ji et al., 2024, *ANAH: Analytical Annotation of Hallucinations in Large Language Models*, pp. 8135-8146.
*   **Verbatim Supporting Quote:**
    > *"Each sentence... undergoes rigorous annotation, involving the retrieval of a reference fragment, the judgment of the hallucination type (No/Contradictory/Unverifiable Hallucination, and No Fact)..."* (Abstract, p. 8135)

#### Critical Scrutiny & Thesis Risk Analysis
*   **Taxonomy Discrepancy:** The thesis invents category names ("entity substitution", "numerical imprecision", "unsupported causal attribution") and attributes them to Ji et al. (2024). ANAH's actual taxonomy strictly utilizes **four** high-level sentence types: (1) **No Hallucination (None)**, (2) **Contradictory Hallucination**, (3) **Unverifiable Hallucination**, and (4) **No Fact** (p. 8138).
*   Citing ANAH to motivate the validation of numeric forecasts via "numerical imprecision" is a severe misreport that will fail examiner review.

#### Safest Thesis-Ready Wording
```latex
Ji et al. (2024), in their ANAH benchmark for knowledge-based generative question answering, established a sentence-level annotation framework that systematically classifies language model outputs into four mutually exclusive categories: No Hallucination (fully supported by the reference text), Contradictory Hallucination, Unverifiable Hallucination (lacking reference evidence), and No Fact (containing no evaluable factual content).
```

---

### Claim ID: LR-32 — Levi et al. (2022) Model Families

*   **Draft Statement:**
    > *"confirm isotonic regression as a consistently effective calibration method across datasets and model families, including gradient-boosted trees such as LightGBM and XGBoost."*
*   **Verdict:** **Contradicted** (High Risk Misattribution).
*   **Exact Source Location:** Levi et al., 2022, *Sensors*, 22, 5540.
*   **Verbatim Supporting Quote:**
    > *"We train a fully connected network with four layers and a ReLU activation function on the generated training set... We use the DenseNet architecture... for the depth regression task."* (p. 5, 6)

#### Critical Scrutiny & Thesis Risk Analysis
*   **Severe Misattribution:** The thesis claims Levi et al. evaluated "gradient-boosted trees such as LightGBM and XGBoost." However, the paper **only** evaluates **neural networks** (a 4-layer fully connected MLP and a deep DenseNet convolutional architecture, p. 5, 6). There is **no** mention or evaluation of XGBoost, LightGBM, or any other gradient-boosted tree algorithms. Citing this to justify calibrating LightGBM forecasts is academically ungrounded.
*   The paper does, however, confirm that post-hoc isotonic regression (proposed by Kuleshov) is highly effective at minimizing Expected Normalized Calibration Error (ENCE) on neural networks.

#### Safest Thesis-Ready Wording
```latex
While Levi et al. (2022) confirmed that post-hoc isotonic regression (Kuleshov et al., 2018) is a consistently effective method to calibrate expected uncertainty intervals—minimizing Expected Normalized Calibration Error (ENCE) across diverse regression datasets—their empirical evaluations were strictly restricted to neural network architectures (MLPs and DenseNets). Causal extensions of this post-hoc calibration to gradient-boosted tree ensembles (such as LightGBM and XGBoost) represent a critical empirical gap in the literature.
```

---

### Claim ID: LR-31 — Kuleshov's Conformal Prediction Gap

*   **Draft Statement:**
    > *"Kuleshov et al. (2018) establish that post-hoc isotonic-regression calibration can align empirical interval coverage with stated coverage probabilities."*
*   **Verdict:** **Qualified** (for the conformal prediction claim).
*   **Exact Source Location:** Kuleshov et al., 2018, *Proceedings of the 35th International Conference on Machine Learning* (PMLR 80).

#### Critical Scrutiny & Thesis Risk Analysis
*   **The Conformal Gap:** In Ch2, the thesis associates Kuleshov with conformal prediction. However, Kuleshov's paper **does not cover conformal prediction at all**. It proposes a post-hoc CDF scaling method using isotonic regression on the empirical cumulative distribution function. Conformal prediction (e.g., split-conformal prediction) is a fundamentally different distribution-free framework with finite-sample coverage guarantees (Lei et al., 2018; Barber et al., 2023).
*   **Risky Gap:** Ch2 currently lacks any literature review on **conformal prediction**, even though the thesis's actual artifact serves split-conformal intervals. Conformal prediction literature (specifically split-conformal, Lei et al., 2018) **must** be written into Ch2.

#### Safest Thesis-Ready Wording
```latex
Kuleshov et al. (2018) demonstrated that a simple post-hoc calibration algorithm utilizing isotonic regression to scale predicted cumulative distribution functions (CDFs) can successfully align empirical interval coverage with stated confidence probabilities across general regression and time-series tasks. However, their scaling method does not provide the distribution-free, finite-sample coverage guarantees characteristic of formal conformal prediction frameworks (e.g., Lei et al., 2018; Barber et al., 2023), representing a distinct mathematical family.
```
