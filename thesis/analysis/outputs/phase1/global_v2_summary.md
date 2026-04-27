# Global LightGBM v2 -- Enhanced Features
> Generated: 2026-04-13
> New features: distribution_momentum, yoy_growth, seasonal_index
> Models tested: MSE+log, Tweedie, Average ensemble

## Results Summary

| Model | Median MAPE | P25 | P75 |
|---|---|---|---|
| GlobalLGB_v2_MSE | 26.2% | 18.5% | 43.4% |
| GlobalLGB_v2_Tweedie | 23.8% | 16.4% | 40.9% |
| GlobalLGB_v2_Avg | 22.5% | 16.0% | 42.8% |
| GlobalLGB_v1 (baseline) | 28.2% | - | - |

## Feature Importance (MSE model)

|                       |   importance |
|:----------------------|-------------:|
| weighted_dist         |         1886 |
| price_per_unit        |         1771 |
| rolling_mean_13       |         1447 |
| distribution_momentum |         1376 |
| lag_1                 |         1222 |
| promo_intensity       |         1164 |
| month                 |         1110 |
| brand_enc             |         1104 |
| seasonal_index        |          954 |
| rolling_std_4         |          941 |
| rolling_mean_4        |          918 |
| lag_2                 |          773 |
| lag_3                 |          727 |
| yoy_growth            |          673 |
| lag_4                 |          543 |
| lag_12                |          529 |
| lag_8                 |          513 |
| lag_13                |          393 |
| holiday_month         |          142 |
| quarter               |           34 |

## Key Findings

- New features (distribution_momentum, yoy_growth, seasonal_index) add real predictive value
- Tweedie loss tested as alternative for intermittent demand brands
- Oracle bound (best possible with current features): 27.5%
