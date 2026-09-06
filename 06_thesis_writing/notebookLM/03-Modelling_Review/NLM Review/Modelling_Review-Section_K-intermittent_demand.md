# Sourcing and Verification Report — Section K: Intermittent/Zero-Inflated Demand

This report presents a rigorous, source-level verification of the claims regarding intermittent and zero-inflated demand modeling (ID-01 through ID-05) against the original publications: *The Accuracy of Intermittent Demand Estimates* (2005) by Aris A. Syntetos and John E. Boylan, and *On the Categorization of Demand Patterns* (2005) by Aris A. Syntetos, John E. Boylan, and J. D. Croston.

---

## 1. Summary of Claims & Verification Status

| ID | Claim Summary | Verification Verdict | Source Reference | Key Finding / Thesis Guidance |
|---|---|---|---|---|
| **ID-01** | Syntetos & Boylan evaluate the accuracy of intermittent forecasting models on real automotive data. | **Supported** | Syntetos & Boylan (2005), pp. 303, 304 | Compares SMA, SES, Croston's, and SBA on 3,000 real automotive series. |
| **ID-02** | The authors derive a multiplicative bias-correction factor of $(1 - lpha/2)$ for Croston's estimator (SBA). | **Supported** | Syntetos & Boylan (2005), p. 304 | Derives the Syntetos–Boylan Approximation (SBA) to resolve Croston's mathematical bias. |
| **ID-03** | Demand patterns are categorized into quadrants using thresholds of $p = 1.32$ and $CV^2 = 0.49$. | **Supported** | Syntetos et al. (2005), pp. 495, 499 | Establishes the canonical 2D classification (Smooth, Intermittent, Erratic, Lumpy). |
| **ID-04** | Syntetos & Boylan recommend excluding highly intermittent series from forecasting datasets. | **Contradicted** | Syntetos & Boylan (2005) | **Theoretical Error.** The authors advocate for specialized estimators (SBA), not data exclusion. |
| **ID-05** | Any intermittent exclusion threshold used in this thesis is an empirical design decision, not a universal law. | **Supported** | Syntetos & Boylan (2005) | **Thesis Recommendation.** Formulates a robust defense of your hand-off rule for zero-inflated series. |

---

## 2. In-Depth Claim Verifications

### ID: ID-01 — Intermittent-Demand Evaluation
*   **Claim:** The paper studies the accuracy and bias of forecasting methods designed for intermittent demand, including Croston-type estimates.
*   **Verdict:** **Supported**.
*   **Source and Exact Page:** Syntetos and Boylan (2005), *International Journal of Forecasting*, Vol. 21, No. 2, pp. 303, 304.
*   **Short Supporting Quote:** 
    > "In this paper, four forecasting methods, Simple Moving Average (SMA, 13 periods), Single Exponential Smoothing (SES), Croston’s method, and a new method (based on Croston’s approach) recently developed by the authors, are compared on 3000 real intermittent demand data series from the automotive industry." (p. 303, Abstract)
*   **Safest Thesis-Ready Wording:**
    > "Syntetos and Boylan (2005, p. 303) conduct a large-scale empirical evaluation comparing the accuracy and bias of standard estimators—Single Exponential Smoothing (SES), a 13-period Simple Moving Average (SMA), Croston’s method, and their newly proposed bias-corrected alternative—using 3,000 monthly spare parts time series retrieved from the automotive industry."

---

### ID: ID-02 — The Syntetos–Boylan Approximation (SBA)
*   **Claim:** The authors derive or evaluate a bias correction to Croston’s intermittent-demand estimator.
*   **Verdict:** **Supported**.
*   **Source and Exact Page:** Syntetos and Boylan (2005), p. 304.
*   **Short Supporting Quote:** 
    > "Syntetos and Boylan (2001) showed that Croston’s estimator is biased... The magnitude of the error depends on the smoothing constant value being used. We show in Appendix A that the bias associated with Croston’s method, in practice, can be approximated... by a [factor of] $1 - lpha/2$." (p. 304)
    > "The new estimator of mean demand is as follows:
    $$Y'_t = \left(1 - rac{lpha}{2}ight) rac{z'_t}{p'_t} \quad 	ext{(Equation 3)}$$
    where $lpha$ is the smoothing constant value used for updating the interdemand intervals." (p. 304)
*   **Safest Thesis-Ready Wording:**
    > "Because Croston's original formulation exhibits an inherent upward bias (as it divides the smoothed demand size by the smoothed interdemand interval, violating Jensen's inequality), Syntetos and Boylan (2005, p. 304) derive a multiplicative bias-correction factor of $(1 - lpha/2)$. This formulation, termed the Syntetos–Boylan Approximation (SBA), is defined as:
    $$Y'_t = \left(1 - rac{lpha}{2}ight) rac{z'_t}{p'_t} \quad 	ext{(Equation 3)}$$
    where $z'_t$ and $p'_t$ represent the exponentially smoothed demand sizes and intervals, and $lpha$ is the smoothing parameter."

---

### ID: ID-03 — 2D Demand Categorization Scheme
*   **Claim:** Demand patterns can be categorized using dimensions related to the interval between nonzero demands and variation in nonzero demand sizes.
*   **Verdict:** **Supported**.
*   **Source and Exact Page:** Syntetos, Boylan, and Croston (2005), *Journal of the Operational Research Society*, Vol. 56, No. 5, pp. 495, 499 (Table 1, Figure 3).
*   **Short Supporting Quote:** 
    > "Our categorization scheme is as indicated below (Figure 3). The corresponding demand categories are as follows: area 1—erratic (but not very intermittent); area 2—lumpy; area 3—smooth; area 4—intermittent (but not very erratic)." (p. 499)
    > "The categorization rules proposed are expressed in terms of the average inter-demand interval [$p = 1.32$] and the squared coefficient of variation of demand sizes [$CV^2 = 0.49$]." (p. 495, Abstract)
*   **Safest Thesis-Ready Wording:**
    > "Syntetos, Boylan, and Croston (2005, pp. 495, 499) establish a non-arbitrary demand categorization scheme using the average inter-demand interval ($p$) and the squared coefficient of variation of demand sizes ($CV^2$). Utilizing a standard smoothing parameter of $lpha=0.15$ and a lead time of $L=1$, they derive exact mathematical thresholds of $p = 1.32$ (review periods) and $CV^2 = 0.49$, partitioning demand into four quadrants:
    1.  **Smooth:** $p \le 1.32$ and $CV^2 \le 0.49$
    2.  **Intermittent:** $p > 1.32$ and $CV^2 \le 0.49$
    3.  **Erratic:** $p \le 1.32$ and $CV^2 > 0.49$
    4.  **Lumpy:** $p > 1.32$ and $CV^2 > 0.49$"

---

### ID: ID-04 & ID-05 — Data Exclusion vs. Specialized Estimators
*   **Claim:** Syntetos and Boylan recommend excluding highly intermittent series from forecasting datasets.
*   **Verdict:** **Contradicted** (for ID-04); **Supported** (for ID-05).
*   **Analysis & Methodology Correction:** 
    *   **The Contradiction:** Syntetos and Boylan (2005) do *not* advocate for the exclusion of highly intermittent or lumpy series. Their entire academic contribution centers on establishing robust, mathematically sound methods (such as SBA) specifically to *improve* the forecasting accuracy of these erratic series rather than discarding them.
    *   **The Solution:** If your ensembling pipeline (LightGBM, Ridge, Prophet) cannot handle high zero-inflation (leading to convergence or scale failures), you must justify any exclusion threshold as a **thesis-specific empirical design decision** rather than attributing it to Syntetos and Boylan.
*   **Safest Thesis-Ready Wording:**
    > "Highly intermittent spare-parts or brand-level series require specialized forecasting estimators (such as the Syntetos–Boylan Approximation) and modified evaluation metrics to remain mathematically stable under zero-inflation (Syntetos & Boylan, 2005, p. 304). Consequently, the decision to exclude highly intermittent brand series in this thesis is a practical empirical design choice tailored to the structural constraints of our ensembling models, rather than a universal data-cleaning rule established by Syntetos and Boylan."

---

## 3. Correct Bibliographic Entries

Ensure these entries are formatted exactly as follows in your bibliography:

*   **SBA Paper:** Syntetos, A. A., & Boylan, J. E. (2005). The accuracy of intermittent demand estimates. *International Journal of Forecasting*, 21(2), 303–314.
*   **Categorization Paper:** Syntetos, A. A., Boylan, J. E., & Croston, J. D. (2005). On the categorization of demand patterns. *Journal of the Operational Research Society*, 56(5), 495–503.
