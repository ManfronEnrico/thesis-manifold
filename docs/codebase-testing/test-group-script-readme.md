# test_group.py — Reusable Zotero Group Library Test Script

**Created**: 2026-04-15  
**Status**: ✅ Working  
**Reusability**: High — Can deploy to other projects

---

## What It Does

Tests your Zotero group library connection and displays all items with:
- Item number
- Title
- Item type (paper, preprint, attachment, note, etc.)

**Output**: Formatted list of all 39 items in your group library

---

## Usage

### Basic Usage

```bash
python test_group.py
```

### From PowerShell (Windows)

```powershell
python test_group.py
```

### From Any Directory

```bash
cd path/to/CMT_Codebase
python test_group.py
```

---

## Requirements

| Requirement | Status | How to Install |
|------------|--------|----------------|
| `pyzotero` | ✅ Installed | `pip install pyzotero` or `uv add pyzotero` |
| `.env` file | ✅ Created | Already in project root |
| `ZOTERO_GROUP_ID` | ✅ Add manually | Add `ZOTERO_GROUP_ID=6479832` to `.env` |
| `ZOTERO_API_KEY` | ✅ In `.env` | Already present |
| Python 3.11+ | ✅ Available | You have it in `.venv` |

---

## What the Script Does (Line by Line)

```python
load_dotenv(env_path)  # Load .env variables
```
→ Reads credentials from `.env`

```python
zot = Zotero(
    library_id=os.environ['ZOTERO_GROUP_ID'],  # From .env
    library_type='group',
    api_key=os.environ['ZOTERO_API_KEY']
)
```
→ Connects to your Zotero group library

```python
items = zot.everything(zot.items(limit=100))
```
→ Fetches all items (up to 100)

```python
for i, item in enumerate(items, 1):
    title = item["data"].get("title", "Untitled")
    item_type = item["data"].get("itemType", "?")
```
→ Loops through items and extracts title and type

---

## Sample Output

```
Connecting to Zotero group: 6479832

Fetching items... OK (39 items)

======================================================================
GROUP LIBRARY CONTENTS
======================================================================

 1. Full Text PDF
    Type: attachment

 2. Sample, Predict, then Proceed: Self-Verification Sampling for Tool Use of LLMs
    Type: book

 3. Snapshot
    Type: attachment

... (36 more items) ...

39. Toolformer: Language Models Can Teach Themselves to Use Tools
    Type: journalArticle

======================================================================
Total: 39 items
======================================================================
```

---

## Error Handling

**If you see an error**, the script will tell you exactly what's wrong:

| Error | Cause | Fix |
|-------|-------|-----|
| `ERROR: .env file not found` | `.env` missing | Create `.env` in project root |
| `ERROR: ZOTERO_GROUP_ID not found` | Missing from `.env` | Add `ZOTERO_GROUP_ID=6479832` to `.env` |
| `ERROR: ZOTERO_API_KEY not found` | Missing from `.env` | Already should be there; check `.env` |
| `403 Forbidden` | Invalid API key | Check https://www.zotero.org/settings/keys |
| `Connection timeout` | Network issue | Check your internet connection |

---

## Reusing in Other Projects

To use this script in another project:

1. **Copy the script**:
   ```bash
   cp test_group.py /path/to/other/project/
   ```

2. **Add `.env` to that project**:
   ```
   ZOTERO_GROUP_ID=6479832
   ZOTERO_API_KEY=ZtTh8WsMUW4QJPmiRyJLIos9
   ```

3. **Install pyzotero** (if not already installed):
   ```bash
   pip install pyzotero
   ```

4. **Run it**:
   ```bash
   python test_group.py
   ```

**That's it!** The script is portable and doesn't depend on any CMT_Codebase-specific files.

---

## Variations (Copy-Paste Ready)

### Show Only Papers (Filter Attachments)

```python
for i, item in enumerate(items, 1):
    item_type = item["data"].get("itemType", "?")
    if item_type in ["journalArticle", "conferencePaper", "book", "thesis", "preprint"]:
        title = item["data"].get("title", "Untitled")
        print(f"{i}. {title} ({item_type})")
```

### Show Authors and Year

```python
for item in items:
    title = item["data"].get("title", "Untitled")
    creators = item["data"].get("creators", [])
    year = item["data"].get("year", "?")
    
    authors = ", ".join(c.get("lastName", "") for c in creators[:2])
    print(f"- {title}")
    print(f"  Authors: {authors}")
    print(f"  Year: {year}")
```

### Export as BibTeX

```python
zot.add_parameters(format='bibtex')
bibtex_items = zot.everything(zot.items(limit=100))
# bibtex_items now contains BibTeX-formatted entries
```

---

## File Location

```
CMT_Codebase/
└── test_group.py ← You are here
```

---

## Next Steps

- ✅ Run `python test_group.py` to verify connection
- ✅ Review your 39 items (11 papers + 28 attachments/notes)
- ⬜ Plan Phase 2: Bidirectional sync (when ready)
- ⬜ Deploy to other projects as needed

---

## Troubleshooting Checklist

- [ ] `.env` file exists in project root
- [ ] `ZOTERO_GROUP_ID=6479832` is in `.env`
- [ ] `ZOTERO_API_KEY` is in `.env`
- [ ] `pyzotero` is installed (`pip list | grep pyzotero`)
- [ ] You have internet connection
- [ ] API key is valid (check https://www.zotero.org/settings/keys)
- [ ] You're not in a VPN/firewall that blocks API calls

---

**Status**: Ready to use  
**Portability**: High — Works on any project with same `.env` setup  
**Maintenance**: None required
