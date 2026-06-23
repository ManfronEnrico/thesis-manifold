# Per-category EDA under DVH EXCL. HD (2026-06-23)

Recomputed locally from the regenerated feature matrices (DVH EXCL. HD,
MIN_PERIODS=30). Material for Ch4 §4.3.

## Distribution / seasonality / promo

| Category | Promo corr (sales~promo) | Peak month | Top brand | Total units |
|---|---|---|---|---|
| CSD | r=0.937 (n=2442) | December | HARBOE | 6.87B |
| danskvand | no promo (all zero) | June | HARBOE | 0.14B |
| energidrikke | r=0.988 (n=887) | March | RED BULL | 0.30B |
| RTD | no promo (all zero) | December | BREEZER | 0.10B |

## Stationarity (ADF) and autocorrelation (ACF, brand-demeaned log)

| Category | ADF log-level p | Verdict | ADF Δlog p | ACF lag1 | ACF lag3 | ACF lag13 |
|---|---|---|---|---|---|---|
| CSD | 0.421 | non-stationary, I(1) | 0.0000 | +0.78 | +0.55 | −0.15 |
| danskvand | 0.998 | non-stationary, I(1) | 0.0004 | +0.55 | +0.25 | +0.05 |
| energidrikke | 0.901 | non-stationary, I(1) | 0.0000 | +0.71 | +0.39 | −0.12 |
| RTD | 0.000 | stationary in level | 0.0000 | +0.82 | +0.58 | +0.00 |

## Reading

- Log transform is used for variance stabilisation; the **mean** is handled by
  differencing / lag features. Three of four category-level series are I(1)
  (non-stationary in log level, stationary after first differencing); RTD is
  already stationary in log level.
- Strong positive short-horizon autocorrelation (lag1 +0.55..+0.82, lag3
  +0.25..+0.58) justifies the lag_{1,2,3,4} and rolling features. Lag-13 is near
  zero or slightly negative, consistent with annual mean-reversion rather than a
  strong 12-month carry.
- Seasonality is sensible per category (CSD/RTD December, danskvand June for
  water, energidrikke March), supporting the calendar features
  (month/quarter/holiday_month).
- danskvand and RTD carry no promotional data (all-zero promo column) — an
  unmeasured-variable coverage limitation, to be framed as such in Ch4.

## Caveat

CSD ADF p=0.421 reproduces the earlier audit value exactly. ACF magnitudes here
use a pooled brand-demeaned log series; an alternative per-brand-averaged ACF
(used in an earlier note) gives smaller lag1 values — method to be stated when
finalising §4.3. The qualitative conclusions (I(1), positive short-lag
autocorrelation, seasonality) are robust to the method.
