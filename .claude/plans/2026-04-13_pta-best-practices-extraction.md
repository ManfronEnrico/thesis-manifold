# pta-cbp-parser: Claude Code Best-Practices Extraction & Transferability Assessment

_Standalone analysis. Separate from thesis-repository comparison task._

---

## Context

**Purpose**: Audit the `pta-cbp-parser` project to extract Claude Code operational patterns, explicit rules, and implicit conventions that are worth reusing in a different project context — specifically a thesis-writing repository.

**Scope**: Analysis and recommendation only. No changes to either repository in this run.

**Target project**: `C:\Users\brian\OneDrive\Documents\01 - P - Projects and Tasks\2026-01-03 - Preferential Trade Project\pta-cbp-parser`

---

## 1. Executive Summary

The `pta-cbp-parser` project is a production-grade Claude Code operating environment. It has evolved, through real use, into a system that solves four concrete problems:

1. **Tool safety**: OneDrive + Windows breaks standard Edit/Write tools in ways Claude cannot self-detect. A PreToolUse hook enforces a safe patching pattern.
2. **Context continuity**: Multi-session work needs persistent session logs, carry-over task tracking, and structured progress visibility. The standup workflow solves this.
3. **Execution clarity**: Complex multi-phase pipelines need documented workflows so Claude can reconstruct intent without re-exploring code. Rules files and architecture docs solve this.
4. **Output quality**: Reproducing runs, validating extractions, and managing review cycles require explicit mechanisms — seeds, cache invalidation hashes, benchmark specs, triage reports.

Most of these patterns are **domain-agnostic**. The standup lifecycle, plan workflow, commit generation, tooling-issue registry, and context optimization strategies transfer directly or with trivial adaptation to any long-running project.

**Highest-value takeaways for thesis**: standup workflow system, plan lifecycle (YYYY-MM-DD naming + outcome sections), tooling-issue registry, and the CLAUDE.md-as-navigation-hub pattern.

---

## 2. Repository Structure and Operating Model

### High-Level Architecture

```
pta-cbp-parser/
├── .claude/                    ← Claude Code operating environment
│   ├── hooks/                  ← PreToolUse enforcement (safety)
│   ├── rules/                  ← Auto-loaded workflow rules (11 files)
│   ├── skills/                 ← Custom slash commands (8 skills)
│   ├── plans/                  ← Dated plan files with outcome sections
│   └── settings.json           ← Hook registration
├── CLAUDE.md                   ← Primary Claude guide (navigation hub)
├── docs/                       ← Human + Claude reference documentation
│   ├── tooling-issues.md       ← Living registry of solved environment issues
│   ├── WORKFLOW_AND_LOGGING.md ← Full architecture reference
│   ├── FILTERING_AND_SAMPLING.md
│   ├── COMMAND_CHEATSHEET.md
│   └── CHEATSHEET.md
├── dev/
│   └── repository_map.md       ← Quick file-to-purpose map
├── project_updates/            ← Standup drafts and meeting minutes
│   ├── standup_draft.md        ← Live session log (never deleted mid-cycle)
│   ├── standup_draft_archive.md
│   └── standup_draft_formatting.md
├── pipeline/                   ← Phase-based orchestration (~4 phases)
├── jurisdiction_modules/       ← Domain logic (regex, LLM, schema)
├── shared_modules/             ← Cross-cutting utilities
├── input_data/                 ← Source data + benchmarks
├── cache_data/                 ← Downloaded documents (gitignored)
└── output_data/                ← Generated outputs (gitignored)
```

### Operating Model

The project operates as a **phased pipeline** with reproducible execution. Claude is expected to:
- Navigate via `CLAUDE.md` → `repository_map.md` → `WORKFLOW_AND_LOGGING.md`
- Follow `.claude/rules/` without re-learning them each session
- Use `.claude/skills/` for recurring actions (standup, commit, docs update)
- Reference `docs/tooling-issues.md` before any plan to avoid re-solving known problems
- Log all session work into `standup_draft.md` (auto-trigger at session end)
- Track plan execution with outcome sections in `.claude/plans/`

---

## 3. Explicit Claude Rules / Instruction Artifacts

### 3a. CLAUDE.md — Navigation Hub

**File**: `CLAUDE.md` (root)

**Role**: Session entry point. Does NOT contain full workflow details — it links to them. Organized as:
- Quick navigation (repository_map, WORKFLOW docs)
- Tooling rule summary + 1-line rule
- Run commands (all CLI flags)
- Directory map (annotated file tree)
- Key conventions (document text format, caching, benchmark schema)
- Known TODOs (frozen decisions)
- Testing checklist (syntax, corruption, benchmark, smoke tests)

**Key design principle**: CLAUDE.md is a **navigation hub and constraint list**, not a full specification. Workflows live in `.claude/rules/`. This prevents the file from becoming a context bloat source while still ensuring Claude finds what it needs.

### 3b. `.claude/settings.json` — Hook Registration

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

Runs on every Edit/Write tool call. Blocks `.py` files on OneDrive paths and `.env` files anywhere. Returns `permissionDecision: "deny"` with instructions to use the safe patching pattern.

### 3c. `.claude/hooks/check_file_edit.py` — Safety Enforcer

Reads `tool_input.file_path` from stdin JSON. Two block conditions:
- `.py` + "OneDrive" in path → block (EEXIST + `\b` → `\x08` corruption risk)
- `.env` anywhere → block (secret leakage)

Returns structured deny output with the safe pattern inline. Enforces a convention Claude cannot override by "trying anyway."

### 3d. `.claude/rules/` — 11 Auto-Loaded Rule Files

| File | Auto-loads? | Purpose |
|------|------------|---------|
| `context-token-optimization.md` | Yes | Model tier selection, tool cost order, compaction timing, session start/end checklist |
| `repository-map-reference.md` | Yes | Navigation triggers → repository_map.md |
| `tooling-issues-workflow.md` | Yes | Mandatory pre-task read of tooling-issues.md; update on trigger phrases |
| `trigger-standup-workflow.md` | Yes (path: `project_updates/`) | Full standup lifecycle: log/prep/finalize/init |
| `trigger-plan-workflow.md` | Yes (path: `**`) | Plan file location, naming convention, outcome format |
| `trigger-git-commit-workflow.md` | Yes (path: `**`) | Commit message generation algorithm |
| `trigger-docs-workflow.md` | Yes (path: `**`) | Ordered docs update workflow |
| `field-review-annotations-workflow.md` | Yes (path: `field_review_annotations.jsonl`) | Annotation JSONL schema |
| `ruling-id-loading.md` | Yes | ID source priority chain, 6 filters |
| `testing.md` | Yes | Benchmark test scripts (N340865, N271081) |
| `one-off-execution.md` | Yes | Default non-recurring trigger semantics |

### 3e. `.claude/skills/` — 8 Custom Commands

| Skill | Trigger | What it does |
|-------|---------|-------------|
| `log_standup` | `/log_standup` | Appends session entry to standup draft with date > priority > time hierarchy |
| `prep_standup` | `/prep_standup` | Creates supervisor meeting file; strips meta-notes |
| `finalize_standup` | `/finalize_standup` | Finalizes meeting file + writes to archive |
| `init_standup` | `/init_standup` | Initializes next draft; carries over unchecked tasks |
| `draft_commit` | `/draft_commit` | Generates commit message from session context + standup + git log |
| `update_plan` | `/update_plan [name]` | Appends Outcome section to plan file; relocates/renames if needed |
| `update_all_docs` | `/update_all_docs` | Runs ordered docs update across 7 document types |
| `commit` | `/commit` | Wrapper for commit workflow |

---

## 4. Implicit Claude-Friendly Patterns

Patterns not labeled as Claude-specific but that significantly improve Claude's effectiveness.

### 4a. Repository Map as a Separate File

`dev/repository_map.md` is a dedicated file mapping every module to its purpose, line count, and role in the pipeline. This keeps CLAUDE.md shorter and lets Claude quickly orientate in a new session without re-reading source files.

### 4b. Dated, Phase-Named Output Directories

```
output_data/ny/
├── ruling-doc-fetch/
├── ruling-parse-regex/
├── ruling-parse-llm/
├── report-parsing_triage/
├── report-excel_review/
└── logs/
```

Each directory name encodes the pipeline phase. Claude can infer which output belongs to which phase without reading code.

### 4c. Phase-Based Module Decomposition

`pipeline/` separates orchestration from logic:
- `phase0_id_loading.py` (~130 lines)
- `phase1_doc_fetch.py` (~110 lines)
- `phase2_extraction.py` (~350 lines)
- `phase_reporting.py` (~200 lines)

No phase file exceeds 400 lines. This keeps each file within a single-read context window and avoids the need for Claude to hold the full pipeline in memory.

### 4d. Cache-Aware Parser Invalidation

The parse cache first line contains an MD5 hash of parser source files. On load, if the hash mismatches, the cache is discarded. Claude does not need to remember "I changed the parser" — the mechanism auto-detects staleness.

### 4e. Benchmark Spec as Configuration

`benchmark_spec.json` contains `field_order` and `disabled_fields`. This means enabling/disabling a field requires editing one file, not tracing where the field appears in 10 modules. The architecture reduces diff scope for Claude.

### 4f. Seed-Based Sampling with Explicit CLI Flags

`--sample N --seed 42` is consistently documented in CLAUDE.md, COMMAND_CHEATSHEET.md, and the rules file. Claude can reproduce any sampling run by repeating the exact command without understanding the implementation.

### 4g. `.env.example` as Contract

`.env.example` documents the required environment variables without exposing secrets. Combined with the `.env` write-block hook, this creates a clean separation: humans manage secrets, Claude manages code.

### 4h. `docs/tooling-issues.md` as a Living Issue Registry

Eight numbered issues with Symptom / Cause / Solution / Key lesson structure. This functions like a project-specific error log that Claude reads before any plan. Prevents re-diagnosing known problems.

### 4i. `project_updates/` as Session Memory

`standup_draft.md`, `standup_draft_archive.md`, and meeting files provide a complete, human-readable history of what was done, when, and for what purpose. Claude can reconstruct prior session context without a long conversation history.

### 4j. Known TODOs Section in CLAUDE.md

A dedicated section listing deliberate limitations and frozen decisions (disabled field, known miss rates, schema version changes). This prevents Claude from "fixing" something that was intentionally left as-is.

### 4k. Plan Files with Outcome Sections

All plans follow `YYYY-MM-DD_<short-slug>.md` naming and include an `## Outcome` section after execution (✅/🔄/❌ format). Plans stay in `.claude/plans/` (project-local) never global. This creates a dated audit trail of what was planned vs. what actually happened.

---

## 5. Workflow / Trigger / Automation Analysis

### 5a. Standup Lifecycle (4-phase)

```
/log_standup → /prep_standup → /finalize_standup → /init_standup
```

- **log_standup**: Session-level entry; auto-triggers at session end when code changes were made
- **prep_standup**: Pre-meeting; strips meta-notes; creates supervisor copy
- **finalize_standup**: Post-meeting; overwrites meeting file with edited version; archives draft
- **init_standup**: Resets draft for next cycle; carries over unchecked tasks; starts fresh Progress Log

**Design insight**: The standup system separates the *live draft* (working doc, includes meta-notes) from the *supervisor copy* (clean, human-facing). Claude manages the transition between them.

### 5b. Plan Workflow (3-step)

1. Create plan (via EnterPlanMode) in `~/.claude/plans/` or `.claude/plans/`
2. Execute plan
3. `/update_plan` → relocate to project folder + rename to slug + append Outcome

The relocate+rename step prevents plans from accumulating in the global folder with random names.

### 5c. Git Commit Workflow (5-step deduction)

```
Session context → git status → git log -1 → standup Progress Log → cross-reference → draft message
```

The commit algorithm explicitly handles multi-session scenarios: standup entries timestamped after the last commit are included even if they're from a different Claude session. This is a mature, edge-case-aware design.

### 5d. Docs Update Workflow (ordered)

The `/update_all_docs` skill enforces a fixed update order:
1. standup_draft → 2. architecture docs → 3. tooling-issues → 4. CLAUDE.md → 5. README → 6. plan files → 7. rules files

This order matters: later documents may reference information that earlier documents must first establish.

### 5e. Mandatory Pre-Task Tooling Check

Before any plan, Claude must read `docs/tooling-issues.md`. This is documented in the rule file AND referenced in CLAUDE.md. Double-documentation of a critical guardrail.

### 5f. One-Off Execution Default

`one-off-execution.md` explicitly states that trigger phrases execute once by default. This prevents Claude from setting up recurring automations when a one-time action was requested.

---

## 6. Validation and Quality-Control Mechanisms

### 6a. Three-Level Testing Protocol

From CLAUDE.md Testing Checklist:
1. **Syntax check**: `python -m py_compile`
2. **Corruption check**: Count `\x08` bytes (must be 0)
3. **Benchmark test**: N340865 (32/32 fields) + N271081 spot-check
4. **Modularization test**: Import validation + 4 smoke-test commands
5. **Full pipeline**: `--single-classification` on 190 rulings

Each level catches a different failure mode. The corruption check specifically targets the `\b→\x08` encoding bug that is invisible in text editors.

### 6b. Parsing Triage / QA

`shared_modules/parsing_triage.py` compares:
- Regex output vs. benchmark (ground truth)
- LLM output vs. benchmark
- Regex vs. LLM (disagreement signal)

Produces a structured report that Claude or a human can read to identify where extraction is failing.

### 6c. MD5 Hash-Based Cache Invalidation

Parser source files are hashed. Cache is auto-discarded on hash mismatch. Removes a class of stale-cache bugs.

### 6d. Anomaly Registry

`input_data/ny/ruling_anomalies.jsonl` is a persistent registry of known-bad rulings (duplicates, malformed content, special cases). This prevents Claude from repeatedly investigating the same anomalies.

### 6e. Excel Review Import Loop

`--import-review` reads manual corrections from an Excel file and writes them back to `benchmark_values.json` and `field_review_annotations.jsonl`. This creates a human-in-the-loop QA mechanism where domain expert corrections feed back into the benchmark.

### 6f. Session Performance Log

`output_data/{jurisdiction}/logs/log-session-per_run.jsonl` tracks every run with timing, cache hit rates, token counts, and costs. Claude can reference this log to understand system behavior across runs.

---

## 7. Transferability Assessment

### Domain-Specific (Keep in Parser Project)

| Pattern | Why Domain-Specific |
|---------|-------------------|
| Tiered document fetcher (JSON API / HTML / .doc) | CBP-specific; specific to ruling doc format |
| Win32COM `.doc` extraction | Windows+Word dependency; parser-domain constraint |
| Regex + LLM field extraction | CBP ruling letter format |
| Benchmark spec (32 fields) | Parser-domain ground truth |
| JSONL ruling ID scraper | CBP API-specific |
| Parsing triage report | Parser-domain QA |
| `--single-classification` filter | Ruling-domain semantics |

### Domain-Agnostic (Transfer Directly)

| Pattern | Transfer to Thesis |
|---------|-------------------|
| CLAUDE.md as navigation hub with linked rules | Yes — any complex project |
| `.claude/rules/` for auto-loaded workflows | Yes — any project |
| `.claude/skills/` for custom slash commands | Yes — any project |
| PreToolUse hook for safety | Conditional — only if same OneDrive path issues apply |
| Standup workflow (log/prep/finalize/init) | Yes — any project with periodic check-ins |
| Plan lifecycle (YYYY-MM-DD naming + outcome) | Yes — any planned work |
| Git commit deduction workflow | Yes — any git project |
| Docs update workflow (ordered) | Yes — any documented project |
| Tooling-issues registry | Yes — any project with env issues |
| Repository map as separate file | Yes — any large project |
| One-off execution default | Yes — any Claude project |
| Context optimization guide (model tier, compact timing) | Yes — any Claude project |
| Known TODOs section in CLAUDE.md | Yes — any project with deliberate limitations |
| Seed-based reproducible sampling | If thesis has quantitative sampling |
| Phase-based module decomposition (≤400 lines) | Yes — any multi-step pipeline |

### Reusable With Adaptation

| Pattern | Adaptation Needed |
|---------|-----------------|
| Standup workflow | Rename "Sebastian" → thesis supervisor; adjust sections for academic context |
| `project_updates/` directory | Adapt section headings (PRIMARY/SECONDARY) to thesis phases |
| Benchmark spec as config | Reframe as "analysis spec" or "chapter checklist" |
| Cache invalidation hash | Only relevant if thesis has computationally expensive steps |
| Excel review import loop | Only relevant if thesis uses spreadsheet-based review |
| Performance log (timing, tokens, cost) | Simplify to track word counts, session counts, chapter progress |

---

## 8. Recommended Reusable Patterns

### Full Transferability Table

| Pattern | Source Location | Type | Purpose | Transferability | Adaptation Effort | Risk | Recommendation |
|---------|----------------|------|---------|----------------|------------------|------|----------------|
| CLAUDE.md as navigation hub | `CLAUDE.md` | Explicit Claude rule | Session entry point; links to rules, not duplicates them | High | Low | Low | **Adopt directly** |
| Auto-loaded `.claude/rules/` | `.claude/rules/*.md` | Explicit Claude rule | Persistent workflow rules across sessions | High | Low | Low | **Adopt directly** |
| Custom `.claude/skills/` | `.claude/skills/*.md` | Explicit Claude rule | Slash commands for recurring tasks | High | Low | Low | **Adopt directly** |
| Standup lifecycle (4-phase) | `trigger-standup-workflow.md` + 4 skills | Automation mechanism | Session continuity, supervisor visibility | High | Medium | Low | **Adapt — rename supervisor, adjust sections** |
| Plan lifecycle (YYYY-MM-DD + Outcome) | `trigger-plan-workflow.md` | Automation mechanism | Durable planning + execution record | High | Low | Low | **Adopt directly** |
| Git commit deduction workflow | `trigger-git-commit-workflow.md` | Automation mechanism | Accurate commit messages across sessions | High | Low | Low | **Adopt directly** |
| Docs update ordered workflow | `trigger-docs-workflow.md` | Automation mechanism | Consistent documentation maintenance | High | Low | Low | **Adopt directly** |
| Tooling-issues registry | `docs/tooling-issues.md` + rule | Human process + automation | Prevent re-solving known env problems | High | Low | Low | **Adopt directly** |
| Repository map as separate file | `dev/repository_map.md` | Implicit convention | Reduces session startup cost | High | Low | Low | **Adopt directly** |
| One-off execution default | `one-off-execution.md` | Explicit Claude rule | Prevents unintended automation | High | Low | Low | **Adopt directly** |
| Context optimization guide | `context-token-optimization.md` | Explicit Claude rule | Cost + quality management | High | Low | Low | **Adopt directly** |
| Known TODOs section in CLAUDE.md | `CLAUDE.md` | Implicit convention | Prevents Claude from "fixing" frozen decisions | High | Low | Low | **Adopt directly** |
| PreToolUse hook (OneDrive safety) | `settings.json` + `check_file_edit.py` | Automation mechanism | Prevents file corruption | Medium | Medium | Low | **Adopt if OneDrive path applies** |
| Phase-based module decomposition | `pipeline/*.py` | Implicit convention | Keeps files within single-read context | High | Medium | Low | **Adopt as convention** |
| `project_updates/` session memory | `project_updates/` directory | Human process | Cross-session continuity | High | Medium | Low | **Adapt — different section headings** |
| Seed-based reproducible execution | CLI flags + docs | Implicit convention | Reproducibility | Conditional | Medium | Low | **Adopt if thesis has analysis runs** |
| Benchmark spec as configuration | `benchmark_spec.json` | Implicit convention | Single-file feature enable/disable | Conditional | Medium | Low | **Adapt as chapter/section config** |

---

## 9. Patterns to Avoid Reusing

| Pattern | Reason to Skip |
|---------|---------------|
| `--import-review` Excel loop | Parser-specific; thesis review cycle is different |
| Win32COM `.doc` extraction | Windows+Word dependency; not applicable to thesis |
| CBP API scraper | Domain-specific tool |
| Parsing triage (regex vs. LLM) | Parser-domain QA; thesis doesn't extract structured fields from rulings |
| Tiered document fetcher | CBP-specific fetch logic |
| `\b` corruption workaround (safe patching) | Only needed on this OneDrive+Windows path; if thesis repo is in a different path it may not apply |
| Ruling anomaly registry | Parser-domain concept |
| MD5 hash cache invalidation | Only valuable if thesis has expensive recomputable steps (e.g. model runs) |
| `YEAR_CANDIDATES` fallback loop | CBP-specific URL structure |

**General principle**: Any pattern tied to the CBP ruling document format, the CBP API, or ruling-specific data structures should not transfer. Patterns tied to *how Claude operates over multiple sessions* should.

---

## 10. Standalone Adaptation Roadmap for Future Use

This section describes how to port the best patterns into a thesis-writing repository in a future follow-up run. Do not execute now.

### Step 1 — Bootstrap the `.claude/` Infrastructure (30 min)

1. Create `.claude/` directory at thesis repo root
2. Create `.claude/rules/` (empty, to be populated)
3. Create `.claude/skills/` (empty, to be populated)
4. Create `.claude/plans/` (for plan files)
5. Create `.claude/settings.json` with the PreToolUse hook if the repo is on an OneDrive path

### Step 2 — Write CLAUDE.md for the Thesis Project (1–2 hours)

Adapt the CLAUDE.md structure:
- **Navigation section**: link to a `dev/repository_map.md` (to be created) and a `docs/THESIS_WORKFLOW.md`
- **Key conventions**: chapter naming, citation format, output structure, analysis scripts
- **Run commands**: any Python analysis scripts or build commands
- **Known frozen decisions**: deliberate methodological choices Claude should not second-guess
- **Testing checklist**: linting, reference checking, word count validation

### Step 3 — Port Domain-Agnostic Rules (2–3 hours)

Copy and adapt these rule files (rename references and adjust project-specific details):

| Parser Rule | Thesis Equivalent |
|-------------|-----------------|
| `trigger-standup-workflow.md` | Adapt: rename "Sebastian" → supervisor name; adjust PRIMARY/SECONDARY labels to thesis phases (e.g., writing vs. analysis) |
| `trigger-plan-workflow.md` | Copy directly — plan lifecycle is identical |
| `trigger-git-commit-workflow.md` | Copy directly — commit workflow is identical |
| `trigger-docs-workflow.md` | Adapt: replace doc list with thesis docs (thesis chapters, methodology notes, CLAUDE.md, README) |
| `tooling-issues-workflow.md` | Copy directly — env issue registry applies anywhere |
| `context-token-optimization.md` | Copy directly — model tier strategy is universal |
| `one-off-execution.md` | Copy directly |
| `repository-map-reference.md` | Adapt: reference thesis `dev/repository_map.md` |

### Step 4 — Port and Adapt Skills (1–2 hours)

Copy these skill files and adapt project-specific references:

| Skill | Adaptation |
|-------|-----------|
| `log_standup.md` | Update file path to `project_updates/standup_draft.md`; adjust section names |
| `prep_standup.md` | Adapt supervisor name; adjust what gets stripped as meta-notes |
| `finalize_standup.md` | Copy structure; update file naming pattern |
| `init_standup.md` | Copy structure; update carry-over rules for thesis context |
| `draft_commit.md` | Copy directly |
| `update_plan.md` | Copy directly |
| `update_all_docs.md` | Adapt doc update order for thesis documents |

### Step 5 — Create Supporting Infrastructure (1 hour)

1. **`project_updates/`** directory with:
   - `standup_draft.md` (initialized with thesis supervisor name and meeting schedule)
   - `standup_draft_formatting.md` (gold-standard template; never overwritten by skills)
   - `standup_draft_archive.md` (empty initially)

2. **`docs/tooling-issues.md`** — start with any known env issues

3. **`dev/repository_map.md`** — map thesis repo structure (chapters, scripts, data, output)

### Step 6 — Validate (30 min)

Test that:
- CLAUDE.md links resolve correctly
- Rules files auto-load (test by opening a session and asking about a trigger phrase)
- Skills invoke correctly (`/log_standup`, `/update_plan`, `/draft_commit`)
- Hook (if installed) correctly blocks on target paths

### Prioritization

If time is short, implement in this order:
1. CLAUDE.md (navigation hub) — highest ROI per minute
2. `.claude/rules/trigger-standup-workflow.md` + 4 standup skills — highest operational value
3. `.claude/rules/trigger-plan-workflow.md` — essential for structured work
4. `docs/tooling-issues.md` — prevents repeated env debugging
5. `dev/repository_map.md` — reduces session startup cost
6. Git commit workflow — valuable once work accumulates
7. Docs update workflow — valuable once docs become complex

---

## 11. Open Questions / Uncertainties

| Question | Impact | How to Resolve |
|----------|--------|---------------|
| Does the thesis repo live on an OneDrive path? | Determines whether PreToolUse hook is needed | Check file path |
| Does the thesis project have a regular supervisor meeting cycle? | Determines standup workflow cadence | Clarify with user |
| What document types will the thesis project have? | Determines which docs go in the update_all_docs workflow | Map thesis repo structure |
| Are there computationally expensive steps in the thesis (model runs, data processing)? | Determines whether cache invalidation + reproducible seeds are worth porting | Clarify scope of analysis scripts |
| Is the thesis project a solo repo or collaborative? | Affects commit workflow design | Clarify |
| What does "PRIMARY" vs "SECONDARY" mean in a thesis context? | Determines standup priority labeling | Map to: writing deliverables vs. infrastructure/tooling |
| Should plan files in the thesis project also follow YYYY-MM-DD naming? | Consistency decision | Recommend: yes, keep the same convention |

---

## Prioritized Shortlist — Highest-Value Reusable Practices

In rank order (value / adaptation effort ratio):

1. **CLAUDE.md as navigation hub with linked rules** — reduces session startup cost, prevents context bloat. 1 hour to create. Immediate.

2. **Standup lifecycle (4 skills: log/prep/finalize/init)** — provides cross-session continuity, supervisor visibility, and carry-over task tracking. 2–3 hours. Highest operational value.

3. **Plan lifecycle (YYYY-MM-DD naming + Outcome sections)** — creates a durable audit trail of planned vs. executed work. 30 minutes. Copy-paste with minor renames.

4. **`docs/tooling-issues.md` + mandatory pre-task read** — prevents spending time re-solving known environment problems. 30 minutes to bootstrap. Immediate value.

5. **`dev/repository_map.md`** — fast orientation in new sessions. 30–60 minutes to write. Reduces re-exploration.

6. **Git commit deduction workflow** — generates accurate commit messages even across multi-session work. 15 minutes to port. Adopt directly.

7. **Context optimization guide (model tier, compaction timing)** — reduces cost and improves quality of Claude outputs. 15 minutes to port. Adopt directly.

8. **One-off execution default** — prevents accidental automations. 5 minutes. Copy directly.

9. **Known TODOs / frozen decisions in CLAUDE.md** — prevents Claude from undoing deliberate choices. 20 minutes to populate. Essential discipline.

10. **Ordered docs update workflow (`/update_all_docs`)** — maintains documentation consistency as the project evolves. 1 hour to adapt. High value for thesis.
