# Archived per-category preprocessing scripts

Archived 2026-08-18.

These are the **superseded** per-category pipeline scripts. They are kept for
reference, not for running.

## Why they were replaced

Each category had its own near-identical copy of the same 7 steps, which meant a
fix applied to one category silently failed to reach the other three. Two
concrete consequences:

- A defect in the CSD notebook (`df['promo_units']` guarded by an `.empty` check,
  which tests for zero rows rather than a missing column) meant three of four
  categories produced no EDA at all.
- `{Category}_HOLIDAY_MONTHS` was copied verbatim across all three non-CSD
  scripts as `{1, 4, 6, 10, 12}`, under a category-prefixed name that made an
  inherited constant look like a measurement. Danskvand peaks in summer
  (June-September); its script asserted January. On current data three of those
  five months are **below** average for CSD.

The replacement is a single shared pipeline in `_shared_modules/`, which
discovers what each category has rather than assuming, and takes its parameters
from a per-category contract JSON derived in step 3.

## Do not run these

They still contain the stale constants described above. They are superseded by:

    _shared_modules/step_0_validate_cache.py
    _shared_modules/step_1_load_and_aggregate.py
    _shared_modules/step_2_eda_descriptive.py
    _shared_modules/step_3_derive_params.py
    ... and the remaining steps as they land

## When these can be deleted

After the shared pipeline is verified end-to-end for all four categories
(P0038 task 23, the parity check). They are the baseline that check compares
against, so they must survive until it passes. Deletion is task 24.
