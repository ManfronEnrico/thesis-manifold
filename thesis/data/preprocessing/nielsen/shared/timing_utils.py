"""
Timing and logging utilities for preprocessing pipeline steps.
Records step execution time, row counts, and memory usage to JSON logs.
"""

import json
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
from datetime import datetime


@contextmanager
def step_timer(step_name: str):
	"""
	Context manager for timing a step.

	Usage:
		with step_timer("Build Calendar"):
			df = process(df)
	"""
	start_time = time.perf_counter()
	try:
		yield
	finally:
		elapsed = time.perf_counter() - start_time


def log_step_timing(step_num: int, step_name: str, category: str,
					elapsed_sec: float, row_count: int, output_log_path: Path,
					input_cols: int = None, output_cols: int = None) -> None:
	"""
	Write JSON log entry for this step.

	Args:
		step_num: Step number (0-6)
		step_name: Human-readable step name
		category: Category name (CSD, Energidrikke, etc.)
		elapsed_sec: Elapsed time in seconds
		row_count: Output row count
		output_log_path: Path to save JSON log file
		input_cols: Number of input columns (optional)
		output_cols: Number of output columns (optional)

	Appends to existing log if file exists, creates new log otherwise.
	"""
	output_log_path.parent.mkdir(parents=True, exist_ok=True)

	log_entry = {
		"timestamp": datetime.now().isoformat(),
		"step_num": step_num,
		"step_name": step_name,
		"category": category,
		"elapsed_sec": round(elapsed_sec, 2),
		"output_rows": row_count,
	}

	if input_cols is not None:
		log_entry["input_cols"] = input_cols
	if output_cols is not None:
		log_entry["output_cols"] = output_cols

	# Append to log file (or create if doesn't exist)
	if output_log_path.exists():
		with open(output_log_path, "r") as f:
			logs = json.load(f)
	else:
		logs = []

	logs.append(log_entry)

	with open(output_log_path, "w") as f:
		json.dump(logs, f, indent=2)
