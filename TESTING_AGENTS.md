# Testing the Agent Workflow

This guide shows how to test the fixed agent data paths and verify the workflow end-to-end.

## Quick Start (PowerShell)

```powershell
cd "C:\Users\brian\OneDrive\Documents\02--A--Areas\MSc. Data Science\2026-03 - CBS Master Thesis\CMT_Codebase"

# Test 1: Configuration and data loading
python thesis\thesis_agents\test_agents.py

# Test 2: Full LangGraph pipeline
python thesis\thesis_agents\test_langgraph_pipeline.py
```

## What Each Test Does

### Test 1: Agent Configuration & Data Loading (`test_agents.py`)

**What it tests:**
- Config classes load with correct relative paths
- Data directories exist and are accessible
- CSV files are found at expected locations
- Pandas can read the CSV files

**Expected output:**
```
[OK] NielsenConfig created
[OK] IndeksDanmarkConfig created
[OK] Nielsen directory exists: 29 CSV files
[OK] Indeks Danmark directory exists: 3 CSV files
[OK] Nielsen CSV loaded: 2,535,464 rows, 10 columns
[OK] Indeks Danmark CSV loaded: 20,134 rows, 6,364 columns
```

**Run it:**
```powershell
python thesis\thesis_agents\test_agents.py
```

### Test 2: LangGraph Pipeline (`test_langgraph_pipeline.py`)

**What it tests:**
- LangGraph coordinator builds successfully
- Pipeline can be invoked with initial state
- Data assessment agent executes
- Data loads correctly through the pipeline

**Expected output:**
```
[OK] LangGraph built successfully
[OK] Graph execution completed
[OK] Data assessment node executes (loads Nielsen + Indeks data)
```

**Run it:**
```powershell
python thesis\thesis_agents\test_langgraph_pipeline.py
```

## Manual Testing in Python

If you want to test components individually:

```python
# 1. Test config loading
from thesis.thesis_agents.ai_research_framework.config import NielsenConfig, IndeksDanmarkConfig

cfg = NielsenConfig()
print(f"Nielsen CSV dir: {cfg.csv_dir}")
print(f"Exists: {cfg.csv_dir.exists()}")

# 2. Test CSV finding
csv_files = list(cfg.csv_dir.glob("csd_clean_facts_v.csv"))
print(f"Found {len(csv_files)} Nielsen CSV files")

# 3. Test CSV loading
import pandas as pd
df = pd.read_csv(csv_files[0])
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
print(f"Columns: {df.columns.tolist()[:5]}")

# 4. Test DataAssessmentAgent
from thesis.thesis_agents.ai_research_framework.agents import DataAssessmentAgent
agent = DataAssessmentAgent(
    nielsen_cfg=cfg,
    indeks_cfg=IndeksDanmarkConfig(),
    output_path=Path("docs/data")
)
print("Agent created successfully")
```

## What Was Fixed

### System A (ai_research_framework)

**config.py:**
- ✅ Added `csv_dir: Path` fields to both config classes
- ✅ Added `__post_init__()` validation methods
- ✅ Removed stale `local_available` boolean attribute
- ✅ Changed env var access to use safe `.get()` with fallbacks

**data_assessment_agent.py:**
- ✅ `_assess_nielsen()` now uses `csv_dir.glob()` to find and load CSVs
- ✅ `_assess_indeks_danmark()` now uses `csv_dir.glob()` to find and load CSVs
- ✅ Replaced `NotImplementedError` placeholders with actual pandas CSV loading
- ✅ Removed references to non-existent `local_available` attribute
- ✅ Added clear error messages with correct relative paths

### System B (thesis_production_system)

**writing_agent.py:**
- ✅ Updated Chapter 4 bullet template to reflect data is now available
- ✅ Changed status from "⚠️ NOT YET OBTAINED" to "[OK] Available locally at..."
- ✅ Removed all "Google Drive" references
- ✅ Updated outstanding tasks to reflect current data status

## Data Locations

```
thesis/data/
├── nielsen/
│   └── .csv/                           # 29 CSV files
│       ├── csd_clean_facts_v.csv       (2.5M rows)
│       ├── csd_clean_dim_market_v.csv
│       ├── csd_clean_dim_period_v.csv
│       └── ... (26 more files)
│
└── spss_indeksdanmark/
    └── .csv/                           # 3 CSV files
        ├── indeksdanmark_data.csv      (20K rows, 6.3K cols, 254MB)
        ├── indeksdanmark_metadata.csv
        └── official_codebook.csv
```

## Troubleshooting

### Error: "Nielsen data directory not found"
- Check that `thesis/data/nielsen/.csv/` exists
- Check file permissions on the directory
- Verify CSV files are actually in the directory: `ls thesis/data/nielsen/.csv/`

### Error: "Indeks Danmark data directory not found"
- Check that `thesis/data/spss_indeksdanmark/.csv/` exists
- This directory should have 3 CSV files

### Error: "ModuleNotFoundError: No module named 'ai_research_framework'"
- Make sure you're running from the CMT_Codebase directory
- Verify `thesis/thesis_agents/` exists

### Error: "FileNotFoundError: [Errno 2] No such file or directory: 'csd_clean_facts_v.csv'"
- The CSV files exist but aren't being found
- Check that CSV filenames match exactly (case-sensitive)
- Try: `ls thesis/data/nielsen/.csv/ | grep csd_clean_facts_v`

## Next Steps

1. **Run the basic test:** `python thesis\thesis_agents\test_agents.py`
2. **Run the pipeline test:** `python thesis\thesis_agents\test_langgraph_pipeline.py`
3. **Check file loading:** Verify CSV data loads in Python
4. **Implement feature engineering:** The `_engineer_features()` method still raises `NotImplementedError`
5. **Test forecasting agents:** Once data flows through, test the forecasting nodes

## Files Modified in This Session

| File | Changes |
|------|---------|
| `thesis/thesis_agents/ai_research_framework/config.py` | Added csv_dir paths, validation, env var safety |
| `thesis/thesis_agents/ai_research_framework/agents/data_assessment_agent.py` | Implemented CSV loading |
| `thesis/thesis_agents/thesis_production_system/agents/writing_agent.py` | Updated bullet points |

All changes are relative paths that work for both local development and Enrico's future setup.
