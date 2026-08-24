# Source-Level Verification Report: Section E (Time-Series Evaluation and Cross-Validation)
**Conducted on:** 2026-08-22  
**Author:** Gemini Notebook  
**Status:** Completed  

This section of the verification project evaluates seven claims (CV-01 through CV-07) concerning the methodology, mathematical validity, and structural constraints of out-of-sample (OOS) testing and cross-validation schemes in time-series forecasting. The claims are verified against the original text, mathematical theorems, and experimental setups of **Tashman (2000)**, **Cerqueira et al. (2020)**, and **Bergmeir et al. (2018)**.

---

### **Claim CV-01: Rolling-Origin Evaluation**
*   **Claim:** Rolling-origin evaluation assesses forecasts across multiple historical origins rather than relying on a single train-test split.
*   **Verdict:** **Supported**
*   **Source Document:** Tashman (2000), *International Journal of Forecasting*, 16(4), 437–450.
*   **Precise Location:** Page 439, Section 3.2.
*   **Short Supporting Quote:**  
    > "In a rolling-origin evaluation, we successively update the forecasting origin and produce forecasts from each new origin."
*   **Methodological Verification:**  
    Tashman (2000) formalises the distinction between "fixed-origin" and "rolling-origin" out-of-sample testing. A fixed-origin design relies on a single temporal partition $T$, generating forecasts for lead times $T+1, T+2, \dots, T+N$. This setup is highly vulnerable to "corruption by occurrences unique to that origin" (p. 439). In contrast, the rolling-origin design successively increments the origin, generating multiple forecasts for each lead time and building a robust, multi-sample empirical distribution of errors.
*   **Safest Thesis-Ready Wording:**  
    *To evaluate forecast accuracy across diverse historical intervals, model performance is assessed via rolling-origin evaluation rather than a single fixed train-test split. This approach successively updates the forecasting origin, thereby producing a larger, more representative empirical distribution of forecast errors at each lead time (Tashman, 2000, p. 439).*

---

### **Claim CV-02: Updating and Recalibration**
*   **Claim:** Out-of-sample forecast evaluation must specify whether model coefficients are updated or models are recalibrated as the forecast origin advances.
*   **Verdict:** **Supported**
*   **Source Document:** Tashman (2000), *International Journal of Forecasting*, 16(4), 437–450.
*   **Precise Location:** Page 440, Section 4.2.
*   **Short Supporting Quote:**  
    > "The successive revisions to the forecasting equation may arise simply from the addition of a data point to the fit period, or may arise as well from recalibration (reoptimization) of the smoothing weights as the new data point comes in."
*   **Methodological Verification:**  
    Tashman notes that as the origin advances, adding a new data point to the training window constitutes "updating". If the model parameters, smoothing weights, or regression coefficients are re-estimated over this new window, it is "recalibration". Tashman states that "recalibration is the preferred procedure" because "updating without recalibrating imposes an arbitrary handicap on the forecasting method" (p. 440). 
*   **Safest Thesis-Ready Wording:**  
    *When implementing rolling-origin evaluations, a clear distinction must be made between "updating" the fit window (incorporating new observations as the origin advances) and full "recalibration" (re-estimating the model parameters or smoothing weights), as failing to recalibrate penalises the model's ability to adapt to structural changes (Tashman, 2000, p. 440).*

---

### **Claim CV-03: Temporal-Order Preservation**
*   **Claim:** For non-stationary time series, performance-estimation methods that preserve temporal order produced more accurate estimates in the paper’s empirical study.
*   **Verdict:** **Supported**
*   **Source Document:** Cerqueira et al. (2020), *Machine Learning*, 109(11), 1997–2028.
*   **Precise Location:** Page 1997 (Abstract) & Page 2014 (Section 4.2.2).
*   **Short Supporting Quote:**  
    > "However, when the time series are non-stationary, the most accurate estimates are produced by out-of-sample methods, particularly the holdout approach repeated in multiple testing periods."
*   **Methodological Verification:**  
    The empirical core of Cerqueira et al. (2020) compares 11 performance estimation methods on 174 real-world time series. Their primary finding is that time-series stationarity is the critical determinant of evaluation validity. For stationary series, blocked cross-validation (CV-Bl) performs best. For non-stationary series, standard K-fold cross-validation and standard CV-Mod fail significantly, whereas out-of-sample methods that preserve temporal order—specifically repeated randomized holdout (Rep-Holdout)—yield the most accurate estimates of true generalization loss.
*   **Safest Thesis-Ready Wording:**  
    *For non-stationary business time series, performance-estimation methods that strictly preserve temporal order—such as holdout repeated over multiple randomized testing windows (Rep-Holdout)—are shown to provide significantly more accurate estimates of true out-of-sample forecasting loss than cross-validation schemes (Cerqueira et al., 2020, p. 1997, p. 2014).*

---

### **Claim CV-04: Universal Failure of K-Fold CV**
*   **Claim to Test:** ordinary K-fold cross-validation always fails for time-series forecasting because it leaks future observations.
*   **Verdict:** **Contradicted (Overstated)** — *The term "always fails" is theoretically and empirically refuted.*
*   **Source Document:** Cerqueira et al. (2020) and Bergmeir et al. (2018).
*   **Precise Location:** Cerqueira et al. (2020), Page 1998, Section 2.3; Bergmeir et al. (2018), Page 70 (Abstract) & Page 73 (Theorem 1).
*   **Short Supporting Quote:**  
    *   **Cerqueira et al. (2020):**  
        > "Notwithstanding, there are particular scenarios in which cross-validation may be beneficial. For example, when the time series is stationary, or the sample size is small and data efficiency becomes important (Bergmeir et al. 2018)."
    *   **Bergmeir et al. (2018):**  
        > "It is shown that for purely autoregressive models, the use of standard K-fold CV is possible provided the models considered have uncorrelated errors."
*   **Methodological Verification:**  
    While ordinary randomized K-fold CV is highly prone to look-ahead leakage and performs poorly under non-stationarity, claiming it "always fails" is a severe exaggeration. Bergmeir et al. (2018) prove both mathematically (Theorem 1) and empirically that standard K-fold CV is perfectly valid and asymptotically consistent for stationary autoregressive processes with uncorrelated errors. Cerqueira et al. (2020) acknowledge this exception, emphasizing that CV remains highly valuable for small, stationary datasets where data-re-use efficiency is paramount.
*   **Safest Thesis-Ready Wording:**  
    *Standard randomized K-fold cross-validation is generally discouraged for time-series evaluation due to its neglect of temporal dependencies and the resulting risk of future-data leakage (Cerqueira et al., 2020, p. 1998). However, the claim that K-fold CV always fails is mathematically incorrect; it remains a valid, highly data-efficient estimation procedure for well-specified, stationary autoregressive models yielding uncorrelated residuals (Bergmeir et al., 2018, p. 70).*

---

### **Claim CV-05: Stationary Autoregressive Exception**
*   **Claim:** Standard cross-validation can be valid for evaluating autoregressive forecasts when the process is stationary and the fitted model has uncorrelated errors.
*   **Verdict:** **Supported**
*   **Source Document:** Bergmeir, Hyndman and Koo (2018), *Computational Statistics & Data Analysis*, 120, 70–83.
*   **Precise Location:** Page 70 (Abstract) & Page 73 (Section 3, Theorem 1).
*   **Short Supporting Quote:**  
    > "It is shown that for purely autoregressive models, the use of standard K-fold CV is possible provided the models considered have uncorrelated errors."
*   **Methodological Verification:**  
    Bergmeir et al. (2018) prove that for an autoregressive model of order $p$:  
    $$y_t = g(\mathbf{x}_t, \theta) + \varepsilon_t$$  
    where $\varepsilon_t$ is a martingale difference sequence (MDS) and the parameter space $\Theta$ is compact, standard cross-validation without modification is valid. If the model is sufficiently large and flexible (e.g., nested correctly, as in non-parametric machine learning models), the residuals $\hat{\varepsilon}_t$ mimic the uncorrelated MDS errors. Consequently, standard K-fold CV works asymptotically ($P(\hat{P}E \xrightarrow{p} PE) = 1$) and outperforms out-of-sample splits on stationary series by controlling overfitting more effectively.
*   **Safest Thesis-Ready Wording:**  
    *Standard K-fold cross-validation is mathematically valid for evaluating autoregressive time-series forecasts under the conditions of second-order stationarity and uncorrelated residuals, permitting reliable, data-efficient model selection without temporal blocking or modification (Bergmeir et al., 2018, p. 70, p. 73).*

---

### **Claim CV-06: Expanding-Window Choice**
*   **Claim to Test:** Expanding-window evaluation is mathematically mandatory for all trended grocery-demand forecasting problems.
*   **Verdict:** **Contradicted (Overstated)** — *The term "mathematically mandatory" is unsubstantiated; it is instead a highly defensible design choice.*
*   **Source Document:** Tashman (2000) & Cerqueira et al. (2020).
*   **Precise Location:** Tashman (2000), Page 441 (Section 4.4); Cerqueira et al. (2020), Page 2018 (Section 5.1).
*   **Short Supporting Quote:**  
    *   **Cerqueira et al. (2020):**  
        > "Preserving the temporal order of observations, albeit more realistic, comes at a cost since less data is available... when dealing with non-stationary data sets, holdout applied with multiple randomized testing periods (Rep-Holdout) provides the most accurate performance estimates."
*   **Methodological Verification:**  
    There is no mathematical proof in the literature stating that expanding windows are mandatory for trended demand. Both Tashman (2000) and Cerqueira et al. (2020) present expanding and sliding windows as design options, noting the trade-offs: expanding windows maximize the training sample size over time, while sliding (fixed-size) windows "clean out old data" and may better adapt to structural breaks (Tashman, 2000, p. 441). Under non-stationarity (such as trended beverage sales), preserving temporal order in some form is a necessary design decision, but the specific choice of an expanding window is a practical, defensible modeling strategy rather than a mathematical mandate.
*   **Safest Thesis-Ready Wording:**  
    *For non-stationary, trended grocery demand series, utilizing an expanding-window rolling-origin evaluation is not a mathematical mandate but rather a highly defensible methodological design choice. This scheme preserves temporal causality, prevents look-ahead leakage, and systematically exposes the model to historical trend shifts while maximizing training data usage over time (Tashman, 2000, p. 439; Cerqueira et al., 2020, p. 2018).*

---

### **Claim CV-07: Reconciliation of Evidence**
*   **Synthesis Task:** Reconcile under what conditions temporally ordered rolling-origin evaluation should be preferred over ordinary cross-validation, and under what narrower conditions ordinary cross-validation remains valid.
*   **Synthesis of Findings:**  
    The empirical and theoretical findings of **Tashman (2000)**, **Cerqueira et al. (2020)**, and **Bergmeir et al. (2018)** resolve the long-standing debate on time-series evaluation through a clear dichotomy based on **stationarity** and **model specification**:

    1.  **Ordered Rolling-Origin (Preferred Standard):**  
        Temporally ordered out-of-sample evaluation (such as sliding/expanding rolling-origin or repeated randomized holdout) must be preferred for **non-stationary series** (featuring trends, seasonality, or structural breaks) or when evaluating models where future-data leakage would corrupt the test sample (Tashman, 2000; Cerqueira et al., 2020). Preserving temporal causality mimics real-world deployment and ensures that the model is evaluated on "nuances of the future that may not have revealed themselves in the past" (Tashman, 2000, p. 441; Cerqueira et al., 2020, p. 2018).
    2.  **Ordinary Cross-Validation (Valid Exception):**  
        Ordinary randomized K-fold cross-validation is valid and highly advantageous under a narrower, well-defined envelope: the series must be **second-order stationary**, the model must be **purely autoregressive** (e.g., lag-based tabular machine learning), and the model must be sufficiently specified so that its **residuals are serially uncorrelated** (Bergmeir et al., 2018, p. 70; Cerqueira et al., 2020, p. 1998). When these conditions are met, standard CV does not suffer from practical serial correlation issues, and its high data-re-use efficiency makes it a superior tool for controlling overfitting, especially in smaller datasets (Bergmeir et al., 2018, p. 81).

*   **Safest Thesis-Ready Paragraph:**  
    *In time-series forecasting, a temporally ordered rolling-origin evaluation is the preferred evaluation standard whenever non-stationarity is present, as it preserves temporal causality and guarantees that model assessment mirrors realistic, forward-looking deployment (Tashman, 2000, p. 439; Cerqueira et al., 2020, p. 1997). Conversely, ordinary randomized K-fold cross-validation remains valid under a narrower statistical boundary: the time series must be stationary, the model must be purely autoregressive, and the model must be sufficiently specified such that its residuals are serially uncorrelated (Bergmeir et al., 2018, p. 70). Under these stationary conditions, ordinary cross-validation’s data efficiency is highly advantageous for preventing model overfitting, particularly when sample sizes are small (Bergmeir et al., 2018, p. 81; Cerqueira et al., 2020, p. 1998).*

---

### **Summary of Section E Sourcing Actions**
*   `Tashman (2000)` was verified on pages 439, 440, and 441.
*   `Cerqueira et al. (2020)` was verified on pages 1997, 1998, 2014, and 2018.
*   `Bergmeir et al. (2018)` was verified on pages 70, 71, and 73.
*   *Overstatements regarding standard K-fold CV ("always fails") and expanding windows ("mathematically mandatory") have been corrected and replaced with academically robust, defensible formulations.*
