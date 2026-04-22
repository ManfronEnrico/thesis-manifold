"""
Audit all available datasets in Nielsen Fabric warehouse.
Lists all tables, views, metadata with columns and generates SCHEMA_SNAPSHOT.md.
Usage: python audit_datasets.py
"""

import os
import struct
import pyodbc
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential

# Load credentials
_env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(_env_path)

SERVER   = os.environ["RU_SERVER_STRING"]
DATABASE = os.environ["RU_DATABASE"]
CLIENT_ID     = os.environ["RU_CLIENT_ID"]
TENANT_ID     = os.environ["RU_TENANT_ID"]
CLIENT_SECRET = os.environ["RU_CLIENT_SECRET"]
ODBC_DRIVER = "ODBC Driver 18 for SQL Server"

def _get_token() -> bytes:
    credential = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    token = credential.get_token("https://database.windows.net/.default")
    token_bytes = token.token.encode("UTF-16-LE")
    return struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

def get_connection() -> pyodbc.Connection:
    token_struct = _get_token()
    connection_string = (
        f"Driver={{{ODBC_DRIVER}}};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    return pyodbc.connect(connection_string, attrs_before={1256: token_struct})

def get_table_columns(conn, table_name: str) -> list:
    """Get list of column names for a table."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM dbo.{table_name} WHERE 1=0")
        columns = [d[0] for d in cursor.description]
        return columns
    except:
        return []

def get_row_count(conn, table_name: str) -> int:
    """Get row count for a table."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM dbo.{table_name}")
        return cursor.fetchone()[0]
    except:
        return 0

def audit_schema():
    """Query database schema and generate snapshot with columns."""
    print(f"Connecting to {DATABASE}...")
    conn = get_connection()
    print("OK\n")

    cursor = conn.cursor()

    # Get all tables and views
    cursor.execute("""
        SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'dbo'
        ORDER BY TABLE_TYPE, TABLE_NAME
    """)

    results = cursor.fetchall()

    # Group by type
    views = []
    tables = []
    metadata = []

    for schema, name, table_type in results:
        if "metadata" in name.lower():
            metadata.append(name)
        elif table_type == "VIEW":
            views.append(name)
        else:
            tables.append(name)

    # Report to terminal
    print(f"VIEWS ({len(views)}):")
    for view in sorted(views):
        cols = get_table_columns(conn, view)
        row_count = get_row_count(conn, view)
        cols_str = ", ".join(cols) if cols else "N/A"
        print(f"  {view} ({row_count:,} rows)")
        print(f"    Columns: {cols_str}")

    print(f"\nBASE TABLES ({len(tables)}):")
    for table in sorted(tables):
        cols = get_table_columns(conn, table)
        row_count = get_row_count(conn, table)
        cols_str = ", ".join(cols) if cols else "N/A"
        print(f"  {table} ({row_count:,} rows)")
        print(f"    Columns: {cols_str}")

    print(f"\nMETADATA ({len(metadata)}):")
    for meta in sorted(metadata):
        cols = get_table_columns(conn, meta)
        row_count = get_row_count(conn, meta)
        cols_str = ", ".join(cols) if cols else "N/A"
        print(f"  {meta} ({row_count:,} rows)")
        print(f"    Columns: {cols_str}")

    print(f"\nTOTAL: {len(results)} objects")

    # Categories present
    categories = set()
    for name in views + tables + metadata:
        for cat in ["csd", "totalbeer", "energidrikke", "danskvand", "rtd"]:
            if cat in name.lower():
                categories.add(cat.upper())
                break

    print(f"\nCATEGORIES FOUND: {', '.join(sorted(categories))}")

    # Generate schema snapshot
    print(f"\nGenerating SCHEMA_SNAPSHOT.md...")
    _generate_schema_snapshot(conn, views, tables, metadata)

def _generate_schema_snapshot(conn, views, tables, metadata):
    """Generate comprehensive schema snapshot with columns."""
    output_dir = Path(__file__).resolve().parents[2] / ".csv"
    output_dir.mkdir(parents=True, exist_ok=True)

    md = f"""# Nielsen Fabric Database Schema Snapshot

**Database:** {DATABASE}
**Snapshot Date:** {datetime.now().isoformat()}
**Server:** {SERVER}

---

## Summary

| Type | Count |
|------|-------|
| Views (cleaned data) | {len(views)} |
| Base Tables (raw data) | {len(tables)} |
| Metadata Tables | {len(metadata)} |
| **Total** | **{len(views) + len(tables) + len(metadata)}** |

---

## Views (Cleaned Data — Use These for Modeling)

"""

    for view in sorted(views):
        cols = get_table_columns(conn, view)
        row_count = get_row_count(conn, view)

        md += f"### {view}\n"
        md += f"**Rows:** {row_count:,} | **Columns:** {len(cols)}\n"
        md += f"**Column List:** `{', '.join(cols)}`\n\n"

    md += f"""---

## Base Tables (Raw Data)

"""
    for table in sorted(tables):
        cols = get_table_columns(conn, table)
        row_count = get_row_count(conn, table)

        md += f"### {table}\n"
        md += f"**Rows:** {row_count:,} | **Columns:** {len(cols)}\n"
        md += f"**Column List:** `{', '.join(cols)}`\n\n"

    md += f"""---

## Metadata Tables

"""
    for meta in sorted(metadata):
        cols = get_table_columns(conn, meta)
        row_count = get_row_count(conn, meta)

        md += f"### {meta}\n"
        md += f"**Rows:** {row_count:,} | **Columns:** {len(cols)}\n"
        md += f"**Column List:** `{', '.join(cols)}`\n\n"

    # Write file
    snapshot_path = output_dir / "SCHEMA_SNAPSHOT.md"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"  Saved: {snapshot_path}")

if __name__ == "__main__":
    audit_schema()
