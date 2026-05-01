"""
Indeks Danmark / SPSS Data Load & Cache Script
================================================
Loads 3 CSV files from local storage, validates structure,
and returns DataFrames for analysis.

Usage (command line):
    python datasets/data_spss_indeksdanmark/scripts/spss_indeksdanmark_loader.py

Usage (in code):
    from thesis.data.indeksdanmark.scripts.spss_indeksdanmark_loader import (
        load_main_data,
        load_codebook,
        load_metadata
    )
    df_main = load_main_data()
    df_codebook = load_codebook()
    df_metadata = load_metadata()
"""

import sys
import pandas as pd
from pathlib import Path

# Add repo root to path so imports work from anywhere
repo_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(repo_root))


DATA_DIR = Path(__file__).resolve().parent.parent / ".csv"

# File paths
MAIN_DATA_FILE = DATA_DIR / "indeksdanmark_data.csv"
CODEBOOK_FILE = DATA_DIR / "official_codebook.csv"
METADATA_FILE = DATA_DIR / "indeksdanmark_metadata.csv"


def load_main_data() -> pd.DataFrame:
    """
    Load main Indeks Danmark survey data.

    Returns:
        pd.DataFrame with 20,134 rows × 6,364 columns (all float64)
    """
    if not MAIN_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Main data file not found: {MAIN_DATA_FILE}\n"
            f"Place indeksdanmark_data.csv in: {DATA_DIR}"
        )

    print(f"[SPSS] Loading main data: {MAIN_DATA_FILE.name}", flush=True)
    df = pd.read_csv(MAIN_DATA_FILE)
    print(f"[SPSS] ✓ Loaded {len(df)} rows × {len(df.columns)} columns", flush=True)
    return df


def load_codebook() -> pd.DataFrame:
    """
    Load codebook with variable documentation + survey weights.

    Returns:
        pd.DataFrame with 6,364 rows (one per variable) × 11 columns
    """
    if not CODEBOOK_FILE.exists():
        raise FileNotFoundError(
            f"Codebook file not found: {CODEBOOK_FILE}\n"
            f"Place official_codebook.csv in: {DATA_DIR}"
        )

    print(f"[SPSS] Loading codebook: {CODEBOOK_FILE.name}", flush=True)
    df = pd.read_csv(CODEBOOK_FILE)
    print(f"[SPSS] ✓ Loaded {len(df)} variable definitions", flush=True)
    return df


def load_metadata() -> pd.DataFrame:
    """
    Load value label mappings (numeric → readable labels).

    Returns:
        pd.DataFrame with 29,185 rows × 3 columns (Variable, Value, Label)
    """
    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_FILE}\n"
            f"Place indeksdanmark_metadata.csv in: {DATA_DIR}"
        )

    print(f"[SPSS] Loading metadata: {METADATA_FILE.name}", flush=True)
    df = pd.read_csv(METADATA_FILE)
    print(f"[SPSS] ✓ Loaded {len(df)} value label mappings", flush=True)
    return df


def load_all() -> tuple:
    """
    Load all 3 files at once.

    Returns:
        Tuple of (main_data, codebook, metadata) DataFrames
    """
    return load_main_data(), load_codebook(), load_metadata()


def main():
    """Command-line interface."""
    try:
        print("[SPSS] Loading Indeks Danmark data files...\n")
        df_main, df_codebook, df_metadata = load_all()

        print(f"\n✓ All files loaded successfully:")
        print(f"  Main data: {len(df_main)} rows × {len(df_main.columns)} columns")
        print(f"  Codebook: {len(df_codebook)} variables")
        print(f"  Metadata: {len(df_metadata)} value labels")
        print(f"\nMain data info:")
        print(f"  Columns: {list(df_main.columns[:5])}... (showing first 5)")
        print(f"  Data types:\n{df_main.dtypes.value_counts()}")

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
