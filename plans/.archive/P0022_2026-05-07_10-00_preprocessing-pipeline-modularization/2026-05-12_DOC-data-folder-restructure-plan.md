---
created: 2026-05-12
plan_for: P0022 + data folder restructure
---

# Plan: Restructure thesis/data/ Folder Hierarchy

## Context

The current `thesis/data/` folder is logically inconsistent:
- Raw source data lives at `raw_nielsen/` and `raw_spss_indeksdanmark/` (inconsistent prefix)
- Stage 1 conversion scripts (`raw_to_parquet/` on disk — stale name) and their output cache (`parquet_nielsen/`) are buried inside `preprocessing/`—even though they are format conversion utilities, not preprocessing logic
- `parquet_nielsen/` mixes two things: Stage 1 cache (raw, views, metadata parquet) AND Stage 2 outputs (engineered feature matrices)
- The Stage 1 folder is named `raw_to_parquet/` on disk but should be named `jsonl_to_parquet/` — specific to the format (JSONL→Parquet for Nielsen). The scripts already reference `jsonl_to_parquet/` which is the correct target name. The disk folder is what needs renaming on move.
- The P0022 modular scripts under `preprocessing/nielsen/` look for their own local cache folder (`nielsen/Energidrikke/views/`) instead of the centralized Stage 1 cache—causing the Energidrikke run failure

**Goal:** Establish a clean 3-tier `thesis/data/` hierarchy where each folder has one responsibility, then fix all stale references so the full pipeline runs correctly.

---

## Target Folder Structure

```
thesis/data/
├── raw/
│   ├── nielsen/                        ← renamed from: raw_nielsen/
│   │   ├── data_jsonl/                 (unchanged inside)
│   │   └── description/                (unchanged inside)
│   └── spss_indeksdanmark/             ← renamed from: raw_spss_indeksdanmark/
│       └── data_csv/                   (unchanged inside)
│
├── converted/
│   ├── nielsen/
│   │   ├── jsonl_to_parquet/             ← moved from: preprocessing/raw_to_parquet/
│   │   │   ├── convert_category.py
│   │   │   ├── run_all_conversions.py
│   │   │   └── README.md
│   │   └── parquet_nielsen/            ← moved from: preprocessing/parquet_nielsen/
│   │       └── {CSD,Energidrikke,Danskvand,RTD,Totalbeer}/
│   │           ├── raw/                (Stage 1 cache — parquet only)
│   │           ├── views/              (Stage 1 cache — parquet only)
│   │           └── metadata/           (Stage 1 cache — parquet only)
│   └── spss_indeksdanmark/             ← future, create empty for symmetry
│       ├── csv_to_parquet/             (placeholder, not implemented yet)
│       └── parquet_spss/               ← moved from: preprocessing/parquet_spss/ (if it exists)
│
└── preprocessing/
    └── nielsen/
        ├── shared/                     ← unchanged (terminal_utils, timing_utils, base_preprocessing)
        ├── CSD/
        │   ├── pre_csd_0_cache.py      ← updated: reads from raw/nielsen/, writes to converted/nielsen/parquet_nielsen/
        │   ├── pre_csd_1_load.py       ← updated: reads from converted/nielsen/parquet_nielsen/
        │   ├── pre_csd_{2-6}...py      ← updated paths
        │   ├── preprocessing_csd.py    ← orchestrator updated
        │   └── engineered/             ← Stage 2 outputs land here (moved from parquet_nielsen/CSD/engineered/)
        ├── Energidrikke/               ← same pattern
        ├── Danskvand/                  ← same pattern
        ├── RTD/                        ← same pattern
        ├── Totalbeer/                  ← same pattern
        ├── preprocessing_all.py        ← Phase 3 master orchestrator (pending)
        └── [legacy scripts]            ← preprocessing_*.py + run_all_preprocessing.py
                                           stay here during transition; retired in Phase 3
```

**Note on legacy scripts:** `preprocessing_csd.py` through `preprocessing_totalbeer.py` and `run_all_preprocessing.py` remain in `preprocessing/nielsen/` (or `preprocessing/` as currently placed) for now. They will be retired when Phase 3 master orchestrator is complete.

---

## Migration Steps

### Step 1 — Update PATHS.py (do first; all moves depend on it)

File: `/root/dev/thesis-manifold/PATHS.py`

Remove/rename these constants:
| Old Constant | New Constant | New Path |
|---|---|---|
| `THESIS_DATA_NIELSEN_DIR` | `THESIS_DATA_RAW_NIELSEN_DIR` | `thesis/data/raw/nielsen/` |
| `THESIS_DATA_NIELSEN_JSONL_DIR` | `THESIS_DATA_RAW_NIELSEN_JSONL_DIR` | `thesis/data/raw/nielsen/data_jsonl/` |
| `THESIS_DATA_NIELSEN_DESC_DIR` | `THESIS_DATA_RAW_NIELSEN_DESC_DIR` | `thesis/data/raw/nielsen/description/` |
| `THESIS_DATA_SPSS_DIR` | `THESIS_DATA_RAW_SPSS_DIR` | `thesis/data/raw/spss_indeksdanmark/` |
| `THESIS_DATA_SPSS_CSV_DIR` | `THESIS_DATA_RAW_SPSS_CSV_DIR` | `thesis/data/raw/spss_indeksdanmark/data_csv/` |
| `THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR` | `THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR` | `thesis/data/converted/nielsen/parquet_nielsen/` |
| `THESIS_DATA_PREPROCESSING_PARQUET_SPSS_DIR` | `THESIS_DATA_CONVERTED_SPSS_PARQUET_DIR` | `thesis/data/converted/spss_indeksdanmark/parquet_spss/` |

Add new constants:
```python
THESIS_DATA_RAW_DIR                  = THESIS_DATA_DIR / "raw"
THESIS_DATA_CONVERTED_DIR            = THESIS_DATA_DIR / "converted"
THESIS_DATA_CONVERTED_NIELSEN_DIR    = THESIS_DATA_CONVERTED_DIR / "nielsen"
THESIS_DATA_CONVERTED_SPSS_DIR       = THESIS_DATA_CONVERTED_DIR / "spss_indeksdanmark"
```

Update helper functions — change their internal paths to use new constants:
- `get_category_parquet_dir(category)` → `converted/nielsen/parquet_nielsen/{category}/`
- `get_category_raw_dir(category)` → `converted/nielsen/parquet_nielsen/{category}/raw/`
- `get_category_views_dir(category)` → `converted/nielsen/parquet_nielsen/{category}/views/`
- `get_category_metadata_dir(category)` → `converted/nielsen/parquet_nielsen/{category}/metadata/`
- `get_category_engineered_dir(category)` → `preprocessing/nielsen/{category}/engineered/`
- `get_category_jsonl_views_dir(category)` → `raw/nielsen/data_jsonl/{category}/views/` ← rename to `get_category_source_jsonl_dir(category)` for clarity

---

### Step 2 — Move folders on disk (git mv to preserve history)

Perform these git moves in order:

```bash
# 2a. Rename raw source folders
git mv thesis/data/raw_nielsen thesis/data/raw_temp_nielsen
mkdir -p thesis/data/raw
git mv thesis/data/raw_temp_nielsen thesis/data/raw/nielsen
git mv thesis/data/raw_spss_indeksdanmark thesis/data/raw/spss_indeksdanmark

# 2b. Create converted/ structure
mkdir -p thesis/data/converted/nielsen
mkdir -p thesis/data/converted/spss_indeksdanmark

# 2c. Move + rename Stage 1 scripts (raw_to_parquet on disk → jsonl_to_parquet, format-specific)
git mv thesis/data/preprocessing/raw_to_parquet thesis/data/converted/nielsen/jsonl_to_parquet

# 2d. Move Stage 1 cache (parquet_nielsen — cache subdirs only, NOT engineered/)
mkdir -p thesis/data/converted/nielsen/parquet_nielsen
# Move per category, leaving engineered/ behind:
for CAT in CSD Energidrikke Danskvand RTD Totalbeer; do
    mkdir -p thesis/data/converted/nielsen/parquet_nielsen/$CAT
    for SUBDIR in raw views metadata; do
        [ -d thesis/data/preprocessing/parquet_nielsen/$CAT/$SUBDIR ] && \
            git mv thesis/data/preprocessing/parquet_nielsen/$CAT/$SUBDIR \
                   thesis/data/converted/nielsen/parquet_nielsen/$CAT/$SUBDIR
    done
done

# 2e. Move engineered outputs → preprocessing/nielsen/{category}/engineered/
for CAT in CSD Energidrikke Danskvand RTD Totalbeer; do
    mkdir -p thesis/data/preprocessing/nielsen/$CAT/engineered
    [ -d thesis/data/preprocessing/parquet_nielsen/$CAT/engineered ] && \
        git mv thesis/data/preprocessing/parquet_nielsen/$CAT/engineered/* \
               thesis/data/preprocessing/nielsen/$CAT/engineered/
done

# 2f. Move parquet_spss if it exists
[ -d thesis/data/preprocessing/parquet_spss ] && \
    git mv thesis/data/preprocessing/parquet_spss \
           thesis/data/converted/spss_indeksdanmark/parquet_spss

# 2g. Remove now-empty parquet_nielsen/ remnant
rmdir thesis/data/preprocessing/parquet_nielsen/*/  # empty category dirs
rmdir thesis/data/preprocessing/parquet_nielsen/
```

---

### Step 3 — Update Stage 1 scripts (converted/nielsen/jsonl_to_parquet/)

File: `thesis/data/converted/nielsen/jsonl_to_parquet/convert_category.py`
- Update input path: `THESIS_DATA_RAW_NIELSEN_JSONL_DIR` (was `THESIS_DATA_NIELSEN_JSONL_DIR`)
- Update output path: `THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR` (was `THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR`)
- Fix manifest path if hard-coded

File: `thesis/data/converted/nielsen/jsonl_to_parquet/run_all_conversions.py`
- Same path constant renames
- Rename manifest file: `jsonl_to_parquet_manifest.json` (was `jsonl_to_parquet_manifest.json` — no change needed if already correct)

---

### Step 4 — Update legacy Stage 2 scripts (preprocessing_*.py × 5)

For each of: `preprocessing_csd.py`, `preprocessing_energidrikke.py`, `preprocessing_danskvand.py`, `preprocessing_rtd.py`, `preprocessing_totalbeer.py`

- Update input path constants to use `get_category_views_dir()` (now resolves to `converted/nielsen/parquet_nielsen/{category}/views/`)
- Update output path constants to use `get_category_engineered_dir()` (now resolves to `preprocessing/nielsen/{category}/engineered/`)
- Fix hard-fail error message: update printed Stage 1 path from `preprocessing/jsonl_to_parquet/` → `converted/nielsen/jsonl_to_parquet/`
- Fix docstring header: update path references from `preprocessing/parquet_nielsen/` → `converted/nielsen/parquet_nielsen/`

---

### Step 5 — Update P0022 modular scripts (preprocessing/nielsen/*/...)

**Key architectural fix:** Remove Step 0 from modular orchestrators' responsibility. Stage 1 cache is now owned entirely by `converted/nielsen/jsonl_to_parquet/`. Modular pipeline starts at Step 1.

For each orchestrator (`preprocessing_energidrikke.py`, `preprocessing_danskvand.py`, `preprocessing_rtd.py`, `preprocessing_totalbeer.py`, `preprocessing_csd.py`):
- Update `cache_exists()` to check `THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / category / "views"`
- Remove auto-run of Step 0 if cache missing; replace with helpful error message pointing to Stage 1 script
- Remove Step 0 from default STEPS list (Step 0 is now Stage 1's responsibility)

For each Step 0 script (`pre_{cat}_0_cache.py` × 5):
- Update input dir: `THESIS_DATA_RAW_NIELSEN_JSONL_DIR / CATEGORY` (was `THESIS_DATA_NIELSEN_JSONL_DIR`)
- Update output dir: `THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY` (was `THESIS_DATA_PREPROCESSING_DIR / "nielsen" / CATEGORY`)
- These scripts are now invoked by Stage 1, not by the modular orchestrators

For each Step 1–6 script:
- Update input to read from `THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"`
- Update output for engineered results to `THESIS_DATA_PREPROCESSING_DIR / "nielsen" / CATEGORY / "engineered"`

---

### Step 6 — Clean up and verify

```bash
# Confirm parquet_nielsen is gone from preprocessing/
ls thesis/data/preprocessing/  # should NOT contain parquet_nielsen or raw_to_parquet

# Confirm new structure exists
ls thesis/data/raw/
ls thesis/data/converted/nielsen/
ls thesis/data/preprocessing/nielsen/

# Compile check — all scripts
python -m py_compile thesis/data/converted/nielsen/jsonl_to_parquet/convert_category.py
python -m py_compile thesis/data/converted/nielsen/jsonl_to_parquet/run_all_conversions.py
python -m py_compile thesis/data/preprocessing/preprocessing_*.py
python -m py_compile thesis/data/preprocessing/nielsen/*/pre_*.py
python -m py_compile thesis/data/preprocessing/nielsen/*/preprocessing_*.py

# Import check — PATHS.py helpers resolve correctly
python -c "from PATHS import get_category_views_dir, get_category_engineered_dir; \
    print(get_category_views_dir('CSD')); print(get_category_engineered_dir('CSD'))"
```

---

### Step 7 — Update P0022 plan + docs

- Update P0022 plan frontmatter: add note about folder restructure, date 2026-05-12
- Update `docs/contributing/repository_map.md` with new `thesis/data/` hierarchy
- Update `converted/nielsen/jsonl_to_parquet/README.md` with new path references

---

## Stale Reference Inventory (confirmed by grep)

| File | Stale Reference | Fix |
|---|---|---|
| `preprocessing_*.py` ×5 | docstrings + error messages reference `jsonl_to_parquet/` — correct target name, but old path prefix (`preprocessing/`) | → `converted/nielsen/jsonl_to_parquet/` |
| `preprocessing_*.py` ×5 | `parquet_nielsen/` in docstrings | → `converted/nielsen/parquet_nielsen/` |
| `raw_to_parquet/convert_category.py` | `THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR` | → `THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR` |
| `raw_to_parquet/run_all_conversions.py` | manifest file may still be named `jsonl_to_parquet_manifest.json` — verify path is correct after move | → keep as `jsonl_to_parquet_manifest.json` |
| `nielsen/*/pre_*_0_cache.py` | local output dir under `nielsen/{cat}/` | → `converted/nielsen/parquet_nielsen/` |
| `nielsen/*/pre_*_{1-6}*.py` | local views/metadata input dir | → `converted/nielsen/parquet_nielsen/` |
| `nielsen/*/preprocessing_*.py` ×5 | `cache_exists()` checks local `views/` folder | → check `converted/nielsen/parquet_nielsen/` |

---

## What Is NOT Changing

- Content inside `raw/nielsen/data_jsonl/` and `raw/nielsen/description/` — just moved, not modified
- Legacy scripts `preprocessing_*.py` and `run_all_preprocessing.py` — stay in `preprocessing/` during transition
- P0022 modular script logic (Steps 1–6) — paths updated but no algorithmic changes
- `thesis/data/assessment/` — untouched

---

## Verification (end-to-end)

After all steps, validate the full pipeline runs:
```bash
# Stage 1: Convert CSD JSONL → Parquet (fast, CSD is small)
python thesis/data/converted/nielsen/jsonl_to_parquet/convert_category.py --category CSD

# Stage 2 (legacy): Run CSD feature engineering
python thesis/data/preprocessing/preprocessing_csd.py

# Stage 2 (modular): Run CSD via P0022 orchestrator
python thesis/data/preprocessing/nielsen/CSD/preprocessing_csd.py

# Confirm outputs landed in correct locations
ls thesis/data/converted/nielsen/parquet_nielsen/CSD/views/
ls thesis/data/preprocessing/nielsen/CSD/engineered/
```
