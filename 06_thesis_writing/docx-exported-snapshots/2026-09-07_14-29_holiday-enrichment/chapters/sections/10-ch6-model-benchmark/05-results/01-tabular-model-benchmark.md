# Tabular-model benchmark

> Section of **Model Benchmark & Selection > Results > Tabular-model benchmark**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**4 comment(s) on this section** -- VERIFY, TABLE-REFERENCE, SOURCE, METACOMMENT. Detail: `comments/sections/10-ch6-model-benchmark/05-results/01-tabular-model-benchmark.md`

---

Both gradient-boosted models were tuned with Optuna (TPE, 100 trials) against an expanding-window cross-validation objective, then scored once on the untouched test split. Because WMAPE and median APE are minimised by different functionals (§6.4.1), each model was tuned **twice**  - once per objective - and both results are reported. cv_metrics.csv.
| Category | Model | CV WMAPE | Test WMAPE | Test medMAPE | n test |
|---|---|---|---|---|---|
| CSD | LightGBM | 17.0% | 14.5% | 33.2% | 665 |
| CSD | XGBoost | 16.1% | 15.2% | 31.8% | 665 |
| danskvand | LightGBM | 17.9% | 20.5% | 38.6% | 174 |
| danskvand | XGBoost | 17.1% | 20.9% | 35.8% | 174 |
| energidrikke | LightGBM | 10.6% | 16.5% | 34.7% | 308 |
| energidrikke | XGBoost | 10.6% | 13.0% | 32.3% | 308 |
| RTD | LightGBM | 27.9% | 31.8% | 38.1% | 372 |
| RTD | XGBoost | 28.0% | 36.1% | 32.8% | 372 |
**Table** **12** - Performance Overview - Tuned WMAPE adn medMAPE
**The two objectives select different models and produce different rankings.** Tuning for median APE improves that metric and degrades WMAPE, as the theory in §6.4.1 predicts: absolute-error loss is minimised by the median, while a pointwise percentage error is minimised by a lower functional. On energidrikke the effect is large - LightGBM tuned for medMAPE reaches 29.8% test WMAPE against 16.5% when tuned for WMAPE. **A single “best model” number is therefore meaningless without naming the objective it was tuned against**, which is why both are carried here.
**Validation-to-test movement is substantial and is not hidden.** energidrikke tunes to 10.6% in cross-validation and lands at 13.0–16.5% on test; RTD moves the other way on LightGBM. The gap is consistent with the selection bias documented in §6.3.5 - this protocol is not nested, so the cross-validation figure is an optimistically biased estimate of generalisation, to an unquantifiable degree (Cawley & Talbot, 2010).
