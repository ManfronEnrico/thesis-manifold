---
pid: P0046
created: 2026-09-05 21:10:00
updated: 2026-09-05 21:10:00
---

# Findings — P0046

## F1 — CORRECTED. The 2026-08-18 rename is NOT evidence against a real holiday calendar

**This finding originally claimed the project had "already run this experiment informally
and got a negative answer". That was wrong, and Brian corrected it on 2026-09-05.**

What actually happened on 2026-08-18 was a **naming fix**. The feature called
`holiday_month(s)` was, underneath, computing *peak months* — months whose mean target
exceeds the overall mean by 10%. It consulted no calendar. The rename made the name match
the computation (`step_3_derive_params.py:105-116`):

> The rule consults no holiday calendar -- there is no such input anywhere in the pipeline
> -- so the old name asserted a cause the computation never established.

**That is evidence the old feature was mislabelled. It is not evidence that a real holiday
calendar carries no signal.** A derived peak-month rule and an external holiday calendar are
different inputs; the first has been tested and the second never has.

The seasonality observations in that comment (CSD peaks at quarter-ends, danskvand in
summer, energidrikke with no December peak) remain true and remain useful — they describe
where the *measured* peaks fall. But they were produced by the peak rule, so they cannot
adjudicate what a holiday calendar would add. In particular:

- A holiday calendar could mark months the peak rule misses entirely, precisely *because*
  the peak rule only fires above a 10% uplift threshold.
- Divergence between the two is not automatically the holiday feature being wrong. It could
  be signal the peak rule threshold discards.

**What survives from the original finding, and it is worth keeping:**

- The new feature must be **justified against `peak_month`**, which already exists and is
  measured per category. The question to answer empirically is what a calendar adds *over*
  the peak rule, not whether it correlates with sales.
- Reporting an "enriched" ensemble without separating the two would repeat the original
  defect's *shape* — a name asserting a cause the computation never established.

**Status: no prior art exists.** The enrichment question is genuinely open. Option C's
delta is unknown rather than predictable, which strengthens the case for measuring it.

## F2 — CORRECTED. The Prophet/grain argument is narrower than first stated

**Also corrected 2026-09-05.** The original F2 argued that a holiday calendar is
structurally a weekly/daily instrument, and that claiming otherwise would contradict the
thesis's own explanation of Prophet's weakness (`export_appendix.py:571-576`):

> monthly observations do not support the weekly-seasonality and holiday-window components
> that the method is designed around

**The consistency point is real but it is about holiday *windows*, not holiday months.**
Prophet's holiday component models a window of days around a date — that genuinely cannot
be expressed at monthly grain. A monthly holiday feature (a count of public-holiday days in
the month, or trading-day count) is a different construct and is expressible.

So the honest statement is:

- Prophet's holiday-window machinery is unusable at monthly grain -> **still true**, keep it
- Therefore a monthly holiday feature adds nothing -> **does not follow**, and was never
  tested

There remains a real question about how much a monthly holiday count adds over `month` and
`quarter`, which already partition the year. But it is a question for measurement, not a
settled argument. **Trading-day count in particular is not a re-encoding of month-of-year**
— it varies year to year for the same calendar month, which is exactly the kind of variation
a month dummy cannot carry.

This nuance is going into `writing-notes/` (task 9) so the thesis does not accidentally
argue the overreaching version in prose.

## F3 — What is actually exogenous today (the ground truth for Option A)

Live features in `engineer_features.py`:

| feature | kind |
|---|---|
| `lag_1`, `lag_2`, ... | endogenous (past target) |
| `rolling_mean_*`, `rolling_std_4` | endogenous (shifted, no look-ahead) |
| `month`, `quarter` | calendar-derived |
| `peak_month` | **measured** seasonality, per category, 10% uplift threshold |
| `promo_intensity` | **genuinely exogenous** — promotion is a decision external to the series; lagged one period after the P0032 leakage fix |
| `weighted_distribution` | **genuinely exogenous** — shelf availability |
| `zero_run_*`, `log_sales_units` | endogenous transforms |

So the accurate claim is **promotional and distribution signals plus calendar features**,
not "exogenous contextual enrichment" in the M5 sense. Option A's narrowing is therefore not
a retreat to a weaker true statement — it is a correction to an accurate one. SHAP already
ranks `weighted_distribution` second behind `lag_1` (Ch9 §9.1.1), so the exogenous features
the thesis *does* have are carrying real weight and are worth naming precisely.

**Caveat on promo:** it is reported for CSD and energidrikke but not danskvand or RTD. Any
claim about promotional signal must carry that asymmetry
(-> `[[sample-size-and-tool-interface-rationale]]` §8).
