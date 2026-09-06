# P0047 — Findings

## F1 — The 2026-08-18 rename is NOT evidence against a holiday calendar

**Originally claimed the project had "already run this experiment informally and
got a negative answer". Wrong; Brian corrected it 2026-09-05.**

What happened on 2026-08-18 was a **naming fix**. `holiday_month(s)` was
computing *peak months* — months whose mean target exceeds the overall mean by
10% — and consulted no calendar (`step_3_derive_params.py:105-116`).

That is evidence the old feature was **mislabelled**, not that a real calendar
carries no signal. A derived peak-month rule and an external calendar are
different inputs; only the first was ever tested.

- A calendar can mark months the peak rule misses, precisely *because* the rule
  only fires above a 10% uplift threshold.
- Divergence between them is not automatically the calendar being wrong — it may
  be signal the threshold discards.

The seasonality observations from that comment (CSD peaks at quarter-ends,
danskvand in summer, energidrikke with no December peak) remain true and useful,
but they were produced *by the peak rule*, so they cannot adjudicate what a
calendar adds.

**What survives:** the new feature must be justified **against `peak_month`**.
The question is what a calendar adds *over* the peak rule, not whether it
correlates with sales.

**Status: no prior art. Delta unknown rather than predictable** — which
strengthens the case for measuring it.

## F2 — The Prophet/grain argument is narrower than first stated

**Also corrected 2026-09-05.** The original F2 argued a holiday calendar is
structurally a weekly/daily instrument, contradicting the thesis's own
explanation of Prophet's weakness (`export_appendix.py:571-576`):

> monthly observations do not support the weekly-seasonality and holiday-window
> components that the method is designed around

**True of holiday *windows*, not holiday *months*.** Prophet's holiday component
models a span of days around a date — genuinely inexpressible monthly. A monthly
**count** is a different construct and is expressible.

| claim | verdict |
|---|---|
| Prophet's holiday-window machinery is unusable at monthly grain | **still true**, keep it |
| ∴ a monthly holiday feature adds nothing | **does not follow**, never tested |

**Consistency requirement for the write-up:** state the window/count distinction
explicitly wherever Prophet's weakness is explained, so the thesis never argues
both "monthly data cannot support holiday effects" and "our holiday enrichment
helped".

## F3 — What is actually exogenous today

| feature | kind |
|---|---|
| `lag_*`, `rolling_*`, `log_sales_units` | endogenous |
| `month`, `quarter` | calendar-derived |
| `peak_month` | **measured** seasonality (10% uplift threshold, per category) |
| `promo_intensity` | **genuinely exogenous** (lagged 1 period after P0032 leakage fix) |
| `weighted_distribution` | **genuinely exogenous** (shelf availability) |

Accurate phrasing: **promotional and distribution signals plus calendar
features**. SHAP ranks `weighted_distribution` second behind `lag_1`, so what the
thesis *does* have carries real weight and deserves naming precisely.

Asymmetry to carry with any promo claim: promotional measures exist for CSD and
energidrikke but **not** danskvand or RTD — a property of the Danish market as
Nielsen measures it, not a defect of the extract.

## F4 — The free Nager endpoint is a different host from the one first tried

`nagerholidays.com/api/pro/v1/...` returns **HTTP 401** — the commercial tier,
key required. Empty curl output, no visible error.

The free tier is the same project elsewhere:

```
https://date.nager.at/api/v3/PublicHolidays/{year}/DK   → 200, no key
```

DK returns `global: true`, `types: ["Public"]`, `counties: null` — no regional
split to resolve. Recorded because the 401 is silent and a future maintainer
would otherwise repeat the dead end. (Brian's own BDBI exam script used the
correct host, which is what confirmed it.)

## F5 — Store Bededag is the strongest single argument for the feature

Holiday-days per year, DK: **2018–2023 = 15, 2024–2027 = 14.**

Store Bededag was abolished effective 2024. This is a **permanent structural
break landing mid-panel** — no month-of-year encoding can represent it, since
`month` is by construction identical in every year.

Discovered by running the fetch, not by reasoning. It is a better argument than
anything in the original F1/F2, and it is verifiable against Danish legislation
rather than against our own data.

## F6 — Danish retail is open at weekends; "trading days" was wrong twice

An early design carried `trading_days` = weekday count minus holidays. Brian
caught it: Danish supermarkets trade Saturdays and Sundays (Lukkeloven
liberalised 2012), and the target is Nielsen *retail scan* data.

Two independent errors in one feature:

1. **Wrong retail model** — excluding weekends encodes a US/UK office calendar
   that is false for this panel.
2. **Wrong name** — "trading day" is a finance term (exchange open days).

Final: `non_holiday_days = days_in_month - n_holidays`. Named for what it
computes, asserting nothing about opening hours — the same discipline as the
`holiday_months → peak_months` rename (F1). `selling_days` was also rejected.

**Residual limitation to state in prose:** stores are not uniformly closed on
public holidays either, so this is a proxy for trading exposure, not a
measurement of it.

## F7 — The monthly matrix is the anti-collinearity evidence

`n_holidays` is partly collinear with `month` (Christmas is always December), so
"WMAPE improved" invites the reply that month-of-year was re-encoded.

Appendix table 92 (`92_holiday_monthly_matrix`) answers it structurally:

| month | range across 2018–2027 |
|---|---|
| March | **0 – 4** |
| April | **0 – 5** |
| May | **2 – 5** |
| June | **1 – 3** |
| December | **4 – 4** (flat) |

December's flatness is the control: Christmas does not move, so `month` captures
it. March/April vary inversely as Easter moves; May drops from 2024 (F5). That
variation is not reachable from `month`, `quarter` or `peak_month`.

The empirical half is still required — the SHAP before/after comparison in task
6. This finding makes the structural case; it does not substitute for measurement.

## F8 — Step 4's DEC-NO-FALLBACK forced the architecture

The agreed guardrail chain was *refetch → cached → drop the feature*. The last
step is **incompatible with step 4**, which derives nothing and treats a missing
parameter as a hard failure — because four scripts once carried four private
opinions about `HOLIDAY_MONTHS`.

A silently-vanishing feature would reintroduce that class of bug, and worse: a
model trained without the feature would report numbers as if trained with it.

**Resolution — the fallback moved rather than being dropped:**

| stage | role |
|---|---|
| fetch | guardrail chain lives here; a human sees the failure |
| step 3 | **decides**; records `holiday_enrichment` + reason in contract v1.2 |
| step 4 | **applies**; contract says true → cache must load or hard-fail |

The pipeline still runs when the API is down (Brian's requirement), but the
unenriched run is **declared in its contract** rather than silently different.
A benchmark can therefore never report enriched numbers from an unenriched run.

Contract v1.2 is **additive** (no v1.1 field moved or re-typed), so step 4
accepts both and reads v1.1 as "no enrichment". Absence is unambiguous here
precisely because nothing was renamed — unlike v1.0, still refused.

## F9 — A narrow re-run silently shrank the manifest

`fetch_holidays.py --years 2023-2025` after a 2018–2027 pull rewrote
`years_covered` to three years while ten remained cached on disk. Step 3 trusts
the manifest, so it would have refused enrichment for a panel that was in fact
fully covered — a false negative with no error message.

Fixed by merging the on-disk cache into every manifest write: **the manifest
describes the cache, not the invocation.** A year that failed this run but is
cached from an earlier one is covered, not missing.

Found by testing the second run, not the first. Worth remembering that
cache-first code paths need their *second* invocation tested.
