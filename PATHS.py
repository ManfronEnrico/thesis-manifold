"""
Project Paths Configuration

Centralizes all path definitions for the thesis project using pathlib.Path for
cross-platform compatibility. Paths are organized hierarchically from root
directory down through subdirectories.

Each path variable includes type hints and docstrings to provide context on
hover in your IDE. Use these constants throughout notebooks and scripts
instead of hardcoded strings.

Reference: PATHS_markdown.ipynb for detailed documentation with examples.
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

THESIS_DIR: Path = ROOT_DIR / "thesis"
"""
Main thesis folder containing all modelling, data, and related files.

This is the central hub for all thesis-related work including computational
modelling, datasets, figures, and model outputs. It is subdivided into
'modelling' and 'data' subdirectories for organizational clarity.

Example:
    from PATHS import THESIS_DIR
    print(THESIS_DIR.resolve())  # C:\\dev\\thesis-manifold\\thesis
"""

# ============================================================================
# 1.1 MODELLING SUBDIRECTORY
# ============================================================================

THESIS_MODELLING_DIR: Path = THESIS_DIR / "modelling"
"""
Directory containing all computational modelling work, notebooks, outputs, and figures.

This folder holds all Jupyter notebooks, generated figures, prompt configurations,
and modelling outputs organized by research question and category. It serves as
the hub for all computational and analytical work on the thesis.

Example:
    from PATHS import THESIS_MODELLING_DIR
    print(THESIS_MODELLING_DIR.resolve())  # C:\\dev\\thesis-manifold\\thesis\\modelling
"""

THESIS_MODELLING_NOTEBOOKS_DIR: Path = THESIS_MODELLING_DIR / "notebooks"
"""
Directory containing all Jupyter notebooks for modelling work.

Houses notebooks organized by research question (SRQ_1, SRQ_2, etc.) and
modelling type. Each notebook contains code, exploration, and results for
specific analytical tasks.

Example:
    from PATHS import THESIS_MODELLING_NOTEBOOKS_DIR
    notebook_path = THESIS_MODELLING_NOTEBOOKS_DIR / "SRQ_1" / "modelling.ipynb"
"""

THESIS_MODELLING_PROMPTS_DIR: Path = THESIS_MODELLING_DIR / "prompts"
"""
Directory containing prompt templates and configurations.

Stores reusable prompts for system interactions, model queries, and other
computational tasks used across the thesis modelling.

Example:
    from PATHS import THESIS_MODELLING_PROMPTS_DIR
    prompts_file = THESIS_MODELLING_PROMPTS_DIR / "system_prompts.json"
"""

# ============================================================================
# 1.2 DATA SUBDIRECTORY
# ============================================================================

THESIS_DATA_DIR: Path = THESIS_DIR / "data"
"""
Directory containing all datasets, raw data sources, and preprocessing scripts.

Organized by data source (Nielsen, Indeks Danmark, assessment data) and
processing stage. This is the hub for all data management related to the
thesis research.

Example:
    from PATHS import THESIS_DATA_DIR
    print(THESIS_DATA_DIR.resolve())  # C:\\dev\\thesis-manifold\\thesis\\data
"""

THESIS_DATA_ASSESSMENT_DIR: Path = THESIS_DATA_DIR / "assessment"
"""
Directory containing human evaluation and assessment data.

Stores evaluation results, annotations, and assessment data used for
validating model predictions and analyzing system performance in the
thesis research.

Example:
    from PATHS import THESIS_DATA_ASSESSMENT_DIR
    assessments = THESIS_DATA_ASSESSMENT_DIR / "human_eval.csv"
"""


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
Organized by source (Nielsen, etc.) and category (CSD, Danskvand, etc.).

Example:
    from PATHS import THESIS_DATA_ENGINEERED_DIR
    features = THESIS_DATA_ENGINEERED_DIR / "nielsen" / "CSD" / "csd_feature_matrix.parquet"
"""

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
    print(THESIS_DATA_RAW_DIR.resolve())  # C:\\dev\\thesis-manifold\\thesis\\data\\_00_raw
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
    print(THESIS_DATA_CONVERTED_DIR.resolve())  # C:\\dev\\thesis-manifold\\thesis\\data\\_01_converted
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

# ============================================================================
# 1.2.3 INDEKS DANMARK SPSS DATA (RAW + CONVERTED)
# ============================================================================

THESIS_DATA_RAW_SPSS_DIR: Path = THESIS_DATA_RAW_DIR / "spss_indeksdanmark"
"""
Directory containing Indeks Danmark SPSS data files (source format).

Parent directory for SPSS data exports from Indeks Danmark used for consumer
behavior modelling and market insights in the thesis research.

Example:
    from PATHS import THESIS_DATA_RAW_SPSS_DIR
    data = THESIS_DATA_RAW_SPSS_DIR / "indeks_danmark.sav"
"""

THESIS_DATA_RAW_SPSS_CSV_DIR: Path = THESIS_DATA_RAW_SPSS_DIR / "data_csv"
"""
Directory containing Indeks Danmark SPSS data exported as CSV files (source format).

Stores CSV exports from Indeks Danmark SPSS data (indeks_danmark_*.csv files).
These are generated by data export scripts and serve as the source for
SPSS-based data preprocessing and analysis pipelines.

Files are directly queryable with pd.read_csv() and provide accessible
format for data transformation and feature engineering.

Example:
    from PATHS import THESIS_DATA_RAW_SPSS_CSV_DIR
    df = pd.read_csv(THESIS_DATA_RAW_SPSS_CSV_DIR / "indeks_danmark.csv")
"""

THESIS_DATA_CONVERTED_SPSS_DIR: Path = THESIS_DATA_CONVERTED_DIR / "spss_indeksdanmark"
"""
Directory containing Indeks Danmark SPSS data converted to Parquet format (Stage 1 cache).

Placeholder for future SPSS-to-Parquet conversion pipeline. Currently empty.

Example:
    from PATHS import THESIS_DATA_CONVERTED_SPSS_DIR
    print(THESIS_DATA_CONVERTED_SPSS_DIR.resolve())
"""

THESIS_DATA_CONVERTED_SPSS_PARQUET_DIR: Path = THESIS_DATA_CONVERTED_SPSS_DIR / "parquet_spss"
"""
Directory containing Indeks Danmark SPSS data converted to Parquet format (Stage 1 cache).

Stores pre-processed, optimized Indeks Danmark datasets converted from CSV
or SPSS format to columnar Parquet format for efficient loading in notebooks.

All analysis notebooks that use Indeks Danmark data load processed datasets
from this directory.

Format: indeks_danmark_*.parquet

Example:
    from PATHS import THESIS_DATA_CONVERTED_SPSS_PARQUET_DIR
    df = pd.read_parquet(THESIS_DATA_CONVERTED_SPSS_PARQUET_DIR / "indeks_danmark_features.parquet")
"""

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
        >>> print(csd_dir)  # C:\\dev\\thesis-manifold\\thesis\\data\\converted\\nielsen\\parquet_nielsen\\CSD
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


def get_category_engineered_dir(category: str) -> Path:
    """
    Get the engineered features directory for a Nielsen data category (Tier 4 output).

    Contains final outputs from the preprocessing pipeline: feature matrices, series indices,
    split boundaries, and preprocessing reports. This is Tier 4 (engineered outputs),
    separate from Tier 3 (preprocessing scripts) and Tier 2 (converted cache).

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to _03_engineered/nielsen/{category}/

    Example:
        >>> eng_dir = get_category_engineered_dir("CSD")
        >>> features = pd.read_parquet(eng_dir / "csd_feature_matrix.parquet")
        >>> split_dates = json.load(open(eng_dir / "csd_split_dates.json"))
    """
    return THESIS_DATA_ENGINEERED_DIR / "nielsen" / category


def get_category_preprocessing_scripts_dir(category: str) -> Path:
    """
    Get the directory containing preprocessing scripts for a Nielsen category.

    Preprocessing scripts (pre_{category}_0.py through pre_{category}_6.py) and
    the orchestrator (preprocessing_{category}.py) live in this directory.

    Args:
        category: Category name (e.g., "CSD", "Danskvand", "Energidrikke", "RTD", "Totalbeer")

    Returns:
        Path to thesis/data/preprocessing/nielsen/{category}/

    Example:
        >>> scripts_dir = get_category_preprocessing_scripts_dir("CSD")
        >>> orchestrator = scripts_dir / "preprocessing_csd.py"
        >>> step_script = scripts_dir / "pre_csd_1_load_and_aggregate.py"
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
        >>> step1_output = pd.read_parquet(outputs_dir / "step_1_aggregate.parquet")
        >>> step_timing = json.load(open(outputs_dir / "step_1_log.json"))
    """
    return THESIS_DATA_PREPROCESSING_DIR / "nielsen" / category / "pipeline_step_outputs"


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
        print(f"THESIS_DIR: {THESIS_DIR.resolve()}")
        print(f"THESIS_MODELLING_DIR: {THESIS_MODELLING_DIR.resolve()}")
        print(f"THESIS_MODELLING_NOTEBOOKS_DIR: {THESIS_MODELLING_NOTEBOOKS_DIR.resolve()}")
        print(f"THESIS_MODELLING_PROMPTS_DIR: {THESIS_MODELLING_PROMPTS_DIR.resolve()}")
        print(f"THESIS_DATA_DIR: {THESIS_DATA_DIR.resolve()}")
        print(f"THESIS_DATA_ASSESSMENT_DIR: {THESIS_DATA_ASSESSMENT_DIR.resolve()}")
        print(f"THESIS_DATA_PREPROCESSING_DIR: {THESIS_DATA_PREPROCESSING_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_DIR: {THESIS_DATA_RAW_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_NIELSEN_DIR: {THESIS_DATA_RAW_NIELSEN_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_NIELSEN_JSONL_DIR: {THESIS_DATA_RAW_NIELSEN_JSONL_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_NIELSEN_DESC_DIR: {THESIS_DATA_RAW_NIELSEN_DESC_DIR.resolve()}")
        print(f"THESIS_DATA_CONVERTED_DIR: {THESIS_DATA_CONVERTED_DIR.resolve()}")
        print(f"THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR: {THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_SPSS_DIR: {THESIS_DATA_RAW_SPSS_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_SPSS_CSV_DIR: {THESIS_DATA_RAW_SPSS_CSV_DIR.resolve()}")
        print(f"THESIS_DATA_CONVERTED_SPSS_PARQUET_DIR: {THESIS_DATA_CONVERTED_SPSS_PARQUET_DIR.resolve()}\n")
    else:
        print("\n=== KEY PROJECT PATHS ===")
        print(f"ROOT_DIR: {ROOT_DIR.resolve()}")
        print(f"THESIS_DATA_RAW_NIELSEN_JSONL_DIR: {THESIS_DATA_RAW_NIELSEN_JSONL_DIR.resolve()}")
        print(f"THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR: {THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR.resolve()}\n")

if DEBUG:
    print_all_paths(verbose=True)
