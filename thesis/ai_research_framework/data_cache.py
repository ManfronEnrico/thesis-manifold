"""
Data Caching Layer — Audit-Trail DataFrame Storage

Provides a unified interface for loading data from remote sources (SQL, APIs, Google Drive)
and caching to local Parquet files. Maintains checksums for integrity verification.

All datasets are cached locally in .data/processed/ to:
- Minimize RAM usage (load only when needed, unload when done)
- Enable audit trails (checksums prove data hasn't changed between runs)
- Support reproducibility (re-run pipeline with exact same data)
"""

from __future__ import annotations

import gc
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd


class DataCache:
    """
    Lazy-load remote datasets, cache locally, verify integrity.

    Usage:
        df = DataCache.load_or_fetch(
            source_name='indeks_danmark',
            fetch_fn=lambda: pd.read_csv(url),
            hash_check=True
        )
    """

    CACHE_DIR = Path(".data/processed")
    RAW_DIR = Path(".data/raw")
    CHECKSUMS_FILE = CACHE_DIR / "checksums.json"

    @classmethod
    def load_or_fetch(
        cls,
        source_name: str,
        fetch_fn: Callable[[], pd.DataFrame],
        hash_check: bool = True,
        force_refresh: bool = False,
    ) -> pd.DataFrame:
        """
        Load cached DataFrame or fetch from source.

        Args:
            source_name: Cache key, e.g. 'indeks_danmark', 'nielsen_csd'
            fetch_fn: Callable returning pd.DataFrame
            hash_check: Verify cached data integrity before returning
            force_refresh: Ignore cache, fetch fresh data

        Returns:
            pd.DataFrame loaded from cache or fetched fresh

        Raises:
            FileNotFoundError: If fetch_fn fails and no cache exists
            AssertionError: If hash_check fails
        """
        cache_file = cls.CACHE_DIR / f"{source_name}.parquet"

        # Return cached if exists and not forcing refresh
        if cache_file.exists() and not force_refresh:
            df = pd.read_parquet(cache_file)
            if hash_check:
                cls._verify_hash(source_name, df)
            return df

        # Fetch, cache, and return
        print(f"[DataCache] Fetching {source_name}...", flush=True)
        df = fetch_fn()

        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[DataCache] Caching {source_name} → {cache_file}", flush=True)
        df.to_parquet(cache_file, compression="snappy", index=False)
        cls._save_hash(source_name, df)

        print(f"[DataCache] ✓ {source_name} cached ({len(df)} rows)", flush=True)
        return df

    @classmethod
    def _save_hash(cls, source_name: str, df: pd.DataFrame) -> None:
        """Compute and store DataFrame integrity hash."""
        hash_data = {
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(df[col].dtype) for col in df.columns},
            "hash": hashlib.sha256(
                pd.util.hash_pandas_object(df, index=True).values
            ).hexdigest(),
        }

        checksums = cls._read_checksums()
        checksums[source_name] = hash_data

        cls.CHECKSUMS_FILE.parent.mkdir(parents=True, exist_ok=True)
        cls.CHECKSUMS_FILE.write_text(json.dumps(checksums, indent=2))

    @classmethod
    def _verify_hash(cls, source_name: str, df: pd.DataFrame) -> None:
        """Verify cached file matches stored hash."""
        checksums = cls._read_checksums()

        if source_name not in checksums:
            print(f"[DataCache] Warning: no hash for {source_name} (first load?)")
            return

        record = checksums[source_name]

        # Check row count and columns
        assert len(df) == record["rows"], (
            f"[DataCache] Row count mismatch for {source_name}: "
            f"cached {record['rows']}, loaded {len(df)}"
        )
        assert list(df.columns) == record["columns"], (
            f"[DataCache] Column mismatch for {source_name}"
        )

        # Recompute hash to detect data corruption
        new_hash = hashlib.sha256(
            pd.util.hash_pandas_object(df, index=True).values
        ).hexdigest()

        if new_hash != record["hash"]:
            print(
                f"[DataCache] ⚠️  Hash mismatch for {source_name} "
                f"(file may have been modified)"
            )
        else:
            print(f"[DataCache] ✓ {source_name} hash verified")

    @classmethod
    def _read_checksums(cls) -> dict:
        """Load checksums from disk or return empty dict."""
        if cls.CHECKSUMS_FILE.exists():
            return json.loads(cls.CHECKSUMS_FILE.read_text())
        return {}

    @classmethod
    def get_cache_status(cls) -> dict:
        """Return summary of cached datasets."""
        if not cls.CACHE_DIR.exists():
            return {"cached_files": [], "total_size_mb": 0}

        files = list(cls.CACHE_DIR.glob("*.parquet"))
        total_mb = sum(f.stat().st_size for f in files) / 1_048_576

        return {
            "cached_files": [f.stem for f in files],
            "total_size_mb": round(total_mb, 2),
            "checksums_file": str(cls.CHECKSUMS_FILE),
        }

    @classmethod
    def clear_cache(cls, source_name: Optional[str] = None) -> None:
        """Delete cached files (careful: irreversible until next fetch)."""
        if source_name:
            cache_file = cls.CACHE_DIR / f"{source_name}.parquet"
            if cache_file.exists():
                cache_file.unlink()
                print(f"[DataCache] Cleared {source_name}")
        else:
            import shutil
            if cls.CACHE_DIR.exists():
                shutil.rmtree(cls.CACHE_DIR)
                print(f"[DataCache] Cleared all caches")

    @staticmethod
    def unload(df: Optional[pd.DataFrame]) -> None:
        """Explicitly release DataFrame memory after processing."""
        if df is not None:
            del df
        gc.collect()
