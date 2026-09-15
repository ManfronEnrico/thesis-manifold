---
name: 2026-09-15_BRANCH_A_ch5-operational-profile-figures-stale
description: NOTE - Section 5.5.6 cites six memory and latency figures that no longer match profiling.csv, and omits Prophet entirely. Two REWORDs, both paste-ready.
category: reference
applies-to: [ch5-model-benchmark, 5.5.6 Operational profile]
triggers: [applying the appendix pass, checking Ch5 resource claims]
created: 2026_09_15-14_10
updated: 2026_09_15-14_10
snapshot: 2026-09-15_13-08_appendix-pass-context
status: not applied
---

# Ch5 §5.5.6 — the operational profile cites superseded measurements

Found while regenerating `ch5_resource_profile_v2`, which you flagged as
showing three models against a prose sentence naming four.

**The figure was right to be questioned and the prose is the stale half.**
`05_thesis_results/05_model_benchmark/tables/profiling.csv` is the artefact
both the figure and the prose draw on. Every current value, read from it:

| Model | Peak fit RSS (MB) | Fit (s) | Predict (ms) | Train rows |
|---|---|---|---|---|
| Ridge | 1.5 | 0.008 | 2.2 | 2,280 |
| LightGBM | 17.9 | 1.758 | 15.5 | 2,280 |
| XGBoost | 34.5 | 1.679 | 11.8 | 2,280 |
| ARIMA (per-series) | 2.1 | 0.04 | 4.7 | 24 |
| Prophet (per-series) | 5.2 | 11.373 | 95.3 | 24 |

**Six of the section's figures no longer match, and a fifth model is missing.**
The figure now plots all five; these two rewords bring the prose alongside it.

---

## Fix 1 — the memory sentence

### Anchor

**Section 5.5.6 Operational profile**, the first sentence of the section,
immediately under the heading.

Starts: *"Peak resident memory during fitting is in the tens of megabytes"*

Ends: *"...and 1.6 for Ridge."*

### Action

REWORD.

#### Replace with

> Peak resident memory during fitting is in the tens of megabytes at most: 34.5 MB for XGBoost, 17.9 for LightGBM, 5.2 for a per-series Prophet, 2.1 for a per-series ARIMA and 1.5 for Ridge. Against the four-gigabyte sequential budget, the memory constraint is non-binding by two orders of magnitude at this data scale. That is a real answer to the research question rather than a missing measurement: the constraint that motivated the question does not bite here.

### Note — what changed and why

Three of the four cited numbers moved (31.9→34.5, 14.9→17.9, 1.6→1.5; ARIMA
2.0→2.1), and Prophet was absent although it is one of the six families §5.2
describes. "in the tens of megabytes for every model" was also loose in the
other direction — three of the five are under 6 MB — so it becomes "at most".

---

## Fix 2 — the latency sentence

### Anchor

**Section 5.5.6**, second paragraph.

Starts: *"Latency is likewise immaterial for an interactive setting."*

Ends: *"...far below the threshold at which a user perceives delay."*

### Action

REWORD.

#### Replace with

> Latency is likewise immaterial for an interactive setting. XGBoost fits in 1.7 seconds and predicts in 11.8 milliseconds; LightGBM fits in 1.8 seconds and predicts in 15.5. Prediction is the operation an agent waits on, and at tens of milliseconds it is far below the threshold at which a user perceives delay.

### Note — the one figure that does not fit the claim

All four cited numbers are stale (3.6→1.7 s, 13.8→11.8 ms, 8.0→1.8 s,
33.0→15.5 ms), and in every case the current measurement is *faster*, so the
argument strengthens.

**Prophet is deliberately left out of this sentence.** It fits in 11.4 seconds
and predicts in 95.3 ms — an order of magnitude slower than the rest, and the
only model that would complicate "immaterial". It is not hidden: it appears in
the figure and in the table above. If you would rather meet it head-on, add
after the second sentence:

> Prophet is the exception at 11.4 seconds to fit and 95.3 milliseconds to predict, still well inside an interactive budget, and it is fitted per series rather than once per category.

---

## Note — this is the second artefact in this section to go stale the same way

§5.5.6's third paragraph says *"These figures are measured on the eighteen-feature
matrix the substrate currently uses"* — which is still true, and is exactly why
the numbers moved: they were measured on an earlier run of that matrix. The
paragraph reads as though it dates the figures, and it does not.

No change proposed there; flagged only so it is not read as confirmation that
the figures above it are current.
