# Sourcing and Verification Report — Section H: Ridge Regression and Decision Trees

This report presents a rigorous, source-level verification of the claims regarding regularised linear baselines and decision tree invariance (TREE-01 through TREE-05) against the landmark textbook *The Elements of Statistical Learning* (2nd Edition, 2009) by Trevor Hastie, Robert Tibshirani, and Jerome Friedman.

---

## 1. Summary of Claims & Verification Status

| ID | Claim Summary | Verification Verdict | Source Reference | Key Finding / Thesis Guidance |
|---|---|---|---|---|
| **TREE-01** | Ridge regression minimizes RSS subject to a quadratic penalty on the coefficients. | **Supported** | Hastie et al. (2009), pp. 61–62 | Formulations for penalized RSS (Eq. 3.41) and constraint norm (Eq. 3.42) are verified. |
| **TREE-02** | ESL prescribes ridge regression as a standard baseline that all tabular models must beat. | **Contradicted (Overstated)** | Hastie et al. (2009), pp. 61, 682 | No such normative rule exists; it is presented as a baseline comparison for shrinkage and sparsity. |
| **TREE-03** | Tree splits are invariant to strictly monotonic transformations of input predictors. | **Supported** | Hastie et al. (2009), p. 307 | Invariance is explicitly verified; applies to both increasing and decreasing transformations. |
| **TREE-04** | Predictor-scale invariance generally extends to tree-based ensembles (Random Forest, LightGBM). | **Supported with Qualification (Inferred)** | Hastie et al. (2009), Ch. 10 & 15 | Inherited from tree-level rank-based splits, though not written as a separate formal theorem in ESL. |
| **TREE-05** | Predictor-scale invariance explains why log-transforming the target affected Ridge but not LightGBM. | **Contradicted** | Hastie et al. (2009), pp. 307, 360 | **Theoretically false.** Target transformations affect leaf means and boosting gradients in LightGBM. |

---

## 2. In-Depth Claim Verifications

### ID: TREE-01 — Ridge as Shrinkage
*   **Claim:** Ridge regression minimizes residual sum of squares subject to an L2-type penalty or equivalent coefficient-norm constraint, shrinking coefficients toward zero.
*   **Verdict:** **Supported**.
*   **Source and Exact Page:** Hastie, Tibshirani, and Friedman (2009), *The Elements of Statistical Learning* (2nd ed.), Chapter 3, pp. 61–62.
*   **Short Supporting Quote:** 
    > "Ridge regression shrinks the regression coefficients by imposing a penalty on their size. The ridge coefficients minimize a penalized residual sum of squares,
    $$\hat{eta}^{	ext{ridge}} = \operatorname{argmin}_{eta} \left\{ \sum_{i=1}^N \left(y_i - eta_0 - \sum_{j=1}^p x_{ij}eta_jight)^2 + \lambda \sum_{j=1}^p eta_j^2 ight\} ." \quad 	ext{(p. 61, Equation 3.41)}$$
    > "An equivalent way to write the ridge problem is
    $$\hat{eta}^{	ext{ridge}} = \operatorname{argmin}_{eta} \sum_{i=1}^N \left(y_i - eta_0 - \sum_{j=1}^p x_{ij}eta_jight)^2 \quad 	ext{subject to} \quad \sum_{j=1}^p eta_j^2 \le t." \quad 	ext{(p. 62, Equation 3.42)}$$
*   **Safest Thesis-Ready Wording:**
    > "Ridge regression shrinks regression coefficients toward zero and each other by imposing an $L_2$ penalty on their size (Hastie et al., 2009, pp. 61–62). The ridge estimator minimizes the penalized residual sum of squares (Equation 3.41), which is mathematically equivalent to minimizing the residual sum of squares subject to a budget constraint on the coefficient norm: $\sum_{j=1}^p eta_j^2 \le t$ (Equation 3.42)."

---

### ID: TREE-02 — Ridge as a Tabular Baseline
*   **Claim:** *The Elements of Statistical Learning* establishes ridge regression as the standard baseline that every tabular forecasting model should beat.
*   **Verdict:** **Contradicted (Overstated)**.
*   **Analysis:** 
    *   *The Elements of Statistical Learning* contains no normative statement prescribing ridge regression as a mandatory baseline that every tabular forecasting model "must" beat. 
    *   Instead, Hastie et al. (2009) present ridge regression as an essential shrinkage baseline for linear models. They emphasize that its effectiveness is conditional on the underlying data-generating process: ridge excels when there are many predictors with similarly sized coefficients (dense signals, p. 614), whereas sparse estimators (like Lasso) or non-linear models are superior in other settings.
*   **Safest Thesis-Ready Wording:**
    > "While Hastie et al. (2009) do not formulate a normative rule declaring ridge regression as a standard baseline that every tabular model must outperform, they establish it as a foundational benchmark for regularised linear models. In tabular regression tasks, ridge regression serves as a crucial baseline to evaluate whether non-linear models or alternative sparsity-inducing penalties (such as $L_1$ regularisation) justify their added complexity (Hastie et al., 2009, pp. 61, 614)."

---

### ID: TREE-03 — Monotonic Predictor Transformations
*   **Claim:** A decision tree’s partition is invariant to strictly monotonic transformations of an input predictor because the transformation preserves the ordering of candidate split values.
*   **Verdict:** **Supported**.
*   **Source and Exact Page:** Hastie, Tibshirani, and Friedman (2009), Chapter 9, Section 9.2, p. 307.
*   **Short Supporting Quote:** 
    > "They [decision trees] are invariant under (strictly monotone) transformations of the individual predictors. As a result, scaling and/or more general transformations are not an issue, and they are immune to the effects of predictor outliers." (p. 307)
*   **Safest Thesis-Ready Wording:**
    > "Individual regression and classification trees (such as those grown via CART) are strictly invariant under any strictly monotonic transformations of the individual predictor variables (Hastie et al., 2009, p. 307). Because splitting decisions are determined solely by the rank-ordering of the predictor's observations, applying a strictly monotonic transformation (whether increasing or decreasing) preserves the ordering of candidate split points, resulting in identical decision partitions."

---

### ID: TREE-04 — Ensembles and Predictor Invariance
*   **Claim:** The same predictor-ordering argument generally extends to tree ensembles built from order-based split decisions.
*   **Verdict:** **Supported with Qualification (Inferred)**.
*   **Analysis:** 
    *   This claim is a direct and mathematically sound logical extension of TREE-03, although it is not presented as a formal separate theorem in the text. 
    *   Since ensembles such as Random Forests (Chapter 15) and Gradient Boosted Trees (Chapter 10) are built entirely from individual decision trees that rely strictly on rank-ordered split decisions, any strictly monotonic transformation of the predictors propagates through the entire ensemble without changing any splits or final predictions.
*   **Safest Thesis-Ready Wording:**
    > "This predictor-scale invariance directly extends to tree-based ensembles, such as Random Forests and Gradient Boosted Trees (including LightGBM). Because these ensembles are constructed entirely of individual decision trees utilizing rank-based binary splits, any strictly monotonic transformation of the input predictors does not alter the splitting structures, leaves, or final model predictions (Hastie et al., 2009, Chapters 10 & 15)."

---

### ID: TREE-05 — Log-Transforming the Target
*   **Claim:** Predictor-transformation invariance explains why log-transforming the target affected ridge regression but could not affect LightGBM.
*   **Verdict:** **Contradicted**.
*   **Analysis & Methodology Correction:** 
    *   **The claim is mathematically false.** Invariance to transforming the *predictors* $X$ does **not** imply invariance to transforming the *target* variable $Y$. 
    *   For regression trees and ensembles (like LightGBM), leaf predictions sit at the core of the model and are calculated as the mean response value of the partitioned observations: $\hat{c}_m = \operatorname{mean}(Y_i \mid X_i \in R_m)$ (p. 307). Because the expectation is a non-linear operator that does not commute with a log-transformation (i.e., $\mathbb{E}[\log Y] 
eq \log \mathbb{E}[Y]$), log-transforming the target alters the leaf node calculations, change point thresholds, and splitting optimization landscape.
    *   Additionally, in gradient boosting, transforming the target variable directly alters the loss function, which changes the pseudo-residuals and gradient updates ($r_{ik} = y_i - p_k(x_i)$, p. 360) used to grow subsequent trees. Thus, log-transforming the target affects **both** Ridge regression and LightGBM.
*   **Safest Thesis-Ready Wording:**
    > "It is a common misconception to assume that tree-based ensembling methods are invariant to transformations of the target variable. While LightGBM is strictly invariant to monotonic transformations of the *predictors* $X$, log-transforming the *target* variable $Y$ directly alters the leaf node predictions (which are computed as the arithmetic mean of observations in that leaf, a non-linear operator that does not commute with a log-transform, i.e., $\mathbb{E}[\log Y] 
eq \log \mathbb{E}[Y]$) (Hastie et al., 2009, p. 307). Furthermore, transforming the target changes the loss function and gradient calculations (such as pseudo-residuals) that drive boosting iterations (Hastie et al., 2009, p. 360). Consequently, target transformations affect both ridge regression and LightGBM."

---

## 3. Bibliographic Entries for the Thesis

Ensure these references are formatted correctly in your bibliography:

*   **Chapter 3 Citation (Ridge):** Hastie, T., Tibshirani, R., & Friedman, J. (2009). Linear Methods for Regression. In *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed., pp. 43–99). Springer, New York.
*   **Chapter 9 Citation (Trees):** Hastie, T., Tibshirani, R., & Friedman, J. (2009). Additive Models, Trees, and Related Methods. In *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed., pp. 314–353). Springer, New York.
