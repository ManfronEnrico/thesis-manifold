# %%
# Import necessary libraries
from pathlib import Path
from IPython.display import Markdown, display

# %%
# PROJECT PATHS CONFIGURATION
Markdown(
"""
# Configuration: Project Paths

This file centralizes all path definitions for the thesis project using pathlib.Path for cross-platform
compatibility. Paths are organized hierarchically from root directory down through subdirectories.

Each path variable includes type hints and docstrings to provide context on hover in your IDE.
Use these constants throughout notebooks instead of hardcoded strings.
""")

# %%
# 0. ROOT REPOSITORY
Markdown(
"""
## 0. Root Repository

The root directory is the base folder of the project, containing all subfolders and files related to the thesis.
This is where the main paths configuration file (paths.py) is located, which defines paths to all other
important directories and files used in the project. Using pathlib.Path ensures cross-platform compatibility
across Windows, macOS, and Linux systems.
""")

# %%
ROOT_DIR: Path = Path(__file__).parent
"""
Base folder of the thesis project containing all subfolders and files.

This is the root directory where paths.py is located. All other paths in the project
are defined relative to ROOT_DIR for cross-platform compatibility across Windows, macOS,
and Linux. When referenced in notebooks, use ROOT_DIR.resolve() to get the absolute path.

Example:
    from paths import ROOT_DIR
    print(ROOT_DIR.resolve())  # C:\\dev\\thesis-manifold
"""
print(f"ROOT_DIR = {ROOT_DIR.resolve()}")

# %%
# 1. THESIS DIRECTORY
Markdown(
"""
## 1. Thesis Directory

The thesis folder serves as the central hub for all thesis-related work. It contains subdirectories for modelling
(notebooks, figures, outputs) and data (raw datasets, preprocessing scripts, assessment data). All paths within
this section are relative to THESIS_DIR.
""")

# %%
THESIS_DIR: Path = ROOT_DIR / "thesis"
"""
Main thesis folder containing all modelling, data, and related files.

This is the central hub for all thesis-related work including computational modelling,
datasets, figures, and model outputs. It is subdivided into 'modelling' and 'data'
subdirectories for organizational clarity.

Example:
    from paths import THESIS_DIR
    print(THESIS_DIR.resolve())  # C:\\dev\\thesis-manifold\\thesis
"""
print(f"THESIS_DIR = {THESIS_DIR.resolve()}")


# %%
Markdown(
"""
## 1.1 Modelling Subdirectory

The modelling folder contains all notebooks, figures, prompts, and output files generated during the thesis work.
This is where computational modelling, visualizations, and model outputs are stored and organized by category.
""")

# %%
THESIS_MODELLING_DIR: Path = THESIS_DIR / "modelling"
"""
Directory containing all computational modelling work, notebooks, outputs, and figures.

This folder holds all Jupyter notebooks, generated figures, prompt configurations,
and modelling outputs organized by research question and category. It serves as the
hub for all computational and analytical work on the thesis.

Example:
    from paths import THESIS_MODELLING_DIR
    print(THESIS_MODELLING_DIR.resolve())  # C:\\dev\\thesis-manifold\\thesis\\modelling
"""
print(f"THESIS_MODELLING_DIR = {THESIS_MODELLING_DIR.resolve()}")

# %%


# %%
Markdown(
"""
## 1.1.1 Modelling Sub-Subdirectories

The modelling directory is further organized into specific subdirectories for different types of outputs:
- **notebooks**: Jupyter notebooks containing modelling code and results
- **prompts**: Prompt templates and configurations for system interactions
""")

# %%
THESIS_MODELLING_NOTEBOOKS_DIR: Path = THESIS_MODELLING_DIR / "notebooks"
"""
Directory containing all Jupyter notebooks for modelling work.

Houses notebooks organized by research question (SRQ_1, SRQ_2, etc.) and modelling type.
Each notebook contains code, exploration, and results for specific analytical tasks.

Example:
    from paths import THESIS_MODELLING_NOTEBOOKS_DIR
    notebook_path = THESIS_MODELLING_NOTEBOOKS_DIR / "SRQ_1" / "modelling.ipynb"
"""
print(f"THESIS_MODELLING_NOTEBOOKS_DIR = {THESIS_MODELLING_NOTEBOOKS_DIR.resolve()}")

# %%
THESIS_MODELLING_PROMPTS_DIR: Path = THESIS_MODELLING_DIR / "prompts"
"""
Directory containing prompt templates and configurations.

Stores reusable prompts for system interactions, model queries, and other
computational tasks used across the thesis modelling.

Example:
    from paths import THESIS_MODELLING_PROMPTS_DIR
    prompts_file = THESIS_MODELLING_PROMPTS_DIR / "system_prompts.json"
"""
print(f"THESIS_MODELLING_PROMPTS_DIR = {THESIS_MODELLING_PROMPTS_DIR.resolve()}")


# %%
Markdown(
"""
## 1.2 Data Subdirectory

The data folder contains all datasets, raw data sources, and preprocessing scripts. It is organized into
subdirectories for different data sources and processing stages.
""")

# %%
THESIS_DATA_DIR: Path = THESIS_DIR / "data"
"""
Directory containing all datasets, raw data sources, and preprocessing scripts.

Organized by data source (Nielsen, Indeks Danmark, assessment data) and processing stage.
This is the hub for all data management related to the thesis research.

Example:
    from paths import THESIS_DATA_DIR
    print(THESIS_DATA_DIR.resolve())  # C:\\dev\\thesis-manifold\\thesis\\data
"""
print(f"THESIS_DATA_DIR = {THESIS_DATA_DIR.resolve()}")

# %%
Markdown("""
## 1.2.1 Data Sub-Subdirectories

The data directory is further organized into specific subdirectories for different data sources:
- **assessment**: Human evaluation and assessment data
- **nielsen**: Nielsen market research data exports
- **preprocessing**: Data preprocessing scripts and intermediate files
- **spss_indeksdanmark**: Indeks Danmark SPSS data files
""")

# %%
THESIS_DATA_ASSESSMENT_DIR: Path = THESIS_DATA_DIR / "assessment"
"""
Directory containing human evaluation and assessment data.

Stores evaluation results, annotations, and assessment data used for validating
model predictions and analyzing system performance in the thesis research.

Example:
    from paths import THESIS_DATA_ASSESSMENT_DIR
    assessments = THESIS_DATA_ASSESSMENT_DIR / "human_eval.csv"
"""
print(f"THESIS_DATA_ASSESSMENT_DIR = {THESIS_DATA_ASSESSMENT_DIR.resolve()}")


# %%
THESIS_DATA_PREPROCESSING_DIR: Path = THESIS_DATA_DIR / "preprocessing"
"""
Directory for data preprocessing scripts and intermediate files.

Contains Python scripts, notebooks, and intermediate data files used for
cleaning, transforming, and preparing raw data for modelling.

Example:
    from paths import THESIS_DATA_PREPROCESSING_DIR
    script = THESIS_DATA_PREPROCESSING_DIR / "clean_data.py"
"""
print(f"THESIS_DATA_PREPROCESSING_DIR = {THESIS_DATA_PREPROCESSING_DIR.resolve()}")



# %%
Markdown(
"""
### 1.2.1.1 nielsen
"""
)


# %%
THESIS_DATA_NIELSEN_DIR: Path = THESIS_DATA_DIR / "raw_nielsen"
"""
Directory containing Nielsen market research data exports.

Stores Nielsen data extracts and processed files used for market modelling,
product category information, and sales data in the thesis research.

Example:
    from paths import THESIS_DATA_NIELSEN_DIR
    data = THESIS_DATA_NIELSEN_DIR / "data_csv" / "csd_clean_facts_v.csv"
"""
print(f"THESIS_DATA_NIELSEN_DIR = {THESIS_DATA_NIELSEN_DIR.resolve()}")


# %%
THESIS_DATA_NIELSEN_CSV_DIR: Path = THESIS_DATA_NIELSEN_DIR / "data_csv"
"""
Directory containing raw Nielsen data exported as CSV files.

Stores CSV exports from Nielsen Fabric warehouse (csd_clean_dim_*.csv,
csd_clean_facts_v.csv, etc.) and category-specific metadata. These are
generated by thesis/data/nielsen/scripts/save_all_datasets.py.

Files are directly queryable with pd.read_csv() and serve as the source
for data preprocessing pipelines.

Example:
    from paths import THESIS_DATA_NIELSEN_CSV_DIR
    df = pd.read_csv(THESIS_DATA_NIELSEN_CSV_DIR / "csd_clean_facts_v.csv")
"""
print(f"THESIS_DATA_NIELSEN_CSV_DIR = {THESIS_DATA_NIELSEN_CSV_DIR.resolve()}")


# %%
THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR: Path = THESIS_DATA_PREPROCESSING_DIR / "parquet_nielsen"
"""
Directory containing Nielsen data converted to Parquet format.

Stores pre-processed, optimized Nielsen datasets (one parquet per category +
combined feature matrices). Generated by preprocessing scripts that convert
raw CSVs to columnar Parquet format for efficient loading in notebooks.

All specialized notebooks (specialized_CSD.ipynb, specialized_danskvand.ipynb, etc.)
and aggregation notebooks load feature matrices from this directory.

Format: specialized_{category}_feature_matrix.parquet

Example:
    from paths import THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR
    df = pd.read_parquet(THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR / "specialized_CSD_feature_matrix.parquet")
"""
print(f"THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR = {THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR.resolve()}")


# %%
Markdown(
"""
### 1.2.1.2 spss_indeksdanmark
"""
)

# %%
THESIS_DATA_SPSS_DIR: Path = THESIS_DATA_DIR / "raw_spss_indeksdanmark"
"""
Directory containing Indeks Danmark SPSS data files and converted formats.

Parent directory for SPSS data exports from Indeks Danmark used for consumer behavior modelling
and market insights in the thesis research.

Example:
    from paths import THESIS_DATA_SPSS_DIR
    data = THESIS_DATA_SPSS_DIR / "indeks_danmark.sav"
"""
print(f"THESIS_DATA_SPSS_DIR = {THESIS_DATA_SPSS_DIR.resolve()}")


# %%
THESIS_DATA_SPSS_CSV_DIR: Path = THESIS_DATA_SPSS_DIR / "data_csv"
"""
Directory containing Indeks Danmark SPSS data exported as CSV files.

Stores CSV exports from Indeks Danmark SPSS data (indeks_danmark_*.csv files).
These are generated by data export scripts and serve as the source for SPSS-based
data preprocessing and analysis pipelines.

Files are directly queryable with pd.read_csv() and provide accessible format
for data transformation and feature engineering.

Example:
    from paths import THESIS_DATA_SPSS_CSV_DIR
    df = pd.read_csv(THESIS_DATA_SPSS_CSV_DIR / "indeks_danmark.csv")
"""
print(f"THESIS_DATA_SPSS_CSV_DIR = {THESIS_DATA_SPSS_CSV_DIR.resolve()}")


# %%
THESIS_DATA_PREPROCESSING_PARQUET_SPSS_DIR: Path = THESIS_DATA_PREPROCESSING_DIR / "parquet_spss"
"""
Directory containing Indeks Danmark SPSS data converted to Parquet format.

Stores pre-processed, optimized Indeks Danmark datasets converted from CSV or SPSS format
to columnar Parquet format for efficient loading in notebooks.

All analysis notebooks that use Indeks Danmark data load processed datasets from this directory.

Format: indeks_danmark_*.parquet

Example:
    from paths import THESIS_DATA_PREPROCESSING_PARQUET_SPSS_DIR
    df = pd.read_parquet(THESIS_DATA_PREPROCESSING_PARQUET_SPSS_DIR / "indeks_danmark_features.parquet")
"""
print(f"THESIS_DATA_PREPROCESSING_PARQUET_SPSS_DIR = {THESIS_DATA_PREPROCESSING_PARQUET_SPSS_DIR.resolve()}")