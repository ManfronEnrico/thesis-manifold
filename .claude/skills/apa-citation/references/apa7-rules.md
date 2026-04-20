# APA 7 Edge Case Rules

Reference: American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). https://doi.org/10.1037/0000165-000

---

## Author Formatting

| Situation | Rule | Example |
|---|---|---|
| Single author | Last, F. I. | Makridakis, S. |
| Two authors | Last, F. I., & Last, F. I. | Hevner, A. R., & March, S. T. |
| Three authors | Last, F. I., Last, F. I., & Last, F. I. | Peffers, K., Tuunanen, T., & Rothenberger, M. A. |
| 4–20 authors | List all, last preceded by & | See APA 7 §9.8 |
| 21+ authors | List first 19, then `...`, then last author | — |
| No author | Move title to author position | *Title of Work*. (Year). |
| Organisation as author | Spell out full name | World Health Organization. (2020). |
| Same author, same year | Add letter suffix to year | (Makridakis et al., 2020a) / (Makridakis et al., 2020b) |
| Initials needed to distinguish | Include initials in in-text | (A. R. Hevner, 2004) |

---

## Source Type Formatting

### Journal Article
```
Last, F. I., & Last, F. I. (Year). Title of article in sentence case with only 
proper nouns capitalised. Journal Name in Title Case, Volume(Issue), first–last. 
https://doi.org/xxxxx
```

### Journal Article — Advance Online Publication (no volume/issue/pages yet)
```
Last, F. I. (Year). Title of article. Journal Name. Advance online publication. 
https://doi.org/xxxxx
```

### Book (whole)
```
Last, F. I. (Year). Title of book in sentence case. Publisher. https://doi.org/xxxxx
```

### Book Chapter (edited volume)
```
Last, F. I. (Year). Title of chapter in sentence case. In E. E. Editor & E. E. Editor (Eds.), 
Title of book (pp. NNN–NNN). Publisher. https://doi.org/xxxxx
```

### Conference Paper (proceedings)
```
Last, F. I., & Last, F. I. (Year). Title of paper. In E. E. Editor (Ed.), 
Proceedings of the Conference Name (pp. NNN–NNN). Publisher. https://doi.org/xxxxx
```

### Conference Paper (no editors listed)
```
Last, F. I. (Year, Month Day–Day). Title of paper [Conference session]. Conference Name, 
City, Country. https://doi.org/xxxxx
```

### arXiv Preprint
```
Last, F. I., & Last, F. I. (Year). Title of paper. arXiv. https://arxiv.org/abs/XXXX.XXXXX
```
> Note: Flag arXiv preprints — CBS may require peer-reviewed sources. Add "(preprint)" note in refs.md if not peer-reviewed.

### Working Paper / NBER
```
Last, F. I. (Year). Title of paper (Working Paper No. NNNNN). National Bureau of Economic Research. 
https://doi.org/xxxxx
```

### Technical Report
```
Last, F. I. (Year). Title of report (Report No. XXX). Organisation Name. URL
```

### Software / GitHub Repository
```
Last, F. I. (Year). Software name (Version X.X) [Software]. Publisher or GitHub. URL
```
> Example: Chase, H., et al. (2024). *LangGraph* (Version 0.2) [Software]. LangChain AI. https://github.com/langchain-ai/langgraph

### Dissertation / Thesis
```
Last, F. I. (Year). Title of dissertation [Doctoral dissertation, University Name]. Repository Name. URL
```

### Website / Online Document
```
Last, F. I. (Year, Month Day). Title of page. Site Name. URL
```

### Dataset
```
Last, F. I. (Year). Title of dataset (Version N) [Dataset]. Repository Name. https://doi.org/xxxxx
```

---

## Title Formatting Rules

| Rule | Correct | Wrong |
|---|---|---|
| Article titles: sentence case | The M4 competition: 100,000 time series | The M4 Competition: 100,000 Time Series |
| Proper nouns capitalised | LightGBM, LangGraph, FMCG, Danish | Lightgbm, Langgraph |
| Journal names: title case | International Journal of Forecasting | International journal of forecasting |
| Colons: capitalise word after | Competition: Results, findings | Competition: results, findings |
| Subtitles: capitalise first word after colon | Design science: A new paradigm | Design science: a new paradigm |

---

## DOI Formatting

- Always use full URL format: `https://doi.org/10.xxxx/xxxxx`
- Never use `doi:` prefix or shortened forms
- If no DOI: include full stable URL
- If no URL and no DOI: include database name (e.g., "Retrieved from PsycINFO")
- Do not add a period after a DOI or URL at the end of a reference

---

## In-Text Citation Edge Cases

| Situation | Format |
|---|---|
| Citing a secondary source | (Original Author, Year, as cited in Secondary Author, Year) — use sparingly |
| Multiple citations in one parenthesis | Alphabetical order, semicolon-separated: (Hevner et al., 2004; Peffers et al., 2007) |
| Citing a specific page | (Last et al., Year, p. N) |
| Citing a range of pages | (Last et al., Year, pp. N–N) |
| Narrative citation | Makridakis et al. (2020) found that... |
| Work with no date | (Last, n.d.) |
| Personal communication | (F. I. Last, personal communication, Month Day, Year) — not in reference list |
| Reprinted/translated work | (Original Year/Current Year) |

---

## Specific Cases for This Thesis

### LangGraph (software, no academic paper)
```
In-text: (LangChain AI, 2024)

References:
LangChain AI. (2024). *LangGraph* (Version 0.2) [Software]. GitHub. 
https://github.com/langchain-ai/langgraph
```

### M4 Competition (Makridakis et al., 2020)
```
In-text: (Makridakis et al., 2020)

References:
Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 
100,000 time series and 61 forecasting methods. International Journal of Forecasting, 
36(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014
```

### M5 Competition (Makridakis et al., 2022)
```
In-text: (Makridakis et al., 2022)

References:
Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: 
Results, findings, and conclusions. International Journal of Forecasting, 38(4), 1346–1364. 
https://doi.org/10.1016/j.ijforecast.2021.11.013
```

### Hevner et al. (2004)
```
In-text: (Hevner et al., 2004)

References:
Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information 
systems research. MIS Quarterly, 28(1), 75–105. https://doi.org/10.2307/25148625
```

### Peffers et al. (2007)
```
In-text: (Peffers et al., 2007)

References:
Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science 
research methodology for information systems research. Journal of Management Information 
Systems, 24(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302
```

### arXiv preprints (flag all)
Any arXiv source must be flagged with `[PREPRINT — not peer-reviewed]` in `thesis/writing/references.md`.
Confirm with supervisor before citing in final submission.

---

## References List Rules

1. **Alphabetical order**: by first author surname, then chronological for same author
2. **Hanging indent**: first line flush left, subsequent lines indented (5–7 spaces in Markdown: use `   `)
3. **No numbering**: APA uses alphabetical list, not numbered
4. **Double-spaced** in the final Word document (python-docx handles this via paragraph spacing)
5. **"References"** as heading — not "Bibliography", not "Works Cited"
6. All entries in `thesis/writing/references.md` are the single source of truth — cross-referenced by `/verify-citations`
