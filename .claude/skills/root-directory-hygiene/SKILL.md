---
name: root-directory-hygiene
description: >
  Repository root and Markdown documentation hygiene auditor.
  Analyzes the repo root against a minimal-root policy and audits
  Markdown files for correct folder placement, filename format,
  and YAML front matter completeness.
  Trigger: /root-directory-hygiene analyze | plan | fix --safe | apply V001,V002
compatibility: any
---

# repo-hygiene

Audit repository root cleanliness and Markdown documentation hygiene. Emits a structured compliance report, proposes a remediation plan, and applies only approved or explicitly safe fixes.

## When to Use

- Root directory has accumulated non-canonical Markdown or asset files
- Documentation files lack YAML front matter, correct naming, or correct folder placement
- Before a handover or major collaboration — confirm docs are discoverable and well-typed
- After a sprint or session — catch docs created in root that should live in `docs/`
- Periodic hygiene check on any project

## Subcommand Interface

```
/root-directory-hygiene analyze              # audit only — no changes
/root-directory-hygiene analyze --scope root # root files only
/root-directory-hygiene analyze --scope docs # markdown files only
/root-directory-hygiene plan                 # audit + full remediation plan
/root-directory-hygiene fix --safe           # apply high-confidence safe fixes only
/root-directory-hygiene apply V003,V007      # apply specific violation IDs
```

Default when no subcommand given: `analyze`.

---

## Workflow

### Step 1 — Discover

Use Glob and Read to gather:
- All files at repo root: `Glob("*")`
- All Markdown files: `Glob("**/*.md")`
- Detect repo type from root contents: Python (`pyproject.toml`), JS/TS (`package.json`), monorepo (`pnpm-workspace.yaml`/`turbo.json`), docs-heavy (`mkdocs.yml`/`docusaurus.config.*`), or plain
- Detect docs tooling: MkDocs, Docusaurus, Sphinx (`conf.py`), or none

### Step 2 — Classify root files

For every file at the repo root, assign one classification using intelligent detection:

**First, check against allowlist** (in `references/root-allowlist.md`):
- **Required**: CLAUDE.md, README.md, INDEX.md, paths.py, requirements.txt, setup.py, pyproject.toml, package.json, etc.
- **Allowed**: When repo actively uses (config files, CI files per conventions)
- **Exception**: Explicitly declared in `.claude/rules/root-documentation-boundary.md`

**Then, apply context-aware heuristics** for unrecognized files:

| Pattern | Heuristic Detection | Classification |
|---------|---|---|
| Filename contains `REFERENCE`, `SUMMARY`, `GUIDE`, `ANALYSIS`, `REPORT`, `AUDIT` | Content-bearing documentation | **Discouraged** → move to `docs/reference/` |
| Filename starts `YYYY_MM_DD-` or `YYYY-MM-DD` | Time-bound doc (plan, handover, note) | **Discouraged** → move to `plans/{status}/P{NNNN}_.../` |
| Filename is `QUICK_REFERENCE*` or similar | Reference material | **Discouraged** → move to `docs/reference/` or `plans/` |
| Extension is `.txt`, `.csv`, `.json` with non-config name | Data or content-bearing artifact | **Discouraged** → classify by content, suggest folder |
| File is uppercase with underscores (`FILE_NAME.ext`) | Likely artifact/generated doc | **Discouraged** → infer type from name, suggest folder |
| Contains no code, no config syntax, human-readable prose | Documentation artifact | **Discouraged** → classify and suggest folder |
| Extension `.md` and not foundational | **Always discouraged** — use ROOT-MD rule |
| Size > 1KB and not config | Likely documentation/artifact | **Discouraged** → suggest folder based on content inference |

| Class | Meaning |
|-------|---------|
| `required` | Must be present (foundational) |
| `allowed` | Permitted when the repo actively uses it (config/CI) |
| `discouraged` | Should move to appropriate folder; emit WARN |
| `forbidden` | Must not be in root; emit HIGH violation |
| `exception` | Explicitly declared in rules — informational only |

**Key insight**: Don't hard-code file formats. Infer intent from filename, size, and content type. If it reads like documentation (prose, not config), it's discouraged.

### Step 3 — Classify all documentation files (any format)

For each file that looks like documentation (regardless of extension), evaluate placement rules:

**Root rules**
- `ROOT-DOC` (HIGH): Any documentation file at root not on allowlist → propose move to correct folder
  - `.md` files → `docs/{architecture,integration,reference,contributing}` or `plans/{status}/P{NNNN}_...`
  - `.txt` reference files → `docs/reference/` or `plans/{status}/P{NNNN}_...`
  - `.json`, `.csv` with semantic name → `docs/reference/` or relevant subfolder
  - Any time-bound doc (contains date) → `plans/{status}/P{NNNN}_YYYY-MM-DD_HHMM_{TYPE}/`
- `ROOT-DUP` (HIGH): multiple README-like or same-topic root docs
- `ROOT-ASSET` (MEDIUM): image/export at root

**Placement rules**
- `DOC-PLACE` (MEDIUM): file in wrong folder for its inferred doc class
  - Use folder taxonomy from `.claude/rules/root-documentation-boundary.md` (routing table)
  - **Plan-related docs**: Always route to `plans/03-outcome_plans/P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}/` or active plan folder
  - **Reference/skill development docs**: Route to `docs/reference/` or plan outcome folder if they document a plan

**Naming rules**
- `DOC-DATE` (MEDIUM): time-bound doc (plan, handover, note, ADR, RFC, postmortem, migration) missing `YYYY_MM_DD-` prefix
- `DOC-NAME` (LOW): evergreen doc not in `kebab-case.md` or `UPPER_CASE.txt`
- `PLAN-DOC-ROUTING` (HIGH): Plan-related supporting docs (reference guides, summaries, analysis) belong in plan outcome folder, not root or generic `docs/` folders

**Metadata rules**
- `DOC-META-ABSENT` (MEDIUM): time-bound doc has no YAML front matter at all
- `DOC-META-FIELDS` (MEDIUM): YAML present but missing required fields (`title`, `type`, `status`, `created`)
- `DOC-META-TYPE` (LOW): `type:` value not in controlled vocabulary
- `DOC-META-STATUS` (LOW): `status:` value not in controlled vocabulary

**Staleness rules**
- `DOC-STALE` (MEDIUM): `status: deprecated` or `status: archived` but not in `docs/archive/`; or dated plan older than 90 days with no active owner

**Formatting rules** (LOW severity, auto-fixable)
- `DOC-FMT-HEADING`: heading levels skipped (e.g. H1 → H3)
- `DOC-FMT-FENCE`: code block missing language tag
- `DOC-FMT-LINK`: absolute internal repo link (should be relative)

**Overlap**
- `DOC-OVERLAP` (MEDIUM): two or more files share the same topic/title — report only, do not auto-fix

---

### Step 3b — Intelligent Routing Logic (Context-Aware Classification)

When a file is detected as documentation (any format), determine its destination **dynamically** based on content and naming:

**Detection Heuristics:**

1. **Plan-related docs** (highest priority):
   - Contains keywords: `PLAN`, `OUTCOME`, `SUMMARY`, `ANALYSIS` + date pattern `YYYY-MM-DD` or `YYYY_MM_DD`
   - Contains P-ID reference (`P0021`, `P0019`, etc.) in name or content
   - Belongs in: `plans/03-outcome_plans/P{NNNN}_YYYY-MM-DD_HHMM_{TYPE}/` or active plan folder
   - **Example**: `EDITED_FILES_SUMMARY.md` (plan outcome support) → `plans/03-outcome_plans/P0021_.../EDITED_FILES_SUMMARY.md`

2. **Skill/rule development docs**:
   - Contains keywords: `REFERENCE`, `SKILL`, `RULE`, `DEVELOPMENT`, `ENFORCEMENT`
   - Associated with a plan outcome (documents that explain how to enforce a structure)
   - Belongs in: Plan outcome folder if tied to a plan; else `docs/reference/`
   - **Example**: `QUICK_REFERENCE_EDITED_FILES.txt` (skill dev reference for P0021) → `plans/03-outcome_plans/P0021_.../QUICK_REFERENCE_EDITED_FILES.txt`

3. **Generic reference/verification docs**:
   - Contains keywords: `VERIFICATION`, `TEST`, `AUDIT`, `REPORT`, `CHECKLIST`, `QUICK-REF`
   - No date pattern, not tied to a plan
   - Belongs in: `docs/reference/`
   - **Example**: `VERIFICATION_REPORT.md` → `docs/reference/VERIFICATION_REPORT.md`

4. **Architecture/design docs**:
   - Contains keywords: `ARCHITECTURE`, `DESIGN`, `PATTERN`, `ADR`, `DECISION`
   - Belongs in: `docs/architecture/`

5. **Setup/integration docs**:
   - Contains keywords: `SETUP`, `INTEGRATION`, `GUIDE`, `HOWTO`, `INSTALL`, `CONFIG`
   - Belongs in: `docs/integration/`

6. **Developer/workflow docs**:
   - Contains keywords: `CONTRIBUTOR`, `GIT`, `WORKFLOW`, `REPOSITORY`, `BRANCH`
   - Belongs in: `docs/contributing/`

**Decision Tree**:
```
Is this a plan-related document?
  YES → Is it about skill/rule enforcement?
    YES → Move to plan outcome folder (e.g., P0021_OUTCOME)
    NO → Move to plan status folder (backlog/in-progress/archive)
  NO → Is it time-bound or historical?
    YES → Move to docs/00_archive/ or plan folder
    NO → Classify by semantic keywords (above)
         → Route to docs/{architecture,integration,reference,contributing}/
```

### Step 4 — Produce structured report

Emit the report using the schema in `references/output-format.md`:

```
Compliance: compliant | conditionally-compliant | non-compliant
Policy variant: default
Summary score: 0–100
Root status: pass | warn | fail
Docs status: pass | warn | fail
Metadata status: pass | warn | fail

Violations:
- [V001] HIGH    | ROOT-MD        | CHANGELOG.md → move to docs/archive/        | confidence: high
- [V002] MEDIUM  | DOC-DATE       | docs/planning/release-plan.md → rename to 2026_04_19-release_plan.md | confidence: high
- [V003] MEDIUM  | DOC-META-ABSENT| docs/guides/zotero-setup.md → insert YAML front matter | confidence: high
- [V004] MEDIUM  | DOC-OVERLAP    | docs/planning/plan-a.md ↔ docs/planning/plan-b.md share topic | confidence: low

Proposed target structure:
  docs/guides/
  docs/planning/
  docs/decisions/
  docs/handover/
  docs/notes/
  docs/reference/
  docs/explanation/
  docs/archive/
  docs/assets/images/

Proposed fix plan:
- [V001] move CHANGELOG.md → docs/archive/CHANGELOG.md; update inbound links
- [V002] rename docs/planning/release-plan.md → docs/planning/2026_04_19-release_plan.md
- [V003] insert YAML front matter block in docs/guides/zotero-setup.md
- [V004] SKIPPED — overlap requires human review

Safety notes:
- V001, V002, V003: auto-fixable (high confidence)
- V004: requires confirmation — not auto-applied
```

### Step 5 — Apply (mode-gated)

| Mode | Behaviour |
|------|-----------|
| `analyze` | Emit report only. No file changes. |
| `plan` | Emit report + full remediation plan. No file changes. |
| `fix --safe` | Apply HIGH-confidence mechanical fixes only. After each move: rewrite relative links in affected files. Re-run audit. Emit post-fix report. Suggest `git stash` before bulk changes. |
| `apply V…` | Apply only the named violation IDs. Same safety protocol as `fix --safe`. |

**Safety invariants (never break these):**
- Prefer move over delete — never delete files
- Never apply `DOC-OVERLAP` fixes automatically
- Never archive or delete without explicit approval
- After any move, update relative internal links in affected files
- Re-run the audit after applying changes and show the post-fix report
- If confidence is medium or low, report and ask — do not apply

---

## YAML Front Matter Schema

Required for all **time-bound** docs (plans, handovers, notes, ADRs, RFCs, postmortems, migration plans):

```yaml
---
title: Clear canonical title
type: guide | decision | handover | plan | reference | note | adr | postmortem | rfc
status: draft | active | deprecated | archived
owner: person-or-team          # recommended
created: YYYY-MM-DD
updated: YYYY-MM-DD            # update whenever content changes
tags:                          # optional
  - topic
supersedes: path-or-id         # optional
superseded_by: path-or-id      # optional
review_by: YYYY-MM-DD          # optional — for time-sensitive docs
---
```

**Evergreen docs** (README, CONTRIBUTING, stable guides, reference pages): YAML front matter is not required. Git history is the authoritative provenance record.

---

## Filename Convention

| Doc class | Format | Example |
|-----------|--------|---------|
| Time-bound (plan, handover, note, ADR, RFC, postmortem, migration) | `YYYY_MM_DD-slug_with_underscores.md` | `2026_04_19-handover_system_b.md` |
| Evergreen (guide, reference, explanation, tutorial) | `kebab-case.md` | `zotero-setup.md` |
| Root special files | Exact conventional name | `README.md`, `CONTRIBUTING.md` |

**Why `YYYY_MM_DD-slug`**: On Windows, double-clicking in a filename selects hyphen-separated tokens. Underscores inside the date block and inside the slug mean one double-click selects the whole date, one selects the whole title — two clean units.

---

## References

- `references/rule-catalog.md` — all rule IDs, severity, confidence, auto-apply status
- `references/root-allowlist.md` — canonical root allowlist/denylist with rationale
- `references/doc-taxonomy.md` — folder taxonomy, type vocabulary, filename rules
- `references/output-format.md` — full structured report schema
- `examples/sample-report.md` — example output from a real analyze run
