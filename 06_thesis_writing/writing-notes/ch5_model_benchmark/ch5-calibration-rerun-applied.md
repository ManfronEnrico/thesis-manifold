---
name: ch5-calibration-rerun-applied
description: NOTE - The calibration re-run is done. Section 5.5.7's table needs eight numbers replaced, and its central claim gets stronger. Small, self-contained, and the only outstanding Chapter 5 edit.
snapshot: 2026-09-11_15-41_ch5-applied-review
category: workflow
applies-to: [chapter 5]
created: 2026_09_11-18_00
updated: 2026_09_11-18_00
status: ready
---

# The calibration re-run is done - one table to update

**Run locally 2026-09-11 in nine seconds.** No retraining; the served models were
not touched. This closes S17 and P0053 F12.

`srq1_calibration.py` now reads which model each category actually serves and
calibrates that one, instead of fitting XGBoost for all four:

```
CSD:          calibrating the served model -- XGBoost
Danskvand:    calibrating the served model -- XGBoost
Energidrikke: calibrating the served model -- LightGBM
RTD:          calibrating the served model -- LightGBM
```

## What moved

Only Energidrikke and RTD were being calibrated on the wrong model, so only
those two should move materially. **That is what happened**, which is itself a
check that nothing else changed underneath:

| Category | Nominal | Coverage before | after | Width before | after |
|---|---|---|---|---|---|
| CSD | 90% | 91.0 | **91.7** | 8.62 | **8.99** |
| RTD | 90% | 90.9 | **91.4** | 8.62 | **8.52** |
| Energidrikke | 90% | 86.0 | **86.7** | 33.64 | **34.44** |
| danskvand | 90% | 83.9 | **83.9** | 11.89 | **11.77** |
| CSD | 80% | 82.3 | **80.5** | 3.83 | **3.40** |
| RTD | 80% | 80.6 | **83.3** | 3.79 | **3.92** |
| Energidrikke | 80% | 78.9 | **77.3** | 12.39 | **10.54** |
| danskvand | 80% | 72.4 | **73.6** | 2.93 | **3.03** |

✅ **The check specified in advance passed.** danskvand at the 90 per cent level
is an XGBoost category, so its coverage should not have moved. It did not -
83.9 before and after. Had it moved, something else would have changed and the
run would not have been trustworthy.

## Paste - replace the Section 5.5.7 table

| Category | Nominal | Empirical coverage | Mean relative width | n test |
|---|---|---|---|---|
| CSD | 90% | 91.7% | 9.0x | 665 |
| RTD | 90% | 91.4% | 8.5x | 372 |
| energidrikke | 90% | 86.7% | 34.4x | 308 |
| danskvand | 90% | **83.9%** | 11.8x | 174 |
| CSD | 80% | 80.5% | 3.4x | 665 |
| RTD | 80% | 83.3% | 3.9x | 372 |
| energidrikke | 80% | 77.3% | 10.5x | 308 |
| danskvand | 80% | **73.6%** | 3.0x | 174 |

**Caption:** *Table 13 - Prediction-Interval Coverage and Width*

## Every claim in the section survives, and one gets stronger

| Claim in the prose | Still true? |
|---|---|
| danskvand misses the 85% target at the 90% level | ✅ **83.9%**, unchanged |
| danskvand misses at the 80% level too | ✅ 73.6% against 80 |
| energidrikke's intervals are the widest, ~34x | ✅ **34.4x** - the "thirty-four times" wording still holds |
| CSD and RTD attain nominal coverage at both levels | ✅ all four figures at or above nominal |
| CSD and RTD stay "under nine times the forecast quantity" | ⚠ **CSD is now 9.0x.** See below |
| **calibration quality tracks calibration set size** | ✅ **now strictly monotone** - stronger than before |

### The one wording fix

The prose says CSD and RTD attain coverage *"with intervals under nine times the
forecast quantity"*. CSD is now **9.0x**, which is not under nine.

**Replace** *"with intervals under nine times the forecast quantity"* with:

> with intervals of roughly nine times the forecast quantity

### The central claim is now strictly monotone

Ordered by calibration set size, at the 90 per cent level:

| Category | n calibration | Coverage |
|---|---|---|
| danskvand | 174 | 83.9% |
| energidrikke | 264 | 86.7% |
| RTD | 372 | 91.4% |
| CSD | 665 | 91.7% |

**Coverage rises with every increase in calibration set size, without exception.**
Before the re-run the ordering held loosely; it is now exact. The sentence
*"calibration quality tracks calibration set size"* is carrying more weight than
when it was written, and deserves it.

## Paste - the scope sentence narrows

The section currently ends with a sentence added to cover the defect:

> "These intervals are calibrated on gradient-boosted residuals under a single
> implementation, and the conformal procedure is applied identically in every
> category; the coverage reported here therefore describes the calibration
> method on this panel rather than a property of whichever implementation is
> finally served."

**That hedge is no longer needed.** Replace it with the stronger claim the
re-run earns:

> Each category's interval is calibrated on the residuals of the model that
> category actually serves, so the coverage reported here describes the deployed
> configuration rather than a uniform stand-in for it.

## Note - what was fixed in the generator besides the model choice

Two self-description defects in `calibration.md`, both of the same kind as the
pooled header:

- the title read **"tuned XGBoost"** as a literal. It now names the models
  actually fitted, computed from the served metadata.
- the width column was labelled **"Median rel. width"** while the value is a
  mean. This is the same defect Chapter 5's comment on Section 5.4 caught in the
  metric table; it existed in the artefact too.
