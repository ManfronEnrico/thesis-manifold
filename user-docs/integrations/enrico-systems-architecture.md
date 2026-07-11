# Systems Architecture: Data Flow & Integration Map

**For**: Enrico  
**Date**: 2026-04-18  
**Status**: Operational with manual orchestration

---

## The Big Picture

Your work integrates four systems:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          THESIS PROJECT ECOSYSTEM                       │
└─────────────────────────────────────────────────────────────────────────┘

                           ┌──────────────────┐
                           │   ZOTERO GROUP   │
                           │  6479832         │
                           │  35+ papers      │
                           │  metadata        │
                           └────────┬─────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │ python scripts/zotero_client.py
                    │ (on demand, ~1 second)
                    ↓
          ┌─────────────────────────┐
          │ docs/literature/        │
          │  ├─ bibtex.bib          │ ← BibTeX keys for LaTeX
          │  └─ citations.json      │ ← JSON for Python
          └──────────┬──────────────┘
                     │ (human reads)
                     │
      ┌──────────────┴───────────────────┐
      │                                  │
      ↓                                  ↓
┌─────────────────┐            ┌─────────────────────────┐
│ THESIS DRAFTS   │            │ GOOGLE DRIVE            │
│ (ch2, ch3, ...) │            │ 1cwK41FAJM_3WlpO...    │
│ cite{Key}       │            │                         │
│ \cite{Key}      │            │ ├─ 1_essential/        │
│                 │            │ │  ├─ Wang_et_al...pdf │
└─────────────────┘            │ │  └─ ...              │
                               │ ├─ 2_high/             │
                               │ │  └─ ...              │
                               │ ├─ 0_not_relevant/     │
                               │ └─ UNSURE/             │
                               │                        │
                               │ (manually organized)   │
                               └────────┬───────────────┘
                                        │
                        ┌───────────────┴──────────────┐
                        │ (future automation)          │
                        │ scripts/notebooklm_ingestion.py
                        ↓
                ┌──────────────────────────┐
                │ NOTEBOOKLM NOTEBOOKS     │
                │ (grounded analysis)      │
                │                          │
                │ ├─ ch2-literature        │
                │ ├─ ch3-methodology       │
                │ ├─ ch4-models            │
                │ ├─ ch5-synthesis         │
                │ ├─ ch6-evaluation        │
                │ └─ thesis-defense        │
                │                          │
                │ (source PDFs ingested)   │
                │ (citations verified)     │
                └──────────┬───────────────┘
                           │
                   ┌───────┴─────────┐
                   ↓                 ↓
            ┌────────────┐   ┌─────────────┐
            │ Chat QA    │   │ Study Guides│
            │ (grounded) │   │ (summaries) │
            └────────────┘   └─────────────┘
```

---

## System Roles

### **ZOTERO** — Bibliographic Authority

| Aspect | Detail |
|--------|--------|
| **Role** | Single source of truth for citation metadata |
| **Owner** | Both you and Enrico (shared group library) |
| **Contains** | 35+ academic papers with full metadata |
| **Fields** | Title, author, year, DOI, journal, abstract, keywords, etc. (26 total) |
| **Access** | Web UI (`https://www.zotero.org/groups/6479832/`) + Python API |
| **Sync** | Automatic (API reads live) |
| **Output** | BibTeX file + JSON for programmatic use |
| **Read-only?** | No — both can add/edit papers |

**When to use Zotero**:
- Add a new paper to the thesis
- Export citations for LaTeX
- Check what papers the team has
- Verify author/year/DOI for citation

---

### **GOOGLE DRIVE** — File Storage & Organization

| Aspect | Detail |
|--------|--------|
| **Role** | Central repository for PDF files |
| **Owner** | You (Brian), Enrico has read-only access |
| **Contains** | 50+ PDF papers organized by importance |
| **Folder ID** | `1cwK41FAJM_3WlpO-_9cOYMF04cjhV_LD` |
| **Access** | Web UI + Python API (service account) |
| **Sync** | Manual (you/Enrico drag-drop PDFs) |
| **Output** | File list + metadata (size, date, importance) |
| **Read-only?** | Enrico: Yes (Viewer role). You: No. |

**Organization scheme**:
```
Papers/
├── 1_essential/           ← Must-read papers
│   ├── Wang_et_al-2026-AgentNoiseBench.pdf
│   └── ...
├── 2_high/                ← Should-read papers
│   └── ...
├── 0_not_relevant/        ← Rejected papers
│   └── ...
└── UNSURE/                ← Needs classification
    └── ...
```

**When to use Google Drive**:
- Store PDF files you want to analyze
- Share PDFs between team members
- Check paper file size/metadata
- (Future) Auto-ingest PDFs to NotebookLM

---

### **NOTEBOOKLM** — Grounded Analysis Engine

| Aspect | Detail |
|--------|--------|
| **Role** | AI-assisted literature analysis with source verification |
| **Owner** | You (Brian), Enrico has read-only access (future) |
| **Contains** | Notebooks per thesis chapter + defense prep |
| **Access** | Web UI (notebooklm.google.com) + Python API |
| **Sync** | Manual (Phase 0) / Semi-automatic (Phase 1+) |
| **Output** | Chat answers with citations, study guides, briefing docs |
| **Read-only?** | Enrico: Yes (via Python API). You: Full access. |

**Notebooks** (planned):
```
ch2-literature        ← Cross-paper literature QA
ch3-methodology       ← Method extraction and comparison
ch4-models            ← Model selection and rationale
ch5-synthesis         ← Theory synthesis
ch6-evaluation        ← Evaluation methodology
thesis-defense        ← Defense preparation Q&A
```

**When to use NotebookLM**:
- Ask: "What do the papers say about X?" (grounded answer)
- Compare methodologies across papers
- Extract key quotes with source verification
- Prepare for thesis defense
- Generate study guides (summaries)

---

## Data Flow Scenarios

### **Scenario 1: Adding a New Paper**

```
Step 1: Enrico finds paper
  ↓
Step 2: Enrico adds to Zotero group library
  └─→ Zotero: new record with metadata
  
Step 3: You download PDF from Zotero
  ↓
Step 4: You move PDF to Google Drive (1_essential or 2_high)
  └─→ Drive: new file with importance classification
  
Step 5: (Optional) Manual ingestion to NotebookLM
  └─→ NotebookLM: new source in ch2-literature or ch3-methodology
  
Step 6: You run: python scripts/zotero_client.py
  └─→ Regenerates bibtex.bib and citations.json
  
Step 7: Enrico or you use in thesis draft
  └─→ LaTeX: \cite{BibTeXKey}
  └─→ NotebookLM: /notebooklm-ask "Does this paper support claim X?"
```

**Who does what**:
- Enrico: Find paper, add to Zotero
- You: Download PDF, organize in Drive, optionally ingest to NotebookLM
- Automation: scripts/zotero_client.py (regenerates BibTeX)

---

### **Scenario 2: Citing a Paper in Thesis Draft**

```
Step 1: You're writing Chapter 2
  └─→ Need to cite a paper on agent reasoning
  
Step 2: Look it up in citations.json
  └─→ Find BibTeX key: AgentReasoningSmith2024
  
Step 3: Add to LaTeX draft
  └─→ \cite{AgentReasoningSmith2024}
  
Step 4: (Optional) Verify via NotebookLM
  └─→ /notebooklm-ask ch2-literature "Provide exact quote from Smith et al on agent reasoning"
  └─→ NotebookLM returns: "According to [Smith et al, p. 5]: '...'"
  
Step 5: Check in actual PDF
  └─→ Open PDF in Drive
  └─→ Verify quote matches
  └─→ Mark citation as verified: True
  
Step 6: Compile thesis
  └─→ BibTeX processes \cite{} keys
  └─→ Creates references section
```

**Who does what**:
- You: Write, look up citation
- NotebookLM (optional): Provide source verification
- You: Manually check PDF if uncertain

---

### **Scenario 3: Gap Filling (Future)**

```
Step 1: You're writing Chapter 5 (Synthesis)
  └─→ Notice: "No papers on consumer sentiment impact on demand"
  
Step 2: You ask NotebookLM
  └─→ /notebooklm-ask ch5-synthesis "Find papers on consumer sentiment and demand forecasting"
  
Step 3: NotebookLM searches + finds candidates
  └─→ Returns: 3 papers with relevance scores
  
Step 4: Enrico or you adds to Zotero
  └─→ Zotero: new papers added
  
Step 5: You download PDFs to Drive
  └─→ Drive: new files in 1_essential or 2_high
  
Step 6: Auto-ingest to NotebookLM (Phase 1.5)
  └─→ scripts/notebooklm_ingestion.py detects new PDFs
  └─→ Adds to ch5-synthesis notebook
  └─→ Updates ingestion_manifest.json
  
Step 7: Now you can cite the new papers
  └─→ Zotero BibTeX updated
  └─→ NotebookLM ready for Q&A
```

**Who does what**:
- You: Identify gap, ask NotebookLM
- NotebookLM: Suggest papers
- Enrico: Add to Zotero
- You: Download PDFs
- Automation (Phase 1.5): Ingest to NotebookLM

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Metadata source** | Zotero | Centralized, team-accessible, 26 fields |
| **File source** | Google Drive | Shared storage, importance-based org, no git bloat |
| **Analysis engine** | NotebookLM | Grounded citations, zero hallucinations, UI fallback |
| **Ingestion** | Manual (Phase 0/1) → Automated (Phase 1.5+) | Risk-managed progression |
| **Citation safety** | Always verify against PDF | Academic integrity non-negotiable |
| **Team access** | Zotero (edit), Drive (read-only), NotebookLM (read) | Separation of duties |

---

## Consistency Rules

**Always keep these in sync**:

1. **Zotero → BibTeX**
   - Run every time you add a paper
   - Command: `python scripts/zotero_client.py`
   - Output: `docs/literature/bibtex.bib`

2. **Zotero → JSON**
   - Automatic with BibTeX
   - Output: `docs/literature/citations.json`
   - Used by Python scripts

3. **Drive → ingestion_manifest.json**
   - When you ingest a new PDF to NotebookLM
   - Manually update: `papers/ingestion_manifest.json`
   - Tracks: {zotero_key, drive_id, notebooklm_source_id}

4. **NotebookLM → verification log**
   - When you cite NotebookLM sources
   - Add to `docs/literature/verified_citations.md`
   - Record: {paper, quote, page, verified_date}

---

## Troubleshooting Matrix

| System | Problem | Diagnosis | Fix |
|--------|---------|-----------|-----|
| **Zotero** | API fails | `403 Forbidden` | Check API key in .env |
| **Zotero** | No papers appear | `[]` from scripts/zotero_client.py | Verify group library membership |
| **Drive** | Can't list papers | `RuntimeError: Failed to initialize` | Check service account JSON in .env |
| **Drive** | Missing papers | Papers listed but count is wrong | Check all importance folders (1_, 2_, 0_, UNSURE_) |
| **NotebookLM** | Auth expired | `AuthError` when querying | Re-run `notebooklm login` or use manual UI |
| **NotebookLM** | No sources | Notebook is empty | Run ingestion script or manually add PDFs |
| **Integration** | Can't find paper in 3 systems | Paper in one but not others | Check ingestion_manifest.json; may not be synced |

---

## Next Steps for Implementation

### **Phase 1 (Now → 1 week): Consolidate Manual Workflow**
- [x] Zotero integration complete
- [x] Google Drive setup complete
- [ ] Document ingestion_manifest.json schema
- [ ] Test end-to-end: Add paper → Zotero → Drive → verify citation

### **Phase 1.5 (1–2 weeks): Semi-Automated Ingestion**
- [ ] Create script to detect new PDFs in Drive
- [ ] Auto-ingest to correct NotebookLM notebook
- [ ] Update ingestion_manifest.json

### **Phase 2 (Post-deadline): Full Verification Workflow**
- [ ] Confidence scoring for citations
- [ ] Verification audit before submission
- [ ] Defense preparation agent

---

**Questions?** Refer to `INTEGRATION_AUDIT_AND_HANDOVER.md` or ask Brian.
