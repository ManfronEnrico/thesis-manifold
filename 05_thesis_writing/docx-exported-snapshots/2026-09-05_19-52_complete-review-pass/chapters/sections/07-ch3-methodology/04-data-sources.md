# Data Sources

> Section of **Methodology > Data Sources**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**4 comment(s) on this section** -- APPENDIX, OUTDATED, CONTEXT. Detail: `comments/sections/07-ch3-methodology/04-data-sources.md`

---

This thesis uses one data source: the Nielsen/Prometheus beverage scanner panel, the core forecasting input across all five categories.
The Nielsen/Prometheus dataset provides longitudinal retail transaction data for five Danish beverage categories: carbonated soft drinks (CSD), still and sparkling water (danskvand), energy drinks (energidrikke), ready-to-drink beverages (RTD), and beer (totalbeer). Its structure follows a star schema, with a facts table recording sales value, sales in litres, sales units, and weighted distribution at the brand-times-retailer-times-period level, linked to dimension tables for market, period, and product. The panel provides between 37 and 42 monthly periods per category (CSD being the longest, October 2022 to March 2026), giving a transaction history of roughly three to three-and-a-half years. The sales metrics include both base and promotional variants, enabling the identification of promotional uplifts as a feature engineering input. The weighted distribution metric provides a proxy for product availability, which is a meaningful predictor of sales volume for categories with intermittent distribution. The Nielsen dataset is used under a confidentiality agreement with Manifold AI.
