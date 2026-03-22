# Data Access Setup Guide
> Nielsen / Prometheus Database — Cross-platform setup (Windows & macOS)

---

## What is this?

We have credentials to connect to the **Nielsen/Prometheus SQL database** hosted on Azure.
These credentials were shared once via a one-time secret and must be kept secure.

This guide explains how to get your local machine connected to the database.

---

## What is and isn't on GitHub

| What | On GitHub? | Why |
|---|---|---|
| All Python code (`ai_research_framework/`, etc.) | ✅ Yes | Safe — no secrets |
| `.env.example` (template, no values) | ✅ Yes | Safe — just variable names |
| `docs/` and `README.md` | ✅ Yes | Safe |
| `.env` (actual credentials) | ❌ **No** | Contains secrets — blocked by `.gitignore` |
| Any data files (`.csv`, `.xlsx`, `.parquet`, etc.) | ❌ **No** | Confidential — blocked by `.gitignore` |
| CBS guideline PDFs | ❌ **No** | Large files, not needed on GitHub |

> **Rule of thumb:** If you can see sensitive values in the file, it must not be on GitHub.
> The `.gitignore` at the repo root enforces all of this automatically.

---

## Setup Steps

### Step 1 — Clone the repo (if not already done)

```bash
git clone https://github.com/ManfronEnrico/thesis-manifold.git
cd thesis-manifold
```

---

### Step 2 — Create your `.env` file

The repo contains `.env.example` — a template with no values.
Copy it and fill in the credentials (ask your co-author for the values):

**macOS / Linux:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

Then open `.env` in any text editor and fill in all five values:

```
RU_SERVER_STRING=<value from co-author>
RU_DATABASE=<value from co-author>
RU_CLIENT_ID=<value from co-author>
RU_TENANT_ID=<value from co-author>
RU_CLIENT_SECRET=<value from co-author>
```

> Never commit `.env` to git. It is already listed in `.gitignore` — but double-check with
> `git status` before any commit. You should never see `.env` in the output.

---

### Step 3 — Install ODBC Driver 18 for SQL Server

This is a system-level driver (not a Python package) and must be installed separately on each machine.

#### Windows

1. Download from Microsoft:
   Search: **"Download ODBC Driver 18 for SQL Server"** → microsoft.com
   Direct path: `sqlchoice.azurewebsites.net` → ODBC Driver 18 → Windows x64

2. Run the `.msi` installer — click through defaults

3. Verify installation:
```powershell
Get-OdbcDriver -Name "ODBC Driver 18 for SQL Server"
```
Should return one result. If empty, the install did not complete.

#### macOS

Using Homebrew:

```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18
```

Verify:
```bash
odbcinst -q -d -n "ODBC Driver 18 for SQL Server"
```

> Apple Silicon (M1/M2/M3): this works natively — no Rosetta needed as of driver v18.3+.

---

### Step 4 — Set up Python virtual environment

```bash
python -m venv .venv
```

**Activate — macOS/Linux:**
```bash
source .venv/bin/activate
```

**Activate — Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Activate — Windows (cmd):**
```cmd
.venv\Scripts\activate.bat
```

---

### Step 5 — Install Python dependencies

```bash
pip install -r ai_research_framework/requirements.txt
```

Key packages this installs for the database connection:

| Package | Purpose |
|---|---|
| `pyodbc` | Python interface to ODBC Driver 18 |
| `azure-identity` | Azure AD service principal authentication |
| `python-dotenv` | Loads `.env` file into `os.environ` |

---

### Step 6 — Test the connection

```bash
python -m ai_research_framework.data.nielsen_connector
```

Expected output:
```
Connection successful.
```

If it fails, see the Troubleshooting section below.

---

### Step 7 — Explore the data (first time)

Run the exploration script to get a first look at what's in the database:

```bash
python scripts/explore_nielsen.py
```

This prints:
- All available tables/views in the schema
- Column names and data types for the 4 known tables
- Row counts and date range
- First 10 rows of `csd_clean_facts_v`

---

## How the connection works (brief)

We authenticate using an **Azure AD Service Principal** — think of it as a dedicated "app account" that has read access to the database. Instead of a username/password, we use:

- `RU_CLIENT_ID` + `RU_CLIENT_SECRET` → proves who we are to Azure
- `RU_TENANT_ID` → identifies which Azure organisation
- Azure issues a short-lived token → passed to the SQL driver
- `RU_SERVER_STRING` + `RU_DATABASE` → tells pyodbc which server/database to connect to

The flow in code: `azure-identity` → token → `pyodbc` → SQL Server.
The credentials never touch the database directly — Azure validates them first.

---

## Troubleshooting

### `pyodbc.Error: ('01000', "[01000] [unixODBC]...")`
The ODBC driver is not installed or not found. Redo Step 3.

### `KeyError: 'RU_SERVER_STRING'`
Your `.env` file is missing or not filled in. Check that `.env` exists in the repo root and all 5 variables have values.

### `azure.core.exceptions.ClientAuthenticationError`
The credentials are wrong or expired. Ask your co-author to re-share the `.env` values.

### `SSL: CERTIFICATE_VERIFY_FAILED` (macOS)
Run:
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

### `ModuleNotFoundError: No module named 'pyodbc'`
Your virtual environment is not activated or dependencies weren't installed. Redo Steps 4–5.

---

## Security reminders

- The `.env` file contains credentials — treat it like a password
- Never share it over email or Slack — use Signal or WhatsApp
- Never commit it to git (`git status` should never show `.env`)
- The Nielsen data itself must stay local — do not upload to any cloud storage
