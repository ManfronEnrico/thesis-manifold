# Google Drive Integration — Quick Start

## What's Set Up

✓ **MCP OAuth** — authenticated, ready to use  
✓ **Python wrapper** at `src/google_drive_integration.py`  
⏳ **Service Account** — you create, then share with Enrico

---

## For You (Right Now)

### Query papers from Claude
I can now list your papers directly. Just ask:
> "List all papers in Google Drive with metadata"

### List papers in code
```python
# Brian's setup (you've already authenticated via /mcp)
import src.google_drive_integration as gd

api = gd.GoogleDriveAPI(
    service_account_key="path/to/thesis-service-account.json"
)
papers = api.list_papers_with_metadata()
```

---

## For Enrico (After Service Account Creation)

1. You create the service account in Google Cloud (5 min) — see `docs/GOOGLE_DRIVE_SETUP.md` section 2
2. Download the JSON key file
3. Send to Enrico via encrypted channel
4. Enrico sets env var: `GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY`
5. Enrico runs same code as you — it just works

---

## Detecting New Papers

```python
api = gd.GoogleDriveAPI(service_account_key="...")

# Papers uploaded in last hour
new = api.detect_new_papers(minutes_since=60)
for p in new:
    print(f"NEW: {p['name']} ({p['size_mb']} MB)")
```

---

## Next Steps

1. **Create service account** (15 min) — follow `docs/GOOGLE_DRIVE_SETUP.md`
2. **Share JSON with Enrico** — securely
3. **Optional**: Set up automation script to detect new papers daily

---

## Docs

- Full setup: `docs/GOOGLE_DRIVE_SETUP.md`
- Python API: `src/google_drive_integration.py` (docstrings)
- This file: Quick reference only
