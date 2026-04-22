"""
Save all Nielsen Fabric datasets to local CSV files.
Usage: python save_all_datasets.py
Output: thesis/data/nielsen/.csv/
"""

import os
import struct
import pyodbc
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential

# Load credentials from project root
_env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(_env_path)

SERVER   = os.environ["RU_SERVER_STRING"]
DATABASE = os.environ["RU_DATABASE"]
CLIENT_ID     = os.environ["RU_CLIENT_ID"]
TENANT_ID     = os.environ["RU_TENANT_ID"]
CLIENT_SECRET = os.environ["RU_CLIENT_SECRET"]
ODBC_DRIVER = "ODBC Driver 18 for SQL Server"

OUTPUT_DIR = Path(__file__).resolve().parents[2] / ".csv"
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

def save_table_to_csv(conn, table_name: str, output_path: Path) -> dict:
    """Query and save a table/view to CSV. Return metadata about the save."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM dbo.{table_name}")
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]

        if not rows:
            print(f"  WARNING: {table_name}: No data")
            return {"status": "empty", "name": table_name}

        # Write CSV
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            f.write(",".join(cols) + "\n")
            for row in rows:
                f.write(",".join(str(v) if v is not None else "" for v in row) + "\n")

        mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  OK: {table_name}: {len(rows)} rows ({mb:.1f} MB)")
        return {
            "status": "saved",
            "name": table_name,
            "rows": len(rows),
            "columns": len(cols),
            "size_mb": round(mb, 2),
            "file": output_path.name,
        }

    except Exception as e:
        print(f"  ERROR: {table_name}: {e}")
        return {"status": "error", "name": table_name, "error": str(e)}

def main():
    """Save all CSD and category views + metadata."""
    print(f"Connecting to Nielsen Fabric warehouse...")
    conn = get_connection()
    print("Connection OK\n")

    print(f"Output: {OUTPUT_DIR}\n")

    # Main CSD views
    csd_views = [
        "csd_clean_dim_market_v",
        "csd_clean_dim_period_v",
        "csd_clean_dim_product_v",
        "csd_clean_facts_v",
    ]

    # CSD metadata
    csd_metadata = [
        "metadata_csd_clean_dim_market",
        "metadata_csd_clean_dim_period",
        "metadata_csd_clean_dim_product",
        "metadata_csd_clean_facts",
        "metadata_csd_columns",
    ]

    # Category metadata
    category_metadata = [
        "metadata_totalbeer_columns",
        "metadata_energidrikke_columns",
        "metadata_danskvand_columns",
        "metadata_rtd_columns",
    ]

    # Other category views
    other_views = [
        "totalbeer_clean_dim_market_v",
        "totalbeer_clean_dim_period_v",
        "totalbeer_clean_dim_product_v",
        "totalbeer_clean_facts_v",
        "energidrikke_clean_dim_market_v",
        "energidrikke_clean_dim_period_v",
        "energidrikke_clean_dim_product_v",
        "energidrikke_clean_facts_v",
        "danskvand_clean_dim_market_v",
        "danskvand_clean_dim_period_v",
        "danskvand_clean_dim_product_v",
        "danskvand_clean_facts_v",
        "rtd_clean_dim_market_v",
        "rtd_clean_dim_period_v",
        "rtd_clean_dim_product_v",
        "rtd_clean_facts_v",
    ]

    manifest = []

    print("CSD views:")
    for view in csd_views:
        result = save_table_to_csv(conn, view, OUTPUT_DIR / f"{view}.csv")
        manifest.append(result)

    print("\nCSD metadata:")
    for table in csd_metadata:
        result = save_table_to_csv(conn, table, OUTPUT_DIR / f"{table}.csv")
        manifest.append(result)

    print("\nCategory metadata:")
    for table in category_metadata:
        result = save_table_to_csv(conn, table, OUTPUT_DIR / f"{table}.csv")
        manifest.append(result)

    print("\nOther category views:")
    for view in other_views:
        result = save_table_to_csv(conn, view, OUTPUT_DIR / f"{view}.csv")
        manifest.append(result)

    _generate_schema_snapshot(conn, OUTPUT_DIR)
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
    main()
