# Thesis Repository Upgrade Plan
## CBS Master Thesis — CMT_Codebase

---

## 1. Executive Summary

The current thesis repository is a well-governed but **LaTeX-free, Markdown-first** codebase built around two Python agent systems (research contribution + thesis production). It has strong project architecture and compliance tracking but lacks any document rendering pipeline — there is no way to produce a final thesis PDF today. The two reference repositories contribute complementary patterns: **academic-research-skills** provides an orchestrated workflow with integrity verification gates; **scientific-agent-skills** provides a modular skill architecture. The recommended strategy adopts Markdown → LaTeX (via Pandoc) as the rendering pipeline, imports the integrity gate and handoff schema patterns from academic-research-skills, and restructures agents into SKILL.md-style modules. NotebookLM fits as a verification and defense-prep layer, fed from the Markdown content already authored.

**Data access status (confirmed):** Both Nielsen and Indeks Danmark datasets are fully available — this critical blocker is resolved. Research computation (System A) can proceed immediately.

---

## 2. Current Repository Audit

### 2.1 Folder Structure (Key Paths)
```
CMT_Codebase/
├── .claude/commands/          # REV, REV-brian custom agent commands
├── .claude/settings.local.json
├── ai_research_framework/     # System A: research computation (LangGraph, ML)
│   ├── agents/                # 4 agents (skeleton/placeholder)
│   ├── core/                  # LangGraph coordinator
│   ├── config.py              # Central config (RAM budget, models)
│   └── requirements.txt
├── thesis_production_system/  # System B: thesis writing (Pydantic, 10 agents)
│   ├── agents/builder/        # Autonomous trial loop (5 submodules)
│   └── core/                  # Plan→Execute→Critic coordinator
├── Thesis/                    # Obsidian vault (37 annotated paper notes)
├── docs/
│   ├── thesis/sections/       # 13 Markdown section skeletons (all complete)
│   ├── thesis/figures/        # 6 SVG+PNG architecture diagrams
│   ├── literature/            # Gap analysis, RQ evolution, annotations
│   ├── compliance/            # CBS guidelines, compliance report
│   └── tasks/thesis_state.json
├── generate_figures.py        # 40KB monolith (Graphviz + Matplotlib)
├── CLAUDE.md                  # 383-line master instruction file
└── README.md
```

### 2.2 Build/Render Pipeline
**Status: DOES NOT EXIST.** No LaTeX, no Makefile, no CI, no Pandoc config, no PDF output at all. All thesis content lives as Markdown bullet skeletons.

### 2.3 What Works Well
| Strength | Notes |
|---|---|
| System A/B separation | Clean research vs. writing isolation |
| CLAUDE.md governance | Comprehensive, rule-enforced session management |
| Literature corpus | 37 papers, 3 scraping runs, gap analysis v4 |
| Compliance tracking | All 13 sections marked compliance_checked |
| State management | LangGraph TypedDict + Pydantic for type safety |
| Obsidian integration | 37 annotated notes, seamless knowledge base |
| Page budget tracking | 120-page limit tracked per section |

### 2.4 Weaknesses and Gaps
| Issue | Severity | Category |
|---|---|---|
| No LaTeX/PDF pipeline whatsoever | **CRITICAL** | Output |
| ~~Data access unconfirmed~~ — **CONFIRMED: both datasets available** | ~~CRITICAL~~ RESOLVED | Research |
| System A agents are skeleton code (~75%) | HIGH | Research |
| No integrity verification or checkpoint gates | HIGH | Quality |
| generate_figures.py is 40KB monolith | MEDIUM | Maintainability |
| Hard-coded paths throughout codebase | MEDIUM | Maintainability |
| No CI/CD or automated validation | MEDIUM | DevOps |
| CLAUDE (1).md stale backup | LOW | Cleanup |
| No ADR (Architecture Decision Records) | LOW | Documentation |
| Obsidian machine-specific files in repo | LOW | Collaboration |

---

## 3. Reference Repository Analysis

### 3.1 academic-research-skills (Imbad0202)

**Architecture:** Orchestrated 10-stage pipeline (Research → Write → Integrity → Review → Revise → Re-Review → Re-Revise → Final Integrity → Finalize → Summary). Dispatcher-only orchestrator; 30+ agents for execution.

**Key strengths for thesis use:**
- **Integrity verification gates** at Stage 2.5 (pre-review) and 4.5 (post-revision) with 7-mode AI failure checklist
- **Handoff schemas (v3.3)** — 11 data contracts with HANDOFF_INCOMPLETE errors; enforces schema compliance between stages
- **Material Passport audit trail** — immutable provenance tracking per artifact
- **Style calibration protocol** — learns author voice from samples (6 dimensions)
- **Adaptive checkpoints** — FULL/SLIM/MANDATORY modes; MANDATORY cannot be skipped
- LaTeX → Tectonic → PDF rendering pipeline
- DOI-based citation verification via Semantic Scholar API
- AI usage disclosure built into outputs

**Limitations for thesis use:**
- Max 1 re-revision cycle (thesis committees may require more)
- zh-TW/English only bilingual support
- Re-revision limit inflexibility
- High token cost per cycle ($4–6)
- Semantic Scholar coverage gaps for niche papers

### 3.2 scientific-agent-skills (K-Dense-AI)

**Architecture:** Modular skill library (180+ independent SKILL.md-documented skills, zero orchestration). Installed via `npx skills add`.

**Key strengths for thesis use:**
- **SKILL.md documentation pattern** — standardized format enabling agent skill discovery
- **Modular independence** — each skill is fully self-contained; selective adoption
- **scan_skills.py** — automated skill discovery and compliance validation
- Scientific writing, literature review, citation management, peer review skills
- Open Agent Skills standard (works with Claude Code, Cursor, Codex)

**Limitations for thesis use:**
- Zero workflow orchestration (agents must compose manually)
- No integrity verification or quality gates
- 180+ skills mostly irrelevant (bioinformatics, chemistry, lab automation)
- Requires Python 3.13+

---

## 4. Cross-Repo Comparison Matrix

| Dimension | CMT_Codebase | academic-research-skills | scientific-agent-skills |
|---|---|---|---|
| **Document rendering** | ❌ None | ✅ LaTeX → Tectonic → PDF | ⚠️ Scientific-writing skill only |
| **Integrity gates** | ❌ None | ✅ Stage 2.5 + 4.5 | ❌ None |
| **Workflow orchestration** | ⚠️ Plan→Execute→Critic (skeletal) | ✅ 10-stage pipeline | ❌ Agent-driven only |
| **Citation handling** | ⚠️ Manual APA7 (no validator) | ✅ DOI verification, Semantic Scholar | ⚠️ Citation-management skill |
| **Human checkpoints** | ⚠️ CLAUDE.md rules only | ✅ MANDATORY gates | ❌ None |
| **Audit trail** | ⚠️ thesis_state.json (mutable) | ✅ Material Passport (immutable) | ❌ None |
| **Modular architecture** | ⚠️ Partial (some isolation) | ⚠️ Monolithic agents | ✅ 180+ independent skills |
| **Skill documentation** | ⚠️ CLAUDE.md + REV commands | ⚠️ 4 main SKILL.md files | ✅ SKILL.md per skill |
| **Literature management** | ✅ 37 papers + Obsidian | ✅ Research agent + bibliography | ⚠️ literature-review skill |
| **Compliance checking** | ✅ CBS guidelines extracted | ⚠️ Generic compliance checklist | ❌ None |
| **Agent architecture** | ✅ LangGraph + Pydantic | ✅ Dispatcher pattern | N/A (skill library) |
| **Style calibration** | ❌ None | ✅ 6-dimension voice learning | ❌ None |
| **Claude Code friendliness** | ✅ CLAUDE.md + REV commands | ✅ Native skills | ✅ Native skills |

---

## 5. Gap Analysis

| Gap | Priority | Recommended Solution | Source |
|---|---|---|---|
| **No LaTeX/PDF output pipeline** | P0 | Add Pandoc + CBS LaTeX template | New build (reference academic-research-skills for Tectonic pattern) |
| **No integrity verification** | P1 | Import Stage 2.5/4.5 pattern as thesis checkpoints | Adapt from academic-research-skills |
| **No citation validator / no bibliography.bib** | P1 | Zotero → BibTeX export integrated into build pipeline | Adapt from scientific-agent-skills citation-management skill |
| **No style consistency check** | P2 | Adapt style_calibration_protocol | Adapt from academic-research-skills |
| **Agents not SKILL.md-documented** | P2 | Add SKILL.md to each agent directory | Adapt from scientific-agent-skills |
| **generate_figures.py monolith** | P2 | Modularize into per-figure scripts | New design |
| **Hard-coded paths** | P2 | Centralize in config.py | Internal refactor |
| **No handoff schema enforcement** | P3 | Import handoff_schemas concept | Adapt from academic-research-skills |
| **No audit trail for writing** | P3 | Lightweight Material Passport pattern | Adapt from academic-research-skills |
| **No defense preparation workflow** | P3 | NotebookLM integration (see §8) | New design |
| **Builder Agent unclear purpose** | P3 | Clarify role or remove | Internal decision |
| **CLAUDE (1).md stale file** | P4 | Delete | Cleanup |

**What NOT to import:**
- academic-research-skills' 10-stage journal-publication pipeline (thesis ≠ journal)
- scientific-agent-skills' bioinformatics/chemistry/quantum skills (irrelevant domain)
- Semantic Scholar API dependency (coverage gaps; use DOI manual check instead)
- Bilingual (zh-TW) abstract agents (unnecessary)
- Re-revision limit enforcement (thesis needs flexibility)

---

## 6. Recommended Target Architecture

### 6.1 End-State Overview
```
Markdown Sections (thesis/writing/sections/)
         │
         ▼
  [Pandoc + CBS LaTeX template]
         │
         ▼
  LaTeX source (.tex files) ← Optional: sync to Overleaf
         │
         ▼
  [LaTeX compiler: pdflatex or tectonic]
         │
         ▼
         PDF
```

**Agent interaction model:**
- System A agents feed research findings → Markdown sections (via WritingAgent)
- System B WritingAgent outputs Markdown prose (bullets → prose conversion)
- Build script converts Markdown → LaTeX → PDF
- Integrity gates validate at section completion and full draft completion
- NotebookLM receives exported Markdown for grounded Q&A and defense prep

### 6.2 Document/Template Strategy

**Recommended: Single CBS-compliant LaTeX template (one-column)**
- File: `templates/cbs_thesis.cls` (or `cbs_thesis.tex` preamble)
- Based on standard memoir or report class with CBS formatting
- Covers: frontpage, abstract, TOC, chapters, appendices, bibliography (APA7 via biblatex)
- Local rendering via pdflatex (cross-platform, no Tectonic required)
- Overleaf sync: optional, via `overleaf-sync` CLI or manual upload

**One-column rationale:**
- CBS master theses use standard A4 one-column format (consistent with CBS guidelines extracted)
- Two-column is appropriate for conference papers/journal articles (ACM, IEEE) — not appropriate here
- Obsidian Markdown → Pandoc → LaTeX works cleanly in one-column
- No layout switch needed

### 6.3 Build Flow (Proposed)
```
Makefile targets:
  make pdf        → pandoc → pdflatex → thesis.pdf
  make check      → integrity gate (citation check + structure check)
  make figures    → python generate_figures.py [modularized]
  make clean      → remove build artifacts
```

### 6.4 Validation/Review Checkpoints
Adapted from academic-research-skills (not full 10-stage, but key gates):
- **Gate 1 (Pre-Draft):** All section bullet skeletons reviewed, page budget checked
- **Gate 2 (Post-Draft):** Prose written, citation format validated (APA7 spot check)
- **Gate 3 (Pre-Submission):** Full integrity check (7-mode AI failure checklist), figures verified, CBS compliance recheck

### 6.5 Citation/Reference Flow
- Bibliography managed in `bibliography.bib` (BibTeX format)
- biblatex + biber for APA7 formatting in LaTeX
- Citations referenced from Obsidian paper annotations (REV output)
- Manual DOI verification for all Tier A/B papers (no API dependency)

---

## 7. Template/Layout Recommendation

### Decision Table: Template Options

| Option | Format | CBS Compliant | Overleaf | Agent-Friendly | Effort |
|---|---|---|---|---|---|
| **Pandoc + custom cbs_thesis.cls** | 1-col LaTeX | ✅ Yes | ✅ Optional sync | ✅ High | Medium |
| Pure Overleaf editing | 1-col LaTeX | ✅ Yes | ✅ Native | ⚠️ Low | Low |
| Markdown only → PDF via WeasyPrint | 1-col HTML/CSS | ⚠️ Partial | ❌ No | ✅ High | Low |
| IEEE two-column template | 2-col LaTeX | ❌ No | ✅ Yes | ✅ High | Low |
| ACM two-column template | 2-col LaTeX | ❌ No | ✅ Yes | ✅ High | Low |

**Recommended:** Option 1 — Pandoc + custom cbs_thesis.cls

**Overleaf strategy (confirmed):**
- User has existing template from a previous project on a separate Overleaf account
- Do NOT build the primary workflow around Overleaf (renders on remote server, limited agent interaction)
- Use Overleaf as an **optional sync target** only: periodically upload `build/thesis.tex` for advisor review or formatting verification
- Primary source of truth remains the local repo (Markdown → Pandoc → LaTeX → PDF)
- Existing Overleaf template should be fetched and used as CBS formatting reference when building `cbs_thesis.cls`

**Authoring model (confirmed): Pandoc bridge (Markdown-first)**
- Aligns with what academic-research-skills uses (Pandoc intermediate + Tectonic/pdflatex final)
- Claude Code agents edit `.md` files natively — no LaTeX syntax errors
- Formula support: Pandoc passes `$...$` and `$$...$$` LaTeX math through to the .tex output cleanly
- Full LaTeX formatting control preserved in `cbs_thesis.cls` template

**One-column vs. Two-column verdict:**
- CBS master thesis → **one-column** (mandatory)
- IEEE/ACM two-column → appropriate only for journal papers derived from thesis after submission
- Pandoc template supports both; thesis uses one-column; paper submission adapts template

**Forked repos in VSCode (confirmed):**
- **Not necessary to clone locally.** Files will be fetched from GitHub via WebFetch during implementation as needed.
- No additional workspace configuration required.

---

## 8. NotebookLM Integration Plan

### 8.1 Where NotebookLM Fits

```
REPO                                    NOTEBOOKLM
────────────────────                    ────────────────────────
Markdown sections        ──export──►    Source documents
(thesis/writing/sections/)                 (upload as PDF/text)

Obsidian paper notes     ──export──►    Literature corpus
(Thesis/papers/)                        (upload annotations)

CBS guidelines PDFs      ──direct──►    Institutional context
(Thesis/Thesis Guidelines/)

Experiment results       ──export──►    Findings verification
(docs/tasks/, JSON)
```

### 8.2 Recommended Uses

| Use Case | How | When |
|---|---|---|
| **Source grounding verification** | Ask NotebookLM "Does claim X appear in the literature?" | Before Gate 2 and Gate 3 |
| **Hallucination reduction** | Cross-check LLM-written prose against uploaded sources | After each WritingAgent section |
| **Literature Q&A** | "What do papers say about demand forecasting in retail?" | During writing of Ch.2, Ch.5, Ch.7 |
| **Consistency checking** | "Does Ch.6 contradict any statement in Ch.3?" | Pre-submission |
| **Defense preparation** | Generate likely examiner questions from thesis text | 2–3 weeks before defense |
| **Argument stress-testing** | Ask "What are the three strongest weaknesses in the methodology?" | After Gate 2 |

### 8.3 Inputs to NotebookLM

| Export from Repo | Format | Frequency |
|---|---|---|
| Final section Markdown files | PDF (pandoc-rendered) | After Gate 2 |
| Obsidian paper annotations | Markdown (batch export) | After each scraping run |
| CBS guidelines PDFs | PDF (direct) | Once |
| Gap analysis + RQ evolution | Markdown | Once |
| Experiment result summaries | Markdown | After Phase 4 |

### 8.4 What Stays in Repo (NOT NotebookLM)

- Python code / agent logic
- Raw data (Nielsen, Indeks Danmark)
- Git history
- CLAUDE.md agent instructions
- Build scripts

### 8.5 NotebookLM Limitations

- No persistent memory between sessions (re-upload needed for fresh analysis)
- Cannot verify code or data — only natural language text
- Not a replacement for human academic proofreading
- Does not enforce citation format (do not rely on it for APA7 checking)

---

## 9. Phased Implementation Roadmap

### Phase 0: Analysis Complete (NOW) ✅
**Status:** This plan document is Phase 0.

**Deliverables:**
- [x] Current repo audit (documented above)
- [x] Reference repo analysis (documented above)
- [x] Gap analysis (§5)
- [x] Architecture recommendation (§6)
- [x] Template recommendation (§7)

---

### Phase 1: Architecture Decisions (Week 1)
**Goal:** Resolve critical template and tooling decisions before any building.

**Tasks:**
1. Decision: Confirm CBS thesis formatting requirements (A4, font, margin, page numbering)
2. Decision: Confirm Overleaf sync is desired (adds complexity) or local-only
3. Decision: Confirm Pandoc as Markdown → LaTeX bridge (vs. pure LaTeX authoring)
4. Decision: Clarify Builder Agent (thesis_production_system/agents/builder/) purpose — keep or remove
5. Verify CBS guidelines PDFs for exact formatting specs

**Deliverables:**
- `docs/decisions/ADR-001-template-strategy.md`
- `docs/decisions/ADR-002-build-pipeline.md`
- `docs/decisions/ADR-003-builder-agent-fate.md`

**Dependencies:** None (analysis only)
**Risk:** CBS may have specific formatting requirements not yet extracted
**Payoff:** Prevents costly rework in later phases

---

### Phase 2: Quick Wins and Low-Risk Cleanup (Week 1–2)
**Goal:** Remove obvious dead weight; add missing structure.

**Tasks:**
1. **Delete** `CLAUDE (1).md` (confirmed stale backup)
2. **Add** `templates/` directory with `cbs_thesis_template.tex` stub
3. **Add** `Makefile` with `make pdf`, `make check`, `make figures` targets (stubs OK)
4. **Set up Zotero Better BibTeX auto-export** — configure Zotero to auto-export collection to `bibliography.bib` in repo root (replaces manual .bib seeding). Adapted from scientific-agent-skills citation-management skill pattern.
5. **Centralize path config** — add `PATHS` dict to `ai_research_framework/config.py` for `SECTIONS_DIR`, `FIGURES_DIR`, etc.
6. **Add SKILL.md** to each agent directory (document what agent does, inputs, outputs)
7. **Update .gitignore** to exclude `build/`, `*.pdf`, `*.aux`, `*.log` (LaTeX artifacts)

**Zotero integration detail:**
- Install Zotero plugin: [Better BibTeX for Zotero](https://retorque.re/zotero-better-bibtex/)
- Configure collection export: File → Export Library → Better BibTeX format → check "Keep Updated"
- Export path: `CMT_Codebase/bibliography.bib`
- Result: Every paper added to Zotero auto-syncs to the repo's .bib file; Pandoc/LaTeX picks it up automatically
- Citation keys: Use `[auth:lower][year]` format (e.g., `smith2023`) for consistency with Markdown `[@smith2023]` syntax

**Critical files to modify:**
- `CLAUDE.md` — add build/render instructions
- `ai_research_framework/config.py` — add PATHS dict
- `.gitignore` — add LaTeX artifacts

**Dependencies:** Phase 1 decisions
**Risk:** Low — all additive or deleting stale files
**Payoff:** Foundation for Phase 3; eliminates confusion from stale files

---

### Phase 3: Core Pipeline Build (Week 2–3)
**Goal:** Working Markdown → PDF render chain.

**Tasks:**
1. **Create `templates/cbs_thesis.cls`** (or `cbs_thesis.tex` preamble)
   - Based on LaTeX `report` class
   - CBS formatting: A4, 2.5cm margins, Times New Roman 12pt (or Palatino)
   - Sections: frontpage, abstract, TOC, chapters, bibliography, appendices
   - biblatex + biber for APA7
2. **Create `pandoc/thesis.yaml`** (Pandoc metadata file)
   - Author, title, supervisor, institution, date, keywords
   - Template reference: `templates/cbs_thesis.cls`
3. **Create `pandoc/thesis_build.sh`** (or add to Makefile)
   - Concatenate section Markdown files in chapter order
   - Run Pandoc → LaTeX → pdflatex
   - Output to `build/thesis.pdf`
4. **Test render** with current Markdown sections (even bullets compile to PDF)
5. **Verify Overleaf sync** if desired (manual upload test)

**Adapting from academic-research-skills:**
- Reference Tectonic/pdflatex invocation pattern
- Reference LaTeX preamble structure (not full adoption)

**Key files to create:**
- `templates/cbs_thesis.cls`
- `pandoc/thesis.yaml`
- `Makefile`
- `build/.gitkeep`

**Dependencies:** Phase 2 complete, CBS formatting specs confirmed (Phase 1)
**Risk:** Medium — LaTeX template may need iteration for CBS compliance
**Payoff:** First PDF render of thesis; unblocks all downstream work

---

### Phase 4: Integrity Gates and Validation (Week 3–4)
**Goal:** Add quality checkpoints adapted from academic-research-skills.

**Tasks:**
1. **Create `scripts/check_integrity.py`**
   - Gate 1 (pre-draft): section completeness, page budget validation
   - Gate 2 (post-draft): citation format spot check (APA7 pattern match), figure reference validation
   - Gate 3 (pre-submission): AI usage disclosure present, CBS compliance checks
2. **Create `thesis/compliance/integrity_checklist.md`**
   - 7-mode AI failure checklist (adapted from academic-research-skills Stage 2.5/4.5)
   - Thesis-specific modes: CBS compliance, page budget, data integrity claims
3. **Add integrity check to Makefile** (`make check`)
4. **Export NotebookLM package** — script to batch-export section Markdown as PDF
5. **Add Gate triggers to CLAUDE.md** — specify when integrity checks must run

**Adapting from academic-research-skills:**
- Stage 2.5/4.5 integrity gate concept
- 7-mode failure checklist (adapted for thesis rather than journal)
- Lightweight Material Passport: add provenance frontmatter to section files

**Key files to create:**
- `scripts/check_integrity.py`
- `thesis/compliance/integrity_checklist.md`

**Dependencies:** Phase 3 (PDF pipeline must exist to test)
**Risk:** Low — checks are additive; no existing behavior changes
**Payoff:** Catches errors before Gate 3 submission; builds confidence

---

### Phase 5: Workflow Hardening and Final Validation (Week 4+)
**Goal:** Production-ready workflow for thesis completion.

**Tasks:**
1. **Modularize generate_figures.py** — split into per-figure scripts or at minimum per-figure functions
2. **Add CI-equivalent validation** — pre-commit hook or script that runs `make check` on commit
3. **Defense prep NotebookLM export** — create `scripts/export_notebooklm.py` to package thesis + annotations
4. **Final end-to-end test** — full Markdown → PDF render with all 13 sections
5. **Validate bibliography.bib** completeness against 37 papers
6. **ADR documentation** — write remaining ADRs for Builder Agent and synthesis scoring decisions

**Dependencies:** All prior phases, data access confirmed (parallel track)
**Risk:** Low — hardens existing pipeline
**Payoff:** Submission-ready workflow

---

## 10. Feature Adoption Decision Table

| Feature | Source Repo | Why Useful | Integration Effort | Risk | Recommendation |
|---|---|---|---|---|---|
| Integrity verification gates (Stage 2.5/4.5) | academic-research-skills | Catches AI hallucinations and structural errors before advisor review | Medium | Low | **Adapt** — simplify to 3-gate model for thesis |
| LaTeX → PDF pipeline (Tectonic pattern) | academic-research-skills | Reference for pdflatex invocation, preamble structure | Low | Low | **Adopt** — use pdflatex locally (drop Tectonic) |
| Handoff schema enforcement | academic-research-skills | Validates agent outputs before next stage | High | Medium | **Adapt** — lightweight version (Pydantic validation, not full 11-schema) |
| Material Passport audit trail | academic-research-skills | Immutable provenance tracking for thesis artifacts | Medium | Low | **Adapt** — YAML frontmatter in section files |
| Style calibration protocol | academic-research-skills | Maintains consistent author voice across chapters | Medium | Low | **Adopt** — feed 3+ writing samples to CLAUDE.md |
| Adaptive checkpoint system (FULL/SLIM/MANDATORY) | academic-research-skills | Right-sizes human review burden | Low | Low | **Adopt** — add to CLAUDE.md checkpoint definitions |
| SKILL.md documentation pattern | scientific-agent-skills | Enables agent skill discovery and self-documentation | Low | None | **Adopt directly** — add SKILL.md to each agent dir |
| scan_skills.py pattern | scientific-agent-skills | Automated skill compliance validation | Medium | Low | **Adapt** — simplified validator for thesis skills |
| Modular skill architecture | scientific-agent-skills | Extensibility, selective adoption | Medium | Low | **Adapt** — restructure agents as discrete skills |
| Scientific writing skill | scientific-agent-skills | May contain useful prose generation patterns | Low | None | **Evaluate** — read content, adopt relevant patterns |
| **Zotero-based citation management skill** | scientific-agent-skills | User already uses Zotero; eliminates manual .bib maintenance; APA7 export via Zotero's Better BibTeX | Low | Low | **Adopt directly** — configure Zotero Better BibTeX → auto-export to `bibliography.bib` on save |
| Full 10-stage pipeline | academic-research-skills | Overkill for thesis workflow | High | High | **Reject** — design thesis-specific stages instead |
| Semantic Scholar API integration | academic-research-skills | Coverage gaps, API dependency | High | High | **Reject** — use manual DOI verification |
| zh-TW bilingual abstracts | academic-research-skills | Not needed for CBS thesis | N/A | N/A | **Reject** |
| Max 1 re-revision enforcement | academic-research-skills | Inflexible for thesis committee cycles | N/A | N/A | **Reject** |
| Bioinformatics/chemistry skills | scientific-agent-skills | Domain-specific; irrelevant | N/A | N/A | **Reject** |

---

## 11. Risks and Open Questions

### Critical Risks
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Data access delayed beyond 2026-04-30 | High | Critical | Escalate data access as separate urgent track; prepare synthetic data fallback |
| CBS LaTeX formatting specs unclear | Medium | High | Extract from CBS guidelines PDFs in Phase 1 before building template |
| Thesis deadline (2026-05-15) conflict with upgrade work | Medium | High | Phase 1–2 must complete by 2026-04-20; Phase 3+ only if data is flowing |
| Pandoc → LaTeX introduces formatting issues | Low | Medium | Test render early (Phase 3, week 1) with real content |

### Open Questions (Require User Decision)
1. **Overleaf sync desired?** — If yes, adds `overleaf-sync` tooling step; if no, local-only render is simpler.
2. **Builder Agent fate** — Is `thesis_production_system/agents/builder/` for automated hyperparameter tuning or manual tracking? If unclear, remove.
3. **Pandoc vs. pure LaTeX authoring** — Should sections remain as Markdown (Pandoc bridge) or be rewritten directly in LaTeX? Markdown preferred for agent-friendliness.
4. **Obsidian vault in repo** — Should Obsidian metadata (`.obsidian/workspace.json`) be gitignored to prevent merge conflicts?
5. **NotebookLM export frequency** — Weekly batch export or per-Gate exports only?

---

## 12. Quick Wins (Safe Immediate Actions)

These are small, isolated, low-risk improvements that could be done immediately:

| Action | File(s) | Effort | Value |
|---|---|---|---|
| Delete `CLAUDE (1).md` | `CLAUDE (1).md` | 1 min | Removes confusion |
| Add LaTeX artifacts to `.gitignore` | `.gitignore` | 2 min | Prevents accidental commits |
| Add `build/` directory stub | `build/.gitkeep` | 1 min | Prepares for Phase 3 |
| Set up Zotero Better BibTeX auto-export | Zotero config + `bibliography.bib` | 15 min | All 37 papers auto-synced; future papers auto-added |
| Add `templates/` directory stub | `templates/README.md` | 5 min | Signals template intent |
| Gitignore Obsidian workspace.json | `.gitignore` | 2 min | Prevents merge conflicts |
| Add PATHS dict to config.py | `ai_research_framework/config.py` | 15 min | Centralizes hard-coded paths |

---

## 13. Prioritized Action List

**P0 — Immediate (before any code changes):**
1. Confirm CBS thesis LaTeX formatting requirements (extract from Thesis Guidelines/ PDFs)
2. ~~Confirm Overleaf sync~~ — **DECIDED:** Local Pandoc pipeline primary; Overleaf optional sync only
3. Confirm Builder Agent purpose or removal decision
4. ~~Confirm data access~~ — **CONFIRMED:** Data access is now available
5. Fetch existing Overleaf template (from user's Overleaf account) as CBS formatting reference for `cbs_thesis.cls`
6. ~~Add forked repos to VSCode~~ — **NOT NEEDED:** Fetch specific files from GitHub as needed during implementation

**P1 — Phase 2 Quick Wins (this week):**
5. Delete `CLAUDE (1).md`
6. Add LaTeX/build artifacts to `.gitignore`
7. **Set up Zotero Better BibTeX auto-export → `bibliography.bib`** (replaces manual seeding)
8. Add PATHS dict to `config.py`
9. Create `templates/` directory stub
10. Gitignore `.obsidian/workspace.json`

**P2 — Phase 3 Pipeline (Week 2–3):**
11. Draft `templates/cbs_thesis.cls` (CBS-compliant LaTeX preamble)
12. Create `pandoc/thesis.yaml` metadata
13. Create `Makefile` with `make pdf` and `make check` targets
14. First end-to-end render test (Markdown → PDF)
15. Add SKILL.md to each agent directory

**P3 — Phase 4 Integrity (Week 3–4):**
16. Create `scripts/check_integrity.py` (Gate 1/2/3 checks)
17. Create `thesis/compliance/integrity_checklist.md`
18. Add adaptive checkpoints to CLAUDE.md
19. First NotebookLM export package (batch Markdown → PDF)

**P4 — Phase 5 Hardening (Week 4+, data-dependent):**
20. Modularize `generate_figures.py`
21. Defense prep NotebookLM workflow
22. Full bibliography validation (37 papers)
23. Final pre-submission integrity gate run
