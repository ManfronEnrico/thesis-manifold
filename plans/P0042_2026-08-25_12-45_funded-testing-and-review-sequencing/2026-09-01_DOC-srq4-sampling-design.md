---
name: 2026-09-01-doc-srq4-sampling-design
description: RULE - The frozen SRQ4 sampling design under budget constraint, with the methodology wording it must be reported in.
category: governance
applies-to: [srq4, 05_thesis_writing, scenario_setup]
triggers: [running a paid SRQ4 scenario block, writing Ch3 methodology, writing Ch7/Ch8 results]
created: 2026_09_01-00_00
updated: 2026_09_01-00_00
---

# SRQ4 sampling design — frozen 2026-09-01

This discharges **P0042 gate 1**: scope committed in writing *before* any result
is seen. Decided by Brian, 2026-09-01.

## The design principle: allocation inversely proportional to per-run cost

Per F2, `A_plain` costs ~63x `C_model` per run. Equal allocation across scenarios
is therefore **not** the efficient design — it spends most of the budget on the
arm whose result is least in doubt.

Samples are allocated where they buy information:

| Scenario | Reps | Rationale |
|---|---:|---|
| `A_plain` | 3 | Establishes the floor. The A->B gap measured +17.8pp — far too large to be in doubt at any plausible n. Deliberately under-sampled |
| `B_data` | 10 | The contested increment. B->C measured +3.5pp; F17 sizes n=10 for 80% power |
| `C_model` | 10 | as above |
| `C_model` breadth | 5 x 9 brands | Generalisation across all 4 categories at ~$0.03/run |

**This is a design decision, not a shortfall.** The reporting wording is fixed in
the last section below and must not drift toward apology.

## The blocks

| Block | Config | Runs | Est. | Realistic |
|---|---|---:|---:|---:|
| 1. A floor | CSD, 2 brands x 3 reps, `--scenarios A` | 6 | $2.57 | ~$11 |
| 2. B vs C core | CSD stratified 3 brands x 10 reps, `--scenarios B,C` | 60 | $8.20 | ~$28 |
| 3. C breadth | 9 brands (danskvand/energidrikke/RTD) x 5 reps, `--scenarios C` | 45 | $0.31 | ~$0.50 |
| | | **111** | **~$11** | **~$40** |

Realistic figures apply the surcharge to A and B only, per F1.

### Block 1 — the A floor
```
--full --categories CSD --brands HARBOE COCA_COLA --repeats 3 \
  --scenarios A --budget 20
```
Reuses the pilot's two brands so the existing A data is comparable. Closes the
unmeasured Coca Cola `A_plain` cell noted in PLANS_INDEX.

### Block 2 — the statistically serious block
```
--full --categories CSD --brand-strategy stratified --brands-per-cat 3 \
  --repeats 10 --scenarios B,C --budget 60
```
HARBOE / NIKOLINE / VOELKEL — ranks 1, 41 and 76 of 76 scorable CSD brands.
This is the block that produces the confidence interval.

### Block 3 — generalisation for pocket change
```
--full --categories danskvand energidrikke RTD --brand-strategy stratified \
  --brands-per-cat 3 --repeats 5 --scenarios C --budget 5
```
Answers "does it generalise beyond CSD?" without paying for A or B outside CSD.

## Why single-category for the full ladder

SRQ4's independent variable is **the mechanism by which a forecast is produced**
(own code vs. served model), not the product category. Category variation is
SRQ1's question (single vs. pooled). Running the full ladder on four categories
would multiply cost ~4x to vary a factor that is not under test.

Volume, volatility and data density — the properties that actually determine
whether a forecasting advantage survives — are varied **within** CSD by the
stratified selection (ranks 1, 41, 76). Block 3 then checks the served-model arm
across all four categories directly.

**Limitation to state in Ch3 and Ch9:** the full three-scenario ladder is
established on one category. Cross-category evidence exists for `C_model` only.

## Budget cap discipline

Set `--budget` per block, at roughly 2x the block estimate. A cap that fires
mid-block leaves an unbalanced factorial, which is worse than a smaller balanced
one (this happened on 2026-08-19: the cap stopped the Coca Cola `A_plain` re-run).
Run `--dry-run` before each block.

## Not yet decided — D/E

D/E repeat counts are **deliberately not frozen here**, because `D_prometheus`
runs an E2B sandbox whose per-run cost is unmeasured (F6). Run
`measure_e2b_cost.py` first, then freeze D/E scope in a follow-up section of this
file. P0042 gate 1 requires D/E scope committed before B2 runs.

Note the tension to resolve then: P0042 says D/E should match A/B/C's scope so
D->E and B->C stay comparable. A/B/C is now 3 brands x 10 reps for B/C, not the
pilot's 2 x 3. **D/E should match the B/C core block (3 brands x 10 reps) if E2B
cost permits** — decide against the measured number.

## How this is reported (fixed wording)

In Ch3 methodology, as a design choice:

> Sampling was allocated inversely to per-run cost. Measured pilot costs differ
> by a factor of ~63 between the plain-LLM and served-model scenarios, so equal
> allocation would have concentrated the budget on the arm whose result was least
> in doubt. Repeats were therefore concentrated on the contested B->C increment
> (n=10, sized for 80% power against the observed 3.5pp gap), the A floor was
> established at n=3 where the observed gap of 17.8pp is large relative to any
> plausible sampling error, and generalisation across categories was tested on
> the near-zero-cost served-model arm.

In Ch9 limitations:

> The full three-scenario ladder was run on a single product category, and the
> plain-LLM scenario at n=3. Both follow from per-run cost differences rather
> than from a methodological preference; a larger budget would widen the ladder
> to all four categories and raise n uniformly. The served-model arm was tested
> across all four categories.

**Do not write "we could not afford more."** Same facts, weaker framing.
