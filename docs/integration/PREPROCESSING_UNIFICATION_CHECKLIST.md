# Preprocessing Unification Checklist

**Status:** CSD Complete, 4 Categories Remaining

---

## Completed ✅

- [x] **PATHS.py** — Added 5 category/type helper functions
- [x] **save_all_datasets.py** — Reorganized CSV output by category / (raw | views | metadata)
- [x] **preprocessing_csd.py** — Load raw tables, save all three types, simplified naming

---

## To Do: Apply Same Pattern to 4 Other Categories

### preprocessing_danskvand.py
- [ ] Update PATHS imports (add helpers)
- [ ] Update input paths: `INPUT_RAW_DIR`, `INPUT_VIEWS_DIR`, `INPUT_METADATA_DIR`
- [ ] Update output paths: `OUT_RAW`, `OUT_VIEWS`, `OUT_METADATA`, `OUT_ENGINEERED`
- [ ] Update load_raw() to load from raw tables (not views)
- [ ] Add save_dimension_tables() call in main()
- [ ] Rename save_outputs() → save_engineered_outputs()
- [ ] Update output filenames: `danskvand_feature_matrix.parquet`, etc.
- [ ] Test: Verify all directories created

### preprocessing_energidrikke.py
- [ ] (Same as Danskvand)

### preprocessing_rtd.py
- [ ] (Same as Danskvand)

### preprocessing_totalbeer.py
- [ ] (Same as Danskvand)

---

## Notebook Updates

### specialized_CSD.ipynb
- [ ] Update Cell 10: Load dimension tables from new parquet paths
  ```python
  from PATHS import get_category_views_dir
  views_dir = get_category_views_dir("CSD")
  dim_period = pd.read_parquet(views_dir / "csd_clean_dim_period_v.parquet")
  ```

### specialized_danskvand.ipynb
- [ ] (Same as CSD)

### specialized_energidrikke.ipynb
- [ ] (Same as CSD)

### specialized_rtd.ipynb
- [ ] (Same as CSD)

### specialized_totalbeer.ipynb
- [ ] (Same as CSD)

---

## Testing Workflow

1. **Run save_all_datasets.py** (once Nielsen data available)
   - Verify CSV files organized into category / (raw | views | metadata)
   - Verify manifest generated

2. **Run preprocessing_csd.py**
   - Verify Step 0 caches raw/views/metadata as parquet
   - Verify `OUT_RAW`, `OUT_VIEWS`, `OUT_METADATA`, `OUT_ENGINEERED` directories created
   - Verify engineered outputs use simplified naming (csd_*, not specialized_CSD_*)

3. **Test specialized_CSD.ipynb**
   - Verify dimension tables load from new parquet paths
   - Verify notebook runs without errors

4. **Repeat for 4 other categories**

---

## Migration Checklist (For Later)

- [ ] Delete old specialized_CSD output folder structure (after verified working)
- [ ] Update `.gitignore` to exclude new parquet directories
- [ ] Update GitHub workflow/CI if preprocessing runs are automated
- [ ] Document new directory structure in team wiki/docs

---

## Time Estimate

- **Per script:** 15–20 minutes (mechanical copy-paste with category name changes)
- **All 4 scripts:** 1–1.5 hours
- **All 5 notebooks:** 1–1.5 hours
- **Total:** 2–3 hours for full unification

---

## Notes

- **CSD is the template:** Use preprocessing_csd.py as reference for other 4
- **Naming pattern:** `{category_lower}_*` (csd_, danskvand_, energidrikke_, rtd_, totalbeer_)
- **PATHS helpers:** All 5 categories use the same helper functions (no changes needed)
- **Raw tables source:** All categories have raw tables in Nielsen schema (same pattern)

---

## Questions?

Refer to:
- `docs/integration/IMPLEMENTATION_SUMMARY_20260505.md` — What was implemented & why
- `docs/integration/NIELSEN_DATA_ARCHITECTURE.md` — Design rationale & data usage
- `PATHS.py` — Helper function signatures & docstrings
- `preprocessing_csd.py` — Working example implementation
