# Zotero Quick Reference

**For fast lookup — full guide in `docs/ZOTERO_INTEGRATION_SETUP.md`**

---

## Setup (One-Time, 5 minutes)

```bash
# 1. Get API key: https://www.zotero.org/settings/keys

# 2. Create .env
echo ZOTERO_API_KEY=<your-key> > .env
echo ZOTERO_GROUP_ID=6479832 >> .env

# 3. Install
pip install -e .

# 4. Test
python scripts/zotero_client.py
# Should output:
# Fetched 25 citation items
# [OK] Synced BibTeX...
# [OK] Derived citations.json...
```

---

## Daily Use

```bash
# Sync latest papers
python scripts/zotero_client.py

# Use in Python
from scripts.zotero_client import get_citations
cites = get_citations()  # Live API call, always fresh
```

---

## In Python

```python
from scripts.zotero_client import get_citations

# Get all citations
cites = get_citations()  # 25+ papers

# Each has: key, title, author, year, month, journal, publisher,
#           doi, url, abstract, keywords, archiveID, and 14+ more fields

for c in cites:
    print(f"{c['author']} - {c['title']} ({c['year']})")

# Filter
agents = [c for c in cites if 'agent' in c['title'].lower()]
recent = [c for c in cites if c['year'] == '2025']
```

---

## In LaTeX

```latex
\bibliography{docs/literature/bibtex.bib}

\cite{DU89C8T9}
```

---

## Generated Files

| File | Format | Auto-Generated |
|------|--------|---|
| `docs/literature/bibtex.bib` | BibTeX (source of truth) | Yes, every call |
| `docs/literature/citations.json` | JSON (programmatic) | Yes, every call |

---

## Available Fields (26 total)

**Core:** key, itemType, title, shorttitle, author, year, month

**Publication:** journal, journalAbbreviation, publisher, volume, issue, pages

**Online:** url, urldate, doi, issn, isbn

**Content:** abstract, language, keywords

**Archive:** archiveID, repository, archive, archiveLocation

**Metadata:** copyright, libraryCatalog, callNumber, citationKey, format, genre

**Series:** series, seriesNumber, conferenceName, proceedingsTitle, eventPlace

**Other:** section, partNumber, place, edition, originalDate, originalPublisher, extra

---

## Common Commands

```bash
# Check config
cat .env

# Test
python -c "from scripts.zotero_client import get_citations; print(len(get_citations()))"

# Use in notebook
import pandas as pd
from scripts.zotero_client import get_citations
df = pd.DataFrame(get_citations())
print(df.groupby('year').size())
```

---

## Troubleshooting

```bash
# Missing key?
# → Generate at https://www.zotero.org/settings/keys

# 401 Unauthorized?
# → Check key is correct in .env

# No citations?
# → Verify you're member of group 6479832
# → Check https://www.zotero.org/groups/6479832/

# Permission denied on .env?
# → Ensure write access: chmod 600 .env
```

---

## Resources

- **Full Setup:** `docs/ZOTERO_INTEGRATION_SETUP.md`
- **Group Library:** https://www.zotero.org/groups/6479832/
- **API Keys:** https://www.zotero.org/settings/keys
- **Pyzotero:** https://pyzotero.readthedocs.io/

---

**Last Updated:** 2026-04-18  
**Status:** ✅ Complete — 25 papers, 26 fields, live sync
