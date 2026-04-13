# CMT_Codebase Master Upgrade Plan
## Synthesized from: zippy-launching-quail.md (forked repo analysis) + shimmying-gathering-flute.md (PTA best-practices analysis)

> Source file: `~/.claude/plans/compressed-sniffing-bachman.md` — relocated to project on 2026-04-13

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

[Full plan content is in the global file ~/.claude/plans/compressed-sniffing-bachman.md — kept as reference]

---

## Outcome

_Completed: 2026-04-13_

### ✅ Completed

**Pre-Phase — .claude/ Operating Infrastructure:**
- Installed PreToolUse hook: `.claude/hooks/check_file_edit.py` + `.claude/settings.json`
- Created 8 rule files in `.claude/rules/`: context-token-optimization, repository-map-reference, tooling-issues-workflow, trigger-standup-workflow, trigger-plan-workflow, trigger-git-commit-workflow, trigger-docs-workflow, one-off-execution
- Created 7 skill files in `.claude/skills/`: log_standup, prep_standup, finalize_standup, init_standup, draft_commit, update_plan, update_all_docs
- Initialized `project_updates/` standup infrastructure: standup_draft.md (Meeting 1), standup_draft_formatting.md, standup_draft_archive.md
- Created `dev/repository_map.md` from 2026-04-13 FileFolderTree
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
