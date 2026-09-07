# SRQ1 -- demand-pattern categorisation (Syntetos-Boylan-Croston)

Every brand is classified on two measured quantities, using the derived
cut-offs of Syntetos, Boylan & Croston (2005, *JORS* 56(5), 495-503, p. 495):

- **p** -- average inter-demand interval (periods per non-zero demand)
- **CV^2** -- squared coefficient of variation of **non-zero** demand sizes

| | CV^2 <= 0.49 | CV^2 > 0.49 |
|---|---|---|
| **p <= 1.32** | smooth | erratic |
| **p > 1.32** | intermittent | lumpy |

The thresholds are **derived, not tuned** -- they mark where the relative
accuracy ordering of Croston's method, the SBA and simple exponential
smoothing changes. Classification uses **train+val only**; using test rows to
categorise and then reporting test accuracy per class would leak.

## Brands per class

| Category | smooth | erratic | intermittent | lumpy | total |
|---|---|---|---|---|---|
| CSD | 44 | 32 | 5 | 14 | 95 |
| RTD | 32 | 20 | 2 | 8 | 62 |
| danskvand | 16 | 9 | 3 | 1 | 29 |
| energidrikke | 16 | 18 | 2 | 8 | 44 |
| **all** | **108** | **79** | **12** | **31** | **230** |

## Why this replaces the 1 unit/month volume floor

The floor was a judgement call standing in for 'series too irregular to
inform a comparison'. Volume is a poor proxy for regularity, and the
measured overlap shows how poor:

| | brands |
|---|---:|
| Below the old floor (<1 unit/month) | 38 |
| — of which **smooth** (well-behaved, merely small) | **8** |
| — of which lumpy or intermittent | 22 |
| **Above** the floor yet lumpy/intermittent (the floor missed them) | **21** |

So the floor **removed well-behaved small brands** -- exactly the series a
forecasting study should keep -- while **leaving irregular ones in**. The SBC
scheme measures the property that actually matters.

## How to use this

**This categorises; it does not exclude.** Report accuracy **per demand
class**, so that a weak result on lumpy series is visible as a stated
limitation rather than absorbed into a pooled average or hidden behind a
threshold. Both Hyndman & Koehler (2006, p. 683) and Syntetos & Boylan
(2005) object to discarding difficult series; categorising them is the
response their own work recommends.

**A caveat to state.** The cut-offs were derived for Croston-type estimators
under specific assumptions (alpha = 0.15, lead time 1), not for gradient
boosting on a brand-month panel. They are used here as a **principled,
citable partition of demand patterns**, not as a claim that the same
accuracy ordering holds for these models -- which is itself a question the
per-class results can answer.
