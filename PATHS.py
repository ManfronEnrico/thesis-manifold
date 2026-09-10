"""
Project Paths Configuration

Centralizes all path definitions for the thesis project using pathlib.Path for
cross-platform compatibility. Paths are organized hierarchically from root
directory down through subdirectories.

Each path variable includes type hints and docstrings to provide context on
hover in your IDE. Use these constants throughout notebooks and scripts
instead of hardcoded strings.

Reference: PATHS_markdown.ipynb for detailed documentation with examples.

Repo structure — SRQ-ALIGNED RESTRUCTURE, 2026-09-06 (P0046). This SUPERSEDES
the P0028 topic-oriented tiers. Top-level folders now map one-to-one onto the
research questions, so a script's location states which SRQ it answers:

    00_thesis_context/          research-questions/, thesis-topic/,
                                formal-requirements/, methodology/,
                                prometheus-integration/
    01_SRQ1_Model_Training/     01_thesis_data/  (_00_raw .. _03_engineered)
                                02_thesis_modelling/  (model_training/)
    02_SRQ2_Tool_Interface/     forecast_tool.py, forecast_log.jsonl
    03_SRQ3_Integration_Readiness/   (empty — SRQ3 not yet started)
    04_SRQ4_Scenario_Experiment/     scenario_setup/, plus the runs and raw
                                responses those scenarios produce
    05_thesis_results/          srq{N}_{slug}/ — aggregated tables, figures and
                                diagrams ONLY. Every artefact that could enter
                                the thesis lives here, exactly once.
    06_thesis_writing/          citations/, docx-exported-snapshots/,
                                notebookLM/, sections-drafts/, writing_notes/

CLEAN-REPO BOUNDARY (DEC-P0046-SHIP-SCOPE): tiers 01-05 ship to assessors.
Tier 00 and tier 06 are the AI-guided writing harness and are excluded.

ARTEFACT RULE (DEC-P0046-SINGLE-HOME): tier 06 holds NO figures, tables or
diagrams. Producers live with their SRQ and write into 05_thesis_results/.
There is no second copy of any artefact anywhere.

Everything else at root (utility_scripts/, plans/, user-docs/, .claude/) is
tooling/governance/docs, not thesis content, and is out of this numbered scheme
by design.
"""


from pathlib import Path


DEBUG = False  # Set to True to print all paths on import

# ============================================================================
# 0. ROOT REPOSITORY
# ============================================================================

ROOT_DIR: Path = Path(__file__).parent
"""
Base folder of the thesis project containing all subfolders and files.

This is the root directory where PATHS.py is located. All other paths in the
project are defined relative to ROOT_DIR for cross-platform compatibility
across Windows, macOS, and Linux.

Example:
    from PATHS import ROOT_DIR
    print(ROOT_DIR.resolve())  # C:\\dev\\thesis-manifold
"""

# ============================================================================
# 1. THESIS DIRECTORY
# ============================================================================

THESIS_DIR: Path = ROOT_DIR
"""
Alias for ROOT_DIR, kept for backwards compatibility with code that still
imports THESIS_DIR.

As of the P0028 repo restructure, the "thesis/" folder segment was removed
entirely — every former thesis/* subfolder now lives directly at repo root
(00_thesis_context/, 01_thesis_research/, 02_thesis_data/, etc.). THESIS_DIR
is retained as a plain alias for ROOT_DIR rather than removed outright, to
avoid breaking any import that hasn't been updated yet.

Example:
    from PATHS import THESIS_DIR
    print(THESIS_DIR.resolve())  # C:\\dev\\thesis-manifold
"""

# ============================================================================
# 0.1 TOP-LEVEL TIER-ROOT DIRECTORIES (P0028 restructure)
# ============================================================================

THESIS_CONTEXT_DIR: Path = ROOT_DIR / "00_thesis_context"
"""
Tier 00 — project context. NOT shipped to assessors (writing harness).

Holds 'research-questions/' (moved here 2026-09-06 when 01_thesis_research/ was
archived), 'thesis-topic/', 'formal-requirements/', 'methodology/' and
'prometheus-integration/'.

Example:
    from PATHS import THESIS_CONTEXT_DIR
    print(THESIS_CONTEXT_DIR.resolve())
"""

# REMOVED 2026-09-06 (P0046 SRQ restructure): THESIS_RESEARCH_DIR and
# THESIS_RESEARCH_LITERATURE_DIR. The 01_thesis_research/ tier was archived; its
# research-questions/ folder moved under 00_thesis_context/ (see
# THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR below) and the literature corpus now
# lives with the writing apparatus at 06_thesis_writing/citations/ (see
# THESIS_WRITING_CITATIONS_DIR). The tier number 01 was reused for
# 01_SRQ1_Model_Training/, so leaving these constants pointing at
# "01_thesis_research" would have silently resolved into an unrelated tree.

THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR: Path = THESIS_CONTEXT_DIR / "research-questions"
"""
The RQ/SRQ definitions. Moved from 01_thesis_research/research-questions/ on
2026-09-06.

Example:
    from PATHS import THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR
    rqs = THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR / "2026_08_22-20_00-research-questions.md"
"""

THESIS_CONTEXT_METHODOLOGY_DIR: Path = THESIS_CONTEXT_DIR / "methodology"
"""
Saunders research-onion notes and the SRQ4 evaluation protocol.
"""

THESIS_CONTEXT_REQUIREMENTS_DIR: Path = THESIS_CONTEXT_DIR / "formal-requirements"
"""
CBS compliance notes, citation-verification SOP, compliance reports.
"""

THESIS_RESULTS_DIR: Path = ROOT_DIR / "05_thesis_results"
"""
Tier 05 — THE single home for every figure, table and diagram that could enter
the thesis. Shipped to assessors.

Renumbered from 04_thesis_results/ on 2026-09-06. Per DEC-P0046-SINGLE-HOME no
artefact is ever copied out of here into the writing tier: humans browse this
tree and paste from it directly into the .docx.

Per DEC-P0046-ROUTING, producers live with their SRQ (01_SRQ1_.., 04_SRQ4_..)
and write their aggregated outputs here. Raw per-run material stays with the
experiment that produced it, NOT here.

Example:
    from PATHS import THESIS_RESULTS_DIR
    print(THESIS_RESULTS_DIR.resolve())
"""

# ---------------------------------------------------------------------------
# CHAPTER-KEYED RESULTS (DEC-CHAPTER-FOLDERS, 2026-09-07)
# ---------------------------------------------------------------------------
# Artefacts are filed by the THESIS CHAPTER that discusses them, not by the SRQ
# whose script produced them. The writing workflow is chapter by chapter, so the
# folder a writer opens should be the chapter they are writing.
#
# The two keys genuinely disagree, which is why this layer exists:
#   * export_appendix.py lives under SRQ4 but 6 of its 14 tables are pipeline
#     and model tables belonging to Ch4 and Ch6;
#   * the holiday tables split Ch4 (the calendar source) from Ch6 (the ablation
#     RESULTS) while sharing a subject.
#
# Folders are named "{NN}_{slug}" so the tree sorts in reading order, but the
# NUMBER IS DERIVED from position in CHAPTER_SLUGS and never written down twice.
# A reorder is under active consideration (P0048 phase 8: swapping the benchmark
# and architecture chapters, and possibly moving feature diagnostics into the
# data chapter), so a hand-typed number would go stale the moment it happens.
#
# The slug names the SUBJECT and survives a renumbering; the prefix is only a
# sort key. Nothing in the codebase references a chapter number to build a path,
# so reordering CHAPTER_SLUGS is the whole edit -- see get_chapter_results_dir.

CHAPTER_SLUGS: tuple = (
    "introduction",
    "literature_review",
    "methodology",
    "data_assessment",
    "model_benchmark",
    "architecture",
    "decision_synthesis",
    "experimental_evaluation",
    "discussion",
    "conclusion",
)
"""The ten chapter subjects, in current document order.

Slugs, not numbers -- see the note above. To reorder the thesis, reorder this
tuple; nothing else needs to change, because no path contains a chapter number.
"""

CHAPTER_ORDER: dict = {slug: i + 1 for i, slug in enumerate(CHAPTER_SLUGS)}
"""slug -> current chapter number. The ONLY place the numbering is written down.

Use it for display ("Chapter 6"), never to build a path.
"""


def _chapter_folder(slug: str) -> str:
    """"{NN}_{slug}" -- the on-disk folder name for a chapter.

    Used by both the constants below and get_chapter_results_dir(), so the
    prefix is computed in exactly one place. Typing "05_model_benchmark" into a
    constant would survive a reorder of CHAPTER_SLUGS and silently point at the
    wrong chapter.
    """
    return f"{CHAPTER_ORDER[slug]:02d}_{slug}"


THESIS_RESULTS_SRQ1_DIR: Path = THESIS_RESULTS_DIR / _chapter_folder("model_benchmark")
"""
SRQ1 — model performance: benchmark metrics, calibration, SHAP, demand classes.

Renamed from "srq1" 2026-09-06 to carry a descriptive slug (DEC-P0046-SLUGS).
NOTE: contents are known to be partly stale (P0046 F16/F19) and are pending the
Phase 3b reorganisation into figures/ tables/ models/.
"""

THESIS_RESULTS_SRQ2_DIR: Path = THESIS_RESULTS_DIR / _chapter_folder("decision_synthesis")
"""
SRQ2 — structured tool interface results.

Renamed from "srq2" 2026-09-06. NOTE: known to contain LLM-as-Judge outputs from
a dropped design (P0046 F19); do not cite before the Phase 3b staleness triage.
"""

THESIS_RESULTS_SRQ3_DIR: Path = THESIS_RESULTS_DIR / _chapter_folder("discussion")
"""
SRQ3 — integration readiness. Placeholder: SRQ3 has not been started, so this
directory may not exist on disk yet.
"""

THESIS_RESULTS_SRQ4_DIR: Path = THESIS_RESULTS_DIR / _chapter_folder("experimental_evaluation")
"""
SRQ4 — scenario comparison: AGGREGATED results only (summary tables, figures).

Renamed from "srq4" 2026-09-06. Per DEC-P0046-RUNS-WITH-EXPERIMENT the per-run
folders and raw LLM responses live at SRQ4_EXPERIMENT_DIR, not here — this holds
the aggregation across runs.
"""

# REMOVED 2026-09-07 (DEC-CHAPTER-FOLDERS): THESIS_RESULTS_APPENDIX_DIR and
# THESIS_RESULTS_DIAGRAMS_DIR. Both directories are gone -- appendix tables and
# diagrams are now written into the chapter that discusses them, via
# get_chapter_tables_dir() / get_chapter_figures_dir().
#
# Removed rather than repointed because there is no single directory left for
# either to name: their contents deliberately span several chapters. A constant
# resolving to a path that no longer exists is how the pre-2026-09-06 breakage
# went unnoticed -- Path() never validates, so it fails at read/write time
# rather than at import.

THESIS_RESULTS_EDA_DIR: Path = (THESIS_RESULTS_DIR
                                 / _chapter_folder("data_assessment") / "eda")
"""
Per-category EDA artefacts promoted as thesis candidates: the markdown tables
and PNG plots (~38 per category).

Per DEC-P0046-EDA-SPLIT the .csv step outputs stay in the pipeline, because
downstream EDA steps consume them; the .md tables and .png plots are report
material and belong here.
"""

THESIS_WRITING_DIR: Path = ROOT_DIR / "06_thesis_writing"
"""
Tier 06 — the writing harness. NOT shipped to assessors.

Renumbered from 05_thesis_writing/ on 2026-09-06. Holds ONLY writing apparatus:
citations/ (Zotero), docx-exported-snapshots/, notebookLM/, sections-drafts/,
thesis_inspiration/, writing_notes/.

Per DEC-P0046-SINGLE-HOME this tier holds NO figures, tables or diagrams. If you
are about to write an artefact here, it belongs in THESIS_RESULTS_DIR instead.

Example:
    from PATHS import THESIS_WRITING_DIR
    print(THESIS_WRITING_DIR.resolve())
"""

THESIS_WRITING_CITATIONS_DIR: Path = THESIS_WRITING_DIR / "citations"
"""
Zotero-backed literature corpus (bibtex.bib, citations.json). Was
01_thesis_research/literature/ before the 2026-09-06 restructure.
"""

THESIS_WRITING_DRAFTS_DIR: Path = THESIS_WRITING_DIR / "sections-drafts"
"""
Bullet skeletons, status headers and provenance notes — NOT prose. Prose lives
in the OneDrive .docx (see .claude/rules/writing-surface-authority.md).
"""

THESIS_WRITING_SNAPSHOTS_DIR: Path = THESIS_WRITING_DIR / "docx-exported-snapshots"
"""
Read-only diffable mirror of the .docx, regenerated by
utility_scripts/scripts/thesis_snapshot.py. Never hand-edited.
"""

THESIS_WRITING_NOTES_DIR: Path = THESIS_WRITING_DIR / "writing-notes"
"""
Notes for Brian and Enrico, never for an assessor.

Tiers 01-05 are read by assessors, so nothing student-facing may appear in them
-- whether or not it is marked as internal. That is why the generators write
their editorial notes HERE rather than into the artefacts they describe.

Filed by chapter -- see get_chapter_notes_dir below.
"""

# Editorial notes for generated tables and figures are filed by CHAPTER, under
# the same writing-notes folder that already holds the hand-written notes for
# that chapter. They exist to help finish a chapter, so they belong beside the
# other notes for it -- grouping by producer would serve the producer, not the
# person writing.
#
# The folder name carries the chapter NUMBER as a prefix because Brian and
# Enrico navigate these by hand and think in chapter numbers. The number is
# derived from CHAPTER_ORDER, never typed, so a reorder in Word moves the notes
# with the chapter instead of leaving them under a stale prefix.

_CHAPTER_NOTES_FOLDER: dict = {
    # Two chapters were given short folder names before this mapping existed and
    # are kept as they are: they are folders the authors already open by hand,
    # and the slug is recoverable from the chapter number beside it.
    "decision_synthesis": "synthesis",
    "experimental_evaluation": "experiment",
}
"""slug -> folder suffix, where the established folder differs from the slug."""


def get_chapter_notes_dir(slug: str) -> Path:
    """Writing notes for one chapter -- `writing-notes/ch{N}_{name}/`.

    Notes for GENERATED artefacts land in a `generated/` subfolder, so a
    regenerated note can never overwrite something a human wrote.

    Raises on an unknown slug rather than defaulting, for the same reason
    _chapter_dir does: a default files a note in whichever chapter was
    convenient and lets it sit there unnoticed.
    """
    if slug not in CHAPTER_ORDER:
        raise KeyError(
            f"Unknown chapter slug {slug!r}; expected one of {list(CHAPTER_SLUGS)}")
    name = _CHAPTER_NOTES_FOLDER.get(slug, slug)
    d = THESIS_WRITING_NOTES_DIR / f"ch{CHAPTER_ORDER[slug]}_{name}"
    return d


def get_chapter_generated_notes_dir(slug: str) -> Path:
    """Where a producer writes the editorial note for one generated artefact."""
    return get_chapter_notes_dir(slug) / "generated"

# ============================================================================
# 0.2 SRQ TIER ROOTS (2026-09-06 SRQ-aligned restructure)
# ============================================================================

SRQ1_DIR: Path = ROOT_DIR / "01_SRQ1_Model_Training"
"""
SRQ1 — model training. Holds both the data pipeline and the modelling code,
because the models are what the data pipeline exists to feed.
"""

SRQ2_DIR: Path = ROOT_DIR / "02_SRQ2_Tool_Interface"
"""
SRQ2 — the structured tool interface (forecast_tool.py, forecast_log.jsonl).

NOTE: the former model_serving_interface/ subfolders (system_a_forecast/,
system_b_conversational/, srq2_synthesis/) no longer exist as live code — those
scripts are in .archive/superseded_scripts_2026-08/. Constants for them were
removed rather than left dangling; see the note further below.
"""

SRQ3_DIR: Path = ROOT_DIR / "03_SRQ3_Integration_Readiness"
"""
SRQ3 — integration readiness. Currently empty; SRQ3 has not been started.
"""

SRQ4_DIR: Path = ROOT_DIR / "04_SRQ4_Scenario_Experiment"
"""
SRQ4 — scenario experiments: the harness, plus the runs and raw responses it
produces. Aggregated results go to THESIS_RESULTS_SRQ4_DIR.
"""

SRQ4_SCENARIO_SETUP_DIR: Path = SRQ4_DIR / "scenario_setup"
"""
The SRQ4 harness: srq4_experiment.py, prompts.py, verify_setup.py,
inspect_runs.py, export_appendix.py and the resource-measurement scripts.

Was 03_thesis_modelling/scenario_setup/ before 2026-09-06.
"""

SRQ4_RUNS_DIR: Path = SRQ4_DIR / "runs"
"""
Per-run scenario outputs and raw LLM responses.

Per DEC-P0046-RUNS-WITH-EXPERIMENT these live beside the harness that produced
them, not in the results tier, which holds only the aggregation across runs.
"""

# ============================================================================
# 1.1 MODELLING SUBDIRECTORY
# ============================================================================

THESIS_MODELLING_DIR: Path = SRQ1_DIR / "02_thesis_modelling"
"""
Modelling code for SRQ1. Moved under 01_SRQ1_Model_Training/ on 2026-09-06.

Example:
    from PATHS import THESIS_MODELLING_DIR
    print(THESIS_MODELLING_DIR.resolve())
"""

# REMOVED 2026-08-19: THESIS_MODELLING_NOTEBOOKS_DIR and
# THESIS_MODELLING_PROMPTS_DIR. Both directories were archived to
# 03_thesis_modelling/.archive/ and the constants would have resolved to paths
# that no longer exist.
#   notebooks/ -> .archive/notebooks_srq1_srq2_2026-08/  (6 of 10 referenced
#                 `totalbeer`, the fifth category dropped by DEC-GRAIN; they also
#                 predate the H=3 horizon and the 2026-08-18 leakage fixes)
#   prompts/   -> .archive/prompts_srq2_2026-08/  (Enrico's SRQ2/SRQ3 prompt set
#                 and partially-executed human-eval pilot -- a DIFFERENT research
#                 question from SRQ4; see the archive README before reusing)
# SRQ4 prompts now live in 03_thesis_modelling/scenario_setup/prompts.py, as
# code rather than data, so they are diffable and reviewable alongside the
# harness that sends them.

# MOVED 2026-09-06: THESIS_MODELLING_SCENARIO_DIR is now SRQ4_SCENARIO_SETUP_DIR
# (03_thesis_modelling/scenario_setup/ -> 04_SRQ4_Scenario_Experiment/scenario_setup/).
# Kept as an alias so existing imports keep working.
THESIS_MODELLING_SCENARIO_DIR: Path = SRQ4_SCENARIO_SETUP_DIR
"""Deprecated alias for SRQ4_SCENARIO_SETUP_DIR. Prefer the SRQ4_* name."""

THESIS_MODELLING_ARCHIVE_DIR: Path = THESIS_MODELLING_DIR / ".archive"
"""
Superseded modelling artefacts, retained as provenance rather than deleted.

Nothing here is on a live code path, but at least one item (the SRQ2/SRQ3
human-eval pilot) holds results that were never reproduced elsewhere and is
gitignored, so it exists only on the machine that generated it. Read
.archive/README.md before deleting anything.
"""

THESIS_MODELLING_TRAINING_DIR: Path = THESIS_MODELLING_DIR / "model_training"
"""
Directory containing ML model training scripts (SRQ1 forecasting, SRQ2 synthesis,
SRQ4 code-as-action experiments).

Example:
    from PATHS import THESIS_MODELLING_TRAINING_DIR
    script = THESIS_MODELLING_TRAINING_DIR / "srq1_benchmark.py"
"""

# REMOVED 2026-09-06 (P0046 SRQ restructure): THESIS_MODELLING_SERVING_DIR,
# THESIS_MODELLING_SERVING_SRQ2_SYNTHESIS_DIR,
# THESIS_MODELLING_SERVING_SYSTEM_A_DIR and
# THESIS_MODELLING_SERVING_SYSTEM_B_DIR.
#
# 03_thesis_modelling/model_serving_interface/ no longer exists. Its scripts
# (forecast_service.py, srq2_synthesis.py, srq2_agent.py) are archived under
# 01_SRQ1_Model_Training/02_thesis_modelling/.archive/superseded_scripts_2026-08/,
# and SRQ2's live surface is now 02_SRQ2_Tool_Interface/forecast_tool.py — see
# SRQ2_DIR. These constants are removed rather than repointed because there is
# no live directory for them to point at; a constant resolving to a missing path
# is how the pre-2026-09-06 breakage went unnoticed.

# ============================================================================
# 1.2 DATA SUBDIRECTORY
# ============================================================================

THESIS_DATA_DIR: Path = SRQ1_DIR / "01_thesis_data"
"""
Directory containing all datasets, raw data sources, and preprocessing scripts.

Organized by data source (Nielsen, Indeks Danmark, assessment data) and
processing stage. This is the hub for all data management related to the
thesis research.

Moved under 01_SRQ1_Model_Training/ on 2026-09-06: the data pipeline exists to
feed SRQ1's models, so it lives with them.

Example:
    from PATHS import THESIS_DATA_DIR
    print(THESIS_DATA_DIR.resolve())
"""

# REMOVED 2026-09-06: THESIS_DATA_ASSESSMENT_DIR. The 02_thesis_data/assessment/
# directory did not survive the restructure and has no replacement on disk.
# Human-eval material, where it exists, is in the modelling .archive/.

THESIS_DATA_PREPROCESSING_DIR: Path = THESIS_DATA_DIR / "_02_preprocessing"
"""
Directory for data preprocessing scripts and intermediate pipeline outputs.

This is Tier 3 of the 4-tier data hierarchy. Contains Python scripts for preprocessing
workflows and intermediate pipeline outputs (step 0-6 logs, temporary parquets).

Example:
    from PATHS import THESIS_DATA_PREPROCESSING_DIR
    script = THESIS_DATA_PREPROCESSING_DIR / "nielsen" / "CSD" / "preprocessing_csd.py"
"""

THESIS_DATA_ENGINEERED_DIR: Path = THESIS_DATA_DIR / "_03_engineered"
"""
Directory for final engineered feature matrices and model-ready outputs.

This is Tier 4 of the 4-tier data hierarchy. Contains final outputs from feature
engineering pipelines: feature matrices, split metadata, series indices.
Holds a single granularity subfolder, bymonth/ (see
THESIS_DATA_ENGINEERED_BYMONTH_DIR below). Per DEC-GRAIN (2026-07-12) the
project grain is locked to brand x month; the former bychain/ split was
deleted from disk and its path constants removed in P0035.

Example:
    from PATHS import THESIS_DATA_ENGINEERED_DIR
    print(THESIS_DATA_ENGINEERED_DIR.resolve())
"""

THESIS_DATA_ENGINEERED_BYMONTH_DIR: Path = THESIS_DATA_ENGINEERED_DIR / "bymonth"
"""
Tier 4 engineered feature matrices at brand×month granularity (DVH EXCL. HD).

Was: _03_engineered_dvhexclhd/ before the P0028 restructure.

Example:
    from PATHS import THESIS_DATA_ENGINEERED_BYMONTH_DIR
    features = THESIS_DATA_ENGINEERED_BYMONTH_DIR / "CSD" / "csd_feature_matrix.parquet"
"""

# NOTE (P0035, 2026-08-01): THESIS_DATA_ENGINEERED_BYCHAIN_DIR was removed here.
# DEC-GRAIN (2026-07-12) locked the project grain to brand x month; the
# _03_engineered/bychain/ directory was deleted from disk, leaving this constant
# resolving to a non-existent path. Chain grain is now a documented limitation +
# future work, not a live code path.

# ============================================================================
# 1.2.1 RAW DATA TIER
# ============================================================================

THESIS_DATA_RAW_DIR: Path = THESIS_DATA_DIR / "_00_raw"
"""
Directory containing all raw source data (JSONL from Nielsen, CSV from SPSS, etc.).

This is Tier 1 of the 4-tier data hierarchy. Raw data is never modified;
it's the source of truth for all downstream processing.

Example:
    from PATHS import THESIS_DATA_RAW_DIR
    print(THESIS_DATA_RAW_DIR.resolve())  # C:\\dev\\thesis-manifold\\02_thesis_data\\_00_raw
"""

THESIS_DATA_RAW_NIELSEN_DIR: Path = THESIS_DATA_RAW_DIR / "nielsen"
"""
Directory containing Nielsen market research data exports (source format: JSONL).

Stores Nielsen Fabric data extracts used for market modelling, product category
information, and sales data. Data is organized in JSONL format by category
(CSD, Totalbeer, Energidrikke, Danskvand, RTD).

Example:
    from PATHS import THESIS_DATA_RAW_NIELSEN_DIR
    data = THESIS_DATA_RAW_NIELSEN_DIR / "data_jsonl" / "CSD" / "views" / "csd_clean_facts_v.jsonl"
"""

THESIS_DATA_RAW_NIELSEN_JSONL_DIR: Path = THESIS_DATA_RAW_NIELSEN_DIR / "data_jsonl"
"""
Directory containing Nielsen Fabric data exported as JSONL files (source format).

Primary source for all Nielsen data preprocessing. Data is organized hierarchically
by category (CSD, Totalbeer, Energidrikke, Danskvand, RTD) and type:
- views/: Cleaned, column-reduced tables from Nielsen Fabric
- raw/: Full tables with all columns and metadata
- metadata/: Schema documentation tables

JSONL format offers faster loading than CSV (no string escaping) and enables
streaming. Generated by thesis/data/raw/nielsen/scripts/save_all_datasets.py.
Files are directly queryable with pd.read_json(lines=True).

Example:
    from PATHS import THESIS_DATA_RAW_NIELSEN_JSONL_DIR
    facts = pd.read_json(THESIS_DATA_RAW_NIELSEN_JSONL_DIR / "CSD" / "views" / "csd_clean_facts_v.jsonl", lines=True)
    dims = pd.read_json(THESIS_DATA_RAW_NIELSEN_JSONL_DIR / "CSD" / "views" / "csd_clean_dim_market_v.jsonl", lines=True)
"""

THESIS_DATA_RAW_NIELSEN_DESC_DIR: Path = THESIS_DATA_RAW_NIELSEN_DIR / "description"
"""
Directory containing Nielsen schema documentation and snapshots (source format).

Stores metadata files including SCHEMA_SNAPSHOT.md which documents the Nielsen
Fabric database schema with object counts and row tallies. Generated by
thesis/data/raw/nielsen/scripts/save_all_datasets.py.

Example:
    from PATHS import THESIS_DATA_RAW_NIELSEN_DESC_DIR
    schema = (THESIS_DATA_RAW_NIELSEN_DESC_DIR / "SCHEMA_SNAPSHOT.md").read_text()
"""

# ============================================================================
# 1.2.2 CONVERTED DATA TIER (Stage 1 Cache)
# ============================================================================

THESIS_DATA_CONVERTED_DIR: Path = THESIS_DATA_DIR / "_01_converted"
"""
Directory containing converted/cached data in optimized formats (Parquet, etc.).

This is Tier 2 of the 4-tier data hierarchy. Converted data is the output of
Stage 1 conversion pipelines. It serves as cache for Stage 2 preprocessing scripts.

Example:
    from PATHS import THESIS_DATA_CONVERTED_DIR
    print(THESIS_DATA_CONVERTED_DIR.resolve())  # C:\\dev\\thesis-manifold\\02_thesis_data\\_01_converted
"""

THESIS_DATA_CONVERTED_NIELSEN_DIR: Path = THESIS_DATA_CONVERTED_DIR / "nielsen"
"""
Directory containing Nielsen data converted to Parquet format (Stage 1 cache).

Stores pre-processed, optimized Nielsen datasets organized by conversion type
(jsonl_to_parquet/) and by category within the parquet cache.

Example:
    from PATHS import THESIS_DATA_CONVERTED_NIELSEN_DIR
    print(THESIS_DATA_CONVERTED_NIELSEN_DIR.resolve())
"""

THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR: Path = THESIS_DATA_CONVERTED_NIELSEN_DIR / "parquet_nielsen"
"""
Directory containing Nielsen JSONL data converted to Parquet (Stage 1 cache).

Stores cached Parquet views, raw, and metadata tables—one subdirectory per
Nielsen category (CSD, Energidrikke, etc.). Generated by Stage 1 conversion
scripts in converted/nielsen/jsonl_to_parquet/.

Stage 2 feature engineering scripts read from this cache. Parquet format provides
efficient columnar access and compression for large Nielsen datasets.

Example:
    from PATHS import THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR
    views = pd.read_parquet(THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / "CSD" / "views" / "csd_clean_facts_v.parquet")
"""

# REMOVED 2026-09-06: the four Indeks Danmark / SPSS constants
# (THESIS_DATA_RAW_SPSS_DIR, THESIS_DATA_RAW_SPSS_CSV_DIR,
# THESIS_DATA_CONVERTED_SPSS_DIR, THESIS_DATA_CONVERTED_SPSS_PARQUET_DIR).
#
# The Indeks Danmark consumer-survey dataset was never used and will not be
# before submission. The source data is archived at
# .archive/spss_indeksdanmark_2026-09/ -- see its README, which also records the
# open item this creates: the thesis abstract still names Indeks Danmark as part
# of the empirical base, and that claim needs correcting in the .docx.
#
# Three of these four already resolved to non-existent directories before the
# archival; only the _00_raw folder ever materialised.

# ============================================================================
# HELPER FUNCTIONS — CATEGORY & TYPE-SPECIFIC PATHS
# ============================================================================

def get_category_parquet_dir(category: str) -> Path:
    """
    Get the base parquet directory for a Nielsen data category (Stage 1 cache).

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to converted/nielsen/parquet_nielsen/{category}/

    Example:
        >>> csd_dir = get_category_parquet_dir("CSD")
        >>> print(csd_dir)  # C:\\dev\\thesis-manifold\\02_thesis_data\\_01_converted\\nielsen\\parquet_nielsen\\CSD
    """
    return THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / category


def get_category_raw_dir(category: str) -> Path:
    """
    Get the raw tables directory for a Nielsen data category.

    Raw tables contain full data from Nielsen Fabric with all columns and metadata.

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to preprocessing/parquet_nielsen/{category}/raw/

    Example:
        >>> raw_dir = get_category_raw_dir("CSD")
        >>> facts = pd.read_parquet(raw_dir / "csd_clean_facts.parquet")
    """
    return get_category_parquet_dir(category) / "raw"


def get_category_source_jsonl_dir(category: str) -> Path:
    """
    Get the source JSONL views directory for a Nielsen data category (raw, source format).

    Views are cleaned, column-reduced tables from Nielsen Fabric (suffix _v in source).
    Contains JSONL files for raw data loading in Stage 1 conversion pipeline.

    This is the **source** directory for JSONL-to-Parquet conversion. Do NOT confuse
    with Parquet cache (which lives in converted/). This path contains the original
    JSONL export from Nielsen Fabric.

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to raw/nielsen/data_jsonl/{category}/views/

    Example:
        >>> views_dir = get_category_source_jsonl_dir("CSD")
        >>> facts = pd.read_json(views_dir / "csd_clean_facts_v.jsonl", lines=True)
    """
    return THESIS_DATA_RAW_NIELSEN_JSONL_DIR / category / "views"


def get_category_jsonl_views_dir(category: str) -> Path:
    """
    Deprecated: Use get_category_source_jsonl_dir() instead.

    This function is kept for backwards compatibility but redirects to the new
    naming convention which better reflects that the data is in raw/ tier (source format).
    """
    return get_category_source_jsonl_dir(category)


def get_category_views_dir(category: str) -> Path:
    """
    Get the views directory for a Nielsen data category (Stage 1 cache, Parquet format).

    Views are cleaned, column-reduced tables from Nielsen Fabric, cached in Parquet.
    Output of Stage 1 conversion pipeline; input to Stage 2 feature engineering.

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to converted/nielsen/parquet_nielsen/{category}/views/

    Example:
        >>> views_dir = get_category_views_dir("CSD")
        >>> facts = pd.read_parquet(views_dir / "csd_clean_facts_v.parquet")
        >>> dim_market = pd.read_parquet(views_dir / "csd_clean_dim_market_v.parquet")
    """
    return get_category_parquet_dir(category) / "views"


def get_category_metadata_dir(category: str) -> Path:
    """
    Get the metadata directory for a Nielsen data category (Stage 1 cache, Parquet format).

    Metadata contains schema documentation (column names, types, descriptions, null semantics)
    from Nielsen's metadata tables, cached in Parquet.

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to converted/nielsen/parquet_nielsen/{category}/metadata/

    Example:
        >>> metadata_dir = get_category_metadata_dir("CSD")
        >>> schema = pd.read_parquet(metadata_dir / "metadata_csd_columns.parquet")
    """
    return get_category_parquet_dir(category) / "metadata"


def get_category_engineered_bymonth_dir(category: str) -> Path:
    """
    Get the engineered features directory for a Nielsen data category at
    brand×month granularity (Tier 4 output, DVH EXCL. HD).

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to _03_engineered/bymonth/{category}/

    Example:
        >>> eng_dir = get_category_engineered_bymonth_dir("CSD")
        >>> features = pd.read_parquet(eng_dir / "csd_feature_matrix.parquet")
        >>> split_dates = json.load(open(eng_dir / "csd_split_dates.json"))
    """
    return THESIS_DATA_ENGINEERED_BYMONTH_DIR / category


# NOTE (P0035, 2026-08-01): get_category_engineered_bychain_dir() and the
# deprecated get_category_engineered_dir() alias were removed here. See the
# note at THESIS_DATA_ENGINEERED_BYCHAIN_DIR's former location above.
# Call get_category_engineered_bymonth_dir() explicitly instead.


def get_category_preprocessing_scripts_dir(category: str) -> Path:
    """
    Get the directory containing per-step preprocessing scripts (pre_{category}_0.py
    through pre_{category}_6.py, plus the EDA notebook/script) for a Nielsen category.

    The orchestrator (preprocessing_{category}.py) and the generated
    {category}_preprocessing_report.md stay one level up, at
    THESIS_DATA_PREPROCESSING_DIR / "nielsen" / {category}/ — this function returns
    the step-scripts subfolder they call into, not the orchestrator's own location.

    CSD was regrouped (2026-07-13) into a "pipeline_step_scripts/" subfolder one
    level below the orchestrator, so its step scripts are one level deeper than
    the other categories. Danskvand/Energidrikke/RTD have not been regrouped yet
    and still keep their step scripts flat alongside their orchestrator — this
    function returns the correct directory for both layouts without callers
    needing to know which one a given category uses.

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to thesis/data/preprocessing/nielsen/{category}/ (flat layout), or
        thesis/data/preprocessing/nielsen/{category}/pipeline_step_scripts/ (CSD, regrouped)

    Example:
        >>> scripts_dir = get_category_preprocessing_scripts_dir("CSD")
        >>> step_script = scripts_dir / "pre_csd_1_load_and_aggregate.py"
        >>> orchestrator = get_category_preprocessing_dir("CSD") / "preprocessing_csd.py"
    """
    base_dir = THESIS_DATA_PREPROCESSING_DIR / "nielsen" / category
    regrouped_dir = base_dir / "pipeline_step_scripts"
    if regrouped_dir.is_dir():
        return regrouped_dir
    return base_dir


def get_category_preprocessing_dir(category: str) -> Path:
    """
    Get the top-level preprocessing directory for a Nielsen category — where the
    orchestrator (preprocessing_{category}.py) and the generated
    {category}_preprocessing_report.md live, regardless of whether that
    category's step scripts have been regrouped into a "pipeline_step_scripts/"
    subfolder (see get_category_preprocessing_scripts_dir()).

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to thesis/data/preprocessing/nielsen/{category}/

    Example:
        >>> cat_dir = get_category_preprocessing_dir("CSD")
        >>> orchestrator = cat_dir / "preprocessing_csd.py"
        >>> report = cat_dir / "csd_preprocessing_report.md"
    """
    return THESIS_DATA_PREPROCESSING_DIR / "nielsen" / category


def get_category_pipeline_step_outputs_dir(category: str) -> Path:
    """
    Get the directory for pipeline step intermediate outputs.

    Each step (0-6) saves its output parquet file and timing log here.
    Serves as checkpoints for resumption and step-to-step data passing.

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to thesis/data/preprocessing/nielsen/{category}/pipeline_step_outputs/

    Example:
        >>> outputs_dir = get_category_pipeline_step_outputs_dir("CSD")
        >>> step1_output = pd.read_parquet(outputs_dir / "step_1_aggregate_bymonth.parquet")
        >>> step_timing = json.load(open(outputs_dir / "step_1_log.json"))
    """
    return THESIS_DATA_PREPROCESSING_DIR / "nielsen" / category / "pipeline_step_outputs"


# ---------------------------------------------------------------------------
# Per-SRQ result subdirectories (P0046 Phase 3b, 2026-09-06)
# ---------------------------------------------------------------------------
# Each SRQ results folder has the same three-way shape, so a reader who learns
# one folder can navigate all of them:
#
#     srq{N}_{slug}/
#         figures/   .png / .svg -- paste into the thesis
#         tables/    .csv + .md twins -- .md to paste, .csv to trace back
#         models/    serialised estimators + the hyperparameters defining them
#
# There is deliberately no raw/: per DEC-P0046-RUNS-WITH-EXPERIMENT raw per-run
# material stays with the experiment that produced it and never reaches the
# results tier, which holds only what could enter the thesis.
#
# The .csv/.md pair is ONE artefact in two formats, which is why the split is by
# role rather than by file extension -- splitting on extension would separate
# `calibration.md` from the `calibration.csv` it was rendered from.

def get_chapter_results_dir(slug: str) -> Path:
    """The results folder for one thesis chapter.

    Args:
        slug: one of CHAPTER_SLUGS, e.g. "data_assessment".

    Returns:
        Path to 05_thesis_results/{NN}_{slug}/, where NN is the chapter's
        position in CHAPTER_SLUGS -- so the tree sorts in reading order.

    The number is DERIVED, never typed. Reordering CHAPTER_SLUGS renumbers the
    folders on the next run; nothing else references a number, so a reorder
    cannot leave a folder claiming a position it no longer holds.

    Raises on an unknown slug rather than silently creating a stray folder --
    a typo would otherwise produce a directory nobody looks in, which is how
    artefacts go missing.

    Example:
        >>> get_chapter_results_dir("model_benchmark")
        .../05_thesis_results/05_model_benchmark
    """
    if slug not in CHAPTER_ORDER:
        raise ValueError(
            f"Unknown chapter slug {slug!r}; expected one of {list(CHAPTER_SLUGS)}")
    return THESIS_RESULTS_DIR / _chapter_folder(slug)


def get_chapter_figures_dir(slug: str) -> Path:
    """Figures for a chapter -- .svg to paste into the document."""
    d = get_chapter_results_dir(slug) / "figures"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_chapter_tables_dir(slug: str) -> Path:
    """Tables for a chapter -- .csv data plus their rendered .md twins."""
    d = get_chapter_results_dir(slug) / "tables"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_chapter_models_dir(slug: str) -> Path:
    """Serialised estimators + hyperparameters, for chapters that train."""
    d = get_chapter_results_dir(slug) / "models"
    d.mkdir(parents=True, exist_ok=True)
    return d


# SRQ -> chapter, for the get_srq_*_dir() helpers below.
#
# This is the hinge of DEC-CHAPTER-FOLDERS: ~25 producer scripts already reach
# the results tier through these three helpers, so repointing the helpers moves
# their output without touching the scripts. A script asks for "somewhere to put
# SRQ1's tables"; where that is, is this file's decision, not the script's.
#
# SRQ3 has no results of its own -- integration readiness is argued in the
# discussion from evidence the other chapters produce.
_SRQ_CHAPTER: dict = {
    1: "model_benchmark",          # Ch6: the benchmark and selection
    2: "decision_synthesis",       # Ch7: the tool interface in use
    3: "discussion",               # Ch9: readiness is assessed, not measured
    4: "experimental_evaluation",  # Ch8: the scenario comparison
}


def get_srq_figures_dir(srq: int) -> Path:
    """Figures for an SRQ, filed under the chapter that discusses them.

    Example:
        >>> get_srq_figures_dir(1)   # .../05_thesis_results/model_benchmark/figures
    """
    return get_chapter_figures_dir(_srq_chapter(srq))


def get_srq_tables_dir(srq: int) -> Path:
    """Tables for an SRQ -- .csv data plus their rendered .md twins."""
    return get_chapter_tables_dir(_srq_chapter(srq))


def get_srq_models_dir(srq: int) -> Path:
    """Serialised models + hyperparameter files for an SRQ."""
    return get_chapter_models_dir(_srq_chapter(srq))


def _srq_chapter(srq: int) -> str:
    """The chapter slug an SRQ's artefacts belong to."""
    if srq not in _SRQ_CHAPTER:
        raise ValueError(f"Unknown SRQ {srq!r}; expected one of {sorted(_SRQ_CHAPTER)}")
    return _SRQ_CHAPTER[srq]


def get_srq_results_dir(srq: int) -> Path:
    """
    Get the results directory for an SRQ by number.

    Args:
        srq: 1, 2, 3 or 4.

    Returns:
        Path to 05_thesis_results/srq{N}_{slug}/

    Example:
        >>> get_srq_results_dir(1)   # .../05_thesis_results/srq1_model_performance
    """
    mapping = {
        1: THESIS_RESULTS_SRQ1_DIR,
        2: THESIS_RESULTS_SRQ2_DIR,
        3: THESIS_RESULTS_SRQ3_DIR,
        4: THESIS_RESULTS_SRQ4_DIR,
    }
    if srq not in mapping:
        raise ValueError(f"Unknown SRQ {srq!r}; expected one of {sorted(mapping)}")
    return mapping[srq]


def get_category_eda_plots_dir(category: str) -> Path:
    """
    Get the pipeline's EDA plot directory for a Nielsen category (~8 PNGs).

    This is where the pipeline WRITES them. Plots promoted as thesis candidates
    are copied to get_category_eda_results_dir(category) / "plots" — see
    DEC-P0046-EDA-SPLIT.

    Example:
        >>> get_category_eda_plots_dir("CSD")   # .../pipeline_step_outputs/csd_eda_plots
    """
    return (get_category_pipeline_step_outputs_dir(category)
            / f"{category.lower()}_eda_plots")


def get_category_eda_tables_dir(category: str) -> Path:
    """
    Get the pipeline's EDA markdown-table directory for a Nielsen category (~30 .md).

    Example:
        >>> get_category_eda_tables_dir("CSD")  # .../pipeline_step_outputs/csd_eda_tables
    """
    return (get_category_pipeline_step_outputs_dir(category)
            / f"{category.lower()}_eda_tables")


def get_category_eda_results_dir(category: str) -> Path:
    """
    Get the results-tier home for a category's promoted EDA artefacts.

    Per DEC-P0046-EDA-SPLIT the .csv step outputs stay in the pipeline (later EDA
    steps consume them); the .md tables and .png plots are report material and
    are promoted here.

    Example:
        >>> get_category_eda_results_dir("CSD")  # .../05_thesis_results/eda/CSD
    """
    return THESIS_RESULTS_EDA_DIR / category


# ============================================================================
# DEBUG PATH VERIFICATION
# ============================================================================

def print_all_paths(verbose: bool = True) -> None:
    """
    Print all configured paths for verification.

    Usage:
        from PATHS import print_all_paths
        print_all_paths()

    Args:
        verbose: If True, print all paths. If False, print only key paths.
    """
    if verbose:
        print("\n=== ALL PROJECT PATHS ===")
        print(f"ROOT_DIR: {ROOT_DIR.resolve()}")
        print(f"THESIS_DIR (alias of ROOT_DIR): {THESIS_DIR.resolve()}")
        print(f"THESIS_CONTEXT_DIR: {THESIS_CONTEXT_DIR.resolve()}")
        print(f"THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR: {THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR.resolve()}")
        print(f"SRQ1_DIR: {SRQ1_DIR.resolve()}")
        print(f"SRQ2_DIR: {SRQ2_DIR.resolve()}")
        print(f"SRQ3_DIR: {SRQ3_DIR.resolve()}")
        print(f"SRQ4_DIR: {SRQ4_DIR.resolve()}")
        print(f"SRQ4_SCENARIO_SETUP_DIR: {SRQ4_SCENARIO_SETUP_DIR.resolve()}")
        print(f"THESIS_MODELLING_DIR: {THESIS_MODELLING_DIR.resolve()}")
        print(f"THESIS_MODELLING_TRAINING_DIR: {THESIS_MODELLING_TRAINING_DIR.resolve()}")
        print(f"THESIS_MODELLING_SCENARIO_DIR: {THESIS_MODELLING_SCENARIO_DIR.resolve()}")
        print(f"THESIS_MODELLING_ARCHIVE_DIR: {THESIS_MODELLING_ARCHIVE_DIR.resolve()}")
        print(f"THESIS_DATA_DIR: {THESIS_DATA_DIR.resolve()}")
        print(f"THESIS_DATA_PREPROCESSING_DIR: {THESIS_DATA_PREPROCESSING_DIR.resolve()}")
        print(f"THESIS_DATA_ENGINEERED_DIR: {THESIS_DATA_ENGINEERED_DIR.resolve()}")
        print(f"THESIS_DATA_ENGINEERED_BYMONTH_DIR: {THESIS_DATA_ENGINEERED_BYMONTH_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_DIR: {THESIS_DATA_RAW_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_NIELSEN_DIR: {THESIS_DATA_RAW_NIELSEN_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_NIELSEN_JSONL_DIR: {THESIS_DATA_RAW_NIELSEN_JSONL_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_NIELSEN_DESC_DIR: {THESIS_DATA_RAW_NIELSEN_DESC_DIR.resolve()}")
        print(f"THESIS_DATA_CONVERTED_DIR: {THESIS_DATA_CONVERTED_DIR.resolve()}")
        print(f"THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR: {THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR.resolve()}")
        print(f"THESIS_RESULTS_DIR: {THESIS_RESULTS_DIR.resolve()}")
        print(f"THESIS_RESULTS_SRQ1_DIR: {THESIS_RESULTS_SRQ1_DIR.resolve()}")
        print(f"THESIS_RESULTS_SRQ2_DIR: {THESIS_RESULTS_SRQ2_DIR.resolve()}")
        print(f"THESIS_RESULTS_SRQ3_DIR: {THESIS_RESULTS_SRQ3_DIR.resolve()}")
        print(f"THESIS_RESULTS_SRQ4_DIR: {THESIS_RESULTS_SRQ4_DIR.resolve()}")
        print(f"THESIS_RESULTS_EDA_DIR: {THESIS_RESULTS_EDA_DIR.resolve()}")
        print(f"THESIS_WRITING_DIR: {THESIS_WRITING_DIR.resolve()}\n")
    else:
        print("\n=== KEY PROJECT PATHS ===")
        print(f"ROOT_DIR: {ROOT_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_NIELSEN_JSONL_DIR: {THESIS_DATA_RAW_NIELSEN_JSONL_DIR.resolve()}")
        print(f"THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR: {THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR.resolve()}\n")

if DEBUG:
    print_all_paths(verbose=True)
