"""
Base preprocessing utilities for Nielsen data pipeline.
Provides validation, caching, and common data operations.
"""

from pathlib import Path
from typing import List, Optional
import pandas as pd


def validate_input(path: Path, file_pattern: str, required: bool = True) -> bool:
	"""
	Validate that input file(s) exist.

	Args:
		path: Directory or file path to check
		file_pattern: Glob pattern (e.g. "*.jsonl") if path is directory
		required: If True, raise error if missing; if False, return False

	Returns:
		True if file(s) exist, False otherwise
	"""
	if path.is_file():
		exists = path.exists()
	else:
		exists = len(list(path.glob(file_pattern))) > 0

	if not exists and required:
		raise FileNotFoundError(f"Required input not found: {path}")

	return exists


def get_required_jsonl_files(category: str) -> dict:
	"""
	Get list of required JSONL files by category.

	Returns dict with keys: 'raw', 'views', 'metadata'
	Each contains list of required filenames (without path).
	"""
	base_name = category.lower().replace(" ", "_")

	# Raw tables (full granularity, if available)
	raw_files = [
		f"{base_name}_clean_facts.jsonl",
		f"{base_name}_clean_dim_product.jsonl",
		f"{base_name}_clean_dim_period.jsonl",
		f"{base_name}_clean_dim_market.jsonl",
	]

	# Views (cleaned, column-reduced)
	view_files = [
		f"{base_name}_clean_facts_v.jsonl",
		f"{base_name}_clean_dim_product_v.jsonl",
		f"{base_name}_clean_dim_period_v.jsonl",
		f"{base_name}_clean_dim_market_v.jsonl",
	]

	# Metadata (schema documentation)
	metadata_files = [
		f"metadata_{base_name}_clean_facts.jsonl",
		f"metadata_{base_name}_clean_dim_product.jsonl",
		f"metadata_{base_name}_clean_dim_period.jsonl",
		f"metadata_{base_name}_clean_dim_market.jsonl",
		f"metadata_{base_name}_columns.jsonl",
	]

	return {
		"raw": raw_files,
		"views": view_files,
		"metadata": metadata_files,
	}


def cache_jsonl_tables(input_dir: Path, output_dir: Path, table_names: List[str]) -> int:
	"""
	Cache JSONL tables as parquet files.

	Args:
		input_dir: Directory containing JSONL files
		output_dir: Directory to save parquet files
		table_names: List of table names (without extension)

	Returns:
		Total rows cached
	"""
	output_dir.mkdir(parents=True, exist_ok=True)
	total_rows = 0

	for table_name in table_names:
		jsonl_path = input_dir / f"{table_name}.jsonl"
		if not jsonl_path.exists():
			print(f"    ⚠ {table_name}: JSONL not found (skipped)")
			continue

		try:
			df = pd.read_json(jsonl_path, lines=True)
			output_path = output_dir / f"{table_name}.parquet"
			df.to_parquet(output_path, index=False)
			total_rows += len(df)
			print(f"    ✓ {table_name}: {len(df):,} rows")
		except Exception as e:
			print(f"    ✗ {table_name}: {e}")

	return total_rows
