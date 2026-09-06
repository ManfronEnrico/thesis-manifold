# Indeks Danmark / SPSS data — archived 2026-09-06

**Decision (Brian, 2026-09-06):** the Indeks Danmark consumer-survey dataset was
never used, and with 9 days to submission it will not be. Archived rather than
deleted, since it is real licensed source data.

## What is here

```
spss_indeksdanmark/
  indeksdanmark_data.csv          survey responses
  indeksdanmark_metadata.csv      variable metadata
  official_codebook.csv           codebook
  description/spss_indeksdanmark_data_model.md
  scripts/spss_indeksdanmark_loader.py
```

Was at `01_SRQ1_Model_Training/01_thesis_data/_00_raw/spss_indeksdanmark/`
(and before the 2026-09-06 SRQ restructure, `02_thesis_data/_00_raw/...`).

## What was removed alongside it

`PATHS.py` constants, all four already resolving to non-existent directories
before this archival (only the `_00_raw` folder ever materialised):

- `THESIS_DATA_RAW_SPSS_DIR`
- `THESIS_DATA_RAW_SPSS_CSV_DIR`
- `THESIS_DATA_CONVERTED_SPSS_DIR`
- `THESIS_DATA_CONVERTED_SPSS_PARQUET_DIR`

## Open item this creates — the thesis still claims this data

Two lines in the abstract describe Indeks Danmark as part of the empirical base:

- "deployed on Danish CSD retail data (Nielsen CSD panel + **Indeks Danmark
  consumer survey**)"
- "Single empirical context: Danish CSD retail, Manifold AI / Nielsen CSD panel,
  **Indeks Danmark consumer survey**"

Present in both `06_thesis_writing/sections-drafts/abstract.md` (lines 40, 56)
and the 2026-09-05 `.docx` snapshot — i.e. **in the authoritative `.docx`**.

Since the dataset was never used, these are claims about data that does not
inform any result. They must be corrected in the `.docx` (per
`.claude/rules/writing-surface-authority.md`, prose is edited there, not in the
draft `.md`). Tracked as P0046 F23.

## Also superseded

`utility_scripts/scripts/ml_retraining/01_ingest_raw.py` ingests Indeks at
`PROJECT_ROOT / "Thesis" / "indeksdanmark"` — a path that has not existed since
the P0028 restructure (2026-07-11). That whole `ml_retraining/` folder is an
April-era pipeline superseded by `01_SRQ1_Model_Training/`; it was left in place
here because it is broken for reasons predating this change, and archiving it is
a separate decision.
