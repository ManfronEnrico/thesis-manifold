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
DEFAULT_HOLIDAY_MONTHS: frozenset[int] = frozenset({1, 4, 6, 10, 12})
DEFAULT_TARGET_MARKET: str = "DVH EXCL. HD"
DEFAULT_MIN_PERIODS: int = 30
DEFAULT_TRAIN_END: tuple[int, int] = (2025, 2)   # inclusive
DEFAULT_VAL_END: tuple[int, int] = (2025, 8)     # inclusive


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


def make_calendar(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """
    Add a datetime 'date' column and ensure every brand has the full month
    calendar (fill gaps with 0 for sales, ffill/bfill for distribution).
    Clips negative sales (returns/corrections) to 0.

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
    all_brands = df["brand"].unique()

    idx = pd.MultiIndex.from_product(
        [all_brands, all_dates], names=["brand", "date"]
    )
    full = pd.DataFrame(index=idx).reset_index()
    full = full.merge(
        df.drop(columns=["period_year", "period_month"]),
        on=["brand", "date"], how="left",
    )

    sales_cols = ["sales_units", "sales_value", "sales_liters", "promo_units"]
    full[sales_cols] = full[sales_cols].fillna(0)
    full["weighted_dist"] = (
        full.groupby("brand")["weighted_dist"]
        .transform(lambda s: s.replace(0, np.nan).ffill().bfill().fillna(0))
    )

    for c in sales_cols:
        full[c] = full[c].clip(lower=0)

    full = full.sort_values(["brand", "date"]).reset_index(drop=True)
    return full, all_dates


def filter_series(
    df: pd.DataFrame,
    min_periods: int = DEFAULT_MIN_PERIODS,
    target_col: str = DEFAULT_TARGET_COL,
) -> pd.DataFrame:
    """Keep only brands with >= min_periods of non-zero target observations."""
    nonzero = df.groupby("brand")[target_col].apply(lambda s: (s > 0).sum())
    keep = nonzero[nonzero >= min_periods].index
    return df[df["brand"].isin(keep)].copy()


def engineer_features(
    df: pd.DataFrame,
    target_col: str = DEFAULT_TARGET_COL,
    lags: Iterable[int] = DEFAULT_LAGS,
    rolling_windows: Iterable[int] = DEFAULT_ROLLING_WINDOWS,
    holiday_months: Iterable[int] = DEFAULT_HOLIDAY_MONTHS,
) -> pd.DataFrame:
    """
    Add time-series features per brand:
      - autoregressive lags
      - rolling mean/std (with shift(1) — no look-ahead)
      - calendar (month, quarter, holiday_month)
      - promo intensity
      - log target

    Leakage analysis: every transformation here is either deterministic
    (calendar, promo ratio, log) or uses only the past within each group
    (lags via shift, rolling via shift(1)). Therefore the function is safe
    to apply on the full frame before train/val/test split.
    """
    df = df.sort_values(["brand", "date"]).copy()
    g = df.groupby("brand")

    # Autoregressive lags
    for lag in lags:
        df[f"lag_{lag}"] = g[target_col].shift(lag)

    # Rolling statistics on shifted series (avoids leakage of t into t)
    holiday_set = set(holiday_months)
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
    df["holiday_month"] = df["month"].isin(holiday_set).astype(int)

    # Promo intensity (clip to [0, 1])
    df["promo_intensity"] = np.where(
        df["sales_units"] > 0,
        df["promo_units"] / df["sales_units"].clip(lower=1),
        0,
    ).clip(0, 1)

    # Log-transformed target
    df["log_sales_units"] = np.log1p(df["sales_units"])

    return df


def apply_split(
    df: pd.DataFrame,
    train_end: tuple[int, int] = DEFAULT_TRAIN_END,
    val_end: tuple[int, int] = DEFAULT_VAL_END,
) -> pd.DataFrame:
    """Label rows with split = 'train' | 'val' | 'test' based on date cutoffs."""
    df = df.copy()
    train_cutoff = pd.Timestamp(f"{train_end[0]}-{train_end[1]:02d}-01")
    val_cutoff = pd.Timestamp(f"{val_end[0]}-{val_end[1]:02d}-01")
    conditions = [
        df["date"] <= train_cutoff,
        (df["date"] > train_cutoff) & (df["date"] <= val_cutoff),
    ]
    df["split"] = np.select(conditions, ["train", "val"], default="test")
    return df


def build_series_index(df: pd.DataFrame) -> pd.DataFrame:
    """Per-brand summary: how many periods, splits, total sales."""
    return (
        df.groupby("brand")
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
    holiday_months: frozenset[int] = DEFAULT_HOLIDAY_MONTHS
    min_periods: int = DEFAULT_MIN_PERIODS
    train_end: tuple[int, int] = DEFAULT_TRAIN_END
    val_end: tuple[int, int] = DEFAULT_VAL_END

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
        df, _ = make_calendar(brand_month_df)
        df = filter_series(df, self.min_periods, self.target_col)
        df = engineer_features(
            df,
            target_col=self.target_col,
            lags=self.lags,
            rolling_windows=self.rolling_windows,
            holiday_months=self.holiday_months,
        )
        df = apply_split(df, self.train_end, self.val_end)
        return df

    def fit_transform(self, brand_month_df: pd.DataFrame) -> pd.DataFrame:
        self.fit(brand_month_df)
        return self.transform(brand_month_df)


# ── Persistence helpers ───────────────────────────────────────────────────────


def save_feature_matrix(
    df: pd.DataFrame,
    output_dir: Path,
    series_idx: pd.DataFrame | None = None,
) -> dict[str, Path]:
    """
    Save feature matrix and series index to disk under output_dir/.
    Returns dict of written paths for downstream agents (ForecastingAgent).
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fm_path = output_dir / "feature_matrix.parquet"
    df.to_parquet(fm_path, index=False)

    paths = {"feature_matrix": fm_path}
    if series_idx is not None:
        si_path = output_dir / "series_index.csv"
        series_idx.to_csv(si_path, index=False)
        paths["series_index"] = si_path
    return paths


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
