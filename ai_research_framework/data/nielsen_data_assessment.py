"""
Nielsen Data Assessment Script — Phase 1
Connects to the Nielsen_clean Microsoft Fabric warehouse and runs
a comprehensive data quality + coverage assessment across all 4 views.

Usage:
    cd /Users/enricomanfron/Desktop/Thesis\ Maniflod
    python3 -m ai_research_framework.data.nielsen_data_assessment
"""

import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_research_framework.data.nielsen_connector import get_connection


def q(conn, sql: str) -> pd.DataFrame:
    """Run a SQL query and return a DataFrame (cursor-based to avoid pandas warnings)."""
    cursor = conn.cursor()
    cursor.execute(sql)
    cols = [d[0] for d in cursor.description]
    rows = cursor.fetchall()
    return pd.DataFrame([list(r) for r in rows], columns=cols)


def section(title: str) -> None:
    print(f"\n{'='*72}")
    print(f"  {title}")
    print(f"{'='*72}")


def sub(title: str) -> None:
    print(f"\n--- {title} ---")


# ── 4.1 DIM MARKET ────────────────────────────────────────────────────────────

def assess_dim_market(conn):
    section("4.1  DIM MARKET  (csd_clean_dim_market_v)")
    df = q(conn, "SELECT * FROM dbo.csd_clean_dim_market_v ORDER BY market_description")
    print(f"Row count : {len(df)}")
    print(f"Columns   : {list(df.columns)}")
    print("\nAll markets:")
    for _, row in df.iterrows():
        print(f"  {row['market_id']}  |  {row['market_description']}")

    # NULLs
    nulls = {c: int(df[c].isnull().sum()) for c in df.columns}
    print(f"\nNULL counts: {nulls}")


# ── 4.2 DIM PERIOD ────────────────────────────────────────────────────────────

def assess_dim_period(conn):
    section("4.2  DIM PERIOD  (csd_clean_dim_period_v)")
    df = q(conn, "SELECT * FROM dbo.csd_clean_dim_period_v ORDER BY period_id")
    print(f"Row count : {len(df)}")
    print(f"Columns   : {list(df.columns)}")

    sub("Year / month distribution")
    for yr, grp in df.groupby("period_year"):
        months = sorted(grp["period_month"].unique().tolist())
        print(f"  {yr}: months {months}  (n={len(months)})")

    sub("Date range")
    print(f"  Earliest : {df['date_key'].min()}")
    print(f"  Latest   : {df['date_key'].max()}")

    nulls = {c: int(df[c].isnull().sum()) for c in df.columns}
    print(f"\nNULL counts: {nulls}")

    return df


# ── 4.3 DIM PRODUCT ───────────────────────────────────────────────────────────

def assess_dim_product(conn):
    section("4.3  DIM PRODUCT  (csd_clean_dim_product_v)")
    df = q(conn, "SELECT * FROM dbo.csd_clean_dim_product_v")
    print(f"Row count (SKUs) : {len(df)}")
    print(f"Columns          : {list(df.columns)}")

    sub("NULL counts per column")
    for col in df.columns:
        n = int(df[col].isnull().sum())
        pct = 100 * n / len(df) if len(df) > 0 else 0
        print(f"  {col:<30}: {n:>4} nulls  ({pct:.1f}%)")

    sub("Distinct values for key categorical columns")
    cat_cols = ["brand", "manufacturer", "packaging", "type",
                "regular_light", "price_category", "organic",
                "private_label", "corporation_ru_1"]
    for col in cat_cols:
        if col in df.columns:
            vals = sorted(df[col].dropna().unique().tolist())
            print(f"  {col} ({len(vals)} distinct): {vals}")

    sub("Top brands by SKU count")
    if "brand" in df.columns:
        top = df["brand"].value_counts().head(20)
        for brand, cnt in top.items():
            print(f"  {brand:<30}: {cnt} SKUs")

    return df


# ── 4.4 FACTS ─────────────────────────────────────────────────────────────────

def assess_facts(conn):
    section("4.4  FACTS  (csd_clean_facts_v)")

    # Columns
    df_top = q(conn, "SELECT TOP 1 * FROM dbo.csd_clean_facts_v")
    cols = list(df_top.columns)
    print(f"Columns : {cols}")

    # Row count
    row_count = int(q(conn, "SELECT COUNT(*) AS n FROM dbo.csd_clean_facts_v").iloc[0, 0])
    print(f"Total rows : {row_count:,}")

    sub("NULL counts per column")
    for col in cols:
        cnt = int(q(conn, f"SELECT COUNT(*) AS n FROM dbo.csd_clean_facts_v WHERE [{col}] IS NULL").iloc[0, 0])
        pct = 100 * cnt / row_count if row_count > 0 else 0
        print(f"  {col:<35}: {cnt:>7,} nulls  ({pct:.2f}%)")

    sub("Descriptive statistics — key numeric columns")
    numeric_cols = ["sales_value", "sales_in_liters", "sales_units",
                    "sales_value_any_promo", "sales_in_liters_any_promo",
                    "sales_units_any_promo", "weighted_distribution"]
    available = [c for c in numeric_cols if c in cols]
    for col in available:
        r = q(conn, f"""
            SELECT
                MIN([{col}]) AS mn,
                MAX([{col}]) AS mx,
                AVG([{col}]) AS avg,
                STDEV([{col}]) AS std
            FROM dbo.csd_clean_facts_v
        """).iloc[0]
        print(f"  {col:<35}: min={r['mn']:.2f}  max={r['mx']:.2f}  mean={r['avg']:.2f}  std={r['std']:.2f}")

    sub("Zero-sales rows (sales_units = 0)")
    zero = int(q(conn, "SELECT COUNT(*) AS n FROM dbo.csd_clean_facts_v WHERE sales_units = 0").iloc[0, 0])
    print(f"  sales_units = 0: {zero:,} rows  ({100*zero/row_count:.2f}%)")

    sub("Promotional rows (sales_units_any_promo > 0)")
    promo = int(q(conn, "SELECT COUNT(*) AS n FROM dbo.csd_clean_facts_v WHERE sales_units_any_promo > 0").iloc[0, 0])
    print(f"  Promo rows: {promo:,}  ({100*promo/row_count:.2f}%)")

    sub("Coverage — distinct keys")
    for dim, col in [("Markets", "market_id"), ("Periods", "period_id"), ("Products", "product_id")]:
        n = int(q(conn, f"SELECT COUNT(DISTINCT [{col}]) AS n FROM dbo.csd_clean_facts_v").iloc[0, 0])
        print(f"  Distinct {dim}: {n}")

    sub("Row count by market_id")
    df_mkt = q(conn, """
        SELECT f.market_id, m.market_description, COUNT(*) AS row_count
        FROM dbo.csd_clean_facts_v f
        JOIN dbo.csd_clean_dim_market_v m ON f.market_id = m.market_id
        GROUP BY f.market_id, m.market_description
        ORDER BY row_count DESC
    """)
    print(df_mkt.to_string(index=False))

    sub("Row count by period_id")
    df_per = q(conn, """
        SELECT f.period_id, p.period_year, p.period_month, COUNT(*) AS row_count
        FROM dbo.csd_clean_facts_v f
        JOIN dbo.csd_clean_dim_period_v p ON f.period_id = p.period_id
        GROUP BY f.period_id, p.period_year, p.period_month
        ORDER BY f.period_id
    """)
    print(df_per.to_string(index=False))

    return row_count, cols


# ── 4.5 FORECASTING SUITABILITY ───────────────────────────────────────────────

def assess_forecasting_suitability(conn, period_df: pd.DataFrame):
    section("4.5  FORECASTING SUITABILITY")

    sub("Top 15 brand × market combinations by total sales_units")
    df_top = q(conn, """
        SELECT TOP 15
            p.brand,
            m.market_description,
            SUM(f.sales_units)              AS total_units,
            COUNT(DISTINCT f.period_id)     AS n_periods,
            CAST(AVG(f.sales_units) AS DECIMAL(18,1)) AS avg_units_per_period
        FROM dbo.csd_clean_facts_v f
        JOIN dbo.csd_clean_dim_product_v p ON f.product_id = p.product_id
        JOIN dbo.csd_clean_dim_market_v  m ON f.market_id  = m.market_id
        WHERE f.sales_units > 0
        GROUP BY p.brand, m.market_description
        ORDER BY total_units DESC
    """)
    print(df_top.to_string(index=False))

    sub("Time-series length distribution (periods per brand × market series)")
    df_len = q(conn, """
        SELECT period_count, COUNT(*) AS n_series
        FROM (
            SELECT p.brand, f.market_id,
                   COUNT(DISTINCT f.period_id) AS period_count
            FROM dbo.csd_clean_facts_v f
            JOIN dbo.csd_clean_dim_product_v p ON f.product_id = p.product_id
            GROUP BY p.brand, f.market_id
        ) sub
        GROUP BY period_count
        ORDER BY period_count
    """)
    print(df_len.to_string(index=False))

    sub("Proposed train / validation / test split")
    total = len(period_df)
    t_end = int(total * 0.70)
    v_end = int(total * 0.85)
    print(f"  Total periods : {total}")
    print(f"  Train (~70%)  : period_id {period_df['period_id'].iloc[0]} "
          f"({period_df['period_year'].iloc[0]}-{period_df['period_month'].iloc[0]:02d}) "
          f"→ {period_df['period_id'].iloc[t_end-1]} "
          f"({period_df['period_year'].iloc[t_end-1]}-{period_df['period_month'].iloc[t_end-1]:02d})")
    print(f"  Val  (~15%)   : period_id {period_df['period_id'].iloc[t_end]} "
          f"({period_df['period_year'].iloc[t_end]}-{period_df['period_month'].iloc[t_end]:02d}) "
          f"→ {period_df['period_id'].iloc[v_end-1]} "
          f"({period_df['period_year'].iloc[v_end-1]}-{period_df['period_month'].iloc[v_end-1]:02d})")
    print(f"  Test (~15%)   : period_id {period_df['period_id'].iloc[v_end]} "
          f"({period_df['period_year'].iloc[v_end]}-{period_df['period_month'].iloc[v_end]:02d}) "
          f"→ {period_df['period_id'].iloc[-1]} "
          f"({period_df['period_year'].iloc[-1]}-{period_df['period_month'].iloc[-1]:02d})")

    sub("DVH EXCL. HD scope — brand-level completeness")
    df_dvh = q(conn, """
        SELECT
            p.brand,
            COUNT(DISTINCT f.period_id)  AS n_periods,
            SUM(f.sales_units)           AS total_units,
            MIN(f.sales_units)           AS min_units,
            MAX(f.sales_units)           AS max_units
        FROM dbo.csd_clean_facts_v f
        JOIN dbo.csd_clean_dim_product_v p ON f.product_id = p.product_id
        JOIN dbo.csd_clean_dim_market_v  m ON f.market_id  = m.market_id
        WHERE m.market_description = 'DVH EXCL. HD'
          AND f.sales_units > 0
        GROUP BY p.brand
        ORDER BY total_units DESC
    """)
    print(df_dvh.to_string(index=False))


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print("Nielsen Data Assessment — Phase 1")
    print("Connecting...")
    conn = get_connection()
    print("Connection OK")

    try:
        assess_dim_market(conn)
        period_df = assess_dim_period(conn)
        assess_dim_product(conn)
        row_count, cols = assess_facts(conn)
        assess_forecasting_suitability(conn, period_df)
    finally:
        conn.close()
        print("\n\nAssessment complete. Connection closed.")


if __name__ == "__main__":
    main()
