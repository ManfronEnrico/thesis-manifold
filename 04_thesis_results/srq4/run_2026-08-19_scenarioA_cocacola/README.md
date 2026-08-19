# Scenario A, second attempt — 2026-08-19 — INCOMPLETE (credits exhausted)

Intended: Coca Cola x 3 repeats, Scenario A, to complete the ladder on both
brands. **Did not reach Coca Cola.** $0.90 spent, then HTTP 429
`credit_balance_exhausted`.

| brand | rep | forecast | APE | outcome |
|-------|----:|---------:|----:|---------|
| HARBOE | 0 | 3,300,000 | 30.9% | ok |
| HARBOE | 1 | 2,700,000 | 43.5% | ok |
| HARBOE | 2 | — | — | credits exhausted |
| COCA COLA | 0-2 | — | — | credits exhausted |

## Why it did not reach Coca Cola

`--brands-per-cat 2` selects the top 2 brands and iterates from the first, so the
run repeated HARBOE before reaching Coca Cola. There is no "skip to brand N"
switch. Scenario A costs ~$0.45/run, so 6 runs is ~$2.70 — more than the ~$1.50
estimated for "3 calls".

**Fix for next time**: add a `--brands` switch naming specific brands, or run
with `--brands-per-cat 1` after reordering. Do not assume a partial re-run costs
only the missing cells.

## Usable data

The two completed HARBOE runs (30.9%, 43.5%) are consistent with the first
corrected run (35.1%, 35.1%, 30.9%). Pooling all five gives HARBOE Scenario A a
median APE of ~35% and visible run-to-run spread (30.9-43.5%), which is a wider
CV than the first three runs alone suggested.

**Coca Cola's Scenario A figure is still unmeasured**, so the A→B increment is
established on one brand only.
