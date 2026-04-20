---
name: Zotero Integration Recommendation
description: Phase-based approach to integrate Zotero reference management with thesis literature corpus
type: project
---

## Decision: Zotero Integration via Pyzotero

**Status**: ✅ PHASE 1 COMPLETE — Group library discovered & configured  
**Recommendation**: Phase approach (start with read-only sync in Phase 1)

### Current State
- 48 confirmed papers in `/docs/literature/papers/*.md` with YAML metadata
- Group library "CMT - CBS Master Thesis" (ID: 6479832) has 39 items, 11 papers
- Literature managed via Markdown + Zotero group library + NotebookLM ingestion manifest
- Manual PDF organization in `/papers/` subfolders by chapter
- System B Literature Agent handles scraping, confirmation, gap analysis

### Zotero Configuration (DISCOVERED 2026-04-15)

| Property | Value |
|----------|-------|
| Personal Library ID | 15775662 |
| Group Library ID | **6479832** |
| Group Name | CMT - CBS Master Thesis |
| Group Items | 39 total, 11 papers (5 journal articles + 6 preprints) |
| API Key | In `.env` |

### Why Zotero?
Solves ongoing corpus maintenance problems:
- **Centralized PDF management**: Move source of truth from local files to Zotero
- **Metadata sync**: Auto-sync between Zotero and thesis Markdown
- **Collaboration**: Support multi-user reference management via Zotero group library
- **Export consistency**: BibTeX/CSL-JSON exports stay in sync

### Recommended Tool: Pyzotero (Official Python API Client)
- MIT licensed, actively maintained
- Full read/write support for items, collections, tags, attachments
- Lightweight (single package: `uv add pyzotero`)
- Already recommended in `scientific-agent-skills/pyzotero/` skill

### Implementation Phases

| Phase | Goal | Time | Risk |
|-------|------|------|------|
| 1 | Read-only sync (detect drift) | 2-3h | LOW |
| 2 | Bidirectional metadata sync | 4-6h | MEDIUM |
| 3 | PDF attachment management | 6-8h | MEDIUM |

**Phase 1 is the MVP** — proves pyzotero setup works without data mutation risk.

### Credential Pattern
Use `.env` file (NOT in git) with API key from https://www.zotero.org/settings/keys:
```
ZOTERO_LIBRARY_ID=<user_id>
ZOTERO_API_KEY=<api_key>
ZOTERO_LIBRARY_TYPE=user
```

Already safe: `.claude/hooks/check_file_edit.py` enforces `.env` safety.

### Next Steps
1. Get Zotero API credentials (5 min at https://www.zotero.org/settings/keys)
2. Create Phase 1 task: read-only sync script
3. Document workflow in CHEATSHEET.md
4. Full recommendation at `.claude/ZOTERO_INTEGRATION_RECOMMENDATION.md`

### Key Principles
- **Keep Markdown as durable source**, Zotero is sync layer
- **Phase 1 read-only first**, Phase 2+ after proved stable
- **Always use `--dry-run`** before committing syncs
- **Log all changes** (timestamps, sources)
- **Use conflict resolution policy** (Zotero wins? Thesis wins? Manual?)

### Related Artifacts
- Full recommendation: `.claude/ZOTERO_INTEGRATION_RECOMMENDATION.md` (comprehensive guide)
- Pyzotero skill docs: `scientific-agent-skills/scientific-skills/pyzotero/SKILL.md`
- Current literature agent: `thesis_production_system/agents/literature_agent.py`
- Paper records: `docs/literature/papers/*.md` (48 files, YAML+Markdown format)
