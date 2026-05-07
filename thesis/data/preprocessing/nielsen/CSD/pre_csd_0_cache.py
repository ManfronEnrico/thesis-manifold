#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 0: Cache Raw Data

Input:  Raw Nielsen JSONL files from thesis/data/raw_nielsen/data_jsonl/CSD/
		- raw/csd_clean_facts.jsonl (and 3 other raw tables)
		- views/csd_clean_facts_v.jsonl (and 3 other view tables)
		- metadata/metadata_csd_clean_facts.jsonl (and 4 other metadata tables)

Output: Step 0 output (parquet cached copies for reference)
		- Raw tables: raw/csd_clean_facts.parquet, etc.
		- View tables: views/csd_clean_facts_v.parquet, etc.
		- Metadata: metadata/metadata_csd_clean_facts.parquet, etc.

Logic:
  - Read JSONL files from raw_nielsen data source
  - Convert to parquet for faster subsequent access
  - Skip missing files gracefully
"""

import sys, time
from pathlib import Path

# Find project root
current = Path.cwd()
while current != current.parent:
	if (current / "CLAUDE.md").exists():
		ROOT_DIR = current
		break
	current = current.parent
else:
	raise FileNotFoundError("Could not find project root")

sys.path.insert(0, str(ROOT_DIR))

from PATHS import THESIS_DATA_NIELSEN_JSONL_DIR, THESIS_DATA_PREPROCESSING_DIR, get_category_pipeline_step_outputs_dir

from thesis.data.preprocessing.nielsen.shared.base_preprocessing import (
	get_required_jsonl_files, cache_jsonl_tables
)
from thesis.data.preprocessing.nielsen.shared.terminal_utils import (
	step_execution, print_info, print_warning
)
from thesis.data.preprocessing.nielsen.shared.timing_utils import log_step_timing

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_NUM = 0
STEP_NAME = "Cache Raw Data"

# Input paths (Nielsen JSONL data)
INPUT_RAW_DIR = THESIS_DATA_NIELSEN_JSONL_DIR / CATEGORY / "raw"
INPUT_VIEWS_DIR = THESIS_DATA_NIELSEN_JSONL_DIR / CATEGORY / "views"
INPUT_METADATA_DIR = THESIS_DATA_NIELSEN_JSONL_DIR / CATEGORY / "metadata"

# Output paths (parquet cache)
OUTPUT_RAW_DIR = THESIS_DATA_PREPROCESSING_DIR / "nielsen" / CATEGORY / "raw"
OUTPUT_VIEWS_DIR = THESIS_DATA_PREPROCESSING_DIR / "nielsen" / CATEGORY / "views"
OUTPUT_METADATA_DIR = THESIS_DATA_PREPROCESSING_DIR / "nielsen" / CATEGORY / "metadata"

LOG_FILE = get_category_pipeline_step_outputs_dir(CATEGORY) / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def main():
	"""Execute step 0: Cache raw data as parquet."""
	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()
		total_rows = 0

		# Get required file lists
		required_files = get_required_jsonl_files(CATEGORY)

		# Cache raw tables
		print("\nCaching raw tables as parquet...")
		if INPUT_RAW_DIR.exists():
			raw_rows = cache_jsonl_tables(INPUT_RAW_DIR, OUTPUT_RAW_DIR,
										 [f.replace(".jsonl", "") for f in required_files["raw"]])
			total_rows += raw_rows
		else:
			print_warning(f"Raw input directory not found: {INPUT_RAW_DIR}")

		# Cache view tables
		print("\nCaching view tables as parquet...")
		if INPUT_VIEWS_DIR.exists():
			view_rows = cache_jsonl_tables(INPUT_VIEWS_DIR, OUTPUT_VIEWS_DIR,
										  [f.replace(".jsonl", "") for f in required_files["views"]])
			total_rows += view_rows
		else:
			print_warning(f"Views input directory not found: {INPUT_VIEWS_DIR}")

		# Cache metadata tables
		print("\nCaching metadata tables as parquet...")
		if INPUT_METADATA_DIR.exists():
			metadata_rows = cache_jsonl_tables(INPUT_METADATA_DIR, OUTPUT_METADATA_DIR,
											 [f.replace(".jsonl", "") for f in required_files["metadata"]])
			total_rows += metadata_rows
		else:
			print_warning(f"Metadata input directory not found: {INPUT_METADATA_DIR}")

		# Summary
		step_elapsed = time.perf_counter() - step_start
		LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
		log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, total_rows, LOG_FILE)

		print_info(f"Total rows cached: {total_rows:,}")


if __name__ == "__main__":
	main()
