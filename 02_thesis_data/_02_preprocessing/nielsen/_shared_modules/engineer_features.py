"""
Feature Engineering Module — System A
======================================
Single source of truth for feature engineering used by both:
  - DataAssessmentAgent (LangGraph node, in-memory pipeline)
  - thesis/data/preprocessing/combined_scripts/preprocessing.py (CLI batch)

Design contract:
  - Pure functions (lag/rolling/calendar/promo/log) take and return DataFrames.
    They are deterministic and have no fittable state (no scalers, no encoders).
    Hence they are leakage-safe by construction: applying them to train+val+test
    together does NOT leak future information into the past.
  - The FeatureEngineer class wraps these functions in a sklearn-style
    fit/transform interface. Today fit() is a no-op. The shape exists so future
    additions (scalers, encoders, target encoding) can be fit on train only and
    transformed on val/test without duplication.

Author: System A integration (2026-04-23) — refactored from preprocessing.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


# ── Defaults (match preprocessing.py constants) ──────────────────────────────
DEFAULT_TARGET_COL: str = "sales_units"
DEFAULT_LAGS: tuple[int, ...] = (1, 2, 3, 4, 8, 13)
DEFAULT_ROLLING_WINDOWS: tuple[int, ...] = (4, 13)
# REMOVED 2026-08-18: there was a DEFAULT_HOLIDAY_MONTHS = {1, 4, 6, 10, 12}
# here. It was measured on an early CSD extract and never revisited, and on the
# current data three of its five months are BELOW average for CSD (January
# -26.6%, October -16.0%, April -9.2%) -- it flagged the weakest months of the
# year as high season.
#
# Worse, it had been copied verbatim into all three non-CSD per-category
# scripts under category-prefixed names (Danskvand_HOLIDAY_MONTHS,
# Energidrikke_HOLIDAY_MONTHS, RTD_HOLIDAY_MONTHS), which made an inherited
# constant look like a per-category measurement. Danskvand actually peaks in
# summer (June-September); its script claimed January.
#
# There is no correct default, because seasonality is a property of the
# category, so `peak_months` is now a REQUIRED argument. Step 3 measures it
# per category and writes it to the contract; step 4 passes it through.
DEFAULT_TARGET_MARKET: str = "DVH EXCL. HD"
# REMOVED 2026-08-18: there was a DEFAULT_MIN_PERIODS = 30 here. It was a THIRD
# live value for the same threshold -- the notebook used 40, this module 30 --
# and none was derived. MIN_PERIODS is not a free parameter: it follows from the
# feature specification as warmup + horizon + 1, so it is 15 at horizon 1 and 17
# at horizon 3. Any fixed default is therefore wrong at one of the two horizons
# this project reports.
#
# `min_periods` is now a REQUIRED argument of filter_series(). Step 3 derives it
# per horizon and writes it to the contract (DEC-MINPERIODS / DEC-CONTRACT).

# Split sizing is PROPORTIONAL, not calendar-fixed. Each category's panel
# starts at a different month and grows every time the warehouse is refreshed,
# so any fixed cutoff silently redistributes rows on every re-pull: newly
# arrived months all land in whichever split is defined as "the remainder".
# Measured on the 2026-07 extract, the two previous fixed schemes had drifted to
#   fixed dates  (2025-02 / 2025-08): CSD 63/13/24, RTD 59/15/27
#   fixed counts (train=24, val=6)  : CSD 52/13/35, RTD 59/15/27
# against an intended 70/15/15. Proportions hold the ratio steady as the panel
# grows and make categories comparable to each other, which SRQ1's cross-category
# ranking depends on.
DEFAULT_TRAIN_FRAC: float = 0.70
DEFAULT_VAL_FRAC: float = 0.15
# test takes the remainder (~0.15) so the three always sum to exactly 1.

# Retained ONLY to reproduce splits published before 2026-08-12. Passing these
# to apply_split() as train_end/val_end restores the old fixed-date behaviour.
LEGACY_TRAIN_END: tuple[int, int] = (2025, 2)   # inclusive
LEGACY_VAL_END: tuple[int, int] = (2025, 8)     # inclusive


# ── Pure functions ────────────────────────────────────────────────────────────


def _get_facts_columns(conn, category: str) -> set[str]:
    """Return the set of columns available in dbo.{category}_clean_facts_v."""
    cur = conn.cursor()
    cur.execute(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_NAME = ? AND TABLE_SCHEMA = 'dbo'",
        f"{category}_clean_facts_v",
    )
    return {row[0] for row in cur.fetchall()}


def aggregate_brand_month_from_db(
    category: str,
    conn,
    target_market: str = DEFAULT_TARGET_MARKET,
) -> pd.DataFrame:
    """
    Pull facts × dim_product × dim_period × dim_market from Nielsen Fabric for
    the given category (csd, danskvand, energidrikke, rtd, totalbeer) and
    aggregate to (brand, period_year, period_month) for the target market.

    Output schema matches aggregate_brand_month_from_csvs() so downstream
    feature engineering is category-agnostic. Distribution metric is
    weighted_distribution averaged across products.

    Schema differences across categories (e.g. danskvand has no
    sales_units_any_promo) are handled by checking column existence first
    and substituting 0 for missing columns.

    Use this in preference to the CSV path for the 4 new categories — their
    exported dim_product CSVs are incomplete (60–100% orphan rates).
    """
    # SCOPE ASSERT (P0032, 2026-08-01): the query below filters
    # `WHERE m.market_description = '{target_market}'` on a JOINed dim_market.
    # If two market_ids share that description the JOIN fans out and every
    # SUM() silently double-counts -- the same 6.16x defect the CSV path's
    # assert guards, reached through the JOIN rather than an isin() list.
    # Checked up-front so the failure is loud and precedes the expensive query.
    _mkt_cur = conn.cursor()
    _mkt_cur.execute(
        f"SELECT market_id FROM dbo.{category}_clean_dim_market_v "
        "WHERE market_description = ?",
        target_market,
    )
    _market_ids = [r[0] for r in _mkt_cur.fetchall()]
    if len(_market_ids) == 0:
        raise ValueError(
            f"Target market {target_market!r} not found in "
            f"dbo.{category}_clean_dim_market_v."
        )
    if len(_market_ids) > 1:
        raise ValueError(
            f"Target market {target_market!r} resolves to {len(_market_ids)} "
            f"market_ids ({_market_ids}) in dbo.{category}_clean_dim_market_v, "
            "expected exactly 1. The market_description JOIN below would fan "
            "out and double-count every aggregate. Disambiguate first."
        )

    available = _get_facts_columns(conn, category)
    promo_expr = (
        "SUM(COALESCE(f.sales_units_any_promo, 0))"
        if "sales_units_any_promo" in available
        else "0"
    )
    sales_value_col = "sales_value" if "sales_value" in available else "0"
    sales_liters_col = (
        "sales_in_liters" if "sales_in_liters" in available else "0"
    )
    weighted_dist_expr = (
        "AVG(COALESCE(f.weighted_distribution, 0))"
        if "weighted_distribution" in available
        else "0"
    )

    sql = f"""
    SELECT
        p.brand,
        t.period_year,
        t.period_month,
        SUM(f.sales_units)              AS sales_units,
        SUM(f.{sales_value_col})        AS sales_value,
        SUM(f.{sales_liters_col})       AS sales_liters,
        {promo_expr}                    AS promo_units,
        {weighted_dist_expr}            AS weighted_dist
    FROM dbo.{category}_clean_facts_v f
    JOIN dbo.{category}_clean_dim_product_v p ON f.product_id = p.product_id
    JOIN dbo.{category}_clean_dim_period_v  t ON f.period_id  = t.period_id
    JOIN dbo.{category}_clean_dim_market_v  m ON f.market_id  = m.market_id
    WHERE m.market_description = '{target_market}'
      AND f.sales_units > 0
    GROUP BY p.brand, t.period_year, t.period_month
    ORDER BY p.brand, t.period_year, t.period_month
    """
    cur = conn.cursor()
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    return pd.DataFrame([list(r) for r in rows], columns=cols)


def aggregate_brand_month_from_csvs(
    csv_dir: Path,
    target_market: str = DEFAULT_TARGET_MARKET,
) -> pd.DataFrame:
    """
    Read the 4 CSD CSVs (facts + 3 dim) and aggregate to (brand, period_year,
    period_month) for the given target market. Equivalent in pandas to the SQL
    JOIN+GROUP BY in aggregate_brand_month_from_db().

    Returns columns: brand, period_year, period_month, sales_units, sales_value,
    sales_liters, promo_units, weighted_dist.

    Note: only CSD has a complete CSV-exported dim_product. For the 4 new
    categories use aggregate_brand_month_from_db() — their CSV dims are
    incomplete (60–100% orphan rates).
    """
    csv_dir = Path(csv_dir)
    facts = pd.read_csv(csv_dir / "csd_clean_facts_v.csv", low_memory=False)
    dim_market = pd.read_csv(csv_dir / "csd_clean_dim_market_v.csv")
    dim_period = pd.read_csv(csv_dir / "csd_clean_dim_period_v.csv")
    # dim_product CSV has unquoted commas inside product names (e.g. "0,75 L").
    # Use python engine with on_bad_lines='skip' to recover; the dropped rows
    # are <0.5% and only affect product metadata, not the facts series.
    dim_product = pd.read_csv(
        csv_dir / "csd_clean_dim_product_v.csv",
        engine="python",
        on_bad_lines="skip",
    )

    # Filter market = target_market (e.g. "DVH EXCL. HD")
    market_match = dim_market[dim_market["market_description"] == target_market]
    if market_match.empty:
        available = sorted(dim_market["market_description"].dropna().unique())
        raise ValueError(
            f"Target market {target_market!r} not found. "
            f"Available: {available[:10]}{'...' if len(available) > 10 else ''}"
        )
    target_market_ids = market_match["market_id"].tolist()
    # SCOPE ASSERT (P0032, 2026-08-01): fail loudly on a multi-id market.
    # The empty case is handled above; the >1 case previously fell through
    # silently and would sum the same brand-month across several market rows,
    # reintroducing the 6.16x double-count this filter exists to prevent.
    if len(target_market_ids) > 1:
        raise ValueError(
            f"Target market {target_market!r} resolves to "
            f"{len(target_market_ids)} market_ids ({target_market_ids}), "
            "expected exactly 1. Aggregating across them would double-count "
            "every brand-month. Disambiguate the market before proceeding."
        )
    facts = facts[facts["market_id"].isin(target_market_ids)]

    # Drop zero/null sales_units (matches WHERE f.sales_units > 0)
    facts = facts[facts["sales_units"].fillna(0) > 0]

    # Join with dim_period (brand, year, month) and dim_product (brand)
    facts = facts.merge(
        dim_period[["period_id", "period_year", "period_month"]],
        on="period_id", how="left",
    )
    facts = facts.merge(
        dim_product[["product_id", "brand"]],
        on="product_id", how="left",
    )

    # Aggregate: sum sales metrics, average distribution
    grouped = (
        facts
        .dropna(subset=["brand", "period_year", "period_month"])
        .groupby(["brand", "period_year", "period_month"], as_index=False)
        .agg(
            sales_units=("sales_units", "sum"),
            sales_value=("sales_value", "sum"),
            sales_liters=("sales_in_liters", "sum"),
            promo_units=("sales_units_any_promo", lambda s: s.fillna(0).sum()),
            weighted_dist=("weighted_distribution", lambda s: s.fillna(0).mean()),
        )
        .sort_values(["brand", "period_year", "period_month"])
        .reset_index(drop=True)
    )
    return grouped


def make_calendar(
    df: pd.DataFrame,
    group_keys: list[str] = ["brand"],
) -> tuple[pd.DataFrame, list]:
    """
    Add a datetime 'date' column and ensure every group (default: each brand)
    has the full month calendar (fill gaps with 0 for sales, ffill for
    distribution). Clips negative sales (returns/corrections) to 0.

    Two distinct leakage risks are guarded here — they are easy to conflate:

    1. CROSS-GROUP leakage (handled by group_keys). Without grouping, ffill
       carries the last row of series A into the first gap of series B.
       group_keys identifies a distinct series: default ["brand"] matches
       brand×month grain; pass e.g. ["brand", "market_id"] for a region/chain
       grain so the calendar cross-product and the ffill don't mix rows.

    2. FUTURE leakage WITHIN a series (handled by not calling bfill). An
       earlier version chained .ffill().bfill(); the bfill filled leading gaps
       — months before a brand's first observation — with the brand's FIRST
       OBSERVED value, i.e. a fact from the future. Such a row cannot be
       constructed at forecast time, so a model trained on it is scored on
       information it would not have in production. Leading gaps now fill 0,
       which is also the truthful value: the brand was not yet distributed.

    Guard 1 was documented from the start; guard 2 was not, which is why the
    bfill survived review. Keep both documented.

    Returns: (filled_df, sorted list of unique dates).
    """
    df = df.copy()
    df["date"] = pd.to_datetime(
        df["period_year"].astype(int).astype(str)
        + "-"
        + df["period_month"].astype(int).astype(str).str.zfill(2)
        + "-01"
    )
    all_dates = sorted(df["date"].unique())
    group_values = df[group_keys].drop_duplicates()

    idx_frames = []
    for _, row in group_values.iterrows():
        block = pd.DataFrame({"date": all_dates})
        for key in group_keys:
            block[key] = row[key]
        idx_frames.append(block)
    idx = pd.concat(idx_frames, ignore_index=True)

    full = idx.merge(
        df.drop(columns=["period_year", "period_month"]),
        on=group_keys + ["date"], how="left",
    )

    # Only the columns actually present are filled. An earlier version listed
    # these four unconditionally and raised KeyError on any category lacking
    # one -- Danskvand and RTD have no promo_units at all, because Nielsen does
    # not report promotion for them, so this function worked on exactly the two
    # categories it had been tested against (P0038, 2026-08-18).
    #
    # Zero-fill is correct for every column named here on the same grounds as
    # the ffill note below: in a month with no observation the brand recorded no
    # sales, no value, no volume and no promoted units. That is a measurement,
    # not a gap to be imputed.
    CANDIDATE_SALES_COLS = ["sales_units", "sales_value", "sales_liters", "promo_units"]
    sales_cols = [c for c in CANDIDATE_SALES_COLS if c in full.columns]
    full[sales_cols] = full[sales_cols].fillna(0)
    # ffill only -- NO bfill. bfill would pull a FUTURE distribution value
    # backward into a leading gap, encoding information that did not exist at
    # that date. Leading gaps (months before a brand's first observation) fill
    # with 0, which is also the truthful value: the brand was not distributed.
    # Measured on CSD at parent scope: bfill contaminated 1,176 rows (19.1% of
    # the calendar) across 51 brands, every one of them a leading gap.
    if "weighted_dist" in full.columns:
        full["weighted_dist"] = (
            full.groupby(group_keys)["weighted_dist"]
            .transform(lambda s: s.replace(0, np.nan).ffill().fillna(0))
        )

    for c in sales_cols:
        full[c] = full[c].clip(lower=0)

    # Restore the panel's canonical period columns. They are dropped above so
    # the merge keys on `date` alone, but steps 1-3 and every contract express
    # a period as (period_year, period_month), and a downstream consumer should
    # not have to re-derive from `date` what the panel already had. Rebuilt
    # from `date` rather than merged back, so calendar-filled rows -- which had
    # no source row -- also carry correct values.
    full["period_year"] = full["date"].dt.year
    full["period_month"] = full["date"].dt.month

    full = full.sort_values(group_keys + ["date"]).reset_index(drop=True)
    return full, all_dates


def filter_series(
    df: pd.DataFrame,
    min_periods: int,
    target_col: str = DEFAULT_TARGET_COL,
    group_keys: list[str] = ["brand"],
) -> pd.DataFrame:
    """
    Keep only groups (default: brands) with >= min_periods of non-zero target
    observations.

    group_keys: see make_calendar(). Filtering by ["brand"] alone when the grain
    is actually brand×region would let a brand pass the threshold on periods
    summed across all regions, even if no single region-series meets it.
    """
    nonzero = df.groupby(group_keys)[target_col].apply(lambda s: (s > 0).sum())
    keep_df = nonzero[nonzero >= min_periods].index.to_frame(index=False)
    return df.merge(keep_df, on=group_keys, how="inner").copy()


def engineer_features(
    df: pd.DataFrame,
    target_col: str = DEFAULT_TARGET_COL,
    lags: Iterable[int] = DEFAULT_LAGS,
    rolling_windows: Iterable[int] = DEFAULT_ROLLING_WINDOWS,
    group_keys: list[str] = ["brand"],
    *,
    peak_months: Iterable[int],
) -> pd.DataFrame:
    """
    Add time-series features per group (default: per brand):
      - autoregressive lags
      - rolling mean/std (with shift(1) — no look-ahead)
      - calendar (month, quarter, peak_month)
      - promo intensity
      - log target

    group_keys: see make_calendar(). Lags/rolling stats use shift() within each
    group — grouping by "brand" alone when the true grain is brand×region would
    let lag_1 for brand X at region A silently pick up brand X's prior-month
    value from region B, since rows would only be sorted by (brand, date).

    Leakage analysis: every transformation here is either deterministic
    (calendar, promo ratio, log) or uses only the past within each group
    (lags via shift, rolling via shift(1)). Therefore the function is safe
    to apply on the full frame before train/val/test split.
    """
    df = df.sort_values(group_keys + ["date"]).copy()
    g = df.groupby(group_keys)

    # Autoregressive lags
    for lag in lags:
        df[f"lag_{lag}"] = g[target_col].shift(lag)

    # Rolling statistics on shifted series (avoids leakage of t into t)
    peak_set = set(peak_months)
    for w in rolling_windows:
        df[f"rolling_mean_{w}"] = (
            g[target_col]
            .shift(1)
            .transform(lambda s: s.rolling(w, min_periods=max(2, w // 4)).mean())
        )
        if w == 4:  # match preprocessing.py: only window=4 has std
            df[f"rolling_std_{w}"] = (
                g[target_col]
                .shift(1)
                .transform(lambda s: s.rolling(w, min_periods=2).std().fillna(0))
            )

    # Calendar features
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["peak_month"] = df["month"].isin(peak_set).astype(int)

    # Promo intensity (clip to [0, 1]), lagged one period.
    #
    # LEAKAGE FIX (P0032, 2026-08-01): the ratio is computed from realised
    # sales_units at t, which is the target's own denominator -- at forecast
    # time for month t, sales_units_t is unknown, so the contemporaneous value
    # is unconstructible. It is shifted by one period to match every other
    # feature in this function (lags at shift(lag), rolling at shift(1)).
    #
    # The shift is applied WITHIN group_keys: a bare shift(1) on a frame sorted
    # by (brand, date) would carry the last row of one series into the first row
    # of the next -- cross-series leakage. The ratio is formed first and then
    # shifted (rather than shifting promo_units/sales_units separately) so the
    # result is unambiguously "last period's promo intensity" even when an
    # intervening month has zero sales.
    #
    # The first observation of each series is NaN, exactly as for lag_1;
    # downstream consumers already fillna(0.0) at feature-selection time.
    # promo_units is a CATEGORY CAPABILITY, not a guaranteed column: Nielsen
    # reports promotion for CSD and Energidrikke but not for Danskvand or RTD.
    # Where it is absent the feature is OMITTED rather than zero-filled -- a
    # zero column would assert "no promotion ran", which is a factual claim the
    # data does not support and which a model would happily learn from. An
    # absent feature is honest; a constant-zero feature is a fabrication.
    #
    # Downstream consumers must therefore select features from what the matrix
    # contains rather than from a fixed list. This is the same open-world rule
    # the pipeline applies to measures generally (DEC-OPEN-WORLD).
    if "promo_units" in df.columns:
        _promo_intensity_t = pd.Series(
            np.where(
                df["sales_units"] > 0,
                df["promo_units"] / df["sales_units"].clip(lower=1),
                0,
            ).clip(0, 1),
            index=df.index,
        )
        df["promo_intensity"] = _promo_intensity_t.groupby(
            [df[k] for k in group_keys]
        ).shift(1)

    # Intermittency (restored from the archived notebook, P0038, 2026-08-18).
    #
    # The notebook computed these UNSHIFTED -- zero_run_flag was exactly
    # (sales_units == 0) at time t, i.e. a function of the target itself.
    # Verified 100.00% identical on the preserved baseline. It went unnoticed
    # because that matrix had 0 zero-rows (regional scope dropped them); the
    # current parent-scope matrix has 588 (13.5%), so the same code would now
    # leak on one row in seven.
    #
    # The signal is genuine -- intermittent demand is a distinct forecasting
    # regime, and a brand two months into a stock-out behaves unlike one that is
    # selling steadily. So it is kept, but shifted by one period within
    # group_keys, matching promo_intensity above: at time t these describe
    # t-1, which a forecaster actually knows.
    _is_zero = (df["sales_units"] == 0).astype("int8")
    _grouped = _is_zero.groupby([df[k] for k in group_keys])

    # Run length: cumulative count of consecutive zeros, reset by any non-zero.
    # cumsum() over the non-zero mask gives a run id; counting within it gives
    # the length; multiplying by _is_zero zeroes out the non-zero rows.
    _run_id = (1 - _is_zero).groupby([df[k] for k in group_keys]).cumsum()
    _run_len = _is_zero.groupby(
        [df[k] for k in group_keys] + [_run_id]
    ).cumsum() * _is_zero

    df["zero_run_flag"] = _grouped.shift(1)
    df["zero_run_length"] = _run_len.groupby(
        [df[k] for k in group_keys]
    ).shift(1)

    # Log-transformed target
    df["log_sales_units"] = np.log1p(df["sales_units"])

    return df


def resolve_split_cutoffs(
    df: pd.DataFrame,
    train_frac: float = DEFAULT_TRAIN_FRAC,
    val_frac: float = DEFAULT_VAL_FRAC,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Derive (train_end, val_end) as (year, month) from the frame's own periods.

    Cutoffs are positional: the distinct periods present in `df` are sorted
    ascending and cut at round(n * train_frac) and round(n * (train_frac +
    val_frac)). Both returned cutoffs are INCLUSIVE ends, matching the tuple
    form apply_split() accepts, so the result can be logged, persisted to
    {category}_split_dates.json, or passed back in to reproduce the same split.

    Cutting on distinct periods rather than rows is deliberate: brands enter
    and exit the panel, so a row-wise quantile would place the boundary at a
    different month depending on how many brands happened to be active. Every
    series must be cut at the SAME date or the split stops being temporal.

    Raises ValueError if fewer than 3 periods are present (cannot form three
    non-empty splits) or if the fractions are not a valid proportion.
    """
    if not (0 < train_frac < 1 and 0 < val_frac < 1):
        raise ValueError(
            f"train_frac and val_frac must each lie in (0, 1); "
            f"got train_frac={train_frac}, val_frac={val_frac}"
        )
    if train_frac + val_frac >= 1:
        raise ValueError(
            f"train_frac + val_frac must be < 1 to leave a non-empty test "
            f"split; got {train_frac} + {val_frac} = {train_frac + val_frac}"
        )

    periods = sorted({(d.year, d.month) for d in pd.to_datetime(df["date"])})
    n = len(periods)
    if n < 3:
        raise ValueError(
            f"need at least 3 distinct periods to form train/val/test; got {n}"
        )

    n_train = int(round(n * train_frac))
    n_val = int(round(n * val_frac))

    # Clamp so all three splits are non-empty even on short panels, where
    # rounding can otherwise starve val or test.
    n_train = max(1, min(n_train, n - 2))
    n_val = max(1, min(n_val, n - n_train - 1))

    return periods[n_train - 1], periods[n_train + n_val - 1]


def apply_split(
    df: pd.DataFrame,
    train_end: tuple[int, int] | None = None,
    val_end: tuple[int, int] | None = None,
    train_frac: float = DEFAULT_TRAIN_FRAC,
    val_frac: float = DEFAULT_VAL_FRAC,
) -> pd.DataFrame:
    """
    Label rows with split = 'train' | 'val' | 'test'.

    By default the cutoffs are derived PROPORTIONALLY from the periods present
    in `df` (see resolve_split_cutoffs), so the train/val/test ratio stays
    constant as the panel grows and is identical across categories whose panels
    start at different dates.

    Passing explicit `train_end` / `val_end` (year, month) tuples overrides the
    proportional calculation -- use that only to reproduce a previously
    published split (e.g. LEGACY_TRAIN_END / LEGACY_VAL_END). Both must be given
    together; supplying one without the other is ambiguous and raises.

    Cutoffs are inclusive: a row exactly at train_end is train, not val.
    """
    if (train_end is None) != (val_end is None):
        raise ValueError(
            "train_end and val_end must be supplied together (or both omitted "
            "to derive them proportionally); got "
            f"train_end={train_end}, val_end={val_end}"
        )

    if train_end is None:
        train_end, val_end = resolve_split_cutoffs(df, train_frac, val_frac)

    df = df.copy()
    train_cutoff = pd.Timestamp(f"{train_end[0]}-{train_end[1]:02d}-01")
    val_cutoff = pd.Timestamp(f"{val_end[0]}-{val_end[1]:02d}-01")
    if val_cutoff <= train_cutoff:
        raise ValueError(
            f"val_end ({val_end}) must be strictly after train_end "
            f"({train_end}); an empty validation split is never intended"
        )
    conditions = [
        df["date"] <= train_cutoff,
        (df["date"] > train_cutoff) & (df["date"] <= val_cutoff),
    ]
    df["split"] = np.select(conditions, ["train", "val"], default="test")
    return df


def build_series_index(
    df: pd.DataFrame,
    group_keys: list[str] = ["brand"],
) -> pd.DataFrame:
    """
    Per-group summary: how many periods, splits, total sales.

    group_keys: see make_calendar(). Grouping by "brand" alone on a
    brand×region grain silently collapses the region dimension in n_periods/
    total_units — the underlying parquet still retains the extra key, but the
    summary report becomes misleading (e.g. n_periods double-counts across
    regions instead of reporting per-series depth).
    """
    return (
        df.groupby(group_keys)
        .agg(
            n_periods=("date", "count"),
            n_nonzero=("sales_units", lambda s: (s > 0).sum()),
            total_units=("sales_units", "sum"),
            train_periods=("split", lambda s: (s == "train").sum()),
            val_periods=("split", lambda s: (s == "val").sum()),
            test_periods=("split", lambda s: (s == "test").sum()),
        )
        .reset_index()
        .sort_values("total_units", ascending=False)
    )


# ── sklearn-style wrapper class ───────────────────────────────────────────────


@dataclass
class FeatureEngineer:
    """
    Wraps the pure functions above in a sklearn-compatible fit/transform shape.

    Today fit() is a no-op because no transformations require training data
    (lags, rolling, calendar, promo, log are all leakage-safe by construction).
    The class exists so future additions — categorical encoders, standard
    scalers, target encoding — can be fit on train only and applied on val/test
    via the same interface, without rewriting the agent.

    Usage:
        fe = FeatureEngineer()
        fe.fit(brand_month_train_df)           # currently a no-op
        feature_matrix = fe.transform(brand_month_full_df)
    """

    target_col: str = DEFAULT_TARGET_COL
    lags: tuple[int, ...] = DEFAULT_LAGS
    rolling_windows: tuple[int, ...] = DEFAULT_ROLLING_WINDOWS
    # No defaults: both are contract values (DEC-CONTRACT). See the removal
    # notes at the top of this module for why a default is wrong for each.
    # kw_only so they can stay required despite following defaulted fields --
    # and so callers must name them at the call site.
    peak_months: frozenset[int] = field(kw_only=True)
    min_periods: int = field(kw_only=True)
    # None -> apply_split derives cutoffs proportionally from the data. Set both
    # to (year, month) tuples only to reproduce a previously published split.
    train_end: tuple[int, int] | None = None
    val_end: tuple[int, int] | None = None
    train_frac: float = DEFAULT_TRAIN_FRAC
    val_frac: float = DEFAULT_VAL_FRAC
    group_keys: tuple[str, ...] = ("brand",)

    is_fitted: bool = field(default=False, init=False)

    def fit(self, brand_month_df: pd.DataFrame) -> "FeatureEngineer":
        """
        Currently a no-op: every transformation in this module is leakage-safe
        by construction (lags/rolling use shift, calendar/promo/log are
        deterministic). No statistics are learned from training data.

        Method exists so future additions (scalers, encoders, target encoding)
        can be fit on train only and applied to val/test consistently.
        """
        self.is_fitted = True
        return self

    def transform(self, brand_month_df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply the full pipeline: calendar fill → series filter → features → split.

        The series filter (min_periods of nonzero observations) is a data-quality
        gate, not a learned transformation, so it operates on the full frame.
        """
        group_keys = list(self.group_keys)
        df, _ = make_calendar(brand_month_df, group_keys=group_keys)
        df = filter_series(df, self.min_periods, self.target_col, group_keys=group_keys)
        df = engineer_features(
            df,
            target_col=self.target_col,
            lags=self.lags,
            rolling_windows=self.rolling_windows,
            peak_months=self.peak_months,
            group_keys=group_keys,
        )
        df = apply_split(
            df,
            train_end=self.train_end,
            val_end=self.val_end,
            train_frac=self.train_frac,
            val_frac=self.val_frac,
        )
        return df

    def fit_transform(self, brand_month_df: pd.DataFrame) -> pd.DataFrame:
        self.fit(brand_month_df)
        return self.transform(brand_month_df)


# ── Persistence helpers ───────────────────────────────────────────────────────


# save_feature_matrix() was removed here (P0038, 2026-08-18).
#
# It wrote an un-suffixed "feature_matrix.parquet" -- the notebook-era name,
# which carries no horizon and so has no unambiguous referent now that the
# pipeline produces one matrix per horizon. It had no callers in live code (the
# only one in the repo is an archived pre-integration agent), and step 6 owns
# artifact writing.
#
# Deleted rather than deprecated: a dead helper that writes a horizon-ambiguous
# filename invites someone to wire it back up, recreating precisely the stale
# artifact this cleanup removed -- and lending it the authority of a shared
# module.


# ── Pooled feature matrix construction ────────────────────────────────────────


def build_pooled_feature_matrix(
    matrices_by_category: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Concatenate per-category feature matrices into one pooled frame, adding a
    'category' column (categorical). Brands are NOT renamed even if a string
    appears in multiple categories — the (category, brand) pair is the natural
    series identifier in the pooled setting.

    All categories must share the same column schema (which they do when
    produced via aggregate_brand_month_from_db + FeatureEngineer in this
    module). LightGBM consumes 'category' as a categorical feature.
    """
    parts = []
    for cat, df in matrices_by_category.items():
        df = df.copy()
        df["category"] = cat
        parts.append(df)
    pooled = pd.concat(parts, ignore_index=True)
    pooled["category"] = pooled["category"].astype("category")
    # Keep deterministic ordering: by (category, brand, date)
    pooled = pooled.sort_values(
        ["category", "brand", "date"], kind="stable"
    ).reset_index(drop=True)
    return pooled
