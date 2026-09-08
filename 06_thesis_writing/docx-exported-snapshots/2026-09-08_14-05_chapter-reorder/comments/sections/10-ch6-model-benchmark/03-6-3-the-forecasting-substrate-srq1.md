# Comments -- 6.3 The Forecasting Substrate (SRQ1)

> Objections on **Chapter 6 | Predictive-Extension Architecture > 6.3 The Forecasting Substrate (SRQ1)**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/03-6-3-the-forecasting-substrate-srq1.md`
>
> 3 comment(s) in 3 thread(s).

Extracted 2026-09-08 from `thesis_full.docx`.
3 comment(s) in 3 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [313](#c313) | 6.3 The Forecasting Substrate (SRQ1) | MISSING |  | MISSING: the holiday api enrichment... |
| [314](#c314) | 6.3 The Forecasting Substrate (SRQ1) | UPDATE |  | UPDATE: Not really relevant due to the low ram usage on deploy (50mb). As i said... |
| [315](#c315) | 6.3 The Forecasting Substrate (SRQ1) | VERIFY |  | VERIFY... |

---

<a id="c313"></a>

## [313] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `MISSING`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.3 The Forecasting Substrate (SRQ1)
- **Date:** 2026-09-03T17:53:00
- **On:** “). The gradient-boosted models use the exogenous predictors described in Chapter 4”

MISSING: the holiday api enrichment

<a id="c314"></a>

## [314] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `UPDATE`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.3 The Forecasting Substrate (SRQ1)
- **Date:** 2026-09-03T17:53:00
- **On:** “First, models are executed sequentially (load, run, unload) so that only one model occupies memory at a time, rather than concurrently”

UPDATE: Not really relevant due to the low ram usage on deploy (50mb). As i said before, so sequential is not necessary

<a id="c315"></a>

## [315] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `VERIFY`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.3 The Forecasting Substrate (SRQ1)
- **Date:** 2026-09-03T17:54:00
- **On:** “RSS terms: XGBoost adds about 15 MB, LightGBM about 7 MB, and Ridge under 1 MB over the runtime baseline (sequential, one model resident at a time)”

VERIFY
