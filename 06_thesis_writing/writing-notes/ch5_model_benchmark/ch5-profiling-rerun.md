---
name: ch5-profiling-rerun
description: NOTE - profiling.csv predated the last training and has been re-run. Section 5.5.6's four figures change, and its disclaimer is now falsified in the opposite direction. Small, self-contained, the only outstanding Chapter 5 edit.
snapshot: 2026-09-11_18-35_ch6-post-rename
category: workflow
applies-to: [ch5-model-benchmark]
created: 2026_09_11-18_45
updated: 2026_09_11-18_45
status: ready
---

# The operational profile was measured before the last training

**Found by applying your own rule:** any cited number must come from an artefact
regenerated *after* the last training run.

| | |
|---|---|
| last training | **2026-09-09 21:10** (served model metadata) |
| `profiling.csv` was written | **2026-09-01 21:32** |

**Eight days early.** It was the only Chapter 5 source that failed the test, and
it failed it because `srq1_profiling.py` is deliberately excluded from
`run_both_horizons.py` - it runs at `n_jobs=-1` on purpose, so folding it into
the deterministic suite would destroy what it measures. The exclusion is
correct. The consequence was that nothing re-ran it.

**Re-run 2026-09-11, twelve seconds.** No retraining; it reads tuned
hyperparameters from disk, exactly like the calibration re-run.

## What moved, and it is not a small correction

| Model | Peak fit RSS before | after |
|---|---|---|
| LightGBM | 38.1 | **14.9** |
| XGBoost | 29.2 | **31.9** |
| Ridge | 5.4 | **1.6** |
| ARIMA (per series) | 1.9 | **2.0** |

Two other columns moved with them: **features 13 → 18**, and **training rows
2,470 → 2,280**, the latter from the horizon fix.

## Paste - Section 5.5.6, the figures

**Anchor** - Section 5.5.6 Operational profile, first paragraph, opening:

> "Peak resident memory during fitting is in the tens of megabytes for every
> model: 38.1 MB for LightGBM, 29.2 for XGBoost, 5.4 for Ridge and 1.9 for a
> per-series ARIMA."

**Action:** REWORD the first sentence.

> Peak resident memory during fitting is in the tens of megabytes for every
> model: 31.9 MB for XGBoost, 14.9 for LightGBM, 2.0 for a per-series ARIMA and
> 1.6 for Ridge.

⚠ **The ordering reverses.** XGBoost is now the largest, where LightGBM was
before. Listing them descending keeps the sentence readable and makes the
reversal deliberate rather than accidental.

## Paste - the disclaimer is now falsified, and must go

The section currently ends:

> "These figures were measured on a thirteen-feature matrix and are therefore a
> lower bound on the memory the current eighteen-feature model requires. The
> conclusion is unaffected: the margin against the budget is large enough that a
> proportional increase does not approach it."

⚠ **That was a reasonable inference and it is now measured to be wrong.** More
features did **not** cost more memory. LightGBM fell by 61 per cent and Ridge by
70 per cent. Only XGBoost rose, by 9 per cent.

**Replace the whole passage with:**

> These figures are measured on the eighteen-feature matrix the substrate
> currently uses. Memory tracks the size of the tuned ensemble rather than the
> width of the feature matrix: the models that shrank did so because tuning
> selected fewer and shallower trees, not because they were given less to read.
> The margin against the budget is large enough in either case that the
> comparison does not turn on it.

### Note - why the numbers fell, verified

Not a measurement artefact. The tuned configurations changed at the last
retraining, and ensemble size is what drives the footprint:

| | tuned now |
|---|---|
| CSD LightGBM | 302 trees, 107 leaves |
| CSD XGBoost | 983 trees, depth 9 |

The previous table's own note describes the XGBoost ensemble it measured as
**926 trees at depth 7**. XGBoost grew slightly and its memory grew with it;
LightGBM's shrank. **The feature count was never the driver**, which is exactly
what the old disclaimer assumed and why it pointed the wrong way.

⚠ **This is a better finding than the one it replaces.** A chapter that says
"memory follows the tuned ensemble, not the feature set" has said something
about the substrate. The old sentence only hedged.

## What else this touches

| Artefact | State |
|---|---|
| `profiling.csv` / `.md` | **regenerated** |
| appendix `05_substrate_resource_profile` | **regenerated** from it; now reads 18 features and 4096 MB |
| Chapter 6 | **no edit needed.** The consolidated pass already cuts its figures and cites Chapter 5 |

The appendix table's budget-share row now reads **0.04 to 0.78 per cent** of
4096 MB, all four models. Serving remains three orders of magnitude below
fitting, at **0.03 to 0.47 MB**.

## The four artefacts that still predate the training

Same check, same folder. None is cited in Chapter 5 or 6 today, but each is a
trap for a later pass:

| Artefact | Written |
|---|---|
| `param_drift.csv` | 09-01 21:32 |
| `refit_vs_retune.csv` | 09-01 21:32 |
| `retune_single_cutoff.csv` | 09-01 21:32 |
| `sandbox_profiling.csv` | 09-03 11:45 |

⚠ `08_parameter_drift` **was** regenerated on 09-10 and is current; the raw
`param_drift.csv` beside it is the stale one. **Cite the numbered appendix
table, not the raw CSV**, wherever both exist.
