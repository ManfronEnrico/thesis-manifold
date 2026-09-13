---
name: ch9-ch10-book-citations-and-the-methodology-defence
description: NOTE - The defence answer for "why was the methodology not right the first time", plus limitations citations with exact sources.
category: reference
applies-to: [ch9 discussion, ch10 limitations, defence preparation]
triggers: [ch9 prose pass, writing limitations, preparing for defence]
created: 2026_09_13-21_15
updated: 2026_09_13-21_15
source: P0055 book scan, 41/41 sections. Full catalogue in plans/P0055_*/findings.md F15
---

# Ch9 / Ch10 - the limitations citations, and the question the defence will ask

---

# Part 1 - THE DEFENCE QUESTION

**Brian raised this directly on 2026-09-13:** if the thesis admits a
methodological gap, an examiner asks *why did you not do it properly*, and
"we did not do our research in time" is not an answer.

**It is also not what happened, and the record shows it.**

## The sequence, as evidenced

| What happened | Evidence |
|---|---|
| The diagnostics WERE performed, before the matrix was built | Ch4 does log transformation with skewness evidence, ADF tests, differencing and ACF analysis, all cited |
| They were CORRECT | the repo's own ACF found lag 12 significant for **20 of 20** brands tested |
| They never reached the feature matrix | `p_diff` computed at `step_2_eda_descriptive.py:543`, ignored by the rule at `:549`. The transform verdict is computed, then a constant is returned |
| The contradiction is IN THE REPO's own metadata | the provenance field says *"the lag-12 term is retained"* while the manifests ship `13` |

## The answer to give

> The diagnostics were performed and documented. They did not propagate into
> feature construction, because **no contract existed between the analysis layer
> and the engineering layer** - the EDA wrote reports for human readers, and the
> feature builder read a hardcoded configuration. Nothing connected them, so a
> correct diagnostic and a wrong feature could coexist indefinitely without
> either being revised.

**Why this answer is strong:**

1. **It is true and line-numbered.** Not a rationalisation.
2. **It is a recognised class of defect** - provenance failure between pipeline
   stages - not ignorance of forecasting methodology.
3. **It converts the worst finding into an SRQ2 contribution.** A forecast is
   auditable only if its features carry their justification. That IS the thesis
   argument, demonstrated by its own failure case.

⚠ **Two things this answer does NOT cover - be honest about both:**

- **It does not fully excuse `lag_13`.** No contract was needed to notice that
  13 is not a multiple of 12 on monthly data. If the lag set was inherited from
  an earlier weekly-grain prototype and not re-derived when the grain became
  monthly, **say that** - it is ordinary and true. **Brian must confirm whether
  that is what happened; do not assert it otherwise.**
- **The tense depends on Branch B.** If the repairs land, the answer becomes
  "we found it and corrected it". If not, it stays "we found it". The first is
  substantially stronger, and is the best argument for doing Branch B at all.

---

# Part 2 - LIMITATIONS CITATIONS

Each of these upgrades an existing hedge into a **sourced** limitation with a
named alternative. All free.

## 1. Section 13.3 - post-hoc clipping is nowhere endorsed

> "To impose a positivity constraint, we can simply **work on the log scale**"

and for bounded intervals, the scaled logit. Critically:

> "The **bias-adjustment is automatically applied** here, and the prediction
> intervals... have the **same coverage probability**... because **quantiles are
> preserved under monotonically increasing transformations**."

**Ch5 already calls its upper bound "a departure from that preference".** The
book **confirms the departure is real** and names the principled alternative.
Upgrade the hedge to a sourced limitation.

## 2. Section 5.6 - back-transformed forecasts are MEDIANS, and medians do not add

> "the back-transformed point forecast **will not be the mean**... it will
> usually be the **median**... **But medians do not add up, whereas means do.**"

Bias-adjusted mean for lambda=0: `y_hat = exp(w_hat) * [1 + sigma^2/2]`.

**Consequence:** every served point forecast is a median, so **brand forecasts
must not be summed to a category total** without bias adjustment. P0048 already
records this as an SRQ2 item - **5.6 is the citation AND the formula.**

## 3. Section 9.9 - no model passes every residual test, and that is normal

> "it is **not possible to find a model that passes all of the residual
> tests**... In practice, we would normally use the **best model we could
> find**, even if it did not pass all of the tests."

A free limitations sentence, and it attaches directly to the non-seasonal ARIMA
admission Ch5 already makes.

## 4. Sections 11.1 / 11.3 - the panel is hierarchical and is never reconciled

The panel is exactly a mixed hierarchical/grouped structure: (category / brand)
x market. **Brand forecasts do not reconcile to a category total, and the thesis
never reconciles them.** 11.3 gives the machinery (MinT; `wls_struct` "needs no
residuals", so it suits judgmental base forecasts - i.e. the LLM scenarios).

**This is a real, named, literature-recognised gap - not an oversight to hide.**
Record as future work with the vocabulary attached.

---

# Part 3 - SRQ4 FRAMING (Ch9)

## Section 6.7 - judgmental adjustment is exactly what B -> C measures

> adjustments "should not aim to correct for a systematic pattern in the data
> thought to have been missed by the statistical model. This has been proven to
> be ineffective, as forecasters tend to **read non-existent patterns in noisy
> series**."

Effective "**only when there is significant additional information at hand**";
**large adjustments are more accurate than small ones**; small optimistic ones
actively hinder.

**An LLM handed a model forecast plus context IS doing judgmental adjustment.**
The book's condition for it helping - genuine extra information, not
pattern-reading - is precisely the distinction the B->C increment measures.

The TFC example (published forecasts persistently optimistic) is a **citable
precedent** for the over-forecasting observed in `A_llm_plain`.

## Section 6.1 - anchoring is a testable prediction, and the data already exists

> it is common to "**take the last observed value** as a reference point... may
> lead to **conservatism and undervaluing new information**"

**This predicts a measurable behaviour**: an LLM given a history may anchor on
the final observed value - naive-1 in disguise. **The 63 logged runs can test
it**, free, with no new spend. Branch B task 17.

Either result is reportable. If the plain arm anchors and the model-backed arm
does not, that is a **mechanism** for the B->C increment rather than just a size.

## Section 6.2 - the v6 schema is justified from OUTSIDE the ML literature

Five principles, each mapping onto an SRQ4 control:

| Book principle | The thesis control |
|---|---|
| set the task "clearly and concisely" | the v6 shared prompt composition |
| "implement a **systematic approach**... checklists of categories of information" | the capability-note blocks |
| "**Document and justify**... leads to accountability, which can lead to **reduced bias**" | the auditability argument for the typed tool (SRQ2) |
| "**Systematically evaluate**" | the run log |
| "**Segregate forecasters and users**" | the planner-vs-forecaster split in the scenario prompts |

Plus: "**setting targets is different from producing forecasts, and the two
should not be confused.**"

**Why this matters defensively:** it sources SRQ2/SRQ4 design choices - including
the locked v6 prompt schema - from the *forecasting* literature rather than from
ML practice. The PBS case study is "the thesis's own finding in miniature".
