# Zotero Quick Reference Card

**Print this or bookmark it!**

---

## Your Zotero Setup (Discovered 2026-04-15)

```
Personal Library ID:  15775662
Group Library ID:     6479832 ← Use this for thesis!
Group Name:           CMT - CBS Master Thesis
API Key:              In .env (ZOTERO_API_KEY)
```

---

## Manual Step (Do This First!)

Edit `.env` and add:
```
ZOTERO_GROUP_ID=6479832
```

---

## Test Connection (Copy-Paste in Terminal)

```bash
cd C:\Users\brian\OneDrive\Documents\02\ -\ A\ -\ Areas\MSc.\ Data\ Science\2026-03\ -\ CBS\ Master\ Thesis\CMT_Codebase

python << 'EOF'
import os
from pathlib import Path
from pyzotero import Zotero
from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env")

zot = Zotero(
    library_id="6479832",
    library_type='group',
    api_key=os.environ['ZOTERO_API_KEY']
)

items = zot.everything(zot.items(limit=100))
print(f"Group library: {len(items)} items\n")

for item in items[:10]:
    title = item["data"].get("title", "Untitled")
    print(f"  - {title}")
EOF
```

---

## What's in Your Group Library

| Type | Count |
|------|-------|
| Academic Papers (journalArticle) | 5 |
| Preprints | 6 |
| PDF Attachments | 23 |
| Notes | 5 |
| **Total** | **39** |

### Key Papers
1. Sample, Predict, then Proceed (Tool Use in LLMs)
2. Hybrid AI & LLM Decision Support (Industrial)
3. Cost-Aware ML 3PL Supply Chain Forecasting
4. DSS4EX: AI Pipeline Decision Support
5. Toolformer: LMs Teaching Themselves Tools

---

## File Locations

| File | Purpose |
|------|---------|
| `docs/ZOTERO_SETUP_GUIDE.md` | Full reference (start here) |
| `.claude/ZOTERO_INTEGRATION_RECOMMENDATION.md` | Strategy & phases |
| `.claude/SESSION_2026-04-15_ZOTERO_SUMMARY.md` | Session notes |
| `scripts/zotero_sync_phase1.py` | Test script (personal library) |
| `memory/project_zotero_integration.md` | Decision context |

---

## Next Steps

- [ ] Add `ZOTERO_GROUP_ID=6479832` to `.env` manually
- [ ] Run the test connection command (above)
- [ ] Review the 11 papers in your group library
- [ ] Plan Phase 2 with supervisor (auto-sync papers to thesis?)

---

## Phase Timeline

| Phase | Goal | Time | Status |
|-------|------|------|--------|
| **Phase 1** | Read-only connection | 2-3h | ✅ DONE |
| **Phase 2** | Metadata sync (Zotero → Thesis) | 4-6h | ⬜ Next |
| **Phase 3** | PDF management | 6-8h | ⬜ Later |
| **Phase 4** | Team collaboration | 2-3h | ⬜ Later |

---

## Quick Commands

**Check group library items:**
```bash
python scripts/zotero_sync_phase1.py
cat docs/zotero_sync_report.md
```

**Run Phase 1 comparison:**
```bash
python scripts/zotero_sync_phase1.py --output docs/zotero_sync_report.md
```

**Export as BibTeX:**
```python
from pyzotero import Zotero
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path.cwd() / ".env")
zot = Zotero("6479832", 'group', os.environ['ZOTERO_API_KEY'])
zot.add_parameters(format='bibtex')
bibtex = zot.everything(zot.items(limit=100))
print(bibtex)
```

---

## Common Issues

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: pyzotero` | `pip install pyzotero` or `uv add pyzotero` |
| `403 Forbidden` | Check API key at https://www.zotero.org/settings/keys |
| `ZOTERO_GROUP_ID not found` | Add it to `.env` manually |
| Unicode errors on Windows | Already fixed in scripts (use UTF-8 encoding) |

---

## Resources

- **Pyzotero Docs**: https://pyzotero.readthedocs.io/
- **Zotero API v3**: https://www.zotero.org/support/dev/web_api/v3/start
- **Your Group Library**: https://www.zotero.org/groups/6479832/cmt-cbs-master-thesis
- **API Settings**: https://www.zotero.org/settings/keys

---

**Last Updated**: 2026-04-15  
**Status**: Phase 1 Complete ✅  
**Next Session**: Phase 2 Planning
