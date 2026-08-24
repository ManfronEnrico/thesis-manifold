# Conformal Prediction: Source-Level Sourcing and Verification Report (Section A)

This report provides a rigorous, source-grounded verification of the conformal prediction claims (CP-01 through CP-06) outlined in the Master's Thesis Handover Report. Each claim has been evaluated against the original, peer-reviewed source materials contained in the project's repository. Every verdict and factual assertion is directly traceable to the specific sections, pages, and mathematical formulations of the sources.

---

## 1. Final Verified Claim Bank

Below is the clean, consolidated list of verified claims for Section A (Conformal Prediction), formulated using the safest and most mathematically precise wording, accompanied by exact page and section citations. These entries are ready to be integrated directly into the final thesis.

1. **CP-01 (Supported):** Papadopoulos et al. (2002) introduced the **Inductive Confidence Machine (ICM)** for regression to overcome the computational inefficiency of the earlier Transductive Confidence Machine (TCM). The ICM separates model fitting from confidence estimation by splitting the training dataset into a *proper training set* and a *calibration set*. The regression model is trained on the proper training set only once, and prediction intervals are constructed by ranking the test candidate's residual against the calibration residuals, resulting in a massive improvement in computational efficiency [27, 28, 30]. *(Source: Papadopoulos et al., 2002, pp. 345–347, 349).*
2. **CP-02 (Supported):** Split conformal prediction constructed from i.i.d. (or exchangeable) training samples $(X_i, Y_i)_{i=1}^n$ provides a guaranteed distribution-free, finite-sample marginal coverage level of at least $1 - \alpha$ for a new test point $(X_{n+1}, Y_{n+1})$ [2764, 2765]. This coverage guarantee is marginal rather than conditional, holds for any arbitrary symmetric regression algorithm $\hat{\mu}$, and does not rely on any model assumptions or consistency properties of the estimator [2757, 2758, 2764]. *(Source: Lei et al., 2018, Section 2.2, Theorem 2).*
3. **CP-03 (Supported):** Split conformal inference is computationally cheaper than full conformal inference because the base regression model is trained only once, whereas full conformal inference requires retraining the model for every candidate value $y$ on a grid [2762, 2763]. However, this gain in computational efficiency comes at the cost of statistical efficiency, as split conformal prediction trains its model on only a portion of the available data, which can result in wider prediction intervals [2764]. *(Source: Lei et al., 2018, Sections 2.1 and 2.2).*
4. **CP-04 (Supported):** Weighted conformal prediction generalizations can bound the loss of coverage (the **coverage gap**) under violations of exchangeability (such as distribution drift over time) without making any assumptions on the joint distribution of the data [2505, 2510, 2511]. The coverage gap—defined as the difference between the nominal level $1 - \alpha$ and the true probability of coverage—is bounded by a weighted sum of the total variation ($d_{TV}$) distance terms between the swapped sequences or their residuals [2510, 2511, 2528]. *(Source: Barber et al., 2023, Sections 1.2 and 4.1, Theorem 2).*
5. **CP-05 (Supported):** Conformal prediction can be generalized to non-exchangeable time-series observations using weighted quantiles, but ordinary, unmodified split conformal prediction (which applies equal weights $w_i \equiv 1$) does not automatically retain its nominal $1-\alpha$ coverage guarantee when exchangeability is violated due to distribution drift or temporal autocorrelation [2506, 2510, 2511, 2524]. *(Source: Barber et al., 2023, Sections 1, 1.2, and 3.1).*

---

## 2. Detailed Claim-by-Claim Verification

### CP-01 — Origin of Inductive Conformal Regression
* **Source:** Papadopoulos et al. (2002), "Inductive Confidence Machines for Regression."
* **Thesis Claim:** Papadopoulos et al. introduced an inductive approach to conformal regression that separates model fitting from confidence estimation and is computationally more efficient than the earlier transductive approach.
* **Verdict:** **Supported**
* **Grounded Analysis:**
  * **Terminology Check:** 
    * The paper explicitly uses the term **"Inductive Confidence Machine" (ICM)** in its title, abstract, and Section 2 (pages 345, 346–347) [26, 28].
    * It contrasts ICM with the earlier **"Transductive Confidence Machine" (TCM)**, mentioning "transductive inference" and "transductive techniques" (pages 345, 346) [26, 27].
    * Regarding computational complexity, Section 1 states: *"The main disadvantage of the existing variants of TCM is their relative computational inefficiency... This paper makes a much more radical step introducing Inductive Confidence Machine, ICM... On the other hand, the improvement in the computational efficiency is massive."* (pages 346, 355) [27, 36].
  * **Procedural Steps (Grounded in Section 2, pp. 347, 349) [28, 30]:**
    1. **Data Splitting:** The training dataset of $l$ examples is split into two subsets: a *proper training set* $\{ (x_1, y_1), ..., (x_m, y_m) \}$ with $m < l$ elements, and a *calibration set* $\{ (x_{m+1}, y_{m+1}), ..., (x_l, y_l) \}$ with $k := l - m$ elements.
    2. **Model Training:** A regression algorithm (e.g., Ridge Regression) is applied to the proper training set *only once* to derive a prediction rule.
    3. **Strangeness of Calibration Set:** Using the derived prediction rule, a *strangeness measure* (absolute residual) is associated with each pair in the calibration set:
       $$\alpha_i := |y_{m+i} - \hat{y}_{m+i}| \quad \text{for } i = 1, ..., k$$
    4. **Strangeness of Candidate:** For a new unlabelled test point $x_{l+1}$ and a candidate label $y \in \mathbb{R}$, we calculate the test point's strangeness:
       $$\alpha_{k+1} := |y - \hat{y}_{l+1}|$$
    5. **p-Value Calculation:** The p-value associated with the candidate label $y$ is computed as:
       $$p(y) := \frac{\# \{ i = 1, ..., k+1 : \alpha_i \ge \alpha_{k+1} \}}{k+1}$$
    6. **Interval Construction:** The prediction region at a significance level $\delta$ (where confidence is $1 - \delta$) is defined as $\{ y : p(y) > \delta \}$.
  * **Bibliographic Verification:** The paper was published in *Proceedings of the 13th European Conference on Machine Learning (ECML 2002)*, Springer LNCS 2430, pp. 345–356. *(Corrected from the erroneous pp. 327–338).* [26, 2503]

---

### CP-02 — Split-Conformal Coverage
* **Source:** Lei et al. (2018), "Distribution-Free Predictive Inference for Regression."
* **Thesis Claim:** Split conformal inference can construct prediction intervals around an arbitrary regression estimator while providing finite-sample marginal coverage under exchangeability.
* **Verdict:** **Supported**
* **Grounded Analysis:**
  * **Required Assumptions:** The coverage guarantee strictly requires that the training and test data points $(X_i, Y_i)_{i=1}^{n+1}$ are independent and identically distributed (i.i.d.) (or exchangeable) [2745, 2752]. Crucially, **no assumptions** are made regarding the underlying regression function $\mu$, the noise distribution, or the estimator $\hat{\mu}$ (except that $\hat{\mu}$ acts as a symmetric function of the training points) [2745, 2753].
  * **Finite-Sample Validity:** Yes, the coverage is valid nonasymptotically for any finite sample size $n$. This is proven in Theorem 2 (page 1099) [2746, 2764].
  * **Marginal vs. Conditional Coverage:** The coverage guarantee is strictly **marginal (average)** over the joint distribution of the training and test data [2758]. As Remark 3 (page 1098) explains: *"marginal... coverage guarantees. This should not be confused with $P(Y_{n+1} \in C(x) | X_{n+1} = x) \ge 1 - \alpha$ for all $x$, i.e. conditional coverage, which is a much stronger property and cannot be achieved by finite-length prediction intervals without regularity and consistency assumptions on the model and the estimator."* [2758]
  * **Arbitrary Estimator:** The estimator $\hat{\mu}$ can be completely arbitrary, including highly complex, non-consistent estimators [2744, 2749]. As noted on page 1095: *"the method always provides finite-sample coverage, in any setting—regardless of whether or not the lasso estimator is consistent."* [2749]
  * **Algorithm and Theorem Numbers:**
    * **Algorithm 2** (Split Conformal Prediction) on page 1098 outlines the splitting, fitting, and residual sorting procedure [2761, 2762].
    * **Theorem 2** (page 1099) establishes the lower bound and a continuous-residual upper bound:
      $$P(Y_{n+1} \in C_{\text{split}}(X_{n+1})) \ge 1 - \alpha$$
      $$P(Y_{n+1} \in C_{\text{split}}(X_{n+1})) \le 1 - \alpha + \frac{2}{n+2} \quad \text{(under continuous residuals)}$$ [2764]
  * **Bibliographic Verification:** Lei et al. (2018) was published in the *Journal of the American Statistical Association*, 113(523), 1094–1111. *(Corrected from the erroneous JRSS Series B, 80(5), 1097–1121).* [2503]

---

### CP-03 — Full versus Split Conformal
* **Source:** Lei et al. (2018), "Distribution-Free Predictive Inference for Regression."
* **Thesis Claim:** Split conformal inference is computationally cheaper than full conformal inference, although the data split may reduce statistical efficiency or produce wider intervals.
* **Verdict:** **Supported**
* **Grounded Analysis:**
  * **Computational Cost:** Section 2.2 states that the full conformal method is computationally intensive because it requires retraining the model on the augmented dataset $(X_1, Y_1), ..., (X_n, Yn), (X_{n+1}, y)$ for each trial value $y$ on a grid [2762]. In contrast: *"The split conformal method separates the fitting and ranking steps using sample splitting, and its computational cost is simply that of the fitting step."* [2763]
  * **Statistical Efficiency (Width):** Section 2.2 notes: *"A drawback of the split conformal method is the loss of accuracy due to sample splitting..."* [2764] because only a portion of the data is used to fit the model. Full conformal uses the entire augmented set of $n+1$ points for training: *"By avoiding data splitting, full conformal often (but not always) yields more precise [narrower] prediction intervals than split conformal."* [2764]

---

### CP-04 — Non-Exchangeable Observations
* **Source:** Barber et al. (2023), "Conformal Prediction Beyond Exchangeability."
* **Thesis Claim:** Classical conformal coverage relies on exchangeability, while weighted conformal procedures can reduce coverage loss under certain forms of distribution drift or non-exchangeability.
* **Verdict:** **Supported**
* **Grounded Analysis:**
  * **Definition of Robustness:** Mathematically, robustness is quantified by the **coverage gap**, which represents the maximum loss of coverage compared to the nominal level $1 - \alpha$ when exchangeability is violated:
    $$P(Y_{n+1} \in \hat{C}_n(X_{n+1})) \ge 1 - \alpha - \text{Coverage gap}$$ [2509, 2510]
  * **Established Bounds / Guarantees (Section 1.2, pp. 817–818; Section 4.1, p. 825) [2510, 2511, 2528]:**
    * For weighted conformal prediction with normalized weights $\tilde{w}_i$ (where $\sum_{i=1}^{n+1} \tilde{w}_i = 1$), the paper establishes bounds on the coverage gap with **no assumptions** on the joint distribution of the data:
      1. **Full Sequence Bound (Equation 3):**
         $$\text{Coverage gap} \le \frac{\sum_{i=1}^n w_i \cdot d_{TV}(Z, Z_i)}{1 + \sum_{i=1}^n w_i}$$
         where $Z = (Z_1, ..., Z_{n+1})$ is the original sequence, and $Z_i$ is the sequence after swapping the test point with the $i$-th training point: $Z_i = (Z_1, ..., Z_{i-1}, Z_{n+1}, Z_{i+1}, ..., Z_n, Z_i)$ [2510].
      2. **Residual-Based Bound (Equation 4):**
         $$\text{Coverage gap} \le \frac{\sum_{i=1}^n w_i \cdot d_{TV}(R(Z), R(Z_i))}{1 + \sum_{i=1}^n w_i}$$
         where $R(Z)$ represents the vector of residuals [2511].
      3. **Individual Points TV Bound (Theorem 2):** For a symmetric algorithm under distribution drift (independent but non-identically distributed data):
         $$\text{Coverage gap} \le 2 \sum_{i=1}^n \tilde{w}_i \cdot d_{TV}((X_i, Y_i), (X_{n+1}, Y_{n+1}))$$ [2528]
         where $d_{TV}$ is the total variation distance. If the data are exchangeable, $d_{TV} = 0$, the coverage gap becomes zero, recovering the nominal coverage rate of $1-\alpha$ exactly [2509, 2510].

---

### CP-05 — Time-Series Applicability
* **Source:** Barber et al. (2023), "Conformal Prediction Beyond Exchangeability."
* **Thesis Claim:** Barber et al. justify the use of conformal prediction for non-exchangeable forecasting observations, but do not establish that ordinary unmodified split conformal prediction automatically retains nominal coverage for every autocorrelated time series.
* **Verdict:** **Supported**
* **Grounded Analysis:**
  * Barber et al. (2023) introduce a weighted conformal prediction framework (weighted split and weighted full conformal) specifically designed to regain coverage under distribution drift or temporal non-exchangeability [2508, 2509].
  * They explicitly show that **unmodified, unweighted split conformal prediction** (where $w_i \equiv 1$) **loses coverage** significantly when exchangeability is violated [2507, 2508]. In their empirical demonstration on Australian electricity data (Figure 1, ELEC2 dataset), they show: *"over a substantial stretch of time, [standard unmodified] conformal prediction loses coverage, its intervals decreasing far below the target 90% coverage level."* [2507, 2508]
  * This is because, without temporal weights that prioritize recent data, the total variation distances in the coverage gap bound accumulate to a large value, rendering the lower bound of standard split conformal prediction vacuous [2510, 2511].

---

### CP-06 — Scrutiny Claim: Robustness on Autocorrelated Retail Demand
* **Source:** Lei et al. (2018); Barber et al. (2023).
* **Thesis Claim to Test:** Conformal prediction is guaranteed to achieve the target coverage on autocorrelated retail demand data even when exchangeability is violated.
* **Verdict:** **Contradicted (False)**
* **Grounded Analysis:**
  * **Violates Core Conformal Theory:** The absolute finite-sample coverage guarantee of standard conformal prediction (Theorem 1 and Theorem 2 of Lei et al., 2018) is strictly contingent upon the **exchangeability** (or i.i.d.) assumption of the residuals [2745, 2752, 2757].
  * **Proved Coverage Degradation:** For autocorrelated retail demand data, exchangeability is heavily violated due to temporal dependence and non-stationarity [2506]. In such settings, unmodified conformal prediction **does not provide any guarantee** of achieving the nominal target coverage [2507, 2508].
  * **Weighted Generalizations Are Not Absolute:** Even the robust, weighted nonexchangeable conformal procedures introduced by Barber et al. (2023) do not provide an absolute guarantee of achieving the target coverage under arbitrary exchangeability violations [2528]. Their coverage lower bound is $1 - \alpha - \text{Coverage gap}$, where the coverage gap is bounded by the weighted sum of total variation distances between distributions [2528]. If the temporal autocorrelation or distribution drift is too severe (meaning the total variation distance terms are large), the coverage gap will be large, and coverage can fall far below the nominal $1-\alpha$ target.
  * **Conclusion:** The assertion that conformal prediction is "guaranteed" to achieve nominal coverage on autocorrelated retail demand data when exchangeability is violated is scientifically incorrect and directly contradicted by the mathematical limits proven in the literature.

---

## 3. Corrected Bibliographic References (Section A)

The student's thesis must use the following corrected bibliographic citations, as several page ranges and journal titles were incorrectly listed in the Handover Report's original text:

1. **Papadopoulos et al. (2002):**
   * *Incorrect:* Papadopoulos, H., Proedrou, K., Vovk, V., & Gammerman, A. (2002). "Inductive Confidence Machines for Regression." *Proceedings of the 13th European Conference on Machine Learning (ECML 2002)*, pp. 327–338.
   * *Correct:* Papadopoulos, H., Proedrou, K., Vovk, V., & Gammerman, A. (2002). "Inductive Confidence Machines for Regression." In *Machine Learning: ECML 2002*, Lecture Notes in Artificial Intelligence (LNAI 2430), Springer, pp. **345–356** [2503].
2. **Lei et al. (2018):**
   * *Incorrect:* Lei, J., G’Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). "Distribution-Free Predictive Inference for Regression." *Journal of the Royal Statistical Society Series B: Statistical Methodology*, 80(5), 1097–1121.
   * *Correct:* Lei, J., G’Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). "Distribution-Free Predictive Inference for Regression." ***Journal of the American Statistical Association***, **113(523), 1094–1111** [2503].
