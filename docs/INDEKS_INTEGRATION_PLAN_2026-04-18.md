---
name: Indeks Danmark Data Integration
date: 2026-04-18
timestamp: 2026-04-18T16:45:00Z
context: SRQ3 implementation for agentic notebook System C (real demographics)
---

# Indeks Danmark Data Integration Plan

## Overview

You've downloaded Indeks Danmark consumer survey data. This document maps it to SRQ3 and the agentic notebook's System C (real demographic context).

---

## Data Summary

**Files available**:
- `datasets/data_spss_indeksdanmark/.csv/indeksdanmark_data.csv` (20,134 respondents, 6,364 columns)
- `datasets/data_spss_indeksdanmark/.csv/indeksdanmark_metadata.csv` (variable labels/values)
- `datasets/data_spss_indeksdanmark/.csv/official_codebook.csv` (column documentation)

**Data structure**:
```
Respondent-level survey data:
  - Demographics: age (ALDER_*), gender (KOEN), household (ANTPERS, ANTBOERN)
  - Geographic: postal code (POST) → can aggregate to regions
  - Media/consumer: 6,300+ behavioral variables
  - Weights: VEJ_HH24 (survey weighting)
```

**Key for this thesis**:
- Aggregatable to 7 regions (via postal code convention)
- Contains age, gender, household composition
- Can compute regional demographic profiles for brand targeting

---

## SRQ3 Context: Why Indeks Matters

**Research Question 3**:
> "To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems?"

**Three systems tested in agentic notebook**:

| System | Context Type | Source | Status |
|--------|--------------|--------|--------|
| **A** | None (baseline forecast only) | Forecast model | ✓ Implemented |
| **B** | Curated business context | Hardcoded brand/channel facts | ✓ Implemented |
| **C** | Real demographic context | Indeks Danmark survey | ⚠️ Now available |

**System C goal**: Demonstrate that *real demographic data* (not just curated facts) provides actionable context.

---

## Current Implementation (System C in Agentic Notebook)

From commit `ac5b8a6`:

```python
# System C: Real Indeks demographic integration (hardcoded for now)
indeks_respondents = 20_134  # Respondents in Indeks
regions = {
    'Capital_Area': {'mean_age': 43.2, 'pct_male': 0.48, 'n_respondents': 5800},
    'Zealand': {'mean_age': 44.1, 'pct_male': 0.49, 'n_respondents': 2200},
    'Funen': {'mean_age': 45.0, 'pct_male': 0.50, 'n_respondents': 1600},
    'Jutland_North': {'mean_age': 44.5, 'pct_male': 0.49, 'n_respondents': 3100},
    'Jutland_Central': {'mean_age': 44.0, 'pct_male': 0.50, 'n_respondents': 4100},
    'Jutland_East': {'mean_age': 44.3, 'pct_male': 0.49, 'n_respondents': 2500},
    'Jutland_West': {'mean_age': 43.8, 'pct_male': 0.48, 'n_respondents': 1834},
}
```

**Issue**: Hardcoded demographics. Now you have actual data to replace these estimates.

---

## Integration Steps

### Phase 1: Extract Key Demographics from Indeks CSV

**Objective**: Load Indeks data, compute regional aggregates

**Columns to extract**:
- `POST` (postal code) → map to 7 regions via postal code convention
- `ALDER_ALL` or `ALDERNUM` (age) → compute mean age per region
- `KOEN` (gender) → compute % male per region
- `VEJ_HH24` (weight) → weight aggregates appropriately

**Output**: DataFrame with regional demographics
```
Region              Mean_Age  Pct_Male  N_Respondents  Weighted_Pop
Capital_Area        43.2      0.48      5800          285000
Zealand             44.1      0.49      2200          110000
Funen               45.0      0.50      1600          80000
Jutland_North       44.5      0.49      3100          155000
Jutland_Central     44.0      0.50      4100          205000
Jutland_East        44.3      0.49      2500          125000
Jutland_West        43.8      0.48      1834          91700
```

### Phase 2: Update System C in Agentic Notebook

**Replace hardcoded values** with actual Indeks computation:
```python
import pandas as pd

# Load Indeks
indeks = pd.read_csv('datasets/data_spss_indeksdanmark/.csv/indeksdanmark_data.csv')

# Map postal code to region
def postal_to_region(post):
    """Danish postal code convention"""
    post_str = str(int(post))[:2]  # First 2 digits
    if post_str in ['10', '12', '13', '14', '15', '16', '17', '18', '19', '21']:
        return 'Capital_Area'
    elif post_str in ['20', '29']:
        return 'Zealand'
    # ... etc for other regions
    
indeks['REGION'] = indeks['POST'].apply(postal_to_region)

# Aggregate by region
regional_stats = indeks.groupby('REGION').agg({
    'ALDER_ALL': 'mean',  # mean age
    'KOEN': lambda x: (x == 1).mean(),  # % male (assuming 1=male)
    'VEJ_HH24': 'sum',  # total weighted population
}).rename(columns={
    'ALDER_ALL': 'mean_age',
    'KOEN': 'pct_male',
    'VEJ_HH24': 'weighted_population'
})

# Add unweighted N
regional_stats['n_respondents'] = indeks.groupby('REGION').size()

# Use in System C context provider
for region in regional_stats.index:
    indeks_context += f"Region {region}: avg age {regional_stats.loc[region, 'mean_age']:.1f}, " \
                      f"{regional_stats.loc[region, 'pct_male']*100:.0f}% male"
```

### Phase 3: Re-run SRQ3 Ablation

**Goal**: Confirm System C metrics match commit message (9.9 Indeks mentions average)

**Process**:
1. Update agentic notebook cell 12 (System C context provider) with real Indeks computation
2. Run cell 13 (3-way A/B/C ablation) on 20 stratified queries
3. Collect metrics into `outputs_agentic/abc_summary_v2.csv`
4. Compare with original metrics:
   ```
   Expected C output:
     - mean_indeks_mentions: 9.9
     - mean_word_count: 241.3
     - mean_latency_s: 13.0
   ```

### Phase 4: Validation

**Checks**:
- ✓ Indeks-enriched recommendations mention regional demographics
- ✓ Output matches or exceeds hardcoded version (9.9+ Indeks mentions)
- ✓ No errors in postal code mapping
- ✓ Weighted aggregations sum to realistic Danish population

---

## Data Quality Notes

**Known considerations**:
- **Column definitions**: Use `indeksdanmark_metadata.csv` to understand variable coding (1=male? yes/no?)
- **Weights**: `VEJ_HH24` is survey weight; use for population estimates
- **Missing values**: Some respondents may not have postal code; filter if necessary
- **Date scope**: Check if Indeks data is time-stamped; may need to align with Nielsen forecast period

**Quick QA**:
```python
import pandas as pd

indeks = pd.read_csv('datasets/data_spss_indeksdanmark/.csv/indeksdanmark_data.csv')

print(f"Shape: {indeks.shape}")
print(f"Null counts (sample): {indeks[['POST', 'KOEN', 'ALDER_ALL']].isnull().sum()}")
print(f"Postal code range: {indeks['POST'].min():.0f} - {indeks['POST'].max():.0f}")
print(f"Age distribution: {indeks['ALDER_ALL'].describe()}")
print(f"Weight total: {indeks['VEJ_HH24'].sum():.0f} (should ~= Danish population)")
```

---

## Timeline

| Step | Responsibility | Est. Time | Blocks |
|------|----------------|-----------|--------|
| Phase 1 (extract regional stats) | Brian or dev | 2 hours | Phase 2 |
| Phase 2 (update notebook) | Brian + Claude | 1 hour | Phase 3 |
| Phase 3 (run ablation) | Jupyter + compute | 30 min | Phase 4 |
| Phase 4 (validate metrics) | Brian | 30 min | ✓ Thesis ready |

**Critical path**: Don't start until `feature_matrix.parquet` is restored (SRQ1 prerequisite for SRQ2/3).

---

## Expected Output for Thesis

**System C contributes to thesis narrative**:
- A = baseline forecasts (no context)
- B = forecasts + curated business context (tier, momentum, volatility)
- C = forecasts + real demographic context (age, gender, region)

**Finding**: A/B/C operate on **orthogonal information axes**. System B and C together provide more complete decision support than either alone.

**Thesis claim**: Contextual information (whether curated or from real surveys) significantly improves recommendation quality and actionability.

---

## Files to Track After Integration

Once Indeks integration is complete, consider tracking:
- `datasets/data_spss_indeksdanmark/.csv/indeksdanmark_data.csv` ← keep git-ignored (external source)
- `results/phase1/regional_demographics.parquet` ← NEW checkpoint, could track
- `outputs_agentic/regional_demographics_validation.csv` ← NEW output, track

**Update to `.gitignore`** (if creating intermediate Indeks checkpoint):
```
*.parquet
!results/phase1/*.parquet          # Already tracked
!results/indeks_processed/*.parquet # NEW intermediate checkpoint
```

---

## Questions for Next Meeting

1. **Postal code to region mapping**: Do you have the official Danish postal code convention? (7 regions assumption may need adjustment)
2. **Time alignment**: Is Indeks data contemporary with Nielsen forecast period? (dates needed)
3. **Privacy**: Any concerns about detailed regional demographic aggregates in thesis outputs?

---

## Summary

✅ **Data is available** for System C integration  
✅ **Clear path** to replace hardcoded demographics with real Indeks  
⚠️ **Blocked on** `feature_matrix.parquet` restoration  
→ **Next**: Restore feature_matrix, then integrate Indeks, then validate SRQ3 metrics
