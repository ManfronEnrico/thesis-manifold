"""
Console and table capture utilities for the Nielsen preprocessing pipeline.

WHY THIS EXISTS
---------------
The CSD pipeline previously lived in a Jupyter notebook, where console output
and printed DataFrames were retained in the .ipynb on save. Decomposing the
notebook into scripts (P0038) loses that for free -- printed output would go to
a terminal and vanish. These utilities restore the property explicitly:

    tee_console(path)   -- mirror everything printed to a .log file on disk
    save_table(df, ...) -- persist a DataFrame as CSV (machine) + TXT (human)

Plots already persisted via plt.savefig() in the notebook, so they need no
equivalent here.

Separate from terminal_utils.py on purpose: terminal_utils is Rich-based
presentation, this is disk persistence. A script can use one without the other.
"""

import sys
from contextlib import contextmanager
from pathlib import Path

import pandas as pd


# ============================================================================
# CONSOLE CAPTURE
# ============================================================================

class _Tee:
	"""Write to two streams at once (real stdout + a log file).

	Deliberately not a full io.TextIOBase: only the methods print() and Rich
	actually touch are implemented, plus the isatty/fileno pair that Rich
	queries to decide whether to emit ANSI colour.
	"""

	def __init__(self, stream, handle):
		self._stream = stream
		self._handle = handle

	def write(self, data):
		self._stream.write(data)
		self._handle.write(data)
		return len(data)

	def flush(self):
		self._stream.flush()
		self._handle.flush()

	def isatty(self):
		# Report the REAL stream's tty-ness. Rich asks this to decide on colour
		# codes; answering False unconditionally would strip colour from the
		# live terminal, answering True unconditionally would write escape
		# sequences into the log file.
		return self._stream.isatty()

	def fileno(self):
		return self._stream.fileno()


@contextmanager
def tee_console(log_path: Path, echo: bool = True):
	"""Mirror stdout+stderr into `log_path` for the duration of the block.

	Args:
		log_path: file to write. Parent dirs are created. Overwritten, not
			appended -- each run should reflect that run alone, otherwise a
			re-run silently doubles the file and diffing two runs is useless.
		echo: if False, output goes ONLY to the file (used by the orchestrator
			when running steps as subprocesses, which capture stdout already).

	Usage:
		with tee_console(STEP_OUTPUT_DIR / "step_0_console.log"):
			print("this lands in both places")

	Restores the original streams even if the block raises, so a failing step
	still leaves a complete log up to the point of failure.
	"""
	log_path = Path(log_path)
	log_path.parent.mkdir(parents=True, exist_ok=True)

	original_stdout, original_stderr = sys.stdout, sys.stderr
	handle = log_path.open("w", encoding="utf-8")

	if echo:
		sys.stdout = _Tee(original_stdout, handle)
		sys.stderr = _Tee(original_stderr, handle)
	else:
		sys.stdout = handle
		sys.stderr = handle

	try:
		yield log_path
	finally:
		# Restore BEFORE closing: if close() raised while the tee was still
		# installed, the traceback would try to write to a closed file.
		sys.stdout, sys.stderr = original_stdout, original_stderr
		handle.close()


# ============================================================================
# TABLE CAPTURE
# ============================================================================

def save_table(
	df: pd.DataFrame,
	name: str,
	output_dir: Path,
	caption: str | None = None,
	index: bool = False,
	float_format: str = "%.4f",
) -> tuple[Path, Path]:
	"""Persist a DataFrame as both CSV and a Markdown table.

	Two formats because they serve different readers:
	  - .csv  : re-loadable, feeds Ch4 tables and any downstream comparison
	  - .md   : the human/appendix artifact. Markdown rather than the
	            fixed-width TXT this used to write: these tables are destined
	            for thesis appendices, and monospace alignment is lost the
	            moment it is pasted into Word or Docs, which reflows it in a
	            proportional font. A Markdown table survives that paste,
	            renders as a real table in any previewer, and screenshots
	            cleanly -- while still diffing line-by-line, which is why it
	            can replace the notebook's stored output.

	Args:
		df: frame to persist.
		name: stem for both files, e.g. "step_2_brand_summary".
		output_dir: destination directory (created if absent).
		caption: optional heading written above the TXT rendering.
		index: whether to write the DataFrame index. Default False because most
			pipeline tables carry a meaningful column key already; pass True for
			describe()/value_counts() output where the index IS the label.
		float_format: applied to both outputs so CSV and TXT agree.

	Returns:
		(csv_path, md_path)
	"""
	output_dir = Path(output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)

	csv_path = output_dir / f"{name}.csv"
	md_path = output_dir / f"{name}.md"

	df.to_csv(csv_path, index=index, float_format=float_format, encoding="utf-8")

	# to_markdown() needs tabulate. It is a hard dependency of this function
	# rather than an optional nicety, so fail loudly with the fix rather than
	# silently degrading to to_string() -- a silent fallback would write a
	# fixed-width body into a .md file, and the appendix would look broken for
	# a reason nobody could see from the output.
	try:
		rendered = df.to_markdown(index=index, floatfmt=float_format.lstrip("%"))
	except ImportError as exc:  # pragma: no cover
		raise ImportError(
			"save_table() writes Markdown tables and needs `tabulate`. "
			"Install it with: python -m pip install tabulate"
		) from exc

	with md_path.open("w", encoding="utf-8") as fh:
		if caption:
			# H2, not H1: these files are appendix fragments pasted under a
			# thesis heading, so they should not claim the top level.
			fh.write(f"## {caption}\n\n")
		fh.write(rendered)
		fh.write("\n")

	return csv_path, md_path


def print_and_save_table(
	df: pd.DataFrame,
	name: str,
	output_dir: Path,
	caption: str | None = None,
	index: bool = False,
	max_rows: int = 25,
) -> tuple[Path, Path]:
	"""save_table(), plus echo a truncated view to stdout.

	The notebook printed full frames; a terminal-run script printing 140 brands
	buries the surrounding narrative. So the console gets `max_rows`, while the
	CSV/Markdown on disk always get the complete frame.
	"""
	if caption:
		print(f"\n{caption}")
		print("-" * max(len(caption), 40))

	if len(df) > max_rows:
		print(df.head(max_rows).to_string(index=index))
		print(f"... {len(df) - max_rows:,} more rows (full table in {name}.csv)")
	else:
		print(df.to_string(index=index))

	return save_table(df, name, output_dir, caption=caption, index=index)
