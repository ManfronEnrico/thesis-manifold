### 1. Main Dataset: indeksdanmark_data.csv (Complete Indeks Danmark Survey)

- **Format**: CSV
- **Rows**: 20,134 (respondents)
- **Columns**: 6,364 variables (all float64, all variable labels available from codebook/SPSS metadata)
- **Content**: Contains demographic, behavioral, attitudinal, and preference variables for all survey sections

### 2. Codebook: official_codebook.csv (Codebook with Survey Weights)

- **Format**: CSV
- **Rows**: 6,364 (one row per variable in the main dataset)
- **Columns**: 11 (includes weight column for survey weighting)
- **Content**: Variable documentation with survey weight information in the "weight" column
- **Use Case**: Use when performing weighted analysis to account for survey design and population representation

### 3. Value Labels: indeksdanmark.metadata.csv (SPSS Value Label Mappings)

- **Format**: CSV
- **Rows**: 29,185 (value label mappings for categorical variables)
- **Columns**: 3 (Variable, Value, Label)
- **Content**: Maps numeric codes to human-readable labels for categorical variables (e.g., 1.0 → "A: the Danish Social Democrats" for STEMT_HH23)
- **Use Case**: Essential for interpreting categorical variables and creating meaningful visualizations with proper labels
