# Sourcing and Verification Report — Section G: Model-Selection Bias

This report presents a rigorous, source-level verification of the model-selection bias claims (MS-01 through MS-04) against the original publication by Gavin C. Cawley and Nicola L. C. Talbot (2010), published in the *Journal of Machine Learning Research*.

---

## 1. Summary of Claims & Verification Status

| ID | Claim Summary | Verification Verdict | Source Reference | Key Finding / Thesis Guidance |
|---|---|---|---|---|
| **MS-01** | Model selection can overfit a noisy selection criterion just as training can overfit data. | **Supported** | Cawley & Talbot (2010), pp. 2079, 2080, 2083 | The variance of the estimator allows overfitting in the outer loop of multi-level inference. |
| **MS-02** | Using the same estimates to select and evaluate models introduces selection bias. | **Supported** | Cawley & Talbot (2010), pp. 2079, 2101 | Re-using the same observations for selection and evaluation leaks statistical information. |
| **MS-03** | Unbiased assessment requires nested cross-validation or an untouched test set. | **Supported** | Cawley & Talbot (2010), pp. 2080, 2094, 2101 | An "internal" (nested) cross-validation protocol must be used to report generalisation performance. |
| **MS-04** | Peeking at test results repeatedly can be described as "mildly optimistic." | **Qualified / Inferred** | Cawley & Talbot (2010), pp. 2101–2102 | The term "mild" is ungrounded. Peeking can introduce a bias of "surprising magnitude." |

---

## 2. In-Depth Claim Verifications

### ID: MS-01 — Overfitting the Selection Criterion
*   **Claim:** Hyperparameter and model selection can overfit a noisy selection criterion, just as model training can overfit training data.
*   **Verdict:** **Supported**.
*   **Source and Exact Page:** Cawley and Talbot (2010), *Journal of Machine Learning Research*, Vol. 11, No. 70, pp. 2079, 2080, 2083.
*   **Short Supporting Quote:** 
    > "While unbiasedness is often cited as a beneficial quality of a model selection criterion, we demonstrate that a low variance is at least as important, as a nonnegligible variance introduces the potential for over-fitting in model selection as well as in training the model... we show that the effects of this form of over-fitting are often of comparable magnitude to differences in performance between learning algorithms" (p. 2079, Abstract)
    > "Here we use 'over-fitting in model selection' to mean minimisation of the model selection criterion beyond the point at which generalisation performance ceases to improve and subsequently begins to decline." (p. 2083, Section 4)
*   **Safest Thesis-Ready Wording:**
    > "Just as a predictive model can overfit the training dataset at the first level of inference, Cawley and Talbot (2010, pp. 2079, 2083) demonstrate that optimization of a model-selection criterion over a finite dataset can lead to 'overfitting in model selection.' This occurs when a hyperparameter optimization routine minimizes a noisy selection criterion (such as cross-validation error or Bayesian evidence) beyond the point at which out-of-sample generalization performance ceases to improve, subsequently resulting in a decline in true test performance."
*   **Technical Context & Assumptions:**
    *   This form of overfitting is driven by the *variance* of the model-selection estimator. While leave-one-out cross-validation is nearly unbiased, its high variance makes it highly susceptible to overfitting when optimizing over a large or high-dimensional hyperparameter space (e.g., Automatic Relevance Determination kernels).
    *   The risk of model-selection overfitting scales with the number of hyperparameters being optimized and the smallness of the validation sample (p. 2092).

---

### ID: MS-02 — Selection Bias in Performance Evaluation
*   **Claim:** Using the same data or performance estimates both to select a model and to report its final performance can introduce optimistic selection bias.
*   **Verdict:** **Supported**.
*   **Source and Exact Page:** Cawley and Talbot (2010), pp. 2079, 2097, 2101.
*   **Short Supporting Quote:** 
    > "Furthermore, we show that some common performance evaluation practices are susceptible to a form of selection bias as a result of this form of over-fitting and hence are unreliable." (p. 2079, Abstract)
    > "In a biased evaluation protocol, occasionally observed in machine learning studies, an initial model selection step is performed using all of the available data... the test data are no longer statistically pure, as they have been 'seen' by the models in tuning the hyperparameters... We should therefore expect to observe an optimistic bias in the performance estimates obtained in this manner." (p. 2101, Section 5.3)
*   **Safest Thesis-Ready Wording:**
    > "Using the same dataset to both select model hyperparameters and evaluate final predictive performance introduces an optimistic selection bias. Because the hyperparameter optimization routine tunes parameters to exploit the statistical peculiarities of that specific sample, the evaluation data is no longer statistically independent or 'pure' (Cawley & Talbot, 2010, p. 2101). Cawley and Talbot (2010, p. 2097) prove that this bias remains highly significant even when there is absolutely no overlap between the training and test observations, as long as the hyperparameter selection procedure is exposed to evaluation-set variations."
*   **Technical Context & Assumptions:**
    *   Cawley and Talbot (2010, Section 5.2.1) perform a crucial experiment on a synthetic benchmark where training, validation, and test sets are strictly mutually disjoint (no shared observations). Yet, they prove that the "median" hyperparameter protocol still exhibits a statistically significant optimistic bias. This is because taking the median or selecting a "winner" based on evaluation sets acts as a variance-reduction step that artificially shields the reported error from the true out-of-sample variance.

---

### ID: MS-03 — Nested Evaluation
*   **Claim:** An unbiased assessment of a model-selection procedure requires evaluation data that did not influence the selection process, such as an outer evaluation loop or untouched test set.
*   **Verdict:** **Supported**.
*   **Source and Exact Page:** Cawley and Talbot (2010), pp. 2080, 2094, 2101.
*   **Short Supporting Quote:** 
    > "In order to avoid this bias, model selection must be treated as an integral part of the model fitting process and performed afresh every time a model is fitted to a new sample of data. Furthermore, as the differences in performance due to model selection are shown to be often of comparable magnitude to the difference in performance between learning algorithms... robust unbiased performance evaluation is likely to require more rigorous and computationally intensive protocols, such a nested cross-validation or 'double cross' (Stone, 1974)." (p. 2080)
    > "This is termed the 'internal' protocol as the model selection process is performed independently within each fold of the resampling procedure. In this way, the performance estimate includes a component properly accounting for the error introduced by over-fitting the model selection criterion." (p. 2094)
*   **Safest Thesis-Ready Wording:**
    > "To generate an unbiased assessment of a model's generalization performance, the model selection and training stages must be treated as an unified, single model-fitting procedure. Under a rigorous 'internal' or nested cross-validation protocol, model selection (including hyperparameter tuning) must be performed completely afresh within each fold of the outer cross-validation loop, utilizing only the local training fold (Cawley & Talbot, 2010, pp. 2080, 2094). This ensures that the outer validation folds remain completely untouched and have no influence—direct or indirect—on the model selection process."
*   **Technical Context & Assumptions:**
    *   In the "internal" (unbiased) protocol, the reported test metrics reflect the performance of the *combined algorithm-selection procedure*, rather than a single fixed set of hyperparameters. This is the only way to mathematically account for the variance and potential overfitting introduced during model selection.

---

### ID: MS-04 — "Mildly Optimistic" Results
*   **Claim:** If the final test results were inspected repeatedly while making modelling decisions, it is defensible to describe the reported performance as mildly optimistic.
*   **Verdict:** **Qualified / Inferred**.
*   **Source and Exact Page:** Cawley and Talbot (2010), pp. 2101–2102.
*   **Analysis & Thesis Guidance:**
    *   **Overstatement Flag:** Describing the resulting bias as "mild" is a subjective and statistically ungrounded assumption. Cawley and Talbot (2010, p. 2102) demonstrate that the optimistic bias introduced by an "external" (pre-tuned) protocol is often of "surprising magnitude" and can easily be "large enough to conceal even the true difference between state-of-the-art and uncompetitive learning algorithms."
    *   If final test partitions are repeatedly "peeked" at to make structural or hyperparameter adjustments, the reported results are **optimistically biased to an unquantifiable degree**. To ensure maximum academic rigor, the word "mildly" should be stripped from the thesis.
*   **Safest Thesis-Ready Wording:**
    *   *If the bias cannot be nested:* "Because final model selection decisions were made following successive iterations of testing, the reported out-of-sample metrics must be interpreted as optimistically biased to an unquantifiable degree. Peeking at test partitions during model selection creates an implicit memory of the evaluation data, which, as Cawley and Talbot (2010, p. 2102) warn, can introduce an optimistic bias of a magnitude sufficient to obscure true performance differences between competing algorithms."

---

## 3. Methodological Summary for the Thesis

To defend your evaluation protocol against examiner scrutiny, you must clearly distinguish between **internalized (nested) validation** and **externalized peeking**. The table below summarizes the methodological paths:

| Protocol Type | Cawley & Talbot Classification | Generalisation Validity | Impact on Your Results |
|---|---|---|---|
| **Nested Cross-Validation** (Model selection inside each outer fold) | **Internal (Unbiased)** | **100% Valid**. Reflects true operational performance of the pipeline. | Used for baseline model comparison on the main beverage dataset. |
| **Fixed Test-Set Peeking** (Adjusting models after viewing test-set scores) | **External (Biased)** | **Invalidated**. Introduces selection bias of "surprising magnitude." | Flagged as a limitation in the draft; results must be reported as optimistically biased. |

---

## 4. Correct Bibliographic Entry

Ensure your bibliography is formatted exactly as follows to prevent citation discrepancies:

*   **Standard Reference:** Cawley, G. C., & Talbot, N. L. C. (2010). On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. *Journal of Machine Learning Research*, 11(70), 2079–2107.
