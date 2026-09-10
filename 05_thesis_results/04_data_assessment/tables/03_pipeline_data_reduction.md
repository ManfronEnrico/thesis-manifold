**Panel size through the preprocessing pipeline.** Rows and brands at each stage of matrix construction, per category and horizon. The panel is aggregated at step 1; step 4 then completes each brand's month grid and applies the contract measured at step 3, producing the modelling matrix.

| Category     |   Horizon (months) |   Panel rows |   Panel brands |   After calendar fill |   Matrix rows |   Matrix brands |   Matrix columns |
|:-------------|-------------------:|-------------:|---------------:|----------------------:|--------------:|----------------:|-----------------:|
| CSD          |                  1 |        4,209 |            142 |                 6,532 |         4,876 |             106 |               52 |
| CSD          |                  3 |        4,209 |            142 |                 6,532 |         4,370 |              95 |               52 |
| Danskvand    |                  1 |        1,225 |             55 |                 2,255 |         1,230 |              30 |               34 |
| Danskvand    |                  3 |        1,225 |             55 |                 2,255 |         1,189 |              29 |               34 |
| Energidrikke |                  1 |        1,702 |             68 |                 2,924 |         2,150 |              50 |               52 |
| Energidrikke |                  3 |        1,702 |             68 |                 2,924 |         1,892 |              44 |               52 |
| RTD          |                  1 |        2,509 |            101 |                 4,141 |         2,952 |              72 |               50 |
| RTD          |                  3 |        2,509 |            101 |                 4,141 |         2,542 |              62 |               50 |

*Note.* Matrix rows EXCEED panel rows while brand counts fall. Both follow from step 4: each retained brand's month grid is completed before features are built, so that a lag refers to the previous month rather than to the previous observed row, which adds rows; and brands whose series is too short to satisfy the contract's minimum-periods requirement are excluded, which removes them. Exclusion is by the measured contract, not by manual selection.
