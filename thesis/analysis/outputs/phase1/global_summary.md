# Global LightGBM Results -- SRQ1
> Generated: 2026-04-13
> Architecture: 1 model trained on all 77 brands simultaneously
> Training rows: 2,695 (train+val)  |  Test rows: 539

## Summary

| Metric | Global LightGBM | XGBoost (per-brand) |
|---|---|---|
| Median MAPE (test) | 28.2% | 45.6% |
| Volume-weighted MAPE | 28.6% | 38.8% |
| Top-10 brands MAPE | 21.0% | 20.3% |
| Brands where Global wins | 56/77 | 21/77 |

## Feature Importance (Top 10)

|                 |   importance |
|:----------------|-------------:|
| weighted_dist   |         2111 |
| price_per_unit  |         1988 |
| lag_1           |         1515 |
| month           |         1320 |
| brand_enc       |         1310 |
| rolling_mean_13 |         1304 |
| promo_intensity |         1176 |
| rolling_mean_4  |          899 |
| rolling_std_4   |          854 |
| lag_3           |          819 |

## Per-Brand Comparison

| brand               |   test_mape |   xgb_perbrand_mape |           delta | winner       |
|:--------------------|------------:|--------------------:|----------------:|:-------------|
| MACARN              |   227.469   |          9764.02    | -9536.55        | GlobalLGB    |
| EAST IMPERIAL       |   326.349   |          4138.18    | -3811.83        | GlobalLGB    |
| THE PERFECT MIXER   |   168.254   |          1687.03    | -1518.78        | GlobalLGB    |
| CARLSBERG SPORT     |    32.9311  |          1287.02    | -1254.09        | GlobalLGB    |
| THE LONDON ESSENCE  |    47.2862  |          1034.08    |  -986.798       | GlobalLGB    |
| CHUPA CHUPS         |    94.1212  |           646.613   |  -552.491       | GlobalLGB    |
| CANDY CAN           |   114.19    |           521.734   |  -407.544       | GlobalLGB    |
| GAZOZ               |   137.28    |           530.736   |  -393.455       | GlobalLGB    |
| EASIS               |   245.012   |           622.409   |  -377.397       | GlobalLGB    |
| INDI & CO           |   346.679   |           672.408   |  -325.729       | GlobalLGB    |
| AYYO                |    51.6796  |           286.181   |  -234.502       | GlobalLGB    |
| BOYLAN              |    28.3631  |           156.166   |  -127.803       | GlobalLGB    |
| EFFERVE             |    24.007   |           135.323   |  -111.316       | GlobalLGB    |
| THOMAS HENRY        |    19.3047  |            89.1772  |   -69.8725      | GlobalLGB    |
| VIMTO               |    32.4164  |            99.9669  |   -67.5505      | GlobalLGB    |
| DOUBLE DUTCH        |    34.7097  |            99.3203  |   -64.6106      | GlobalLGB    |
| OLD JAMAICA         |    81.301   |           141.953   |   -60.6522      | GlobalLGB    |
| SIRMA               |    14.2905  |            70.1997  |   -55.9093      | GlobalLGB    |
| NATUR FRISK         |    14.4831  |            68.9029  |   -54.4198      | GlobalLGB    |
| DEPANNEUR FRIZZANTE |    90.3484  |           140.354   |   -50.0051      | GlobalLGB    |
| 7-UP                |    18.5652  |            65.5647  |   -46.9994      | GlobalLGB    |
| LE VILLAGE          |    47.7244  |            94.1658  |   -46.4413      | GlobalLGB    |
| FENTIMANS           |    26.4782  |            72.0785  |   -45.6002      | GlobalLGB    |
| PACHA               |    20.4288  |            62.9232  |   -42.4945      | GlobalLGB    |
| SFC                 |    77.3805  |           115.646   |   -38.2653      | GlobalLGB    |
| ØVRIGE BRAND        |    17.9587  |            55.8782  |   -37.9196      | GlobalLGB    |
| WARHEADS            |    34.6237  |            65.5829  |   -30.9593      | GlobalLGB    |
| RUBICON             |    13.6806  |            44.4036  |   -30.723       | GlobalLGB    |
| FINGERS CROSSED     |    31.965   |            61.8353  |   -29.8703      | GlobalLGB    |
| FRANKLIN & SONS     |    16.0638  |            44.6331  |   -28.5693      | GlobalLGB    |
| LØGISMOSE           |    27.6438  |            52.1437  |   -24.5         | GlobalLGB    |
| SAN BENEDETTO       |   118.337   |           141.339   |   -23.0017      | GlobalLGB    |
| FREM                |     7.05304 |            27.2192  |   -20.1661      | GlobalLGB    |
| D&G                 |    66.9964  |            85.1119  |   -18.1155      | GlobalLGB    |
| THOR                |    43.1053  |            59.7914  |   -16.6861      | GlobalLGB    |
| HATA RAMUNE         |    23.4286  |            39.5665  |   -16.1379      | GlobalLGB    |
| MOUNTAIN DEW.       |    17.9846  |            31.4893  |   -13.5047      | GlobalLGB    |
| JARRITOS            |    21.6752  |            31.7243  |   -10.0491      | GlobalLGB    |
| GUARANA ANARCTICA   |    35.9636  |            45.8277  |    -9.86418     | GlobalLGB    |
| MIRINDA             |    21.4004  |            30.8278  |    -9.42733     | GlobalLGB    |
| TUBORG SQUASH       |    26.7078  |            35.9897  |    -9.28197     | GlobalLGB    |
| THY                 |    21.8728  |            28.7451  |    -6.87226     | GlobalLGB    |
| EBELTOFT            |    18.1519  |            24.8807  |    -6.72883     | GlobalLGB    |
| HARBOE OTHER        |    19.3448  |            26.0458  |    -6.70095     | GlobalLGB    |
| EGO                 |     7.66379 |            14.2519  |    -6.58811     | GlobalLGB    |
| SCHWEPPES           |    12.4313  |            18.5598  |    -6.12853     | GlobalLGB    |
| SPRITE              |    14.8298  |            20.3938  |    -5.56405     | GlobalLGB    |
| ULUDAG              |    66.914   |            71.768   |    -4.85397     | GlobalLGB    |
| VOELKEL             |    27.0358  |            31.673   |    -4.63717     | GlobalLGB    |
| FRESH               |    48.9424  |            52.9809  |    -4.03851     | GlobalLGB    |
| ØRBÆK               |    15.4461  |            18.4444  |    -2.99827     | GlobalLGB    |
| DR PEPPER           |    20.4265  |            21.9833  |    -1.55685     | GlobalLGB    |
| FAXE KONDI          |    18.189   |            19.4197  |    -1.2307      | GlobalLGB    |
| BUNDABERG           |    17.8876  |            18.5977  |    -0.710033    | GlobalLGB    |
| COCA COLA           |    27.7816  |            28.162   |    -0.380397    | GlobalLGB    |
| HARBOE              |    42.2949  |            42.2949  |    -2.16189e-06 | GlobalLGB    |
| PEPSI               |    21.5826  |            21.188   |     0.394532    | XGB_PerBrand |
| NODA                |    16.6974  |            16.251   |     0.446406    | XGB_PerBrand |
| FEVER TREE          |    20.4908  |            19.1125  |     1.37833     | XGB_PerBrand |
| CARIBIA             |    36.4144  |            34.8021  |     1.61234     | XGB_PerBrand |
| KINLEY              |    15.7517  |            13.6757  |     2.07592     | XGB_PerBrand |
| JOLLY               |    45.012   |            42.5191  |     2.49292     | XGB_PerBrand |
| FANTA               |    17.8379  |            15.1758  |     2.66215     | XGB_PerBrand |
| FRESH MOJITO        |    70.2136  |            67.4892  |     2.72442     | XGB_PerBrand |
| 1724                |    54.0778  |            50.5037  |     3.57418     | XGB_PerBrand |
| NIKOLINE            |    32.3018  |            28.4753  |     3.82649     | XGB_PerBrand |
| FUGLSANG            |    49.1861  |            45.282   |     3.90407     | XGB_PerBrand |
| HANCOCK             |    10.0956  |             3.87362 |     6.22195     | XGB_PerBrand |
| LE TRIBUTE          |    33.6574  |            27.3419  |     6.31548     | XGB_PerBrand |
| ORANGINA            |    31.754   |            24.461   |     7.29301     | XGB_PerBrand |
| REINE DES LIMONADES |    25.8271  |            17.7468  |     8.08031     | XGB_PerBrand |
| SAN PELLEGRINO      |    24.4924  |            12.4973  |    11.9951      | XGB_PerBrand |
| ALBANI              |    27.9487  |            14.6238  |    13.325       | XGB_PerBrand |
| SALTUM              |    42.9262  |            28.9145  |    14.0117      | XGB_PerBrand |
| NICOLAS VAHE        |   119.002   |            82.2419  |    36.76        | XGB_PerBrand |
| HAWAI               |   139.129   |            44.9854  |    94.1441      | XGB_PerBrand |
| ØNDLINGS            |   nan       |           nan       |   nan           | XGB_PerBrand |

## Interpretation

The global model trains on 2,695 rows vs ~35 rows per brand for per-brand models.
Cross-brand learning allows the model to borrow statistical strength from major brands
(Coca-Cola, Pepsi) to improve forecasts for smaller brands -- the M5 Competition winning approach.
