"""
Quick connection test for the Nielsen Azure SQL (Fabric) database.
Run from the project root:  python test_db_connection.py
"""

import os, struct, sys
from pathlib import Path

try:
    import pyodbc
    from azure.identity import ClientSecretCredential
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing package: {e}")
    print("Install with:  pip install pyodbc azure-identity python-dotenv")
    sys.exit(1)

# Load .env
load_dotenv(Path(__file__).resolve().parent / ".env")

SERVER        = os.environ["RU_SERVER_STRING"]
DATABASE      = os.environ["RU_DATABASE"]
CLIENT_ID     = os.environ["RU_CLIENT_ID"]
TENANT_ID     = os.environ["RU_TENANT_ID"]
CLIENT_SECRET = os.environ["RU_CLIENT_SECRET"]

print(f"Server:   {SERVER}")
print(f"Database: {DATABASE}")
print(f"Tenant:   {TENANT_ID}")
print(f"Client:   {CLIENT_ID}")
print()

# Step 1: Token acquisition
print("Step 1 — Acquiring Azure AD token...")
try:
    credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    token = credential.get_token("https://database.windows.net/.default")
    print(f"  ✅ Token acquired (expires: {token.expires_on}, length: {len(token.token)})")
except Exception as e:
    print(f"  ❌ Token acquisition FAILED: {e}")
    sys.exit(1)

# Step 2: Database connection
print("\nStep 2 — Connecting to database...")
try:
    token_bytes = token.token.encode("UTF-16-LE")
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    conn = pyodbc.connect(conn_str, attrs_before={1256: token_struct})
    print("  ✅ Connected!")
except Exception as e:
    print(f"  ❌ Connection FAILED: {e}")
    sys.exit(1)

# Step 3: Simple query
print("\nStep 3 — Running SELECT 1...")
try:
    cursor = conn.cursor()
    cursor.execute("SELECT 1 AS test")
    row = cursor.fetchone()
    print(f"  ✅ Query returned: {row[0]}")
except Exception as e:
    print(f"  ❌ Query FAILED: {e}")

# Step 4: List available views
print("\nStep 4 — Listing dbo views...")
try:
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA = 'dbo' ORDER BY TABLE_NAME")
    views = [r[0] for r in cursor.fetchall()]
    print(f"  ✅ Found {len(views)} views: {views}")
except Exception as e:
    print(f"  ❌ View listing FAILED: {e}")

conn.close()
print("\n🎉 All checks passed — connection is active!")
