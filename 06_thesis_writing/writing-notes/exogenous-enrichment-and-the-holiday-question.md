---
name: exogenous-enrichment-and-the-holiday-question
description: RULE - What the thesis may and may not claim about exogenous enrichment, why the 2026-08-18 peak_months rename is not evidence about holiday calendars, and the precise boundary of the Prophet grain argument.
category: reference
applies-to: [ch1, ch2, ch3, ch4, ch5, ch6, ch10]
triggers: [writing an enrichment claim, citing M4/M5 explanatory variables, explaining Prophet's weakness, describing the feature set, answering a reviewer on exogenous features]
created: 2026_09_05-21_40
updated: 2026_09_05-21_40
---

# Exogenous enrichment and the holiday question

Five Word threads object that the thesis claims exogenous enrichment it does not have
(ch1 15/18/20, ch2 66/69, ch3 127, ch4 177, ch5 207 `MISSING: the holiday api enrichment`).
This note records what may be claimed today, and two arguments that are **tempting, adjacent
to the truth, and wrong** — both of which a first pass at this question produced.

## Quick reference

| claim | status |
|---|---|
| The feature set includes promotional and distribution signals | **True** — `promo_intensity`, `weighted_distribution` |
| The feature set includes calendar features | **True** — `month`, `quarter`, `peak_month` |
| The thesis "takes up" M4/M5's explanatory-variable direction | **Not as written** — see below |
| The pipeline enriches with holiday, weather or macro data | **False** — no such input exists |
| The 2026-08-18 rename showed holiday features do not help here | **False** — see Trap 1 |
| Monthly grain rules out any holiday feature | **False** — see Trap 2 |

## What is actually exogenous

| feature | kind |
|---|---|
| `lag_*`, `rolling_mean_*`, `rolling_std_4`, `zero_run_*`, `log_sales_units` | endogenous |
| `month`, `quarter` | calendar-derived |
| `peak_month` | **measured** seasonality — months exceeding the mean by 10%, derived per category |
| `promo_intensity` | **genuinely exogenous** (a promotion is a decision external to the series; lagged one period after the P0032 leakage fix) |
| `weighted_distribution` | **genuinely exogenous** (shelf availability) |

So the accurate phrase is **promotional and distribution signals plus calendar features**.
SHAP ranks `weighted_distribution` second behind `lag_1`, so the exogenous features the
thesis *does* have carry real weight and are worth naming precisely rather than vaguely.

Carry the asymmetry with any promo claim: promotional measures are reported for CSD and
energidrikke but **not** danskvand or RTD — a structural property of the Danish market as
Nielsen measures it, not a defect of the extract.

## Trap 1 — the `peak_months` rename says nothing about holiday calendars

On 2026-08-18 a feature named `holiday_month(s)` was renamed `peak_months`, because
underneath it was computing peak months and **consulting no calendar**
(`step_3_derive_params.py:105-116`). The accompanying observations are correct and useful:
CSD peaks at quarter-ends (trade loading), danskvand in summer, energidrikke has no December
peak, and January is CSD's weakest month at −26.6%.

**It is nonetheless invalid to cite this as evidence that a real holiday calendar adds
nothing.** The rename fixed a *mislabelled feature*. A derived peak-month rule and an
external holiday calendar are different inputs, and only the first has ever been tested.

Two specific reasons the inference fails:

- The peak rule only fires above a **10% uplift threshold**, so it discards by construction
  anything smaller. A calendar could mark real effects the rule filters out.
- Divergence between the two is not automatically the calendar being wrong. It may be signal
  the threshold discards.

**Do not write, in prose or in a reviewer response, that the project tested holiday features
and found no effect.** It has not. As of 2026-09-05 the question is open and P0046 exists to
answer it empirically.

## Trap 2 — the Prophet grain argument is about holiday *windows*, not holiday months

The thesis explains Prophet's weakness this way, and correctly
(`export_appendix.py:571-576`):

> monthly observations do not support the weekly-seasonality and holiday-window components
> that the method is designed around

Prophet's holiday component models a **window of days** around a date. That genuinely cannot
be expressed at monthly grain, and this sentence should stay.

**What does not follow is that no monthly holiday feature is constructible.** At least two
are:

| construct | expressible monthly? | orthogonal to `month`? |
|---|---|---|
| Prophet-style holiday window (± days around a date) | **No** | — |
| Count of public-holiday days in the month | Yes | Partly — Easter moves between March and April |
| **Trading-day count** | Yes | **Yes** — varies year to year for the same calendar month |

Trading-day count is the important row. A month dummy cannot carry it, because the same
calendar month has a different number of trading days in different years. Whatever it
contributes is information `month`, `quarter` and `peak_month` structurally cannot hold.

**Consistency requirement.** The thesis must not argue both "monthly data cannot support
holiday effects" (to explain Prophet) and "our holiday enrichment materially improved the
monthly models" (to answer the enrichment objection). The reconciliation is the distinction
above: *windows* need sub-monthly grain, *counts* do not. State it once, explicitly, wherever
Prophet's weakness is explained.

## How to write it, depending on how P0046 resolves

**If enrichment ships (P0046 Option C):** report the with/without delta per category
whatever it is. A null result at monthly grain is a finding — it says the seasonal structure
in Danish beverage demand is trade-driven rather than holiday-driven, which the peak-month
evidence already suggests and which nobody has published for this panel. Do not bury it.

**If it does not ship (Option A):** narrow every claim to promotional + distribution +
calendar. The M4/M5 "explanatory variables are the open frontier" quotation may stay **only**
if the thesis stops saying it takes up that direction. Ch10 gets a specific future-work item
naming the holiday calendar and the grain problem, not a generic "more features".

Either way, the claim that must not survive is the current one in Ch1 §1.1: *"This thesis
takes up that direction by incorporating exogenous predictors into its forecasting
substrate"* — unqualified, it reads as the M5 sense of enrichment, which is not what the
pipeline does.

## Related

- `plans/P0046_2026-09-05_21-10_exogenous-enrichment-decision/` — the decision, its findings
  (F1 and F2 are the corrected versions of the two traps above), and the build tasks
- `plans/P0043_.../` — the five Word threads, in the comment corpus (F47)
- `plans/P0045_.../` — ch1/ch2/ch5 drafts already carry the narrowed claim as an Open item
- [[sample-size-and-tool-interface-rationale]] §8 — cross-category asymmetry, including
  which categories report promotional measures
- `02_thesis_data/_02_preprocessing/nielsen/_shared_modules/step_3_derive_params.py` — the
  rename and its rationale
