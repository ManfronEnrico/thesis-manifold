# Source-Level Verification Report
## Section B: Global versus Local Forecasting

This report provides a rigorous source-level verification of claims **GL-01 through GL-05** concerning the global versus local forecasting paradigm, assessed against the primary text: **Montero-Manso, P., & Hyndman, R. J. (2021). "Principles and algorithms for forecasting groups of time series: locality and globality." *International Journal of Forecasting*, 37(4), 1632–1653.**

---

### Verification Summary Table

| Claim ID | Proposed Claim | Verdict | Source and Page | Exact Supporting Passage | Safest Thesis-Ready Wording |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GL-01** | A local forecasting approach fits a separate forecasting function or model to each series, whereas a global approach estimates a single function across multiple series. | **Supported** | Page 1632 (Abstract), Page 1633 (Section 1), Page 1634 (Section 2.1) | "The local approach fits a function to each time series in the set. The global approach fits the same function to all time series in the set." (p. 1634) | A local forecasting approach fits a separate, independent model or function to each individual time series, whereas a global approach estimates a single, shared forecasting function across a pooled set of multiple time series [1]. |
| **GL-02** | A global forecasting model is not inherently restricted to groups of homogeneous or similar time series. | **Supported** | Page 1632 (Abstract), Page 1634 (Section 2.1, Proposition 1), Page 1648 (Section 6.2) | "Global and local methods can produce the same forecasts without any assumptions about similarity of the series in the set." (p. 1632) | In the general univariate setting, a global forecasting model is not theoretically restricted to homogeneous or similar time-series groups; under mild uniqueness assumptions, any set of forecasts produced by independent local estimators can be mathematically replicated by a single, shared global function [1]. |
| **GL-03** | Model complexity of local models grows with the number of series, while global model complexity can remain fixed, giving global models a generalization advantage. | **Supported with Qualification** | Page 1632 (Abstract), Page 1638 (Section 3.3, Proposition 2) | "The complexity of local methods grows with the size of the set while it remains constant for global methods." (p. 1632); Proposition 2 bounds (p. 1638). | Assuming cross-series independence, the aggregate model complexity of a collection of local estimators scales with the number of time series in the dataset, whereas the complexity of a global model remains constant; this theoretical scaling properties can afford global models a superior generalization bound [1]. |
| **GL-04** | Global models are advantageous when individual series are short because pooling observations allows a more complex model to be estimated without overfitting. | **Supported** (Theoretical & Empirical Inference) | Page 1633 (Section 1), Page 1642 (Section 5.1) | "The global approach... prevents over-fitting because a larger sample size is used for learning compared to a local counterpart." (p. 1633) | When individual time series are short, data-driven local models are highly prone to overfitting due to limited sample sizes; global models mitigate this constraint by pooling observations across series, enabling the robust estimation of more flexible shared parameters [1]. |
| **GL-05** | Global models begin to outperform local models once the pooled dataset contains approximately 750–1,000 observations. | **Contradicted** (as a universal claim from the source) | Not Found in Montero-Manso & Hyndman (2021) | *No such numerical threshold exists in the text.* | The specific crossover threshold of approximately 750 to 1,000 observations—below which pooled global models outperform specialized local estimators—is an empirical, study-specific design finding of this thesis rather than a universal threshold established in literature [1]. |

---

### Detailed Analysis and Scrutiny of Claims

#### **GL-01: Definition of Global and Local Models**
*   **Verdict:** **Supported**
*   **Source and Page:** Montero-Manso & Hyndman (2021), Page 1632 (Abstract), Page 1633 (Section 1), Page 1634 (Section 2.1)
*   **Exact Supporting Passage:** 
    *   *Abstract (p. 1632):* "Global methods that fit a single forecasting method to all time series in a set have recently shown surprising accuracy, even when forecasting large groups of heterogeneous time series... traditional local methods that fit a separate forecasting method to each series..."
    *   *Section 1 (p. 1633):* "The idea behind the global approach is to introduce the strong assumption that all time series in the set come from the same process... Global methods pool the data of all series together and fit a single univariate forecasting function..."
    *   *Section 2.1 (p. 1634):* "The local approach fits a function to each time series in the set. The global approach fits the same function to all time series in the set. Both approaches are learning algorithms, functions that take data as input and produce forecasting functions as output."
*   **Safest Thesis-Ready Wording:** 
    > "A local forecasting approach fits a separate, independent model or function to each individual time series, whereas a global approach estimates a single, shared forecasting function across a pooled set of multiple time series [1]."

---

#### **GL-02: General Applicability and Heterogeneity**
*   **Verdict:** **Supported**
*   **Source and Page:** Montero-Manso & Hyndman (2021), Page 1632 (Abstract), Page 1634 (Section 2.1), Page 1648 (Section 6.2)
*   **Exact Supporting Passage:**
    *   *Abstract (p. 1632):* "Global and local methods can produce the same forecasts without any assumptions about similarity of the series in the set."
    *   *Section 2.1 (p. 1634):* "local and global approaches do not differ in the forecasts they are able to produce... local and global methods are equally general."
    *   *Section 6.2 (p. 1648):* "From Proposition 1 we can derive that global models can approximate general sets as well as local models, without requiring similarity or other 'tricks'..."
*   **Formal Reasoning Scrutiny:** 
    The authors prove equivalence via **Proposition 1 (Equivalence of Local and Global Algorithms)**. Under realistic assumptions:
    1. Let $S = \{X_1, \dots, X_K\}$ be a set of $K$ historical series. Let $A_L$ be a local algorithm that fits independent functions $\{f_1, \dots, f_K\}$ such that the forecast for $X_i$ is $f_i(X_i)$.
    2. If all $X_i$ in $S$ are unique ($X_i \neq X_j$ for all $i \neq j$), the set of target forecasts $\{f_i(X_i)\}$ is finite. A single global function $g$ can always be constructed (using universal approximators like high-order polynomials, kernels, or neural networks) such that $g(X_i) = f_i(X_i)$ for all $i \in \{1, \dots, K\}$.
    3. If there exists some $X_i = X_j$ but $f_i(X_i) \neq f_j(X_j)$, a single function $g$ cannot map the identical input to different outputs. However, because a local algorithm $A_L$ is a deterministic function of the data, equal inputs *must* map to equal local models ($X_i = X_j \implies A_L(X_i) = A_L(X_j) \implies f_i = f_j \implies f_i(X_i) = f_j(X_j)$). Thus, this contradiction cannot occur in time-series forecasting.
    4. *Crucial Caveat:* To guarantee equivalence when models have finite memory ($M < T$), the global model must use relatively *longer memory* than the local model to resolve identical subsequences.
*   **Safest Thesis-Ready Wording:**
    > "In the general univariate setting, a global forecasting model is not theoretically restricted to homogeneous or similar time-series groups; under mild uniqueness assumptions, any set of forecasts produced by independent local estimators can be mathematically replicated by a single, shared global function [1]."

---

#### **GL-03: Model Complexity and Generalization Bounds**
*   **Verdict:** **Supported with Qualification**
*   **Source and Page:** Montero-Manso & Hyndman (2021), Page 1632 (Abstract), Page 1638 (Section 3.3, Proposition 2)
*   **Exact Supporting Passage:**
    *   *Abstract (p. 1632):* "The complexity of local methods grows with the size of the set while it remains constant for global methods. This result supports the recent evidence and provides principles for the design of new algorithms."
    *   *Section 3.3 (p. 1638):* "For the local approach, the size of the hypothesis class is the size of the Cartesian product of all the local hypotheses $H_i$ used to fit the series, while for the global approach, the size is $|J|$."
    *   *Proposition 2 Generalization Bounds:*
        $$E_{\text{Local}}^{\text{out}} < E_{\text{Local}}^{\text{in}} + \sqrt{\frac{\log\left(\prod_{i=1}^K |H_i|\right) + \log\left(\frac{2}{\delta}\right)}{2NK}}$$
        $$E_{\text{Global}}^{\text{out}} < E_{\text{Global}}^{\text{in}} + \sqrt{\frac{\log(|J|) + \log\left(\frac{2}{\delta}\right)}{2NK}}$$
*   **Critical Scrutiny and Assumptions:**
    *   **Independence Assumption:** The generalization bounds in Proposition 2 strictly rely on the **assumption of independence between the different time series in the set** (p. 1638) to apply the Hoeffding inequality. Under heavy cross-series correlation, the theoretical generalization guarantees lose their validity (though empirical performance may remain robust).
    *   **Effective Sample Size:** It assumes an equal effective sample size $N$ for each of the $K$ series, resulting in $NK$ total samples in the pooled dataset.
    *   **Nature of Bound:** This is a **theoretical generalization error bound** (worst-case probabilistic difference between training and testing error). The paper validates this theory via **empirical findings** across 20+ large benchmark datasets (e.g., M1, M3, M4, Tourism), demonstrating that global models generalize better (narrower gap between in-sample and out-of-sample error, as illustrated in Fig. 5, p. 1644).
*   **Safest Thesis-Ready Wording:**
    > "Assuming cross-series independence, the aggregate model complexity of a collection of local estimators scales with the number of time series in the dataset, whereas the complexity of a global model remains constant; these theoretical scaling properties can afford global models a superior generalization bound [1]."

---

#### **GL-04: Advantage on Short Time Series**
*   **Verdict:** **Supported**
*   **Source and Page:** Montero-Manso & Hyndman (2021), Page 1633 (Section 1), Page 1642 (Section 5.1)
*   **Exact Supporting Passage:**
    *   *Section 1 (p. 1633):* "Temporal dependence and the short length of the series make time series forecasting a notoriously difficult problem. Individual time series cannot be modeled in a data-driven way because even basic models (e.g. linear models) will suffer from over-fitting... The global approach... prevents over-fitting because a larger sample size is used for learning compared to a local counterpart."
    *   *Section 5.1 (p. 1642):* "Realistically, we would need 10–100-times more observations than parameters in a single series to fit it by ordinary least squares. Global methods use the whole dataset to fit these coefficients."
*   **Safest Thesis-Ready Wording:**
    > "When individual time series are short, data-driven local models are highly prone to overfitting due to limited sample sizes; global models mitigate this constraint by pooling observations across series, enabling the robust estimation of more flexible shared parameters [1]."

---

#### **GL-05: Universal Crossover Threshold (750–1,000 Observations)**
*   **Verdict:** **Contradicted** (as a general claim attributed to this source) / **Not Found**
*   **Scrutiny and Flagging:**
    There is **no mention** of a "750–1,000 observations" threshold in Montero-Manso and Hyndman (2021). The datasets analyzed in their work represent vastly different scales (ranging from 617 series in M1 to 100,000 series in M4, with lengths from 24 to thousands of observations). 
    *   **Source of the Threshold:** This crossover threshold (~750 to 1,000 brand-month observations) is an **empirical finding specific to the dataset and category partitions evaluated in your thesis** (where specialized local/category-specific models only began to beat global models when category observations crossed this scale). Attributing this numerical range to Montero-Manso and Hyndman (2021) is a **misattribution and a severe factual overstatement**.
*   **Safest Thesis-Ready Wording:**
    > "The specific crossover threshold of approximately 750 to 1,000 observations—below which pooled global models outperform specialized local estimators—is an empirical, study-specific design finding of this thesis rather than a universal threshold established in literature [1]."

---

### Key Recommendations for the Thesis Draft

1.  **Do not cite Montero-Manso & Hyndman (2021) for the 750–1,000 observation threshold.** Report this strictly as your own empirical finding from your beverage demand dataset. Use Montero-Manso & Hyndman (2021) only to provide the *theoretical backing* (e.g., sample size limitations of local parameters, p. 1633) that explains *why* a crossover threshold exists.
2.  **Explicitly state the independence assumption** when discussing the generalization advantage of global models. Acknowledging that the mathematical bound (Proposition 2) assumes cross-series independence demonstrates exceptional academic rigour.
3.  **Emphasize the memory requirement.** When explaining why global models can outperform local ones on heterogeneous data, cite their discovery that global models require *relatively longer memory* (Proposition 1 and Section 3.5, p. 1639) to achieve the same approximation capacity as local models.

---
### **References**
*   **[1]** Montero-Manso, P., & Hyndman, R. J. (2021). "Principles and algorithms for forecasting groups of time series: locality and globality." *International Journal of Forecasting*, 37(4), 1632–1653.
