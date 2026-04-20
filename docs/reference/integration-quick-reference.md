# Integration Quick Reference
**For quick lookup while working**

---

## The Three Systems at a Glance

### Zotero
```
WHERE:   https://www.zotero.org/groups/6479832/
API:     python scripts/zotero_client.py
OUTPUT:  docs/literature/bibtex.bib (BibTeX keys for LaTeX)
         docs/literature/citations.json (JSON for Python)
SYNC:    On demand (run script when you add papers)
STATUS:  ✅ Ready
```

### Google Drive
```
WHERE:   https://drive.google.com/drive/folders/1cwK41FAJM_3WlpO-_9cOYMF04cjhV_LD
API:     from src.google_drive_integration import GoogleDriveAPI
PYTHON:  api.list_papers_with_metadata()
FOLDERS: 1_essential/, 2_high/, 0_not_relevant/, UNSURE/
STATUS:  ✅ Ready
```

### NotebookLM
```
WHERE:   https://notebooklm.google.com/
AUTH:    notebooklm login (browser)
API:     from thesis_production_system.research.notebooklm_access import NotebookLMAccess
PHASE:   Phase 0 (auth) ✅ | Phases 1-4 (automation) ⏳
STATUS:  🟡 Auth ready, automation deferred
```

---

## Daily Workflows

### Add a New Paper
```bash
1. Find it (arXiv, journal, etc.)
2. Add to Zotero: https://www.zotero.org/groups/6479832/
3. Download PDF from Zotero
4. Move to Google Drive (1_essential or 2_high)
5. Run: python scripts/zotero_client.py
6. Done — cite via BibTeX key
```

### Cite in Thesis
```bash
1. Check bibtex.bib for the key: \cite{AuthorYear}
2. Add to your .tex file
3. (Optional) Verify with NotebookLM: /notebooklm-ask ch2-literature "quote from [Author]?"
4. Check PDF if using NotebookLM
5. Record in docs/literature/verified_citations.md
```

### Ask NotebookLM (Manual UI)
```bash
1. Go to: https://notebooklm.google.com/
2. Choose notebook (ch2-literature, etc.)
3. Ask question in chat
4. Get answer + citations
5. Verify quote in original PDF
6. Use in thesis if verified
```

---

## Key Files

| File | Purpose | When to use |
|------|---------|------------|
| `docs/ZOTERO_SETUP_GUIDE.md` | Full Zotero reference | First-time setup |
| `ZOTERO_QUICK_REFERENCE.md` | Quick Zotero lookup | Daily use |
| `docs/GOOGLE_DRIVE_SETUP.md` | Full Drive reference | Enrico setup |
| `docs/ENRICO_GOOGLE_DRIVE_SETUP.md` | Enrico-specific Drive | Enrico setup |
| `GOOGLE_DRIVE_QUICK_START.md` | Quick Drive lookup | Daily use |
| `docs/ENRICO_SYSTEMS_ARCHITECTURE.md` | How systems connect | Understanding architecture |
| `docs/CITATION_VERIFICATION_SOP.md` | Citation safety process | Before citing NotebookLM |
| `INTEGRATION_AUDIT_AND_HANDOVER.md` | Complete audit + decisions | Strategic decisions |
| `HANDOVER_SUMMARY.md` | TL;DR version | Quick summary |

---

## Metadata Mapping

**How the same paper appears in each system:**

```
ZOTERO:
  Key: "SmithEtAl2024"
  Title: "Agents with Reasoning Improve Performance"
  Author: "Smith, J. et al."
  Year: 2024
  DOI: 10.1234/...

BIBTEX (from zotero_client.py):
  @article{SmithEtAl2024,
    author = {Smith, J. and others},
    title = {Agents with Reasoning Improve Performance},
    year = {2024},
    ...
  }

GOOGLE DRIVE:
  Name: "Smith_et_al-2024-AgentReasoningPerformance.pdf"
  Folder: "1_essential/"
  Size: 2.4 MB
  Modified: 2026-04-18

NOTEBOOKLM:
  Source Name: "Smith_et_al-2024-AgentReasoningPerformance.pdf"
  Notebook: "ch2-literature"
  Source ID: "src-uuid-abc123"
  Page 12: "Agents with reasoning improve task completion by 15%"

INGESTION MANIFEST:
  {
    "zotero_key": "SmithEtAl2024",
    "google_drive_id": "file-xyz",
    "notebooklm_source_id": "src-uuid-abc123",
    "verified": true
  }
```

---

## Common Commands

```bash
# Sync Zotero to BibTeX/JSON
python scripts/zotero_client.py

# List papers in Google Drive
python -c "from src.google_drive_integration import GoogleDriveAPI; api = GoogleDriveAPI(service_account_key_json=os.getenv('GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY')); papers = api.list_papers_with_metadata(); print(f'Found {len(papers)} papers')"

# Test Zotero connection
python -c "from scripts.zotero_client import get_citations; cites = get_citations(); print(f'{len(cites)} papers in Zotero')"

# Login to NotebookLM (if auth expires)
notebooklm login
```

---

## Citation Trust Levels

| Level | Source | Verification | Use? |
|-------|--------|------|------|
| **1** | You read PDF | You logged page number | ✅ Yes |
| **2** | NotebookLM | You checked PDF | ✅ Yes |
| **3** | NotebookLM | Not checked yet | ❌ No — verify first |
| **4** | Cited in another paper | N/A | ❌ No — use primary |

**Rule**: No Level 3 or Level 4 in final thesis.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: pyzotero` | Missing dependency | `pip install -e .` |
| `401 Unauthorized` Zotero | Bad API key | Check `.env` ZOTERO_API_KEY |
| `RuntimeError: Failed to initialize` Google Drive | Bad service account JSON | Check `.env` GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY |
| `AuthError` NotebookLM | Auth expired | `notebooklm login` or use manual UI |
| Papers not found in Drive | Wrong folder | Check: 1_essential/, 2_high/, 0_not_relevant/, UNSURE/ |

---

## Pre-Submission Checklist

Before you submit thesis to CBS:
- [ ] All citations are in `verified_citations.md`
- [ ] All citations have `Status: APPROVED`
- [ ] No citations with `Status: PENDING`
- [ ] No NotebookLM quotes without PDF verification
- [ ] BibTeX compiles correctly
- [ ] References section is complete

---

## Post-Deadline Roadmap

After May 15, implement:
- Phase 1: Automated Drive → NotebookLM ingestion
- Phase 2: Confidence scoring for citations
- Phase 3: Gap-filling research tool
- Phase 4: Defense preparation agent

For now: Stick to manual workflows (they work great).

---

## One-Liners

```bash
# "I added a paper to Zotero, update the exports"
python scripts/zotero_client.py

# "List all papers I have"
python -c "from scripts.zotero_client import get_citations; import json; print(json.dumps([{c['author'], c['title']} for c in get_citations()], indent=2))"

# "Find a paper by keyword"
python -c "from scripts.zotero_client import get_citations; target = 'reasoning'; print([c['title'] for c in get_citations() if target.lower() in c['title'].lower()])"

# "Export all citations as CSV"
python -c "from scripts.zotero_client import get_citations; import csv; w = csv.DictWriter(open('cites.csv', 'w'), get_citations()[0].keys()); w.writeheader(); w.writerows(get_citations())"
```

---

**Last updated**: 2026-04-18  
**Status**: All systems operational  
**Enrico setup guide**: See `ENRICO_ONBOARDING.md`
