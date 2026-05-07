"""
Terminal UI utilities for preprocessing pipeline using Rich library.
Provides progress bars, spinners, and formatted output for step execution.
"""

import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Callable, Any

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.style import Style
from rich.panel import Panel
from rich.table import Table

console = Console()

# ============================================================================
# STEP EXECUTION CONTEXT
# ============================================================================

@contextmanager
def step_execution(step_num: int, step_name: str, category: str):
	"""
	Context manager for step execution with header and timing.

	Usage:
		with step_execution(2, "Build Calendar", "CSD"):
			df = load_data()
			df = process(df)
			save_data(df)
	"""
	start_time = time.perf_counter()

	# Print header
	header = f"Nielsen {category} — Step {step_num}: {step_name}"
	console.print(f"\n{'='*80}")
	console.print(f"[bold cyan]{header}[/bold cyan]")
	console.print(f"{'='*80}\n")

	try:
		yield
	except Exception as e:
		console.print(f"\n[red]✗ FAILED[/red]: {e}\n")
		raise
	finally:
		elapsed = time.perf_counter() - start_time
		console.print(f"\n[green]✓ Completed in {elapsed:.1f}s[/green]\n")


# ============================================================================
# PROGRESS TRACKING
# ============================================================================

@contextmanager
def progress_bar(description: str, total: int, show_percentage: bool = True):
	"""
	Rich progress bar context manager.

	Usage:
		with progress_bar("Processing rows", total=1000000) as progress:
			task = progress.add_task("MyTask", total=1000000)
			for i in range(0, 1000000, 10000):
				do_work(i)
				progress.update(task, advance=10000)
	"""
	with Progress(
		SpinnerColumn(),
		TextColumn("[bold blue]{task.description}"),
		BarColumn(),
		TextColumn("[progress.percentage]{task.percentage:>3.0f}%") if show_percentage else TextColumn(""),
		TextColumn("•"),
		TextColumn("[cyan]{task.fields[rows]:,}[/cyan]"),
		TimeRemainingColumn(),
		console=console,
		transient=True,
	) as progress:
		yield progress


def progress_task(progress: Progress, description: str, total: int) -> int:
	"""
	Add a task to an existing progress bar.

	Usage:
		with progress_bar("Processing", 1000) as progress:
			task = progress_task(progress, "Step 1", 1000)
			for i in range(1000):
				do_work()
				progress.update(task, advance=1)
	"""
	return progress.add_task(description, total=total, rows=0)


# ============================================================================
# FILE OPERATIONS FEEDBACK
# ============================================================================

def print_file_load(file_path: Path, shape: tuple, elapsed: float = None):
	"""Print formatted message for loaded file."""
	size_mb = file_path.stat().st_size / (1024 * 1024)
	msg = f"✓ Loaded: {file_path.name}"
	msg += f" • {shape[0]:,} rows × {shape[1]} cols"
	msg += f" • {size_mb:.1f} MB"
	if elapsed:
		msg += f" • {elapsed:.2f}s"
	console.print(msg)


def print_file_save(file_path: Path, shape: tuple, elapsed: float = None):
	"""Print formatted message for saved file."""
	size_mb = file_path.stat().st_size / (1024 * 1024)
	msg = f"✓ Saved: {file_path.name}"
	msg += f" • {shape[0]:,} rows × {shape[1]} cols"
	msg += f" • {size_mb:.1f} MB"
	if elapsed:
		msg += f" • {elapsed:.2f}s"
	console.print(msg)


def print_validation_result(valid: bool, message: str):
	"""Print validation result."""
	icon = "✓" if valid else "✗"
	color = "green" if valid else "red"
	console.print(f"[{color}]{icon}[/{color}] {message}")


def print_step_summary(step_num: int, step_name: str, elapsed: float,
					   input_rows: int = None, output_rows: int = None,
					   input_cols: int = None, output_cols: int = None,
					   memory_mb: float = None, output_file: Path = None):
	"""Print formatted summary of step completion."""
	summary_lines = [
		f"Step {step_num}: {step_name}",
		f"Elapsed: {elapsed:.1f}s",
	]
	if input_rows is not None:
		summary_lines.append(f"Input rows: {input_rows:,}")
	if output_rows is not None:
		summary_lines.append(f"Output rows: {output_rows:,}")
	if input_cols is not None:
		summary_lines.append(f"Input columns: {input_cols}")
	if output_cols is not None:
		summary_lines.append(f"Output columns: {output_cols}")
	if memory_mb is not None:
		summary_lines.append(f"Peak RAM: {memory_mb:.1f} MB")
	if output_file is not None:
		summary_lines.append(f"Output file: {output_file}")

	panel = Panel(
		"\n".join(summary_lines),
		title="[bold cyan]Summary[/bold cyan]",
		border_style="cyan"
	)
	console.print(panel)


# ============================================================================
# ERROR HANDLING & WARNINGS
# ============================================================================

def print_warning(message: str):
	"""Print warning message."""
	console.print(f"[yellow]⚠ WARNING[/yellow]: {message}")


def print_error(message: str):
	"""Print error message."""
	console.print(f"[red]✗ ERROR[/red]: {message}")


def print_info(message: str):
	"""Print info message."""
	console.print(f"[cyan]ℹ INFO[/cyan]: {message}")


# ============================================================================
# TABLES & STRUCTURED OUTPUT
# ============================================================================

def print_data_preview(df, title: str = "Data Preview", max_rows: int = 10):
	"""Print pandas DataFrame as Rich table."""
	from rich.table import Table

	table = Table(title=f"[bold cyan]{title}[/bold cyan]")

	# Add columns
	for col in df.columns[:10]:  # Limit to 10 columns for readability
		table.add_column(str(col), style="cyan")

	# Add rows
	for i, row in df.head(max_rows).iterrows():
		table.add_row(*[str(v)[:20] for v in row[:10]])

	console.print(table)


def print_timing_summary(timings: dict, category: str):
	"""Print timing summary table for all steps."""
	table = Table(title=f"[bold cyan]Preprocessing Timing — {category}[/bold cyan]")
	table.add_column("Step", style="cyan")
	table.add_column("Elapsed (s)", justify="right")
	table.add_column("Rows", justify="right")
	table.add_column("RAM (MB)", justify="right")

	total_elapsed = 0
	for step_num in sorted(timings.keys()):
		timing = timings[step_num]
		table.add_row(
			f"{step_num}: {timing['step_name']}",
			f"{timing['elapsed']:.1f}",
			f"{timing.get('rows', '—'):,}" if isinstance(timing.get('rows'), int) else "—",
			f"{timing.get('memory_mb', '—'):.1f}" if isinstance(timing.get('memory_mb'), float) else "—",
		)
		total_elapsed += timing['elapsed']

	table.add_row(
		"[bold]TOTAL[/bold]",
		f"[bold]{total_elapsed:.1f}[/bold]",
		"",
		"",
		style="bold"
	)

	console.print(table)


# ============================================================================
# ORCHESTRATOR OUTPUT
# ============================================================================

def print_orchestrator_start(category: str, flags: dict = None):
	"""Print orchestrator start message."""
	msg = f"Preprocessing Pipeline: {category}"
	if flags:
		flag_str = ", ".join([f"{k}={v}" for k, v in flags.items()])
		msg += f" [{flag_str}]"

	panel = Panel(msg, style="bold green", border_style="green")
	console.print(panel)


def print_orchestrator_complete(category: str, total_elapsed: float,
								steps_run: list = None):
	"""Print orchestrator completion message."""
	msg = f"✓ {category} preprocessing complete\n"
	msg += f"Total elapsed: {total_elapsed:.1f}s"
	if steps_run:
		msg += f"\nSteps run: {', '.join([str(s) for s in steps_run])}"

	panel = Panel(msg, style="bold green", border_style="green")
	console.print(panel)


def print_master_summary(category_timings: dict, total_elapsed: float):
	"""Print summary for all categories."""
	table = Table(title="[bold cyan]All Categories Summary[/bold cyan]")
	table.add_column("Category", style="cyan")
	table.add_column("Elapsed (s)", justify="right")
	table.add_column("Status", justify="center")

	for category, timing in sorted(category_timings.items()):
		status_icon = "✓" if timing.get('status') == 'success' else "✗"
		table.add_row(
			category,
			f"{timing['elapsed']:.1f}",
			status_icon
		)

	table.add_row(
		"[bold]TOTAL[/bold]",
		f"[bold]{total_elapsed:.1f}[/bold]",
		"",
		style="bold"
	)

	console.print(table)
