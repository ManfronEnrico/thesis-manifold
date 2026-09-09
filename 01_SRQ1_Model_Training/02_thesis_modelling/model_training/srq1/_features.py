"""
The SRQ1 modelling feature set — defined ONCE.
=============================================

Every SRQ1 script used to carry its own `FEATURES = [...]` literal. Eleven live
copies, and they had **already drifted**: `srq1_pooled.py` was missing
`promo_intensity`, so the pooled-vs-per-category comparison ran on two different
feature spaces without saying so. That is the comparison's whole point, silently
confounded.

This module is that list, in one place, for the same reason `_horizon.py` owns
the horizon.

WHY THE MATRIX HAS 54 COLUMNS AND THE MODEL USES ~16
-----------------------------------------------------
The gap is not an oversight; most of those columns are unusable by construction.

| Group | n | Why it is excluded |
|---|---|---|
| Identifiers, split, target | 8 | not features (`brand`, `date`, `split`, `sales_units`, ...) |
| Nielsen measures at time *t* | ~28 | **contemporaneous** -- `sales_value`, `promo_units`, `weighted_dist`, the whole `baseline_*` family. At forecast time for month *t* none of these is known. Including them leaks the target's own period |
| Modelling features | ~16 | this module |

Anything derived from month *t* must be shifted before it is usable. That is why
`promo_intensity` is a feature (it is `shift(1 + h - 1)` of the raw ratio) while
`promo_units` is not.

**Adding a raw Nielsen column here is a leak.** Shift it in
`engineer_features()` first, then add the shifted name.

HOLIDAY FEATURES
----------------
`days_in_month`, `n_holidays` and `non_holiday_days` are CONDITIONAL: they exist
only in matrices built from a contract with `holiday_enrichment: true`
(DEC-NO-FALLBACK -- step 3 decides, step 4 applies). `resolve()` intersects
against the matrix, so a script reading an unenriched matrix simply does not see
them, and one reading an enriched matrix does.

They were engineered on 2026-08-18 and measured by `srq1_holiday_ablation.py`,
but were **never added to any FEATURES list** -- so the ablation reported a
benefit the served model could not receive. Retraining alone would not have fixed
that: `available_features()` intersects the literal with the matrix and never
*adds* a column the literal omits (P0049 F31).
"""

from __future__ import annotations

from typing import Iterable, Sequence

# ---------------------------------------------------------------------------
# The feature set, grouped by what each group contributes.
# ---------------------------------------------------------------------------

# Autoregressive history. Names keep their H=1 meaning at every horizon:
# `lag_1` is "the most recent observation available to the forecaster", which is
# shift(3) at H=3. See _horizon.py.
LAGS: tuple[str, ...] = ("lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13")

# Level and volatility over recent windows, shifted so no value from the
# predicted month enters.
ROLLING: tuple[str, ...] = ("rolling_mean_4", "rolling_std_4", "rolling_mean_13")

# Deterministic calendar position. `peak_month` is per-category, measured in
# step 3 rather than assumed.
CALENDAR: tuple[str, ...] = ("month", "quarter", "peak_month")

# CATEGORY CAPABILITY, not a guarantee. Nielsen reports promotion for CSD and
# Energidrikke but not for Danskvand or RTD. Where absent the column is OMITTED,
# never zero-filled -- a constant-zero column asserts "no promotion ran", which
# the data does not support and a model would happily learn from.
PROMO: tuple[str, ...] = ("promo_intensity",)

# Danish holiday calendar. Present only under holiday_enrichment contracts.
HOLIDAY: tuple[str, ...] = ("days_in_month", "n_holidays", "non_holiday_days")

# Intermittency regime, shifted (P0038). A brand two months into a stock-out
# behaves unlike one selling steadily.
INTERMITTENCY: tuple[str, ...] = ("zero_run_flag", "zero_run_length")

#: The canonical wanted-feature list. Order is stable so that a model file, a
#: SHAP plot and a permutation-importance table all index the same way.
FEATURES: tuple[str, ...] = (
    LAGS + ROLLING + CALENDAR + PROMO + HOLIDAY + INTERMITTENCY
)

# Features whose units are sales volume, so they are log-scaled alongside the
# target for the linear model. Counts and flags are NOT in here: log-scaling a
# 0/1 flag or a month number is meaningless.
LOG_SCALE: tuple[str, ...] = LAGS + ROLLING


def resolve(matrix_columns: Iterable[str],
            wanted: Sequence[str] | None = None) -> list[str]:
    """The wanted features this matrix actually has (DEC-DISCOVER-COLUMNS).

    Intersection, never assertion: categories differ in *capability*, not only in
    values, so a fixed list would raise KeyError on exactly the categories that
    lack promotion, or on any matrix built without holiday enrichment.

    Order follows FEATURES, not the matrix, so two categories with the same
    capabilities produce identically-ordered feature vectors.
    """
    cols = set(matrix_columns)
    return [c for c in (FEATURES if wanted is None else wanted) if c in cols]


def describe(matrix_columns: Iterable[str]) -> str:
    """One line naming what resolved and what did not.

    Printed by scripts at run start. A feature set that silently depends on the
    matrix is a feature set someone will eventually misread -- the same reasoning
    as `_horizon.banner()`.
    """
    cols = set(matrix_columns)
    got = resolve(cols)
    missing = [c for c in FEATURES if c not in cols]
    s = f"[features] {len(got)}/{len(FEATURES)} resolved"
    return s + (f"; absent: {', '.join(missing)}" if missing else "")
