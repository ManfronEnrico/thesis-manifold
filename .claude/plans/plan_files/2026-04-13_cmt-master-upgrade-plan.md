# CMT_Codebase Master Upgrade Plan
## Synthesized from: zippy-launching-quail.md (forked repo analysis) + shimmying-gathering-flute.md (PTA best-practices analysis)

---

## 1. Executive Synthesis

**Core decision:** The two plans address entirely different domains and are largely complementary, not competing. The forked repo plan defines *what to build* (architecture, LaTeX pipeline, integrity gates). The PTA plan defines *how Claude operates* (rules, workflows, automation model). The synthesis is straightforward: adopt the forked repo plan as the primary roadmap and inject PTA's operational infrastructure as a pre-phase that runs in parallel with Phase 1 architecture decisions.

**Four critical synthesis decisions:**

| Decision | Resolution | Rationale |
|---|---|---|
| Clone reference repos locally? | **YES — do this first** | Direct file reads via VSCode/Claude Code are faster and more reliable than WebFetch. GitHub rate limits and network failures block template extraction. Clone academic-research-skills and scientific-agent-skills as additional working directories. Remove after extraction. |
| PreToolUse hook (PTA marked "Conditional") | **ADOPT** — mandatory | CMT_Codebase IS on an OneDrive path (`C:\Users\brian\OneDrive\...`). The corruption risk is real. |
| Priority conflict: .claude/ infra vs. LaTeX pipeline | **Both are P0, parallel tracks** | .claude/ setup takes 4–5 hours and is additive/zero-risk. LaTeX pipeline requires Phase 1 decisions first. These do not block each other. |
| Standup workflow | **ADAPT from PTA** | Forked repo plan is silent on this. PTA's standup lifecycle provides cross-session continuity critical for a thesis with a supervisor meeting cadence. |

**Summary verdict:** The forked repo plan is architecturally correct and complete. The PTA plan fills its operational gap (Claude rules, session continuity, safety). Merged, they produce a production-grade thesis development environment.

---

## 2. Plan Comparison Summary

### Agreements (Both Plans)
- CLAUDE.md as navigation hub with linked rules (not a monolithic spec)
- `.claude/rules/` and `.claude/skills/` as the primary Claude governance layer
- Plan lifecycle: YYYY-MM-DD naming + Outcome sections
- Git commit deduction workflow (multi-session aware)
- Repository map as a dedicated file separate from CLAUDE.md
- Phase-based decomposition with files ≤400 lines

### Conflicts (Resolved Below)

| Conflict | PTA Position | Forked Repo Position | Resolution |
|---|---|---|---|
| What is P0? | Bootstrap .claude/ infra first (highest ROI) | LaTeX/PDF pipeline first (CRITICAL gap) | Parallel tracks — not actually in conflict |
| PreToolUse hook | Conditional (if OneDrive path applies) | Silent | ADOPT — path confirmed as OneDrive |
| Standup workflow detail | Full 4-phase lifecycle defined | Not mentioned | Follow PTA's design |
| Docs update order | 7-document ordered workflow | Not mentioned | Follow PTA's design, adapted for thesis docs |

### Unique Contributions

**PTA only** (no equivalent in forked repo plan):
- Standup lifecycle (4-phase: log/prep/finalize/init)
- Context-token optimization guide
- One-off execution default rule
- Known TODOs / frozen decisions pattern in CLAUDE.md
- `docs/tooling-issues.md` living registry
- `project_updates/` session memory directory
- Ordered docs update workflow

**Forked repo only** (no equivalent in PTA plan):
- LaTeX → PDF rendering pipeline (Pandoc + cbs_thesis.cls)
- 3-gate integrity verification model
- NotebookLM integration design
- SKILL.md per-agent documentation pattern
- Zotero Better BibTeX auto-export → bibliography.bib
- ADR (Architecture Decision Records) pattern
- Makefile (make pdf / make check / make figures)
- generate_figures.py modularization

---

## 2.5 Actual Repo State (from 2026-04-13 FileFolderTree — authoritative)

Key facts that correct or refine the forked repo plan's audit:

| Observation | Impact on Plan |
|---|---|
| `.gitignore` already exists | Phase 2: UPDATE it, do not create it |
| `scripts/` dir already exists (`explore_nielsen.py`) | Phase 3/4: ADD `check_integrity.py` here, don't create the dir |
| `tests/` dir exists (`test_builder_integration.py`) | Noted; add integrity tests here in Phase 4 if desired |
| `CHEATSHEET.md` at repo root | Include in `/update_all_docs` workflow; reference in CLAUDE.md |
| `README_builder.md` at root | Include in docs update workflow; separate from README.md |
| `docs/experiments/` exists (experiment_registry.json + experiment_summary.md) | Add to repository_map.md |
| `ai_research_framework/templates/` exists (base_config.py) | Do NOT overwrite; thesis `templates/` is a NEW top-level dir |
| `Thesis/papers/` has **24** Obsidian notes | Correct "37 papers" references in plan |
| `thesis/literature/papers/` has **49** annotated `.md` files | Authoritative literature count; use 49 in bibliography validation |
| `thesis_production_system/agents/builder/` has 6 substantive files (architect, builder_graph, coder, evaluator, executor, experiment_registry) | Builder is more developed than "unclear purpose" implies; decision needed but lean toward keep + SKILL.md |
| `.env` and `.env.example` both present | Hook must block `.env` writes (already in PTA hook design) |
| `.claude/settings.local.json` exists | Create `.claude/settings.json` as NEW file (separate from local); do not overwrite settings.local.json |
| `CLAUDE (1).md` confirmed present | Safe to delete |
| `thesis/compliance/` has `cbs_guidelines_notes.md` + `compliance_report_20260315.md` | Add `integrity_checklist.md` here in Phase 4 |

---

## 3. Weighting and Decision Logic

**Forked repo (HIGH weight) governs:**
- All LaTeX/template decisions — the CBS formatting requirements are non-negotiable
- Thesis workflow architecture — System A → System B → Markdown → PDF
- Integrity gates — adapt from academic-research-skills (3-gate model)
- Agent documentation — SKILL.md per agent
- Citation management — Zotero Better BibTeX auto-export
- NotebookLM integration
- ADR documentation

**PTA (MEDIUM weight, process layer only) governs:**
- Claude rules infrastructure (`.claude/rules/`, `.claude/skills/`)
- Standup workflow design and skill files
- Context-token optimization strategy
- Tooling-issues registry pattern
- Repository map design
- CLAUDE.md structure and Known TODOs pattern
- PreToolUse hook (now confirmed necessary)

**Neither plan governs / New decisions:**
- Repo path for `.claude/plans/` — use project-local `.claude/plans/` (not global `~/.claude/plans/`) per PTA convention
- Obsidian workspace.json — gitignore (low-priority quick win)

---

## 4. Final Target Architecture

```
CMT_Codebase/
│
├── .claude/                            ← [PTA] Claude operating environment
│   ├── hooks/
│   │   └── check_file_edit.py          ← OneDrive corruption safety enforcer
│   ├── rules/                          ← 8 auto-loaded rule files (see §6)
│   ├── skills/                         ← 7 adapted slash command skills (see §6)
│   ├── plans/                          ← YYYY-MM-DD dated plan files + Outcomes
│   └── settings.json                   ← PreToolUse hook registration
│
├── .claude/commands/                   ← [EXISTING] REV, REV-brian commands
│
├── ai_research_framework/              ← [EXISTING] System A: research computation
│   ├── agents/
│   │   └── [each agent dir]/SKILL.md   ← [forked-repo] Self-documenting skills
│   └── config.py + PATHS dict          ← [forked-repo] Centralized path config
│
├── thesis_production_system/           ← [EXISTING] System B: thesis writing
│   └── agents/
│       └── [each agent dir]/SKILL.md   ← [forked-repo] Self-documenting skills
│
├── Thesis/                             ← [EXISTING] Obsidian vault (24 notes + data models)
│
├── docs/
│   ├── thesis/sections/                ← [EXISTING] 13 Markdown section skeletons
│   ├── thesis/figures/                 ← [EXISTING] 6 SVG+PNG diagrams
│   ├── decisions/                      ← [forked-repo] ADR files
│   │   ├── ADR-001-template-strategy.md
│   │   ├── ADR-002-build-pipeline.md
│   │   └── ADR-003-builder-agent-fate.md
│   ├── compliance/
│   │   ├── integrity_checklist.md      ← [forked-repo] 7-mode AI failure checklist
│   │   └── [existing CBS guidelines]
│   └── literature/                     ← [EXISTING] gap analysis, RQ evolution
│
├── templates/
│   └── cbs_thesis.cls                  ← [forked-repo] CBS-compliant LaTeX template
│
├── pandoc/
│   ├── thesis.yaml                     ← [forked-repo] Pandoc metadata
│   └── thesis_build.sh                 ← [forked-repo] Build script
│
├── scripts/                           ← [EXISTING dir] explore_nielsen.py + new additions
│   ├── explore_nielsen.py             ← existing
│   ├── check_integrity.py             ← [forked-repo] Gate 1/2/3 checks (ADD)
│   └── export_notebooklm.py           ← [forked-repo] batch export (ADD)
│
├── build/                             ← [forked-repo] gitignored output dir
│   └── .gitkeep
│
├── project_updates/                   ← [PTA] Standup lifecycle + session memory
│   ├── standup_draft.md
│   ├── standup_draft_archive.md
│   └── standup_draft_formatting.md
│
├── dev/
│   └── repository_map.md              ← [PTA] Fast session orientation
│
├── bibliography.bib                   ← [forked-repo] Zotero auto-export target
├── Makefile                           ← [forked-repo] make pdf / check / figures
├── CLAUDE.md                          ← [MERGED] Navigation hub + thesis rules
├── .gitignore                         ← [EXISTING] UPDATE: +LaTeX artifacts, Obsidian ws
└── README.md
```

---

## 5. Integrated Workflow Design

### Track 1: Content Production (PRIMARY — forked repo)

```
System A (LangGraph agents)
        │
        ▼ research findings + data analysis
System B WritingAgent
        │
        ▼ Markdown sections (thesis/writing/sections/)
[INTEGRITY GATE 1 — Pre-Draft]
  • Section completeness check
  • Page budget validation (120-page limit)
  • Bullet skeleton review complete
        │
        ▼ prose expansion approved
[Pandoc pipeline: make pdf]
  • Concatenate section Markdown in chapter order
  • Pandoc → LaTeX (cbs_thesis.cls template)
  • pdflatex → build/thesis.pdf
        │
[INTEGRITY GATE 2 — Post-Draft]
  • APA7 citation format spot check
  • Figure reference validation
  • NotebookLM hallucination cross-check
        │
        ▼
[INTEGRITY GATE 3 — Pre-Submission]
  • 7-mode AI failure checklist (make check)
  • CBS compliance recheck
  • AI usage disclosure present
  • Full bibliography validation (49 docs/literature papers)
        │
        ▼
    thesis.pdf  →  [optional] Overleaf sync for advisor review
```

### Track 2: Claude Operations (SUPPORT — PTA)

```
Session start:
  CLAUDE.md → docs/dev/repository_map.md → docs/tooling-issues.md (mandatory read)

Session work:
  Log progress to project_updates/standup_draft.md

Supervisor meeting prep:
  /prep_standup → /finalize_standup → /init_standup

Planning:
  EnterPlanMode → .claude/plans/YYYY-MM-DD_slug.md → execute → /update_plan

Commits:
  /draft_commit (deduced from session context + standup + git log)

Docs update:
  /update_all_docs (ordered: standup → sections → compliance → CLAUDE.md → CHEATSHEET.md → README → README_builder.md → plans → rules)
```

### Track 2 PTA enhancements clearly marked:

| Enhancement | Source | Where It Applies |
|---|---|---|
| `[PTA]` Standup 4-phase lifecycle | PTA | Cross-session continuity, supervisor meetings |
| `[PTA]` Mandatory tooling-issues pre-read | PTA | Before any plan or task |
| `[PTA]` YYYY-MM-DD plan naming + Outcome | PTA | All planning sessions |
| `[PTA]` Ordered docs update workflow | PTA | After major writing sessions |
| `[PTA]` Context-token optimization | PTA | Model tier selection, compaction timing |
| `[PTA]` One-off execution default | PTA | Prevents accidental recurring automation |
| `[PTA]` Known TODOs / frozen decisions | PTA | Methodological choices Claude must not override |

---

## 6. Claude Rules / Repo Conventions (Final Set)

### `.claude/rules/` — 8 Rule Files

| File | Source | Action | Notes |
|---|---|---|---|
| `context-token-optimization.md` | PTA | Copy directly | Model tier, compact timing, session checklist |
| `repository-map-reference.md` | PTA | Adapt | Point to `docs/dev/repository_map.md` |
| `tooling-issues-workflow.md` | PTA | Copy directly | Mandatory pre-task read of tooling-issues.md |
| `trigger-standup-workflow.md` | PTA | Adapt | Rename supervisor field; adjust PRIMARY=writing/SECONDARY=infra |
| `trigger-plan-workflow.md` | PTA | Copy directly | Plan lifecycle identical |
| `trigger-git-commit-workflow.md` | PTA | Copy directly | Commit deduction identical |
| `trigger-docs-workflow.md` | PTA | Adapt | Replace parser docs list with: sections/ → compliance/ → CLAUDE.md → CHEATSHEET.md → README → README_builder.md → plans → rules |
| `one-off-execution.md` | PTA | Copy directly | Prevents unintended automation |

### `.claude/skills/` — 7 Skill Files

| Skill | Source | Action |
|---|---|---|
| `log_standup` | PTA | Adapt: path to `project_updates/standup_draft.md`; adjust section headers for thesis context |
| `prep_standup` | PTA | Adapt: supervisor name; strip meta-notes re: methodology debates |
| `finalize_standup` | PTA | Copy structure; update file naming |
| `init_standup` | PTA | Copy structure; adjust carry-over rules |
| `draft_commit` | PTA | Copy directly |
| `update_plan` | PTA | Copy directly |
| `update_all_docs` | PTA | Adapt: replace 7-doc list with thesis equivalent |

### `CLAUDE.md` — Updated Structure (Merged)

**Add to existing CLAUDE.md:**
1. **Navigation section** (new): link to `docs/dev/repository_map.md`, `docs/THESIS_WORKFLOW.md` (if created)
2. **Build/render instructions** (new): `make pdf`, `make check`, `make figures` commands
3. **Integrity gate triggers** (new): conditions under which Gate 1/2/3 must run
4. **Checkpoint definitions** (new): FULL / SLIM / MANDATORY modes (adapted from academic-research-skills)
5. **Known TODOs / frozen decisions** (new): methodological choices Claude must not "fix" (e.g., measurement model choice, sampling strategy, variable operationalization)
6. **Tooling rule summary** (new): 1-line block re: OneDrive + hook

### `.claude/settings.json` (New)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "python \".claude/hooks/check_file_edit.py\"" }]
      }
    ]
  }
}
```

### `.claude/hooks/check_file_edit.py` (New — from PTA)
Block conditions:
- `.py` file + "OneDrive" in path → deny (EEXIST + `\b → \x08` corruption)
- `.env` anywhere → deny (secret leakage)

---

## 7. Phased Master Roadmap

### Step 0: Clone Reference Repos (FIRST — before anything else)
**Effort:** ~10 minutes. Required for reliable LaTeX template + SKILL.md extraction in later phases.

| Task | Notes |
|---|---|
| Clone `Imbad0202/academic-research-skills` locally | Add as VSCode additional working directory for direct reads |
| Clone `K-Dense-AI/scientific-agent-skills` locally | Add as VSCode additional working directory for direct reads |
| Remove both repos after Phase 3 extraction is complete | Temporary local copies only |

---

### Pre-Phase: .claude/ Operating Infrastructure (NOW — Parallel to Phase 1)
**Effort:** ~4–5 hours. Zero risk. Additive only. Begin immediately.

| Task | Source |
|---|---|
| Create `.claude/hooks/check_file_edit.py` | PTA |
| Create `.claude/settings.json` with PreToolUse hook — NEW file, do NOT overwrite `settings.local.json` | PTA |
| Create 8 rule files in `.claude/rules/` | PTA |
| Create 7 skill files in `.claude/skills/` | PTA |
| Create `project_updates/` with standup_draft.md initialized | PTA |
| Create `docs/dev/repository_map.md` (map current repo structure) | PTA |
| Create `docs/tooling-issues.md` (seed with known env issues) | PTA |
| Update CLAUDE.md: add navigation hub structure, frozen decisions | Both |

---

### Phase 1: Architecture Decisions (Week 1 — current week)
**Goal:** Resolve template and tooling decisions before any building.

| Task | Source |
|---|---|
| Confirm CBS thesis formatting requirements (A4, font, margins) | forked-repo |
| Confirm Overleaf sync desired vs. local-only | forked-repo |
| Decide Builder Agent fate (keep or remove) | forked-repo |
| Fetch CBS Overleaf template as formatting reference | forked-repo |
| Write ADR-001 (template), ADR-002 (pipeline), ADR-003 (builder) | forked-repo |

**Deliverables:** `docs/decisions/ADR-001/002/003`
**Risk:** CBS may have formatting requirements not yet extracted from guidelines PDFs

---

### Phase 2: Quick Wins and Low-Risk Cleanup (Week 1–2)
**Goal:** Remove dead weight; establish build skeleton.

| Task | Source |
|---|---|
| Delete `CLAUDE (1).md` | forked-repo |
| Add LaTeX/build artifacts to `.gitignore` | forked-repo |
| Gitignore `.obsidian/workspace.json` | forked-repo |
| Add `build/.gitkeep` directory stub | forked-repo |
| Create `templates/` directory stub | forked-repo |
| Add PATHS dict to `ai_research_framework/config.py` | forked-repo |
| Set up Zotero Better BibTeX auto-export → `bibliography.bib` | forked-repo |
| Add SKILL.md to each agent directory | forked-repo |
| Add Known TODOs section to CLAUDE.md | PTA |

---

### Phase 3: Core Pipeline Build (Week 2–3)
**Goal:** Working Markdown → PDF render chain.

| Task | Source |
|---|---|
| Create `templates/cbs_thesis.cls` (CBS LaTeX template) | forked-repo |
| Create `pandoc/thesis.yaml` (author, title, supervisor, institution) | forked-repo |
| Create `Makefile` with `make pdf`, `make check`, `make figures` | forked-repo |
| Create `pandoc/thesis_build.sh` (concat sections + pandoc invocation) | forked-repo |
| First end-to-end render test (Markdown → PDF) | forked-repo |
| Verify Overleaf sync if desired (manual upload test) | forked-repo |

**Dependencies:** Phase 1 decisions (CBS formatting specs)
**Risk:** Medium — LaTeX template may need iteration for CBS compliance

---

### Phase 4: Integrity Gates and Validation (Week 3–4)
**Goal:** Quality checkpoints adapted from academic-research-skills.

| Task | Source |
|---|---|
| Create `scripts/check_integrity.py` (Gate 1/2/3 logic) | forked-repo |
| Create `thesis/compliance/integrity_checklist.md` (7-mode AI failure) | forked-repo |
| Add `make check` target to Makefile (calls check_integrity.py) | forked-repo |
| Create `scripts/export_notebooklm.py` (batch Markdown → PDF export) | forked-repo |
| Add Gate trigger conditions to CLAUDE.md | forked-repo |
| Add adaptive checkpoints (FULL/SLIM/MANDATORY) to CLAUDE.md | forked-repo |

**Dependencies:** Phase 3 (PDF pipeline must exist to test)
**Risk:** Low — checks are additive; no existing behavior changes

---

### Phase 5: Workflow Hardening (Week 4+ — data-dependent)
**Goal:** Submission-ready workflow.

| Task | Source |
|---|---|
| Modularize `generate_figures.py` (per-figure scripts/functions) | forked-repo |
| Add pre-commit hook or script that runs `make check` on commit | forked-repo |
| Full bibliography validation (49 thesis/literature/papers/ + 24 Obsidian notes vs. bibliography.bib) | forked-repo |
| Final end-to-end test (all 13 sections → PDF) | forked-repo |
| Defense prep NotebookLM export workflow | forked-repo |
| Adapt `/update_all_docs` skill to include integrity_checklist.md | PTA |

---

## 8. Must-Adopt vs. Nice-to-Have vs. Discard

### Must-Adopt (non-negotiable)

| Item | Source | Why |
|---|---|---|
| LaTeX/PDF pipeline (Pandoc + cbs_thesis.cls) | forked-repo | No path to submission without it |
| PreToolUse hook (OneDrive safety) | PTA | Repo IS on OneDrive; file corruption is real |
| CLAUDE.md navigation hub + linked rules | Both | Session startup cost reduction; hallucination prevention |
| `.claude/rules/` + `.claude/skills/` | PTA | Operating model persistence across sessions |
| Standup lifecycle (4-phase) | PTA | Cross-session continuity; supervisor visibility |
| Plan lifecycle (YYYY-MM-DD + Outcome) | PTA | Audit trail for planned vs. executed work |
| 3-gate integrity model | forked-repo | Catches AI errors before advisor review |
| SKILL.md per agent | forked-repo | Agent discovery; self-documenting architecture |
| Zotero Better BibTeX auto-export | forked-repo | Eliminates manual .bib maintenance |
| Tooling-issues registry | PTA | Prevents re-solving known env problems |
| Repository map (docs/dev/repository_map.md) | PTA | Reduces session startup re-exploration |
| Known TODOs / frozen decisions in CLAUDE.md | PTA | Prevents Claude overriding deliberate choices |

### Nice-to-Have (adopt if bandwidth allows)

| Item | Source | Why Valuable but Not Blocking |
|---|---|---|
| Style calibration protocol | forked-repo | Consistent voice across chapters; feed 3 writing samples |
| Lightweight Material Passport (YAML frontmatter) | forked-repo | Provenance tracking per section |
| Lightweight handoff schema validation (Pydantic) | forked-repo | Catches agent output errors early |
| ADR documentation (docs/decisions/) | forked-repo | Preserves architectural rationale |
| scan_skills.py pattern (simplified) | forked-repo | Validates SKILL.md compliance |
| Ordered docs update workflow | PTA | Ensures docs stay in sync |
| Context optimization guide | PTA | Reduces cost; improves output quality |
| Session log (simplified — word counts, chapter progress) | PTA adapted | Performance visibility |
| NotebookLM export scripts | forked-repo | Useful for defense prep, not thesis submission |

### Discard

| Item | Source | Why |
|---|---|---|
| Full 10-stage journal-publication pipeline | forked-repo | Overkill; thesis ≠ journal |
| Semantic Scholar API integration | forked-repo | Coverage gaps; use manual DOI check |
| zh-TW bilingual abstract agents | forked-repo | Not relevant to CBS |
| Max 1 re-revision enforcement | forked-repo | Inflexible for thesis committee |
| Bioinformatics/chemistry/quantum skills | forked-repo | Domain-irrelevant |
| Excel review import loop | PTA | Parser-specific; no equivalent in thesis |
| Win32COM .doc extraction | PTA | Parser-domain |
| CBP API scraper | PTA | Domain-specific |
| MD5 hash cache invalidation | PTA | Only if thesis has expensive recomputable steps (not confirmed) |
| Ruling anomaly registry | PTA | Parser-domain concept |
| `\b` safe patching pattern (beyond the hook) | PTA | Hook handles this; no manual workaround needed |

---

## 9. Key Risks and Mitigations

| Risk | Source | Probability | Impact | Mitigation |
|---|---|---|---|---|
| CBS LaTeX formatting specs unclear | forked-repo | Medium | High | Extract from Thesis Guidelines/ PDFs in Phase 1 before building template |
| Thesis deadline 2026-05-15 conflict with upgrade work | forked-repo | Medium | High | Phase 1–2 must complete by **2026-04-20**; Phase 3+ only if data is flowing |
| Pandoc → LaTeX introduces formatting issues | forked-repo | Low | Medium | Test render early in Phase 3, Week 1, with real content |
| OneDrive file corruption before hook is installed | PTA | Medium (pre-hook) | High | Install PreToolUse hook in Pre-Phase (now), before any code edits |
| Data access delayed beyond 2026-04-30 | forked-repo | High | Critical | System A work is blocked; Pre-Phase + Phase 1–3 are data-independent and should proceed regardless |
| CLAUDE.md scope creep — becomes too large | PTA | Low | Medium | Keep CLAUDE.md as navigation hub only; full specs live in rules files |

---

## 10. Immediate Next Actions (Top 11)

Ordered by impact and unblocked status. Actions 1–5 require no prior decisions.

1. **[FIRST] Clone reference repos to local VSCode workspace** — Clone `academic-research-skills` (Imbad0202) and `scientific-agent-skills` (K-Dense-AI) as additional working directories. Enables direct file reads for LaTeX template extraction and SKILL.md patterns during Phases 2–3 — faster and more reliable than repeated WebFetch calls. Remove after extraction is complete. (~10 min)

2. **[NOW] Install PreToolUse hook** — Create `.claude/hooks/check_file_edit.py` + `.claude/settings.json` (new file, distinct from existing `settings.local.json`). OneDrive path confirmed. Prevents file corruption on every subsequent edit. (~30 min)

3. **[NOW] Bootstrap `.claude/rules/` and `.claude/skills/`** — Copy 8 rule files from PTA source + adapt supervisor name, doc list, path references. (~2–3 hours)

4. **[NOW] Initialize `project_updates/` standup infrastructure** — Create `standup_draft.md`, `standup_draft_archive.md`, `standup_draft_formatting.md`. Start using `/log_standup` from this session forward. (~20 min)

5. **[NOW] Create `docs/dev/repository_map.md`** — Map current CMT_Codebase structure (use 2026-04-13 FileFolderTree as source). Reduces re-exploration cost in every future session. (~45 min)

6. **[Phase 1] Confirm CBS formatting requirements** — Extract precise specs from `Thesis/Thesis Guidelines/` PDFs (or CBS guidelines in `thesis/compliance/`). A4, font, margins, page numbering, frontpage requirements. Unblocks Phase 3 template work.

7. **[Phase 1] Decide Builder Agent fate** — Builder has 6 substantive files (architect, builder_graph, coder, evaluator, executor, experiment_registry). Lean toward KEEP + add SKILL.md. Write ADR-003 to record the decision.

8. **[Phase 2 Quick Win] Delete `CLAUDE (1).md`** — Confirmed stale. (~1 min)

9. **[Phase 2 Quick Win] Update `.gitignore`** — Existing file; add: `build/`, `*.pdf`, `*.aux`, `*.log`, `*.bbl`, `*.blg`, `.obsidian/workspace.json`. (~5 min)

10. **[Phase 2 Quick Win] Set up Zotero Better BibTeX auto-export → `bibliography.bib`** — 49 docs/literature papers + future papers auto-synced. No manual .bib maintenance. (~15 min, external tool)

11. **[Phase 2] Update CLAUDE.md to navigation hub format** — Add navigation section, build instructions, Known TODOs / frozen decisions section, integrity gate trigger conditions. Include `CHEATSHEET.md` in the navigation links. (~1 hour)

---

## Source Plan Cross-Reference

| Section | Primary Source |
|---|---|
| LaTeX/PDF pipeline | zippy-launching-quail.md §6 |
| Integrity gates (3-gate) | zippy-launching-quail.md §6.4 |
| NotebookLM integration | zippy-launching-quail.md §8 |
| SKILL.md pattern | zippy-launching-quail.md §3.2 |
| Zotero integration | zippy-launching-quail.md §5 |
| .claude/ infrastructure | shimmying-gathering-flute.md §3–4 |
| Standup lifecycle | shimmying-gathering-flute.md §5a |
| Plan lifecycle | shimmying-gathering-flute.md §5b |
| PreToolUse hook | shimmying-gathering-flute.md §3b–3c |
| Tooling-issues registry | shimmying-gathering-flute.md §4h |
| Repository map | shimmying-gathering-flute.md §4a |
| Known TODOs pattern | shimmying-gathering-flute.md §4j |
| Context optimization | shimmying-gathering-flute.md §3d |

---

## Outcome

_Completed: 2026-04-13_

### ✅ Completed

**Pre-Phase — .claude/ Operating Infrastructure:**
- Installed PreToolUse hook: `.claude/hooks/check_file_edit.py` + `.claude/settings.json`
- Created 8 rule files in `.claude/rules/`: context-token-optimization, repository-map-reference, tooling-issues-workflow, trigger-standup-workflow, trigger-plan-workflow, trigger-git-commit-workflow, trigger-docs-workflow, one-off-execution
- Created 7 skill files in `.claude/skills/`: log_standup, prep_standup, finalize_standup, init_standup, draft_commit, update_plan, update_all_docs
- Initialized `project_updates/` standup infrastructure: standup_draft.md (Meeting 1), standup_draft_formatting.md, standup_draft_archive.md
- Created `docs/dev/repository_map.md` from 2026-04-13 FileFolderTree
- Created `docs/tooling-issues.md` with 3 seeded issues
- Created `docs/decisions/` with ADR-001/002/003 stubs

**Phase 2 Quick Wins:**
- Deleted `CLAUDE (1).md` (stale duplicate confirmed)
- Updated `.gitignore`: added LaTeX artifacts (build/, *.pdf, *.aux, *.log, etc.) + Obsidian workspace.json
- Updated `CLAUDE.md` to navigation hub format: added navigation section, tooling rule, build commands (stub), integrity gate triggers (stub), Known TODOs / frozen decisions section

### 🔄 Adjusted

- **What**: Step 0 (clone reference repos) not executed
  **Why**: Direct file access to PTA's `.claude/` directory worked without cloning. All source files were read directly from the PTA project.
  **How**: Used PTA `.claude/rules/` and `.claude/skills/` files directly as templates. No external GitHub clone needed.

### ❌ Dropped (deferred to later phases)

- **What**: Phase 1 ADR decisions (ADR-001/002/003 content)
  **Why**: ADRs require CBS formatting spec extraction + user decisions. Stubs created; content pending.

- **What**: Phase 3 LaTeX pipeline (Pandoc, Makefile, cbs_thesis.cls)
  **Why**: Depends on Phase 1 ADR decisions. Not yet unblocked.

- **What**: Phase 4 integrity gates (check_integrity.py, integrity_checklist.md)
  **Why**: Depends on Phase 3 pipeline.

- **What**: SKILL.md per agent directory
  **Why**: Phase 2 task; deferred to next session after ADR-003 is resolved.

- **What**: Zotero Better BibTeX setup
  **Why**: External tool setup requiring user action.

### Notes

- Pre-Phase is complete and additive — zero risk to existing code
- Next session priority: Phase 1 (resolve ADR-001/002/003) → extract CBS specs from Thesis Guidelines/ PDFs
- Supervisor name placeholder used in standup rules — Brian should update `[SUPERVISOR_NAME]` references in `.claude/rules/trigger-standup-workflow.md` when ready
- Python 3.14 noted in tooling-issues.md — watch for package compatibility
