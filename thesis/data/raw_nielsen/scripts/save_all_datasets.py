"""
Save all Nielsen Fabric datasets to local JSONL files.
Usage: python save_all_datasets.py
Output: thesis/data/raw_nielsen/data_jsonl/
"""

# ============================================================================
# CONFIGURATION FLAGS
# ============================================================================

# Default: download views + metadata only
# Override via command line: python save_all_datasets.py --download-raw
DOWNLOAD_RAW_DATA = False

# %%
import sys
import argparse
import os
import struct
import pyodbc
import json
import tracemalloc
import time
from pathlib import Path
import importlib
from datetime import datetime, date
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.console import Console
from rich.style import Style

console = Console()

# %%

# Find project root by locating CLAUDE.md -> helps dynamically finding the project root regardless of where the script is run from                                                                                                                                                                                                                                                          
current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        ROOT_DIR_FINDER = current
        break
    current = current.parent
else:
    raise FileNotFoundError("Could not find project root (CLAUDE.md)")


print(f"Project root found at: {ROOT_DIR_FINDER}")
sys.path.insert(0, str(ROOT_DIR_FINDER))

import PATHS
importlib.reload(PATHS)  # Reload the config module to ensure we have the latest changes


# %%

from PATHS import *

# Load credentials from project root
_env_path = ROOT_DIR / ".env"
load_dotenv(_env_path)

SERVER   = os.environ["RU_SERVER_STRING"]
DATABASE = os.environ["RU_DATABASE"]
CLIENT_ID     = os.environ["RU_CLIENT_ID"]
TENANT_ID     = os.environ["RU_TENANT_ID"]
CLIENT_SECRET = os.environ["RU_CLIENT_SECRET"]
ODBC_DRIVER = "ODBC Driver 18 for SQL Server"

# Output to JSONL (faster than CSV)
OUTPUT_DIR = THESIS_DATA_NIELSEN_JSONL_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _get_token() -> bytes:
    """Obtain Entra ID access token for Fabric."""
    credential = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    token = credential.get_token("https://database.windows.net/.default")
    token_bytes = token.token.encode("UTF-16-LE")
    return struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

def _generate_schema_snapshot(conn, output_dir: Path) -> None:
    """Generate markdown document of database schema."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'dbo' ORDER BY TABLE_TYPE, TABLE_NAME
    """)

    results = cursor.fetchall()
    views = [name for name, t in results if t == "VIEW"]
    tables = [name for name, t in results if t != "VIEW"]

    md = f"""# Nielsen Fabric Database Schema

**Snapshot:** {datetime.now().isoformat()}
**Total Objects:** {len(results)} (Views: {len(views)}, Tables: {len(tables)})

## Views (Cleaned Data for Modeling)
"""
    for view in sorted(views):
        try:
            cursor.execute(f"SELECT COUNT(*) FROM dbo.{view}")
            rows = cursor.fetchone()[0]
            md += f"- {view} ({rows:,} rows)\n"
        except:
            md += f"- {view}\n"

    output_path = output_dir / "SCHEMA_SNAPSHOT.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"  OK: SCHEMA_SNAPSHOT.md")

class NielsenJSONEncoder(json.JSONEncoder):
    """Custom encoder for Nielsen data with datetime/date support."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

def get_connection() -> pyodbc.Connection:
    """Return open pyodbc connection to Nielsen Fabric warehouse."""
    token_struct = _get_token()
    connection_string = (
        f"Driver={{{ODBC_DRIVER}}};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    return pyodbc.connect(connection_string, attrs_before={1256: token_struct})

def save_table_to_jsonl(conn, table_name: str, output_path: Path, chunk_size: int = 100000) -> dict:
    """
    Query and save a table/view to JSONL with chunked fetching and Rich progress bar.

    Writes one JSON object per line, 100k rows at a time. Much faster than CSV
    (no string escaping), and loads directly into Pandas with pd.read_json(lines=True).

    Args:
        conn: pyodbc connection
        table_name: Nielsen table name
        output_path: Output JSONL path
        chunk_size: Rows to fetch per batch (default 100000)
    """
    try:
        tracemalloc.start()
        t_start = time.perf_counter()
        cursor = conn.cursor()

        # Get row count for progress tracking
        count_cursor = conn.cursor()
        count_cursor.execute(f"SELECT COUNT(*) FROM dbo.{table_name}")
        total_rows = count_cursor.fetchone()[0]
        count_cursor.close()

        if total_rows == 0:
            console.print(f"  [yellow]WARNING[/yellow]: {table_name}: No data")
            return {"status": "empty", "name": table_name}

        # Execute main query and get column names
        cursor.execute(f"SELECT * FROM dbo.{table_name}")
        cols = [d[0] for d in cursor.description]

        # Write JSONL with Rich progress bar
        row_count = 0
        peak_mb = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TextColumn("[cyan]{task.fields[rows]:,}[/cyan] rows"),
            TextColumn("•"),
            TextColumn("[magenta]{task.fields[ram]:.1f}[/magenta] MB"),
            TimeRemainingColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(f"  {table_name}", total=total_rows, rows=0, ram=0.0)

            with open(output_path, "w", encoding="utf-8") as f:
                while True:
                    rows = cursor.fetchmany(chunk_size)
                    if not rows:
                        break

                    # Convert rows to JSON objects and write
                    for row in rows:
                        obj = {col: (None if v is None else v) for col, v in zip(cols, row)}
                        f.write(json.dumps(obj, cls=NielsenJSONEncoder) + "\n")
                        row_count += 1

                    # Update progress bar
                    _, peak = tracemalloc.get_traced_memory()
                    peak_mb = peak / 1024 / 1024
                    progress.update(task, completed=row_count, rows=row_count, ram=peak_mb)

        elapsed = time.perf_counter() - t_start
        tracemalloc.stop()
        mb = output_path.stat().st_size / (1024 * 1024)

        console.print(f"  [green]✓[/green] {table_name}: {row_count:,} rows ({mb:.1f} MB) in {elapsed:.1f}s")
        return {
            "status": "saved",
            "name": table_name,
            "rows": row_count,
            "columns": len(cols),
            "size_mb": round(mb, 2),
            "file": output_path.name,
            "peak_ram_mb": round(peak_mb, 1),
            "elapsed_sec": round(elapsed, 1),
        }

    except Exception as e:
        console.print(f"  [red]ERROR[/red]: {table_name}: {e}")
        return {"status": "error", "name": table_name, "error": str(e)}

def main():
    """Save all Nielsen views, raw tables, and metadata organized by category and type."""
    print(f"Connecting to Nielsen Fabric warehouse...")
    conn = get_connection()
    print("Connection OK\n")

    # Display configuration
    if DOWNLOAD_RAW_DATA:
        print("⚠️  DOWNLOAD_RAW_DATA = True")
        print("   Will download: views + raw tables + metadata (~2 hours)")
    else:
        print("✓ DOWNLOAD_RAW_DATA = False")
        print("  Will download: views + metadata only (~10 minutes)")
        print("  (To include raw tables, set DOWNLOAD_RAW_DATA = True at top of script)\n")

    print(f"Output: {OUTPUT_DIR}\n")

    # Define data by category: views, raw tables, and metadata
    categories_config = {
        "CSD": {
            "views": [
                "csd_clean_dim_market_v",
                "csd_clean_dim_period_v",
                "csd_clean_dim_product_v",
                "csd_clean_facts_v",
            ],
            "raw": [
                "csd_clean_dim_market",
                "csd_clean_dim_period",
                "csd_clean_dim_product",
                "csd_clean_facts",
            ],
            "metadata": [
                "metadata_csd_clean_dim_market",
                "metadata_csd_clean_dim_period",
                "metadata_csd_clean_dim_product",
                "metadata_csd_clean_facts",
                "metadata_csd_columns",
            ],
        },
        "Totalbeer": {
            "views": [
                "totalbeer_clean_dim_market_v",
                "totalbeer_clean_dim_period_v",
                "totalbeer_clean_dim_product_v",
                "totalbeer_clean_facts_v",
            ],
            "raw": [
                "totalbeer_clean_dim_market",
                "totalbeer_clean_dim_period",
                "totalbeer_clean_dim_product",
                "totalbeer_clean_facts",
            ],
            "metadata": [
                "metadata_totalbeer_columns",
            ],
        },
        "Energidrikke": {
            "views": [
                "energidrikke_clean_dim_market_v",
                "energidrikke_clean_dim_period_v",
                "energidrikke_clean_dim_product_v",
                "energidrikke_clean_facts_v",
            ],
            "raw": [
                "energidrikke_clean_dim_market",
                "energidrikke_clean_dim_period",
                "energidrikke_clean_dim_product",
                "energidrikke_clean_facts",
            ],
            "metadata": [
                "metadata_energidrikke_columns",
            ],
        },
        "Danskvand": {
            "views": [
                "danskvand_clean_dim_market_v",
                "danskvand_clean_dim_period_v",
                "danskvand_clean_dim_product_v",
                "danskvand_clean_facts_v",
            ],
            "raw": [
                "danskvand_clean_dim_market",
                "danskvand_clean_dim_period",
                "danskvand_clean_dim_product",
                "danskvand_clean_facts",
            ],
            "metadata": [
                "metadata_danskvand_columns",
            ],
        },
        "RTD": {
            "views": [
                "rtd_clean_dim_market_v",
                "rtd_clean_dim_period_v",
                "rtd_clean_dim_product_v",
                "rtd_clean_facts_v",
            ],
            "raw": [
                "rtd_clean_dim_market",
                "rtd_clean_dim_period",
                "rtd_clean_dim_product",
                "rtd_clean_facts",
            ],
            "metadata": [
                "metadata_rtd_columns",
            ],
        },
    }

    manifest = []

    # Save each category's data organized by type
    for category, config in categories_config.items():
        print(f"\n{'='*60}")
        print(f"CATEGORY: {category}")
        print(f"{'='*60}")

        for data_type in ["views", "raw", "metadata"]:
            if not config[data_type]:
                continue

            # Skip raw tables if DOWNLOAD_RAW_DATA is False
            if data_type == "raw" and not DOWNLOAD_RAW_DATA:
                print(f"\n  RAW: [SKIPPED - DOWNLOAD_RAW_DATA = False]")
                continue

            print(f"\n  {data_type.upper()}:")

            # Create type-specific subdirectory
            type_dir = OUTPUT_DIR / category / data_type
            type_dir.mkdir(parents=True, exist_ok=True)

            for table_name in config[data_type]:
                result = save_table_to_jsonl(conn, table_name, type_dir / f"{table_name}.jsonl")
                manifest.append(result)

    _generate_schema_snapshot(conn, THESIS_DATA_NIELSEN_DESC_DIR)
    conn.close()

    # Write manifest
    manifest_path = OUTPUT_DIR / "MANIFEST.json"
    with open(manifest_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "database": DATABASE,
            "output_dir": str(OUTPUT_DIR),
            "files": [m for m in manifest if m["status"] == "saved"],
            "summary": {
                "total": len(manifest),
                "saved": len([m for m in manifest if m["status"] == "saved"]),
                "empty": len([m for m in manifest if m["status"] == "empty"]),
                "errors": len([m for m in manifest if m["status"] == "error"]),
            }
        }, f, indent=2)

    saved = len([m for m in manifest if m["status"] == "saved"])
    print(f"\nComplete. Saved {saved} tables/views to {OUTPUT_DIR}")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download Nielsen Fabric data to JSONL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python save_all_datasets.py              # Download views + metadata only (~10 min)
  python save_all_datasets.py --download-raw  # Include raw tables (~2 hours total)
        """
    )
    parser.add_argument(
        "--download-raw",
        action="store_true",
        help="Download raw tables in addition to views and metadata (takes ~2 hours)"
    )

    args = parser.parse_args()
    DOWNLOAD_RAW_DATA = args.download_raw

    main()
