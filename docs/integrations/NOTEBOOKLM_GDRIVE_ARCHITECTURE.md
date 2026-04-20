# NotebookLM + Google Drive Architecture (Integrated)

**Date**: 2026-04-18  
**Status**: Fully integrated via GoogleDriveAPI + NotebookLMAccess  
**Integration**: `src/google_drive_integration.py` → `scripts/notebooklm_ingestion.py` → `thesis_production_system/research/`  
**Requirement**: Both collaborators can run code without local PDF dependencies

---

## Architecture

```
┌──────────────────────────────────────────┐
│ Google Drive (Shared Folder)             │
│ /Thesis Papers/                          │
│  ├── 0_not_relevant/ (papers)            │
│  ├── 1_essential/ (papers)               │
│  ├── 2_high/ (papers)                    │
│  └── UNSURE/ (papers)                    │
│ Accessed via GoogleDriveAPI              │
└────────────────┬─────────────────────────┘
                 │ [src/google_drive_integration.py]
                 │ Lists papers with metadata
                 ↓
┌──────────────────────────────────────────┐
│ NotebookLM Ingestion Script              │
│ [scripts/notebooklm_ingestion.py]        │
│                                          │
│ For each paper:                          │
│ - List from Drive via GoogleDriveAPI     │
│ - Add to NotebookLM via NotebookLMAccess │
│ - Update manifest with metadata          │
└────────────────┬─────────────────────────┘
                 ↓ Dual integration
        ┌────────┴────────┐
        ↓                 ↓
    [NotebookLM]  [Manifest JSON]
    Notebooks      (git-tracked)
    ch2-...        papers/
    ch3-...        ingestion_
    ...            manifest.json

Result: Both collaborators query same notebooks
        without local PDF storage
```

## Key Points

### 1. Source of Truth: Google Drive
- Papers live in a **shared Google Drive folder**
- Both collaborators can access the same papers without downloading
- PDFs are never committed to git (not in `papers/` folder)
- No local file dependencies between collaborators

### 2. Manifest as Bridge
`papers/ingestion_manifest.json` tracks:
```json
{
  "notebooks": {
    "ch2-literature": "NOTEBOOK_ID_123"
  },
  "sources": {
    "DRIVE_FILE_ID_123": {
      "file_name": "smith_2023_forecasting.pdf",
      "gdrive_file_id": "DRIVE_FILE_ID_123",
      "gdrive_link": "https://drive.google.com/file/d/...",
      "notebook": "ch2-literature",
      "notebooklm_source_id": "NLMID_456",
      "added_at": "2026-04-20T...",
      "verified": false
    }
  }
}
```

This manifest is **checked into git**, so both collaborators know:
- Which papers have been ingested
- Which NotebookLM IDs to query
- Status of verification

### 3. Ingestion Script Workflow
```python
# Install dependencies
pip install notebooklm google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Set up Google Drive credentials
# Option 1 (local): Use OAuth flow
# Option 2 (server): Set GOOGLE_APPLICATION_CREDENTIALS

# Run ingestion
python scripts/notebooklm_ingestion.py

# Output:
# - Updates manifest.json with new ingestions
# - Verifies notebook integrity
# - Both collaborators' manifest stays in sync via git
```

---

## For Collaborators

### Collaborator A (You)
1. Share Google Drive folder with Collaborator B
2. Upload papers to `/Thesis Papers/ch2-literature/`, etc.
3. Run ingestion script
4. Manifest auto-updates in git
5. Commit manifest

### Collaborator B
1. Pull git repo (includes updated manifest)
2. No PDFs to download (they reference Drive)
3. Run same ingestion script (skips already-ingested papers)
4. Can query NotebookLM directly using notebook IDs from manifest
5. All queries work; no local file dependencies

---

## Configuration

Before running the script, set these environment variables:

```bash
# Shared Google Drive folder structure
export GDRIVE_ROOT_FOLDER_ID="YOUR_SHARED_FOLDER_ID"

# Chapter-specific folder IDs (find these in Drive URL)
export GDRIVE_CH2_FOLDER_ID="folder_id_for_ch2"
export GDRIVE_CH3_FOLDER_ID="folder_id_for_ch3"
# ... etc

# Google Drive authentication
# Option 1: OAuth (interactive)
# Script will prompt you to authenticate

# Option 2: Service account (automated)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

Or edit the script directly:
```python
GDRIVE_ROOT_FOLDER_ID = "YOUR_FOLDER_ID"
GDRIVE_CHAPTER_FOLDERS = {
    "ch2-literature": "FOLDER_ID",
    "ch3-methodology": "FOLDER_ID",
    ...
}
```

---

## Running the Ingestion

```bash
# Navigate to codebase
cd /path/to/CMT_Codebase

# Install dependencies (one-time)
pip install notebooklm google-auth google-auth-oauthlib google-api-python-client

# Run ingestion
python scripts/notebooklm_ingestion.py

# Output example:
# 2026-04-20 10:15:22 [INFO] === NotebookLM Ingestion Pipeline (Google Drive Source) ===
# 2026-04-20 10:15:23 [INFO] Initializing NotebookLM client...
# 2026-04-20 10:15:24 [INFO] Initializing Google Drive service...
# 2026-04-20 10:15:25 [INFO] Loading manifest from papers/ingestion_manifest.json...
# 2026-04-20 10:15:26 [INFO] Ensuring chapter notebooks exist...
#   ch2-literature: Using existing notebook NOTEBOOK_ID_123
# 2026-04-20 10:15:27 [INFO] Ingesting papers from Google Drive...
#   ch2-literature: Found 5 PDFs on Google Drive
#   Ingesting smith_2023.pdf...
#   Skipping johnson_2022.pdf (already ingested)
# ...
# 2026-04-20 10:15:45 [INFO] Ingested 3 new papers from Google Drive.
# 2026-04-20 10:15:46 [INFO] Manifest saved to papers/ingestion_manifest.json
# 2026-04-20 10:15:47 [INFO] Verifying manifest integrity...
# 2026-04-20 10:15:48 [INFO] Manifest integrity verified.
# 2026-04-20 10:15:49 [INFO] Ingestion complete. All papers verified.
```

---

## No Local Files Needed

Agents can query NotebookLM directly using notebook IDs from the manifest:

```python
from thesis_production_system.research import NotebookLMAccess

# Load manifest to get notebook IDs
import json
manifest = json.load(open("papers/ingestion_manifest.json"))
ch2_notebook_id = manifest["notebooks"]["ch2-literature"]

# Query without any local files
access = NotebookLMAccess()
result = await access.ask(ch2_notebook_id, "What methods did papers use?")

# Works for both collaborators — no PDF downloads needed
```

---

## Manifest Reconciliation

The script verifies that:
1. Every paper in manifest is actually in the NotebookLM notebook
2. No papers were deleted from notebooks unexpectedly
3. Manifest ↔ Notebook state stays in sync

If integrity check fails, you'll see:
```
[ERROR] Integrity issues found:
[ERROR]   smith_2023.pdf: manifest ID NLMID_456 not in ch2-literature notebook
```

**Recovery**: Re-ingest the paper or update manifest manually (both operations are safe).

---

## Benefits of This Architecture

✅ **No Local File Dependencies**: Both collaborators share the same Drive folder  
✅ **Git-Tracked Manifest**: Keeps metadata in sync without committing PDFs  
✅ **Scalable**: Can ingest hundreds of papers without repo bloat  
✅ **Reproducible**: Manifest captures exactly which papers are indexed  
✅ **Collaborative**: Both collaborators run the same script, same results  
✅ **Cost-Free**: Uses Google Drive free tier + NotebookLM  

---

## Troubleshooting

### "Google Drive service not initialized"
**Cause**: Missing authentication credentials  
**Solution**:
```bash
# Option 1: OAuth flow (interactive)
python -c "from google.colab import auth; auth.authenticate_user()"

# Option 2: Service account (server)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

### "No PDFs found in folder"
**Cause**: Folder ID is wrong or papers aren't uploaded  
**Solution**: Verify folder ID matches your shared Drive folder

### "Already ingested" for all papers
**Cause**: Manifest is outdated or papers were deleted from Drive  
**Solution**: Delete manifest entry, re-run ingestion

---

## Next Steps

1. Create shared Google Drive folder
2. Upload papers to chapter subfolders
3. Share folder with collaborator
4. Configure folder IDs in ingestion script
5. Run `python scripts/notebooklm_ingestion.py`
6. Commit manifest to git
7. Both collaborators can now query NotebookLM

---

**Key Insight**: Papers live in Drive. Only metadata (manifest) lives in git. Both collaborators query the same NotebookLM notebooks without local file dependencies.
