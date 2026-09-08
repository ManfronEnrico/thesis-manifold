# Comments -- 5.3.4 Validation scheme

> Objections on **Chapter 5 | Model Benchmark & Selection > 5.3 Experimental setup > 5.3.4 Validation scheme**
>
> Prose: `chapters/sections/09-ch5-framework-design/03-5-3-experimental-setup/04-5-3-4-validation-scheme.md`
>
> 1 comment(s) in 1 thread(s).

Extracted 2026-09-08 from `thesis_full.docx`.
1 comment(s) in 1 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [236](#c236) | 5.3.4 Validation scheme | OUTDATED |  | OUTDATED... |

---

<a id="c236"></a>

## [236] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `OUTDATED`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.3 Experimental setup > 5.3.4 Validation scheme
- **Date:** 2026-09-05T15:26:00
- **On:** “Validation schemeHyperparameters are selected by 4-fold expanding-window (rolling-origin) cross-validation, splitting on distinct periods rather than rows - the rows are brand-months, so a row-wise split would place the same month in training and validation for different brands. The training window grows forward and validation is the block immediately following it, so no model ever sees a period later than the one it predicts. The test split is untouched throughout.Rolling-origin evaluation successively advances the forecast origin instead of relying on a single split, which is vulnerable to “corruption by occurrences unique to that origin” (Tashman, 2000, p. 439). Because each fold refits from scratch, this is recalibration rather than mere updating - Tashman’s preferred procedure (p. 440).”

OUTDATED
