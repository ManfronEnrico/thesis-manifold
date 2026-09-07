# 4.1 Overview and Data Strategy

> Section of **Chapter 4 | Data Assessment > 4.1 Overview and Data Strategy**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**4 comment(s) on this section** -- ACADEMIC, PROSE, VERIFY, OUTDATED. Detail: `comments/sections/08-ch4-data-assessment/01-4-1-overview-and-data-strategy/00-intro.md`

---

This thesis draws on one secondary data source in the sense of Saunders et al. (2023): data originally collected by others for another purpose and reanalysed here. The **Nielsen/Prometheus beverage scanner panel** is the forecasting input, covering four Danish beverage categories: carbonated soft drinks (`CSD`), still and sparkling water (`danskvand`), energy drinks (`energidrikke`), and ready-to-drink beverages (`RTD`).  A fifth category, beer (totalbeer), was available at source but excluded from this study. Its fact table is an order of magnitude larger than the others, and retrieving it exceeded the bandwidth and local compute available for this project. The exclusion is therefore a deliberate scoping decision taken under resource constraints, not an absence in the data, and it is recorded as such among the delimitations of Introduction  Chapter 1.4.
CSD is the worked category, assessed in full in Section 4.2  and used to derive the pipeline parameters. The remaining three categories are processed through the identical pipeline, and they are not merely replications: because they differ systematically in scale, promotional structure and series length, they are what allows Chapter 6 to test whether one pooled model generalises across categories or whether category-specific models are required.
It is survey-type, structured, commercial secondary data. Consistent with the pragmatist stance of Chapter 3, it is treated as a partial but workable representation of demand realities, shaped by the collecting instrument, rather than as a theory-free objective record.
This chapter assesses the data following the three-stage secondary-data evaluation of Saunders et al. (2023): (i) **overall suitability** (measurement validity and coverage), (ii) **precise suitability** (reliability/dependability, validity/credibility, and measurement bias/trustworthiness), and (iii) **costs, benefits, and ethics**. The assessment is conducted per category, since the four categories differ systematically in scale and promotional structure. The train, validation, and test split is then specified as a locked, pre-registered design decision applied identically across the forecasting models (Chapter 6), and the key data risks are documented to bound the empirical claims of the later chapters.
