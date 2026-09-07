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

## F10 — The ablation result: real signal, category-dependent, mostly not helpful

Measured 2026-09-06, `srq1_holiday_ablation.py`, untuned benchmark, 4 categories
x 3 models. Delta = with − without, negative means enrichment helped.

| category | LightGBM | XGBoost | Ridge |
|---|---:|---:|---:|
| **RTD** | **−1.67** | **−2.88** | **−10.15** |
| energidrikke | −0.41 | +1.75 | +0.79 |
| danskvand | +0.11 | +1.57 | +0.32 |
| **CSD** | +1.55 | +2.17 | +0.76 |

**8 of 12 combinations got worse.** Helps decisively in RTD, hurts in CSD.

Two follow-ups, both measured rather than assumed:

- **Not a dimensionality problem.** `n_holidays` alone: mean delta **+0.00pp**,
  worse in the same 8 of 12. Dropping to one feature does not rescue it, so the
  three-feature count is not the cause.
- **RTD's gain is not seed luck.** LightGBM improves on all 5 seeds tested
  (−1.19 .. −2.10pp).

**The SHAP redistribution test came back negative** — i.e. the features are NOT
merely re-encoding month-of-year:

| category | `month` before→after | `peak_month` before→after | holiday gained |
|---|---|---|---:|
| CSD | 2.17 → 1.69 | 1.41 → 1.38 | 2.37 |
| RTD | 2.22 → 1.78 | 2.58 → 1.96 | 2.31 |
| danskvand | 1.06 → 0.90 | 3.70 → 3.57 | 1.21 |
| energidrikke | 1.47 → **2.01** | 0.54 → **0.69** | 1.88 |

Holiday features take 1.2–2.4% attribution while the existing calendar features
lose only 0.2–1.1%. So they carry information `month` structurally cannot hold
(F7's argument, now measured) — **and the models still generalise worse with
them in 3 of 4 categories.** Attribution is not accuracy. Report both.

## F11 — The pipeline had no collinearity check, and the feature set is severely collinear

Brian asked whether the pipeline does proper feature-importance and correlation
analysis and keeps only information-adding components. **It did not.** Verified
by search, not assumption:

| capability | status before 2026-09-06 |
|---|---|
| Correlation on the **model** feature set | **absent** |
| VIF / multicollinearity | **absent** |
| Feature selection (RFE, SelectKBest, permutation) | **absent** |
| Correlation heatmaps on **raw measures** | present, `step_2_eda_descriptive.py` — never sees engineered features |
| SHAP | present, post-hoc, consumed by nothing |

`srq1_benchmark.FEATURES` was a hand-maintained list. Its two documented
removals (`weighted_distribution`, `holiday_months`) were justified in **code
comments** from ad-hoc fits — honest, but not a procedure, and never applied to
the 13 features that remained.

`srq1_feature_diagnostics.py` now measures it. First run:

| category | features | VIF = ∞ | VIF > 10 | VIF ≤ 5 |
|---|---:|---:|---:|---:|
| CSD | 16 | 3 | 13 | **2** |
| danskvand | 15 | 3 | 13 | **1** |
| energidrikke | 16 | 3 | 12 | **3** |
| RTD | 15 | 3 | 12 | **2** |

Only `peak_month`, `lag_13` and `promo_intensity` are ever below VIF 5.
`rolling_mean_4` reaches **227–256**. Every category has one 6–7 member
lag/rolling redundancy cluster at |Spearman| ≥ 0.95, plus `month + quarter`
(quarter is derivable from month).

The three ∞ values are the holiday features: `non_holiday_days = days_in_month −
n_holidays` is an exact linear dependency, introduced by this plan.

## F12 — Two of my own claims were wrong, both corrected by measurement

Recorded because both were stated to Brian as findings before being tested.

**(a) "The exact dependency explains RTD's Ridge instability."** It does not.
Dropping `non_holiday_days` changes test WMAPE by **< 0.01pp in all 8**
category × feature-set cells. `StandardScaler` + Ridge's L2 penalty already
absorbs rank deficiency. VIF correctly reports the dependency; the dependency is
not what drives the error. **Report the VIF; do not claim it explains accuracy.**

**(b) "RTD Ridge should be ~43.6% instead of 57.3% — a 13.7pp error."** That
43.6% came from an alpha sweep read **on the test set**, which is the leakage the
protocol exists to prevent. Selected honestly on validation, RTD picks α=0.01 and
scores **47.3%**. Proper alpha selection is worth ~0.3pp on average, not 13.7pp.

`srq1_benchmark.py` does hard-code `alpha=1.0`, and selecting on validation is
still the correct fix — but it is a small correction, and
`srq1_benchmark_tuned.py` already tunes properly. The untuned benchmark is a
deliberate baseline, not a defect.

## F13 — Naive VIF-based feature reduction makes the models worse

The obvious next step after F11 — drop the redundant cluster members — was
implemented, measured, and **rejected**:

| feature set | mean test WMAPE |
|---|---:|
| current, no holiday | 26.44 |
| current + holiday | 25.93 |
| **VIF-reduced (16 → 9)** | **28.82** |

Worse in almost every cell. **Collinearity is a linear-model pathology.** Ridge
cannot apportion credit between `lag_1..lag_4` and `rolling_mean_4`; a
gradient-boosted tree splits on whichever correlated feature is locally most
useful and loses real information when the rest are removed. One reduction rule
cannot serve both families.

This is the finding that answers "did we keep only information-adding
components" properly: **the correlated lags ARE information-adding for the tree
models, and the measurement proves it.** An unvalidated reduction rule would have
degraded every reported number while looking like methodological rigour.

`propose_reduced_set()` therefore emits a diagnostic for the linear track only
and is applied nowhere automatically.

## F14 — Ridge CV: the hard-coded alpha was fine, and I over-claimed twice

Brian asked why Ridge was not cross-validated. It was not — nothing in
`02_thesis_modelling/` used `TimeSeriesSplit`, `KFold` or `cross_val_*`,
including `srq1_benchmark_cv.py` despite its name. `srq1_ridge_cv.py` now does
**rolling-origin CV** (training always precedes validation; ordinary k-fold is
invalid on a time series because shuffling trains on the future).

**Result: proper CV made Ridge slightly WORSE.**

| category | alpha=1 (hard-coded) | CV-selected | change |
|---|---:|---:|---:|
| CSD | 21.06 | 21.25 | −0.20 |
| danskvand | 21.49 | 21.70 | −0.22 |
| energidrikke | 20.24 | 20.31 | −0.07 |
| RTD | 55.64 | 56.30 | −0.66 |

Mean **−0.19pp**. Three categories select the grid's lower edge, i.e. they want
essentially *no* regularisation. Widening the grid to 1e-8 changed test WMAPE by
< 0.01pp, and the CV curve is flat: the spread between the best alpha and
alpha=1 is 0.00–0.44pp. **Alpha barely matters on this data.**

So the hard-coded `alpha=1.0` was not a live defect. It was an unjustified
choice that happened to be near-optimal — worth fixing for method, not for
accuracy. That is now measurable rather than assumed, which is the actual gain.

**Two over-claims of mine, both corrected by this run** (the second compounds
F12b):

- I said the hard-coded alpha was "a live benchmark defect". It is not; the
  correction is worth 0.19pp in the *wrong* direction.
- I said RTD should be "43.6% instead of 57.3%". That figure came from reading an
  alpha sweep **on the test set**. Under honest rolling-origin selection RTD is
  **56.3%**, slightly worse than the baseline.

Both errors shared one cause: quoting a number from an exploratory sweep before
subjecting it to the protocol. A sweep is a hypothesis, not a result.

**One thing the properly-tuned run does confirm:** with both arms CV-tuned, the
holiday effect on Ridge is negative (helpful) in 3 of 4 categories — RTD −8.97,
energidrikke −1.21, danskvand −0.74, CSD +0.95. Ridge likes the features more
than the tree models do, which is consistent with the trees already extracting
that seasonality from the lag structure.

## F15 — A citation was invented, and there is now a register for that

`Hair et al. (2019) Multivariate Data Analysis` was written into
`srq1_feature_diagnostics.py` as the source of the VIF > 10 threshold. It was
recalled **from memory**, is **not in the project's 86-entry Zotero library**,
and was never read — but the comment read as verified.

This is the `holiday_months` defect (a name asserting a cause the computation
never established) transposed into the literature layer, where it is worse,
because a reader cannot check it against the data.

Actions taken:

- Attribution removed. The 5/10 bands remain as **reporting bands only**;
  nothing in the pipeline drops a feature because of them.
- `06_thesis_writing/writing-notes/unverified-claims-to-check.md` created as a
  standing register. Four open items: the VIF bands, the Spearman 0.95 cluster
  threshold (never had a source either), the Lukkeloven 2012 date, and the
  Store Bededag bill number.
- What the library **does** support is cited instead: Hastie, Tibshirani &
  Friedman, *Elements of Statistical Learning*, "Linear Methods for Regression"
  (Zotero key LR3KF2SX) — collinear predictors give high-variance least-squares
  coefficients, which is what ridge shrinkage addresses. That motivates the
  diagnostic without pretending to source the numbers.

**Standing rule: if a source is not in the library, it is not a source.** Write
the claim into the register and let Brian decide.

## F16 — THE THESIS NUMBERS. Tuning changes the answer, and the untuned run was misleading

`srq1_holiday_ablation_tuned.py`, 2026-09-06. Separate Optuna study per arm per
model (30 trials, tuned on validation, refit on train+val, test scored once);
Ridge alpha by rolling-origin CV. **These supersede F10 entirely.**

| category | LightGBM | XGBoost | Ridge |
|---|---:|---:|---:|
| **danskvand** | **−1.12** | **−2.41** | **−0.74** |
| **RTD** | **−3.00** | +3.44 | **−8.97** |
| energidrikke | +0.83 | +0.19 | **−1.21** |
| CSD | +0.47 | +0.95 | +2.56 |

**Helped in 6 of 12, mean −0.75pp** — against 4 of 12 and −0.51pp untuned.

### Why the untuned result could not be trusted

Tuning improved the **baseline itself** enormously in the categories where the
fixed configuration was worst:

| category | model | untuned baseline | tuned baseline | gain |
|---|---|---:|---:|---:|
| danskvand | XGBoost | 32.56 | 19.96 | **12.60** |
| danskvand | LightGBM | 33.12 | 21.09 | **12.03** |
| energidrikke | LightGBM | 17.82 | 14.27 | 3.54 |
| CSD | LightGBM | 18.48 | 15.59 | 2.89 |

Danskvand's fixed-capacity trees were mis-specified by ~12pp. Measuring a
*feature* change on a model that mis-specified is measuring noise: danskvand
flips from +0.11/+1.57 (harmful) to −1.12/−2.41 (helpful) once the model can
actually fit. **The frozen-capacity confound was real and it was large.**

This is the single most important methodological lesson of the session: an
ablation is only interpretable against a properly specified model, and
`srq1_benchmark.py` is a fixed-configuration baseline, not the reported track.

### What the result now says

- **danskvand: helps on all three models.** The only unambiguous category.
- **RTD: helps on 2 of 3, strongly** (−3.00, −8.97), hurts on XGBoost (+3.44).
  The 6.32pp swing between untuned and tuned XGBoost here is the largest
  instability in the table and is worth a caveat: RTD has the fewest usable
  brands and the widest error bars of the four categories.
- **CSD: hurts on all three**, consistently across both runs. The most stable
  negative in the study.
- **energidrikke: essentially null** on trees, helps Ridge.

Ridge benefits in 3 of 4 categories, trees in 3 of 8 model-category cells. That
split is itself a finding, and it is consistent with F13: the trees already
extract this seasonality from the correlated lag structure, so an explicit
calendar adds least where the lags are most informative.

### Reporting rule

Report the full 12-cell table. **The mean is not the result** — it averages over
model families that respond differently, which is the finding. Any single
headline number misrepresents the study.

## F17 — My analysis scripts wrote to the wrong place, and the appendix conventions have a trap

Two defects found while doing task 7, both worth recording because both are the
kind that survive review by looking fine.

**(a) Output placement.** All four scripts I added this session
(`srq1_holiday_ablation`, `_tuned`, `srq1_feature_diagnostics`, `srq1_ridge_cv`)
resolved output to `THESIS_RESULTS_SRQ1_DIR` and dropped **12 loose CSVs at the
top of the results directory** — which already had `figures/ models/ tables/`
subfolders and 33 files correctly filed in them. `PATHS.get_srq_tables_dir(1)`
existed the whole time.

That is precisely the sprawl P0046 Phase 3b is open to fix, created by the
scripts written to fix a different methodology gap. Corrected: all four repointed
to `get_srq_tables_dir(1)`, all 12 files moved, zero loose files remain.

**Lesson: check the destination's existing shape before writing into it.** A
valid `PATHS` constant is not evidence that it is the *right* constant.

**(b) `to_markdown` silently drops significant digits.** Formatting a column to
`"22.20"` and `"-3.00"` is not enough — tabulate re-parses numeric-looking
strings and renders `22.2` and `-3`, dropping a digit from a results table.
`astype(object)` does **not** prevent it; only `disable_numparse=True` does.

In a thesis appendix this matters: trailing zeros state the precision the
measurement was reported at. Every table generator that formats numbers as
strings needs this flag, which likely includes `export_appendix.py` — worth
checking as part of P0046 Phase 7's style pass.

---

## F18 — XGBoost was never reproducible: `n_jobs=-1` made every XGBoost number machine-dependent

**Found while doing:** task 19, which assumed SRQ1 artefacts were stale *because of the
feature-set change*. That premise was false, and testing it exposed a real defect.

### The premise was wrong

Every SRQ1 generator pins a literal 13-name `FEATURES` list that does not contain
`days_in_month`, `n_holidays` or `non_holiday_days`. `available_features()` intersects
*wanted* with *present*, so extra matrix columns are invisible to it. Verified: all four
matrices now carry the three holiday columns with **zero nulls**, and
`set(FEATURES) & set(HOLIDAY_FEATURES) == set()`.

So no existing generator was stale from enrichment. Re-running `srq1_benchmark.py`
should have been a no-op.

### It was not a no-op

Re-running changed **XGBoost rows only** — 4 of 4 — while Ridge, LightGBM and
SeasonalNaive were byte-identical in all four categories (0 of 12 changed).

Isolated with everything else held constant (danskvand, seed 42, same data,
same hyperparameters), varying *only* the thread count:

| n_jobs | WMAPE |
|---|---|
| 1 | 34.648708 (repeatable) |
| 2 | 34.946778 |
| 4 | 35.397904 |
| 8 | 37.297544 |
| -1 | 37.297544 (== 8 on this machine) |

**2.65pp of spread from thread count alone.**

**Cause.** XGBoost's histogram builder sums gradient statistics per thread and reduces
them in completion order. Floating-point addition is not associative, so a different
thread count gives a different sum, a different split, a different tree.
`random_state` fixes the subsample draw; it does **not** fix a parallel reduction order.
LightGBM is unaffected here and Ridge is a closed-form solve, which is exactly why the
drift was XGBoost-only — the signature that identified the cause.

### Why it matters

2.65pp is **larger than most of the holiday effects in table 94**. A reader on a
machine with a different core count could not reproduce the *sign* of several findings.

Two conclusions were not real:
- **`srq1_benchmark.py`: RTD's best model flips XGBoost -> LightGBM.** The old margin
  was 0.43pp — smaller than the artefact.
- **Table 94: 3 of 12 cells flip sign** (RTD XGBoost, danskvand XGBoost,
  energidrikke LightGBM). Headline moves 6/12 -> **7/12 helped**, mean
  -0.75pp -> **-1.42pp**.

### Fix

`XGB_N_JOBS = 1` for every **accuracy** call site (8 scripts), with the measured
rationale inline. `srq1_stability.py` imports it rather than redefining it.

`srq1_generate_performance_figures.py` had **no `n_jobs` at all** — not a neutral
default, since XGBoost then uses every core. Same defect, silent. Fixed.

**Deliberately NOT changed: `srq1_profiling.py`.** It measures memory and latency under
realistic multi-core execution, where `n_jobs=-1` is the thing being measured. It
already records the core count and states the machine-dependence in its output table.
That was correct handling and flattening it would have destroyed a valid measurement.

**Verified:** two consecutive full runs are now byte-identical.

### F18b — a hard-coded number in a generator outlived its data

Table 94's `note` was computed and updated itself. Its `<!-- INTERNAL REVIEW -->` block
was **typed**, and kept asserting "tree models benefit in 3 of 8 cells" (now 4 of 8) and
named "RTD XGBoost" as least-stable (now danskvand LightGBM, 3.81pp).

Both would have shipped wrong. Now derived: counts computed, and the least-stable cell
*found* by max untuned/tuned swing rather than named. This is the failure mode the
no-hard-coding rule exists to prevent, caught inside a file that already claimed
"none is typed into the generator".

### F18c — the stability table's headline is the claim most exposed to F18

`stability.md` currently concludes that LightGBM and XGBoost are **statistically
indistinguishable**, because the per-seed winner **FLIPS in all 4 of 4 categories**:

| Category | winner per seed (pre-fix) |
|---|---|
| CSD | XGB, XGB, LGBM, XGB, LGBM |
| danskvand | LGBM, LGBM, LGBM, XGB, LGBM |
| energidrikke | LGBM, LGBM, XGB, LGBM, LGBM |
| RTD | XGB, XGB, LGBM, LGBM, LGBM |

Its supporting sentence is *"the between-seed spread exceeding the between-model
difference"*.

**That spread was measured with `n_jobs=-1`.** Every XGBoost row therefore carries seed
variation **and** thread variation together. This is the one table where that
conflation attacks the conclusion rather than the digits, because quantifying
seed sensitivity is the table's entire purpose.

Pre-fix XGBoost `wmape_std`: CSD 0.587, danskvand 1.041, energidrikke 0.791, RTD 0.917.

**What to check when the re-run lands (task 21):**

1. Does XGBoost's `wmape_std` **narrow** relative to LightGBM's? LightGBM is unaffected
   by F18, so it is the control. A narrowing means part of the reported seed
   sensitivity was thread artefact.
2. Do any of the four **FLIPS** verdicts become stable? If a category stops flipping,
   the "indistinguishable" claim weakens *for that category* and the table needs
   rewording, not just renumbering.
3. Does "between-seed spread exceeds between-model difference" still hold?

**Either outcome is publishable and neither is a setback.** If the verdict survives, it
survives on clean evidence and is stronger for it. If it changes, the honest finding is
that a previously reported model-equivalence claim was partly an artefact of
non-deterministic training — which is a more interesting methods contribution than the
original claim.

Pre-fix baseline preserved at `prefix_stability_baseline/` with a README, so the
comparison can be made against the actual numbers rather than from memory.

---

## F19 — The stability verdict SURVIVES the determinism fix, with one qualification

Task 21. `srq1_stability.py` re-run under `XGB_N_JOBS = 1` (5 seeds x 2 models x
4 categories, 40 trials). Evaluated against the three F18c criteria.

### Criterion 1 — did XGBoost's seed spread narrow? **No.**

| category | model | std before | std after | change |
|---|---|---|---|---|
| CSD | XGBoost | 0.587 | 0.563 | -0.025 |
| danskvand | XGBoost | 1.041 | 1.218 | +0.177 |
| energidrikke | XGBoost | 0.791 | 0.378 | **-0.413** |
| RTD | XGBoost | 0.917 | 1.503 | +0.586 |

Mean XGBoost `wmape_std` 0.834 -> 0.915. **No systematic narrowing.** Thread noise was
not a large component of the measured seed sensitivity; seed variation genuinely
dominates, which is what the table claimed.

**A caveat on this comparison, stated because it weakens it.** LightGBM was intended as
the control (F18 does not touch it), and it is exactly unchanged in CSD and danskvand —
but it moved in energidrikke (-0.205) and RTD (-1.172), and `n_cells` differs in those
same two categories. LightGBM was verified directly as **run-to-run deterministic**
(same seed, two runs, identical best CV to 6 dp), so this is not non-determinism. The
Aug-24 baseline simply predates other changes, so it is not a clean single-variable
comparison for those two categories. Criterion 1's answer holds for CSD and danskvand
without qualification and is directional elsewhere.

### Criterion 2 — do the FLIPS verdicts survive? **Yes, 4 of 4.**

| Category | winner per seed (post-fix) | verdict |
|---|---|---|
| CSD | XGB, XGB, LGBM, LGBM, LGBM | FLIPS |
| danskvand | LGBM, LGBM, LGBM, XGB, LGBM | FLIPS |
| energidrikke | LGBM, XGB, XGB, LGBM, LGBM | FLIPS |
| RTD | XGB, LGBM, LGBM, LGBM, LGBM | FLIPS |

The per-seed winner still changes in **every** category. The individual seed orderings
differ from the pre-fix run, but the verdict does not.

### Criterion 3 — does "seed spread exceeds model difference" still hold? **In 3 of 4.**

| category | model gap | max seed sd | |
|---|---|---|---|
| CSD | 0.109 | 0.646 | seed spread wins |
| danskvand | 0.736 | 1.218 | seed spread wins |
| energidrikke | 0.418 | 1.379 | seed spread wins |
| **RTD** | **3.159** | **1.944** | **model gap wins** |

**This is the one substantive change.** On RTD the between-model gap (LightGBM 32.3 %
vs XGBoost 35.5 %) now exceeds the seed spread. RTD's winner still flips, so the models
are not cleanly separable there either — but the blanket sentence in Ch6 §6.6, "the
between-seed spread exceeding the between-model difference", is **no longer true of all
four categories** and must be qualified.

### Outcome

The headline conclusion — LightGBM and XGBoost are statistically indistinguishable on
this data, and naming a per-category winner reports one seed's outcome — **stands, and
now rests on runs where only the seed varied.** Before the fix that sentence was
literally false, because thread scheduling varied too.

**Prose consequences (task 12, block P4):**
1. §6.5.9's closing sentence and §6.6's "every input held identical" are now TRUE and can
   stay, once the protocol note (P3) records that thread count is fixed.
2. §6.6's "between-seed spread exceeding the between-model difference" needs qualifying:
   true for CSD, danskvand and energidrikke; **not** for RTD, where the gap is larger.
3. Table 16's per-seed winners must be refreshed from the new run.
4. The §6.6 cross-reference "(§6.5.7)" should read §6.5.9.

---

## F20 — The five pre-fix artefacts are efficiency measurements, not accuracy

Closing the F18 regeneration sweep required deciding whether five files predating the
determinism fix needed re-running. They do not, and the reason is uniform:

| File | Measures |
|---|---|
| `profiling.csv`, `sandbox_profiling.csv` | fit/predict wall-clock, peak RSS |
| `param_drift.csv`, `refit_vs_retune.csv`, `retune_single_cutoff.csv` | refit-vs-retune wall-clock, hyperparameter drift |

**None carries an accuracy metric.** F18 changes which tree gets built, so it moves
accuracy; it does not move timing or memory in any way these tables report. The three
retune files are LightGBM-only (`num_leaves`), and LightGBM was verified run-to-run
deterministic (same seed, two runs, identical best CV to 6 dp).

### A search error worth recording

I first concluded these three were **orphaned** — that no generator or consumer existed
anywhere in the repo. That was wrong. The `Grep` tool returned "No files found" for
`param_drift` both with a `*.py` glob and unfiltered, while a plain `grep -rln` over the
same tree found
`04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py`, which reads all three
(`table_param_drift()` plus two Efficiency metric rows).

They are live inputs to the SRQ4 appendix, not dead files. Had the "orphan" conclusion
been written into the state document unchallenged, a future session could have deleted
artefacts that a published appendix table depends on.

**Practical lesson:** when a search result is the basis for a *destructive or
structural* conclusion ("nothing uses this"), confirm the negative with a second,
differently-implemented search before acting. A false negative from one tool reads
identically to a true absence.

### Still true, and still worth flagging

No script in the repo *generates* these three files — only `export_appendix.py` consumes
them. If they ever need refreshing, the generator has to be reconstructed first. That is
recorded in `LOCKED_STATE.md` §3 so nobody assumes a re-run exists.

---

## F21 — The forecast tool was silently serving forecasts with NO track record

Found while auditing plan state for the handover: `verify_setup.py` reported READY,
all 10 checks passed, but printed two warnings:

```
! track record: neither cv_metrics.csv nor tuned_metrics.csv could be read
! track record: stat_baselines.csv unreadable
```

**Cause.** `02_SRQ2_Tool_Interface/forecast_tool.py` read all three from
`THESIS_RESULTS_SRQ1_DIR / fname` — the results ROOT. The files live in
`THESIS_RESULTS_SRQ1_DIR / "tables" / fname`. Confirmed: all three
`root=False, tables/=True`.

**This is F17a again, in a consumer.** The same defect I fixed in my own four scripts —
writing to / reading from the tier root instead of `tables/`. `get_srq_tables_dir(1)`
existed the whole time. The producer side was fixed on 2026-09-06; this consumer was not,
because nothing linked them.

### Why it mattered and why nobody saw it

Both reads sit inside `try/except`, so the tool **degraded instead of failing**: it
returned a valid payload with the `historical_*` fields simply absent.

Those fields are the thesis contribution. SRQ2's interface exists to carry
"forecast **plus** its measured reliability", and the B->C comparison in SRQ4 tests
whether that evidence changes an LLM's answer. Running the funded scenarios in this state
would have measured C **without** the very thing that makes it C — and the logs would
have looked normal.

**Fixed** to `get_srq_tables_dir(1)`, with the rationale inline. Verified after the fix:

```
historical_wmape: 16.6
historical_median_mape: 33.7
```

Present where they were previously absent. `verify_setup.py` now passes 10/10 with no
warnings.

### Two process lessons

1. **A soft-failing read is worse than a hard-failing one.** DEC-NO-FALLBACK was applied
   to the preprocessing pipeline but not here. A `try/except` around evidence loading
   turns a missing input into a silently weaker experiment.
2. **A "PASS" line and a "!" line on the same run are not the same signal.** The summary
   said READY; the warnings said the payload was incomplete. Read the warnings.

**Consequence for P0042:** this was found BEFORE the ~111 funded runs (~$40) were
spent. Had it not been, the money would have bought an invalid B->C comparison.

---

## F22 — The locked numbers are DETERMINISTIC but they are H1, not H3

Found during the P0049 handover audit, by reading plan P0048 (the parallel session).
**Independently reproduced here before accepting it.**

`engineer_features()` takes no `horizon` argument. `--horizon` is threaded through
parameter derivation, contract validation and filenames, but never reaches feature
construction: lags are `shift(lag)` at both horizons.

Verified on CSD, h1 vs h3 matrices merged on (brand, year, month):

| column | identical across h1/h3 |
|---|---|
| `sales_units` | **True** |
| `lag_1` | **True** |
| `lag_3` | **True** |
| `lag_13` | **True** |
| `rolling_mean_4` | False — but only **33 of 4,370** rows, a `min_periods` warm-up artefact |

Every lag is identical. **Both matrices are one-month-ahead tasks.**

### What this does and does not touch

It does **not** invalidate F18/F19/F20. Determinism is orthogonal: the numbers in
`LOCKED_STATE.md` are reproducible, and re-running them today reproduces them exactly.

It **does** invalidate their *label*. Published results come from the `_h3` file, so the
thesis reports **one-month accuracy while describing a three-month horizon**. That is a
validity problem, not a reproducibility one, and it is the more serious of the two.

### Consequence

`LOCKED_STATE.md` must not be read as "final thesis numbers". It is:

> **deterministic, reproducible, and correct for H1 — and mislabelled as H3.**

Brian's decision (recorded in P0048): implement both horizons and benchmark both,
including SRQ4 at 3 months. Ground truth exists — 7 held-out months with actuals.

**Expect H3 accuracy to worsen after the fix.** A three-month-ahead forecast should be
harder than a one-month one; if it were not, that would itself be evidence the fix had
not worked.

**No H1 results exist as such** — the current numbers are H1 in substance but were
produced from and filed as h3, so a clean dual-horizon table needs a full re-run of both.

### Ordering note for the funded runs

P0042's ~111 runs are **no longer simply unblocked**. The horizon question is upstream of
them: running SRQ4 against a tool whose track record is labelled H3 but measured at H1
would bake the mislabel into the scenario results. Decide the horizon fix first.
