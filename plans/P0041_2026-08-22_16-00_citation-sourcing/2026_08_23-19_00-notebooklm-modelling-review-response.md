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

**This was not harmless.**

| Statistic | scorable-only (as reported) | all brands (correct) |
|---|---:|---:|
| Rows used | 168 of 201 | **201** |
| LightGBM corr(delta_wmape, log volume) | +0.137 | +0.158 |
| **XGBoost corr(delta_wmape, log volume)** | **+0.252** | **−0.095** |

**The XGBoost size correlation flips sign.** 27% of brands were dropped — and they were not a
random 27%. They are the intermittent, low-volume brands, i.e. **exactly the population the
pooling question is about.** Excluding them biased the specific comparison being made.

**Fixed:** two frames, `ok` for MAPE-family statistics and `wm` (all brands) for WMAPE. The
docstring and emitted markdown now state both domains and cite Hyndman & Koehler for why.

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
