"""
Nielsen / Prometheus Database Connector
----------------------------------------
Authenticates via Azure AD service principal (client credentials flow).
Credentials are loaded from .env — never hardcoded.

Requirements:
- ODBC Driver 18 for SQL Server must be installed on the machine.
  Windows: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- pip install pyodbc azure-identity python-dotenv
"""

import struct

import pandas as pd
import pyodbc
from azure.identity import ClientSecretCredential

from ai_research_framework.config import NielsenConnectionConfig, NielsenConfig


# SQL_COPT_SS_ACCESS_TOKEN — pyodbc attribute key for Azure AD token injection
_ACCESS_TOKEN_ATTR = 1256


def _get_access_token(cfg: NielsenConnectionConfig) -> bytes:
    """Obtain an Azure AD bearer token for the SQL database scope."""
    credential = ClientSecretCredential(
        tenant_id=cfg.tenant_id,
        client_id=cfg.client_id,
        client_secret=cfg.client_secret,
    )
    token = credential.get_token("https://database.windows.net/.default")
    token_bytes = token.token.encode("UTF-16-LE")
    return struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)


def get_connection(cfg: NielsenConnectionConfig | None = None) -> pyodbc.Connection:
    """
    Return an open pyodbc connection to the Nielsen/Prometheus database.

    Usage:
        with get_connection() as conn:
            df = pd.read_sql("SELECT TOP 10 * FROM csd_clean_facts_v", conn)
    """
    if cfg is None:
        cfg = NielsenConnectionConfig()

    token_struct = _get_access_token(cfg)

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={cfg.server};"
        f"DATABASE={cfg.database};"
    )

    conn = pyodbc.connect(conn_str, attrs_before={_ACCESS_TOKEN_ATTR: token_struct})
    return conn


def load_table(table: str, cfg: NielsenConnectionConfig | None = None) -> pd.DataFrame:
    """Load a full Nielsen schema table into a DataFrame."""
    nielsen_cfg = NielsenConfig()
    if table not in nielsen_cfg.schema_tables:
        raise ValueError(
            f"'{table}' is not a recognised Nielsen table. "
            f"Valid tables: {nielsen_cfg.schema_tables}"
        )
    with get_connection(cfg) as conn:
        return pd.read_sql(f"SELECT * FROM {table}", conn)


def test_connection() -> bool:
    """Quick connectivity check — returns True if login succeeds."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            print("Connection successful.")
            return True
    except Exception as exc:
        print(f"Connection failed: {exc}")
        return False


if __name__ == "__main__":
    test_connection()
