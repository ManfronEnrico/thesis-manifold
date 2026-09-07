# Schema and Structure

> Section of **Data Assessment > Overview and Data Strategy > Schema and Structure**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**4 comment(s) on this section** -- APPENDIX, OUTDATED, VERIFY. Detail: `comments/sections/08-ch4-data-assessment/01-overview-and-data-strategy/02-schema-and-structure.md`

---

Each category follows a star schema: dimension tables for market, period, and product, linked to a facts table at the grain of market × product × period. The facts table records the core sales metrics (sales value, sales in litres, sales units), their promotional variants (the same metrics under promotion), and a weighted-distribution metric that proxies product availability. The product dimension captures brand, manufacturer, packaging format, flavour or type, price tier, and corporate attribution.
A technical note carried over from the prior pipeline and to be re-verified in reproduction attempts: period identifiers are not necessarily monotonic with calendar time, so all time-series operations sort by the composite key (“period_year”, “period_month”). The facts table may also contain more distinct products than the active product dimension (discontinued or out-of-scope SKUs), so the join to the product dimension is the correct scoping mechanism.
Per-category structural counts (periods, brands, products/SKUs, brand-month rows, in-scope fact rows) are reported in Table 4.1, all computed locally under the DVH EXCL. HD scope.
| Category | Periods (max) | Brands (in scope) | retained ≥40 | retained ≥30 | Catalog SKUs | In-scope SKUs | Brand-month rows | In-scope fact rows |
|---|---|---|---|---|---|---|---|---|
| CSD | 42 | 136 | 57 | 77 | 8,608 | 7,668 | 3,789 | 187,907 |
| danskvand | 37 | 49 | 0 ⚠️ | 24 | 565 | 453 | 1,090 | 24,796 |
| energidrikke | 39 | 64 | 0 ⚠️ | 27 | 747 | 577 | 1,520 | 49,345 |
| RTD | 37 | 93 | 0 ⚠️ | 42 | 589 | 511 | 2,193 | 44,449 |
**Table** **1** - Per-category training structure, filtered to DVH EXCL. HD scope (2026-06-27)
*CSD figures supersede Brian’s all-markets values, inflated 6.16× by summing hierarchical markets; the CSD catalog-SKU count (8,608 distinct* *product_id* *in the product dimension) likewise supersedes the earlier 2,080.*  **Column definitions**: *Catalog SKUs* = distinct product_id in dim_product; *In-scope SKUs* = distinct product_id with positive sales at the DVH EXCL. HD scope; *Brand-month rows* = positive-sales brand × month observations across all in-scope brands (the retained ≥30 subset yields 3,077 / 885 / 1,007 / 1,543 observed rows respectively, per regeneration_report.md).  **MIN_PERIODS feasibility**: danskvand, energidrikke, and RTD have only 37–39 monthly periods, so a ≥40-observation filter retains **zero** brands for them; a single global threshold of **≥30** is therefore adopted across all categories (CSD 77, danskvand 24, energidrikke 27, RTD 42 brands), which is both feasible and consistent - preferable to the inherited mixed rule (40 for CSD, 30 for the rest). The bold column (≥30) is the retained set used downstream.
