
# %%
from pathlib import Path

# %%

# Establish the root directory path using pathlib for better cross-platform compatibility
ROOT_DIR = Path(__file__).parent
print(f"Root directory set to: {ROOT_DIR.resolve()}")

# %%

# General thesis folder

THESIS_DIR = ROOT_DIR / "thesis"
print(f"Thesis directory set to: {THESIS_DIR.resolve()}")

# %%

## Analysis subfolders

THESIS_ANALYSIS_DIR = THESIS_DIR / "analysis"
print(f"Thesis analysis directory set to: {THESIS_ANALYSIS_DIR.resolve()}")

## Analysis sub-subfolders

THESIS_FIGURES_DIR = THESIS_ANALYSIS_DIR / "figures"
print(f"Thesis analysis/figures directory set to: {THESIS_FIGURES_DIR.resolve()}")

THESIS_NOTEBOOKS_DIR = THESIS_ANALYSIS_DIR / "notebooks"
print(f"Thesis analysis/notebooks directory set to: {THESIS_NOTEBOOKS_DIR.resolve()}")

THESIS_PROMPTS_DIR = THESIS_ANALYSIS_DIR / "prompts"
print(f"Thesis analysis/prompts directory set to: {THESIS_PROMPTS_DIR.resolve()}")

THESIS_OUTPUTS_DIR = THESIS_ANALYSIS_DIR / "outputs"
print(f"Thesis analysis/outputs directory set to: {THESIS_OUTPUTS_DIR.resolve()}")

  # %%                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                           
  ## Category-specific output directories
FEATURE_MATRIX_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "feature_matrices"
CSD_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "csd"
DANSKVAND_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "danskvand"
ENERGIDRIKKE_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "energidrikke"
RTD_V2_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "rtd_v2"
TOTALBEER_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "totalbeer"
POOLED_4_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "pooled_4"
POOLED_5_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "pooled_5"

  # %%


# %%

## Data Subfolders

THESIS_DATA_DIR = THESIS_DIR / "data"

## Data sub-subfolders
THESIS_ASSESSMENT_DIR = THESIS_DATA_DIR / "assessment"
print(f"Thesis data/assessment directory set to: {THESIS_ASSESSMENT_DIR.resolve()}")

THESIS_NIELSEN_DIR = THESIS_DATA_DIR / "nielsen"
print(f"Thesis data/nielsen directory set to: {THESIS_NIELSEN_DIR.resolve()}")

THESIS_PREPROCESSING_DIR = THESIS_DATA_DIR / "preprocessing"
print(f"Thesis data/preprocessing directory set to: {THESIS_PREPROCESSING_DIR.resolve()}")

THESIS_SPSS_INDEKSDANMARK_DIR = THESIS_DATA_DIR / "spss_indeksdanmark"







# %%
