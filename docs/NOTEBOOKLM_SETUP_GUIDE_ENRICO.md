# NotebookLM Integration Setup Guide for Collaborators

**Prepared for**: Enrico (and any future collaborators)  
**Date**: 2026-04-18  
**Purpose**: Enable both Brian and Enrico to query NotebookLM notebooks without local PDF dependencies

---

## Overview

This guide walks you through setting up the NotebookLM integration on your machine. The system uses:

1. **Google Drive** (shared) — Papers are stored here (authoritative source)
2. **Google Drive API** (auth-based) — Lists papers from Drive
3. **NotebookLM** — Indexes papers, provides grounded Q&A
4. **Local Manifest** (git-tracked) — Metadata only, keeps both collaborators in sync

**Key insight**: You don't download PDFs locally. Everything is accessed via Google Drive API and NotebookLM.

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/ManfronEnrico/thesis-manifold.git
cd thesis-manifold
```

Verify you can see:
- `src/google_drive_integration.py` — Google Drive API wrapper
- `thesis_production_system/research/` — NotebookLM access layer
- `scripts/notebooklm_ingestion.py` — Ingestion pipeline
- `papers/ingestion_manifest.json` — Paper metadata (already has Brian's entries)

---

## Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r thesis_production_system/requirements.txt

# Verify installations
python -c "import notebooklm; import google.auth; print('All OK')"
```

**Dependencies added**:
- `notebooklm-py==0.3.4` — NotebookLM Python API
- `google-auth>=2.28.0` — Google authentication
- `google-auth-oauthlib>=1.2.0` — OAuth flow
- `google-api-python-client>=2.108.0` — Google Drive API

---

## Step 3: Set Up Google Drive API Authentication

Two options: **OAuth (interactive)** or **Service Account (automated)**.

### Option A: OAuth Flow (Recommended for Personal Use)

OAuth requires you to log in to Google once. After that, the system uses your credentials.

```bash
# No setup needed! The system will prompt you on first use.
# When you run the ingestion script, it will open a browser to authenticate.
```

**How it works**:
1. You run the ingestion script
2. Browser opens → you log in with your Google account
3. System saves credentials locally
4. Next runs use saved credentials (no re-auth needed)

### Option B: Service Account (Recommended for CI/CD)

Service account uses a JSON credentials file (non-interactive, better for servers).

**Setup service account**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable Google Drive API: `APIs & Services → Enable APIs → Google Drive API`
4. Create service account: `APIs & Services → Credentials → Create Service Account`
5. Generate JSON key: `Service Account → Keys → Add Key → JSON`
6. Download the JSON file
7. Share the Google Drive papers folder with the service account email

**Configure service account**:
```bash
# Option B.1: File path
export GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY="/path/to/service-account.json"

# Option B.2: Environment variable (JSON string)
export GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"...","...":"..."}'
```

**For Windows**:
```powershell
$env:GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY = "C:\path\to\service-account.json"
```

---

## Step 4: Set Up NotebookLM Authentication

NotebookLM requires Google authentication (uses Playwright for browser automation).

### One-Time Setup

```bash
python -c "
from notebooklm import NotebookLMClient
import asyncio

async def setup():
    client = await NotebookLMClient.from_storage()
    print('NotebookLM authenticated!')

asyncio.run(setup())
"
```

This opens a browser for you to:
1. Log in to your Google account
2. Grant NotebookLM access
3. Credentials are saved locally

**No further setup needed** — credentials are reused for future runs.

---

## Step 5: Get the Shared Google Drive Folder ID

Brian and Enrico need to share the papers folder.

**How to find folder ID**:
1. Open Google Drive
2. Open the papers folder
3. Copy the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
4. The `FOLDER_ID_HERE` is what you need

**Share with collaborator**:
1. Right-click papers folder → Share
2. Add collaborator email
3. Grant Editor access

---

## Step 6: Verify Configuration

The ingestion script auto-detects:
- ✅ OAuth credentials (if already authenticated)
- ✅ Service account (if `GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY` set)
- ✅ NotebookLM credentials (if already authenticated)

**Test the setup**:
```bash
python scripts/notebooklm_ingestion.py
```

Expected output:
```
2026-04-20 10:15:22 [INFO] === NotebookLM Ingestion Pipeline ===
2026-04-20 10:15:23 [INFO] Initializing NotebookLM client...
2026-04-20 10:15:24 [INFO] Initializing Google Drive API...
2026-04-20 10:15:25 [INFO] Loading manifest...
2026-04-20 10:15:26 [INFO] Listing papers from Google Drive...
2026-04-20 10:15:27 [INFO] Found 16 papers in Google Drive.
2026-04-20 10:15:28 [INFO] Ingesting papers...
2026-04-20 10:15:45 [INFO] Skipping smith_2023.pdf (already ingested)
...
2026-04-20 10:15:50 [INFO] Ingestion complete.
```

---

## Step 7: Query NotebookLM

Once set up, you can query the notebooks directly:

```python
import asyncio
from thesis_production_system.research import NotebookLMAccess

async def main():
    # Initialize client (uses stored credentials)
    client = NotebookLMAccess()
    await client.initialize()
    
    # Query a notebook (notebook IDs are in papers/ingestion_manifest.json)
    result = await client.ask(
        notebook_id="YOUR_NOTEBOOK_ID",
        question="What methodologies did papers use?"
    )
    
    print("Answer:", result.answer)
    print("Citations:", result.citations)
    print("Source:", result.source)  # "api" or "skill_fallback"

asyncio.run(main())
```

**Get notebook IDs from manifest**:
```python
import json

manifest = json.load(open("papers/ingestion_manifest.json"))
print(manifest["notebooks"])
# Output: {"ch2-literature": "NOTEBOOK_ID_1", "ch3-methodology": "NOTEBOOK_ID_2", ...}
```

---

## Step 8: Run as Part of the Workflow

The ingestion script is run by **both collaborators** whenever new papers are added:

```bash
# Brian adds papers to Google Drive
# Enrico pulls the latest code and manifest
git pull

# Both run ingestion (detects new papers, skips old ones)
python scripts/notebooklm_ingestion.py

# Manifest auto-updates (both are in sync)
git pull
git add papers/ingestion_manifest.json
git commit -m "chore: updated paper ingestion manifest"
git push
```

---

## Troubleshooting

### "Google Drive service not initialized"
**Cause**: Missing or invalid authentication  
**Solution**:
```bash
# Option 1: OAuth (interactive)
python -c "
from src.google_drive_integration import GoogleDriveAPI
api = GoogleDriveAPI()  # This will prompt for auth
"

# Option 2: Service account
export GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY="/path/to/credentials.json"
python scripts/notebooklm_ingestion.py
```

### "NotebookLM authentication failed"
**Cause**: Credentials not set up or expired  
**Solution**:
```bash
# Re-authenticate (clears old credentials)
python -c "
from notebooklm import NotebookLMClient
import asyncio

async def reauth():
    client = await NotebookLMClient.from_storage()
    print('Authenticated!')

asyncio.run(reauth())
"
```

### "No papers found in Google Drive"
**Cause**: Folder ID is wrong or not shared  
**Solution**:
1. Verify folder ID (see Step 5)
2. Verify folder is shared with your account
3. Verify folder contains PDFs in importance subfolders:
   - `0_not_relevant/`
   - `1_essential/`
   - `2_high/`
   - `UNSURE/`

### "Already ingested for all papers"
**Cause**: Manifest is stale or papers were moved in Drive  
**Solution**:
```bash
# Option 1: Clean manifest and re-ingest
rm papers/ingestion_manifest.json
python scripts/notebooklm_ingestion.py

# Option 2: Manual fix (edit papers/ingestion_manifest.json)
# Remove entries for papers you want to re-ingest
```

---

## Architecture Recap

```
┌─────────────────────────────────────┐
│ Google Drive (Shared Folder)        │
│ Brian + Enrico both access via API  │
└──────────────┬──────────────────────┘
               │
       [GoogleDriveAPI]
               ↓
┌──────────────────────────────────────┐
│ NotebookLM Notebooks                 │
│ ch2-literature, ch3-methodology, ... │
└──────────────┬───────────────────────┘
               │
      [NotebookLMAccess]
               ↓
┌──────────────────────────────────────┐
│ papers/ingestion_manifest.json       │
│ (git-tracked metadata)               │
│ Brian & Enrico sync via git push/pull│
└──────────────────────────────────────┘
```

**Key insight**: PDFs never go in git. Only metadata (manifest) is version-controlled. Both collaborators access the same Google Drive folder and NotebookLM notebooks.

---

## Next Steps for Enrico

1. ✅ Install dependencies (Step 2)
2. ✅ Set up Google Drive auth (Step 3)
3. ✅ Set up NotebookLM auth (Step 4)
4. ✅ Get shared folder ID from Brian (Step 5)
5. ✅ Test setup (Step 6)
6. ✅ Query NotebookLM (Step 7)
7. ✅ Integrate into your workflow (Step 8)

---

## Questions?

If you hit any issues:
1. Check **Troubleshooting** section above
2. Check `docs/NOTEBOOKLM_GDRIVE_ARCHITECTURE.md` for architecture details
3. Check `docs/NOTEBOOKLM_PHASE_0.5_COMPLETE.md` for API reference
4. Ask Brian (who set it up)

---

**Remember**: You don't need to download PDFs. Just run the ingestion script once, and everything syncs via git and Google Drive API.

Good luck! 🚀
