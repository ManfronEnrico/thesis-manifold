# NotebookLM Integration Plan for Thesis Workflow
*Decision-grade planning document — analysis only, no implementation yet*
*Generated: 2026-04-13 | Thesis deadline: 2026-05-15*

---

## Context

The thesis workflow currently uses a dual-system architecture: System A (AI research framework with LangGraph + PydanticAI agents for forecasting) and System B (thesis production system with 10 writing agents). Literature management is entirely manual — papers are stored as annotated Markdown files, tracked in a CSV, and managed by a LiteratureAgent without any external knowledge-base integration. There is no Zotero API integration and no Google Drive API integration.

The goal of this integration plan is to evaluate whether `notebooklm-py` (unofficial Python API, v0.3.4, 10K+ stars, actively maintained as of April 2026) should be adopted to add a **grounded analysis layer** on top of the 16+ confirmed thesis papers — enabling quote-precise literature review support, paper comparison, and method extraction in a way that reduces hallucination risk and improves citation accuracy.

This plan determines: **adopt directly / wrap / partially adapt / or inspiration only**, with a phased roadmap and explicit safeguards.

---

## 1. Executive Summary

| Dimension | Finding |
|---|---|
| **Repo maturity** | Production-quality code (typed, tested, 90% coverage) but uses undocumented Google RPC API — can break without warning |
| **Capability fit** | High — PDF import, URL import, Drive import, chat-with-citations, study guides, report generation all directly applicable |
| **Auth model** | Browser cookie (Playwright) or env var injection — fragile by nature, requires human login session maintenance |
| **Thesis fit** | Strong for literature review, paper comparison, quote extraction; weak for automated/unattended workflows |
| **Recommendation** | **Thin wrapper approach** — import the library as-is, add a thesis-specific orchestration layer on top. Do not fork or reimplement the RPC layer. |
| **Minimum viable** | Manual-first: create one notebook per thesis chapter, add papers, query manually. Then automate ingestion via `notebooklm-py`. |
| **Risk level** | Medium — unofficial API breakage is the primary risk, mitigated by human fallback path always existing |

---

## 2. Repository Capability Analysis

### Technical Architecture

```
NotebookLMClient (async)
├── notebooks  → create, list, get, delete, rename, describe
├── sources    → add_url, add_file, add_text, add_drive, list, delete, refresh, get_fulltext
├── artifacts  → generate_report (study guide, briefing doc, blog, custom)
│               generate_quiz, generate_flashcard, generate_mind_map
│               generate_audio, generate_video, generate_slide
├── chat       → ask(question) → returns answer + citations
├── research   → start(query), poll(task_id), import_sources()
├── notes      → notebook-level notes
└── sharing    → public access toggle
```

### Authentication Flow
1. `notebooklm login` → Playwright browser opens NotebookLM → cookies captured to local storage file
2. Subsequent calls: `NotebookLMClient.from_storage()` loads cookies → extracts CSRF token + session ID from NotebookLM homepage HTML
3. Auto-refresh: detects auth failure and retries once after token refresh
4. CI/CD alternative: `NOTEBOOKLM_AUTH_JSON` env var

### RPC Protocol
Uses Google's undocumented `batchexecute` endpoint — same protocol used internally by Google's own apps. The library reverse-engineered the request/response encoding. This is the primary fragility point.

### Source Types Supported (15 total)
PDF, Google Docs, Web Page/URL, YouTube, Audio, Video, Image, Google Drive (generic), Google Sheets, Text, Email, Markdown, Epub, Podcast, Other

### Output Types
- Study guides, briefing docs, blog posts (Markdown export)
- Quizzes, flashcards (JSON / Markdown / HTML export)
- Audio overviews (MP3)
- Mind maps
- Data tables (CSV)
- Slide decks (PDF / PPTX)
- Chat responses with inline citations (source UUID + text passages)

### Maintenance Signals
- Last commit: 2026-04-04 (9 days ago as of plan date)
- Stars: 10,439 | Forks: 1,374 | Open issues: 55
- Active CI/CD with 90% code coverage requirement
- CHANGELOG maintained (CHANGELOG.md is 21 KB)
- SKILL.md (26.8 KB) + CLAUDE.md (7.6 KB) → library itself is designed for agent use

---

## 3. Relevant Features for Thesis Workflow

### Feature Relevance Table

| Capability | Repo Support | Thesis Relevance | Integration Complexity | Risk | Recommendation |
|---|---|---|---|---|---|
| **PDF import** | ✅ add_file() with resumable upload | High — 16+ paper PDFs | Low | Low | Use directly |
| **URL import** | ✅ add_url() | Medium — arXiv/DOI links as fallback | Low | Low | Use as fallback |
| **Google Drive import** | ✅ add_drive(drive_id) | Medium — Indeks Danmark data on Drive | Medium | Medium | Use with caution |
| **Chat with citations** | ✅ ask() → citations with source UUID + passage | Very High — quote-precise QA | Low | Medium | Core use case |
| **Study guide generation** | ✅ generate_report("study_guide") | High — per-paper or per-chapter | Low | Low | Use directly |
| **Briefing doc generation** | ✅ generate_report("briefing_doc") | High — chapter literature summaries | Low | Low | Use directly |
| **Notebook management** | ✅ Full CRUD | High — one notebook per thesis chapter | Low | Low | Use directly |
| **Source fulltext extraction** | ✅ get_fulltext() | High — export indexed text for Claude | Medium | Low | Use for verification |
| **Mind map generation** | ✅ generate_mind_map() | Medium — theory synthesis visualization | Low | Low | Nice to have |
| **Quiz/Flashcard generation** | ✅ generate_quiz(), generate_flashcard() | Low-Medium — defense preparation | Low | Low | Phase 3+ |
| **Research tool (web search)** | ✅ research.start(query) | Low — we have our own corpus | Low | Low | Skip |
| **Audio overview** | ✅ generate_audio() | Low | Low | Low | Skip |
| **Source freshness check** | ✅ check_freshness() | Medium — if papers update (preprints) | Low | Low | Phase 3+ |
| **Sharing** | ✅ toggle_public_access() | Low — academic workflow | Low | Low | Skip |

---

## 4. Current Research Stack Fit Assessment

### Existing Stack

| Layer | Tool | State | Gap |
|---|---|---|---|
| **Reference management** | Manual CSV (40 papers) + Markdown annotations (~37 files) | Active | No Zotero, no `.bib` generation |
| **PDF storage** | Local files (assumed OneDrive/Drive) | Unknown | No structured local paper folder found in codebase |
| **Literature orchestration** | LiteratureAgent (System B) | Implemented | Manages tiers and metadata, no knowledge-base query |
| **Knowledge base** | None | Gap | No RAG layer, no NotebookLM |
| **Synthesis** | SynthesisAgent (System A) | Implemented | LLM-only, no grounded source references |
| **Writing** | WritingAgent (System B) | Bullet-points only | No citation management |
| **Compliance** | ComplianceAgent | CBS guidelines | No citation format checking |
| **Orchestration** | LangGraph + Claude Code | Active | Can add NotebookLM calls as new graph nodes |

### Key Gaps NotebookLM Would Fill

1. **Grounded QA**: Currently, asking "what did X paper say about Y" requires trusting the LiteratureAgent's Markdown annotations — which may be summaries, not direct quotes.
2. **Cross-paper synthesis**: No tool currently lets you ask "compare the methodology in paper A vs paper B" over actual source PDFs.
3. **Quote verification**: WritingAgent produces bullet points that reference papers by tier/title — no mechanism to verify or extract verbatim quotes.
4. **Defense prep**: No structured Q&A system over the full literature corpus.

---

## 5. Proposed System Architecture

### System Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│ ZOTERO (not implemented yet — future layer)                      │
│  Owns: bibliographic metadata, citation keys, .bib export        │
│  Produces: structured metadata for ingestion scripts             │
└──────────────────────┬──────────────────────────────────────────┘
                        │ (future: Zotero-to-NotebookLM bridge)
                        ↓
┌─────────────────────────────────────────────────────────────────┐
│ LOCAL THESIS REPO + GOOGLE DRIVE                                 │
│  Owns: actual PDF files, CSV datasets, figure assets            │
│  Organized by: chapter assignment + tier                         │
│  Produces: file paths for ingestion scripts                      │
└──────────────────────┬──────────────────────────────────────────┘
                        │ PDF paths / file handles
                        ↓
┌─────────────────────────────────────────────────────────────────┐
│ NOTEBOOKLM (via notebooklm-py wrapper)                          │
│  Owns: grounded analysis notebooks per chapter                   │
│  One notebook per thesis chapter (max 50 sources per notebook)   │
│  Produces: study guides, briefing docs, citation-backed answers  │
│  Human-verifiable: always accessible via notebooklm.google.com  │
└──────────────────────┬──────────────────────────────────────────┘
                        │ structured outputs (Markdown, JSON)
                        ↓
┌─────────────────────────────────────────────────────────────────┐
│ CLAUDE CODE / SYSTEM B ORCHESTRATION LAYER                       │
│  Owns: workflow logic, prompt engineering, output formatting     │
│  Integrates: NotebookLM outputs into thesis drafting pipeline    │
│  Never trusts: NotebookLM quotes without verification flag       │
│  Produces: bullet-point synthesis for WritingAgent               │
└─────────────────────────────────────────────────────────────────┘
```

### Notebook Structure (Recommended)

| Notebook Name | Papers/Sources | Purpose |
|---|---|---|
| `thesis-ch2-literature` | All 16+ confirmed papers | Cross-corpus literature review QA |
| `thesis-ch3-methodology` | Papers with ML methodology focus (Tier A) | Method extraction and comparison |
| `thesis-ch4-models` | Forecasting model papers + benchmark comparisons | Model rationale and SRQ1 support |
| `thesis-ch5-synthesis` | Consumer signal / sentiment papers | SRQ2 theory grounding |
| `thesis-ch6-evaluation` | Calibration + evaluation methodology papers | SRQ3/SRQ4 evaluation framework |
| `thesis-defense` | All 16+ papers + thesis draft sections | Defense preparation Q&A |

**Decision**: Chapter-based organization (not paper-by-paper) allows cross-paper synthesis queries and mirrors the thesis writing structure.

---

## 6. Source Ingestion and Sync Strategy

### Source-of-Truth Decision

| Question | Options | Decision | Rationale |
|---|---|---|---|
| **Primary metadata source** | Zotero / Manual CSV / Markdown | **Manual CSV + Markdown (current)** | Zotero not integrated; adding it now risks scope creep before May 15 deadline |
| **Primary file source** | Google Drive / Local repo folder / OneDrive | **Local repo folder (create `papers/` dir)** | Single authoritative location, git-trackable paths, no Drive API dependency |
| **Ingestion trigger** | Automated sync / Manual script / On-demand | **Manual script with notebook ID persistence** | Balances reproducibility with auth fragility of unofficial API |
| **Notebook-to-chapter mapping** | One-to-one / Flat / Topic-based | **Chapter-based** | Mirrors thesis structure, prevents >50 source limit issues |
| **Sync frequency** | Continuous / Per-run / Ad hoc | **Ad hoc per phase** | Matches existing human-in-the-loop phase transition model |

### Ingestion Pipeline Design

```
papers/
├── ch2-literature/
│   ├── paper_[slug].pdf
│   └── ...
├── ch3-methodology/
│   └── ...
├── ingestion_manifest.json   ← tracks: paper_slug → notebooklm_source_id + notebook_id
└── ingestion_log.md          ← human-readable audit trail
```

`ingestion_manifest.json` schema:
```json
{
  "notebooks": {
    "ch2-literature": "NOTEBOOK_ID",
    "ch3-methodology": "NOTEBOOK_ID"
  },
  "sources": {
    "paper_slug": {
      "local_path": "papers/ch2-literature/paper_slug.pdf",
      "notebook": "ch2-literature",
      "notebooklm_source_id": "SOURCE_UUID",
      "added_at": "2026-04-14T00:00:00Z",
      "verified": true
    }
  }
}
```

### No Zotero Bridge (Phase 0/1)

For now, paper metadata lives in the existing `docs/literature/papers/*.md` files and the master CSV. A future Zotero bridge (Phase 3+) would export `.bib` and map to ingestion slugs, but this is **post-deadline scope**.

---

## 7. Claude Code + NotebookLM Workflow Design

### Approved Workflow Patterns

**Pattern A — Literature Review QA**
```
1. Claude Code reads docs/literature/gap_analysis.md (existing)
2. Claude Code calls notebooklm_client.chat.ask("What do the sources say about X?", notebook_id=CH2_ID)
3. NotebookLM returns answer + citations (source UUID + text passage)
4. Claude Code formats citations → [Author, Year, NotebookLM citation ref]
5. Output flagged as [NOTEBOOKLM — VERIFY QUOTE BEFORE USE]
6. Human verifies in notebooklm.google.com before writing agent uses it
```

**Pattern B — Study Guide Generation**
```
1. Claude Code calls notebooklm_client.artifacts.generate_report("study_guide", notebook_id=CH_ID)
2. Waits for completion (30s–45m with polling)
3. Downloads Markdown report → saves to docs/literature/guides/ch2_study_guide.md
4. Flagged as [NOTEBOOKLM SUMMARY — NOT VERBATIM QUOTES]
5. LiteratureAgent can read guide as enriched context for synthesis
```

**Pattern C — Quote Verification**
```
1. WritingAgent produces bullet with citation claim
2. Claude Code asks NotebookLM: "Does the literature support claim X? Provide exact quotes."
3. NotebookLM returns grounded response with source passage
4. Claude Code scores confidence: HIGH / MEDIUM / LOW based on citation specificity
5. LOW confidence → mandatory human verification before inclusion
```

**Pattern D — Defense Preparation**
```
1. User asks Claude Code to "prepare me for a defense question on X"
2. Claude Code queries thesis-defense notebook with question
3. NotebookLM returns answer + counter-evidence from sources
4. Claude Code formats as question → likely answer → potential challenge → supporting evidence
```

### Integration in LangGraph

```python
# New node in System B coordinator:
async def notebooklm_enrichment_node(state: ThesisState) -> ThesisState:
    """Queries NotebookLM for current chapter context before WritingAgent runs."""
    chapter = state["current_chapter"]
    notebook_id = NOTEBOOK_MAP[chapter]
    
    enriched_context = await client.chat.ask(
        f"Summarize the key findings relevant to {chapter} from the sources.",
        notebook_id=notebook_id
    )
    
    state["notebooklm_context"] = {
        "answer": enriched_context.answer,
        "citations": enriched_context.citations,
        "verified": False  # Always False until human confirms
    }
    return state
```

---

## 8. Verification / Grounding / Quote-Safety Rules

### Mandatory Rules (Non-Negotiable)

1. **Never pass NotebookLM output directly to WritingAgent** without a `verified: False` flag that must be explicitly cleared by a human.
2. **All quotes** extracted via NotebookLM must be cross-checked against the actual PDF before appearing in any thesis draft.
3. **Study guides and briefing docs** are to be treated as summaries only — not citable as sources. They inform the analyst, not the draft.
4. **Chat citations** (source UUID + passage) provide the nearest passage in the indexed source — they may still be paraphrased. Always check the original PDF at the cited page.
5. **Never use NotebookLM output as evidence** in the validation/evaluation section (SRQ3/SRQ4). These require quantitative results, not AI-generated summaries.

### Trust Level Classification

| Output Type | Trust Level | Use Case | Human Review Required? |
|---|---|---|---|
| Chat answer (general) | LOW | Orientation, hypothesis generation | Yes — before any use |
| Chat citation (passage + source UUID) | MEDIUM | Approximate quote location | Yes — verify against PDF |
| Study guide (Markdown) | LOW-MEDIUM | Literature orientation only | Yes — before citing |
| Briefing doc | LOW-MEDIUM | Context building | Yes — before citing |
| Quiz/Flashcard | MEDIUM | Defense prep | No — low stakes |
| Source fulltext via get_fulltext() | HIGH | Actual indexed content | Spot-check recommended |

### Citation Format Standard

When NotebookLM-sourced material is used in a thesis draft:
```
[Claim/finding] (Author, Year, p. X — verified via NotebookLM citation, PDF confirmed)
```
The `PDF confirmed` tag is required before final submission.

---

## 9. Risk Analysis and Fallback Options

### Risk Table

| Failure Mode | Impact | Detection | Mitigation |
|---|---|---|---|
| **Google breaks undocumented RPC API** | High — all programmatic access fails | 401/500 errors or parsing failures | Fall back to manual NotebookLM UI; all notebooks remain accessible at notebooklm.google.com |
| **Auth session expiry** | Medium — API calls fail silently or with AuthError | AuthError exception in notebooklm-py | Re-run `notebooklm login`; keep manual UI as primary |
| **Rate limiting on artifact generation** | Medium — study guide generation fails | RateLimitError exception | Spread generation across time; cache outputs to disk |
| **Source duplication** | Low-Medium — same paper added twice inflates context | Check ingestion_manifest.json before adding | Idempotency check in ingestion script: skip if source_id already recorded |
| **Provenance ambiguity** | High — "which paper said X" becomes unclear | Citation UUID doesn't resolve cleanly | Always resolve UUID to paper slug via source list; never use floating citations |
| **Quote inaccuracy / paraphrasing** | High — thesis contains inaccurate citations | NotebookLM silently paraphrases instead of quoting | Mandatory PDF verification rule (Section 8); never quote NotebookLM output directly |
| **Automation drift** | Medium — ingestion manifest diverges from actual notebook state | Manifest says paper is in notebook but source was deleted | Periodic manifest reconciliation: compare `client.sources.list()` against manifest |
| **Dependency breaking change** | Low-Medium — notebooklm-py v0.4 changes API | Import errors, changed method signatures | Pin to v0.3.4 in requirements; review CHANGELOG before upgrading |
| **50-source notebook limit** | Medium — chapter notebooks can't hold all papers | SourceError or silent drop | Monitor source count; split notebooks if needed (ch2a-literature, ch2b-literature) |
| **Thesis deadline pressure** | High — integration adds overhead | N/A | Phase 0+1 are low-effort; abort automation if it takes >4 hours to set up |

### Fallback Strategy

**If notebooklm-py breaks entirely:**
- Manual NotebookLM UI remains functional at notebooklm.google.com
- All notebooks created programmatically are still accessible and queryable manually
- Claude Code can still be used to formulate queries for human-to-paste into the UI
- Zero thesis production capability is lost — only the automation layer fails

**If auth is fragile:**
- Create a shared session file updated after each manual login
- Never rely on notebooklm-py for time-critical thesis production work (submission pipeline)

---

## 10. Recommended Adoption Strategy

**Recommendation: Thin Wrapper — Adopt library as-is with thesis-specific orchestration on top**

Do NOT:
- Fork or reimplement the RPC layer (high maintenance, no benefit)
- Build a full Zotero → NotebookLM automated pipeline before May 15
- Use NotebookLM as a primary citation source without human verification
- Integrate NotebookLM into the automated ML pipeline (System A)

DO:
- Install `notebooklm-py` as an additional dependency in System B
- Create a thin `notebooklm_client.py` wrapper that: initializes the client, maps chapter names to notebook IDs, enforces the `verified: False` flag on all outputs
- Create chapter notebooks manually first, verify they work, then automate ingestion
- Use NotebookLM primarily for **literature review support** (Chapter 2) — the highest-value use case given the time constraint
- Cache all generated outputs to disk (study guides, briefing docs) so API fragility doesn't block thesis work

### Architecture Decision Table

| Decision Point | Options | Preferred Option | Rationale |
|---|---|---|---|
| **Source-of-truth for metadata** | Zotero / CSV+Markdown / NotebookLM | CSV + Markdown (current) | Zotero integration is post-deadline scope |
| **Source-of-truth for files** | Google Drive / Local `papers/` folder | Local `papers/` folder in repo | Deterministic paths, no Drive API dependency |
| **Notebook organization** | Per-paper / Per-chapter / Flat | Per-chapter | Mirrors thesis structure, enables cross-paper synthesis |
| **Auth strategy** | Manual browser login / Env var / CI/CD | Manual login + cookie file | Thesis is human-driven workflow; no CI/CD needed |
| **Integration depth** | Full LangGraph node / Standalone script / Manual UI | Standalone script + manual UI (Phase 1), LangGraph node (Phase 2+) | Fail-safe: manual UI always works |
| **Quote trust policy** | Trust directly / Flag always / Never use | Flag always + PDF verification | Academic integrity is non-negotiable |
| **Dependency pinning** | Latest / Pinned / Vendored | Pinned at v0.3.4 | Active development = risk of breaking changes |

---

## 11. Phased Roadmap

### Phase 0 — Capability Audit (1–2 hours) `[Now → 2026-04-14]`

Goal: Confirm the integration works before committing to it.

- [ ] Install `notebooklm-py[browser]` in `.venv`
- [ ] Run `notebooklm login` and verify cookies are captured
- [ ] Create one test notebook: "thesis-test"
- [ ] Add one paper PDF as a source
- [ ] Run `notebooklm ask "What is the main contribution of this paper?"`
- [ ] Generate one study guide: `notebooklm generate report study-guide`
- [ ] Verify citation output format (source UUID + passage)
- [ ] Verify downloaded Markdown study guide quality
- [ ] Document: auth works? Source ingestion works? Chat works? Artifacts work?
- [ ] Decision gate: if auth is broken or rate-limited out of the box → abort and use manual UI only

### Phase 1 — Minimal Viable Integration (4–6 hours) `[2026-04-14 → 2026-04-16]`

Goal: All chapter notebooks set up with confirmed papers; manual workflow established.

- [ ] Create `papers/` directory structure in thesis repo
- [ ] Copy/move all 16 confirmed paper PDFs into `papers/ch2-literature/` (and other chapter folders based on tier/topic)
- [ ] Create 5 chapter notebooks via CLI or Python script
- [ ] Add papers to respective notebooks (use idempotent ingestion script)
- [ ] Create `papers/ingestion_manifest.json` with notebook IDs and source IDs
- [ ] Generate study guides for each chapter notebook → cache to `docs/literature/guides/`
- [ ] Verify study guide quality against known paper annotations
- [ ] Document: does the output quality justify the setup effort?

### Phase 2 — Structured Ingestion Workflow (3–4 hours) `[2026-04-17 → 2026-04-19]`

Goal: Repeatable ingestion from Python; integration with LiteratureAgent.

- [ ] Create `scripts/notebooklm_ingestion.py`:
  - Reads `papers/` directory
  - Checks manifest for already-ingested papers
  - Adds new papers to correct chapter notebook
  - Updates manifest
- [ ] Add `notebooklm_context` field to `ThesisState` (System B)
- [ ] Extend LiteratureAgent to optionally read study guide from `docs/literature/guides/`
- [ ] Test full run: new paper added to `papers/` → ingestion script → NotebookLM source added → guide updated

### Phase 3 — Claude-Assisted Prompting and Orchestration `[2026-04-20 → 2026-04-27]`

Goal: Claude Code can query NotebookLM as part of literature review workflow.

- [ ] Create `notebooklm_client.py` wrapper with chapter → notebook ID map
- [ ] Implement Pattern A (Literature Review QA) as a Claude Code slash command: `/nlm-ask <chapter> <question>`
- [ ] Implement Pattern B (Study Guide) as: `/nlm-guide <chapter>`
- [ ] Implement Pattern C (Quote Verification) in WritingAgent: flag citations for NotebookLM verification
- [ ] Add `verified: bool` field to citation output objects
- [ ] Test on Chapter 2 literature review draft

### Phase 4 — Validation and Hardening `[2026-04-28 → 2026-05-07]`

Goal: Production-ready for thesis submission; defense preparation enabled.

- [ ] Create `thesis-defense` notebook with all papers
- [ ] Implement Pattern D (Defense Preparation) as: `/nlm-defend <question>`
- [ ] Run manifest reconciliation: compare `client.sources.list()` against manifest for each notebook
- [ ] Validate 5 random citations: NotebookLM passage → PDF page → quote accuracy check
- [ ] Document results: citation accuracy rate, false paraphrase rate
- [ ] If accuracy < 90%: add explicit warning in WritingAgent output
- [ ] Freeze notebooks before submission (no more source additions after 2026-05-08)

---

## 12. Immediate Next Actions

1. **Install and test** (today): `pip install notebooklm-py[browser]` in `.venv` and run `notebooklm login`
2. **Phase 0 gate**: 30-minute smoke test to confirm auth, PDF upload, and chat work
3. **Create paper folder**: `mkdir papers/ch2-literature` and copy PDFs for the 16 confirmed Tier A+B papers
4. **Decision point**: After Phase 0, decide whether to continue to Phase 1 or fall back to manual UI exclusively
5. **Do not build Zotero bridge** before May 15 — it's out of scope and would consume time needed for actual thesis writing
6. **Check open issues**: Review the 55 open issues on `teng-lin/notebooklm-py` for any known PDF upload or auth bugs before committing

---

---

## Outcome — Phase 0 Complete (2026-04-13)

**Decision gate: PASSED → proceed to Phase 1.**

| Check | Result |
|---|---|
| Install `notebooklm-py[browser]==0.3.4` | ✅ |
| `notebooklm login` (browser auth) | ✅ |
| `notebooklm source add` (PDF upload) | ✅ |
| `notebooklm ask` (grounded Q&A with citations) | ✅ Citation format confirmed: inline `[1]`, `[2]` with source passage |
| Generate + download study guide | Not tested — treat as low risk given rest passed |

**Findings:**
- Source names = PDF filename. Must use `author_year_shorttitle.pdf` naming convention for clean citations.
- `notebooklm research` (web search) is also relevant for gap analysis — not skip, add to Phase 3+.
- Auth: clean browser flow, no issues.

**Completed (beyond plan):**
- `papers/` directory structure created with chapter subdirectories
- `papers/ingestion_manifest.json` initialized
- `docs/literature/guides/` created
- `thesis_production_system/requirements.txt` updated
- `.env.example` updated with `NOTEBOOKLM_AUTH_JSON`
- `CLAUDE.md` updated with full NotebookLM section
- `CHEATSHEET.md` updated with complete NotebookLM command reference

**Next session (Phase 1):**
1. Delete `thesis-test` notebook
2. Rename paper PDFs to `author_year_shorttitle.pdf` convention
3. Copy to correct `papers/<chapter>/` folders
4. Create 6 chapter notebooks and populate with 16 confirmed papers
5. Run `notebooklm metadata` and populate `ingestion_manifest.json`
6. Generate first study guide for ch2-literature

---

## Critical Files to Modify (When Implementing)

| File | Change |
|---|---|
| `thesis_production_system/requirements.txt` | Add `notebooklm-py[browser]==0.3.4` |
| `thesis_production_system/state/thesis_state.py` | Add `notebooklm_context: Optional[Dict]` field |
| `thesis_production_system/agents/literature_agent.py` | Add optional study guide reader |
| `thesis_production_system/core/coordinator.py` | Add `notebooklm_enrichment_node` (Phase 2+) |
| **New**: `scripts/notebooklm_ingestion.py` | Idempotent ingestion script (Phase 1) |
| **New**: `scripts/notebooklm_client.py` | Thin wrapper with chapter→notebook map |
| **New**: `papers/ingestion_manifest.json` | Source tracking and notebook ID map |
| `CLAUDE.md` | Add NotebookLM section with notebook IDs and rules |
| `.env.example` | Add `NOTEBOOKLM_AUTH_JSON` placeholder |
| `.gitignore` | Add `papers/*.pdf` if PDFs are large; add notebooklm cookie storage |
