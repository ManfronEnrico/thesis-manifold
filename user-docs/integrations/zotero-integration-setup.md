# Zotero Integration Setup Guide (2026-04-18)

**For:** Enrico and collaborators setting up the CMT thesis on local machines

**Last Updated:** 2026-04-18  
**Status:** Complete — Ready for distributed use

---

## Overview

The thesis uses a **live Zotero integration** that automatically syncs citations from group library `6479832`. Every time you run the sync, it fetches the latest data and regenerates:

- **`docs/literature/bibtex.bib`** — BibTeX format (source of truth, 25 papers)
- **`docs/literature/citations.json`** — JSON format (programmatic access, derived)

**Key principle:** BibTeX is authoritative; JSON is generated from it. No caching — always fresh data.

---

## Prerequisites

- **Python 3.11+** (check with `python --version`)
- **Git** (for cloning and pulling updates)
- **Zotero account** with access to group 6479832
- **~2GB disk space** for venv and dependencies

---

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ManfronEnrico/thesis-manifold.git
cd thesis-manifold
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

This installs all project dependencies from `pyproject.toml`:
- `pyzotero>=1.5.0` (Zotero API client)
- `python-dotenv>=1.0` (environment variables)
- All other thesis dependencies (pandas, scikit-learn, LangGraph, etc.)

**Expected output:**
```
Successfully installed ... pyzotero ... python-dotenv ...
```

### 4. Get Your Zotero API Key

Visit: https://www.zotero.org/settings/keys

1. Log in with your Zotero account
2. Click **"New Key"**
3. Name it: `"CMT Thesis Script"`
4. Check these permissions:
   - ✅ Read library contents
   - ✅ Access group libraries
5. Click **"Save"** and copy the key

### 5. Create `.env` File

In the project root directory, create a file named `.env`:

```bash
# Windows (PowerShell)
New-Item -Path .env -Type File

# macOS/Linux
touch .env
```

Open `.env` and add:

```
ZOTERO_API_KEY=<paste-your-key-here>
ZOTERO_GROUP_ID=6479832
```

**Example (do NOT use these values):**
```
ZOTERO_API_KEY=ZtTh8WsMUW4QJPmiRyJLIos9
ZOTERO_GROUP_ID=6479832
```

**IMPORTANT:** 
- `.env` is already in `.gitignore` — never commit it
- Keep your API key private
- Each person needs their own API key

### 6. Verify Setup

Test the integration:

```bash
python scripts/zotero_client.py
```

**Expected output:**
```
Fetching citations from Zotero group library...
  [OK] Synced BibTeX to docs/literature/bibtex.bib
  [OK] Derived citations.json from BibTeX

Fetched 25 citation items

Sample citations:
  [journalArticle] (2025) Overview of Existing Multi-Criteria Decision-Making...
  [preprint] (2023) Measuring Reliability of Large Language Models...
  ...
```

If successful, you're ready to use the integration!

---

## Daily Usage

### Refresh Citations Locally

```bash
python scripts/zotero_client.py
```

This syncs the latest papers from Zotero group library to your local files.

### Use in Python Code

```python
from scripts.zotero_client import get_citations

# Get all 25+ citations
citations = get_citations()

# Each citation is a dict with 26 fields
for c in citations:
    print(f"{c['title']} ({c['year']})")
    print(f"  DOI: {c['doi']}")
    print(f"  Authors: {c['author']}")
    print(f"  Publisher: {c['publisher']}")
```

### Use in LaTeX Document

```latex
% In your thesis .tex file
\bibliography{docs/literature/bibtex.bib}

% Cite a paper by key
\cite{DU89C8T9}  % Example key format
```

### Use in Agents/Scripts

```python
# Any agent or notebook can access fresh citations
from scripts.zotero_client import get_citations

citations = get_citations()  # Live API call
# Always up-to-date, no caching
```

---

## Data Fields Available

All 26 fields from Zotero are extracted (except `note` and `file`):

| Category | Fields |
|----------|--------|
| **Core** | key, itemType, title, shorttitle, author, year, month |
| **Publication** | journal, journalAbbreviation, publisher, volume, issue, pages |
| **Online** | url, urldate, doi, issn, isbn |
| **Content** | abstract, language, keywords |
| **Archive** | archive, archiveID, archiveLocation, repository |
| **Metadata** | copyright, libraryCatalog, callNumber, citationKey, format, genre |
| **Series** | series, seriesNumber, seriesTitle, conferenceName, proceedingsTitle |
| **Other** | section, partNumber, place, edition, originalDate, originalPublisher, extra |

**Sample entry from `citations.json`:**
```json
{
  "key": "DU89C8T9",
  "itemType": "journalArticle",
  "title": "Overview of Existing Multi-Criteria Decision-Making...",
  "authors": "Avramova Tanya, Peneva Teodora, Ivanov Aleksandar",
  "year": "2025",
  "month": "oct",
  "venue": "Technologies",
  "volume": "13",
  "issue": "10",
  "doi": "10.3390/technologies13100444",
  "url": "https://www.mdpi.com/2227-7080/13/10/444",
  "keywords": ["AHP", "MCDM", "TOPSIS", ...],
  ...
}
```

---

## File Structure

```
thesis-manifold/
├── .env                              # Your credentials (DO NOT COMMIT)
├── pyproject.toml                    # Dependencies
├── scripts/
│   └── zotero_client.py             # Main module
├── docs/
│   ├── ZOTERO_INTEGRATION_SETUP.md  # This file
│   └── literature/
│       ├── bibtex.bib               # Auto-generated (25+ papers)
│       └── citations.json           # Auto-generated (derived from BibTeX)
└── ...
```

---

## Troubleshooting

### Error: "Missing ZOTERO_API_KEY in .env"

**Cause:** No `.env` file or key is missing

**Fix:**
```bash
# Check .env exists and has the key
cat .env | grep ZOTERO_API_KEY

# Should output something like:
# ZOTERO_API_KEY=ZtTh8WsMUW4QJPmiRyJLIos9
```

### Error: "401 Unauthorized"

**Cause:** Invalid or expired API key

**Fix:**
1. Generate a new key at https://www.zotero.org/settings/keys
2. Update `.env` with the new key
3. Try again: `python scripts/zotero_client.py`

### Error: "404 Group not found"

**Cause:** Zotero group access denied or wrong group ID

**Fix:**
1. Log into https://www.zotero.org/groups/
2. Check that you're a member of "Manifold AI Thesis" group
3. Verify `.env` has `ZOTERO_GROUP_ID=6479832`
4. If not a member, ask Brian to add you

### Files aren't updating

**Cause:** Script ran but files didn't change

**Fix:**
1. Check that `docs/literature/` directory exists
2. Verify write permissions: `ls -la docs/literature/`
3. Try again with verbose output:
   ```bash
   python -c "from scripts.zotero_client import get_citations; print(get_citations())"
   ```

### "No citations found"

**Cause:** Group library empty or filter too strict

**Fix:**
1. Check Zotero: https://www.zotero.org/groups/6479832/
2. Verify items exist (should show 25+ papers)
3. Check that items aren't marked as attachments/notes in Zotero

---

## Integration with Thesis Workflow

### For Literature Review

```python
# Fetch all papers and filter by keyword
from scripts.zotero_client import get_citations

citations = get_citations()

# Find papers on agent systems
agent_papers = [c for c in citations if 'agent' in c['title'].lower()]

for paper in agent_papers:
    print(f"- {paper['title']}")
    print(f"  {paper['author']} ({paper['year']})")
```

### For Notebook Analysis

```python
# In Jupyter notebooks (e.g., SRQ analysis)
from scripts.zotero_client import get_citations
import pandas as pd

citations = get_citations()
df = pd.DataFrame(citations)

# Analyze by year, publisher, keywords, etc.
print(df.groupby('year').size())
```

### For Thesis Document

```latex
% In thesis.tex
\usepackage{natbib}
\bibliography{docs/literature/bibtex.bib}

% Cite papers
\citet{DU89C8T9}      % Author (year)
\citep{DU89C8T9}      % (Author year)
\cite{DU89C8T9}       % [citation]
```

---

## Keeping Data Fresh

### After Adding Papers to Zotero

1. Go to https://www.zotero.org/groups/6479832/
2. Add new papers to the group library (any member can do this)
3. Run sync on any machine: `python scripts/zotero_client.py`
4. Commit and push the updated files:
   ```bash
   git add docs/literature/
   git commit -m "chore(citations): update from Zotero"
   git push
   ```
5. All machines pull the latest: `git pull`

### Automated Sync (Optional)

To run sync on a schedule (e.g., daily):

```bash
# macOS/Linux: Add to crontab
0 9 * * * cd /path/to/thesis && python scripts/zotero_client.py

# Windows: Use Task Scheduler
# Action: python.exe
# Args: C:\path\to\scripts\zotero_client.py
```

---

## Common Questions

**Q: Do I need to install Zotero desktop app?**  
A: No. The API client connects directly to Zotero servers.

**Q: Can multiple people work on the same group library?**  
A: Yes. Any member can add papers. Just pull before working.

**Q: What if someone deletes a paper from the group library?**  
A: It won't appear in the next sync. The BibTeX/JSON files will update accordingly.

**Q: How often should I sync?**  
A: Whenever you add new papers, or before starting a writing session. The script is fast (~1 second).

**Q: Can I edit the BibTeX file manually?**  
A: Not recommended. It's auto-generated. If you need manual edits, do it in Zotero and re-sync.

---

## Support

- **Zotero API Docs:** https://www.zotero.org/support/dev/web_api/v3/basics
- **Pyzotero Docs:** https://pyzotero.readthedocs.io/
- **Group Library:** https://www.zotero.org/groups/6479832/
- **Ask Brian:** For credential or access issues

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-18 | Added comprehensive BibTeX extraction (26 fields, excludes note/file) |
| 2026-04-18 | Restructured to make BibTeX source of truth, JSON derived |
| 2026-04-18 | Fixed publisher extraction for preprints (arXiv detection) |
| 2026-04-15 | Initial Phase 1 setup guide |

---

## Your Zotero Configuration (Brian)

| Property | Value |
|----------|-------|
| **Personal Library ID** | 15775662 |
| **Group Library ID** | 6479832 |
| **Group Name** | CMT - CBS Master Thesis |
| **API Key** | In `.env` (ZOTERO_API_KEY) |
| **Personal Library Items** | 170 (with titles), 178 total |
| **Group Library Items** | 35 (with titles), 39 total |

### Environment Variables (Add to `.env`)

```bash
ZOTERO_API_KEY=ZtTh8WsMUW4QJPmiRyJLIos9
ZOTERO_USER_ID=15775662
ZOTERO_GROUP_ID=6479832
```

**Note**: `.env` is in `.gitignore` — never commit it.
