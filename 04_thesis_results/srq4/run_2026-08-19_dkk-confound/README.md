# Run 1 — 2026-08-19 — INVALID for Scenario A (unit confound)

18 runs (2 CSD brands x 3 repeats x 3 scenarios), $3.44 estimated.
**Scenarios B and C are valid. Scenario A is not.**

## The defect

The shared question was *"What will {brand} sell ...?"*. All six Scenario A runs
answered in **DKK**, not units:

| run | answer | actual (units) |
|---|---:|---:|
| COCA COLA rep0-2 | 145,000,000 / 118,000,000 / 104,000,000 DKK | 3,152,932 |
| HARBOE rep0-2 | 21,000,000 / 34,000,000 / 32,000,000 DKK | 4,778,907 |

Scenarios B and C infer the unit from the data they are handed. Scenario A has no
data, so an ambiguous question let it answer a *different* question — and its
measured 570% median APE is an artefact of the prompt, not a property of the
scenario. That is precisely the confound the shared question exists to remove.

Note the answers are not unreasonable *as DKK*: ~145M DKK for Coca-Cola monthly
Danish CSD retail is a plausible value estimate. The model was not hallucinating;
it was answering the question asked.

## Fixed

The question now reads *"How many units of {brand} will be sold ... ? Answer in
units sold, not currency."*

## What remains usable

Scenarios B and C were unaffected — both receive the unit implicitly through the
data — so their numbers stand and are consistent with run 2:

| Scenario | median APE | CV across repeats | latency | cost |
|---|---:|---:|---:|---:|
| B_data | 13.5% | 5.27% / 0.48% | 113.6 s | $1.598 |
| C_model | **7.7%** | **0.00%** | **5.2 s** | **$0.041** |

Kept as evidence of the defect and of the B/C comparison at n=3.
