**Preprocessing pipeline execution by category and horizon.** Execution record of the Nielsen preprocessing pipeline, taken from the run manifest each run writes. Timings are wall-clock on the development machine and are reported to evidence that every step ran, not as a performance benchmark.

| Category     |   Horizon (months) | Step 0   | Step 1   | Step 2   |   Step 3 |   Step 4 |   Step 5 |   Step 6 |   Total (s) | All steps passed   |
|:-------------|-------------------:|:---------|:---------|:---------|---------:|---------:|---------:|---------:|------------:|:-------------------|
| CSD          |                  1 | 0.0      | 4.5      | 20.6     |      3.9 |      4.1 |      0.1 |      0.1 |        33.3 | yes                |
| CSD          |                  3 | skipped  | skipped  | skipped  |      3.9 |      4.1 |      0.1 |      0.1 |         8.2 | yes                |
| Danskvand    |                  1 | 0.0      | 0.5      | 9.1      |      0.3 |      0.5 |      0   |      0.1 |        10.6 | yes                |
| Danskvand    |                  3 | skipped  | skipped  | skipped  |      0.4 |      0.4 |      0   |      0.1 |         0.9 | yes                |
| Energidrikke |                  1 | 0.0      | 2.4      | 14.5     |      1.4 |      1.6 |      0   |      0.1 |        20   | yes                |
| Energidrikke |                  3 | skipped  | skipped  | skipped  |      1.9 |      1.6 |      0   |      0.1 |         3.7 | yes                |
| RTD          |                  1 | 0.0      | 2.3      | 15.3     |      1.9 |      1.8 |      0   |      0.1 |        21.4 | yes                |
| RTD          |                  3 | skipped  | skipped  | skipped  |      1.7 |      2.1 |      0   |      0.1 |         3.9 | yes                |

*Note.* Cell values are elapsed seconds for that step. step 0 — validate cache; step 1 — load and aggregate; step 2 — descriptive EDA; step 3 — derive contract; step 4 — engineer features; step 5 — apply split; step 6 — save outputs. An em dash marks a step outside the range of that run; "skipped" marks a horizon-independent step deliberately not repeated on a second horizon (steps 0-2 build the same panel regardless of horizon).

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Generated from run_manifest.json across 4 of 4 categories (8 runs), written 2026-09-07. Regenerate by re-running run_preprocessing.py; the manifest merges horizons rather than overwriting, so H=1 and H=3 accumulate. A category absent here has simply not been re-run since the manifest was added (P0046 F20) -- it is not evidence of a failure. 12 skipped step(s) present.
