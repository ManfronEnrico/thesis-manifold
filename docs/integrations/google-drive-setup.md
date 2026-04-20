# Google Drive Integration Setup

Single source of truth for thesis PDF papers. Two access patterns:
- **MCP (OAuth)** for interactive Claude queries
- **Service Account** for programmatic access (Enrico + automation)

## 1. MCP Setup (Already Done ✓)

Your OAuth token is authenticated. You can now query Google Drive directly via Claude:

```python
# In Claude or via scripts:
from google.ai import GoogleDriveAPI  # Uses MCP
papers = api.list_papers_with_metadata()
```

**When to use MCP:**
- Interactive queries from Claude
- Exploratory analysis
- One-off lookups

---

## 2. Service Account Setup (For Enrico + Automation)

### Step 1: Create Service Account in Google Cloud

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select or create a project
3. Enable **Google Drive API** (APIs & Services → Enable APIs and Services)
4. Go to **IAM & Admin → Service Accounts**
5. **Create Service Account**:
   - Name: `thesis-papers-reader`
   - Description: `Read-only access to CBS thesis PDF papers`
   - Click **Create and Continue** (skip optional steps)
6. **Create Key**:
   - In the service account details, go to **Keys** tab
   - **Add Key → Create new key**
   - Choose **JSON**
   - Download the file → save as `thesis-service-account.json`

### Step 2: Share Google Drive Folder with Service Account

1. Get the service account email from the JSON key file (field: `client_email`)
2. Open Google Drive folder with papers: [PDF Papers](https://drive.google.com/drive/folders/1cwK41FAJM_3WlpO-_9cOYMF04cjhV_LD)
3. **Share → Add** the service account email
4. Grant **Viewer** access (read-only)

### Step 3: Enrico's Setup

1. You share the `thesis-service-account.json` file with Enrico securely (encrypted email/Nextcloud)
2. Enrico saves it locally in his project: `.env` or environment variable
3. Set environment variable:

```bash
# Linux/Mac
export GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY="/path/to/thesis-service-account.json"

# Windows PowerShell
$env:GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY="C:\path\to\thesis-service-account.json"
```

---

## 3. Python Wrapper Functions

Located at: `src/google_drive_integration.py`

### Basic Usage

```python
from src.google_drive_integration import GoogleDriveAPI

# Initialize with service account
api = GoogleDriveAPI(
    service_account_key="/path/to/thesis-service-account.json"
)

# List all papers with metadata
papers = api.list_papers_with_metadata()
for p in papers:
    print(f"{p['name']}: {p['size_mb']} MB, modified {p['modified_datetime']}")

# Detect new/updated papers in last 60 minutes
new = api.detect_new_papers(minutes_since=60)
print(f"Found {len(new)} new papers")

# Get folder statistics
stats = api.get_folder_stats()
print(f"Total PDFs: {stats['pdf_count']}, Size: {stats['total_size_mb']} MB")

# Find paper by name
paper = api.get_file_by_name("Wang et al (2026) - AgentNoiseBench.pdf")
if paper:
    print(f"Found: {paper['webViewLink']}")
```

### One-Line Shortcuts

```python
from src.google_drive_integration import quick_list_papers, quick_detect_new

# Requires GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY env var
papers = quick_list_papers()
new = quick_detect_new(minutes=60)
```

### Return Format

Each paper dict contains:
```python
{
    "name": "Wang et al (2026) - AgentNoiseBench.pdf",
    "id": "1abc...",
    "mimeType": "application/pdf",
    "createdTime": "2026-04-14T18:28:45.225Z",
    "modifiedTime": "2026-04-14T18:28:45.227Z",
    "created_datetime": datetime(...),      # Parsed
    "modified_datetime": datetime(...),     # Parsed
    "size": "471033",                       # Bytes
    "size_mb": 0.45,                        # Human-readable
    "extension": ".pdf",
    "webViewLink": "https://drive.google.com/file/d/..."
}
```

---

## 4. Which Access Method to Use

| Task | Method | Why |
|------|--------|-----|
| Interactive query (Claude) | MCP (OAuth) | Already authenticated, no setup |
| Automation script (detect new papers) | Service Account | Runs without user interaction |
| Batch sync to NotebookLM | Service Account | Scheduled jobs, team access |
| One-off lookup | Either | Both work, MCP is simpler |
| Collaborative access (you + Enrico) | Service Account | Shared credential via JSON |

---

## 5. Integration with NotebookLM

Once you have papers listed:

```python
api = GoogleDriveAPI(service_account_key="...")
new_papers = api.detect_new_papers(minutes_since=1440)  # Last 24h

# Then push to NotebookLM (future skill)
for paper in new_papers:
    notebook_api.upload_pdf(paper["webViewLink"])
```

---

## 6. Security Notes

- **Service account key is sensitive** — treat like a password
- Share with Enrico only via encrypted channels
- Permissions are read-only (Viewer role)
- If compromised, regenerate the key in Google Cloud Console
- OAuth tokens expire automatically; service account keys don't (rotate periodically)

---

## 7. Troubleshooting

**"Failed to initialize service account"**
- Check JSON file path is correct
- Verify file is valid JSON
- Ensure credentials have Google Drive API enabled

**"Service account not authorized to access folder"**
- Verify you shared the folder with the service account email
- Check permissions are "Viewer" or higher

**"Module not found: google.oauth2"**
- Install dependencies: `pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client`

---

## 8. Folder ID Reference

- **Papers folder**: `1cwK41FAJM_3WlpO-_9cOYMF04cjhV_LD`
- Main thesis folder: `1A4Kt1ME7jBatjDyVp-Nf-hyNTSvNWu1s`
