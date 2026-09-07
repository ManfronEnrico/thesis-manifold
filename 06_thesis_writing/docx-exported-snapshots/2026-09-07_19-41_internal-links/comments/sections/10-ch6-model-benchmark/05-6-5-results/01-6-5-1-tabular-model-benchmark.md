# Comments -- 6.5.1 Tabular-model benchmark

> Objections on **Chapter 6 | Model Benchmark & Selection > 6.5 Results > 6.5.1 Tabular-model benchmark**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/05-6-5-results/01-6-5-1-tabular-model-benchmark.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-07 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [287](#c287) | 6.5.1 Tabular-model benchmark | VERIFY, TABLE-REFERENCE |  | VERIFY & TABLE REFERENCE... |
| [289](#c289) | 6.5.1 Tabular-model benchmark | VERIFY |  | VERIFY... |
| [290](#c290) | 6.5.1 Tabular-model benchmark | VERIFY, SOURCE, METACOMMENT |  | VERIFY, METACOMMENT, SOURCE... |
| [291](#c291) | 6.5.1 Tabular-model benchmark | VERIFY, SOURCE |  | VERIFY & SOURCE... |

---

<a id="c287"></a>

## [287] Brian Rohde -- Chapter 6 | Model Benchmark & Selection  `VERIFY * TABLE-REFERENCE`

- **Section:** Chapter 6 | Model Benchmark & Selection > 6.5 Results > 6.5.1 Tabular-model benchmark
- **Date:** 2026-09-05T15:52:00
- **On:** “Both gradient-boosted models were tuned with Optuna (TPE, 100 trials) against an expanding-window cross-validation objective, then scored once on the untouched test split. Because WMAPE and median APE are minimised by different functionals (§6.4.1), each model was tuned twice - once per objective - and both results are reported. cv_metrics.csv.”

VERIFY & TABLE REFERENCE

<a id="c289"></a>

## [289] Brian Rohde -- Chapter 6 | Model Benchmark & Selection  `VERIFY`

- **Section:** Chapter 6 | Model Benchmark & Selection > 6.5 Results > 6.5.1 Tabular-model benchmark
- **Date:** 2026-09-05T15:53:00
- **On:** “Table 12 - Performance Overview - Tuned WMAPE adn medMAPE”

VERIFY

<a id="c290"></a>

## [290] Brian Rohde -- Chapter 6 | Model Benchmark & Selection  `VERIFY * SOURCE * METACOMMENT`

- **Section:** Chapter 6 | Model Benchmark & Selection > 6.5 Results > 6.5.1 Tabular-model benchmark
- **Date:** 2026-09-05T15:54:00
- **On:** “The two objectives select different models and produce different rankings. Tuning for median APE improves that metric and degrades WMAPE, as the theory in §6.4.1 predicts: absolute-error loss is minimised by the median, while a pointwise percentage error is minimised by a lower functional. On energidrikke the effect is large - LightGBM tuned for medMAPE reaches 29.8% test WMAPE against 16.5% when tuned for WMAPE. A single “best model” number is therefore meaningless without naming the objective it was tuned against, which is why both are carried here.”

VERIFY, METACOMMENT, SOURCE

<a id="c291"></a>

## [291] Brian Rohde -- Chapter 6 | Model Benchmark & Selection  `VERIFY * SOURCE`

- **Section:** Chapter 6 | Model Benchmark & Selection > 6.5 Results > 6.5.1 Tabular-model benchmark
- **Date:** 2026-09-05T15:54:00
- **On:** “Validation-to-test movement is substantial and is not hidden. energidrikke tunes to 10.6% in cross-validation and lands at 13.0–16.5% on test; RTD moves the other way on LightGBM. The gap is consistent with the selection bias documented in §6.3.5 - this protocol is not nested, so the cross-validation figure is an optimistically biased estimate of generalisation, to an unquantifiable degree (Cawley & Talbot, 2010).”

VERIFY & SOURCE
