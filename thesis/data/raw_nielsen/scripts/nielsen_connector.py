"""
Nielsen / Microsoft Fabric Data Warehouse connector.
Authenticates using a Service Principal (Entra ID) and returns a pyodbc connection.

Usage:
    from thesis.data.nielsen.scripts.nielsen_connector import get_connection
    conn = get_connection()
    df = pd.read_sql("SELECT TOP 10 * FROM dbo.csd_clean_facts_v", conn)
    conn.close()

Requires:
    - .env file in project root with RU_* credentials
    - ODBC Driver 18 for SQL Server (brew install msodbcsql18)
    - pip install pyodbc azure-identity python-dotenv
"""

# %%

import os
import struct
import pyodbc
from pathlib import Path
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv

# %%

# Load credentials from .env in project root
_env_path = Path(__file__).resolve().parents[4] / ".env"

print(_env_path)

# %%

load_dotenv(_env_path)


SERVER   = os.environ["RU_SERVER_STRING"]
DATABASE = os.environ["RU_DATABASE"]
CLIENT_ID     = os.environ["RU_CLIENT_ID"]
TENANT_ID     = os.environ["RU_TENANT_ID"]
CLIENT_SECRET = os.environ["RU_CLIENT_SECRET"]

ODBC_DRIVER = "ODBC Driver 18 for SQL Server"


def _get_token() -> bytes:
    """Obtain an Entra ID access token for the Fabric data warehouse."""
    credential = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    token = credential.get_token("https://database.windows.net/.default")
    # pyodbc requires the token packed as a UTF-16-LE byte struct
    token_bytes = token.token.encode("UTF-16-LE")
    return struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)


def get_connection() -> pyodbc.Connection:
    """
    Return an open pyodbc connection to the Nielsen_clean Fabric warehouse.
    Caller is responsible for closing the connection.
    """
    token_struct = _get_token()
    connection_string = (
        f"Driver={{{ODBC_DRIVER}}};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    # SQL_COPT_SS_ACCESS_TOKEN = 1256
    conn = pyodbc.connect(connection_string, attrs_before={1256: token_struct})
    return conn


def test_connection() -> None:
    """Quick smoke test â€” prints top-5 rows from each key view."""
    print(f"Connecting to {SERVER} / {DATABASE} ...")
    conn = get_connection()
    print("Connection OK")

    views = [
        "csd_clean_dim_market_v",
        "csd_clean_dim_period_v",
        "csd_clean_dim_product_v",
        "csd_clean_facts_v",
    ]
    for view in views:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT TOP 3 * FROM dbo.{view}")
            rows = cursor.fetchall()
            cols = [d[0] for d in cursor.description]
            print(f"\n--- {view} ({len(cols)} columns) ---")
            print("Columns:", cols)
            for row in rows:
                print(dict(zip(cols, row)))
        except Exception as e:
            print(f"  ERROR on {view}: {e}")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    test_connection()
