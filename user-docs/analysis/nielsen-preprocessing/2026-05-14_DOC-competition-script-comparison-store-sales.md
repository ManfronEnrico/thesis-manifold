# Competition Script Comparison: Store Sales Visualization vs. CSD EDA

**Source:** "Store Sales. Time Series Forecast & Visualization" — maricinnamon (Kaggle)  
**Date:** 2026-05-14  
**Purpose:** Reference document — what this script does, what we already cover, and code snippets for gaps  
**Action required:** None — this is an exploratory overview only. Execute new cells manually on VPS.

---

## Quick Verdict

The competition script is a well-structured Kaggle notebook covering trend, seasonality, lag features, and ML forecasting. About **half of it is modeling** (linear regression, XGBoost, hybrid models) which is out of scope for EDA. The EDA portions are high quality, and three patterns are **not yet in our expanded script** and are worth adding later.

---

## Section-by-Section Comparison

### Section 3.1 — Linear Regression Trend Line

**What she does:**
Groups sales by week/month, plots raw series in gray, overlays OLS regression line in red using `sns.regplot()`. Separately uses `statsmodels.DeterministicProcess` to extract and forecast the linear trend component.

```python
# Competition: trend overlay
axes[1] = sns.regplot(
    x='time', y='mean', data=df_grouped_train_w,
    scatter_kws=dict(color='0.75'),
    line_kws={"color": "red"}, ax=axes[1]
)

# Competition: DeterministicProcess trend
from statsmodels.tsa.deterministic import DeterministicProcess
dp = DeterministicProcess(index=df_grouped['date'], constant=True, order=1, drop=True)
X = dp.in_sample()
model = LinearRegression(fit_intercept=False)
model.fit(X, y)
y_pred = pd.Series(model.predict(X), index=X.index)
```

**Our coverage:** Cell 4.6 (seasonal decomposition) extracts the trend component from decomposition. We don't plot a raw OLS regression overlay on the time series.

**Gap:** Minor. The decomposition trend in Cell 4.6 is sufficient for our purposes.

**Status:** LOW PRIORITY — decomposition trend already validates this.

---

### Section 3.2 — Lag Feature Visualization

**What she does:**
Creates a 1-step lag feature, then plots Y(t) vs Y(t-1) as a scatter with regression line. Shows serial dependence visually.

```python
def add_lag(df, key, freq, col, lag):
    df_grouped = grouped(df, key, freq, col)
    df_grouped['Lag'] = df_grouped['mean'].shift(lag)
    return df_grouped

axes[0] = sns.regplot(
    x='Lag', y='mean', data=df_grouped_train_w_lag1,
    scatter_kws=dict(color='0.75'),
    line_kws={"color": "red"}, ax=axes[0]
)
```

**Our coverage:** Cell 5.5 shows lag correlations as a table. Cell 5.6 shows ACF/PACF plots. Neither shows the raw scatter of Y(t) vs Y(t-lag).

**Gap:** We show *that* lags are correlated (ACF/PACF) but not *what* the scatter looks like. See Section 4.1 below — the advanced `lagplot()` function addresses this much better.

**Status:** Superseded by Section 4.1.

---

### Section 3.3 — Category Bar Chart (value_counts)

**What she does:**
Counts observations by category (holiday type, store type, city) and plots as bar charts using `sns.barplot()`. Includes pie chart for product family distribution.

**Our coverage:** Cell 3 (brand stability), Cell 4 (seasonal bar chart), Cell 8 (promo analysis) all cover categorical bar plots.

**Status:** NOT APPLICABLE — CSD has no multi-store or multi-category structure.

---

### Section 3.4 — Box Plots by Year

**What she does:**
Plots box plots with year on X-axis, metric on Y-axis, with month as hue color. Shows within-year variance and year-over-year changes.

```python
def plot_boxplot(palette, x, y, hue, ax, title):
    sns.set_theme(style="ticks", palette=palette)
    ax = sns.boxplot(x=x, y=y, hue=hue, ax=ax)
    ax.set_title(title, fontsize=18)

# Year on X, month as hue
plot_boxplot("pastel", df_train['date'].dt.year, df_train['sales'],
             df_train['date'].dt.month, axes[0], "Sales by Year")
```

**Our coverage:** Not present in our script.

**Gap:** Would show how sales variance evolves year-over-year in CSD.

**CSD adaptation:**
```python
monthly_agg = df.groupby(['period_year', 'period_month'])['sales_units'].sum().reset_index()
fig, ax = plt.subplots(figsize=(14, 6))
sns.boxplot(x='period_year', y='sales_units', hue='period_month',
            data=monthly_agg, ax=ax, palette='pastel')
ax.set_title("CSD Sales Distribution by Year (month as hue)", fontsize=14)
ax.set_xlabel("Year")
ax.set_ylabel("Sales Units")
plt.tight_layout()
```

**Status:** MEDIUM PRIORITY — nice for thesis, not critical for parameter validation.

---

### Section 3.5 — Moving Average Overlay ⭐ HIGH PRIORITY

**What she does:**
Plots raw series in light gray (`'0.75'`, `linestyle='dashdot'`) with a rolling mean in green (`linewidth=3`). Uses `min_periods` to handle edges cleanly. Compares different window sizes side by side.

```python
def plot_moving_average(df, key, freq, col, window, min_periods, ax, title):
    df_grouped = grouped(df, key, freq, col)
    moving_average = df_grouped['mean'].rolling(
        window=window, center=True, min_periods=min_periods
    ).mean()
    ax = df_grouped['mean'].plot(color='0.75', linestyle='dashdot', ax=ax, label='Raw')
    ax = moving_average.plot(linewidth=3, color='g', ax=ax, label=f'{window}-period MA')
    ax.set_title(title, fontsize=18)
    ax.legend()

# Usage
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(30, 20))
plot_moving_average(df_trans, 'date', 'W', 'transactions', 7, 4, axes[0], 'Transactions MA')
plot_moving_average(df_train, 'date', 'W', 'sales', 7, 4, axes[1], 'Sales MA')
```

**Our coverage:** Cell 4.6 seasonal decomposition extracts trend but doesn't show raw+MA overlay.

**Gap:** We justify `ROLLING_WINDOWS = (4, 13)` with a table but never *visualize* those windows on actual CSD data. A side-by-side of 4-month MA vs 13-month MA would directly validate the parameter choice.

**CSD adaptation (new Cell 6.5):**
```python
# %% [markdown]
# ## Cell 6.5: Moving Average Comparison — Validating ROLLING_WINDOWS = (4, 13)

# %%
PLOT_COLOR = '#386B7F'

monthly = df.groupby(['period_year', 'period_month'])['sales_units'].sum().reset_index()
monthly = monthly.sort_values(['period_year', 'period_month']).reset_index(drop=True)
series = monthly['sales_units']
x_index = range(len(series))

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(18, 10), sharex=True)
fig.suptitle("Rolling Window Comparison — CSD Aggregate Sales", fontsize=14, fontweight='bold')

for ax, window, min_p in zip(axes, [4, 13], [2, 7]):
    ma = series.rolling(window=window, center=True, min_periods=min_p).mean()
    ax.plot(x_index, series, color='0.75', linestyle='dashdot', linewidth=1, label='Raw monthly')
    ax.plot(x_index, ma, color=PLOT_COLOR, linewidth=3, label=f'{window}-month MA')
    ax.set_title(f"{window}-Month Moving Average ({'Nielsen period' if window==4 else 'Quarterly'})",
                 fontsize=12)
    ax.set_ylabel("Sales Units")
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

axes[-1].set_xlabel("Month index")
plt.tight_layout()
plt.savefig(PLOTS_DIR / 'rolling_window_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("✓ Rolling window comparison saved")
```

---

### Section 3.7 — Seasonal Plot (Year-over-Year Lines) ⭐ HIGH PRIORITY

**What she does:**
This is the most distinctive pattern in the script. Each year is a separate colored line, X-axis = month, Y-axis = sales. Lines are annotated at the right edge with year labels using `ax.annotate()`. Uses `husl` palette for visually distinct year colors.

```python
def seasonal_plot(X, y, period, freq, ax=None):
    palette = sns.color_palette("husl", n_colors=X[period].nunique())
    ax = sns.lineplot(
        x=X[freq], y=X[y], hue=X[period],
        ax=ax, palette=palette, legend=False
    )
    ax.set_title(f"Seasonal Plot ({period}/{freq})")
    # Annotate each line at right edge with year/period label
    for line, name in zip(ax.lines, X[period].unique()):
        y_ = line.get_ydata()[-1]
        ax.annotate(
            name,
            xy=(1, y_), xytext=(6, 0),
            color=line.get_color(),
            xycoords=ax.get_yaxis_transform(),
            textcoords="offset points",
            size=14, va="center"
        )
    return ax

# Build features and call
X["day"] = X.index.dayofweek
X["week"] = pd.Int64Index(X.index.isocalendar().week)
X["dayofyear"] = X.index.dayofyear
X["year"] = X.index.year
seasonal_plot(X, y='mean', period="year", freq="dayofyear", ax=ax1)
```

**Our coverage:** Cell 4 shows aggregate monthly means. Cell 4.5 shows a bar chart of those aggregates. Neither shows year-over-year consistency.

**Gap:** A YoY plot shows whether holiday months {3,6,12} peak *consistently each year* — far stronger thesis evidence than an aggregate peak alone.

**CSD adaptation (new Cell 4.7):**
```python
# %% [markdown]
# ## Cell 4.7: Year-over-Year Seasonal Pattern — Validating HOLIDAY_MONTHS consistency

# %%
PLOT_COLOR = '#386B7F'

monthly = df.groupby(['period_year', 'period_month'])['sales_units'].sum().reset_index()
years = sorted(monthly['period_year'].unique())
palette = sns.color_palette("husl", n_colors=len(years))

fig, ax = plt.subplots(figsize=(14, 7))

for year, color in zip(years, palette):
    year_data = monthly[monthly['period_year'] == year].sort_values('period_month')
    if len(year_data) == 0:
        continue
    ax.plot(year_data['period_month'], year_data['sales_units'],
            color=color, linewidth=2, marker='o', markersize=4)
    # Annotate year label at right edge
    last_month = year_data['period_month'].iloc[-1]
    last_val = year_data['sales_units'].iloc[-1]
    ax.annotate(str(year),
                xy=(last_month, last_val),
                xytext=(6, 0),
                textcoords="offset points",
                color=color, va="center", fontsize=11, fontweight='bold')

# Mark holiday months with vertical bands
for hm in [3, 6, 12]:
    ax.axvspan(hm - 0.4, hm + 0.4, alpha=0.08, color='red', label='_nolegend_')

ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'])
ax.set_title("Year-over-Year Seasonal Pattern — CSD Sales Units\n"
             "(red bands = HOLIDAY_MONTHS {3, 6, 12})",
             fontsize=13, fontweight='bold')
ax.set_xlabel("Month")
ax.set_ylabel("Sales Units")
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / 'seasonal_yoy_plot.png', dpi=150, bbox_inches='tight')
plt.show()
print("✓ Year-over-year seasonal plot saved")
```

---

### Section 3.7 — Periodogram

**What she does:**
Computes power spectrum using `scipy.signal.periodogram`, plots on log-scale X-axis with human-readable period labels (Annual, Semiannual, Quarterly, Monthly, etc.). Confirms which frequency components dominate.

```python
def plot_periodogram(ts, detrend='linear', ax=None):
    from scipy.signal import periodogram
    fs = pd.Timedelta("365D") / pd.Timedelta("1D")  # daily data → fs=365
    frequencies, spectrum = periodogram(ts, fs=fs, detrend=detrend,
                                        window="boxcar", scaling='spectrum')
    ax.step(frequencies, spectrum, color="purple")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 6, 12, 26, 52, 104])
    ax.set_xticklabels(["Annual (1)", "Semiannual (2)", "Quarterly (4)",
                        "Bimonthly (6)", "Monthly (12)", "Biweekly (26)",
                        "Weekly (52)", "Semiweekly (104)"], rotation=30)
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylabel("Variance")
    ax.set_title("Periodogram")
```

**Our coverage:** Not present.

**Gap:** For our monthly CSD data, the periodogram confirms which frequency components dominate (annual? quarterly?). The X-axis labels need adapting since CSD is monthly not daily.

**CSD adaptation:**
```python
# %% [markdown]
# ## Cell 4.8 (optional): Periodogram — Frequency Spectrum of CSD Sales

# %%
try:
    from scipy.signal import periodogram as sig_periodogram

    monthly = df.groupby(['period_year', 'period_month'])['sales_units'].sum().reset_index()
    monthly = monthly.sort_values(['period_year', 'period_month'])
    series = monthly['sales_units'].dropna().values

    fs = 12  # monthly data → 12 observations per year
    frequencies, spectrum = sig_periodogram(series, fs=fs, detrend='linear',
                                            window="boxcar", scaling='spectrum')

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.step(frequencies, spectrum, color="purple", linewidth=1.5)
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 6, 12])
    ax.set_xticklabels(["Annual\n(1/yr)", "Semiannual\n(2/yr)",
                        "Quarterly\n(4/yr)", "Bimonthly\n(6/yr)",
                        "Monthly\n(12/yr)"], rotation=30)
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylabel("Variance")
    ax.set_title("Periodogram — CSD Sales Frequency Spectrum", fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'frequency_spectrum.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✓ Periodogram saved")
except ImportError:
    print("⚠ scipy not available — skipping periodogram")
```

**Status:** MEDIUM PRIORITY — adds statistical confirmation of which seasonality frequencies dominate.

---

### Section 4.1 — Advanced Lag Scatter Grid ⭐ HIGH PRIORITY

**What she does:**
A grid of scatter plots showing Y(t) vs Y(t-k) for k=1..N, with:
- LOWESS regression curve (non-parametric — doesn't assume linearity)
- Correlation coefficient annotated in top-left corner via `AnchoredText`
- Shared axes for easy cross-lag comparison

```python
def lagplot(x, y=None, lag=1, standardize=False, ax=None, **kwargs):
    from matplotlib.offsetbox import AnchoredText
    x_ = x.shift(lag)
    if standardize:
        x_ = (x_ - x_.mean()) / x_.std()
    if y is not None:
        y_ = (y - y.mean()) / y.std() if standardize else y
    else:
        y_ = x
    corr = y_.corr(x_)
    scatter_kws = dict(alpha=0.75, s=3)
    line_kws = dict(color='C3')
    ax = sns.regplot(x=x_, y=y_, scatter_kws=scatter_kws,
                     line_kws=line_kws, lowess=True, ax=ax, **kwargs)
    # Annotate correlation coefficient in a box
    at = AnchoredText(f"{corr:.2f}", prop=dict(size="large"),
                      frameon=True, loc="upper left")
    at.patch.set_boxstyle("square, pad=0.0")
    ax.add_artist(at)
    ax.set(title=f"Lag {lag}", xlabel=x_.name, ylabel=y_.name)
    return ax


def plot_lags(x, y=None, lags=6, nrows=1, lagplot_kwargs={}, **kwargs):
    import math
    kwargs.setdefault('nrows', nrows)
    kwargs.setdefault('ncols', math.ceil(lags / nrows))
    kwargs.setdefault('figsize', (kwargs['ncols'] * 2 + 10, nrows * 2 + 5))
    fig, axs = plt.subplots(sharex=True, sharey=True, squeeze=False, **kwargs)
    for ax, k in zip(fig.get_axes(), range(kwargs['nrows'] * kwargs['ncols'])):
        if k + 1 <= lags:
            ax = lagplot(x, y, lag=k + 1, ax=ax, **lagplot_kwargs)
            ax.set_title(f"Lag {k + 1}", fontdict=dict(fontsize=14))
            ax.set(xlabel="", ylabel="")
        else:
            ax.axis('off')
    plt.setp(axs[-1, :], xlabel=x.name)
    plt.setp(axs[:, 0], ylabel=y.name if y is not None else x.name)
    fig.tight_layout(w_pad=0.1, h_pad=0.1)
    return fig

# Usage — lags 1–8 in a 2×4 grid
_ = plot_lags(y_deseason, lags=8, nrows=2)
```

**Our coverage:** Cell 5.5 shows lag correlations as a table. Cell 5.6 shows ACF/PACF bar charts. Neither shows the scatter shape.

**Gap:** ACF/PACF shows *which* lags are significant. The lag scatter grid shows *what the relationship looks like* — is it linear? curved? LOWESS makes no linearity assumption, making this more defensible in a thesis context.

**CSD adaptation (new Cell 5.4 — top 1 brand):**
```python
# %% [markdown]
# ## Cell 5.4: Lag Scatter Grid — Validating LAG_WINDOWS dependency structure

# %%
import math
from matplotlib.offsetbox import AnchoredText

PLOT_COLOR = '#386B7F'

def lagplot_csd(series, lag=1, ax=None):
    x_ = series.shift(lag)
    corr = series.corr(x_)
    ax = sns.regplot(
        x=x_, y=series,
        scatter_kws=dict(alpha=0.6, s=8, color=PLOT_COLOR),
        line_kws=dict(color='C3'),
        lowess=True, ax=ax
    )
    at = AnchoredText(f"r={corr:.2f}", prop=dict(size=10),
                      frameon=True, loc="upper left")
    at.patch.set_boxstyle("square, pad=0.0")
    ax.add_artist(at)
    ax.set_title(f"Lag {lag}", fontsize=12)
    return ax


# Use top brand by total sales volume
top_brand = df.groupby('brand')['sales_units'].sum().idxmax()
brand_data = (df[df['brand'] == top_brand]
              .sort_values(['period_year', 'period_month'])['sales_units']
              .reset_index(drop=True)
              .rename(top_brand))

lags = 8
nrows, ncols = 2, 4
fig, axs = plt.subplots(nrows=nrows, ncols=ncols,
                        figsize=(ncols * 3 + 2, nrows * 3),
                        sharex=True, sharey=True, squeeze=False)
fig.suptitle(f"Lag Scatter Grid — {top_brand} Monthly Sales (Lags 1–{lags})\n"
             f"LOWESS curve + correlation coefficient",
             fontsize=13, fontweight='bold')

for ax, k in zip(fig.get_axes(), range(nrows * ncols)):
    if k + 1 <= lags:
        lagplot_csd(brand_data, lag=k + 1, ax=ax)
    else:
        ax.axis('off')

plt.setp(axs[-1, :], xlabel="Sales (t-lag)")
plt.setp(axs[:, 0], ylabel="Sales (t)")
fig.tight_layout(w_pad=0.1, h_pad=0.1)
plt.savefig(PLOTS_DIR / 'lag_scatter_grid.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"✓ Lag scatter grid saved ({top_brand}, lags 1–{lags})")
```

---

### Sections 5–6 — Hybrid Models and ML Forecasting

**What she does:** Implements BoostedHybrid (LinearRegression + XGBoost), DirRec multi-step forecasting with RegressorChain.

**Status:** NOT APPLICABLE — entirely out of scope for EDA phase.

---

## Summary Table

| Competition Section | Our Coverage | Gap Level | Priority |
|---|---|---|---|
| 3.1 Linear regression trend | Cell 4.6 (decomposition trend) | Minor | Low — skip |
| 3.2 Basic lag scatter | Cell 5.5 (table) | Partial | Superseded by 4.1 |
| 3.3 Category bar charts | Cell 4.5, 8 | None | Not applicable |
| 3.4 Box plots by year | Not present | Medium | Medium — add later |
| **3.5 Moving average overlay** | Not present | **High** | **High — add Cell 6.5** |
| **3.7 Seasonal YoY line plot** | Not present | **High** | **High — add Cell 4.7** |
| 3.7 Periodogram | Not present | Medium | Medium — add Cell 4.8 |
| **4.1 Lag scatter grid (LOWESS)** | Not present | **High** | **High — add Cell 5.4** |
| 5–6 ML modeling | N/A | — | Out of scope |

---

## Three High-Priority Cells to Add

When ready to implement on VPS, insert these three cells into
`thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_enhanced_with_visualizations_expanded.py`:

| New Cell | Insert After | Output File | What It Validates |
|---|---|---|---|
| **Cell 4.7** | Cell 4.6 | `seasonal_yoy_plot.png` | HOLIDAY_MONTHS consistency across all years |
| **Cell 5.4** | Cell 5 (top brands) | `lag_scatter_grid.png` | Lag dependency shape — top brand, lags 1–8 |
| **Cell 6.5** | Cell 6 | `rolling_window_comparison.png` | ROLLING_WINDOWS = (4, 13) visual side-by-side |

Total visualization count: **8 → 11 plots**

---

**Status:** Reference only — code snippets ready to copy-paste on VPS  
**Last Updated:** 2026-05-14
