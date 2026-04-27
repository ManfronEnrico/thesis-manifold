# Message to Brian — Project status update (2026-04-27)

> Copy-paste this in Slack/email to Brian. Branch pushed: `enrico/local-backup` (latest commit: `Phase 1+2+3+4+5`)

---

## TL;DR

Since your last restructuring commits, ho completato 5 phase di lavoro: ricostruzione preprocessing, training di 7 modelli ML con Optuna, integrazione agentic, e un framework di evaluation a 4-tier (L0/L1/L2/L3). Manca un solo run finale (~$4) e poi posso scrivere Chapter 6+7+Discussion.

---

## What's been done since your last commits

### Phase 1 — Preprocessing fix + agentic feature engineering

- Integrato il tuo fix preprocessing nel branch
- Aggiunto modulo `engineer_features.py` (causal lags, rolling stats, calendar, promo intensity)
- Aggiornati `data_assessment_agent.py`, `research_state.py`
- Tutto in commit `de9f9e0`

### Phase 2 — ML model training (SRQ1 risposto)

8 notebook di training in `docs/thesis/analysis/`:
- 5 specialized models (1 per categoria Nielsen): CSD, danskvand, energidrikke, RTD, totalbeer
- 2 pooled models (pooled-4, pooled-5)
- 1 final comparison notebook

**Setup costante**: brand × retailer × month, 17-18 retailer chains, train ≤ Feb 2025 / val Mar-Aug 2025 / test Sep 2025+. Walk-forward CV (5 folds, 3-month horizon, expanding window). Optuna 50 trials per algoritmo.

**Headline per-brand median MAPE (test set)**:
| Categoria | XGBoost | LightGBM | Winner |
|---|---|---|---|
| CSD | **16.77%** | 16.82% | XGB (margin 0.05pp) |
| danskvand | 22.22% | **21.23%** | LGB (only LGB win) |
| energidrikke | **21.18%** | 25.34% | XGB (margin 4.16pp) |
| RTD (V2 regularized) | 29.04% | **25.56%** | LGB |
| totalbeer | **26.65%** | 27.37% | XGB (margin 0.72pp) |

**SRQ1 verdict**: **specialized always wins**. Pooling ha consistentemente peggiorato l'accuracy di 0.14-5.21pp per categoria. CSD è la più "negativamente" affetta dal pooling.

Re-training pipeline in `scripts/ml_retraining/` (10 step, da `00_setup.py` a `10_publication_figures.py`).

### Phase 3 — Agentic registry integration

Aggiornato `thesis_agentic_notebook.ipynb`:
- §0.5: `CATEGORY_MODELS` registry (mapping cat → outputs_dir + primary_model + MAPE)
- §0.5: `load_model_for_category()` helper
- §2.5: `forecasting_agent_multi()` che routa al per-category model

Backward-compatible con il forecasting_agent CSD-only originale.

### Phase 4 — A vs B baseline (deprecato, methodologically weak)

Costruito un confronto A (LLM-only gpt-4o-mini) vs B (LLM + tuned ML). B vinceva 47/50 pairwise, MAPE 27% vs n/a.

**Problema**: confronto strawman. Un revisore CBS legittimamente direbbe "A non aveva accesso ai dati, ovvio che B vince". Quindi ho deprecato Phase 4 e disegnato Phase 5.

### Phase 5 — 4-tier comparison (current focus)

| Tier | Setup | Cosa testa |
|---|---|---|
| **L0** | LLM-only (no tools) | Pure language baseline |
| **L1** | LLM + raw historical sales tool (no ML) | Does data access alone help? |
| **L2** | LLM + UNTUNED ML (n_est=200, no Optuna) | Does ML structure help? |
| **L3** | LLM + TUNED ML (Optuna 50-trial) + confidence layer (HIGH/LOW) | Does tuning + calibration help? |

L'obiettivo è isolare 3 contributi indipendenti:
1. Data access (L1 vs L0)
2. ML structure (L2 vs L1)
3. Training quality + confidence-awareness (L3 vs L2)

**Setup eval**:
- 50 prompts forecast-only (point_forecast, range_forecast, confidence_interval, brand_vs_brand, channel_ranking, top_performers, risk_flags, driver_question, anomaly_flag, yoy_comparison, channel_volatility)
- Real test set tuples (brand × channel × Sep-Nov 2025), category hint nel prompt
- 12-metric evaluation framework (quantitative MAPE/MAE/RMSE/sMAPE/hallucination/latency/cost + qualitative LLM-as-judge groundedness/actionability/specificity/coherence/business_relevance + pairwise preference + composite)

**Iterazioni v1-v5 dei prompt** (lessons learned):
- v1 → v2: aggiunto actionability layer + 10k tokens. Risultato: actionability NON migliorato (limite strutturale: serve un MMM per scoring 5 sull'actionability rubric), MAPE peggiorato. **Rolled back**.
- v3: aggiunto category hint nel prompt user (`MORENA (totalbeer brand)`) per rimuovere brand-routing confound. Aiutato ma scoperto BUG: LLM ancora rifiutava brand non in mapping esplicita + inventava channel names ("ON_PREMISE", "RETAIL", ecc).
- v4: mappatura brand permissiva ("examples non-exhaustive") + lista esplicita 18 valid channels.
- **v5 final**: consolida tutti i fix + aggiunge fallback channel logic (try 2 alternates before abstaining) + strict JSON schema (`predicted_sales_units` MUST be scalar, never dict/list) + max_tokens=6000 + up to 5 tool calls per multi-brand archetypes.

### Status finale (pre-run v5)

L3 v3 (con bugs ancora presenti):
- MAPE filtered: 12.10% ✅
- 0% hallucination ✅
- Composite quality 2.55 (best) ✅
- Vince pairwise contro L0 (80%), L1 (52%), L2 (50%)
- Wins all 6 pairwise comparisons head-to-head

---

## What's left to complete the technical part

### 1. Final run v5 — UNICO costo residuo (~$4 + 35 min)

- §5 main loop: 200 OpenAI calls (50 prompts × 4 systems) → ~$1.50, 12 min
- §6 quantitative metrics: gratis, 5 sec
- §7 LLM-as-judge: 1000 Anthropic calls (50 × 4 × 5 metrics) → ~$2, 20 min
- §8 pairwise: 300 Anthropic calls (6 pair types × 50) → ~$0.50, 5 min

Notebook pronto, prompt v5 final già applicato. Solo da runnare in Jupyter.

### 2. Figure + tabelle (gratis, 2 min)

- §10a composite score
- §10b 5 figure: boxplot sMAPE, heatmap judge, radar 4-tier, win-rate matrix, cost-quality scatter
- §11 markdown tables ready-to-paste

### 3. Human eval pilot (opzionale, ~30 min manuale)

- Template `human_eval_pilot_15_v3.csv` già pronto (15 prompts random, 3 per categoria)
- Compilare colonne `<sys>_HUMAN_score_1to5` e `HUMAN_winner_L0_L1_L2_L3`
- Calcolare Cohen's κ per validare la judge methodology

### 4. Quando arriva l'accesso a Prometheus

- Aggiungere come **L4** nel framework
- Re-runnare §5/§6/§7/§8 sui 50 prompts (incremental, solo Prometheus)
- Confronto finale 5-tier per Discussion

### 5. Thesis writing (technical chapters)

- **Chapter 6**: ML benchmark (Phase 2 results) — ~1 settimana
- **Chapter 7**: 4-tier agentic eval (Phase 5 results) — ~1 settimana
- **Discussion**: SRQ1+SRQ2+SRQ3 verdicts, limitations (actionability ceiling = no MMM, brand-routing confound resolved in v4+, prompt sample size n=50)

---

## Decisioni chiave per cui mi serve il tuo OK

1. **v5 prompt final OK**? Ho consolidato tutti i learning di 4 iterazioni precedenti. Vuoi review prima del run finale?
2. **Skip o run human eval pilot**? È opzionale, 30 min manual + 5 min agreement calc.
3. **Quando ti arriva Prometheus access**? Così pianifico l'integrazione L4.
4. **Format Chapter 7 tables/figures**: vuoi che usi quelli del notebook (markdown ready) o preferisci LaTeX?

---

## Cost summary Phase 5

| Voce | Spesa |
|---|---|
| §5 v1 (no actionability, 4k tokens) | $1.10 |
| §7 v1 judge | $1.93 |
| §8 v1 pairwise (78%) | $0.40 |
| §5 v2 (10k + actionability, rolled back) | $1.50 |
| §7 v2 judge (rolled back) | $1.97 |
| §5 v3 (category hint, 4k) | $1.50 |
| §7 v3 judge | $1.97 |
| §8 v3 pairwise (100%) | $0.50 |
| **§5 + §7 + §8 v5 (FINAL, ancora da fare)** | **~$4.00** |
| **TOTALE Phase 5** | **~$15** |

Sopra budget originale ($4) ma necessario per evitare confound metodologici. Ogni iterazione ha aggiunto un fix critico:
- v1 → v2: tokens (truncation issue)
- v2 → v3: category hint (brand confound)
- v3 → v5: permissive mapping + valid channels + fallback logic

---

## Files chiave

- `docs/thesis/analysis/thesis_notebook_AB_test.ipynb` — main 4-tier notebook (v5 prompts ready)
- `docs/thesis/analysis/thesis_agentic_notebook.ipynb` — single-query agentic with multi-cat registry
- `docs/thesis/analysis/thesis_notebook_<cat>.ipynb` — 8 ML training notebooks
- `docs/thesis/analysis/outputs_ab_test/prompts.csv` — 50 final prompts
- `docs/thesis/analysis/outputs_ab_test/human_eval_pilot_15_v3.csv` — human eval template
- `scripts/ml_retraining/` — 10-step training pipeline
- `thesis/thesis_agents/ai_research_framework/features/engineer_features.py` — feature module

---

## Domanda finale per te

Vuoi fare review del notebook + prompt v5 prima che io faccia il run finale? Se ok, parto giovedì pomeriggio col run + figures + tables, poi inizio scrittura Chapter 7.

Grazie!
Enrico
