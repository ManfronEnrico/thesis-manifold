---
name: brand-sampling-and-inclusion-criteria
description: REFERENCE - The three inclusion criteria that define the SRQ4 brand population (test-window length, non-zero actuals, volume floor), why each exists, the measured evidence for the 1,000-unit floor, and the paragraph the methodology chapter needs.
category: reference
applies-to: [ch3-methodology, ch8-evaluation, ch10-limitations]
triggers: [writing the SRQ4 sampling section, defending brand selection, justifying the volume floor, answering "why these three brands"]
created: 2026_09_11-23_30
updated: 2026_09_11-23_30
---

# Brand sampling: three inclusion criteria, and why each is needed

**Every criterion below is a filter on the POPULATION, applied before any scenario runs
and identically for all seven arms.** None of them selects brands by outcome, and that is
what makes the sample defensible rather than convenient.

---

## The criteria, in the order they apply

| # | criterion | removes | why |
|---|---|---|---|
| 1 | at least HORIZON held-out months | brands with nothing to score at H=3 | a shorter window has no scored month; including them puts brands in the sample that every run then skips |
| 2 | no zero actuals anywhere in the test window | intermittent / zero-inflated series | APE divides by the actual, so a zero month makes the score **undefined**, not merely hard |
| 3 | **scored-month actual >= 1,000 units** | degenerate low-volume series | a defined APE is not automatically a **meaningful** one — see below |

Criteria 1 and 2 predate this work. **Criterion 3 was added 2026-09-11** after measuring
what criterion 2 alone lets through.

---

## Why the volume floor exists — the measured case

Stratifying CSD by volume into max / median / min, over brands passing criteria 1 and 2
only, returns:

| stratum | brand | scored-month actual |
|---|---|---|
| max | HARBOE | 6,365,900 |
| median | NIKOLINE | 457 |
| min | **VOELKEL** | **9** |

On a 9-unit series the arithmetic is decisive:

| error | APE |
|---|---|
| 1 unit | **11.1%** |
| 2 units | 22.2% |
| 3 units | 33.3% |

**A one-unit difference on VOELKEL outweighs the entire measured gap between the
code-as-action and dedicated-model arms on HARBOE.** No forecasting method can influence
a score at that resolution; it measures integer rounding. Including such a brand does not
test robustness on thin series — it injects a number that is noise by construction.

This is not a tail case. **14 of CSD's 76 qualifying brands sell fewer than 100 units** in
the scored month. The low end of the category is a cliff rather than a gradient.

## What the floor keeps

| | before floor | after floor |
|---|---|---|
| CSD brands in pool | 76 | **45** |
| smallest scored actual | 9 | **2,850** |
| worst-case 1-unit APE | 11.1% | **0.035%** |
| orders of magnitude spanned | ~6 | **~3** |

The resulting CSD sample:

| stratum | brand | rank in pool | scored actual | 1-unit APE |
|---|---|---|---|---|
| max | HARBOE | 1 / 45 | 6,365,900 | 0.00002% |
| median | 7-UP | 23 / 45 | 13,042 | 0.008% |
| min | ØRBÆK | 45 / 45 | 2,850 | 0.035% |

**Three orders of magnitude is still a genuine volume range** — this is not a narrow band
chosen to flatter any arm. The floor removes the region where measurement fails, not the
region where the comparison is hard.

---

## The paragraph the methodology chapter needs

Bullets, not prose. Convert only with approval.

- The brand population is defined by three inclusion criteria applied before any run, and
  identically across all seven scenarios.
- **Criterion 1:** the brand must have at least as many held-out months as the forecast
  horizon, or there is no scored month.
- **Criterion 2:** no zero actuals in the held-out window. Percentage error divides by the
  actual, so a zero renders the score undefined. This also scopes the study to brands with
  continuous recent sales, which is the honest population for a demand forecast —
  intermittent series are a different forecasting problem.
- **Criterion 3:** the scored-month actual must be at least 1,000 units. Below roughly that
  volume, percentage error is dominated by integer rounding rather than forecast quality:
  on a nine-unit series a single unit of error registers as 11% error, which exceeds the
  differences the experiment is designed to detect.
- The floor is a property of the **measurement**, not of the method: it identifies where
  the chosen error metric stops discriminating, and excludes that region for every
  scenario equally.
- Within the qualifying population, brands are selected by **volume stratification** —
  highest, median and lowest — so the comparison covers the volume range rather than only
  the largest, most data-rich series, where a trained model would be expected to look best.

### The sentence to avoid

Do **not** write that low-volume brands were excluded because they are "hard to forecast"
or "noisy". That is an outcome-based justification and invites the reader to suspect the
sample was trimmed until the artefact won. The criterion is about the **metric's
resolution**, and the distinction must be explicit.

---

## The limitation to state alongside it

- The volume floor means the results speak to brands above roughly 1,000 units per month
  in the scored period. Whether the findings extend to very-low-volume or intermittent
  series is **not tested here**, and is named as further work.
- Intermittent-demand forecasting has its own literature and its own error metrics, which
  exist precisely because percentage error fails on such series. Applying MAPE-family
  metrics there would be a methodological error, not a harder version of the same study.
- **This is a genuine scope boundary, not a weakness to apologise for.** State it in the
  design section as well as in limitations, so a reader meets it as a decision rather than
  discovering it as a caveat.

---

## Implementation

`MIN_SCORED_UNITS = 1000` in `srq4_experiment.py`, applied by `_above_volume_floor()`,
which `_stratified_brands()` draws from. It filters on the **scored-month actual** — the
value that enters the APE denominator — not on mean or total volume, because a brand can
average well and still be scored on a thin month.

Falls back to the unfloored pool with a printed warning if no brand in a category clears
the floor, rather than failing silently. Measured 2026-09-11: all four categories retain a
usable pool (CSD 45, Danskvand 13, Energidrikke 19, RTD 17).

Evidence and full reasoning: P0049 findings F58.
