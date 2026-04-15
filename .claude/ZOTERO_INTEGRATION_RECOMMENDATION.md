# Zotero Integration Recommendation — CBS Master Thesis CMT

**Date**: 2026-04-15  
**Status**: FEASIBLE with clear scope  
**Recommendation**: **Phase approach — start with read-only integration**

---

## Executive Summary

Your thesis can integrate Zotero via **pyzotero** (official Python API client), enabling dynamic reference management between your Zotero library and thesis metadata. The integration is **not mandatory** for thesis completion, but **highly valuable** for ongoing literature corpus maintenance.

**Key finding**: You already have a robust literature management foundation (48 Markdown paper records, 6-angle scraping strategy, gap analysis). Zotero integration should **augment** this, not replace it.

---

## Current State Assessment

### Your Thesis Literature System (System B — Thesis Production)
| Aspect | Current Approach | Status |
|--------|-----------------|--------|
| Paper records | 48 confirmed papers in `/docs/literature/papers/*.md` | ✅ Stable |
| Metadata | YAML frontmatter (title, authors, year, venue, tier, score, angles, SRQs) | ✅ Comprehensive |
| Scraping strategy | 6 research angles (Ch2–Ch6), manual human confirmation | ✅ Working |
| Source of truth | Markdown files + NotebookLM ingestion manifest | ✅ Single source |
| Attachment handling | PDF files in `/papers/` subfolders by chapter | ✅ Organized |
| Citation format | Currently using Claude Code `/cite` skill (APA 7) | ✅ Compliant |

### Gap Zotero Solves
- **Manual PDF management**: Currently tracking PDFs locally; Zotero centralizes this
- **Metadata synchronization**: If you update a paper's metadata in Zotero, thesis doesn't auto-sync
- **Multi-user collaboration**: If future team members contribute references
- **Export consistency**: Zotero ensures BibTeX/CSL-JSON exports stay in sync across formats
- **Citation network**: Zotero's "cited by" and "citing" features aid literature gap analysis

---

## Zotero Integration Landscape

### Available Tools

#### 1. **Pyzotero** (Official API Client)
**Status**: ✅ **Recommended**

| Feature | Capability |
|---------|-----------|
| Language | Python |
| License | MIT |
| Read operations | Full support (items, collections, tags, attachments) |
| Write operations | Full support (create, update, delete items) |
| File uploads | Supported (PDFs, notes, snapshots) |
| Search | Keyword + advanced parameters (collections, tags, date range) |
| Exports | BibTeX, CSL-JSON, CSL-YAML, RIS, Markdown, HTML, plain text |
| Authentication | API key + library ID (read-only or full access) |
| Local mode | Read-only via local Zotero database (no API key needed) |
| Rate limits | Reasonable (documented in pyzotero docs) |

**Pros**:
- Lightweight, actively maintained
- Full feature parity with Zotero Web API v3
- Works with personal and group libraries
- Can run entirely offline in local mode

**Cons**:
- Requires pyzotero installation (`uv add pyzotero`)
- Need Zotero API credentials (free, but requires setup)
- Only one library per instance (create multiple `Zotero()` instances for groups)

#### 2. **Zotero Official JavaScript SDK** (Alternative)
**Status**: ❌ Not recommended for this thesis

| Why not |
|---------|
| Thesis uses Python + LLM agents; JS SDK adds language mismatch |
| Slower to integrate with LangGraph system |
| Less mature than pyzotero |
| Requires Node.js runtime (extra dependency) |

#### 3. **Direct API Calls via HTTP**
**Status**: ❌ Not recommended

| Why not |
|---------|
| Reinventing what pyzotero already does |
| More error-prone than using a battle-tested client |
| Pyzotero exists specifically for this use case |

---

## Recommended Approach: Phase Integration

### Phase 1: Read-Only Sync (Weeks 1–2)
**Goal**: One-way pull from Zotero → thesis metadata sync

**Steps**:
1. Set up Zotero API credentials (5 min)
2. Create `scripts/zotero_sync.py` using pyzotero to:
   - Fetch all items from your Zotero library
   - Compare against `/docs/literature/papers/` metadata
   - Flag missing/updated items
   - Generate sync report (no write yet)
3. Add to `.claude/skills/` or as a standalone script
4. Run monthly to catch metadata drift
5. Document in CHEATSHEET.md under "Literature Workflows"

**Expected outcome**: 
- Detect if Zotero library diverges from thesis papers
- No risk of data loss (read-only)
- Establish pyzotero credentials + workflow

**Time to implement**: 2–3 hours  
**Risk level**: LOW (read-only, reversible)

---

### Phase 2: Bidirectional Metadata Sync (Weeks 3–4)
**Goal**: Sync tags, notes, and collections between Zotero and thesis metadata

**Steps**:
1. Extend `zotero_sync.py` to:
   - Write paper record metadata back to `/docs/literature/papers/*.md` YAML frontmatter
   - Sync Zotero collections → thesis `angles` field
   - Sync Zotero tags → thesis `srqs` / `tier` fields
   - Auto-update `status` field when Zotero items marked as "CONFIRMED"
2. Add conflict resolution logic (Zotero wins, or thesis wins?)
3. Add dry-run mode (`--dry-run` flag before committing changes)
4. Integrate into `/update_all_docs` skill workflow

**Expected outcome**:
- Single source of truth (can update either Zotero or Markdown, both stay in sync)
- Tags in Zotero become thesis metadata
- No more manual frontmatter updates

**Time to implement**: 4–6 hours  
**Risk level**: MEDIUM (requires careful merge logic)  
**Prerequisite**: Phase 1 stable + team agreement on conflict resolution

---

### Phase 3: Dynamic PDF Attachment Management (Weeks 5–6)
**Goal**: Zotero library PDFs auto-sync to `/papers/` folder structure

**Steps**:
1. Script to:
   - Fetch PDF attachments from Zotero items
   - Download to `/papers/ch2-literature/`, `/papers/ch3-methodology/`, etc. (based on angles/SRQs)
   - Update ingestion manifest with PDF → Zotero item ID mapping
2. Handle attachment types (PDF, snapshot, note)
3. Skip already-downloaded PDFs (hash-based caching)

**Expected outcome**:
- One source of PDFs: Zotero
- Thesis `/papers/` auto-mirrors Zotero attachments
- PDF metadata stays with Zotero metadata

**Time to implement**: 6–8 hours  
**Risk level**: MEDIUM (file I/O, needs careful backup strategy)  
**Prerequisite**: Phase 1 + Phase 2 stable

---

## Skill Integration Points

### Where to add Zotero support in CMT codebase

#### Option A: New standalone skill (`pyzotero.md` in `.claude/skills/`)
**Pros**: Modular, mirrors other academic research skills  
**Cons**: Not auto-triggered, requires manual invocation

**Location**: `.claude/skills/pyzotero/SKILL.md`  
**Files needed**:
- `SKILL.md` — main skill definition
- `examples/` — code snippets for common use cases
- `references/` — authentication, sync patterns, conflict resolution

---

#### Option B: Extend existing `literature_agent.py` (System B)
**Pros**: Integrated into thesis production pipeline  
**Cons**: Couples System B agent to external Zotero dependency

**Modification points**:
- `LiteratureAgent.run_scraping()` — pull from Zotero instead of web search
- `LiteratureAgent.confirm_papers()` — write confirmations back to Zotero
- `LiteratureAgent.update_gap_analysis()` — use Zotero metadata

---

#### Option C: New System B agent (`zotero_agent.py`)
**Pros**: Clean separation of concerns, follows agent pattern  
**Cons**: Adds another agent to manage

**Design**: ZoteroAgent handles:
- Library sync (read metadata)
- Tag management (write confirmations)
- Attachment handling (sync PDFs)

---

## Security & Credential Handling

### API Key Management
✅ **Already safe**: Your `.claude/hooks/check_file_edit.py` enforces `.env` safety.

**Pattern**:
```python
# In .env (NOT in git)
ZOTERO_LIBRARY_ID=123456
ZOTERO_API_KEY=abc123xyz
ZOTERO_LIBRARY_TYPE=user

# In Python code
import os
from dotenv import load_dotenv
from pyzotero import Zotero

load_dotenv()
zot = Zotero(
    library_id=os.environ['ZOTERO_LIBRARY_ID'],
    library_type=os.environ['ZOTERO_LIBRARY_TYPE'],
    api_key=os.environ['ZOTERO_API_KEY']
)
```

### Permissions
- **Read-only API key**: If you only need to pull metadata (Phase 1)
  - Setup at https://www.zotero.org/settings/keys/new → "Read Only"
  - Safer, limits blast radius

- **Full access API key**: If you want to write confirmations back (Phase 2+)
  - Setup at https://www.zotero.org/settings/keys/new → "Write Access"
  - Required for confirmations to propagate

---

## Comparison: Zotero vs. Existing System

| Aspect | Current Approach | Zotero-Enhanced | Win |
|--------|------------------|-----------------|-----|
| Source of truth | Local Markdown + PDFs | Centralized Zotero + sync script | Zotero |
| Metadata updates | Manual edit in thesis | Edit in Zotero, auto-sync | Zotero |
| Collaboration | Share Markdown files | Share Zotero group library | Zotero |
| PDF attachment | Manual drag-drop to `/papers/` | Auto-sync from Zotero | Zotero |
| Citation export | Claude `/cite` skill | Zotero export formats | Both equally good |
| Team onboarding | "Clone repo, edit Markdown" | "Link Zotero group library" | Zotero |
| Offline capability | ✅ Works offline | Needs API for sync (but `local=True` mode exists) | Current |

---

## What NOT to do (Anti-patterns)

❌ **Replace** your Markdown paper records entirely with Zotero API calls
- Keep Markdown as readable, durable source
- Zotero is a sync layer, not the source of truth

❌ **Auto-merge** Zotero and Markdown without conflict detection
- Always use `--dry-run` before syncing
- Log all changes (timestamps, who changed what)

❌ **Assume API key is safe in code**
- Use `.env` + `dotenv`, never hardcode
- Commit `.gitignore` rule: `*.env`

❌ **Skip Phase 1 and go straight to bidirectional sync**
- Phase 1 (read-only) proves the pyzotero setup works
- Reduces risk of data loss in Phase 2

---

## Existing Academic Skills You Already Have

From your `scientific-agent-skills` repo, you **already import**:

| Skill | Relevance to Zotero Integration |
|-------|----------------------------------|
| `citation-management` | Can be extended with Zotero export formats |
| `literature-review` | Complements Zotero scraping |
| `scholarly-evaluation` | Use Zotero metadata (tiers, scores) in evaluation |
| `academic-pipeline` | Chain Zotero sync → literature review → gap analysis |

**Recommendation**: After Phase 1 is stable, audit `scientific-agent-skills/citation-management/` to see if pyzotero patterns align.

---

## Implementation Checklist

### Pre-Phase 1
- [ ] Get Zotero API credentials from https://www.zotero.org/settings/keys
  - [ ] Note your **User ID** (shown on settings page)
  - [ ] Create an API key (https://www.zotero.org/settings/keys/new)
  - [ ] Choose "Read Only" for first phase
- [ ] Create `.env` file (do NOT commit):
  ```
  ZOTERO_LIBRARY_ID=<your_user_id>
  ZOTERO_API_KEY=<your_api_key>
  ZOTERO_LIBRARY_TYPE=user
  ```
- [ ] Install pyzotero: `uv add pyzotero`
- [ ] Test locally: `python -c "from pyzotero import Zotero; print('OK')"`

### Phase 1 Tasks
- [ ] Create `scripts/zotero_sync.py` with read-only logic
- [ ] Add sync report template (`docs/zotero_sync_report.md`)
- [ ] Document in CHEATSHEET.md: `zotero sync` command
- [ ] Run first sync, review report
- [ ] Add `.claude/rules/zotero-integration.md` (workflow documentation)

### Phase 2+ Planning
- [ ] Document conflict resolution policy (who wins in a conflict?)
- [ ] Add `--dry-run` flag to all write operations
- [ ] Create test suite for sync logic
- [ ] Plan integration with `/update_all_docs` workflow

---

## Recommendation Summary

| Question | Answer |
|----------|--------|
| **Should you integrate Zotero?** | YES — valuable for corpus maintenance |
| **Is it required for thesis?** | NO — nice-to-have, not blocking |
| **When to start?** | After Phase 1 planning complete (you're ready now) |
| **Best approach?** | Phase approach (read-only first, then expand) |
| **Time investment** | 2–3 hours (Phase 1), 4–6 hours (Phase 2), 6–8 hours (Phase 3) |
| **Risk level** | LOW (read-only start), escalate with phases |
| **Tool to use** | Pyzotero (official API client) — already recommended in your `scientific-agent-skills` repo |

---

## Next Steps

1. **Review this recommendation** with your supervisor / team
2. **Set up Zotero API credentials** (5 minutes)
3. **Choose implementation scope** (Phase 1 only? All three phases?)
4. **Create task** for Phase 1 (read-only sync)
5. **Link to memory** so future sessions have context

**Questions?** See:
- [Pyzotero SKILL.md](C:\Users\brian\OneDrive\Documents\01 - P - Projects and Tasks\github_academic_skill\scientific-agent-skills\scientific-skills\pyzotero\SKILL.md)
- [Pyzotero Authentication Guide](C:\Users\brian\OneDrive\Documents\01 - P - Projects and Tasks\github_academic_skill\scientific-agent-skills\scientific-skills\pyzotero\references\authentication.md)
- [Zotero API Docs](https://www.zotero.org/support/dev/web_api/v3/start)

---

## Appendix: Code Sketch (Phase 1)

```python
# scripts/zotero_sync.py
import os
from pathlib import Path
from pyzotero import Zotero
from dotenv import load_dotenv

load_dotenv()

zot = Zotero(
    library_id=os.environ['ZOTERO_LIBRARY_ID'],
    library_type=os.environ['ZOTERO_LIBRARY_TYPE'],
    api_key=os.environ['ZOTERO_API_KEY']
)

# Fetch all items from Zotero
zotero_items = zot.everything(zot.items())
print(f"Found {len(zotero_items)} items in Zotero")

# Load thesis paper records
papers_dir = Path("docs/literature/papers")
thesis_papers = {p.stem: p for p in papers_dir.glob("*.md")}
print(f"Found {len(thesis_papers)} papers in thesis")

# Compare and report
missing_in_thesis = [
    item['data']['title'] for item in zotero_items
    if item['data']['title'] not in thesis_papers
]
print(f"\nMissing in thesis: {missing_in_thesis}")

# Report to file
report = Path("docs/zotero_sync_report.md")
with open(report, 'w') as f:
    f.write(f"# Zotero Sync Report\n")
    f.write(f"- Zotero items: {len(zotero_items)}\n")
    f.write(f"- Thesis papers: {len(thesis_papers)}\n")
    f.write(f"- Missing in thesis: {len(missing_in_thesis)}\n")
    if missing_in_thesis:
        f.write(f"\nTitles:\n")
        for title in missing_in_thesis:
            f.write(f"- {title}\n")
```

This is a minimal Phase 1 proof-of-concept. It:
- ✅ Reads from Zotero (read-only)
- ✅ Reports differences
- ✅ No write operations (safe)
- ✅ Can be expanded in Phase 2

---

**End of Recommendation Document**
