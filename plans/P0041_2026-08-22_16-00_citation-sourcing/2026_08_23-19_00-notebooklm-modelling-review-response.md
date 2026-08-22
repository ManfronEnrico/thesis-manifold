---
name: notebooklm-modelling-review-response
description: What the NotebookLM modelling verification (Sections A-C) confirmed, corrected and refuted, and every action taken in response — including two code defects it exposed.
category: reference
applies-to: [srq1, srq2, ch2, ch6, citation-register]
triggers: [acting on a NotebookLM verification section, citing conformal prediction, citing global-vs-local, citing a forecast-accuracy metric]
created: 2026_08_23-19_00
updated: 2026_08_23-19_00
---

# NotebookLM modelling review — response to Sections A, B, C

Three verification sections returned 2026-08-23, covering conformal prediction (CP-01..06),
global vs local forecasting (GL-01..05) and forecast-accuracy measures (FM-01..06).

**Headline: 14 of 17 claims supported, 3 refuted or corrected — and the review found things
this project did not know it had wrong, including two defects in code rather than prose.**

That is the outcome that justifies the exercise. A verification pass that only confirmed what
we already believed would have told us nothing.

---

## 1. What it caught that we had wrong

### 1.1 Two bibliographic errors — both in citations we would have printed

| Source | We had | Correct |
|---|---|---|
| Papadopoulos et al. (2002) | ECML 2002, **pp. 327–338** | LNAI 2430, Springer, **pp. 345–356** |
| Lei et al. (2018) | ***JRSS Series B*, 80(5), 1097–1121** | ***Journal of the American Statistical Association*, 113(523), 1094–1111** |

The Lei et al. error is the serious one: **wrong journal, wrong volume, wrong pages.** JRSS-B
and JASA are different journals. An examiner who tried to follow that citation would not find
the paper. This is the single most concrete value delivered by the whole review so far.

### 1.2 GL-05 — a threshold we were at risk of misattributing

The **~750–1,000 observation crossover** is one of this project's better empirical findings.
The review confirms Montero-Manso & Hyndman (2021) contains **no such threshold**, and warns
that attributing it to them would be "a misattribution and a severe factual overstatement".

**We had not yet written that misattribution** — the finding is currently recorded as our own
in `srq1-pooled-vs-per-category.md`. But the citation register listed Montero-Manso & Hyndman
against the pooling claim, and the drift from "cite for theory" to "cite for the number" is
exactly the error that happens while drafting prose.

**Locked in now**, in the register and the writing note: cite Montero-Manso & Hyndman for *why*
a crossover should exist (local models cannot estimate parameters from short series, p. 1633).
Report the *number* as ours alone.

**This makes the finding more valuable, not less.** A crossover threshold on FMCG brand-month
panels is a contribution precisely because the literature does not supply one.

### 1.3 FM-06 — the zero-exclusion practice is criticised in the literature we cite

We exclude brands with a zero actual in the test window from MAPE-based statistics, reasoning
that APE is undefined there. **The reasoning is right; the framing was not.**

Hyndman & Koehler (2006, p. 683) call excluding zero windows *"an artificial solution that is
impossible to apply in practical situations"* and recommend zero-stable metrics instead of
altering data to suit the metric. Citing them for our metric discussion while doing the thing
they criticise, without acknowledging it, is a defence-day question we would have lost.

The defensible position, now adopted: **the exclusion applies to MAPE only, because APE is
undefined there — and WMAPE, which is defined at zero, is reported as primary.** That is
Hyndman & Koehler's own recommended path, not a workaround.

---

## 2. THE CODE DEFECT: the scorability filter was applied to WMAPE, which never needed it

Acting on FM-06 exposed a genuine bug in `srq1_pooled_perbrand.py`.

**WMAPE is well-defined against zero actuals.** It is `sum|y-yhat| / sum|y|` — the sum sits in
the denominator, so a zero actual contributes a finite numerator term and zero to the
denominator. Nothing divides by zero. That is precisely why the review (FM-02, FM-04) treats
WMAPE as a zero-stable, portfolio-aggregate metric.

The script nonetheless computed **every** statistic on the scorable-only frame, including all
the `delta_wmape` analyses. It took the cost of the exclusion without needing the exclusion.

**This was not harmless.** It dropped 27% of brands, and not a random 27%: they are the
intermittent, low-volume ones, i.e. exactly the population the pooling question concerns.

**Fixed:** two frames -- `ok` for MAPE-family statistics, where APE is genuinely undefined,
and `wm` for WMAPE. The docstring and emitted markdown state both domains and cite Hyndman &
Koehler for why.

### 2.1 What the fix actually changed -- and one claim of mine it corrects

Removing the filter readmitted brands averaging **under one unit per month**. WMAPE is
arithmetically fine there, but the deltas are not: the worst is **-3179pp on a brand selling
0.33 units/month**, and **89 of 460 rows exceed 100pp with a median volume of 0.0
units/month**. Those rows are division by an almost-empty denominator, not evidence about
pooling. A **declared 1 unit/month volume floor** now applies to the WMAPE tables.

All three variants, so the sensitivity is visible rather than asserted:

| Model | Variant | n | r(delta, log vol) | win-rate small/med/large |
|---|---|---:|---:|---|
| LightGBM | A — scorable-only (**the bug**) | 168 | +0.137 | 46 / 45 / 46% |
| LightGBM | B — all brands, no floor | 201 | +0.158 | 58 / 39 / 49% |
| LightGBM | **C — floor ≥1 unit/mo (shipped)** | 192 | **+0.152** | **56 / 41 / 48%** |
| XGBoost | A — scorable-only (**the bug**) | 168 | +0.252 | 68 / 59 / 54% |
| XGBoost | B — all brands, no floor | 201 | **−0.095** | 63 / 54 / 57% |
| XGBoost | **C — floor ≥1 unit/mo (shipped)** | 192 | **+0.176** | **66 / 55 / 55%** |

**CORRECTION to an earlier claim in this document.** An intermediate version reported that the
fix "flips the sign of the XGBoost size correlation, +0.252 → −0.095", and that was written up
as the headline consequence. **It does not survive the volume floor.** The −0.095 exists only
in variant B, and is produced by the 9 sub-1-unit rows; at C the correlation is +0.176, the
same sign as before the fix.

**The right statement is the weaker one:** the correlation is **not robust to inclusion
choices at all** — it ranges from −0.095 to +0.252 across three defensible variants of the
same analysis. That is a more useful finding than any single value, and it is why the script's
verdict is judged on **win-rate monotonicity, not on r** (the same reasoning as F63/F67).

**What IS robust**, holding across all three variants and both algorithms:

- the verdict is **NULL** — win-rate is never monotone across terciles, so the F50 story
  ("pooling helps small brands, hurts large ones") does not hold as stated;
- pooling wins **most often on small brands** (56–68%) and hovers near a coin-flip on large
  ones (46–57%);
- LightGBM's **medium** tercile is the consistent anomaly (39–45%), which no size-monotone
  account explains.

The tercile *medians* did move materially and that part stands: LightGBM's small-brand median
went from **+2.0pp** (bug) to **−9.0pp** (shipped), i.e. from pooling losing to pooling
winning on the brands most affected by the exclusion.

### 2.1 The fix moved a reported result — and exposed a second, separate decision

Re-running with all 201 brands changed the small-volume tercile substantially:

| LightGBM, small tercile | Before (168 rows) | After (201 rows) |
|---|---:|---:|
| median delta (WMAPE pp) | **+2.0** | **−12.7** |
| pooling win rate | 46% | **58%** |

**The sign flips.** Pooling goes from losing by 2pp on small brands to winning by
12.7pp — which is the *direction the F50 explanation predicted all along*, and it was
invisible because the brands carrying the signal had been filtered out.

**The overall verdict is unchanged: NULL for both models.** The win-rate is still not
monotone across terciles (LightGBM 58/39/49, XGBoost 63/54/57), so the F50 story still
does not hold as stated. The evidence beneath that verdict is now correct, which
matters more than the verdict moving.

### 2.2 But the readmitted brands needed a *second*, different decision

Restoring them let in brands averaging **under one unit per month** in the test window.
WMAPE is arithmetically fine there — nothing divides by zero — but the deltas are
absurd: the worst is **−3179pp on a brand selling 0.33 units/month**, and **89 of 460
rows exceed 100pp with a median volume of 0.0 units/month.**

Those rows are not evidence about pooling. They are division by an almost-empty
denominator.

**So a volume floor of 1 unit/month now applies to the WMAPE tables, declared in the
output with its row count and effect.** This is deliberately *not* the scorability
filter returning under another name:

| | Scorability filter (removed) | Volume floor (added) |
|---|---|---|
| Reason | APE is **undefined** at zero | series too **small to inform the question** |
| Applies to | MAPE-family only | WMAPE tables |
| Basis | mathematical | judgement, stated |
| Disclosed | was not | **is, with counts** |

Hyndman & Koehler's objection (p. 683) is to **silently** excluding data so a metric
becomes computable. A declared, justified, quantified inclusion criterion is a
different thing — and the honest response to discovering the first was to make the
second explicit rather than let a 3179pp outlier set a median.

**Methodology lesson, and it is the same one as F63/F67:** the defect was in a *diagnostic*,
not in a model. A metric filter copied from where it was needed to where it was not. Verifying
a citation forced a re-read of the metric's domain, which is how it surfaced. **Source
verification found a data-analysis bug** — that is not what this exercise was for, and it is
the strongest argument for finishing it.

---

## 3. THE SECOND CODE DEFECT: we were not using Lei et al.'s Algorithm 2

CP-02 states the guarantee precisely: split conformal takes the
**`ceil((n+1)(1-alpha))/n`** empirical quantile of the calibration residuals — **not** the
`(1-alpha)` quantile. That finite-sample correction *is* what buys the distribution-free
guarantee at finite `n`.

`srq1_calibration.py` used the plain nominal quantile. The gap is small at our calibration
sizes (+0.3 to +0.8pp of quantile level), but it is the difference between "we implemented
split conformal per Lei et al. (2018)" — which is what the thesis says — and "we implemented
something conformal-flavoured". **We would have cited a theorem whose stated condition our
code did not meet.**

**Fixed.** Coverage improved at the level where it had been undercovering:

| Category | Nominal | Before (naive q) | After (finite-sample q) |
|---|---|---:|---:|
| danskvand | 90% | 85.6% | **87.4%** |
| danskvand | 80% | 70.7% | 70.7% |

`calibration.csv` now records `n_calib` and the realised `quantile_level` per row, so the
correction is auditable rather than buried.

> **Note on the other numbers in `calibration.csv`:** every category's `n_test` also changed
> (e.g. CSD 845→665, RTD 324→372) against the previously committed file. **That is feature-matrix
> drift since the file was last written, not an effect of this fix** — verified by recomputing
> danskvand both ways on the current matrix, where the quantile change alone accounts for
> +1.8pp of coverage and nothing else. The committed results file was simply stale.

### 3.1 A substantive finding this surfaced: danskvand's intervals are close to useless

Median relative interval width, danskvand at 90% nominal: **16.8×** the actual value. CSD is
3.3×, RTD 3.1×.

An interval spanning ~17× the actual technically covers, but carries no decision-relevant
information. **Coverage alone is the wrong success criterion** — an infinitely wide interval
has perfect coverage. Width must be reported beside it, and danskvand's must be reported as a
limitation rather than averaged into a "well-calibrated" claim.

---

## 4. What it confirmed — and what we can now say more strongly

### 4.1 The conformal chain is sound, and now correctly bounded

CP-01 through CP-05 all **Supported**, with exact page-level grounding. The thesis can now
state the split-conformal contract with real citations rather than the unsourced description
flagged as C3 in the register.

**Critically, CP-06 was correctly refuted.** The review tested "conformal prediction is
guaranteed to achieve target coverage on autocorrelated retail demand" and returned
**Contradicted**. It is right, and this matters because it is the claim a careless write-up
would make:

- The guarantee is **marginal**, not conditional (Lei et al., Remark 3) — an average over
  cells, not a promise about any one brand-month.
- It assumes **exchangeability**, which monthly brand demand violates.
- Barber et al. (2023) show unweighted split conformal **loses coverage** materially under
  drift, and *bound* the loss rather than removing it.

**This reframes our own coverage results in a way that strengthens them.** The measured
coverage is an *empirical result under known-violated assumptions*, not a theoretical
entitlement — which is why measuring it on a held-out test period was the right call.
energidrikke's 81.0% against a 90% nominal (pre-fix) is what the violation looks like.

**Written into `calibration.md` as a standing caveat.**

### 4.2 FM-03 resolves the WMAPE-vs-medMAPE disagreement into a *theoretical* finding

This is the most valuable confirmation in the batch. Gneiting (2011) proves:

- **Absolute-error loss → the median** of the predictive distribution (FM-01).
- **Pointwise APE loss → the `(-1)`-median**, a density reweighted by `y^-1`, which biases
  forecasts **systematically downward** (FM-03).
- **WMAPE aggregates before dividing**, so minimising it over a fixed evaluation sample is
  equivalent to minimising MAE — consistent for the **standard** median (FM-02).

**We have been reporting a WMAPE/medMAPE disagreement of up to 20pp as an empirical curiosity
across three analyses. It is a predicted consequence of optimising two different functionals.**

That also explains the dual-objective result — tuning for medMAPE costing 8–13pp of WMAPE — as
**the expected direction**, not an anomaly. Tuning for medMAPE targets the `(-1)`-median and
underforecasts; WMAPE penalises exactly that.

**Upgrade:** an empirical observation becomes a theoretically grounded methodological finding
with a named functional and a citation. This should be stated in Ch6 and referenced in Ch3.

### 4.3 MASE is the gap this exposes

FM-05 confirms Hyndman & Koehler propose MASE as *the* scale-free cross-series measure, and
FM-06 recommends it specifically for the zero-inflated case. **We report neither MASE nor any
scaled metric.** With 27% of brands carrying zero actuals, this is the metric the literature we
cite would have us use.

**Not yet actioned — flagged as a decision.** Adding MASE is cheap (a naive-forecast in-sample
MAE denominator per series) and would let every brand enter one accuracy table, including the
124 rows currently unscorable on MAPE. Recommend adding it; it is a small change that closes
the gap between the metrics we cite and the metrics we report.

### 4.4 Two qualifications worth honouring

- **GL-03** is *Supported with qualification*: the generalization bound assumes **cross-series
  independence** (Hoeffding). Brands in one category are plainly not independent. Stating this
  when claiming a pooling advantage is a rigour point, and cheap to make.
- **GL-02**'s equivalence needs global models to use **relatively longer memory** than local
  ones — a concrete design note, given our fixed lag set is identical across pooled and
  per-category runs. **Possible confound in the pooled comparison**, worth a limitation
  sentence.

---

## 5. Actions

### Done
| # | Action | Where |
|---|---|---|
| 1 | Finite-sample conformal quantile (Lei Alg. 2) + `n_calib`/`quantile_level` recorded | `srq1_calibration.py` |
| 2 | Exchangeability + marginal-coverage caveat emitted into results | `calibration.md` |
| 3 | Scorability filter removed from all WMAPE statistics; two-frame split | `srq1_pooled_perbrand.py` |
| 4 | Both scripts re-run; results regenerated | `04_thesis_results/srq1/` |

### Decisions needed from Brian
| # | Item | Recommendation |
|---|---|---|
| A | **Add MASE** as a reported metric | **Yes** — closes 4.3; cheap; lets all 460 rows into one table |
| B | Report interval **width** beside coverage; flag danskvand | **Yes** — coverage alone is not a success criterion |
| C | State the Gneiting functional argument in Ch6 | **Yes** — upgrades a curiosity to a finding |

### Register updates
- **C3 (conformal) → VERIFIED**, with corrected Lei et al. reference and the marginal /
  exchangeability qualifications attached.
- **C4 (global vs local) → VERIFIED for theory, NOT for the threshold.** Explicit
  do-not-cite-for-the-number note.
- **A6 (Hyndman & Koehler) → VERIFIED**, plus the FM-06 caveat about zero exclusion.
- **New: Gneiting (2011) → VERIFIED** for the metric-functional argument (was unsourced).

---

## 6. What this says about the remaining sections

Three sections produced two bibliographic corrections, one misattribution warning, and **two
code defects**. The hit rate is high enough that the remaining modelling sections should be
worked the same way: read the verdicts, then **check whether the implementation matches the
claim**, not just whether the prose does.

Both defects were found by asking "does our code do what the cited theorem requires?" —
a question the citation register alone does not ask.

## Related

- `2026_08_22-18_00-citation-register.md` — entries C3, C4, A6 updated
- `2026_08_22-22_00-literature-review-audit.md` — D2 (Ceran metric) still open; FM-03 sharpens it
- `05_thesis_writing/notes/srq1-tuning-and-validation-protocol.md` — dual-objective result now has a theory
