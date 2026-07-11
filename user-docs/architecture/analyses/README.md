# Analysis Documents — Thesis Manifold Project

**Location**: `docs/analyses/`  
**Established**: 2026-04-27  
**Purpose**: Central repository for all project analysis documents (migration plans, dependency maps, architectural reviews, etc.)

---

## Naming Convention

All analysis documents use the format:

```
YYYY-MM-DD_HHMM_<analysis_name>.md
```

**Example**: `2026-04-27_1530_ANALYSIS_MIGRATION_PLAN.md`

- **YYYY-MM-DD**: Date the analysis was completed
- **HHMM**: Time the analysis was completed (24-hour format, UTC/local preferred)
- **<analysis_name>**: CamelCase description of what the analysis covers

**Rationale**: Timestamp + filename sorting preserves chronological order and prevents name collisions when multiple analyses cover similar topics.

---

## Documents (Master List)

### Migration Analysis Suite (2026-04-27)

These 5 documents form a complete migration planning suite for moving Enrico's Jupyter notebooks from `docs/thesis/analysis/` to `thesis/analysis/`:

1. **2026-04-27_1530_ANALYSIS_MIGRATION_PLAN.md** (14K)
   - Current state → target structure mapping
   - Path dependencies in each notebook
   - 7-phase migration checklist
   - Risk assessment matrix
   - **Start here for**: Overview + context

2. **2026-04-27_1532_CROSS_REFERENCES_AND_DEPENDENCIES.md** (17K)
   - Master list of all hardcoded paths (by notebook)
   - Which code loads/saves to each path
   - Dependency chain visualization (ASCII)
   - File-by-file migration checklist
   - Risk matrix for each change
   - Fallback logic for safe migration
   - **Start here for**: Detailed path mappings + execution steps

3. **2026-04-27_1533_MIGRATION_EXECUTIVE_SUMMARY.md** (9.4K)
   - Top 3 blocking issues + solutions
   - Migration path (recommended steps 1-6)
   - Execution blockers + unblock plans
   - Critical path to Chapter 7
   - **Start here for**: Quick reference + decision points

4. **2026-04-27_1534_MIGRATION_QUICK_REFERENCE.md** (14K)
   - Copy-paste bash commands
   - Find-and-replace patterns (for each notebook type)
   - Validation checklist
   - Common errors + fixes
   - **Use for**: Hands-on execution (has all the commands)

5. **2026-04-27_1535_NOTEBOOK_STRUCTURE_ANALYSIS.md** (14K)
   - Cell-by-cell breakdown of all 10 notebooks
   - Data flow between notebooks (training → agentic → eval)
   - Phase 5 prompt evolution (v1-v5)
   - Notebook call graph (dependencies)
   - What each notebook does (operational view)
   - **Start here for**: Understanding notebook structure + purpose

---

## How to Use This Convention

When creating new analysis documents:

1. **Complete your analysis** (research, investigation, planning, etc.)
2. **Save to `docs/analyses/`** (do NOT save to `.claude/` or elsewhere)
3. **Use the naming format**: `YYYY-MM-DD_HHMM_<DescriptiveName>.md`
4. **Update this README** with a 1-line entry under the appropriate section
5. **Commit to git** with message: `docs: add analysis — <brief description>`

**Example commit**:
```
docs: add analysis — Prometheus integration architecture

- docs/analyses/2026-04-27_1600_PROMETHEUS_INTEGRATION_ARCHITECTURE.md
- Maps model serving patterns + monitoring strategy
- Identifies L4 tier requirements + fallback logic
```

---

## Organizational Tiers (Optional Subdirectories)

If this grows beyond ~10 documents, consider organizing by topic:

```
docs/analyses/
├── migration/
│   ├── 2026-04-27_1530_ANALYSIS_MIGRATION_PLAN.md
│   ├── 2026-04-27_1532_CROSS_REFERENCES_AND_DEPENDENCIES.md
│   └── ...
├── architecture/
│   ├── 2026-04-27_1600_PROMETHEUS_INTEGRATION.md
│   └── ...
└── README.md
```

**Decision**: Keep flat (current) until >15 documents, then subdivide.

---

## Archive Policy

- **Active documents**: Live in `docs/analyses/`
- **Superseded documents**: Mark with `[SUPERSEDED]` in filename if substantially replaced
  - Example: `[SUPERSEDED]2026-04-27_1530_ANALYSIS_MIGRATION_PLAN.md`
  - This keeps historical record without cluttering the active list
- **Cleanup**: Remove `[SUPERSEDED]` tags annually unless historical reference is needed

---

## Cross-References

- **Thesis root project guide**: [CLAUDE.md](../../CLAUDE.md)
- **Repository file map**: [docs/dev/repository_map.md](../dev/repository_map.md)
- **Project context**: [docs/project-management/context.md](../project-management/context.md)
- **Architecture decisions**: [docs/codebase/architecture.md](../codebase/architecture.md)

---

## Questions?

If you need to refer to or cite these analyses:
- **Link format**: `[Title](docs/analyses/YYYY-MM-DD_HHMM_filename.md)`
- **In git commits**: Reference the date-time to avoid confusion with similarly-named documents
- **In conversation**: Use the 1-line description from this README

**Last Updated**: 2026-04-27 16:00 UTC
