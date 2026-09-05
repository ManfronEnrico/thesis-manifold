---
pid: P0046
created: 2026-09-05 21:10:00
updated: 2026-09-05 21:10:00
status: in_progress
focus_detail: "Decide whether to add a holiday-calendar exogenous feature before the funded SRQ4 runs. This is a scope decision with a deadline, not a prose fix -- it changes feature engineering, hence training, hence every reported number. Read F1 first: the project already removed a fake holiday feature on 2026-08-18 for the reason that matters."
---

# P0046 — Exogenous enrichment: decide, then either build or withdraw

## Why this plan exists, and why it is not part of P0043

The Word review raises the same objection in four chapters: the thesis **claims**
exogenous enrichment it does not **have**.

| where | thread | says |
|---|---|---|
| Ch1 §1.1 | 15, 18, 20 | "We didnt really add any enrichment (e.g. Holiday Calendar)" / "This premise is not supported" |
| Ch2 §2.1 | 66, 69 | "another indication that we maybe really should think about enriching" / "Again an argument for exogenous features" |
| Ch3 Limitations | 127 | "FEATURE: ... adding an external holiday calendar api to enrich, following cited paper best practices" |
| Ch4 Feature Eng. | 177 | "VERIFY & UPDATE: As we are thinking about including exogenous features (holiday calendar)" |
| Ch5 §5.3 | 207 | "MISSING: the holiday api enrichment" |

P0043 can close threads by editing prose. **These five cannot be closed that way**, because
the honest fix has two branches and only one of them is writing:

- **Withdraw** the claim -> a prose fix, and P0043 can do it
- **Deliver** the enrichment -> new feature -> re-engineer features -> retrain -> re-benchmark
  -> every WMAPE in Ch6, Ch8, Ch9 and Ch10 changes

The second branch touches SRQ1 results and the funded SRQ4 runs. That is why it is here.

## The decision has a deadline

P0042 blocks 1-3 are ~111 runs at ~$40 of API credit. **If enrichment lands after those
runs, they are spent against a feature set the thesis no longer uses.** The decision must be
made *before* the credit is spent, not after.

This is the whole reason the plan exists now rather than during the writing pass.

## Options

### Option A — Withdraw the claim (cheapest, defensible, no new results)

Narrow every enrichment claim to what the pipeline actually has: **promotional and calendar
features**. `promo_intensity` genuinely is exogenous (a promotion is a decision external to
the demand series), as is distribution coverage. Month, quarter and `peak_month` are
calendar-derived.

- Cost: prose only. No retraining, no new numbers.
- The M4/M5 "explanatory variables are the open frontier" quotation survives **only** if the
  thesis stops claiming to take up that direction wholesale (Ch1 OPEN REWRITE NOTES item 2).
- Ch10 gains a future-work item that is now specific rather than generic.

### Option B — Add a Danish holiday calendar feature

- New input: Danish public holidays (and plausibly school holidays, which move with them).
  At monthly grain the constructible forms are a **count of public-holiday days per month**
  and a **trading-day count**, not Prophet-style holiday windows (F2).
- Cost: feature engineering + full retrain + re-benchmark + regenerate every affected table
  and figure, **before** the funded runs.
- Risk: reporting only a favourable result. Otherwise the risk is schedule, not validity.

### Option C — Add it as a measured negative result

Build the feature, benchmark with and without, and **report the delta whatever it is**.

- Turns "we did not enrich" into "we enriched and measured what it bought", which answers
  the reviewer objection **and** the M4/M5 framing in one move.
- If the delta is ~0 at monthly grain, that is a publishable finding, not a failure — and it
  is exactly what F1 predicts.
- Costs the same as B, plus the writing. But it is the only option that converts the
  weakness into a contribution.

## Recommendation — Option C, and DECIDED: it runs before the experiments

**Brian, 2026-09-05: enrichment goes in before the funded runs finish.** The deadline
argument is the reason, not an obstacle to work around — spending ~$40 of credit against a
feature set the thesis then abandons is the outcome to avoid.

Option C (build it, report the delta whatever it is) rather than B: the delta is genuinely
unknown (F1 as corrected — no real calendar has ever been tested here), so committing in
advance to reporting it either way is what keeps the result honest. A null result at monthly
grain is publishable and answers the reviewer objection; a positive result improves the
models. Both are usable; only "build it and mention it if it helps" is not.

Option A (withdraw) stays on file as the fallback if task 2's sizing shows the retrain
cannot fit before the funded runs.

**What this changes about sequencing:** enrichment is now upstream of P0042 blocks 1-3, not
parallel to them. Task 2 sizes it; if the size is compatible, tasks 5-7 run first and the
funded runs use the final feature set.

## Tasks

| # | task | blocked by | status |
|---|---|---|---|
| 1 | Establish the ground truth: what IS exogenous in the live feature set today | — | complete |
| 2 | Size Option C honestly — hours to feature, retrain, re-benchmark, regenerate tables | 1 | pending |
| 3 | ~~DECISION GATE~~ **DECIDED 2026-09-05: Option C, before the funded runs.** Task 2 now only confirms it fits the schedule; if it does not, fall back to A | 2 | complete |
| 9 | Record the corrected F1/F2 reasoning in `writing-notes/` so the thesis never argues the overreaching version | — | pending |
| 4 | If A: narrow the claims in ch1/ch2/ch3/ch4/ch5 drafts, hand the prose to P0043 | 3 | pending |
| 5 | If B/C: add the holiday feature to engineer_features.py behind a flag, defaults off | 3 | pending |
| 6 | If B/C: re-run SRQ1 benchmark with and without; record the delta per category | 5 | pending |
| 7 | If B/C: regenerate every affected table/figure; update the staleness audit | 6 | pending |
| 8 | Close the five Word threads with the outcome, whichever branch ran | 4 or 7 | pending |

## Non-goals

- **Weather and macro data.** The comments name a holiday calendar specifically. Do not
  expand the scope to every exogenous source that could exist.
- **Re-opening the grain decision.** Brand x month is locked (DEC-GRAIN); a holiday feature
  at monthly grain is the question here, not whether the grain should change to expose it.
- **Retro-fitting the claim.** If Option A is chosen, the claim is withdrawn, not softened
  into something that still implies enrichment.
- **Arguing from the 2026-08-18 rename.** It was a naming fix on a mislabelled peak-month
  rule, not a negative result about holiday calendars (F1, corrected). Do not cite it as
  evidence either way.

## Related

- `plans/P0043_.../` — the writing-side plan; the five threads live in its corpus (F47)
- `plans/P0042_.../` — the funded runs whose schedule sets this plan's deadline
- `plans/P0045_.../` — draft bullets; ch1/ch2/ch5 already carry the narrowed claim as Open
- `02_thesis_data/_02_preprocessing/nielsen/_shared_modules/step_3_derive_params.py` — the
  2026-08-18 `holiday_months` -> `peak_months` rename, and why it happened (F1)
