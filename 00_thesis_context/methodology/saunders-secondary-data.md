---
name: Saunders Ch8 — Secondary Data Framework (scaffold for Ch4 Data Assessment)
description: Schema of Saunders, Lewis & Thornhill (2023) Ch8 mapped to our Nielsen + Indeks data. Framework to apply when writing Ch4. Not yet applied.
status: PENDING — reference scaffold; apply when writing/aligning Ch4 (data assessment)
source: Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). Research Methods for Business Students (9th ed.). Pearson. Chapter 8 "Obtaining and evaluating secondary data".
updated: 2026-06-19
---

# Saunders Ch8 — Secondary Data (framework for Ch4)

> ⚠️ **UPDATE 2026-06-19: Indeks Danmark DROPPED from the thesis.** Ignore every Indeks / consumer-survey /
> enrichment mention below — the thesis now uses **one** secondary data source (the Nielsen scanner panel).
> The Saunders Ch8 evaluation framework still applies, but to Nielsen only.

> **STATUS: parked.** Schematises Saunders et al. (2023) Ch8 and maps it to our data. Our Nielsen scanner
> panel and Indeks Danmark survey are textbook **secondary data** (collected by others for another purpose,
> reanalysed here). Use this to structure Ch4 in Saunders' language. Not yet applied to prose.

## 1. The framework (what Ch8 gives us)

**Definition.** Secondary data = data originally collected for another purpose, reanalysed to answer a new
research question. Includes raw data and compiled summaries; structured (relational/tabular) vs unstructured.

**Three types** (Saunders' taxonomy):
| Type | Subtypes | 
|---|---|
| Survey | census · continuous/regular survey · ad-hoc survey |
| Document | text · audio · visual/audio-visual |
| Multiple-source | snapshot · longitudinal · continually updated (big data) |

**Philosophy link.** Positivist treats secondary data as objective external reality; critical realist (and our
**pragmatist/moderate-realist** stance) treats it as *partial but meaningful representations* shaped by the
collecting instrument. (This already matches Ch3 §3.1: the Nielsen panel "reflects retailer reporting
conventions and panel design choices".)

**Evaluation = 3-stage process (Figure 8.2)** — the backbone Ch4 should follow:
1. **Overall suitability**: (a) *measurement validity / appropriateness* (do the data measure what we need?),
   (b) *coverage* (right population, period, and enough data after exclusions). If not suitable → stop.
2. **Precise suitability**: *reliability/dependability* (source authority + collection method), *validity/
   credibility* (how data were collected; errors/biases), *measurement bias / trustworthiness* (deliberate
   distortion, changes in collection, construct mismatch).
3. **Costs vs benefits** (+ ethics/access).
Box 8.13 gives a full evaluation checklist.

## 2. Our data, mapped

**Nielsen / Prometheus scanner panel** → **Survey secondary data, continuous/regular survey subtype**;
quantitative, **structured** (star schema). Commercial market-research data → access restricted/costly
(matches our **confidentiality agreement** with Manifold). Multiple-source/longitudinal in use (37–42
monthly periods per category → enables a longitudinal element, a key Saunders advantage).

**Indeks Danmark consumer survey** → **Survey secondary data, regular/ad-hoc survey subtype**;
quantitative + structured, with **survey weights**. The optional enrichment source (future work).

## 3. How Ch4 should be structured (Saunders-grounded scaffold)

1. **Data sources & type** — classify Nielsen + Indeks in Saunders' taxonomy (survey, structured),
   secondary, commercial.
2. **Why secondary data (advantages, §8.3)** — fewer resources / no primary collection; high quality
   (Nielsen's reputation depends on it); enables longitudinal depth; unobtrusive; comparative/contextual.
3. **Overall suitability (§8.6)**:
   - *Measurement validity*: do the recorded metrics (sales value, litres, units, weighted distribution)
     measure our forecasting target? Note the proxy nature of weighted distribution for availability.
   - *Coverage*: 5 categories; 37–42 periods; retailer chains; brand counts (42 RTD → 455 beer);
     market definition (DVH EXCL. HD); exclusions and what remains.
4. **Precise suitability (§8.6)**:
   - *Reliability/dependability*: Nielsen as an authoritative panel provider.
   - *Validity/credibility*: how scanner data are collected/compiled; documented limitations.
   - *Measurement bias / trustworthiness*: definitions fixed by Nielsen (not by us); **promo-zero coverage
     for danskvand and RTD** = an *unmeasured-variable / coverage* limitation in Saunders' terms (the
     promotional variable is absent for some categories) → flag explicitly.
5. **Disadvantages / limitations (§8.4)**: original purpose (market measurement, not forecasting) ≠ our
   need; commercial access constraints; aggregations/definitions set by the provider; no control over data
   quality; data cannot be redistributed (ties to the confidentiality limitation already in Ch3 §3.7).
6. **Costs / benefits + ethics**: confidentiality agreement; data not to leave local environment; Indeks
   survey weights not to be exported (per project-state constraints).

## 4. Flags to carry into Ch4
- Frame the data as *partial representations through a measurement instrument* (pragmatist/realist),
  consistent with Ch3 §3.1 — do **not** present scanner data as theory-free objective truth.
- **promo-zero (danskvand, RTD)** = a coverage/measurement limitation; state it honestly.
- Indeks Danmark = available secondary data for an **optional future enrichment** (not a core evaluated
  input), consistent with v4 framing.
- Big-data "three/five Vs" framing is **not** a good fit (our data is modest, structured, not big data) —
  do not overreach.
- New citation when applied: Saunders, Lewis & Thornhill (2023) — already to be added for Ch3 (Saunders
  onion); single shared reference.

## 5. Open
- Confirm exact retailer-chain counts and the current period spans per category at writing time (numbers
  may shift with the from-scratch data rebuild — do not hard-code stale figures).
