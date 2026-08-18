#!/usr/bin/env python
"""
Step 2 -- Descriptive EDA for one Nielsen category.

Ported from the CSD notebook's cells 17-39 (EDA steps 3.01-3.12), P0038 task 3.

WHAT THIS STEP IS FOR
---------------------
Evidence for Chapter 4, and nothing else. This step produces NO parameters:
nothing downstream reads its output, which is precisely why it is separable
from step 3 (which derives the feature-engineering contract). If a number
computed here is needed by a later step, it is recomputed there deliberately
rather than smuggled across via a JSON file.

Several cells printed a "recommendation" (MIN_PERIODS = 40, HOLIDAY_MONTHS =
{...}). Those are reproduced as printed evidence, exactly as the notebook had
them, and are NOT written anywhere a later step could pick them up. The real
values are step 3's job.

DEC-OPEN-WORLD (P0038, 2026-08-12)
----------------------------------
This script never names a category and never enumerates a column. It discovers
what a category has and analyses that.

The notebook could not do this. Cell 39 referenced `df['promo_units']`
unconditionally, guarded only by an `.empty` check -- which tests for zero
ROWS, not a missing COLUMN. Danskvand has no promo columns at all, so that cell
raised KeyError, and that single line is the reason three of four categories
have no EDA today.

The fix is not a skip-list keyed on category. It is to ask the data what it
has. Each analysis below declares the columns it needs via `requires=`, and
`section()` runs it only if they are all present, reporting the absence in a
line the reader sees. A category with a column nobody else has gets it analysed
for free; a category missing one produces one fewer figure. No branch anywhere
names a category.

USAGE
    python step_2_eda_descriptive.py --category CSD
    python step_2_eda_descriptive.py --category Danskvand --no-plots
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Repo root on sys.path so `import PATHS` resolves when run as a script.
_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
	sys.path.insert(0, str(_REPO_ROOT))

from capture_utils import save_table, tee_console  # noqa: E402
from pipeline_config import (  # noqa: E402
	DPI,
	FIGSIZE_DEFAULT,
	FIGSIZE_LARGE,
	PLOT_COLOR,
	TARGET_COL,
	apply_plot_style,
	get_paths,
	normalise_category,
	suppress_warnings,
)
from step_1_load_and_aggregate import load_and_aggregate, load_merged  # noqa: E402

# ============================================================================
# GRAIN COLUMNS
# ============================================================================
# The panel's identity columns, as produced by step 1. Named here because the
# EDA groups by them constantly; they are structural, not measures.

BRAND_COL = "brand"
YEAR_COL = "period_year"
MONTH_COL = "period_month"

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
			   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Minimum months either side of a candidate structural break (notebook cell 23).
MIN_SEGMENT = 6

# Brands carried into the per-brand ADF test and the time-series plots. Both
# are notebook values, kept so CSD output is comparable run-to-run.
N_BRANDS_ADF = 20
N_BRANDS_PLOT = 5

# Minimum observations for a per-brand ADF test to be meaningful (cell 25).
MIN_OBS_ADF = 10


# ============================================================================
# SECTION RUNNER (the DEC-OPEN-WORLD mechanism)
# ============================================================================

class EdaContext:
	"""Carries state shared between sections, plus the run's bookkeeping.

	The notebook got this for free: every cell shared one namespace, so cell 33
	could read `holiday_months` and `monthly_sales` computed back in cell 31.
	Scripts do not share a namespace, so that coupling is made explicit here --
	a section writes what later sections need into `ctx.derived`.
	"""

	def __init__(self, category: str, df: pd.DataFrame, paths: dict,
				 make_plots: bool = True):
		self.category = category
		self.df = df
		self.paths = paths
		self.make_plots = make_plots
		self.derived: dict = {}
		self.skipped: list[tuple[str, list[str]]] = []
		self.failed: list[tuple[str, str]] = []
		self.tables_written: list[str] = []
		self.plots_written: list[str] = []

	def save(self, frame: pd.DataFrame, name: str, caption: str,
			 index: bool = False, notes: list[str] | None = None) -> None:
		"""Persist a table and echo it, recording that it was written.

		`notes` are interpretation bullets written above the table in the .md
		and echoed to the console. They state what the table shows, how to
		read it, and the methodological basis where one exists -- the .md
		files are pasted into thesis appendices, where a bare number grid
		makes the reader reconstruct the intent from the column headers.
		"""
		print(f"\n{caption}")
		print("-" * max(len(caption), 40))
		if notes:
			for note in notes:
				print(f"  - {note}")
			print()
		print(frame.to_string(index=index))
		save_table(frame, name, self.paths["tables_dir"], caption=caption,
				   index=index, notes=notes)
		self.tables_written.append(name)

	def savefig(self, plt, name: str) -> None:
		"""Persist the current figure, recording that it was written."""
		if not self.make_plots:
			plt.close()
			return
		out = self.paths["plots_dir"]
		out.mkdir(parents=True, exist_ok=True)
		plt.savefig(out / f"{name}.png", dpi=DPI, bbox_inches="tight")
		plt.close()
		self.plots_written.append(name)


def section(ctx: EdaContext, title: str, requires: tuple[str, ...] = ()):
	"""Decorator: run an analysis only if the columns it needs are present.

	`requires` is the whole of DEC-OPEN-WORLD in practice. A section declares
	the columns it cannot run without; if the category lacks any, the section
	is skipped with a visible, specific notice naming the missing columns --
	rather than raising KeyError (the notebook's behaviour) or silently
	producing nothing (worse, because the reader cannot tell).

	Exceptions are caught and recorded rather than aborting the run: the
	notebook wrapped most cells in try/except for the same reason, and an EDA
	pass that dies at section 4 of 12 is far less useful than one that
	completes and reports what failed.
	"""
	def decorator(fn):
		missing = [c for c in requires if c not in ctx.df.columns]
		print("\n" + "=" * 80)
		print(title)
		print("=" * 80)
		if missing:
			print(f"  SKIPPED -- this category has no {', '.join(missing)} "
				  f"column(s).")
			print(f"  Not an error: the analysis is undefined without them, so "
				  f"there is nothing to report.")
			ctx.skipped.append((title, missing))
			return fn
		try:
			fn()
		except Exception as exc:  # noqa: BLE001 -- see docstring
			print(f"  FAILED -- {type(exc).__name__}: {exc}")
			ctx.failed.append((title, f"{type(exc).__name__}: {exc}"))
		return fn
	return decorator


# ============================================================================
# 3.01 -- DATA PREVIEW AND STATISTICS
# ============================================================================

def s01_preview(ctx: EdaContext) -> None:
	@section(ctx, "3.01  DATA PREVIEW AND STATISTICS")
	def _run():
		df = ctx.df
		shape_df = pd.DataFrame({
			"Metric": ["Total Rows", "Unique Brands", "Columns"],
			"Value": [f"{len(df):,}", f"{df[BRAND_COL].nunique()}",
					  f"{len(df.columns)}"],
		})
		ctx.save(shape_df, "step_2_01_shape", "Data Shape",
			notes=[
				"Panel dimensions after step 1: the brand x month grain locked "
				"by DEC-GRAIN (2026-07-12), scoped to the DVH EXCL. HD parent "
				"market (DEC-SCOPE) rather than its nine region children.",
				"Row count is brands x observed months, not a complete grid -- "
				"brands enter and leave the panel, so absent brand-months are "
				"genuinely absent rather than null.",
			],
		)

		cols_info = pd.DataFrame({
			"Column": df.columns,
			"Data Type": df.dtypes.astype(str),
			"Non-Null": df.count(),
			"Missing": df.isnull().sum(),
			"Missing %": (100 * df.isnull().sum() / len(df)).round(1),
		}).reset_index(drop=True)
		ctx.save(cols_info, "step_2_01_columns", "Columns & Data Quality",
			notes=[
				"Every column step 1 produced, with its dtype and null count. "
				"Discovered, not enumerated (DEC-OPEN-WORLD): a category "
				"carrying a column no other category has still appears here.",
				"Column counts differ by category by design -- the four "
				"categories sit at different Nielsen capability tiers, and a "
				"column absent here was never delivered rather than lost in "
				"processing.",
			],
		)

		missing_df = cols_info[cols_info["Missing"] > 0][
			["Column", "Missing", "Missing %"]
		]
		if len(missing_df) > 0:
			ctx.save(missing_df, "step_2_01_missing", "Missing Value Analysis",
				notes=[
					"Nulls per column. In this panel a null is an unreported "
					"measure for an observed brand-month, which is distinct from a "
					"brand-month that does not appear at all.",
					"Matters for feature engineering because a lag or rolling "
					"window computed across a null propagates it forward into every "
					"window that spans the gap.",
				],
			)
		else:
			print("\nMissing Value Analysis: no missing values in any column")

		print("\nSample Data (first 10 rows):")
		print(df.head(10).to_string(index=False))


# ============================================================================
# 3.02 -- DISTRIBUTION ANALYSIS WITH SKEWNESS
# ============================================================================

def s02_distributions(ctx: EdaContext) -> None:
	@section(ctx, "3.02  DISTRIBUTION ANALYSIS WITH SKEWNESS")
	def _run():
		import matplotlib.pyplot as plt
		import seaborn as sns

		df = ctx.df
		# Already open-world in the notebook -- select_dtypes, not a list.
		numeric_cols = [c for c in df.select_dtypes(include="number").columns
						if c not in (YEAR_COL, MONTH_COL)]
		if not numeric_cols:
			print("  No numeric columns to analyse.")
			return

		sns.set_style("darkgrid")
		n = len(numeric_cols)
		ncols = 2
		nrows = (n + ncols - 1) // ncols
		plt.figure(figsize=(14, nrows * 3))

		rows = []
		for idx, feature in enumerate(numeric_cols, 1):
			plt.subplot(nrows, ncols, idx)
			series = df[feature].dropna()
			if len(series) > 0 and series.nunique() > 1:
				sns.histplot(series, kde=True)
			skewness = df[feature].skew()
			plt.title(f"{feature} | Skewness: {round(skewness, 2)}")

			# Order matters: the extreme-negative branch must precede the
			# moderate-negative one, or every value below -2 is reported as
			# merely "left-skewed". Preserved from the notebook.
			if skewness > 2:
				interp = ("Highly right-skewed -- substantial non-normality "
						  "(Kim, 2013) -> log transform necessary")
			elif skewness > 0.5:
				interp = "Right-skewed -- log transform justified"
			elif skewness < -2:
				interp = ("Highly left-skewed -- substantial non-normality "
						  "(Kim, 2013) -> log transform necessary")
			elif skewness < -0.5:
				interp = "Left-skewed (negative)"
			else:
				interp = "Approximately symmetric"
			rows.append({"feature": feature,
						 "skewness": round(float(skewness), 3),
						 "interpretation": interp})

		plt.tight_layout()
		ctx.savefig(plt, "01_distribution_histograms")
		ctx.save(pd.DataFrame(rows), "step_2_02_skewness", "Skewness Analysis",
			notes=[
				"Fisher-Pearson skewness per numeric column. Zero is symmetric; "
				"positive means a long right tail.",
				"Thresholds follow Kim (2013): |skew| > 2 indicates substantial "
				"departure from normality, 0.5-2 moderate. These bands are the "
				"stated basis for the log-transform recommendation, not an "
				"eyeball judgement.",
				"The forecast target's skewness is the empirical case for "
				"LOG_TRANSFORM_TARGET; see 3.15 for the same evidence as a "
				"distribution curve.",
				"Skewness is a property of the marginal distribution and says "
				"nothing about the time-series structure -- 3.05 and 3.16 cover "
				"that.",
			],
		)


# ============================================================================
# 3.03 -- DATE RANGE & TIME PERIOD ANALYSIS
# ============================================================================

def s03_date_range(ctx: EdaContext) -> None:
	@section(ctx, "3.03  DATE RANGE & TIME PERIOD ANALYSIS")
	def _run():
		df = ctx.df
		min_year, max_year = df[YEAR_COL].min(), df[YEAR_COL].max()
		min_month = df[df[YEAR_COL] == min_year][MONTH_COL].min()
		max_month = df[df[YEAR_COL] == max_year][MONTH_COL].max()
		total_months = (max_year - min_year) * 12 + (max_month - min_month) + 1

		coverage_df = pd.DataFrame({
			"Metric": ["Date Range", "Total Months", "Total Rows",
					   "Unique Brands", "Avg Rows/Brand"],
			"Value": [
				f"{min_year}-{min_month:02d} to {max_year}-{max_month:02d}",
				f"{total_months}",
				f"{len(df):,}",
				f"{df[BRAND_COL].nunique()}",
				f"{len(df) / df[BRAND_COL].nunique():.1f}",
			],
		})
		ctx.save(coverage_df, "step_2_03_coverage", "Coverage",
			notes=[
				"Observed span and completeness of the panel. Total months is "
				"the distinct period count, which bounds every window-based "
				"feature: a 12-month rolling mean is undefined in a panel "
				"shorter than 12.",
				"Also bounds the split. Train/validation/test cutoffs are "
				"derived proportionally from this span rather than hardcoded, "
				"after the hardcoded dates drifted to a 24-27% test share "
				"(F25).",
			],
		)

		rows_per_brand = df.groupby(BRAND_COL).size()
		dist_df = pd.DataFrame({
			"Statistic": ["Min", "Max", "Mean", "Median", "Std Dev"],
			"Rows/Brand": [
				f"{rows_per_brand.min()}", f"{rows_per_brand.max()}",
				f"{rows_per_brand.mean():.1f}", f"{rows_per_brand.median():.0f}",
				f"{rows_per_brand.std():.1f}",
			],
		})
		ctx.save(dist_df, "step_2_03_rows_per_brand",
				 "Rows per Brand Distribution",
			notes=[
				"Distribution of observation counts per brand -- how much "
				"history each brand actually has.",
				"Directly relevant to MIN_PERIODS: a brand with few "
				"observations cannot support lag-12 features and contributes "
				"mostly warmup rows. The threshold decision is step 3's (P0036 "
				"task 8 open); this table is its evidence.",
				"A long left tail means the panel is dominated by short-lived "
				"brands, which is a case for filtering rather than pooling them "
				"in.",
			],
		)
		ctx.derived["total_months"] = int(total_months)


# ============================================================================
# 3.04 -- STRUCTURAL BREAK SCAN (AUTO-DETECTED)
# ============================================================================

def s04_structural_break(ctx: EdaContext) -> None:
	@section(ctx, "3.04  STRUCTURAL BREAK SCAN (AUTO-DETECTED)",
			 requires=(TARGET_COL,))
	def _run():
		# Scans every candidate month rather than testing a hardcoded COVID
		# date -- the CSD data starts 2022-10, well after COVID onset, so the
		# original COVID-only check was untestable here. Runs early because a
		# break changes how stationarity, seasonality and lag analysis should
		# all be read.
		from scipy import stats as scipy_stats

		df = ctx.df
		monthly_agg = (
			df.groupby([YEAR_COL, MONTH_COL])[TARGET_COL]
			.sum().reset_index()
			.sort_values([YEAR_COL, MONTH_COL]).reset_index(drop=True)
		)
		n_months = len(monthly_agg)

		if n_months < 2 * MIN_SEGMENT:
			print(f"  Only {n_months} months available -- too few to test for "
				  f"a structural break (need >= {2 * MIN_SEGMENT}). Skipping.")
			ctx.derived["break_detected"] = False
			return

		sales_all = monthly_agg[TARGET_COL].values
		rss_pooled = np.sum((sales_all - sales_all.mean()) ** 2)
		n_total = len(sales_all)
		k = 1  # intercept-only model

		candidates = []
		for t in range(MIN_SEGMENT, n_months - MIN_SEGMENT):
			pre, post = sales_all[:t], sales_all[t:]
			rss_split = (np.sum((pre - pre.mean()) ** 2)
						 + np.sum((post - post.mean()) ** 2))
			if rss_split <= 0:
				continue
			chow_f = ((rss_pooled - rss_split) / k) / (rss_split / (n_total - 2 * k))
			candidates.append({
				"period_year": int(monthly_agg.iloc[t][YEAR_COL]),
				"period_month": int(monthly_agg.iloc[t][MONTH_COL]),
				"chow_f": chow_f,
				"chow_p": 1 - scipy_stats.f.cdf(chow_f, k, n_total - 2 * k),
				"mean_ratio": post.mean() / pre.mean() if pre.mean() > 0 else np.nan,
				"std_ratio": post.std() / pre.std() if pre.std() > 0 else np.nan,
			})

		if not candidates:
			print("  No testable candidate break points.")
			ctx.derived["break_detected"] = False
			return

		cand_df = pd.DataFrame(candidates).sort_values("chow_f", ascending=False)
		top3 = cand_df.head(3).copy()
		top3["date"] = (top3["period_year"].astype(str) + "-"
						+ top3["period_month"].astype(str).str.zfill(2))
		for col in ("chow_f", "mean_ratio", "std_ratio"):
			top3[col] = top3[col].round(3)
		top3["chow_p"] = top3["chow_p"].round(4)

		print(f"\n  Scanned {len(candidates)} candidate break points across "
			  f"{n_months} months")
		ctx.save(top3[["date", "chow_f", "chow_p", "mean_ratio", "std_ratio"]],
				 "step_2_04_structural_break",
				 "Top 3 Break Candidates by Chow F-statistic",
			notes=[
				"Chow test for a structural break in the aggregate series: the "
				"null is that the same relationship holds before and after the "
				"candidate date (Chow, 1960).",
				"A low p-value indicates the series mean/variance shifts at "
				"that point. That matters for the split, because a break inside "
				"the test window means the test period is not drawn from the "
				"training regime.",
				"Reported as the three strongest candidates rather than one "
				"verdict: with a single series and many candidate dates this is "
				"exploratory, and the multiple-comparisons problem is real.",
			],
		)

		best = cand_df.iloc[0]
		break_detected = bool(best["chow_p"] < 0.05)
		if break_detected:
			print(f"\n  STRUCTURAL BREAK DETECTED at "
				  f"{int(best['period_year'])}-{int(best['period_month']):02d} "
				  f"(Chow F={best['chow_f']:.2f}, p={best['chow_p']:.4f})")
			print("  -> Consider a binary post_break feature at this date, or "
				  "separate pre/post models if severity warrants it.")
		else:
			print(f"\n  No significant structural break (best candidate "
				  f"p={best['chow_p']:.4f} >= 0.05)")
			print("  -> A pooled model across the full range is supportable.")
		ctx.derived["break_detected"] = break_detected


# ============================================================================
# 3.05 -- STATIONARITY TESTING WITH ADF (PER BRAND)
# ============================================================================

def s05_stationarity(ctx: EdaContext) -> None:
	@section(ctx, "3.05  STATIONARITY TESTING -- PER-BRAND ADF",
			 requires=(TARGET_COL,))
	def _run():
		# Per brand, not aggregate: a brand entering or exiting distribution
		# carries a structural break that is invisible in the total.
		from statsmodels.tsa.stattools import adfuller

		df = ctx.df
		print("\n  H0: non-stationary  |  p < 0.05 -> stationary")
		print("  Testing raw, log1p, and first-difference\n")

		top_brands = (df.groupby(BRAND_COL)[TARGET_COL].sum()
					  .nlargest(N_BRANDS_ADF).index)

		results = []
		for brand in top_brands:
			series = (df[df[BRAND_COL] == brand]
					  .sort_values([YEAR_COL, MONTH_COL])[TARGET_COL]
					  .fillna(0).values)
			if len(series) < MIN_OBS_ADF:
				continue
			try:
				p_raw = adfuller(series, autolag="AIC")[1]
				p_log = adfuller(np.log1p(series), autolag="AIC")[1]
				p_diff = adfuller(np.diff(series), autolag="AIC")[1]
			except Exception:
				# A constant or near-constant series makes ADF undefined. One
				# brand failing must not lose the other 19.
				continue
			if p_raw < 0.05:
				rec = "raw"
			elif p_log < 0.05:
				rec = "log1p"
			else:
				rec = "log1p+diff"
			results.append({
				"brand": str(brand)[:30], "n": len(series),
				"p_raw": round(float(p_raw), 3),
				"p_log": round(float(p_log), 3),
				"p_diff": round(float(p_diff), 3),
				"recommendation": rec,
			})

		if not results:
			print("  No brand had enough observations for an ADF test.")
			return

		adf_df = pd.DataFrame(results)
		ctx.save(adf_df, "step_2_05_adf_per_brand",
				 "ADF Test per Brand (top brands by volume)",
			notes=[
				"Augmented Dickey-Fuller test per brand. Null hypothesis is a "
				"unit root, i.e. non-stationarity; p < 0.05 rejects it and "
				"indicates a stationary series (Dickey & Fuller, 1979).",
				"Failing to reject is weak evidence -- ADF has low power on "
				"short series, and these brands have at most ~46 monthly "
				"observations. Read a non-rejection as inconclusive, not as "
				"proof of a unit root.",
				"Non-stationary brands are the argument for differencing or for "
				"lag features that let the model absorb the trend rather than "
				"extrapolate it.",
			],
		)

		n_raw = int((adf_df["recommendation"] == "raw").sum())
		n_log = int((adf_df["recommendation"] == "log1p").sum())
		n_diff = int((adf_df["recommendation"] == "log1p+diff").sum())
		total = len(adf_df)
		print(f"\n  CROSS-BRAND STATIONARITY SUMMARY ({total} brands tested):")
		print(f"    Stationary raw:             {n_raw}/{total} ({100*n_raw/total:.0f}%)")
		print(f"    Stationary after log1p:     {n_log}/{total} ({100*n_log/total:.0f}%)")
		print(f"    Needs log1p + differencing: {n_diff}/{total} ({100*n_diff/total:.0f}%)")

		log_necessary = (n_log + n_diff) >= n_raw
		if log_necessary:
			print("\n  -> LOG TRANSFORM SUPPORTED (majority of brands benefit)")
		else:
			print("\n  -> Log transform optional; raw series mostly stationary")
		print("  Note: given the per-brand spread above, feature engineering "
			  "should apply log1p universally for stability.")

		agg_values = df.groupby([YEAR_COL, MONTH_COL])[TARGET_COL].sum().values
		p_agg = adfuller(agg_values, autolag="AIC")[1]
		print(f"\n  Aggregate series (reference only): ADF p={p_agg:.4f} "
			  f"{'(stationary)' if p_agg < 0.05 else '(non-stationary)'}")
		print("  The aggregate can mask per-brand heterogeneity -- the "
			  "per-brand result above takes precedence.")
		ctx.derived["log_transform_supported"] = bool(log_necessary)


# ============================================================================
# 3.06 -- BRAND STABILITY ANALYSIS (SERIES LENGTH)
# ============================================================================

def s06_brand_stability(ctx: EdaContext) -> None:
	@section(ctx, "3.06  BRAND STABILITY ANALYSIS (SERIES LENGTH)",
			 requires=(TARGET_COL,))
	def _run():
		df = ctx.df
		non_zero = df[df[TARGET_COL] > 0].groupby(BRAND_COL).size()
		n_brands = len(non_zero)

		# Thresholds span the observable range rather than the notebook's fixed
		# [20..43], which was written against CSD's 43-month span and would run
		# off the end of a shorter category.
		max_obs = int(non_zero.max()) if n_brands else 0
		thresholds = [t for t in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50)
					  if t <= max_obs] or [max_obs]

		rows = []
		for threshold in thresholds:
			count = int((non_zero >= threshold).sum())
			rows.append({
				"Min Periods": threshold,
				"Brands Retained": count,
				"% of Total": f"{100 * count / n_brands:.1f}%" if n_brands else "n/a",
				"Data Quality": ("Low" if threshold <= 25
								 else ("Medium" if threshold <= 35 else "High")),
			})
		ctx.save(pd.DataFrame(rows), "step_2_06_brand_retention",
				 "Brand Retention at Different MIN_PERIODS Thresholds",
			notes=[
				"How many brands survive each candidate minimum-observation "
				"threshold -- the retention curve for MIN_PERIODS.",
				"Thresholds are generated from the panel's own maximum span "
				"rather than the notebook's fixed 20-43 ladder, which had been "
				"written against CSD's 43-month history and produced empty rows "
				"elsewhere.",
				"The trade-off is explicit: a higher threshold buys longer, "
				"cleaner series at the cost of brand coverage. Look for the "
				"knee where retention falls sharply.",
				"Evidence only -- MIN_PERIODS is decided in step 3 (P0036 task "
				"8).",
			],
		)

		# The notebook printed "RECOMMENDATION: MIN_PERIODS = 40" here. That is
		# an open decision (P0036 task 8), so the evidence is reported and the
		# threshold is deliberately NOT chosen -- step 3 owns that call.
		print("\n  MIN_PERIODS is not selected here. The retention curve above "
			  "is the evidence;")
		print("  the threshold is a modelling decision made in step 3 "
			  "(P0036 task 8, open).")
		print(f"  Observed series length: min={int(non_zero.min()) if n_brands else 0}, "
			  f"max={max_obs}, median={int(non_zero.median()) if n_brands else 0}")


# ============================================================================
# 3.07 -- ZERO-SALES CHARACTERISATION
# ============================================================================

def s07_zero_sales(ctx: EdaContext) -> None:
	@section(ctx, "3.07  ZERO-SALES CHARACTERISATION", requires=(TARGET_COL,))
	def _run():
		# Distinguishes a run of zeros (brand entry/exit) from scattered zeros
		# (data gaps). The two call for opposite treatment, so counting zeros
		# alone would not settle the imputation question.
		df = ctx.df
		rows = []
		for brand, grp in df.groupby(BRAND_COL):
			sales = (grp.sort_values([YEAR_COL, MONTH_COL])[TARGET_COL].values)
			n_total = len(sales)
			n_zero = int((sales == 0).sum())
			if n_zero == 0:
				rows.append({"brand": brand, "n_total": n_total, "n_zero": 0,
							 "pct_zero": 0.0, "max_run": 0, "n_runs": 0,
							 "type": "no zeros"})
				continue

			run_lengths, run = [], 0
			for is_zero in (sales == 0):
				if is_zero:
					run += 1
				elif run > 0:
					run_lengths.append(run)
					run = 0
			if run > 0:
				run_lengths.append(run)

			max_run = max(run_lengths) if run_lengths else 0
			n_runs = len(run_lengths)
			if max_run >= 3:
				zero_type = "clustered (entry/exit)"
			elif n_runs > n_zero / 2:
				zero_type = "scattered (data gaps)"
			else:
				zero_type = "mixed"

			rows.append({"brand": brand, "n_total": n_total, "n_zero": n_zero,
						 "pct_zero": round(100 * n_zero / n_total, 1),
						 "max_run": int(max_run), "n_runs": int(n_runs),
						 "type": zero_type})

		zero_df = pd.DataFrame(rows)
		type_counts = (zero_df["type"].value_counts().rename_axis("type")
					   .reset_index(name="brands"))
		ctx.save(type_counts, "step_2_07_zero_types",
				 f"Zero-Sales Characterisation across {len(zero_df)} brands",
			notes=[
				"Brands classified by where zero-sales months occur: leading "
				"zeros (not yet launched), trailing (delisted), intermittent "
				"(genuinely sporadic demand), or none.",
				"The distinction drives treatment. Leading and trailing zeros "
				"are structural absence and should be trimmed; intermittent "
				"zeros are real demand behaviour and must be kept, since "
				"removing them would bias the target upward.",
				"Intermittent demand also breaks the usual accuracy metrics -- "
				"MAPE is undefined at zero, which constrains metric choice "
				"downstream.",
			],
		)

		with_zeros = zero_df[zero_df["n_zero"] > 0]
		print(f"\n  Brands with any zeros: {len(with_zeros)} / {len(zero_df)}")
		if len(with_zeros) > 0:
			print(f"    Mean % zeros:   {with_zeros['pct_zero'].mean():.1f}%")
			print(f"    Max run length: {int(with_zeros['max_run'].max())} periods")
			save_table(zero_df, "step_2_07_zero_per_brand",
					   ctx.paths["tables_dir"],
					   caption="Zero-sales detail per brand")
			ctx.tables_written.append("step_2_07_zero_per_brand")

		print("\n  Imputation implications:")
		print("    Clustered (entry/exit) -> exclude pre-entry periods; carry a "
			  "distribution indicator")
		print("    Scattered (data gaps)  -> forward-fill up to 2 periods; flag "
			  "with a missingness indicator")
		print("    Rolling means must handle zeros before computing, or lags "
			  "understate the true trend.")


# ============================================================================
# 3.08 -- SEASONAL PATTERN ANALYSIS (HOLIDAY EFFECT)
# ============================================================================

def s08_seasonality(ctx: EdaContext) -> None:
	@section(ctx, "3.08  SEASONAL PATTERN ANALYSIS (HOLIDAY EFFECT)",
			 requires=(TARGET_COL,))
	def _run():
		df = ctx.df
		monthly_sales = df.groupby(MONTH_COL)[TARGET_COL].sum()
		total = monthly_sales.sum()

		rows = []
		for month in range(1, 13):
			if month not in monthly_sales.index:
				continue
			sales = monthly_sales[month]
			pct = 100 * sales / total
			rows.append({
				"Month": month,
				"Month Name": MONTH_NAMES[month - 1],
				"Sales Units": f"{sales:,.0f}",
				"% of Total": f"{pct:.1f}%",
				"Classification": ("PEAK" if pct >= 10
								   else ("Normal" if pct >= 8 else "Valley")),
			})
		ctx.save(pd.DataFrame(rows), "step_2_08_monthly_distribution",
				 "Monthly Sales Distribution (Full Year)",
			notes=[
				"Total target by calendar month, aggregated across all years "
				"and brands -- the seasonal profile of the category.",
				"Confounded with trend: a category growing over the observation "
				"window inflates whichever months its later years cover most. "
				"Read alongside 3.10, where decomposition separates the two.",
				"The empirical basis for HOLIDAY_MONTHS, reported here but not "
				"persisted anywhere step 3 could read (DEC-EDA-SPLIT).",
			],
		)

		top_3 = monthly_sales.nlargest(3).index.tolist()
		bottom_3 = monthly_sales.nsmallest(3).index.tolist()
		q75 = monthly_sales.quantile(0.75)
		holiday_months = sorted(m for m in monthly_sales.index
								if monthly_sales[m] >= q75)

		peak_valley = pd.DataFrame({
			"Category": ["Top 3 Months", "Bottom 3 Months",
						 "Holiday Months (75th pct)"],
			"Months": [str(top_3), str(bottom_3), str(holiday_months)],
			"% of Sales": [
				f"{100 * monthly_sales[top_3].sum() / total:.1f}%",
				f"{100 * monthly_sales[bottom_3].sum() / total:.1f}%",
				f"{100 * monthly_sales[holiday_months].sum() / total:.1f}%",
			],
		})
		ctx.save(peak_valley, "step_2_08_peak_valley", "Peak & Valley Analysis",
			notes=[
				"Highest and lowest months of the seasonal profile, with the "
				"ratio between them as a one-number measure of seasonal "
				"amplitude.",
				"A large peak-to-valley ratio justifies month-of-year features; "
				"a flat profile argues they would add parameters without "
				"signal.",
			],
		)

		# Reported as evidence only. Step 3 derives the contract value; this
		# number is deliberately not persisted anywhere a later step reads.
		print(f"\n  Observed holiday months (top quartile, each >= "
			  f"{q75:,.0f} units): {holiday_months}")

		ctx.derived["monthly_sales"] = monthly_sales
		ctx.derived["holiday_months"] = holiday_months
		ctx.derived["q75"] = float(q75)
		ctx.derived["bottom_3_months"] = bottom_3


# ============================================================================
# 3.09 -- MONTHLY SALES BAR PLOT
# ============================================================================

def s09_monthly_barplot(ctx: EdaContext) -> None:
	@section(ctx, "3.09  MONTHLY SALES BAR PLOT", requires=(TARGET_COL,))
	def _run():
		import matplotlib.pyplot as plt

		# Depends on 3.08 having run. In the notebook this was implicit shared
		# state; here it is checked, so a failure in 3.08 degrades this section
		# to a notice instead of a NameError.
		if "monthly_sales" not in ctx.derived:
			print("  SKIPPED -- requires 3.08, which did not complete.")
			return

		monthly_sales = ctx.derived["monthly_sales"]
		holiday_months = ctx.derived["holiday_months"]
		q75 = ctx.derived["q75"]

		fig, ax = plt.subplots(figsize=FIGSIZE_DEFAULT)
		months = list(range(1, 13))
		values = [monthly_sales.get(m, 0) for m in months]
		colors = [PLOT_COLOR if m in holiday_months else "#A9A9A9"
				  for m in months]

		bars = ax.bar(MONTH_NAMES, values, color=colors, edgecolor="black",
					  alpha=0.7)
		for bar in bars:
			height = bar.get_height()
			ax.text(bar.get_x() + bar.get_width() / 2, height,
					f"{int(height):,}", ha="center", va="bottom",
					fontsize=9, fontweight="bold")

		ax.set_xlabel("Month", fontsize=11, fontweight="bold")
		ax.set_ylabel("Sales Units", fontsize=11, fontweight="bold")
		ax.set_title(f"{ctx.category} -- Monthly Sales Distribution "
					 f"(highlighted: top-quartile months)",
					 fontsize=12, fontweight="bold")
		ax.grid(True, alpha=0.3, axis="y")
		ax.axhline(q75, color="red", linestyle="--", alpha=0.5, linewidth=2,
				   label=f"75th percentile ({q75:,.0f})")
		ax.legend(fontsize=10)
		plt.tight_layout()
		ctx.savefig(plt, "03_monthly_sales_distribution")

		print(f"  Peak months (highlighted): {holiday_months}")
		print(f"  Valley months: {ctx.derived['bottom_3_months']}")


# ============================================================================
# 3.10 -- SEASONAL DECOMPOSITION
# ============================================================================

def s10_decomposition(ctx: EdaContext) -> None:
	@section(ctx, "3.10  SEASONAL DECOMPOSITION", requires=(TARGET_COL,))
	def _run():
		import matplotlib.pyplot as plt
		from statsmodels.tsa.seasonal import seasonal_decompose

		df = ctx.df
		ts_raw = (df.groupby([YEAR_COL, MONTH_COL])[TARGET_COL].sum()
				  .reset_index().sort_values([YEAR_COL, MONTH_COL]))

		# seasonal_decompose(period=12) needs two full cycles.
		if len(ts_raw) < 24:
			print(f"  SKIPPED -- {len(ts_raw)} months available; a period-12 "
				  f"decomposition needs at least 24.")
			return

		dates = pd.to_datetime(
			ts_raw[[YEAR_COL, MONTH_COL]].assign(day=1)
			.rename(columns={YEAR_COL: "year", MONTH_COL: "month"})
		)
		ts_monthly = pd.Series(ts_raw[TARGET_COL].values, index=dates)

		# FMCG seasonal amplitude often scales with trend volume, which is the
		# multiplicative case -- so both models are fitted and the one with
		# lower residual variance wins, rather than assuming additive.
		decomp_add = seasonal_decompose(ts_monthly, model="additive", period=12)
		resid_var_add = np.nanvar(decomp_add.resid)

		# Multiplicative is undefined at zero or negative values.
		if (ts_monthly > 0).all():
			decomp_mult = seasonal_decompose(ts_monthly, model="multiplicative",
											 period=12)
			resid_var_mult = np.nanvar(decomp_mult.resid)
			best_model = ("additive" if resid_var_add <= resid_var_mult
						  else "multiplicative")
			decomposition = (decomp_add if best_model == "additive"
							 else decomp_mult)
			print(f"\n  Additive residual variance:       {resid_var_add:.2e}")
			print(f"  Multiplicative residual variance: {resid_var_mult:.2e}")
			print(f"  -> Selected model: '{best_model}' (lower residual variance)")
		else:
			best_model, decomposition = "additive", decomp_add
			print("\n  Series contains non-positive values; multiplicative "
				  "decomposition is undefined. Using additive.")

		fig, axes = plt.subplots(4, 1, figsize=FIGSIZE_LARGE)
		ts_monthly.plot(ax=axes[0], color=PLOT_COLOR, linewidth=2)
		axes[0].set_title("Original Time Series", fontsize=11, fontweight="bold")
		decomposition.trend.plot(ax=axes[1], color=PLOT_COLOR, linewidth=2)
		axes[1].set_title("Trend Component", fontsize=11, fontweight="bold")
		decomposition.seasonal.plot(ax=axes[2], color=PLOT_COLOR, linewidth=2)
		axes[2].set_title(f"Seasonal Component (period=12, model={best_model})",
						  fontsize=11, fontweight="bold")
		decomposition.resid.plot(ax=axes[3], color=PLOT_COLOR, linewidth=1.5)
		axes[3].set_title("Residual Component", fontsize=11, fontweight="bold")
		axes[3].axhline(y=0, color="red", linestyle="--", alpha=0.5)
		for ax in axes:
			ax.grid(True, alpha=0.3)
		plt.tight_layout()
		ctx.savefig(plt, "04_seasonal_decomposition")

		trend = decomposition.trend.dropna()
		direction = ("Increasing" if trend.iloc[-1] > trend.iloc[0]
					 else "Decreasing")
		seasonal_by_month = (decomposition.seasonal
							 .groupby(decomposition.seasonal.index.month).mean())
		peaks = seasonal_by_month.nlargest(3).index.tolist()
		print(f"\n  Trend over the observed window: {direction}")
		print(f"  Seasonal peaks (top 3 months): {peaks}")
		if "holiday_months" in ctx.derived:
			print(f"  Compare with 3.08 top-quartile months: "
				  f"{ctx.derived['holiday_months']}")


# ============================================================================
# 3.11 -- TOP BRANDS TIME SERIES
# ============================================================================

def s11_top_brands(ctx: EdaContext) -> None:
	@section(ctx, "3.11  TOP BRANDS TIME SERIES", requires=(TARGET_COL,))
	def _run():
		import matplotlib.pyplot as plt

		df = ctx.df
		totals = df.groupby(BRAND_COL)[TARGET_COL].sum()
		top_brands = totals.nlargest(min(N_BRANDS_PLOT, len(totals))).index.tolist()
		if not top_brands:
			print("  No brands to plot.")
			return

		ctx.save(pd.DataFrame({
			"Rank": range(1, len(top_brands) + 1),
			"Brand": top_brands,
			"Total Sales": [f"{totals[b]:,.0f}" for b in top_brands],
		}), "step_2_11_top_brands",
			f"Top {len(top_brands)} Brands by Total Sales",
			notes=[
				"The largest brands by cumulative target volume, with their "
				"series plotted in the companion figure.",
				"These brands dominate any pooled error metric: a model can "
				"score well overall while failing on the long tail. Relevant to "
				"the pooled-versus-specialised question (P0036 task 9).",
				"Volume ranking, not forecastability ranking -- a large brand "
				"is not necessarily a stable or predictable one.",
			],
		)

		# squeeze=False keeps `axes` 2-D even when a category has a single
		# brand, so the indexing below cannot become a scalar.
		fig, axes = plt.subplots(len(top_brands), 1,
								 figsize=(14, 2.4 * len(top_brands)),
								 squeeze=False)
		for idx, brand in enumerate(top_brands):
			data = df[df[BRAND_COL] == brand].copy()
			data["date"] = pd.to_datetime(
				data[YEAR_COL].astype(str) + "-"
				+ data[MONTH_COL].astype(str).str.zfill(2) + "-01"
			)
			data = data.sort_values("date")
			ax = axes[idx][0]
			ax.plot(data["date"], data[TARGET_COL], color=PLOT_COLOR,
					linewidth=2, marker="o", markersize=4, label="Sales")
			ax.set_ylabel("Sales Units", fontsize=10)
			ax.set_title(f"{brand} -- Sales Over Time", fontsize=11,
						 fontweight="bold")
			ax.grid(True, alpha=0.3)
			ax.legend(fontsize=9)
		plt.tight_layout()
		ctx.savefig(plt, "05_top_brands_timeseries")


# ============================================================================
# 3.12 -- CROSS-BRAND HETEROGENEITY
# ============================================================================

def s12_heterogeneity(ctx: EdaContext) -> None:
	@section(ctx, "3.12  CROSS-BRAND HETEROGENEITY", requires=(TARGET_COL,))
	def _run():
		df = ctx.df
		stats = df.groupby(BRAND_COL)[TARGET_COL].agg(["mean", "std"]).dropna()
		stats = stats[stats["mean"] > 0]
		if stats.empty:
			print("  No brand has positive mean sales.")
			return
		stats["cv"] = stats["std"] / stats["mean"]

		ctx.save(pd.DataFrame({
			"Statistic": ["Min", "P25", "Median", "P75", "Max"],
			"CV": [f"{stats['cv'].min():.3f}",
				   f"{stats['cv'].quantile(0.25):.3f}",
				   f"{stats['cv'].median():.3f}",
				   f"{stats['cv'].quantile(0.75):.3f}",
				   f"{stats['cv'].max():.3f}"],
		}), "step_2_12_cv", f"Sales CV (std/mean) across {len(stats)} brands",
			notes=[
				"Coefficient of variation (std / mean) per brand: volatility "
				"normalised by level, so brands of different sizes are "
				"comparable.",
				"High CV means an inherently harder series. Reporting the "
				"spread of CV across brands is what justifies expecting "
				"heterogeneous accuracy rather than treating one aggregate "
				"error as representative.",
				"Undefined for a brand with mean zero, and unstable for "
				"near-zero means -- read the extreme values alongside 3.07.",
			],
		)

		high_cv = int((stats["cv"] > 1.0).sum())
		print(f"\n  Brands with CV > 1.0 (high volatility): "
			  f"{high_cv} / {len(stats)}")
		print("  High CV means the sales pattern varies greatly over time, "
			  "which is harder for a single pooled model.")

		peak_month = (df.groupby([BRAND_COL, MONTH_COL])[TARGET_COL].sum()
					  .groupby(level=0).idxmax().apply(lambda x: x[1]))
		peak_dist = peak_month.value_counts().sort_index()

		print("\n  Distribution of brands' peak sales month:")
		for month, count in peak_dist.items():
			print(f"    {MONTH_NAMES[month - 1]:>3}: {'#' * int(count)} ({count})")

		ctx.save(pd.DataFrame({
			"Month": [MONTH_NAMES[m - 1] for m in peak_dist.index],
			"Brands Peaking": peak_dist.values,
		}), "step_2_12_peak_months", "Brands' Peak Sales Month",
			notes=[
				"Each brand's own peak month, showing whether brands share the "
				"category's seasonal pattern or carry individual ones.",
				"If peaks cluster, a single shared seasonal feature suffices. "
				"If they scatter, brand-specific seasonality is what the model "
				"needs, which is an argument for brand identity interacting "
				"with month.",
			],
		)

		concentration = peak_dist.max() / peak_dist.sum()
		print(f"\n  Peak-month concentration: {concentration:.2f} "
			  f"(1.0 = all brands peak in the same month)")
		if concentration < 0.30:
			print("  -> Brands peak in DIFFERENT months; seasonal features "
				  "should be brand-specific.")
		else:
			print("  -> Most brands share a peak month; a shared seasonal "
				  "feature is likely sufficient.")

		print("\n  Heterogeneity verdict:")
		print("    High CV + varied peak months -> consider brand fixed effects "
			  "or per-brand models.")
		print("    A single pooled model is viable only with a brand "
			  "embedding or categorical feature.")


# ============================================================================
# 3.13 -- PROMO INTENSITY (runs only where promo columns exist)
# ============================================================================

def s13_promo_intensity(ctx: EdaContext) -> None:
	"""Promo spread across brands -- the analysis the notebook could not skip.

	This was the tail of notebook cell 39, where `df['promo_units']` was
	referenced unconditionally. Split into its own section so that a category
	without promo columns loses exactly this analysis and nothing else; in the
	notebook it took the whole heterogeneity cell down with it.
	"""
	@section(ctx, "3.13  PROMO INTENSITY ACROSS BRANDS",
			 requires=("promo_units", TARGET_COL))
	def _run():
		df = ctx.df
		sub = df[df["promo_units"] > 0]
		if sub.empty:
			print("  The promo_units column exists but is zero in every row: "
				  "no promotional activity recorded at this grain.")
			print("  This is a data observation, not a failure -- promo "
				  "features would be constant and carry no signal.")
			return

		intensity = (sub.groupby(BRAND_COL)
					 .apply(lambda g: (g["promo_units"]
									   / g[TARGET_COL].clip(lower=1)).mean(),
							include_groups=False))
		ctx.save(pd.DataFrame({
			"Statistic": ["Min", "P25", "Median", "P75", "Max"],
			"Promo Intensity": [f"{intensity.min():.3f}",
								f"{intensity.quantile(0.25):.3f}",
								f"{intensity.median():.3f}",
								f"{intensity.quantile(0.75):.3f}",
								f"{intensity.max():.3f}"],
		}), "step_2_13_promo_intensity",
			"Promo Intensity per Brand (where promo > 0)",
			notes=[
				"Brands ranked by promotional intensity (promo units as a share "
				"of total units).",
				"Identifies which brands rely on promotion. Only meaningful for "
				"categories where Nielsen delivered promo columns -- this "
				"section is skipped entirely elsewhere rather than reported as "
				"zero.",
				"Descriptive, not causal: intensity reflects commercial "
				"strategy, and promoted brands differ systematically from "
				"unpromoted ones.",
				"See 3.17 for the distribution's shape rather than the brand "
				"ranking.",
			],
		)

		n_with = df[BRAND_COL].isin(intensity.index).sum()
		print(f"\n  Brands with any promotional activity: "
			  f"{intensity.size} / {df[BRAND_COL].nunique()}")
		print(f"  Rows with promo_units > 0: {len(sub):,} / {len(df):,} "
			  f"({100 * len(sub) / len(df):.1f}%)")


# ============================================================================
# 3.14 -- MEASURE-COLUMN DATA QUALITY (open-world)
# ============================================================================

def s14_measure_quality(ctx: EdaContext) -> None:
	"""Per-column quality scan over whatever numeric columns exist.

	New in the script port. The notebook had no equivalent because it only ever
	saw CSD's columns; step 1 now discovers up to 32 measures per category, and
	an unexamined measure is how a defect like F42 (negative distributions in
	RTD) survives into a feature matrix.

	Answers two open questions with measured numbers rather than assumption:
	  - F42: how many rows carry a negative value in a share-like column, and
	    how large are those negatives?
	  - F39: whether a column behaves like a rate (bounded 0-100, so intensive)
	    or a count (unbounded, so additive) -- which decides whether step 1
	    should sum or average it.
	"""
	@section(ctx, "3.14  MEASURE-COLUMN DATA QUALITY")
	def _run():
		df = ctx.df
		numeric_cols = [c for c in df.select_dtypes(include="number").columns
						if c not in (YEAR_COL, MONTH_COL)]
		if not numeric_cols:
			print("  No numeric columns to scan.")
			return

		rows = []
		for col in numeric_cols:
			s = df[col]
			non_null = s.dropna()
			n_neg = int((non_null < 0).sum())
			looks_bounded = bool(len(non_null) > 0
								 and non_null.min() >= 0
								 and non_null.max() <= 100)
			rows.append({
				"column": col,
				"min": non_null.min() if len(non_null) else np.nan,
				"max": non_null.max() if len(non_null) else np.nan,
				"mean": non_null.mean() if len(non_null) else np.nan,
				"nulls": int(s.isna().sum()),
				"zeros": int((non_null == 0).sum()),
				"negatives": n_neg,
				"neg_pct": round(100 * n_neg / len(df), 3) if len(df) else 0.0,
				"in_0_100": looks_bounded,
			})

		quality = pd.DataFrame(rows)
		ctx.save(quality, "step_2_14_measure_quality",
				 "Measure-Column Quality Scan",
			notes=[
				"Per-column scan for the two defects that silently corrupt "
				"aggregation: impossible negatives, and rate columns mistakenly "
				"treated as additive.",
				"Negative counts and negative shares are impossible by "
				"definition, so any listed here are delivery defects. Reported "
				"and left uncorrected (F42): clipping would manufacture a "
				"plausible-looking value and hide the problem, and none of the "
				"affected columns is the target.",
				"The in_0_100 flag answers F39. A column bounded within [0, "
				"100] behaves as a rate and must be averaged when aggregating "
				"-- summing two 70% distribution figures into 140% is the "
				"specific error this check exists to prevent.",
				"The additive/intensive split it implies is what step 1's "
				"aggregation already applies; this table is the evidence that "
				"the classification matches the data.",
			],
		)

		negatives = quality[quality["negatives"] > 0]
		if len(negatives) > 0:
			print(f"\n  {len(negatives)} column(s) carry negative values:")
			for _, r in negatives.iterrows():
				print(f"    {r['column']}: {r['negatives']:,} rows "
					  f"({r['neg_pct']}%), min={r['min']:.4f}")
			print("  A negative share or distribution value is impossible by "
				  "definition, so these are delivery defects.")
			print("  Reported, not corrected: clipping would manufacture a "
				  "plausible-looking value and hide the problem (F42 open).")
		else:
			print("\n  No negative values in any measure column.")

		bounded = quality[quality["in_0_100"]]["column"].tolist()
		if bounded:
			print(f"\n  Column(s) observed entirely within [0, 100], "
				  f"consistent with a rate/share rather than a count:")
			for col in bounded:
				print(f"    {col}")
			print("  Relevant to F39: such columns must be averaged, not "
				  "summed, when aggregating (70% + 70% != 140%).")


# ============================================================================
# 3.15 -- EMPIRICAL CDF OF THE FORECAST TARGET
# ============================================================================

def s15_ecdf(ctx: EdaContext) -> None:
	"""Cumulative distribution of the target, per the notebook's stated plan.

	The notebook header advertises "histograms with skewness, ECDF" and its
	imports include statsmodels' ECDF, but the cell that drew
	02_ecdf_distributions.png had already been deleted by the time this port
	ran -- the PNG on disk had no surviving source (the header claims 14
	visualisations; 8 PNGs exist). Rebuilt from the stated intent rather than
	recovered.

	Complements 3.02: a histogram's shape depends on bin width, an ECDF does
	not. Reading quantiles straight off the curve is what makes it worth
	keeping alongside the skewness figure.
	"""
	@section(ctx, "3.15  EMPIRICAL CDF OF THE FORECAST TARGET",
			 requires=(TARGET_COL,))
	def _run():
		import matplotlib.pyplot as plt

		df = ctx.df
		series = df[TARGET_COL].dropna()
		if series.empty:
			print("  Target column is entirely null; nothing to plot.")
			return

		positive = series[series > 0]
		log_ok = len(positive) > 0

		fig, axes = plt.subplots(1, 2 if log_ok else 1,
								 figsize=FIGSIZE_DEFAULT, squeeze=False)

		x = np.sort(series.values)
		y = np.arange(1, len(x) + 1) / len(x)
		axes[0][0].step(x, y, where="post", color=PLOT_COLOR)
		axes[0][0].set_title(f"ECDF -- {TARGET_COL} (raw)", fontweight="bold")
		axes[0][0].set_xlabel(TARGET_COL)
		axes[0][0].set_ylabel("Cumulative proportion")
		axes[0][0].grid(True, alpha=0.3)

		# Quantile reference lines: the practical reason to prefer an ECDF
		# over a histogram is that these can be read straight off the curve.
		quantiles = {}
		for q in (0.25, 0.50, 0.75, 0.90):
			quantiles[q] = float(series.quantile(q))
			axes[0][0].axhline(q, color="grey", lw=0.6, ls="--", alpha=0.6)

		if log_ok:
			xl = np.sort(np.log1p(positive.values))
			yl = np.arange(1, len(xl) + 1) / len(xl)
			axes[0][1].step(xl, yl, where="post", color=PLOT_COLOR)
			axes[0][1].set_title(f"ECDF -- log1p({TARGET_COL})",
								 fontweight="bold")
			axes[0][1].set_xlabel(f"log1p({TARGET_COL})")
			axes[0][1].set_ylabel("Cumulative proportion")
			axes[0][1].grid(True, alpha=0.3)

		plt.tight_layout()
		ctx.savefig(plt, "02_ecdf_distributions")

		q_df = pd.DataFrame({
			"quantile": [f"p{int(q * 100)}" for q in quantiles],
			"value": [round(v, 4) for v in quantiles.values()],
		})
		ctx.save(
			q_df, "step_2_15_ecdf_quantiles",
			f"Target Distribution Quantiles ({TARGET_COL})",
			notes=[
				f"Cumulative share of brand-months at or below each "
				f"{TARGET_COL} value; shows the spread without the "
				f"bin-width dependence a histogram introduces.",
				f"p50 = {quantiles[0.50]:,.0f} against p90 = "
				f"{quantiles[0.90]:,.0f}: the gap between them is the "
				f"concentration this panel has to forecast across.",
				"A long right tail here is the empirical case for "
				"LOG_TRANSFORM_TARGET. The second panel shows the same data "
				"after log1p, where an approximately straight curve "
				"indicates the transform has done its job.",
				"Companion to 3.02 (skewness): that figure states the "
				"asymmetry as a single number, this one shows where in the "
				"distribution it sits.",
			],
		)


# ============================================================================
# 3.16 -- AUTOCORRELATION STRUCTURE (ACF / PACF)
# ============================================================================

def s16_acf_pacf(ctx: EdaContext) -> None:
	"""ACF/PACF for the largest brands. Ported from notebook cell 43.

	This is the evidential basis for whichever LAGS step 3 selects, which is
	why it is worth keeping as a figure and not only as the number step 3
	derives. Reported here, never persisted: DEC-EDA-SPLIT keeps parameter
	derivation in step 3.
	"""
	@section(ctx, "3.16  AUTOCORRELATION STRUCTURE (ACF / PACF)",
			 requires=(BRAND_COL, TARGET_COL))
	def _run():
		import matplotlib.pyplot as plt
		from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

		df = ctx.df
		totals = df.groupby(BRAND_COL)[TARGET_COL].sum().nlargest(5)
		top_brands = list(totals.index)
		if not top_brands:
			print("  No brands available.")
			return

		fig, axes = plt.subplots(len(top_brands), 2,
								 figsize=(14, 3 * len(top_brands)),
								 squeeze=False)

		rows = []
		for idx, brand in enumerate(top_brands):
			series = (df[df[BRAND_COL] == brand]
					  .sort_values([YEAR_COL, MONTH_COL])[TARGET_COL].values)
			# log1p to match the modelled target, so the lags read off this
			# figure are the lags that matter for the model actually fitted.
			series = np.log1p(series.astype(float))
			n = len(series)

			# statsmodels requires lags < nobs//2. A short brand series gets
			# fewer lags rather than an exception.
			if n < 4:
				axes[idx][0].set_visible(False)
				axes[idx][1].set_visible(False)
				continue
			max_lags = max(1, min(24, n // 2 - 1))

			plot_acf(series, lags=max_lags, ax=axes[idx][0], color=PLOT_COLOR)
			axes[idx][0].set_title(f"{brand} -- ACF", fontweight="bold")
			axes[idx][0].grid(True, alpha=0.3)

			plot_pacf(series, lags=max_lags, ax=axes[idx][1],
					  color=PLOT_COLOR, method="ywm")
			axes[idx][1].set_title(f"{brand} -- PACF", fontweight="bold")
			axes[idx][1].grid(True, alpha=0.3)

			# Significance band is +/-1.96/sqrt(n): the 95% band under the
			# null of no autocorrelation.
			conf = 1.96 / np.sqrt(n)
			acf_vals = [
				float(np.corrcoef(series[k:], series[:-k])[0, 1])
				for k in range(1, max_lags + 1)
				if len(series[k:]) > 1
			]
			sig = [k + 1 for k, v in enumerate(acf_vals)
				   if not np.isnan(v) and abs(v) > conf]
			rows.append({
				"brand": str(brand)[:30],
				"n_periods": n,
				"conf_band": round(conf, 4),
				"significant_lags": str(sig[:15]),
			})

		plt.tight_layout()
		ctx.savefig(plt, "06_acf_pacf_plots")

		if rows:
			sig_df = pd.DataFrame(rows)
			# Consensus across brands: a lag significant for one brand is
			# noise; one significant across the majority is structure.
			all_sig: list[int] = []
			for r in rows:
				all_sig.extend(
					int(v) for v in
					r["significant_lags"].strip("[]").split(",") if v.strip()
				)
			counts: dict[int, int] = {}
			for lag in all_sig:
				counts[lag] = counts.get(lag, 0) + 1
			consensus = sorted(k for k, v in counts.items()
							   if v / len(rows) >= 0.5)
			ctx.derived["acf_consensus_lags"] = consensus

			ctx.save(
				sig_df, "step_2_16_acf_significant_lags",
				"Significant ACF Lags per Brand",
				notes=[
					"Lags whose autocorrelation exceeds the 95% band "
					"(+/-1.96/sqrt(n)) under the null of no autocorrelation "
					"-- the standard Box-Jenkins reading of an ACF plot "
					"(Box & Jenkins, 1970).",
					f"Lags significant in at least half of the top "
					f"{len(rows)} brands: "
					f"{consensus if consensus else 'none'}. A lag clearing "
					f"the band for one brand is noise; one clearing it "
					f"across the majority is structure worth a feature.",
					"A spike at lag 12 indicates annual seasonality; spikes "
					"at 1-3 indicate short-run momentum. Both are what the "
					"lag features exist to capture.",
					"Computed on log1p(target) so these lags describe the "
					"series the model is actually fitted to.",
					"Evidence only -- LAGS is derived in step 3 "
					"(DEC-EDA-SPLIT). This figure is the justification for "
					"whatever that step selects.",
				],
			)


# ============================================================================
# 3.17 -- PROMO INTENSITY DISTRIBUTION
# ============================================================================

def s17_promo_distribution(ctx: EdaContext) -> None:
	"""Promo intensity histogram + promo/no-promo split. Notebook cell 49.

	Distinct from 3.13, which ranks brands by promo intensity. This section
	characterises the distribution's shape and whether promoted brand-months
	differ in level from unpromoted ones.
	"""
	@section(ctx, "3.17  PROMO INTENSITY DISTRIBUTION",
			 requires=("promo_units", TARGET_COL))
	def _run():
		import matplotlib.pyplot as plt
		import seaborn as sns

		df = ctx.df.copy()

		# clip(lower=1) avoids zero-division without the +1 bias that would
		# inflate intensity for low-volume brands. Preserved from cell 49.
		df["promo_intensity"] = (df["promo_units"]
								 / df[TARGET_COL].clip(lower=1))

		# promo_units is a SUBSET of sales_units in Nielsen's model, so a
		# ratio above 1 is a delivery defect, not a heavy promotion.
		invalid = int((df.loc[df[TARGET_COL] > 0, "promo_intensity"] > 1.0)
					  .sum())
		if invalid:
			print(f"  WARNING: {invalid} rows have promo_units > "
				  f"{TARGET_COL} -- data quality issue, reported not "
				  f"corrected.")

		fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_DEFAULT, squeeze=False)

		sns.histplot(df["promo_intensity"], kde=True, ax=axes[0][0],
					 color=PLOT_COLOR, edgecolor="black", alpha=0.7)
		skew = float(df["promo_intensity"].skew())
		axes[0][0].set_title(
			f"Promo intensity distribution\nSkewness: {skew:.3f}",
			fontweight="bold")
		axes[0][0].set_xlabel("Promo intensity (promo / sales)")
		axes[0][0].set_ylabel("Frequency")
		axes[0][0].grid(True, alpha=0.3, axis="y")

		df["has_promo"] = (df["promo_units"] > 0).astype(int)
		sns.boxplot(x="has_promo", y=TARGET_COL, data=df, ax=axes[0][1],
					hue="has_promo", legend=False,
					palette=[PLOT_COLOR, "#A9A9A9"])
		axes[0][1].set_xticks([0, 1])
		axes[0][1].set_xticklabels(["No promo", "With promo"])
		axes[0][1].set_xlabel("Promo status", fontweight="bold")
		axes[0][1].set_ylabel(TARGET_COL, fontweight="bold")
		axes[0][1].set_title(f"{TARGET_COL}: promo vs no promo",
							 fontweight="bold")
		axes[0][1].grid(True, alpha=0.3, axis="y")

		plt.tight_layout()
		ctx.savefig(plt, "07_promo_intensity_analysis")

		with_promo = df.loc[df["has_promo"] == 1, TARGET_COL]
		without = df.loc[df["has_promo"] == 0, TARGET_COL]
		nan = float("nan")
		summary = pd.DataFrame({
			"metric": ["mean intensity", "median intensity", "skewness",
					   "rows with promo", "rows without promo",
					   f"median {TARGET_COL} (promo)",
					   f"median {TARGET_COL} (no promo)",
					   "rows with intensity > 1"],
			"value": [
				round(float(df["promo_intensity"].mean()), 4),
				round(float(df["promo_intensity"].median()), 4),
				round(skew, 4),
				int(df["has_promo"].sum()),
				int((1 - df["has_promo"]).sum()),
				round(float(with_promo.median()), 4) if len(with_promo) else nan,
				round(float(without.median()), 4) if len(without) else nan,
				invalid,
			],
		})
		ctx.save(
			summary, "step_2_17_promo_distribution",
			"Promo Intensity Distribution Summary",
			notes=[
				"Promo intensity = promo_units / max(sales_units, 1). The "
				"clip avoids zero-division without the +1 bias that would "
				"inflate the ratio for low-volume brands.",
				f"promo_units is a subset of sales_units in Nielsen's model, "
				f"so an intensity above 1 is a delivery defect: {invalid} "
				f"such row(s) here, reported and left uncorrected (F42).",
				"The boxplot compares the target's level between promoted "
				"and unpromoted brand-months. A visible shift motivates "
				"promo features; overlapping boxes argue they add little.",
				"Descriptive, not causal: promotions are placed on brands "
				"already expected to sell, so this gap is confounded by "
				"selection and cannot be read as promotional uplift.",
				"Complements 3.13, which ranks brands by intensity; this "
				"section characterises the distribution's shape.",
			],
		)


# ============================================================================
# 3.18 -- CORRELATION STRUCTURE (PEARSON vs SPEARMAN)
# ============================================================================

def s18_correlation(ctx: EdaContext) -> None:
	"""Correlation heatmaps + non-linearity flags. Notebook cell 51.

	Cell 51 hardcoded five column names and silently analysed only those it
	happened to find. Open-world here: correlate every numeric measure
	discovered, so a category with columns the notebook never named still
	gets them analysed.
	"""
	@section(ctx, "3.18  CORRELATION STRUCTURE (PEARSON vs SPEARMAN)",
			 requires=(TARGET_COL,))
	def _run():
		import matplotlib.pyplot as plt
		import seaborn as sns

		df = ctx.df
		numeric = [c for c in df.select_dtypes(include="number").columns
				   if c not in (YEAR_COL, MONTH_COL)]
		# Constant columns give undefined correlations and a row of NaN.
		numeric = [c for c in numeric if df[c].nunique(dropna=True) > 1]
		if len(numeric) < 2:
			print("  Fewer than two varying numeric columns; nothing to "
				  "correlate.")
			return

		pearson = df[numeric].corr(method="pearson")
		spearman = df[numeric].corr(method="spearman")

		# Wider figure when many columns survive discovery: CSD has 29
		# measures, Danskvand far fewer.
		size = max(FIGSIZE_LARGE[0], min(24, len(numeric) * 0.7))
		fig, axes = plt.subplots(1, 2, figsize=(size * 2, size), squeeze=False)

		mask = np.zeros_like(pearson, dtype=bool)
		mask[np.triu_indices_from(mask)] = True

		annot = len(numeric) <= 12  # numbers become unreadable beyond this
		sns.heatmap(pearson, mask=mask, annot=annot, fmt=".2f", cmap="BuPu",
					center=0, square=True, linewidths=0.5,
					cbar_kws={"shrink": 0.8}, ax=axes[0][0])
		axes[0][0].set_title("Pearson correlation", fontweight="bold")

		sns.heatmap(spearman, mask=mask, annot=annot, fmt=".2f", cmap="BuPu",
					center=0, square=True, linewidths=0.5,
					cbar_kws={"shrink": 0.8}, ax=axes[0][1])
		axes[0][1].set_title("Spearman correlation (rank-based)",
							 fontweight="bold")

		plt.suptitle(f"{ctx.category} -- correlation matrix",
					 fontweight="bold")
		plt.tight_layout()
		ctx.savefig(plt, "08_correlation_heatmap")

		# Target correlations, plus the Pearson/Spearman gap that flags a
		# monotone-but-non-linear relationship.
		rows = []
		for col in numeric:
			if col == TARGET_COL:
				continue
			pe = float(pearson.loc[TARGET_COL, col])
			sp = float(spearman.loc[TARGET_COL, col])
			rows.append({
				"column": col,
				"pearson_r": round(pe, 4),
				"spearman_r": round(sp, 4),
				"abs_delta": round(abs(sp - pe), 4),
				"non_linear": abs(sp - pe) > 0.1,
			})
		corr_df = (pd.DataFrame(rows)
				   .sort_values("pearson_r", key=lambda s: s.abs(),
								ascending=False))
		n_nonlinear = int(corr_df["non_linear"].sum())

		ctx.save(
			corr_df, "step_2_18_target_correlations",
			f"Correlation with {TARGET_COL}",
			notes=[
				"Pearson measures linear association; Spearman measures "
				"monotone association on ranks. Reporting both is what makes "
				"the comparison in the next bullet possible.",
				f"abs_delta above 0.1 flags a relationship that is monotone "
				f"but not linear -- a candidate for transformation rather "
				f"than a raw feature. {n_nonlinear} column(s) flagged here.",
				"Spearman is the more trustworthy of the two on this data: "
				"the target is right-skewed (see 3.02 and 3.15) and Pearson "
				"is sensitive to the resulting outliers.",
				"These correlations are contemporaneous, not predictive: "
				"the columns are measured in the same month as the target, "
				"so a high value does not by itself establish forecasting "
				"value at t+1.",
				"Descriptive only. No feature is selected or dropped here; "
				"the contract is step 3's output (DEC-EDA-SPLIT).",
			],
		)

		# Redundancy among predictors: |r| > 0.9 pairs are near-duplicates,
		# which is what P0036 F7 is tracking for weighted_dist.
		redundant = []
		for i, a in enumerate(numeric):
			for b in numeric[i + 1:]:
				r = float(pearson.loc[a, b])
				if abs(r) > 0.9:
					redundant.append({"column_a": a, "column_b": b,
									  "pearson_r": round(r, 4)})

		if redundant:
			red_df = (pd.DataFrame(redundant)
					  .sort_values("pearson_r", key=lambda s: s.abs(),
								   ascending=False))
			ctx.derived["redundant_pairs"] = redundant
			ctx.save(
				red_df, "step_2_18_redundant_pairs",
				"Near-Duplicate Column Pairs (|r| > 0.9)",
				notes=[
					"Column pairs correlating above 0.9 carry substantially "
					"the same information; keeping both adds collinearity "
					"without adding signal.",
					"The 0.9 threshold is conventional for near-duplicate "
					"detection and is deliberately stricter than the 0.756 "
					"weighted_dist correlation P0036 F7 tracks -- pairs "
					"listed here are a stronger claim than that one.",
					"Collinearity inflates coefficient variance in linear "
					"models. Tree ensembles tolerate it but split their "
					"importance across the duplicates, which makes the "
					"resulting importance ranking misleading.",
					"Listed for step 3 to act on, not pruned here.",
				],
			)
		else:
			print("\n  No column pairs exceed |r| > 0.9.")


# ============================================================================
# RUNNER
# ============================================================================

SECTIONS = (
	s01_preview, s02_distributions, s03_date_range, s04_structural_break,
	s05_stationarity, s06_brand_stability, s07_zero_sales, s08_seasonality,
	s09_monthly_barplot, s10_decomposition, s11_top_brands, s12_heterogeneity,
	s13_promo_intensity, s14_measure_quality, s15_ecdf, s16_acf_pacf,
	s17_promo_distribution, s18_correlation,
)


def run(category: str, make_plots: bool = True) -> EdaContext:
	"""Execute descriptive EDA for one category. Returns the run context."""
	suppress_warnings()
	category = normalise_category(category)
	paths = get_paths(category)
	paths["tables_dir"].mkdir(parents=True, exist_ok=True)
	if make_plots:
		paths["plots_dir"].mkdir(parents=True, exist_ok=True)
		apply_plot_style()

	print("=" * 80)
	print(f"STEP 2 -- DESCRIPTIVE EDA: {category}")
	print("=" * 80)

	# Rebuild the panel from step 1 rather than reading an intermediate file:
	# step 1 deliberately writes no panel to disk, and re-deriving keeps this
	# step honest about consuming exactly what step 1 produces.
	print("\nRebuilding the analysis panel via step 1...")
	merged = load_merged(category, paths["views_dir"])
	df = load_and_aggregate(merged)
	print(f"  Panel: {len(df):,} rows x {len(df.columns)} columns, "
		  f"{df[BRAND_COL].nunique()} brands")

	ctx = EdaContext(category, df, paths, make_plots=make_plots)
	for section_fn in SECTIONS:
		section_fn(ctx)

	report(ctx)
	return ctx


def report(ctx: EdaContext) -> None:
	"""Summarise what ran, what was skipped, and what failed."""
	print("\n" + "=" * 80)
	print(f"STEP 2 SUMMARY -- {ctx.category}")
	print("=" * 80)
	n_ran = len(SECTIONS) - len(ctx.skipped) - len(ctx.failed)
	print(f"  Sections completed: {n_ran} / {len(SECTIONS)}")
	print(f"  Tables written:     {len(ctx.tables_written)} "
		  f"-> {ctx.paths['tables_dir']}")
	print(f"  Plots written:      {len(ctx.plots_written)} "
		  f"-> {ctx.paths['plots_dir']}")

	if ctx.skipped:
		print(f"\n  Skipped ({len(ctx.skipped)}) -- column(s) absent in this "
			  f"category:")
		for title, missing in ctx.skipped:
			print(f"    {title}")
			print(f"      missing: {', '.join(missing)}")

	if ctx.failed:
		print(f"\n  FAILED ({len(ctx.failed)}):")
		for title, err in ctx.failed:
			print(f"    {title}: {err}")

	print("\n  This step derives no parameters. Its output is evidence for "
		  "Chapter 4;")
	print("  the feature-engineering contract is step 3's responsibility.")


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Descriptive EDA for one Nielsen category."
	)
	parser.add_argument("--category", required=True,
						help="Category to analyse (case-insensitive).")
	parser.add_argument("--no-plots", action="store_true",
						help="Compute tables and statistics without rendering "
							 "figures (faster for a quick check).")
	args = parser.parse_args()

	category = normalise_category(args.category)
	paths = get_paths(category)
	paths["step_output_dir"].mkdir(parents=True, exist_ok=True)
	log_path = paths["step_output_dir"] / f"{paths['slug']}_step_2_console.log"

	with tee_console(log_path):
		ctx = run(category, make_plots=not args.no_plots)

	print(f"\nConsole log: {log_path}")
	# Skips are a normal, reported outcome; only a genuine failure is non-zero.
	return 1 if ctx.failed else 0


if __name__ == "__main__":
	raise SystemExit(main())
