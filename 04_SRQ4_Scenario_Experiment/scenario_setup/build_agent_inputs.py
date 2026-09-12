#!/usr/bin/env python3
"""
Build the warehouse-shaped payload handed to the data-access scenarios.

WHY THIS SCRIPT EXISTS
----------------------
The SRQ4 comparison asks whether an agent writing its own analysis can match a
purpose-built forecasting pipeline. That question is only answerable if the
agent is given the data a production agent would actually reach.

Prometheus in production has live access to the Nielsen star schema. Asked this
question, it would join facts to the product, period and market dimensions,
filter to a market, and aggregate to brand-month -- roughly what the modelling
pipeline's step 1 does. What it would NOT have is the EDA, the cleaning, the
imputation, the outlier handling, the split contract or the engineered features.
Those are the proprietary pipeline, and they are the thing SRQ4 measures.

So the payload must sit at exactly one point:

    post-join, post-market-filter, post-brand-month-aggregation,
    PRE cleaning, PRE engineering.

That frame existed NOWHERE on disk. `_01_converted` holds the four un-joined
views. `_03_engineered` holds a frame that already carries the human choices.
Neither is the right handoff, so this script produces the missing state.

Until 2026-09-12 the harness sent FOUR columns -- year, month, units, and a
shifted promo ratio -- sliced off the engineered matrix. Three problems:

  1. It withheld 28 warehouse measures the production agent would hold, which
     made "the agent could not find signal" unfalsifiable: it was never given
     the signal to find.
  2. `promo_intensity` is an ENGINEERED column (a shifted ratio built in
     `engineer_features.py`). Sending it handed over a piece of the pipeline's
     own feature engineering.
  3. It silently asked for `weighted_distribution`, which the engineered matrix
     calls `weighted_dist`, so the column never matched and was dropped without
     an error.

WHAT IS AND IS NOT A HUMAN CHOICE HERE
--------------------------------------
Three choices are unavoidable and all three are declared in the manifest rather
than hidden:

  * MARKET. `DVH EXCL. HD` -- Nielsen's own recommended market, the same one the
    modelling pipeline trains on. The one-id assertion below is what stops a
    multi-id description fanning out the join and double-counting every measure.
  * SKU -> BRAND. The product dimension is UPC-only (every row is hierarchy
    level UPC; there are no BRAND-level rows), so reaching brand-month requires
    summing across SKUs. A production agent would face the same constraint.
  * SUM vs MEAN. Volume measures sum; distribution measures are ACV-weighted
    fractions and percentages of category turnover that are NOT additive across
    products, so they average. This follows the `unit` column of the warehouse's
    own metadata, not a modelling preference.

Everything else is left exactly as the warehouse reports it. In particular:

  * NULLS ARE PRESERVED AS NULLS. No zero-filling anywhere. A zero asserts "this
    was measured and was zero", which the warehouse does not say. The sparsity
    is real, it is part of the data-quality problem the agent is being asked to
    handle, and hiding it would be doing the agent's job for it.
  * No outlier handling, no imputation, no smoothing, no derived columns.

OUTPUT
------
Per brand, into SRQ4_AGENT_INPUTS_DIR / <CATEGORY> / :

    <brand-slug>_brand_month.csv   the series, one row per observed month
    schema_dictionary.csv          the warehouse column dictionary (per category)
    manifest.json                  what was built, from what, with which choices

USAGE
    python build_agent_inputs.py --category CSD
    python build_agent_inputs.py --category CSD --brands HARBOE 7-UP OERBAEK
    python build_agent_inputs.py --category CSD --verify-only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _find_root(start: Path) -> Path:
    """Walk up for the repo anchor rather than counting parents (path-handling)."""
    for d in (start, *start.parents):
        if (d / "PATHS.py").is_file():
            return d
    raise RuntimeError("repo root not found (no PATHS.py above this file)")


ROOT = _find_root(Path(__file__).resolve())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PATHS import (  # noqa: E402
    SRQ4_AGENT_INPUTS_DIR,
    get_category_engineered_bymonth_dir,
    get_category_metadata_dir,
    get_category_views_dir,
)

# The market the modelling pipeline trains on: Nielsen's own recommended
# universe, the most complete and highest quality cut. Kept as the DESCRIPTION,
# not an id, so the one-id assertion below stays meaningful.
TARGET_MARKET = "DVH EXCL. HD"

# Join keys and dimension attributes. `brand` is the aggregation key; the rest
# of dim_product describes a UPC, not a brand, so it cannot survive the
# aggregation and is deliberately not carried.
_FACT_KEYS = ("market_id", "period_id", "product_id")
_PERIOD_COLS = ("period_id", "period_year", "period_month", "period_end_date")

# Distribution and reach measures. ACV-weighted fractions of category turnover
# and store counts -- explicitly NOT additive across products (see the metadata
# for `weighted_distribution`: "NOT additive across products"). They average.
_MEAN_MEASURES = (
    "numeric_distribution",
    "numeric_distribution_reach",
    "weighted_distribution",
    "weighted_distribution_reach",
    "total_weighted_distribution_points_tdp_reach",
    "number_of_items_reach",
    "avg_number_of_stores_selling_reach",
    "universe_number_of_stores",
    "avg_no_of_items_per_store_reach",
    "weighted_distribution_any_promo",
    "weighted_distribution_disp_feat",
    "weighted_distribution_disp_w_o_feat",
    "weighted_distribution_feat_w_o_disp",
    "weighted_distribution_total_feat",
    "weighted_distribution_any_disp",
    "weighted_distribution_any_tpr",
)


def _visible_cutoff(category: str, horizon: int) -> tuple[int, int]:
    """The last month an agent may see: the END OF VALIDATION.

    READ, never recomputed. The boundary is whatever was actually applied when
    the matrix was built, persisted by the pipeline to {cat}_split_dates_h{H}.json.
    Re-deriving it from fractions here would produce a second implementation
    that can disagree with the first, and the disagreement would be invisible.

    Train + validation is the fit window: the served model is fitted on exactly
    those rows, so an agent standing at the same forecasting origin sees exactly
    those rows. Test is never visible to anyone -- not to the model, not to any
    scenario.
    """
    p = (get_category_engineered_bymonth_dir(category)
         / f"{category.lower()}_split_dates_h{horizon}.json")
    if not p.is_file():
        raise SystemExit(
            f"No split boundary for {category} at H={horizon}.\n"
            f"  Expected: {p}\n"
            "  The visible window cannot be guessed -- build the matrix first.")
    val_end = json.loads(p.read_text(encoding="utf-8"))["val_end"]
    y, m = val_end.split("-")[:2]
    return int(y), int(m)


# Danish letters have NO combining-mark decomposition: NFKD leaves Ø and Æ
# whole, so a "strip the combining marks" fold deletes them outright and
# ØRBÆK becomes RB-K. Transliterate them explicitly, the way Danish does.
_TRANSLIT = str.maketrans({
    "Ø": "OE", "ø": "oe", "Æ": "AE", "æ": "ae", "Å": "AA", "å": "aa",
    "Ö": "OE", "ö": "oe", "Ä": "AE", "ä": "ae", "ß": "ss",
})


def _slug(name: str) -> str:
    """Filesystem-safe brand slug. ASCII-folded so Windows and git behave."""
    n = str(name).translate(_TRANSLIT)
    n = unicodedata.normalize("NFKD", n)
    n = "".join(c for c in n if not unicodedata.combining(c))
    out = re.sub(r"[^A-Za-z0-9]+", "-", n).strip("-").upper()
    if not out:
        raise ValueError(
            f"brand {name!r} slugged to an empty string -- it would overwrite "
            "another brand's file. Add its characters to _TRANSLIT.")
    return out


def _resolve_market_id(views: Path, category: str) -> str:
    """The single market_id for TARGET_MARKET, or a loud failure.

    A description resolving to several ids would fan the join out and
    double-count every SUM -- the 6.16x defect the modelling pipeline's own
    scope assertion guards against. Checked before the expensive read.
    """
    dm = pd.read_parquet(views / f"{category.lower()}_clean_dim_market_v.parquet")
    hit = dm[dm["market_description"] == TARGET_MARKET]
    if hit.empty:
        raise SystemExit(
            f"Market {TARGET_MARKET!r} not found in {category} dim_market.\n"
            f"  Available (first 10): "
            f"{sorted(dm['market_description'].dropna().unique())[:10]}"
        )
    # Keys stay in their NATIVE dtype (int64 across all four views). Casting to
    # str here silently broke the pushdown filter with an ArrowNotImplemented
    # "equal has no kernel matching (int64, string)" -- the filter must compare
    # like with like, so the dtype is never coerced on the way in.
    ids = hit["market_id"].unique().tolist()
    if len(ids) != 1:
        raise SystemExit(
            f"Market {TARGET_MARKET!r} resolves to {len(ids)} market_ids "
            f"({ids}). The join would fan out and double-count every measure. "
            "Disambiguate before building."
        )
    return ids[0]


def _brand_product_ids(views: Path, category: str, brand: str) -> tuple[list[str], int]:
    """UPC product_ids for one brand, plus the number of distinct SKUs.

    Brand-first is what keeps this tractable: the facts view is ~10.3M rows and
    767MB, and filtering it by a product_id set avoids materialising the lot.
    """
    dp = pd.read_parquet(
        views / f"{category.lower()}_clean_dim_product_v.parquet",
        columns=["product_id", "brand"],
    )
    hit = dp[dp["brand"].astype(str).str.upper() == brand.upper()]
    if hit.empty:
        avail = sorted(dp["brand"].dropna().astype(str).unique())
        raise SystemExit(
            f"Brand {brand!r} not found in {category} dim_product.\n"
            f"  {len(avail)} brands available, e.g. {avail[:8]}"
        )
    # Native dtype, for the same reason as the market id above.
    ids = hit["product_id"].unique().tolist()
    return ids, len(ids)


def build_brand_month(category: str, brand: str,
                      horizon: int) -> tuple[pd.DataFrame, dict]:
    """Join, filter and aggregate ONE brand to brand-month. No cleaning.

    Returns the frame and a provenance record of every count along the way, so
    a fan-out shows up as a number rather than as a silently wrong total.
    """
    views = get_category_views_dir(category)
    cat = category.lower()

    market_id = _resolve_market_id(views, category)
    product_ids, n_skus = _brand_product_ids(views, category, brand)

    facts = pd.read_parquet(
        views / f"{cat}_clean_facts_v.parquet",
        filters=[
            ("market_id", "==", market_id),
            ("product_id", "in", product_ids),
        ],
    )
    n_facts = len(facts)
    if not n_facts:
        raise SystemExit(
            f"No {category} fact rows for {brand!r} in {TARGET_MARKET!r}."
        )

    period = pd.read_parquet(
        views / f"{cat}_clean_dim_period_v.parquet",
        columns=list(_PERIOD_COLS),
    )
    # Validate the join: dim_period is one row per period_id, so a many-to-one
    # merge is the contract. pandas raises if it is not, which is the point --
    # a fan-out here would multiply every measure silently.
    merged = facts.merge(period, on="period_id", how="left", validate="m:1")
    if len(merged) != n_facts:
        raise SystemExit(
            f"Period join changed the row count: {n_facts} -> {len(merged)}."
        )
    n_unmatched = int(merged["period_year"].isna().sum())
    merged = merged.dropna(subset=["period_year", "period_month"])

    measures = [c for c in facts.columns if c not in _FACT_KEYS]
    mean_cols = [c for c in measures if c in _MEAN_MEASURES]
    sum_cols = [c for c in measures if c not in _MEAN_MEASURES]

    # min_count=1 is what preserves NULL. Without it a group of all-NaN sums to
    # 0.0, which asserts "measured, and it was zero" -- a claim the warehouse
    # does not make. The sparsity is real and the agent must see it.
    agg = {c: pd.NamedAgg(column=c, aggfunc=lambda s: s.sum(min_count=1))
           for c in sum_cols}
    agg.update({c: pd.NamedAgg(column=c, aggfunc="mean") for c in mean_cols})

    out = (merged.groupby(["period_year", "period_month"], as_index=False)
                 .agg(n_skus_observed=("product_id", "nunique"), **agg)
                 .sort_values(["period_year", "period_month"])
                 .reset_index(drop=True))
    out.insert(0, "brand", brand)

    # ---------------------------------------------------------------- the cut
    # THE ONLY ROW-DROPPING STEP IN THIS SCRIPT, and it is not cleaning: it is
    # the experiment's leakage boundary.
    #
    # The warehouse holds months past the forecasting origin -- CSD runs to
    # 2026-07 while validation ends 2025-12 -- so an untruncated extract would
    # hand the agent the very months it is asked to forecast, including the
    # scored one. That is not a subtle leak; it is the answer.
    #
    # Applied HERE, at the source, rather than in the harness. A file on disk
    # that is safe only if every reader remembers to truncate it is a file that
    # leaks the first time someone opens it for a different purpose. Cutting at
    # write time makes the leak impossible downstream rather than merely
    # unlikely.
    n_before = len(out)
    cut_y, cut_m = _visible_cutoff(category, horizon)
    keep = (out["period_year"] * 100 + out["period_month"]) <= (cut_y * 100 + cut_m)
    out = out[keep].reset_index(drop=True)
    if out.empty:
        raise SystemExit(
            f"{brand}: no months at or before the visible cutoff "
            f"{cut_y}-{cut_m:02d}.")

    prov = {
        "brand": brand,
        "market_description": TARGET_MARKET,
        # str() only at the manifest boundary -- JSON has no int64, and numpy
        # scalars are not JSON-serialisable. The FILTER above used the native
        # dtype; this is a rendering of it, not the value used to query.
        "market_id": str(market_id),
        "skus_in_dim_product": n_skus,
        "fact_rows_after_filter": n_facts,
        "fact_rows_unmatched_period": n_unmatched,
        "brand_months_visible": len(out),
        "brand_months_before_cut": n_before,
        "months_withheld_as_test": n_before - len(out),
        "visible_cutoff": f"{cut_y}-{cut_m:02d}",
        "distinct_periods_in_facts": int(merged["period_id"].nunique()),
        "first_month": f"{int(out.period_year.iloc[0])}-{int(out.period_month.iloc[0]):02d}",
        "last_month": f"{int(out.period_year.iloc[-1])}-{int(out.period_month.iloc[-1]):02d}",
        "sum_measures": sum_cols,
        "mean_measures": mean_cols,
    }
    return out, prov


def verify(df: pd.DataFrame, prov: dict) -> list[str]:
    """Mechanical checks only.

    There is deliberately NO comparison against the engineered matrix. That
    frame has already had cleaning and human modelling choices applied, so
    agreeing with it would mean this output had inherited exactly what it is
    supposed to exclude. `sales_units` is reported for eyeballing, never as a
    pass condition.
    """
    fail = []
    # Checked BEFORE the cut: the groupby must neither lose nor invent a period.
    # After the cut the counts differ by design, so comparing the visible count
    # here would make the check pass for the wrong reason.
    if prov["brand_months_before_cut"] != prov["distinct_periods_in_facts"]:
        fail.append(
            f"pre-cut brand-months ({prov['brand_months_before_cut']}) != "
            f"distinct periods in the filtered facts "
            f"({prov['distinct_periods_in_facts']}) -- the groupby lost or "
            f"invented a period")
    # The leakage boundary itself. Cheap to check, catastrophic to miss.
    cy, cm = (int(x) for x in prov["visible_cutoff"].split("-"))
    if len(df) and (df["period_year"] * 100 + df["period_month"]).max() > cy * 100 + cm:
        fail.append(f"a month after the visible cutoff {prov['visible_cutoff']} "
                    f"survived the cut -- THE TEST WINDOW IS LEAKING")
    if prov["months_withheld_as_test"] <= 0:
        fail.append("no months were withheld -- the cutoff is at or past the "
                    "end of the data, so nothing is being held out")
    if df.duplicated(["period_year", "period_month"]).any():
        fail.append("duplicate (year, month) rows -- aggregation did not collapse")
    if prov["fact_rows_unmatched_period"]:
        fail.append(f"{prov['fact_rows_unmatched_period']} fact rows had no "
                    f"period match and were dropped")
    for c in prov["mean_measures"]:
        if c.startswith("weighted_") or c.startswith("numeric_"):
            v = df[c].dropna()
            if len(v) and (v > 1.5).any():
                fail.append(f"{c} exceeds 1.5 -- expected a 0-1 fraction; "
                            f"summed instead of averaged?")
    if df[["period_year", "period_month"]].isna().any().any():
        fail.append("null period keys survived the aggregation")
    return fail


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build the post-join/pre-cleaning brand-month payload "
                    "handed to the SRQ4 data-access scenarios.")
    ap.add_argument("--category", default="CSD")
    ap.add_argument("--brands", nargs="+",
                    default=["HARBOE", "7-UP", "ØRBÆK"],
                    help="brands to build; default is the stratified sample")
    ap.add_argument("--horizon", type=int, default=3,
                    help="forecast horizon; selects which split boundary file "
                         "defines the visible window")
    ap.add_argument("--verify-only", action="store_true",
                    help="run and check, write nothing")
    a = ap.parse_args()

    out_dir = SRQ4_AGENT_INPUTS_DIR / a.category
    print(f"building agent inputs: {a.category}, market {TARGET_MARKET!r}")
    print(f"  -> {out_dir}")

    frames, provs, failures = {}, [], {}
    for brand in a.brands:
        df, prov = build_brand_month(a.category, brand, a.horizon)
        bad = verify(df, prov)
        frames[brand] = df
        provs.append(prov)
        failures[brand] = bad
        units = df["sales_units"].dropna()
        print(f"\n  {brand}")
        print(f"    {prov['skus_in_dim_product']} SKUs, "
              f"{prov['fact_rows_after_filter']:,} fact rows "
              f"-> {prov['brand_months_visible']} visible brand-months "
              f"({prov['first_month']} .. {prov['last_month']})")
        print(f"    withheld as test: {prov['months_withheld_as_test']} month(s) "
              f"after {prov['visible_cutoff']}")
        print(f"    columns: {df.shape[1]}  "
              f"(sum {len(prov['sum_measures'])}, mean {len(prov['mean_measures'])})")
        if len(units):
            print(f"    sales_units: min {units.min():,.0f}  "
                  f"median {units.median():,.0f}  max {units.max():,.0f}  "
                  f"[eyeball only, not a pass condition]")
        nulls = df.isna().mean()
        sparse = nulls[nulls > 0].sort_values(ascending=False)
        if len(sparse):
            print(f"    {len(sparse)} column(s) carry nulls, preserved as null:")
            for c, v in sparse.head(6).items():
                print(f"      {c:46s} {v:5.1%} null")
            if len(sparse) > 6:
                print(f"      ... and {len(sparse) - 6} more")
        for f in bad:
            print(f"    FAIL: {f}")

    n_fail = sum(len(v) for v in failures.values())
    if n_fail:
        print(f"\n{n_fail} check(s) failed. Nothing written.")
        return 1
    print("\nAll mechanical checks passed.")

    if a.verify_only:
        print("--verify-only: nothing written.")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    for brand, df in frames.items():
        p = out_dir / f"{_slug(brand)}_brand_month.csv"
        df.to_csv(p, index=False, encoding="utf-8")
        print(f"  wrote {p.name}  ({p.stat().st_size:,} bytes)")

    meta = pd.read_parquet(
        get_category_metadata_dir(a.category)
        / f"metadata_{a.category.lower()}_columns.parquet")
    mp = out_dir / "schema_dictionary.csv"
    meta.to_csv(mp, index=False, encoding="utf-8")
    print(f"  wrote {mp.name}  ({mp.stat().st_size:,} bytes, {len(meta)} columns "
          f"across {meta.table_name.nunique()} tables)")

    manifest = {
        "built_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "category": a.category,
        "horizon": a.horizon,
        "state": ("post-join, post-market-filter, post-brand-month-aggregation, "
                  "truncated at the end of validation; PRE cleaning, "
                  "PRE imputation, PRE feature engineering"),
        "declared_choices": {
            "market": TARGET_MARKET,
            "sku_to_brand": ("dim_product is UPC-only, so brand-month requires "
                             "summing across SKUs"),
            "sum_vs_mean": ("volume measures sum; distribution measures are "
                            "ACV-weighted, non-additive across products, so "
                            "they average"),
            "nulls": "preserved as null; never zero-filled",
            "visible_window": ("train + validation only, read from the "
                               "pipeline's persisted split boundary; the "
                               "test window is cut at write time so no "
                               "downstream reader can leak it"),
        },
        "brands": provs,
    }
    mfp = out_dir / "manifest.json"
    mfp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"  wrote {mfp.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
