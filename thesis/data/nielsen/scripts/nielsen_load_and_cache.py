"""
Nielsen Data Load & Cache Script
=================================
Connects to Nielsen SQL database, fetches csd_clean_facts_v table,
saves to local CSV (untracked), and returns DataFrame.

Usage (command line):
    python datasets/data_nielsen/scripts/nielsen_load_and_cache.py [--force-refresh]

Usage (in code):
    from thesis.data.nielsen.scripts.nielsen_load_and_cache import load_nielsen_data
    df = load_nielsen_data(force_refresh=False)
    print(f"Loaded {len(df)} rows")
"""

import sys
import pandas as pd
from pathlib import Path

# Add repo root to path so imports work from anywhere
repo_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(repo_root))

from thesis.data.nielsen.scripts.nielsen_connector import get_connection


DATA_CACHE_DIR = Path(__file__).resolve().parent.parent / ".csv"
CACHE_FILE = DATA_CACHE_DIR / "nielsen_data.csv"


def load_nielsen_data(force_refresh: bool = False) -> pd.DataFrame:
    """
    Load Nielsen CSD facts table from SQL or cache.

    Args:
        force_refresh: If True, always fetch fresh from SQL; ignore cache.

    Returns:
        pd.DataFrame with Nielsen facts data.

    Raises:
        RuntimeError: If fetch fails and no cache exists.
    """
    # Return from cache if exists and not forcing refresh
    if CACHE_FILE.exists() and not force_refresh:
        print(f"[Nielsen] Loading from cache: {CACHE_FILE}")
        df = pd.read_csv(CACHE_FILE)
        print(f"[Nielsen] ✓ Loaded {len(df)} rows from cache")
        return df

    # Fetch from SQL
    print(f"[Nielsen] Connecting to database...", flush=True)
    conn = get_connection()
    print(f"[Nielsen] Connected. Fetching csd_clean_facts_v...", flush=True)

    try:
        df = pd.read_sql(
            "SELECT * FROM dbo.csd_clean_facts_v",
            conn
        )
        print(f"[Nielsen] ✓ Fetched {len(df)} rows", flush=True)
    finally:
        conn.close()

    # Save to cache
    DATA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[Nielsen] Caching to: {CACHE_FILE}", flush=True)
    df.to_csv(CACHE_FILE, index=False)
    print(f"[Nielsen] ✓ Cached {len(df)} rows to {CACHE_FILE.name}", flush=True)

    return df


def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch Nielsen data from SQL and cache locally"
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Ignore cache, fetch fresh from SQL"
    )
    args = parser.parse_args()

    try:
        df = load_nielsen_data(force_refresh=args.force_refresh)
        print(f"\n✓ Success: {len(df)} rows")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Data types:\n{df.dtypes.to_string()}")
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
