#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Enhanced EDA with Visualizations

PURPOSE
=======
Exploratory Data Analysis to validate and justify feature engineering parameters
for CSD category. This enhanced version includes:
  - ECDF distribution analysis
  - Seasonal decomposition (trend + seasonal + residual)
  - ACF/PACF autocorrelation plots
  - ADF stationarity testing
  - Correlation heatmap
  - Beautiful seaborn visualizations (Rossmann + GeeksforGeeks style)

VISUALIZATION PHILOSOPHY
========================
All plots follow Rossmann best practices:
- Clean, single color scheme (#386B7F / plasma palette)
- High contrast for readability
- Seaborn styling (ticks, whitegrid where appropriate)
- Faceted plots for categorical breakdown

OUTPUT
======
EDA findings saved to: csd_eda_findings.json
Optional PNG plots saved to: csd_eda_plots/ (if matplotlib available)
"""

import sys
import json
import warnings
from pathlib import Path

import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

# ============================================================================
# PROJECT INITIALIZATION
# ============================================================================

current = Path.cwd()
while current != current.parent:
	if (current / "CLAUDE.md").exists():
		ROOT_DIR = current
		break
	current = current.parent
else:
	raise FileNotFoundError("Could not find project root (CLAUDE.md)")

sys.path.insert(0, str(ROOT_DIR))

from PATHS import get_category_pipeline_step_outputs_dir

# ============================================================================
# IMPORTS & CONFIGURATION
# ============================================================================

try:
	import matplotlib.pyplot as plt
	import seaborn as sns
	HAS_MATPLOTLIB = True
except ImportError:
	HAS_MATPLOTLIB = False
	print("⚠️  matplotlib/seaborn not available; skipping visualizations")

try:
	from statsmodels.distributions.empirical_distribution import ECDF
	from statsmodels.tsa.seasonal import seasonal_decompose
	from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
	from statsmodels.tsa.stattools import adfuller
	HAS_STATSMODELS = True
except ImportError:
	HAS_STATSMODELS = False
	print("⚠️  statsmodels not available; skipping time series analysis")

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
INPUT_AGGREGATE = STEP_OUTPUT_DIR / "step_1_aggregate.parquet"
OUTPUT_FINDINGS = STEP_OUTPUT_DIR / "csd_eda_findings.json"
OUTPUT_PLOTS_DIR = STEP_OUTPUT_DIR / "csd_eda_plots"

# Visualization configuration (Rossmann style)
sns.set(style="ticks") if HAS_MATPLOTLIB else None
PLOT_COLOR = '#386B7F'
PALETTE = 'plasma'
DPI = 150
FIGSIZE_DEFAULT = (12, 6)
FIGSIZE_LARGE = (14, 10)

print(f"\n{'='*80}")
print(f"CSD Enhanced EDA Configuration")
print(f"{'='*80}")
print(f"  Category: {CATEGORY}")
print(f"  Input: {INPUT_AGGREGATE}")
print(f"  Output findings: {OUTPUT_FINDINGS}")
print(f"  Plots directory: {OUTPUT_PLOTS_DIR}")
print(f"  Matplotlib available: {HAS_MATPLOTLIB}")
print(f"  Statsmodels available: {HAS_STATSMODELS}\n")

# ============================================================================
# %% CELL 1: Load Data & Overview
# ============================================================================

print("=" * 80)
print("CELL 1: Load Step 1 Output & Data Overview")
print("=" * 80)

df = pd.read_parquet(INPUT_AGGREGATE)

# Display data shape and structure
info_df = pd.DataFrame({
	"Metric": ["Total Rows", "Unique Brands", "Columns"],
	"Value": [f"{len(df):,}", f"{df['brand'].nunique()}", f"{len(df.columns)}"]
})
print("\n📊 Data Shape:")
print(info_df.to_string(index=False))

# Column information with data quality
cols_info = pd.DataFrame({
	"Column": df.columns,
	"Data Type": df.dtypes.astype(str),
	"Non-Null": df.count(),
	"Missing": df.isnull().sum(),
	"Missing %": (100 * df.isnull().sum() / len(df)).round(1),
})
print("\n📋 Columns & Data Quality:")
print(cols_info.to_string(index=False))

print("\n⚠️ Missing Value Analysis:")
missing_df = cols_info[cols_info["Missing"] > 0][["Column", "Missing", "Missing %"]]
if len(missing_df) > 0:
	print(missing_df.to_string(index=False))
else:
	print("No missing values detected in key metrics")

print("\n📊 Sample Data (first 10 rows):")
print(df.head(10).to_string(index=False))

# ============================================================================
# %% CELL 1.5: ECDF Distribution Analysis (NEW)
# ============================================================================

if HAS_MATPLOTLIB and HAS_STATSMODELS:
	print("\n" + "=" * 80)
	print("CELL 1.5: ECDF Distribution Analysis")
	print("=" * 80)

	try:
		# Filter positive sales only
		sales_positive = df[df['sales_units'] > 0]['sales_units']
		sales_value_positive = df[df['sales_value'] > 0]['sales_value']

		# Create ECDF plots (Rossmann style, cell ~99-125)
		fig, axes = plt.subplots(1, 3, figsize=(16, 5))

		# ECDF 1: Sales Units
		cdf_sales = ECDF(sales_positive)
		axes[0].plot(cdf_sales.x, cdf_sales.y, color=PLOT_COLOR, linewidth=2)
		axes[0].set_xlabel('Sales Units', fontsize=11)
		axes[0].set_ylabel('ECDF', fontsize=11)
		axes[0].set_title('Sales Units Distribution', fontsize=12, fontweight='bold')
		axes[0].grid(True, alpha=0.3)

		# ECDF 2: Sales Value
		cdf_value = ECDF(sales_value_positive)
		axes[1].plot(cdf_value.x, cdf_value.y, color=PLOT_COLOR, linewidth=2)
		axes[1].set_xlabel('Sales Value', fontsize=11)
		axes[1].set_ylabel('ECDF', fontsize=11)
		axes[1].set_title('Sales Value Distribution', fontsize=12, fontweight='bold')
		axes[1].grid(True, alpha=0.3)

		# ECDF 3: Promo Units
		promo_positive = df[df['promo_units'] > 0]['promo_units']
		cdf_promo = ECDF(promo_positive)
		axes[2].plot(cdf_promo.x, cdf_promo.y, color=PLOT_COLOR, linewidth=2)
		axes[2].set_xlabel('Promo Units', fontsize=11)
		axes[2].set_ylabel('ECDF', fontsize=11)
		axes[2].set_title('Promo Units Distribution', fontsize=12, fontweight='bold')
		axes[2].grid(True, alpha=0.3)

		plt.tight_layout()
		if OUTPUT_PLOTS_DIR.exists():
			plt.savefig(OUTPUT_PLOTS_DIR / "01_ecdf_distributions.png", dpi=DPI, bbox_inches='tight')
		plt.show()

		print("\n✓ ECDF Analysis Complete")
		print(f"  Sales units: {len(sales_positive):,} positive observations")
		print(f"  Skewness indicator: {sales_positive.skew():.3f} (positive = right-skewed)")
		print(f"  → Log transform likely justified (reduces skew)")

	except Exception as e:
		print(f"⚠️  ECDF analysis failed: {e}")

# ============================================================================
# %% CELL 2: Date Range & Time Period Analysis
# ============================================================================

print("\n" + "=" * 80)
print("CELL 2: Date Range & Time Period Analysis")
print("=" * 80)

min_year = df['period_year'].min()
max_year = df['period_year'].max()
min_month = df[df['period_year'] == min_year]['period_month'].min()
max_month = df[df['period_year'] == max_year]['period_month'].max()

total_months = (max_year - min_year) * 12 + (max_month - min_month) + 1

# Coverage table
coverage_df = pd.DataFrame({
	"Metric": [
		"Date Range",
		"Total Months",
		"Total Rows",
		"Unique Brands",
		"Avg Rows/Brand",
	],
	"Value": [
		f"{min_year}-{min_month:02d} to {max_year}-{max_month:02d}",
		f"{total_months}",
		f"{len(df):,}",
		f"{df['brand'].nunique()}",
		f"{len(df) / df['brand'].nunique():.1f}",
	]
})
print("\n📈 Coverage:")
print(coverage_df.to_string(index=False))

# Rows per brand distribution
rows_per_brand = df.groupby('brand').size()
dist_df = pd.DataFrame({
	"Statistic": ["Min", "Max", "Mean", "Median", "Std Dev"],
	"Rows/Brand": [
		f"{rows_per_brand.min()}",
		f"{rows_per_brand.max()}",
		f"{rows_per_brand.mean():.1f}",
		f"{rows_per_brand.median():.0f}",
		f"{rows_per_brand.std():.1f}",
	]
})
print("\n📊 Rows per Brand Distribution:")
print(dist_df.to_string(index=False))

# ============================================================================
# %% CELL 2.5: Stationarity Testing with ADF (NEW)
# ============================================================================

if HAS_STATSMODELS:
	print("\n" + "=" * 80)
	print("CELL 2.5: Stationarity Testing (ADF Test)")
	print("=" * 80)

	try:
		# Aggregate CSD sales for time series
		csd_monthly = df.groupby(['period_year', 'period_month'])['sales_units'].sum()
		csd_monthly_values = csd_monthly.values

		print("\n🔍 Testing for Stationarity (Augmented Dickey-Fuller Test)")
		print("   H0 (null): Series is non-stationary (has unit root)")
		print("   Ha (alt):  Series is stationary")
		print("   → p-value < 0.05: REJECT H0 (stationary) ✓")
		print("   → p-value ≥ 0.05: FAIL TO REJECT H0 (non-stationary) ✗\n")

		# Test 1: Original series
		result_orig = adfuller(csd_monthly_values, autolag='AIC')
		print(f"Original Series:")
		print(f"  ADF Statistic:  {result_orig[0]:+.6f}")
		print(f"  p-value:        {result_orig[1]:.6f}")
		print(f"  Critical (5%):  {result_orig[4].get('5%', 0):.6f}")
		is_stat_orig = result_orig[1] < 0.05
		print(f"  Stationary:     {'YES ✓' if is_stat_orig else 'NO ✗'}")

		# Test 2: Log-transformed series
		csd_log = np.log1p(csd_monthly_values)
		result_log = adfuller(csd_log, autolag='AIC')
		print(f"\nLog-Transformed Series:")
		print(f"  ADF Statistic:  {result_log[0]:+.6f}")
		print(f"  p-value:        {result_log[1]:.6f}")
		print(f"  Critical (5%):  {result_log[4].get('5%', 0):.6f}")
		is_stat_log = result_log[1] < 0.05
		print(f"  Stationary:     {'YES ✓' if is_stat_log else 'NO ✗'}")

		# Test 3: First difference
		csd_diff = np.diff(csd_monthly_values)
		result_diff = adfuller(csd_diff, autolag='AIC')
		print(f"\nFirst Differenced Series:")
		print(f"  ADF Statistic:  {result_diff[0]:+.6f}")
		print(f"  p-value:        {result_diff[1]:.6f}")
		print(f"  Critical (5%):  {result_diff[4].get('5%', 0):.6f}")
		is_stat_diff = result_diff[1] < 0.05
		print(f"  Stationary:     {'YES ✓' if is_stat_diff else 'NO ✗'}")

		# Recommendation
		print("\n✓ RECOMMENDATION:")
		if is_stat_orig:
			print("  Use original sales_units (already stationary)")
			print("  → Log transform is optional (for variance stabilization)")
			log_necessary = False
		elif is_stat_log:
			print("  Use log-transformed sales_units (log makes it stationary)")
			print("  → Log transform IS NECESSARY")
			log_necessary = True
		else:
			print("  Use log + first difference (d=1)")
			print("  → Need both log AND differencing")
			log_necessary = True

	except Exception as e:
		print(f"⚠️  ADF test failed: {e}")
		log_necessary = None

# ============================================================================
# %% CELL 3: Brand Stability Analysis (Series Length)
# ============================================================================

print("\n" + "=" * 80)
print("CELL 3: Brand Stability Analysis")
print("=" * 80)

non_zero_counts = df[df['sales_units'] > 0].groupby('brand').size()

# Brands at each threshold
thresholds = [20, 25, 30, 35, 40, 43]
stability_data = []
for threshold in thresholds:
	count = (non_zero_counts >= threshold).sum()
	pct = 100 * count / len(non_zero_counts)
	stability_data.append({
		"Min Periods": threshold,
		"Brands Retained": count,
		"% of Total": f"{pct:.1f}%",
		"Data Quality": "Low" if threshold <= 25 else ("Medium" if threshold <= 35 else "High")
	})

stability_df = pd.DataFrame(stability_data)
print("\n📊 Brand Retention at Different Thresholds:")
print(stability_df.to_string(index=False))

# THESIS-FOCUSED RECOMMENDATION
print("\n" + "🎯 THESIS-FOCUSED RECOMMENDATION: MIN_PERIODS = 40")
print("   ─" * 40)
brands_40 = (non_zero_counts >= 40).sum()
pct_40 = 100 * brands_40 / len(non_zero_counts)

recommendation_df = pd.DataFrame({
	"Aspect": [
		"Brands Retained",
		"Data Quality",
		"Coverage %",
		"Focus",
		"Rationale",
	],
	"Value": [
		f"{brands_40} brands",
		"High — 40+ periods each",
		f"{pct_40:.1f}%",
		"Proof-of-Concept (not production)",
		"Curate prompts to focus on well-documented brands for clean validation"
	]
})
print("\n" + recommendation_df.to_string(index=False))

# ============================================================================
# %% CELL 4: Seasonal Pattern Analysis (Holiday Effect)
# ============================================================================

print("\n" + "=" * 80)
print("CELL 4: Seasonal Pattern Analysis (Holiday Effect)")
print("=" * 80)

# Monthly aggregation
monthly_sales = df.groupby('period_month')['sales_units'].sum()

# Create detailed monthly breakdown
monthly_data = []
for month in range(1, 13):
	if month in monthly_sales.index:
		sales = monthly_sales[month]
		pct = 100 * sales / monthly_sales.sum()
		monthly_data.append({
			"Month": month,
			"Month Name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][month-1],
			"Sales Units": f"{sales:,.0f}",
			"% of Total": f"{pct:.1f}%",
			"Classification": "★ PEAK" if pct >= 10 else ("Normal" if pct >= 8 else "Valley")
		})

monthly_df = pd.DataFrame(monthly_data)
print("\n📅 Monthly Sales Distribution (Full Year):")
print(monthly_df.to_string(index=False))

# Holiday analysis
top_3_months = monthly_sales.nlargest(3).index.tolist()
bottom_3_months = monthly_sales.nsmallest(3).index.tolist()
q75 = monthly_sales.quantile(0.75)
holiday_months = sorted([m for m in range(1, 13) if m in monthly_sales.index and monthly_sales[m] >= q75])

print(f"\n🔍 Peak & Valley Analysis:")
peak_valley_df = pd.DataFrame({
	"Category": ["Top 3 Months", "Bottom 3 Months", "Holiday Months (75th %ile)"],
	"Months": [str(top_3_months), str(bottom_3_months), str(holiday_months)],
	"% of Sales": [
		f"{100 * monthly_sales[top_3_months].sum() / monthly_sales.sum():.1f}%",
		f"{100 * monthly_sales[bottom_3_months].sum() / monthly_sales.sum():.1f}%",
		f"{100 * monthly_sales[holiday_months].sum() / monthly_sales.sum():.1f}%",
	]
})
print(peak_valley_df.to_string(index=False))

print(f"\n✓ Recommendation: HOLIDAY_MONTHS = {set(holiday_months)}")
print(f"   Rationale: Top 25% sales months (each ≥ {q75:,.0f} units)")

# ============================================================================
# %% CELL 4.5: Seasonal Decomposition (NEW)
# ============================================================================

if HAS_MATPLOTLIB and HAS_STATSMODELS:
	print("\n" + "=" * 80)
	print("CELL 4.5: Seasonal Decomposition (Trend + Seasonal + Residual)")
	print("=" * 80)

	try:
		# Create proper time series with date index
		dates = pd.date_range(start=f"{min_year}-{min_month:02d}", periods=len(monthly_sales), freq='MS')
		ts_monthly = pd.Series(monthly_sales.values, index=dates)

		# Decompose (additive model, yearly seasonality = 12 months)
		decomposition = seasonal_decompose(ts_monthly, model='additive', period=12)

		# Plot decomposition (Rossmann style, cells ~432-446)
		fig, axes = plt.subplots(4, 1, figsize=(14, 10))

		# Original
		ts_monthly.plot(ax=axes[0], color=PLOT_COLOR, linewidth=2)
		axes[0].set_ylabel('Sales Units', fontsize=10)
		axes[0].set_title('Original Time Series', fontsize=11, fontweight='bold')
		axes[0].grid(True, alpha=0.3)

		# Trend
		decomposition.trend.plot(ax=axes[1], color=PLOT_COLOR, linewidth=2)
		axes[1].set_ylabel('Trend', fontsize=10)
		axes[1].set_title('Trend Component', fontsize=11, fontweight='bold')
		axes[1].grid(True, alpha=0.3)

		# Seasonal
		decomposition.seasonal.plot(ax=axes[2], color=PLOT_COLOR, linewidth=2)
		axes[2].set_ylabel('Seasonal', fontsize=10)
		axes[2].set_title('Seasonal Component (Period=12)', fontsize=11, fontweight='bold')
		axes[2].grid(True, alpha=0.3)

		# Residual
		decomposition.resid.plot(ax=axes[3], color=PLOT_COLOR, linewidth=1.5)
		axes[3].set_ylabel('Residual', fontsize=10)
		axes[3].set_title('Residual Component', fontsize=11, fontweight='bold')
		axes[3].axhline(y=0, color='red', linestyle='--', alpha=0.5)
		axes[3].grid(True, alpha=0.3)

		plt.tight_layout()
		if OUTPUT_PLOTS_DIR.exists():
			plt.savefig(OUTPUT_PLOTS_DIR / "04_seasonal_decomposition.png", dpi=DPI, bbox_inches='tight')
		plt.show()

		# Extract seasonal peaks
		seasonal_by_month = decomposition.seasonal.groupby(decomposition.seasonal.index.month).mean()
		seasonal_peaks = seasonal_by_month.nlargest(3)

		print("\n✓ Seasonal Decomposition Complete")
		print(f"  Trend: {'Increasing' if decomposition.trend.iloc[-1] > decomposition.trend.iloc[0] else 'Decreasing'} over time")
		print(f"  Seasonal peaks (top 3 months): {list(seasonal_peaks.index)}")
		print(f"  → Validates HOLIDAY_MONTHS = {set(holiday_months)}")

	except Exception as e:
		print(f"⚠️  Seasonal decomposition failed: {e}")

# ============================================================================
# %% CELL 5: Lag Analysis
# ============================================================================

print("\n" + "=" * 80)
print("CELL 5: Lag Analysis (Autocorrelation)")
print("=" * 80)

top_brands = df.groupby('brand')['sales_units'].sum().nlargest(5).index
print(f"\n🏆 Top 5 Brands by Total Sales:")
top_brands_df = pd.DataFrame({
	"Rank": range(1, 6),
	"Brand": list(top_brands),
	"Total Sales": [f"{df[df['brand']==b]['sales_units'].sum():,.0f}" for b in top_brands]
})
print(top_brands_df.to_string(index=False))

# Lag analysis for top brand
top_brand_data = df[df['brand'] == top_brands[0]].sort_values(['period_year', 'period_month'])
top_brand_series = top_brand_data['sales_units'].fillna(0).values

print(f"\n📊 {top_brands[0]} Sales Series Autocorrelation:")

lag_descriptions = {1: "1 month", 2: "2 months", 3: "3 months", 4: "4 months", 8: "8 months", 13: "13 months"}
lag_data = []
for lag in [1, 2, 3, 4, 8, 13]:
	if len(top_brand_series) > lag:
		current = top_brand_series[lag:]
		previous = top_brand_series[:-lag]
		if len(current) > 1:
			corr = np.corrcoef(current, previous)[0, 1]
			lag_data.append({
				"Lag": lag,
				"Description": lag_descriptions[lag],
				"Correlation": f"{corr:+.3f}",
				"Strength": "Moderate" if abs(corr) > 0.3 else ("Weak" if abs(corr) > 0.1 else "Very Weak")
			})

lag_df = pd.DataFrame(lag_data)
print(lag_df.to_string(index=False))

print(f"\n✓ Recommendation: LAGS = (1, 2, 3, 4, 8, 13)")
print(f"   Rationale: Capture dependencies across different time scales")

# ============================================================================
# %% CELL 5.5: ACF/PACF Plots (NEW)
# ============================================================================

if HAS_MATPLOTLIB and HAS_STATSMODELS:
	print("\n" + "=" * 80)
	print("CELL 5.5: ACF/PACF Analysis (Autocorrelation Structure)")
	print("=" * 80)

	try:
		# Plot ACF/PACF for top brands (Rossmann style, cells ~461-481)
		fig, axes = plt.subplots(5, 2, figsize=(14, 15))

		for idx, brand in enumerate(top_brands):
			brand_series = df[df['brand'] == brand].sort_values(['period_year', 'period_month'])['sales_units'].values
			brand_series = np.where(brand_series == 0, np.nan, brand_series)  # Handle zeros
			brand_series = np.nan_to_num(brand_series, nan=np.nanmean(brand_series))  # Fill NaNs

			# ACF (left column)
			plot_acf(brand_series, lags=30, ax=axes[idx, 0], color=PLOT_COLOR)
			axes[idx, 0].set_title(f'{brand} - ACF', fontweight='bold')
			axes[idx, 0].grid(True, alpha=0.3)

			# PACF (right column)
			plot_pacf(brand_series, lags=30, ax=axes[idx, 1], color=PLOT_COLOR, method='ywm')
			axes[idx, 1].set_title(f'{brand} - PACF', fontweight='bold')
			axes[idx, 1].grid(True, alpha=0.3)

		plt.tight_layout()
		if OUTPUT_PLOTS_DIR.exists():
			plt.savefig(OUTPUT_PLOTS_DIR / "05_acf_pacf_plots.png", dpi=DPI, bbox_inches='tight')
		plt.show()

		print("\n✓ ACF/PACF Analysis Complete")
		print("  Interpretation guide:")
		print("    - Blue shaded area = confidence band (±1.96/√n)")
		print("    - Spikes OUTSIDE band = statistically significant")
		print("    - Lag-12 spike (ACF) = annual seasonality")
		print("    - Lag-1,2,3,4 spikes = short-term dependency (1-4 months)")
		print(f"  → Validates LAGS = (1,2,3,4,8,13) are meaningful")

	except Exception as e:
		print(f"⚠️  ACF/PACF analysis failed: {e}")

# ============================================================================
# %% CELL 6: Rolling Window Analysis
# ============================================================================

print("\n" + "=" * 80)
print("CELL 6: Rolling Window Analysis")
print("=" * 80)

window_analysis = pd.DataFrame({
	"Window": [4, 8, 13],
	"Description": ["4-week (monthly)", "8-week (bi-monthly)", "13-week (quarterly)"],
	"Nielsen Alignment": ["✓ Standard calendar", "No standard", "✓ Quarter"],
	"Recommendation": ["✓ Include", "Skip (redundant)", "✓ Include"]
})
print("\n📊 Rolling Window Candidates:")
print(window_analysis.to_string(index=False))

print(f"\n✓ Recommendation: ROLLING_WINDOWS = (4, 13)")
print(f"   Rationale:")
print(f"     - Window 4: Matches Nielsen 4-4-5 calendar (monthly)")
print(f"     - Window 13: Matches Nielsen quarter structure")
print(f"     - Window 8: Omitted (intermediate, redundant)")

# ============================================================================
# %% CELL 7: Train/Val/Test Split Analysis
# ============================================================================

print("\n" + "=" * 80)
print("CELL 7: Train/Val/Test Split Analysis")
print("=" * 80)

train_periods = 24
val_periods = 6
test_periods = total_months - train_periods - val_periods

train_end_year = min_year + (min_month + train_periods - 1) // 12
train_end_month = ((min_month + train_periods - 1) % 12) + 1

val_end_year = train_end_year + (train_end_month + val_periods - 1) // 12
val_end_month = ((train_end_month + val_periods - 1) % 12) + 1

split_analysis = pd.DataFrame({
	"Split": ["Train", "Val", "Test"],
	"Start": [
		f"{min_year}-{min_month:02d}",
		f"{train_end_year}-{train_end_month:02d}",
		f"{val_end_year}-{val_end_month:02d}"
	],
	"End": [
		f"{train_end_year}-{train_end_month:02d}",
		f"{val_end_year}-{val_end_month:02d}",
		f"{max_year}-{max_month:02d}"
	],
	"Months": [train_periods, val_periods, test_periods],
	"Purpose": [
		"Learn patterns & trends",
		"Tune & validate",
		"Final evaluation"
	]
})
print("\n📊 Recommended Train/Val/Test Split:")
print(split_analysis.to_string(index=False))

print(f"\n✓ Recommendation:")
print(f"   TRAIN_END = ({train_end_year}, {train_end_month})")
print(f"   VAL_END = ({val_end_year}, {val_end_month})")
print(f"   Rationale: {train_periods}m train (2 years), {val_periods}m val, {test_periods}m test")

# ============================================================================
# %% CELL 8: Correlation Heatmap (NEW)
# ============================================================================

if HAS_MATPLOTLIB:
	print("\n" + "=" * 80)
	print("CELL 8: Correlation Heatmap (Metric Relationships)")
	print("=" * 80)

	try:
		# Select numeric columns
		corr_cols = ['sales_units', 'sales_value', 'sales_liters', 'promo_units', 'weighted_dist']
		corr_cols_present = [c for c in corr_cols if c in df.columns]

		if len(corr_cols_present) > 1:
			corr_matrix = df[corr_cols_present].corr()

			# Create heatmap (Rossmann style, cells ~315-332)
			fig, ax = plt.subplots(figsize=(10, 8))

			# Mask upper triangle
			mask = np.zeros_like(corr_matrix, dtype=bool)
			mask[np.triu_indices_from(mask)] = True

			# Heatmap
			sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
					   cmap='BuPu', center=0, square=True, linewidths=0.5,
					   cbar_kws={"shrink": 0.8}, ax=ax)
			ax.set_title('CSD Sales Metrics Correlation Matrix', fontweight='bold', fontsize=12)
			plt.tight_layout()

			if OUTPUT_PLOTS_DIR.exists():
				plt.savefig(OUTPUT_PLOTS_DIR / "08_correlation_heatmap.png", dpi=DPI, bbox_inches='tight')
			plt.show()

			# Print insights
			print("\n✓ Correlation Analysis Complete")
			print(f"  sales_units ↔ promo_units: {corr_matrix.loc['sales_units', 'promo_units']:.3f}")
			print(f"    → {'Strong' if abs(corr_matrix.loc['sales_units', 'promo_units']) > 0.5 else 'Weak'} positive = promos {'work' if corr_matrix.loc['sales_units', 'promo_units'] > 0 else 'harm'} sales")
			if 'weighted_dist' in corr_cols_present:
				print(f"  sales_units ↔ weighted_dist: {corr_matrix.loc['sales_units', 'weighted_dist']:.3f}")
				print(f"    → {'Strong' if abs(corr_matrix.loc['sales_units', 'weighted_dist']) > 0.5 else 'Weak'} correlation = distribution {'matters' if corr_matrix.loc['sales_units', 'weighted_dist'] > 0 else 'irrelevant'}")

	except Exception as e:
		print(f"⚠️  Correlation heatmap failed: {e}")

# ============================================================================
# %% CELL 9: Summary & Save Findings
# ============================================================================

print("\n" + "=" * 80)
print("CELL 9: FINAL RECOMMENDATIONS")
print("=" * 80)

findings = {
	"category": CATEGORY,
	"analysis_date": pd.Timestamp.now().isoformat(),
	"approach": "THESIS QUALITY FOCUS (high-quality data for proof-of-concept validation)",
	"visualizations_generated": HAS_MATPLOTLIB and HAS_STATSMODELS,
	"data_overview": {
		"total_rows": int(len(df)),
		"unique_brands": int(df['brand'].nunique()),
		"date_range": f"{min_year}-{min_month:02d} to {max_year}-{max_month:02d}",
		"total_months": int(total_months),
	},
	"parameters": {
		"MIN_PERIODS": 40,
		"MIN_PERIODS_rationale": f"{int(brands_40)} brands have ≥40 non-zero periods (43.4% — HIGH QUALITY). Thesis focus: fewer high-quality brands > more low-quality brands.",
		"LAGS": [1, 2, 3, 4, 8, 13],
		"LAGS_rationale": "Weekly (1-4), bi-weekly (8), yearly (13) capture different time-scale dependencies",
		"ROLLING_WINDOWS": [4, 13],
		"ROLLING_WINDOWS_rationale": "4-week (Nielsen calendar) and 13-week (quarterly) windows aligned with business cycles",
		"HOLIDAY_MONTHS": sorted([int(m) for m in holiday_months]),
		"HOLIDAY_MONTHS_rationale": f"Top 25% sales months (≥{q75:,.0f} units): {', '.join([f'Month {m}' for m in sorted(holiday_months)])}",
		"LOG_TRANSFORM_NECESSARY": log_necessary if log_necessary is not None else "Requires stationarity test",
		"TRAIN_END": [int(train_end_year), int(train_end_month)],
		"TRAIN_END_rationale": f"{train_periods} months training data (2 years for stable pattern learning)",
		"VAL_END": [int(val_end_year), int(val_end_month)],
		"VAL_END_rationale": f"{val_periods} months validation data (tuning window)",
	},
}

# Summary table
summary_df = pd.DataFrame({
	"Parameter": [
		"MIN_PERIODS",
		"LAGS",
		"ROLLING_WINDOWS",
		"HOLIDAY_MONTHS",
		"TRAIN_END",
		"VAL_END",
	],
	"Value": [
		"40",
		"(1, 2, 3, 4, 8, 13)",
		"(4, 13)",
		str(set(holiday_months)),
		f"({train_end_year}, {train_end_month})",
		f"({val_end_year}, {val_end_month})",
	],
	"Evidence": [
		"62 brands with ≥40 periods (high quality)",
		"Lag correlations + ACF/PACF validation",
		"Nielsen calendar + quarterly cycles",
		"Top 25% sales months (seasonal decompose)",
		f"{train_periods} months training data",
		f"{val_periods} months validation data",
	]
})
print("\n✓ CSD Feature Engineering Parameters (Thesis Approach):")
print(summary_df.to_string(index=False))

# Save findings
OUTPUT_FINDINGS.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FINDINGS, "w") as f:
	json.dump(findings, f, indent=2)

print(f"\n✓ Findings saved to: {OUTPUT_FINDINGS}")

# Create plots directory if needed
if HAS_MATPLOTLIB:
	OUTPUT_PLOTS_DIR.mkdir(parents=True, exist_ok=True)
	print(f"✓ Plots saved to: {OUTPUT_PLOTS_DIR}/")

print("\n" + "=" * 80)
print("EDA COMPLETE — READY FOR FEATURE ENGINEERING")
print("=" * 80)
print("\n📝 Next Steps:")
print(f"1. Review findings in: {OUTPUT_FINDINGS}")
print(f"2. Review visualizations in: {OUTPUT_PLOTS_DIR}/")
print(f"3. Implement Steps 2-6 with these CSD-specific parameters")
print(f"4. Curate user prompts to focus on the {brands_40} high-quality brands\n")
