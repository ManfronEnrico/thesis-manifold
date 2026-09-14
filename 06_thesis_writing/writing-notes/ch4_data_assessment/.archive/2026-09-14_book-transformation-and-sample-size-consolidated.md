---
name: ch4-book-findings-transformation-and-sample-size
description: NOTE - Three Hyndman & Athanasopoulos findings bearing on Ch4. One CONFIRMS, one REFINES the justification, one may UNDERCUT the MIN_PERIODS argument.
category: reference
applies-to: [ch4 data assessment]
triggers: [ch4 prose pass, defending the log transform, justifying the retention threshold]
created: 2026_09_13-21_15
updated: 2026_09_13-21_15
source: P0055 book scan, 41/41 sections. Full catalogue in plans/P0055_*/findings.md F15
---

# Ch4 - the transformation argument, and one uncomfortable finding

**Two of these strengthen the chapter. One may require rewording.** Read the
third before the prose pass, not after.

---

## 1. Section 3.2 - the log transform commits the thesis to MULTIPLICATIVE seasonality

### What the book says

> "When the variation... appears to be **proportional to the level**, then a
> multiplicative decomposition is more appropriate. Multiplicative
> decompositions are common with economic time series."

And the equivalence that matters:

> "y = S x T x R **is equivalent to** log y = log S + log T + log R"

### What this means for Ch4

The uniform `log1p` **is** a multiplicative-seasonality assumption. That is very
likely correct for retail beverage demand - but the thesis nowhere states that
this is what the transform commits it to.

### To claim

Verdict: **CONFIRMS the choice, REFINES the justification.** The log is
defensible; the reason currently given is incomplete. State what the transform
assumes, and that the assumption suits the domain.

---

## 2. Section 3.1 - Ch4's defence of the uniform transform answers the WRONG objection

### What Ch4 currently argues

That per-series transformation selection was rejected because "the tests that
would drive such a selection have **limited power** at forty-six observations."

### Why that argument does not land

> "The **guerrero** feature (Guerrero, 1993) can be used to **choose a value of
> lambda for you**" - "a good value of lambda is one which makes the size of the
> seasonal variation about the same across the whole series."

**Guerrero is an ESTIMATOR, not a hypothesis test.** The low-power objection
applies to tests. It does not apply to parameter estimation. So the chapter is
defending a correct choice with an argument that does not support it.

### What to do

⚠ **Do not rewrite this until Branch B task 19 runs.** That task estimates
Guerrero lambda per brand, and the result determines the wording. Three
outcomes, all publishable:

| Result | What Ch4 then says |
|---|---|
| lambda near 0 across brands | the log is vindicated **empirically**, not assumed - strictly stronger than today |
| lambda far from 0 | the uniform transform is overturned, and that is a finding |
| lambda dispersed | the low-power argument is **measured** rather than asserted |

**Every outcome improves the chapter.** This is why the task is worth running.

---

## 3. ⚠ Section 13.7 - minimum-sample rules of thumb are rejected outright

**This is the one that may undercut existing prose rather than extend it.**

### What the book says

> "Some textbooks provide **rules-of-thumb giving minimum sample sizes**... These
> are **misleading and unsubstantiated in theory or practice**... There is, for
> example, **no justification for the magic number of 30**... The only
> theoretical limit is that we need more observations than there are parameters."

Recommended instead: "**The AICc is particularly useful here**, because it is a
proxy for the one-step forecast out-of-sample MSE."

Their empirical result on 152 short M3 series: 21 got zero-parameter models, 86
one, 31 two, 13 three, **only 1 got four**.

### The question for Ch4

**How is `MIN_PERIODS` justified?** If the answer is a rule of thumb, the book
explicitly rejects that reasoning. If it is derived from the lag structure
(which the code suggests - `MIN_PERIODS` follows `MAX_LAG`), then it is a
**parameter-count argument** and the book SUPPORTS it.

### What to do

**Check before writing.** The P0055 log's own framing: this "may require
rewording rather than re-engineering." Branch B task 23 does the check.

If it turns out to be parameter-derived, this flips from a threat into another
free citation - the book's "only theoretical limit is that we need more
observations than there are parameters" is precisely the repo's rule.

---

## Also relevant to Ch4, lower priority

| Sec | Finding |
|---|---|
| **2.3** | "cyclic" is **unclaimable** at 39-46 months - cycles are "usually at least 2 years", so two cycles would consume the panel. **Audit the chapter for the word.** Call non-seasonal fluctuation what it is |
| **2.4 / 2.5** | Seasonal **stability across years** is never checked, yet `peak_month` is computed from pooled means. 2.4 is "especially useful in identifying years in which the pattern changes" |
| **11.1** | The panel is exactly a mixed **hierarchical/grouped** structure, (category/brand) x market. The thesis has never named it. Deferred as future work, but naming it costs a sentence |
