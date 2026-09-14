---
name: 2026-09-14_BRANCH_A_ch9-consolidated-defence-and-limitations-citations
description: NOTE - Chapter 9 consolidated pass. The defence answer for "why was the methodology not right the first time", four limitations citations that upgrade existing hedges into sourced limitations, and the hierarchical-reconciliation gap the thesis has never named.
category: workflow
applies-to: [ch9_discussion]
triggers: [ch9 prose pass, writing limitations, preparing for defence, book citations]
created: 2026_09_14-09_30
updated: 2026_09_14-09_30
snapshot: 2026-09-13_21-30_book-citations-pass
status: prose ready to paste, awaiting human review
---

# Chapter 9 — consolidated pass

Verified against snapshot `2026-09-13_21-30_book-citations-pass` (Ch9 at 3,197
words, unchanged from the previous snapshot), repository at `9746b44`, fetch
clean. Zotero: **89 items**.

**Notes swept:**
- `2026-09-13_21-15_BRANCH_A_book-citations-and-methodology-defence.md` — not
  applied, **superseded by this file** and archived with it.
- `the-result-hinges-on-forecasting-practice.md` — **left in place, not
  applied.** Its argument is already carried by §9.4's second limitation
  paragraph in the current text, but it also speaks to Ch5, Ch8 and Ch10, so it
  is not mine to archive from a Ch9 pass. Flagged for a sweep of its own.

**The Ch9 Branch A rewrite and its follow-up are both applied and archived.**
This note adds to a chapter that is already current, which is why every fix
below is an insertion rather than a replacement.

---

# Part 1 — the defence question

**This part is not prose.** It is an answer to have ready, and one paragraph that
may go into the chapter. Read it before the fixes.

The question, as you raised it: if the thesis admits a methodological gap, an
examiner asks *why did you not do it properly*, and "we ran out of time" is not
an answer.

**It is also not what happened, and the record shows it.**

## The sequence, as evidenced

| What happened | Evidence |
|---|---|
| The diagnostics WERE performed, before the matrix was built | Ch4 does the log transformation with skewness evidence, ADF tests, differencing and ACF analysis, all cited |
| They were CORRECT | the repo's own ACF found lag 12 significant for **20 of 20** brands tested |
| They never reached the feature matrix | `p_diff` is computed at `step_2_eda_descriptive.py:543` and ignored by the rule at `:549` — the transform verdict is computed, then a constant is returned |
| The contradiction is in the repo's own metadata | the provenance field says *"the lag-12 term is retained"* while the manifests ship `13` |

## The answer to give

> The diagnostics were performed and documented. They did not propagate into
> feature construction, because **no contract existed between the analysis layer
> and the engineering layer** — the exploratory analysis wrote reports for human
> readers, and the feature builder read a hardcoded configuration. Nothing
> connected them, so a correct diagnostic and a wrong feature could coexist
> indefinitely without either being revised.

**Why this answer is strong:**

1. **It is true and line-numbered.** Not a rationalisation.
2. **It is a recognised class of defect** — provenance failure between pipeline
   stages — rather than ignorance of forecasting methodology.
3. **It converts the worst finding into an SRQ2 contribution.** A forecast is
   auditable only if its features carry their justification. That *is* the thesis
   argument, demonstrated by its own failure case.

⚠ **Two things this answer does not cover. Be honest about both.**

- **It does not fully excuse `lag_13`.** No contract was needed to notice that 13
  is not a multiple of 12 on monthly data. If the lag set was inherited from an
  earlier weekly-grain prototype and never re-derived when the grain became
  monthly, **say that** — it is ordinary and true. **You must confirm whether
  that is what happened. I will not assert it for you.**
- **The tense is "we found it", and that is a complete answer.** The correction
  is not being made within this thesis, so the honest form is that the defect was
  identified, located and explained. **Do not imply a repair is underway.** A
  found-and-diagnosed defect reported with its mechanism is a normal and
  respectable thing for a one-cycle design-science thesis to carry; a hinted-at
  fix that no artefact shows is not.

## Where the chapter currently stands on this

**Chapter 9 does not mention `lag_13` at all.** I checked the full chapter text.
So there is no existing sentence to correct — the question is whether to
*introduce* the admission.

**My recommendation: yes, and Fix 1 below does it**, because the alternative is
that an examiner finds it in the appendix manifests and you answer unprepared.
A limitation you name yourself is a limitation you control.

**NEEDS-BRIAN** — this is a judgement call about how much to volunteer, and it
is yours.

---

# The fixes

## Fix 1 — 9.4, the annual-lag admission

### Anchor

**Section 9.4 Limitations.** The paragraph beginning *"The forecasting practice
on both sides is a property of this comparison rather than of the approaches in
general."*

It ends: *"...and the direction of the accuracy result on the median might not
survive it."*

### Action

INSERT AFTER — one new paragraph between that one and the paragraph beginning
*"The dedicated model is tuned per category..."*.

#### Replace with

> A further asymmetry lies inside the substrate rather than between the two
> sides. The lag set carries a thirteen-month term where a twelve-month term
> would capture the annual cycle the exploratory analysis identified in every
> brand it tested, so the feature intended to carry annual structure is offset by
> one month from the structure it was meant to carry. The diagnostic that
> established the annual signal was performed and reported; it did not reach the
> feature specification, which was configured separately. The gap is therefore
> one of provenance between the analytical and engineering layers rather than of
> method, and it is the same class of defect the structured interface is designed
> to prevent downstream of the model — which is what makes it worth stating
> rather than absorbing.

### Note — what this does and does not concede

**Concedes:** the lag is wrong, and why.

**Does not concede:** that the diagnostics were absent or incorrect. They were
performed, they were right, and the chapter can say so — that is the whole
difference between a methodological gap and a plumbing one.

**And it earns something.** The last clause turns the admission into evidence for
SRQ2's central claim: features must carry their justification or they drift from
it. The thesis's own worst finding becomes its best illustration.

⚠ **Ch5 §4.6 already reports the negative lag-13 autocorrelation honestly**
(*"it is retained because a mild negative annual carry is still information, but
it should not be described as a seasonal signal"*). Wait — that is **Ch4**, line
105. Check the two do not now read as contradicting each other: Ch4 says the
term is defensible as information, Ch9 says it is misplaced as annual structure.
**Both are true and they are compatible**, but a reader meeting them forty pages
apart may not see it. If you want them reconciled, the Ch4 sentence is the one to
adjust, not this one.

---

## Fix 2 — 9.4, the interval limitation names no alternative

### Anchor

**Section 9.4**, the paragraph beginning *"The intervals attain their coverage
guarantee and are too wide to act on for an individual brand."*

It ends: *"...which is the signature of a sample-size limit rather than a
modelling choice."*

### Action

INSERT AFTER — one sentence appended to that paragraph.

#### Replace with

> The bounding of point forecasts carries a related limitation of a different
> kind: the substrate constrains implausible forecasts after back-transformation,
> where the principled alternative is to impose the constraint through the
> transformation itself, which applies the bias adjustment automatically and
> preserves interval coverage (Hyndman & Athanasopoulos, 2021).

### Note

Chapter 5 §5.5.2 already names this departure and defends it on the ground that
*"the constraint is applied after back-transformation because that is where the
divergence appears"*. That is a fair operational answer and the chapter should
keep it.

What the discussion adds is that a **named principled alternative exists**. A
limitation with an alternative attached reads as a considered trade-off; the same
limitation without one reads as an omission the author did not know about.

---

## Fix 3 — 9.4, a new limitation the thesis has never named

### Anchor

**Section 9.4**, the final paragraph, beginning *"What the evaluation measures is
what each scenario communicated and how accurate it was."*

### Action

INSERT AFTER — one new paragraph at the **end** of 9.4, after that paragraph.

#### Replace with

> One structural property of the panel is left entirely unexploited. Brands sit
> within categories and categories within markets, which makes the data a mixed
> hierarchical and grouped structure in the established sense, and forecasts
> produced independently at the brand level are not guaranteed to sum to a
> forecast produced at the category level. The thesis reconciles nothing: each
> series is forecast on its own terms. Two consequences follow. Established
> reconciliation methods would very likely improve accuracy at every level by
> borrowing strength across the hierarchy, and the back-transformed point
> forecasts this substrate serves are medians rather than means, so summing brand
> forecasts to a category total would be biased even before reconciliation is
> considered, since medians do not add (Hyndman & Athanasopoulos, 2021).

### Note — why this belongs in the thesis rather than being left quiet

This is the largest **methodological** gap the book scan found, and it is
entirely unmentioned across ten chapters. Two reasons to name it:

1. **It is literature-recognised and has a vocabulary.** Naming it correctly —
   hierarchical/grouped, reconciliation, MinT — demonstrates command of the
   field. Leaving it unnamed while an examiner recognises it demonstrates the
   opposite.
2. **The medians-do-not-add point is operationally live.** Any user of this tool
   who sums brand forecasts to a category total gets a biased number, with
   nothing in the interface warning them. That is a real property of the shipped
   artefact.

The bias-adjusted mean for lambda = 0 is `y_hat = exp(w_hat) * [1 + sigma^2/2]`.
**Do not put the formula in Chapter 9** — it belongs in Chapter 6 or 7 with the
interface if it is implemented, and P0048 already carries it as an open SRQ2
item.

⚠ **Do not claim reconciliation *would* have improved accuracy.** The prose above
says "very likely", which is what the literature supports in general and what
this thesis has not measured. Any stronger verb is a claim without a run behind
it.

---

## Fix 4 — 9.5, the future-work direction this opens

### Anchor

**Section 9.5 Future research directions.** The opening line:

> "Four directions follow from what this evaluation could not settle."

### Action

EDIT-THEN-INSERT — two steps.

**Step 1.** Change **"Four directions"** to **"Five directions"**.

**Step 2.** INSERT a new paragraph after the one beginning *"The evaluation
should be widened across categories and repeats"* and before the one beginning
*"Finally, whether a communicated forecast improves a planner's decision"*.

#### Replace with

> The hierarchical structure of the panel should be exploited rather than
> ignored. Reconciling brand-level forecasts against category and market
> aggregates is established practice with mature estimators, one of which
> requires no residual history and would therefore extend to the scenario
> forecasts as readily as to the substrate's own. That property makes it an
> unusually good fit for this thesis's comparison, since it would allow
> judgmental and model-based forecasts to be reconciled on the same footing.

### Note — the detail worth knowing and not writing

The estimator that *"needs no residuals"* is `wls_struct`, structural weighted
least squares. It is the one that suits **judgmental** base forecasts — which is
exactly what the language-model scenarios produce.

**Keep the estimator name out of the prose.** Naming a specific implementation in
a future-work paragraph invites "why did you not just run it", and the honest
answer is that reconciliation is a chapter of work rather than a function call.
The prose above says what it would do and why it fits, which is the right
altitude for future work.

---

# Part 2 — SRQ4 framing, and one measurement worth making

**Neither of these is a fix.** They are arguments available to Chapter 9 that I
am not proposing as prose, with the reason in each case.

## The B→C increment is judgmental adjustment, and the literature has a position on it

An LLM handed a model forecast plus context **is** performing judgmental
adjustment in the established sense. The book's position is specific and it cuts
both ways:

- adjustments *"should not aim to correct for a systematic pattern... thought to
  have been missed by the statistical model. This has been proven to be
  ineffective, as forecasters tend to read non-existent patterns in noisy
  series"*
- they are effective *"only when there is significant additional information at
  hand"*
- **large adjustments are more accurate than small ones**; small optimistic ones
  actively hinder

**Why this is a strong framing for §9.1.4:** the book's condition for judgmental
adjustment helping — genuine extra information rather than pattern-reading — is
*precisely* what the B→C increment measures. And the finding that all eighteen
combined-scenario runs carry `deviates_from_model = True` becomes interpretable
rather than merely odd: the agent is adjusting, and the question is whether it
had information or was reading patterns.

**Why I am not proposing it as prose:** §9.1.4 was rewritten four days ago and
reads well. Inserting a literature frame into a section that currently reports a
measurement cleanly risks trading a crisp finding for a discursive one.
**NEEDS-BRIAN** — I will write the block if you want it.

## Anchoring is testable on the runs you already have, for free

The book observes that judgmental forecasters commonly *"take the last observed
value as a reference point"*, leading to *"conservatism and undervaluing new
information"*.

**That is a falsifiable prediction about `A_llm_plain`**, and the 63 logged runs
can test it with **no new spend**: correlate each plain-arm forecast against the
final observed value of the series it was given.

Either result is reportable. If the plain arm anchors and the model-backed arms
do not, that is a **mechanism** for the B→C increment rather than just a size —
which is a substantially stronger contribution than a magnitude.

✅ **This one is safe for Branch A, and it is the only diagnostic in these four
notes that is.** The distinction is that it measures the *experiment's results*
rather than the *substrate's design*. It reads existing logs, it changes no
feature, it triggers no retraining, and **neither outcome can contradict a
choice already baked into the artefact** — if the plain arm does not anchor, that
is simply a null result you need not report.

⚠ **But it is optional, and it is genuinely new analysis.** If the time is not
there, drop it: Chapter 9 is complete without it. Do not start it within a day of
submission — a half-finished analysis is worse than none, and this one earns a
mechanism rather than fixing a defect.

---

# Citations register rows

| | |
|---|---|
| Source | Hyndman & Athanasopoulos (2021), *Forecasting: Principles and Practice*, 3rd ed. |
| Zotero key | `5NFQRRXS` |
| Status | **IN-ZOTERO** ✓ — verified against the 89-item pull |

| Fix | Lands in | Supports the sentence |
|---|---|---|
| 2 | 9.4 | "...impose the constraint through the transformation itself, which applies the bias adjustment automatically and preserves interval coverage" |
| 3 | 9.4 | "...summing brand forecasts to a category total would be biased... since medians do not add" |

**Fix 1 and Fix 4 carry no citation.** Fix 1 is a statement about this repo,
evidenced by line numbers rather than literature. Fix 4 describes future work in
general terms deliberately.

⚠ **Fix 3 cites one source for two distinct claims** — the hierarchical structure
(§11.1) and the median non-additivity (§5.6). Both are in the same book and the
house style cites the book, not the section, so one citation is correct. If a
reader asks which part supports which claim, the answer is in the archived scan
note.

---

# What is now outstanding for Chapter 9

| Item | State |
|---|---|
| Branch A rewrite | ✅ applied, archived |
| Follow-up 01 | ✅ applied, archived |
| The four questionable-recency notes | ✅ three archived; `the-result-hinges-on-forecasting-practice.md` still live |
| This note | awaiting review |
| §9.1.4 judgmental-adjustment frame | **NEEDS-BRIAN** — offered, not written |
| Anchoring test | **optional, Branch A safe** — reads existing logs, no retrain. Drop it if time is short |
