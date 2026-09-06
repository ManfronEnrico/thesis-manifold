# Pooled versus per-category training

> Section of **Model Benchmark & Selection > Results > Pooled versus per-category training**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**5 comment(s) on this section** -- VERIFY, TABLE-REFERENCE, FORMATTING, NAMING. Detail: `comments/sections/10-ch6-model-benchmark/05-results/04-pooled-versus-per-category-training.md`

---

Whether one model trained across all four categories beats four category-specific models is SRQ1’s central design question. Both arms use the same 12-feature intersection, the same tuning protocol, and are scored on identical test rows, so they differ only in which rows they were trained on. pooled_summary.md.
| Category | LightGBM pooled → per-cat | XGBoost pooled → per-cat |
|---|---|---|
| CSD | 17.5% → 16.3% (per-cat better by 1.2 pp) | 16.6% → 15.3% (per-cat by 1.3) |
| danskvand | 21.4% → 23.7% (pooling wins 2.2 pp) | 18.9% → 21.5% (pooling wins 2.5) |
| energidrikke | 12.1% → 13.7% (pooling wins 1.6) | 12.5% → 13.9% (pooling wins 1.4) |
| RTD | 35.8% → 35.1% (per-cat by 0.7) | 37.0% → 35.5% (per-cat by 1.5) |
**Table** **15** - Pooled vs Per Category Performance Differences
The answer is conditional, and the condition is data volume. Pooling wins on the two smallest panels (danskvand 174 test rows, energidrikke 308) and loses on the two largest (CSD 665, RTD 372). This is the expected transfer-learning trade-off: a small category borrows strength from the others, while a large one is diluted by them. The pattern holds for both model families, which is what makes it a finding rather than noise - though §6.5.9 shows the magnitudes here sit within seed noise, so the *direction* is the claim, not the pp values.
Per-brand, the aggregate conceals wide disagreement. Broken out by demand class (pooled_perbrand_summary.md), pooling helps between 44% and 64% of brands depending on class and model - close to a coin flip everywhere. The aggregate deltas above are small differences between two distributions that overlap heavily.
