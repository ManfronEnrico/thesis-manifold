---
pid: P0046
created: 2026-09-05 21:10:00
updated: 2026-09-05 21:10:00
---

# Findings — P0046

## F1 — This project already removed a fake holiday feature, for the reason that matters

**Read this before costing Option B or C.** On 2026-08-18 the pipeline renamed
`holiday_month(s)` to `peak_months`, and the code comment explaining why is the single most
relevant piece of evidence for this decision
(`_shared_modules/step_3_derive_params.py:105-116`):

> The rule consults no holiday calendar -- there is no such input anywhere in the pipeline
> -- so the old name asserted a cause the computation never established, and the evidence
> frequently contradicts it: CSD peaks at quarter-ends (trade loading), Danskvand in summer
> (weather), Energidrikke at quarter-ends with no December peak at all.

Two things follow.

**1. The seasonal structure in this panel is mostly not holidays.** Measured per category,
the peaks are trade loading at quarter-ends and weather in summer. Energidrikke has **no
December peak at all**. A Danish public-holiday calendar would mark December and Easter —
months the data says are not where these categories peak.

**2. The original defect survived review *because* of the name.** The notebook hardcoded
`{1,4,6,10,12}` and called it holiday months; it reads as a plausible holiday list, but read
as "peak months for soft drinks" it is obviously wrong, since **January is the weakest month
of the year at -26.6%**.

So the project has already run this experiment informally and got a negative answer. That
does not settle it — a *real* calendar is not the same as a hardcoded fake one, and holidays
could still carry signal the peak rule misses. But it does mean:

- Option B's upside is smaller than the Word comments assume
- Option C's "measured negative result" is the **likely** outcome, not the fallback one
- Any holiday feature must be justified **against `peak_month`**, which already captures
  measured seasonality per category and is derived rather than assumed

**The trap to avoid:** adding a holiday feature that correlates with `peak_month` where they
agree and is wrong where they disagree, then reporting the ensemble as "enriched". That
reintroduces exactly the defect the rename removed, with a real API behind it.

## F2 — Monthly grain is the structural argument against holiday features

Danish public holidays cluster in a handful of months. At **monthly** aggregation a holiday
feature is close to a coarse re-encoding of month-of-year, which `month`, `quarter` and
`peak_month` already carry. The information a holiday calendar adds over a month dummy is
mostly *within-month timing* — which week Easter falls in, how many trading days a month
has — and that is invisible at this grain.

The honest framing, whichever option is chosen: **a holiday calendar is a weekly- or
daily-grain instrument.** The literature the thesis cites for enrichment (M5, Ma et al.
2025) works at daily product-store grain. Applying its conclusion at brand x month is the
step that needs justifying, and it is the same reasoning the thesis already uses to explain
why Prophet underperforms here — monthly observations do not support the weekly-seasonality
and holiday-window components the method is designed around
(`export_appendix.py:571-576`).

**That existing argument cuts both ways, and consistency matters.** The thesis cannot
explain Prophet's weakness by "monthly data does not support holiday windows" and then claim
a holiday calendar materially improves the same monthly models. Either the grain supports
holiday effects or it does not.

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
