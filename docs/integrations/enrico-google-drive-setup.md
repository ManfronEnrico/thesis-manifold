# Google Drive Integration Setup for Enrico

**Goal**: Access the shared thesis papers Google Drive folder programmatically from your machine.

**What You Need**:
- The `GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY` value (shared securely by Brian)
- Python 3.11+ installed
- A virtual environment (venv)

---

## Step 1: Clone or Update Your Project

Make sure you have the latest code with the Google Drive integration module:

```bash
# If you haven't cloned yet:
git clone <repo-url>
cd CMT_Codebase

# If you already have it, pull the latest:
git pull origin main
```

---

## Step 2: Set Up Virtual Environment

```bash
# Create venv (if not done yet)
python -m venv .venv

# Activate venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Mac/Linux:
source .venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
# Install all project dependencies (including Google Drive packages)
pip install -e .
```

This installs from `pyproject.toml`, which now includes:
- `google-auth-oauthlib>=1.3.1`
- `google-auth-httplib2>=0.3.1`
- `google-api-python-client>=2.94.0`

---

## Step 4: Add the Service Account Key to `.env`

Brian will share the `GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY` value with you securely (encrypted email, Nextcloud, etc.).

1. Open `.env` in your project root
2. Find or create this line:
   ```bash
   GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"...","universe_domain":"googleapis.com"}'
   ```

   **Important**: 
   - Paste the entire JSON as one long line (no newlines inside the quotes)
   - Start with: `GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY='`
   - End with: `'`
   - All on one line

3. Save and close `.env`

---

## Step 5: Test Your Access

Create a test script named `test_drive.py`:

```python
import os
import sys
from pathlib import Path

# Add repo to path
repo_path = Path.cwd()
sys.path.insert(0, str(repo_path))

# Load from .env
from dotenv import load_dotenv
load_dotenv()

# Test
from src.google_drive_integration import GoogleDriveAPI

key_json = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY")
if not key_json:
    print("ERROR: GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY not found in .env")
    exit(1)

try:
    api = GoogleDriveAPI(service_account_key_json=key_json)
    papers = api.list_papers_with_metadata()
    
    print(f"SUCCESS! Found {len(papers)} papers:")
    for p in papers[:5]:
        imp = p.get('importance')
        print(f"  [{imp}] {p['name'][:50]}")
        
    # Show stats
    stats = api.get_folder_stats()
    print(f"\nFolder has {stats['total_files']} files, {stats['pdf_count']} PDFs")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
```

Run it:

```bash
python test_drive.py
```

You should see a list of papers with their importance levels (essential, high, unsure, not_relevant).

---

## Step 6: Use in Your Code

Now you can use the Google Drive API in your scripts:

### Option A: Load from Environment Variable

```python
import os
from src.google_drive_integration import GoogleDriveAPI

key_json = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY")
api = GoogleDriveAPI(service_account_key_json=key_json)

# List all papers
papers = api.list_papers_with_metadata()

# Filter by importance
essential_papers = api.get_papers_by_importance("essential")
high_papers = api.get_papers_by_importance("high")

# Get stats
stats = api.get_folder_stats()
```

### Option B: Quick One-Liners

```python
from src.google_drive_integration import quick_list_papers, quick_detect_new

# List all papers
papers = quick_list_papers()

# Detect papers uploaded/modified in last 24 hours
new = quick_detect_new(minutes=1440)

for p in new:
    print(f"[{p['importance']}] {p['name']}")
```

---

## Paper Metadata Fields

Each paper dict contains:

```python
{
    "name": "Wang_et_al-2026-AgentNoiseBench.pdf",
    "id": "1abc...",                           # Google Drive file ID
    "mimeType": "application/pdf",
    "createdTime": "2026-04-14T18:28:45.225Z",
    "modifiedTime": "2026-04-14T18:28:45.227Z",
    "created_datetime": datetime(...),         # Parsed datetime
    "modified_datetime": datetime(...),        # Parsed datetime
    "size": "471033",                          # Bytes (string)
    "size_mb": 0.45,                           # Human-readable (float)
    "extension": ".pdf",
    "importance": "essential",                 # Importance level
    "folder_path": "1_essential",              # Importance folder name
    "webViewLink": "https://drive.google.com/file/d/1abc.../view"
}
```

---

## Available Methods

### `api.list_papers_with_metadata()`
List all papers with metadata and importance classification.
```python
papers = api.list_papers_with_metadata()
print(f"Found {len(papers)} papers")
```

### `api.detect_new_papers(minutes_since=60)`
Find papers uploaded/modified in the last N minutes.
```python
new = api.detect_new_papers(minutes_since=60)  # Last hour
print(f"New papers: {len(new)}")
```

### `api.get_papers_by_importance(importance: str)`
Filter papers by importance level.
```python
essential = api.get_papers_by_importance("essential")
high = api.get_papers_by_importance("high")
unsure = api.get_papers_by_importance("unsure")
not_rel = api.get_papers_by_importance("not_relevant")
```

### `api.get_folder_stats()`
Get aggregate statistics.
```python
stats = api.get_folder_stats()
print(f"Total: {stats['total_files']} files")
print(f"PDFs: {stats['pdf_count']}")
print(f"Size: {stats['total_size_mb']} MB")
print(f"By importance: {stats['by_importance']}")
```

### `api.get_file_by_name(name: str)`
Find a specific paper by name.
```python
paper = api.get_file_by_name("Wang et al (2026)")
if paper:
    print(f"Found: {paper['webViewLink']}")
```

---

## Troubleshooting

### "ERROR: GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY not found in .env"

**Solution**: 
- Check that `.env` exists in your project root
- Check that the line `GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY='...'` is present
- Make sure it's all on one line (no line breaks inside the JSON)
- Reload your shell or Python after editing `.env`

### "RuntimeError: Failed to initialize service account"

**Solution**:
- Verify the JSON is valid (should be one long line starting with `{` and ending with `}`)
- Check that Brian shared the correct service account JSON
- Ensure the service account email is still allowed access to the shared folder

### "No module named 'src'"

**Solution**:
- Make sure you're running from the project root directory
- Verify `src/__init__.py` exists
- Check that `.venv/Scripts/python` is activated

### Encoding errors on Windows console

**Solution**: This is a known Windows issue. Use a file-writing approach instead:
```python
# Instead of printing, write to file
with open("papers_list.txt", "w", encoding="utf-8") as f:
    for p in papers:
        f.write(f"[{p['importance']}] {p['name']}\n")
```

---

## Integration with NotebookLM (Future)

Once you have this working, Brian plans to add automation to detect new papers and sync them to NotebookLM. The integration will:

1. Run periodically (e.g., daily)
2. Detect new/modified papers via `detect_new_papers()`
3. Extract important metadata (importance level, upload date, PDF link)
4. Push to NotebookLM for analysis

Your setup is the foundation for that automation.

---

## Questions?

- **Paper access issues**: Check that the Google Drive folder is still shared with the service account email
- **Code issues**: Refer to `src/google_drive_integration.py` docstrings
- **Missing papers**: Verify papers are in one of the importance folders (0_not_relevant, 1_essential, 2_high, UNSURE)

Good luck!
