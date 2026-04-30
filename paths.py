# %%
# Import necessary libraries
from pathlib import Path
from IPython.display import Markdown, display

# %%
# PROJECT PATHS CONFIGURATION
display(Markdown("""
# Configuration: Project Paths

This file centralizes all path definitions for the thesis project using pathlib.Path for cross-platform
compatibility. Paths are organized hierarchically from root directory down through subdirectories.

Each path variable includes type hints and docstrings to provide context on hover in your IDE.
Use these constants throughout notebooks instead of hardcoded strings.
"""))

# %%
# ROOT REPOSITORY
display(Markdown("""
## 0. Root Repository

The root directory is the base folder of the project, containing all subfolders and files related to the thesis.
This is where the main paths configuration file (paths.py) is located, which defines paths to all other
important directories and files used in the project. Using pathlib.Path ensures cross-platform compatibility
across Windows, macOS, and Linux systems.
"""))

# %%
ROOT_DIR: Path = Path(__file__).parent
"""
Base folder of the thesis project containing all subfolders and files.

This is the root directory where paths.py is located. All other paths in the project
are defined relative to ROOT_DIR for cross-platform compatibility across Windows, macOS,
and Linux. When referenced in notebooks, use ROOT_DIR.resolve() to get the absolute path.

Example:
    from paths import ROOT_DIR
    print(ROOT_DIR.resolve())  # C:\dev\thesis-manifold
"""

# %%
display(Markdown("""
### 0.1 Root Directory Example

The following example shows how to access the root directory:
"""))

# %%
print(f"ROOT_DIR = {ROOT_DIR.resolve()}")

# %%
display(Markdown("""
## 1. Thesis Directory

The thesis folder serves as the central hub for all thesis-related work. It contains subdirectories for analysis
(notebooks, figures, outputs) and data (raw datasets, preprocessing scripts, assessment data). All paths within
this section are relative to THESIS_DIR.
"""))

# %%
THESIS_DIR: Path = ROOT_DIR / "thesis"
"""
Main thesis folder containing all analysis, data, and related files.

This is the central hub for all thesis-related work including computational analysis,
datasets, figures, and model outputs. It is subdivided into 'analysis' and 'data'
subdirectories for organizational clarity.

Example:
    from paths import THESIS_DIR
    print(THESIS_DIR.resolve())  # C:\dev\thesis-manifold\thesis
"""

# %%
display(Markdown("""
### 1.1 Thesis Directory Example

The following example shows how to access the thesis directory:
"""))

# %%
print(f"THESIS_DIR = {THESIS_DIR.resolve()}")

# %%
display(Markdown("""
### 1.2 Analysis Subdirectory

The analysis folder contains all notebooks, figures, prompts, and output files generated during the thesis work.
This is where computational analysis, visualizations, and model outputs are stored and organized by category.
"""))

# %%
THESIS_ANALYSIS_DIR: Path = THESIS_DIR / "analysis"
"""
Directory containing all computational analysis work, notebooks, outputs, and figures.

This folder holds all Jupyter notebooks, generated figures, prompt configurations,
and analysis outputs organized by research question and category. It serves as the
hub for all computational and analytical work on the thesis.

Example:
    from paths import THESIS_ANALYSIS_DIR
    print(THESIS_ANALYSIS_DIR.resolve())  # C:\dev\thesis-manifold\thesis\analysis
"""

# %%
display(Markdown("""
#### 1.2.1 Analysis Directory Example

The following example shows how to access the analysis directory:
"""))

# %%
print(f"THESIS_ANALYSIS_DIR = {THESIS_ANALYSIS_DIR.resolve()}")

# %%
display(Markdown("""
#### 1.2.2 Analysis Sub-Subdirectories

The analysis directory is further organized into specific subdirectories for different types of outputs:
- **figures**: Visualizations and plots generated from analysis
- **notebooks**: Jupyter notebooks containing analysis code and results
- **prompts**: Prompt templates and configurations for system interactions
- **outputs**: Processed results and model outputs
"""))

# %%
THESIS_FIGURES_DIR: Path = THESIS_ANALYSIS_DIR / "figures"
"""
Directory for all figures and visualizations generated from analysis.

Contains publication-ready plots, charts, and figures generated during the thesis work.
Subdirectories may organize figures by research question, category, or analysis type.

Example:
    from paths import THESIS_FIGURES_DIR
    import matplotlib.pyplot as plt
    plt.savefig(THESIS_FIGURES_DIR / "my_plot.png")
"""

THESIS_NOTEBOOKS_DIR: Path = THESIS_ANALYSIS_DIR / "notebooks"
"""
Directory containing all Jupyter notebooks for analysis work.

Houses notebooks organized by research question (SRQ_1, SRQ_2, etc.) and analysis type.
Each notebook contains code, exploration, and results for specific analytical tasks.

Example:
    from paths import THESIS_NOTEBOOKS_DIR
    notebook_path = THESIS_NOTEBOOKS_DIR / "SRQ_1" / "analysis.ipynb"
"""

THESIS_PROMPTS_DIR: Path = THESIS_ANALYSIS_DIR / "prompts"
"""
Directory containing prompt templates and configurations.

Stores reusable prompts for system interactions, model queries, and other
computational tasks used across the thesis analysis.

Example:
    from paths import THESIS_PROMPTS_DIR
    prompts_file = THESIS_PROMPTS_DIR / "system_prompts.json"
"""

THESIS_OUTPUTS_DIR: Path = THESIS_ANALYSIS_DIR / "outputs"
"""
Directory containing all processed results and model outputs.

Organized by category (csd, danskvand, energidrikke, etc.) and type (feature_matrices,
raw outputs, etc.). This is where final analysis results and feature matrices are stored.

Example:
    from paths import THESIS_OUTPUTS_DIR
    csd_outputs = THESIS_OUTPUTS_DIR / "csd"
"""

# %%
display(Markdown("""
#### 1.2.3 Analysis Sub-Subdirectories Examples

The following examples show how to access each analysis sub-subdirectory:
"""))

# %%
print(f"THESIS_FIGURES_DIR = {THESIS_FIGURES_DIR.resolve()}")
print(f"THESIS_NOTEBOOKS_DIR = {THESIS_NOTEBOOKS_DIR.resolve()}")
print(f"THESIS_PROMPTS_DIR = {THESIS_PROMPTS_DIR.resolve()}")
print(f"THESIS_OUTPUTS_DIR = {THESIS_OUTPUTS_DIR.resolve()}")

# %%
display(Markdown("""
#### 1.2.4 Feature Matrices Output Directory

Feature matrices contain preprocessed data in Parquet format used for machine learning model training.
These files are optimized for efficient data loading and numerical operations.
"""))

# %%
FEATURE_MATRIX_OUTPUTS_DIR: Path = THESIS_OUTPUTS_DIR / "feature_matrices"
"""
Directory for feature matrices in Parquet format used for ML model training.

Contains preprocessed, normalized data in Parquet format optimized for machine learning.
Files are organized by category and time period for easy access during model training.

Example:
    from paths import FEATURE_MATRIX_OUTPUTS_DIR
    import pandas as pd
    df = pd.read_parquet(FEATURE_MATRIX_OUTPUTS_DIR / "csd_features.parquet")
"""

# %%
display(Markdown("""
##### 1.2.4.1 Feature Matrices Directory Example

The following example shows how to access the feature matrices directory:
"""))

# %%
print(f"FEATURE_MATRIX_OUTPUTS_DIR = {FEATURE_MATRIX_OUTPUTS_DIR.resolve()}")

# %%
display(Markdown("""
#### 1.2.5 Category-Specific Output Directories

Output directories are organized by product category to keep results organized and easily accessible.
Each category has its own subdirectory containing analysis results, feature matrices, and model outputs.
"""))

# %%
CSD_OUTPUTS_DIR: Path = THESIS_OUTPUTS_DIR / "csd"
"""
Output directory for CSD (Cold Soft Drinks) category analysis.

Contains all analysis results, feature matrices, and model outputs specific to the
CSD product category used in the thesis research.

Example:
    from paths import CSD_OUTPUTS_DIR
    results = CSD_OUTPUTS_DIR / "model_results.json"
"""

DANSKVAND_OUTPUTS_DIR: Path = THESIS_OUTPUTS_DIR / "danskvand"
"""
Output directory for Danskvand (Danish Water) category analysis.

Contains all analysis results, feature matrices, and model outputs specific to the
Danskvand product category used in the thesis research.

Example:
    from paths import DANSKVAND_OUTPUTS_DIR
    results = DANSKVAND_OUTPUTS_DIR / "predictions.csv"
"""

ENERGIDRIKKE_OUTPUTS_DIR: Path = THESIS_OUTPUTS_DIR / "energidrikke"
"""
Output directory for Energidrikke (Energy Drinks) category analysis.

Contains all analysis results, feature matrices, and model outputs specific to the
Energidrikke product category used in the thesis research.

Example:
    from paths import ENERGIDRIKKE_OUTPUTS_DIR
    results = ENERGIDRIKKE_OUTPUTS_DIR / "evaluation.json"
"""

RTD_V2_OUTPUTS_DIR: Path = THESIS_OUTPUTS_DIR / "rtd_v2"
"""
Output directory for RTD v2 (Ready-to-Drink v2) category analysis.

Contains all analysis results, feature matrices, and model outputs specific to the
RTD v2 product category used in the thesis research.

Example:
    from paths import RTD_V2_OUTPUTS_DIR
    results = RTD_V2_OUTPUTS_DIR / "model_outputs.parquet"
"""

TOTALBEER_OUTPUTS_DIR: Path = THESIS_OUTPUTS_DIR / "totalbeer"
"""
Output directory for TotalBeer category analysis.

Contains all analysis results, feature matrices, and model outputs specific to the
TotalBeer product category used in the thesis research.

Example:
    from paths import TOTALBEER_OUTPUTS_DIR
    results = TOTALBEER_OUTPUTS_DIR / "summary_stats.json"
"""

POOLED_4_OUTPUTS_DIR: Path = THESIS_OUTPUTS_DIR / "pooled_4"
"""
Output directory for pooled analysis (4 categories combined).

Contains results from analysis combining 4 product categories to identify cross-category
patterns and insights for the thesis research.

Example:
    from paths import POOLED_4_OUTPUTS_DIR
    results = POOLED_4_OUTPUTS_DIR / "pooled_results.json"
"""

POOLED_5_OUTPUTS_DIR: Path = THESIS_OUTPUTS_DIR / "pooled_5"
"""
Output directory for pooled analysis (5 categories combined).

Contains results from analysis combining all 5 product categories to identify
comprehensive cross-category patterns and insights for the thesis research.

Example:
    from paths import POOLED_5_OUTPUTS_DIR
    results = POOLED_5_OUTPUTS_DIR / "comprehensive_analysis.json"
"""

# %%
display(Markdown("""
##### 1.2.5.1 Category-Specific Directories Examples

The following examples show how to access each category-specific output directory:
"""))

# %%
print(f"CSD_OUTPUTS_DIR = {CSD_OUTPUTS_DIR.resolve()}")
print(f"DANSKVAND_OUTPUTS_DIR = {DANSKVAND_OUTPUTS_DIR.resolve()}")
print(f"ENERGIDRIKKE_OUTPUTS_DIR = {ENERGIDRIKKE_OUTPUTS_DIR.resolve()}")
print(f"RTD_V2_OUTPUTS_DIR = {RTD_V2_OUTPUTS_DIR.resolve()}")
print(f"TOTALBEER_OUTPUTS_DIR = {TOTALBEER_OUTPUTS_DIR.resolve()}")
print(f"POOLED_4_OUTPUTS_DIR = {POOLED_4_OUTPUTS_DIR.resolve()}")
print(f"POOLED_5_OUTPUTS_DIR = {POOLED_5_OUTPUTS_DIR.resolve()}")

# %%
display(Markdown("""
### 1.3 Data Subdirectory

The data folder contains all datasets, raw data sources, and preprocessing scripts. It is organized into
subdirectories for different data sources and processing stages.
"""))

# %%
THESIS_DATA_DIR: Path = THESIS_DIR / "data"
"""
Directory containing all datasets, raw data sources, and preprocessing scripts.

Organized by data source (Nielsen, Indeks Danmark, assessment data) and processing stage.
This is the hub for all data management related to the thesis research.

Example:
    from paths import THESIS_DATA_DIR
    print(THESIS_DATA_DIR.resolve())  # C:\dev\thesis-manifold\thesis\data
"""

# %%
display(Markdown("""
#### 1.3.1 Data Directory Example

The following example shows how to access the data directory:
"""))

# %%
print(f"THESIS_DATA_DIR = {THESIS_DATA_DIR.resolve()}")

# %%
display(Markdown("""
#### 1.3.2 Data Sub-Subdirectories

The data directory is further organized into specific subdirectories for different data sources:
- **assessment**: Human evaluation and assessment data
- **nielsen**: Nielsen market research data exports
- **preprocessing**: Data preprocessing scripts and intermediate files
- **spss_indeksdanmark**: Indeks Danmark SPSS data files
"""))

# %%
THESIS_ASSESSMENT_DIR: Path = THESIS_DATA_DIR / "assessment"
"""
Directory containing human evaluation and assessment data.

Stores evaluation results, annotations, and assessment data used for validating
model predictions and analyzing system performance in the thesis research.

Example:
    from paths import THESIS_ASSESSMENT_DIR
    assessments = THESIS_ASSESSMENT_DIR / "human_eval.csv"
"""

THESIS_NIELSEN_DIR: Path = THESIS_DATA_DIR / "nielsen"
"""
Directory containing Nielsen market research data exports.

Stores Nielsen data extracts and processed files used for market analysis,
product category information, and sales data in the thesis research.

Example:
    from paths import THESIS_NIELSEN_DIR
    data = THESIS_NIELSEN_DIR / "nielsen_export.csv"
"""

THESIS_PREPROCESSING_DIR: Path = THESIS_DATA_DIR / "preprocessing"
"""
Directory for data preprocessing scripts and intermediate files.

Contains Python scripts, notebooks, and intermediate data files used for
cleaning, transforming, and preparing raw data for analysis.

Example:
    from paths import THESIS_PREPROCESSING_DIR
    script = THESIS_PREPROCESSING_DIR / "clean_data.py"
"""

THESIS_SPSS_INDEKSDANMARK_DIR: Path = THESIS_DATA_DIR / "spss_indeksdanmark"
"""
Directory containing Indeks Danmark SPSS data files.

Stores SPSS data exports from Indeks Danmark used for consumer behavior analysis
and market insights in the thesis research.

Example:
    from paths import THESIS_SPSS_INDEKSDANMARK_DIR
    data = THESIS_SPSS_INDEKSDANMARK_DIR / "indeks_danmark.sav"
"""

# %%
display(Markdown("""
#### 1.3.3 Data Sub-Subdirectories Examples

The following examples show how to access each data sub-subdirectory:
"""))

# %%
print(f"THESIS_ASSESSMENT_DIR = {THESIS_ASSESSMENT_DIR.resolve()}")
print(f"THESIS_NIELSEN_DIR = {THESIS_NIELSEN_DIR.resolve()}")
print(f"THESIS_PREPROCESSING_DIR = {THESIS_PREPROCESSING_DIR.resolve()}")
print(f"THESIS_SPSS_INDEKSDANMARK_DIR = {THESIS_SPSS_INDEKSDANMARK_DIR.resolve()}")