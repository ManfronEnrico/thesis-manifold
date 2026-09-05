# Comments -- Limitations

> Objections on **Methodology > Limitations**
>
> Prose: `chapters/sections/07-ch3-methodology/07-limitations.md`
>
> 6 comment(s) in 6 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
6 comment(s) in 6 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [124](#c124) | Limitations | SOURCE |  | SOURCE: We cant just claim that. We need a source... |
| [125](#c125) | Limitations |  |  | FORMALITY: We must start to quote any model names or industry specific terminolo... |
| [126](#c126) | Limitations | SOURCE |  | SOURCE... |
| [127](#c127) | Limitations |  |  | FEATURE: In previous chapters I already highlighted that we might want to consid... |
| [128](#c128) | Limitations | OUTDATED |  | OUTDATED... |
| [129](#c129) | Limitations | INCORRECT |  | INCORRECT: Not really the case as the actual perfromance numbers are so insignif... |

---

<a id="c124"></a>

## [124] Brian Rohde -- Methodology  `SOURCE`

- **Section:** Methodology > Limitations
- **Date:** 2026-09-03T12:59:00
- **On:** “Between 37 and 42 monthly periods per category is at the lower boundary for reliable time series model estimation. “ARIMA” models generally require a minimum of 24 periods for stable parameter identification”

SOURCE: We cant just claim that. We need a source

<a id="c125"></a>

## [125] Brian Rohde -- Methodology

- **Section:** Methodology > Limitations
- **Date:** 2026-09-03T13:01:00
- **On:** “LightGBM”

FORMALITY: We must start to quote any model names or industry specific terminology. Exception to the rule are abbreviations that have been introduced in its full form once with the abbreviation in brackets, whcih from that point onwards can just be written with no quote marks.

<a id="c126"></a>

## [126] Brian Rohde -- Methodology  `SOURCE`

- **Section:** Methodology > Limitations
- **Date:** 2026-09-03T13:01:00
- **On:** “” and “XGBoost” are less sensitive to sample size constraints than classical time series models, but the restricted training window limits their ability to learn longer-cycle promotional patterns”

SOURCE

<a id="c127"></a>

## [127] Brian Rohde -- Methodology

- **Section:** Methodology > Limitations
- **Date:** 2026-09-03T13:02:00
- **On:** “incorporates lagged variables and rolling statistics that increase the effective information content per observation.”

FEATURE: In previous chapters I already highlighted that we might want to consider adding an external holiday calendar api to enrich, following cited paper best practices.

<a id="c128"></a>

## [128] Brian Rohde -- Methodology  `OUTDATED`

- **Section:** Methodology > Limitations
- **Date:** 2026-09-03T13:02:00
- **On:** “(on the order of fifty prompts)”

OUTDATED

<a id="c129"></a>

## [129] Brian Rohde -- Methodology  `INCORRECT`

- **Section:** Methodology > Limitations
- **Date:** 2026-09-03T13:04:00
- **On:** “The four-gigabyte RAM budget requires models to be executed sequentially rather than in parallel, increasing total pipeline runtime relative to a compute-unconstrained deployment. In a production setting, this latency may be acceptable for monthly batch processing but would be prohibitive for higher-frequency planning cycles. The sequential execution design is a binding architectural constraint of the thesis artefact that would need to be re-evaluated for any real-time or sub-monthly deployment.”

INCORRECT: Not really the case as the actual perfromance numbers are so insignificant (e.g. 50mb RAM) that we can run them in parallel
