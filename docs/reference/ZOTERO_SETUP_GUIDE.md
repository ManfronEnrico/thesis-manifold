# Zotero Integration Setup Guide

**Last Updated**: 2026-04-15  
**Status**: Phase 1 Complete — Ready for Phase 2

---

## Quick Reference

### Your Zotero Configuration

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
# Zotero API
ZOTERO_API_KEY=ZtTh8WsMUW4QJPmiRyJLIos9
ZOTERO_USER_ID=15775662
ZOTERO_GROUP_ID=6479832
```

**Note**: `.env` is in `.gitignore` — never commit it. Share credentials via Signal/WhatsApp.

---

## What You Have

### 1. Pyzotero Library (Official API Client)

**Status**: ✅ Installed  
**Location**: Installed in venv  
**License**: MIT

```python
from pyzotero import Zotero

# Connect to personal library
zot = Zotero(
    library_id='15775662',
    library_type='user',
    api_key='YOUR_API_KEY'
)

# Connect to group library (CMT - CBS Master Thesis)
zot_group = Zotero(
    library_id='6479832',
    library_type='group',
    api_key='YOUR_API_KEY'
)
```

### 2. Pyzotero Skill

**Status**: ✅ Copied  
**Location**: `.claude/skills/pyzotero/`  
**Contents**:
- `SKILL.md` — Main documentation
- `references/` — 12 reference guides covering:
  - Authentication
  - Read/Write API
  - Collections & Tags
  - Exports (BibTeX, CSL-JSON, etc.)
  - File attachments
  - Pagination
  - Error handling
  - CLI usage

### 3. Phase 1 Test Script

**Status**: ✅ Working  
**Location**: `scripts/zotero_sync_phase1.py`  
**Purpose**: Read-only comparison of Zotero library vs thesis corpus

**Run**:
```bash
python scripts/zotero_sync_phase1.py
```

**Output**: `docs/zotero_sync_report.md`

### 4. Project Configuration

**Status**: ✅ Created  
**Location**: `pyproject.toml`  
**Purpose**: Defines dependencies for `uv` package manager

```toml
[project]
dependencies = [
    "pyzotero>=1.5.0",
    "python-dotenv>=1.0",
    ...
]
```

---

## Group Library Inventory

### Current Contents (39 items)

**5 Academic Papers** (journalArticle type):
1. Sample, Predict, then Proceed: Self-Verification Sampling for Tool Use of LLMs
2. Hybrid AI and LLM-Enabled Agent-Based Real-Time Decision Support Architecture for Industrial Batch Processes
3. An information-sharing and cost-aware custom loss machine learning framework for 3PL supply chain forecasting
4. DSS4EX: A Decision Support System framework to explore Artificial Intelligence pipelines with an application in time series forecasting
5. Toolformer: Language Models Can Teach Themselves to Use Tools

**6 Preprints** (preprint type):
1. A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration
2. AutoFlow: Automated Workflow Generation for Large Language Model Agents
3. SciAgent: Tool-augmented Language Models for Scientific Reasoning
4. Neuro-Symbolic AI in 2024: A Systematic Review
5. AgentCompass: Towards Reliable Evaluation of Agentic Workflows in Production
6. AgentNoiseBench: Benchmarking Robustness of Tool-Using LLM Agents Under Noisy Condition
7. ScoreFlow: Mastering LLM Agent Workflows via Score-based Preference Optimization

**23 PDF Attachments** (associated with papers above)

**5 Notes** (Untitled, for annotations)

---

## Recommended Next Steps

### Phase 2: Bidirectional Metadata Sync (4–6 hours)

**Goal**: Sync Zotero metadata ↔ thesis Markdown frontmatter

**Tasks**:
1. Create `scripts/zotero_sync_phase2.py`:
   - Read group library papers
   - Extract title, authors, year, venue
   - Compare against `/docs/literature/papers/*.md`
   - Write missing papers as new Markdown records (YAML + skeleton)

2. Add to existing papers:
   - Sync Zotero tags → thesis `srqs` field
   - Sync collections → thesis `angles` field
   - Mark papers as CONFIRMED when added to thesis

3. Implement conflict resolution:
   - Decision: Zotero wins? Thesis wins? Manual review?
   - Document in `.claude/rules/zotero-sync-conflict-resolution.md`

4. Add `--dry-run` flag to preview changes before committing

5. Integrate with `/update_all_docs` workflow

**Expected outcome**: 
- Group library papers auto-populate thesis corpus
- Metadata stays in sync (edit either Zotero or Markdown, both stay current)

---

### Phase 3: PDF Attachment Management (6–8 hours)

**Goal**: Auto-sync PDF attachments from Zotero to thesis `/papers/` folder

**Tasks**:
1. Create `scripts/zotero_pdf_sync.py`:
   - Fetch PDF attachments from group library
   - Download to `/papers/ch2-literature/`, `/papers/ch3-methodology/`, etc.
   - Organize by research angle (SRQ)
   - Track downloads in `docs/literature/ingestion_manifest.json`

2. Handle edge cases:
   - Skip already-downloaded PDFs (hash-based caching)
   - Handle missing attachments gracefully
   - Create backup before deleting local files

3. Integrate with Phase 2 sync (metadata + attachments together)

**Expected outcome**:
- Single source of PDFs: Zotero
- Thesis `/papers/` auto-mirrors group library
- PDF metadata linked to Zotero item ID

---

### Phase 4: Collaborative Group Features

**Goal**: Enable team members to add papers to group library

**Setup**:
1. Share group library link: `https://www.zotero.org/groups/6479832/cmt-cbs-master-thesis`
2. Add collaborators to group via Zotero web interface
3. Set group permissions (view, edit, add papers)

**Workflow**:
- Team members add papers to group library
- Phase 2 sync automatically pulls them into thesis corpus
- Reduces manual coordination

---

## Common Commands

### Test Zotero Connection

```bash
python << 'EOF'
import os
from pathlib import Path
from pyzotero import Zotero
from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env")

# Test group library
zot = Zotero(
    library_id='6479832',
    library_type='group',
    api_key=os.environ['ZOTERO_API_KEY']
)

items = zot.everything(zot.items(limit=100))
print(f"Group library: {len(items)} items")

for item in items[:5]:
    title = item["data"].get("title", "Untitled")
    print(f"  - {title}")
EOF
```

### Run Phase 1 Sync Report

```bash
python scripts/zotero_sync_phase1.py
cat docs/zotero_sync_report.md
```

### Fetch Specific Paper from Group Library

```python
from pyzotero import Zotero
import os
from dotenv import load_dotenv

load_dotenv()

zot = Zotero(
    library_id='6479832',
    library_type='group',
    api_key=os.environ['ZOTERO_API_KEY']
)

# Get all papers
items = zot.everything(zot.items(limit=100))

# Find by title
target = "Toolformer"
for item in items:
    title = item["data"].get("title", "")
    if target in title:
        print(item["data"])
        break
```

### Export Group Library as BibTeX

```python
from pyzotero import Zotero
import os
from dotenv import load_dotenv

load_dotenv()

zot = Zotero(
    library_id='6479832',
    library_type='group',
    api_key=os.environ['ZOTERO_API_KEY']
)

# Add BibTeX format
zot.add_parameters(format='bibtex')

# Fetch as BibTeX
bibtex = zot.everything(zot.items(limit=100))
print(bibtex)
```

---

## Troubleshooting

### "Missing environment variable: ZOTERO_API_KEY"

**Fix**: Add to `.env`:
```
ZOTERO_API_KEY=ZtTh8WsMUW4QJPmiRyJLIos9
ZOTERO_USER_ID=15775662
ZOTERO_GROUP_ID=6479832
```

### "ModuleNotFoundError: No module named 'pyzotero'"

**Fix**: Install pyzotero:
```bash
pip install pyzotero
# or
uv add pyzotero
```

### "403 Forbidden" Error

**Cause**: API key has incorrect permissions  
**Fix**: 
1. Go to https://www.zotero.org/settings/keys
2. Check API key scope (must have "Write" for Phase 2+)
3. Regenerate if needed

### Unicode Errors on Windows

**Cause**: Python writing UTF-8 to cp1252 console  
**Fix**: Use `encode('utf-8')` when writing files:
```python
output_path.write_bytes(text.encode('utf-8'))
```

---

## Decision Records

### Why Group Library Instead of Personal?

**Rationale**:
- **Collaboration**: Team members can contribute papers
- **Scope**: Focused on thesis papers only (not personal research notes)
- **Audit trail**: Zotero tracks who added what
- **Access control**: Can restrict to team members
- **Scale**: Can grow with thesis without cluttering personal library

**Trade-off**: Requires Zotero group setup (one-time cost, done ✅)

### Why Pyzotero Instead of Zotero API Directly?

**Rationale**:
- Official Python client, actively maintained
- Handles pagination, error handling, rate limiting
- Works with both personal and group libraries
- Lightweight (~1 package)
- Better DX than raw HTTP calls

### Why Phase Approach Instead of All-at-Once?

**Rationale**:
- **Phase 1 (read-only)**: Proves connection works, zero risk
- **Phase 2 (metadata)**: Automates paper ingestion, medium risk
- **Phase 3 (PDFs)**: Auto-manages attachments, file I/O risk
- **Incremental**: Can stop after Phase 1 if needed
- **Testable**: Each phase has clear success criteria

---

## File Structure

```
CMT_Codebase/
├── .env                                    ← Add ZOTERO_GROUP_ID
├── pyproject.toml                          ← Dependencies (has pyzotero)
├── scripts/
│   └── zotero_sync_phase1.py              ← Phase 1: Read-only comparison
├── .claude/
│   ├── skills/pyzotero/                   ← API reference docs
│   └── ZOTERO_INTEGRATION_RECOMMENDATION.md ← Full strategy
├── docs/
│   ├── ZOTERO_SETUP_GUIDE.md              ← This file
│   ├── zotero_sync_report.md              ← Latest sync results
│   └── literature/
│       ├── papers/                        ← 45 thesis papers (Markdown)
│       └── ingestion_manifest.json        ← Paper → NotebookLM mapping
└── memory/
    └── project_zotero_integration.md      ← Decision context for future sessions
```

---

## Resources

| Resource | Link |
|----------|------|
| **Pyzotero Docs** | https://pyzotero.readthedocs.io/ |
| **Zotero API v3** | https://www.zotero.org/support/dev/web_api/v3/start |
| **Your Group Library** | https://www.zotero.org/groups/6479832/cmt-cbs-master-thesis |
| **Your API Settings** | https://www.zotero.org/settings/keys |
| **Pyzotero Skill** | `.claude/skills/pyzotero/SKILL.md` |
| **Full Recommendation** | `.claude/ZOTERO_INTEGRATION_RECOMMENDATION.md` |

---

## Key Dates & Status

| Date | Event | Status |
|------|-------|--------|
| 2026-04-15 | Phase 1 setup & testing | ✅ COMPLETE |
| 2026-04-15 | Discovered group library (ID: 6479832) | ✅ COMPLETE |
| 2026-04-15 | Copied pyzotero skill | ✅ COMPLETE |
| TBD | Phase 2 (bidirectional sync) | ⬜ PENDING |
| TBD | Phase 3 (PDF management) | ⬜ PENDING |
| TBD | Phase 4 (team collaboration) | ⬜ PENDING |

---

**Created by**: Claude Code  
**For**: Brian (CBS Master Thesis — Manifold AI)  
**Status**: Ready for Phase 2 planning
