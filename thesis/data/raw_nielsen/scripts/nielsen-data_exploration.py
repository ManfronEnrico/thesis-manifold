"""
Nielsen Database Explorer
--------------------------
First-look script — run this once to understand what data we're working with.

Usage:
    python scripts/explore_nielsen.py

Output:
    - All tables/views visible to our service principal
    - Column names + data types for the 4 known schema tables
    - Row counts + date range per table
    - First 10 rows of csd_clean_facts_v (the main facts table)
"""

import sys
from pathlib import Path

import pandas as pd

# Allow imports from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from thesis.ai_research_framework.config import NielsenConfig
from thesis.data.nielsen.scripts.nielsen_connector import get_connection

KNOWN_TABLES = NielsenConfig().schema_tables


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def run_query(conn, sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, conn)


def main() -> None:
    print("Connecting to Nielsen / Prometheus database...")
    conn = get_connection()
    print("Connected.\n")

    # ── 1. All visible tables/views ───────────────────────────────────────────
    section("1. All visible tables / views")
    tables_df = run_query(conn, """
        SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
        FROM INFORMATION_SCHEMA.TABLES
        ORDER BY TABLE_SCHEMA, TABLE_NAME
    """)
    print(tables_df.to_string(index=False))

    # ── 2. Column info for each known table ───────────────────────────────────
    section("2. Column names + data types (known tables)")
    for table in KNOWN_TABLES:
        print(f"\n--- {table} ---")
        cols_df = run_query(conn, f"""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION
        """)
        if cols_df.empty:
            print("  (table not found or no access)")
        else:
            print(cols_df.to_string(index=False))

    # ── 3. Row counts ─────────────────────────────────────────────────────────
    section("3. Row counts")
    for table in KNOWN_TABLES:
        try:
            count_df = run_query(conn, f"SELECT COUNT(*) AS row_count FROM {table}")
            print(f"  {table}: {count_df['row_count'].iloc[0]:,} rows")
        except Exception as exc:
            print(f"  {table}: ERROR — {exc}")

    # ── 4. Date range (period dimension) ─────────────────────────────────────
    section("4. Date / period range")
    try:
        period_df = run_query(conn, """
            SELECT MIN(period_id) AS earliest, MAX(period_id) AS latest,
                   COUNT(DISTINCT period_id) AS n_periods
            FROM csd_clean_dim_period_v
        """)
        print(period_df.to_string(index=False))
    except Exception as exc:
        print(f"  Could not query period dimension: {exc}")

    # ── 5. Market / retailer count ────────────────────────────────────────────
    section("5. Markets / retailers")
    try:
        market_df = run_query(conn, """
            SELECT COUNT(DISTINCT market_id) AS n_markets,
                   COUNT(DISTINCT market_name) AS n_unique_names
            FROM csd_clean_dim_market_v
        """)
        print(market_df.to_string(index=False))

        top_markets = run_query(conn, """
            SELECT TOP 10 market_name
            FROM csd_clean_dim_market_v
            ORDER BY market_name
        """)
        print("\nSample market names:")
        print(top_markets.to_string(index=False))
    except Exception as exc:
        print(f"  Could not query market dimension: {exc}")

    # ── 6. Product count ─────────────────────────────────────────────────────
    section("6. Products")
    try:
        product_df = run_query(conn, """
            SELECT COUNT(DISTINCT product_id) AS n_products
            FROM csd_clean_dim_product_v
        """)
        print(product_df.to_string(index=False))

        top_products = run_query(conn, """
            SELECT TOP 10 *
            FROM csd_clean_dim_product_v
            ORDER BY product_id
        """)
        print("\nFirst 10 products:")
        print(top_products.to_string(index=False))
    except Exception as exc:
        print(f"  Could not query product dimension: {exc}")

    # ── 7. Facts table — first 10 rows ────────────────────────────────────────
    section("7. csd_clean_facts_v — first 10 rows (head)")
    try:
        facts_df = run_query(conn, "SELECT TOP 10 * FROM csd_clean_facts_v")
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 200)
        print(facts_df.to_string(index=False))
    except Exception as exc:
        print(f"  Could not query facts table: {exc}")

    # ── 8. Facts — null check on key metrics ─────────────────────────────────
    section("8. Null check — key metrics in facts table")
    try:
        null_df = run_query(conn, """
            SELECT
                COUNT(*) AS total_rows,
                SUM(CASE WHEN sales_value IS NULL THEN 1 ELSE 0 END) AS null_sales_value,
                SUM(CASE WHEN sales_in_liters IS NULL THEN 1 ELSE 0 END) AS null_sales_liters,
                SUM(CASE WHEN sales_units IS NULL THEN 1 ELSE 0 END) AS null_sales_units
            FROM csd_clean_facts_v
        """)
        print(null_df.to_string(index=False))
    except Exception as exc:
        print(f"  Could not run null check: {exc}")

    conn.close()
    print("\nDone. Connection closed.")


if __name__ == "__main__":
    main()
