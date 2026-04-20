# Unified Sync Check Guide

## Overview

The unified sync check integrates three paper management systems:
- **Zotero** (source of truth for paper metadata)
- **Google Drive** (PDF file storage)
- **NotebookLM** (paper ingestion and notebook organization)

This guide explains how to run sync checks and interpret the results.

---

## Quick Start

### Basic Sync Check (No Changes)

```bash
python scripts/unified_sync_check.py --check-only
```

**Output**: Summary of current state without modifying the manifest.

### Live Sync Check (Update Manifest)

```bash
python scripts/unified_sync_check.py
```

**Output**: Updates `thesis/literature/ingestion_manifest.json` with current state.

### Verbose Mode (Show Details)

```bash
python scripts/unified_sync_check.py --verbose
```

**Output**: Shows match confidence scores and detailed component matching.

---

## Understanding Sync Status

Each paper has a `sync_status` that describes its state across the three systems:

| Status | Meaning | Action |
|--------|---------|--------|
| **COMPLETE** | In Zotero, Drive, and NotebookLM | Nothing needed |
| **PARTIAL** | In 2 of 3 systems | Manual review needed |
| **NEW_ZOTERO** | In Zotero only | Add PDF to Drive, then ingest to NotebookLM |
| **NEW_GDRIVE** | In Drive only | Add to Zotero and NotebookLM |
| **MISNAMED** | In all 3 systems but Drive filename is wrong | Rename file to match standard |
| **ORPHAN_NOTEBOOKLM** | Ingested in NotebookLM but not in Zotero/Drive | Investigate: paper may have been deleted |

---

## Filename Standards

Generated filenames follow this pattern:

```
FirstAuthor-SecondAuthor_or_et_al-Year-Title_with_underscores.pdf
```

### Rules

- **1 author**: `Smith-2024-Title_of_Paper.pdf`
- **2 authors**: `Smith-Jones-2024-Title_of_Paper.pdf`
- **3+ authors**: `Smith-et_al-2024-Title_of_Paper.pdf`
- **Author names with hyphens**: Replace with underscores (e.g., `al_karkhi-rzadkowski-...`)
- **Title spaces**: Replace with underscores
- **Title length**: First 50-60 characters

### Example

```
Avramova-Fedele-2025-Overview_of_Existing_Multi_Criteria_Decision_Making.pdf
```

---

## Manual Workflow

### Adding a New Paper

1. **Add to Zotero** (fill in: authors, title, year, date)
   ```bash
   # Run sync to generate filename
   python scripts/unified_sync_check.py
   # Output: Paper shows NEW_ZOTERO status
   ```

2. **Download PDF and Upload to Drive**
   - Get the expected filename from sync output
   - Upload PDF with that name to appropriate folder
   - Run sync again to verify it's found

3. **Ingest to NotebookLM** (manual for now)
   - Add to selected notebooks (ch2-literature, srq1-models, etc.)
   - After ingestion, run sync to update status to INGESTED

### Fixing Misnamed Files

If sync shows `MISNAMED` status:

```bash
python scripts/unified_sync_check.py --resolve-misnamed
```

This will:
1. Show you which files need renaming
2. Prompt for confirmation for each file
3. Rename files on Drive to match standard

---

## Manifest Schema (v2.1)

Each entry tracks:

```json
{
  "citation_key": "avramova_overview_2025",
  "title": "Overview of Existing Multi-Criteria Decision Making...",
  "gdrive_filename": "Avramova-et_al-2025-Overview_of_...",
  "gdrive_file_id": "file-abc123",
  
  "zotero_status": "active",           // active, archived, removed, missing
  "gdrive_status": "found",            // found, missing, misnamed, pending_rename
  "notebooklm_status": "ingested",     // ingested, ingested_partial, pending, missing, error
  
  "sync_status": "COMPLETE",           // Computed: COMPLETE, PARTIAL, NEW_*, ORPHAN, MISNAMED
  "match_confidence": 1.0,             // 0.0-1.0 (exact=1.0, fuzzy=0.5-0.9)
  "last_checked": "2026-04-20T12:00:00Z",
  
  "notebooks": ["ch2-literature", "srq1-models"],
  "srqs": ["SRQ1", "SRQ3"],
  "notebooklm_source_ids": {
    "ch2-literature": "src-uuid-abc1",
    "srq1-models": "src-uuid-abc2"
  }
}
```

---

## Troubleshooting

### "Could not find insertion marker"

**Problem**: Manifest file is malformed.

**Solution**: Check that `thesis/literature/ingestion_manifest.json` is valid JSON.

```bash
python -m json.tool thesis/literature/ingestion_manifest.json
```

### Match confidence is low (< 0.8)

**Problem**: Filename doesn't match Zotero data well.

**Solution**: 
1. Check Zotero metadata (author, year, title)
2. Manually rename Drive file if needed
3. Update Zotero metadata to be more complete

### Paper shows "ORPHAN_NOTEBOOKLM"

**Problem**: Paper is ingested in NotebookLM but not found in Zotero.

**Solution**: 
1. Check if paper was deleted from Zotero
2. Either re-add to Zotero or remove from NotebookLM
3. Run sync again

---

## Next Steps

After Phase 1 (filename generation), Phase 2 will add:
- Manual SRQ tagging in Zotero UI (user-driven)
- Automated notebook assignment based on SRQ coverage
- Per-notebook sync status

Phase 3+ will automate:
- Batch PDF uploads from Zotero
- Scheduled sync checks
- Auto-ingestion to NotebookLM
