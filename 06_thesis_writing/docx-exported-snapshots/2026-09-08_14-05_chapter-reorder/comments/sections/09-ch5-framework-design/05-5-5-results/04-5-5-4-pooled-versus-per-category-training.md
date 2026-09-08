# Comments -- 5.5.4 Pooled versus per-category training

> Objections on **Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.4 Pooled versus per-category training**
>
> Prose: `chapters/sections/09-ch5-framework-design/05-5-5-results/04-5-5-4-pooled-versus-per-category-training.md`
>
> 5 comment(s) in 5 thread(s).

Extracted 2026-09-08 from `thesis_full.docx`.
5 comment(s) in 5 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [273](#c273) | 5.5.4 Pooled versus per-category training | VERIFY, TABLE-REFERENCE |  | VERIFY, TABLE REFERENCE... |
| [274](#c274) | 5.5.4 Pooled versus per-category training | VERIFY, FORMATTING |  | VERIFY, FORMATTING... |
| [276](#c276) | 5.5.4 Pooled versus per-category training | NAMING |  | NAMING... |
| [277](#c277) | 5.5.4 Pooled versus per-category training | VERIFY |  | VERIFY... |
| [278](#c278) | 5.5.4 Pooled versus per-category training | VERIFY |  | VERIFY... |

---

<a id="c273"></a>

## [273] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `VERIFY * TABLE-REFERENCE`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.4 Pooled versus per-category training
- **Date:** 2026-09-05T16:11:00
- **On:** “Whether one model trained across all four categories beats four category-specific models is SRQ1’s central design question. Both arms use the same 12-feature intersection, the same tuning protocol, and are scored on identical test rows, so they differ only in which rows they were trained on. pooled_summary.md.”

VERIFY, TABLE REFERENCE

<a id="c274"></a>

## [274] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `VERIFY * FORMATTING`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.4 Pooled versus per-category training
- **Date:** 2026-09-05T16:12:00
- **On:** “RTD | 35.8% → 35.1% (per-cat by 0.7) | 37.0% → 35.5% (per-cat by 1.5)”

VERIFY, FORMATTING

<a id="c276"></a>

## [276] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `NAMING`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.4 Pooled versus per-category training
- **Date:** 2026-09-05T16:12:00
- **On:** “Table 15 - Pooled vs Per Category Performance Differences”

NAMING

<a id="c277"></a>

## [277] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `VERIFY`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.4 Pooled versus per-category training
- **Date:** 2026-09-05T16:13:00
- **On:** “The answer is conditional, and the condition is data volume. Pooling wins on the two smallest panels (danskvand 174 test rows, energidrikke 308) and loses on the two largest (CSD 665, RTD 372). This is the expected transfer-learning trade-off: a small category borrows strength from the others, while a large one is diluted by them. The pattern holds for both model families, which is what makes it a finding rather than noise - though §6.5.9 shows the magnitudes here sit within seed noise, so the direction is the claim, not the pp values.”

VERIFY

<a id="c278"></a>

## [278] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `VERIFY`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.4 Pooled versus per-category training
- **Date:** 2026-09-05T16:14:00
- **On:** “Per-brand, the aggregate conceals wide disagreement. Broken out by demand class (pooled_perbrand_summary.md), pooling helps between 44% and 64% of brands depending on class and model - close to a coin flip everywhere. The aggregate deltas above are small differences between two distributions that overlap heavily.”

VERIFY
