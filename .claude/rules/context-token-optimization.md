# Context & Token Optimization Guide

## Overview

This guide documents strategies for optimizing context window and token consumption in Claude Code sessions for `CMT_Codebase`. Apply these patterns to reduce cost, improve response latency, and maintain clarity across multi-session thesis work.

---

## 1. Model Tier Selection Strategy

| Model | Best For | Use In This Project |
|-------|----------|-------------------|
| **Haiku 4.5** | Quick edits, single-file changes, exploration | Standup logging, minor doc updates |
| **Sonnet 4.6** | Multi-file implementation, cross-module changes | Standard development, chapter editing, agent work |
| **Opus 4.6** | Complex architecture, deep reasoning, literature analysis | Architecture decisions, literature review, ADRs, integrity gate design |

**Rule**: Use Sonnet by default. Escalate to Opus for:
- Architecture decisions (ADR-001/002/003)
- Literature synthesis and gap analysis
- Complex pipeline design (Pandoc, LaTeX template)
- Integrity gate logic design

---

## 2. Tool Optimization

### Preferred Tool Stack (Cost Order)

1. **Bash** — File inspection, git operations, make commands
2. **Read** — File content (not `cat`)
3. **Grep** — Pattern search (not `rg` in Bash)
4. **Glob** — File discovery (not `find`/`ls`)
5. **Edit** → **Write** — Avoid Edit/Write on `.py` files on this OneDrive path (hook blocks these); use temp-script pattern instead

---

## 3. Context Management: When to Compact

Use **Strategic Compact** after reaching context milestones:

| Transition | Compact? | Reason |
|-----------|----------|---------|
| Exploration → Planning | **Yes** | Research context is bulky; plan is distilled and saved |
| Planning → Implementation | **Yes** | Plan survives; frees context for writing |
| Implementation → Testing/Validation | **Maybe** | Keep if tests reference recent code |
| Debugging → Next chapter | **Yes** | Debug traces pollute new work |
| Mid-implementation | **No** | Losing context costly mid-flow |

**Survives Compaction**:
- `CLAUDE.md` instructions
- `.claude/rules/` files (all workflows)
- Memory files (`~/.claude/memory/`)
- Git state and files on disk
- TodoWrite task list

**Lost**:
- Conversation history
- Previously read file contents
- Intermediate reasoning

---

## 4. Session Start / End Checklist

**Session start:**
- [ ] Read `CLAUDE.md` → `dev/repository_map.md` → `docs/tooling-issues.md`
- [ ] Check current thesis phase and blocked tasks
- [ ] Identify PRIMARY tasks (thesis writing deliverables) vs SECONDARY (infrastructure)

**Session end:**
- [ ] Run `/log_standup` if any writing or code changes were made
- [ ] Mark tasks complete in TodoWrite
- [ ] Commit if meaningful changes were made (`/draft_commit`)

---

## 5. Context Consumption Hotspots

| Component | Risk | Mitigation |
|-----------|------|------------|
| Literature review (49 papers) | Very high | Read summaries only; never load all papers at once |
| Thesis chapter sections (13 files) | High | Load 1-2 sections at a time |
| `.claude/rules/` | Low | Auto-loaded; manageable size |
| `CLAUDE.md` | Medium | Keep as navigation hub only; don't bloat |
| System A/B agent files | Medium | Load per-agent, not the whole system |

---

## 6. Adaptive Checkpoints (FULL / SLIM / MANDATORY)

| Mode | When | What Claude does |
|------|------|-----------------|
| **FULL** | First session after data changes | Read all relevant docs, verify integrity gates |
| **SLIM** | Standard writing/coding sessions | Load CLAUDE.md + repository_map + active section only |
| **MANDATORY** | Before any thesis submission prep | Run full integrity check (`make check`), verify all 49 citations |

---

## 7. Duplicate Instruction Detection

Periodically audit for waste:
- `CLAUDE.md` should reference `.claude/rules/` files (not repeat them)
- Each `.claude/rules/*.md` file should have one purpose (no overlap)
- Skills should not duplicate CLAUDE.md instructions

**Why**: Saves ~500-1K tokens per session.
