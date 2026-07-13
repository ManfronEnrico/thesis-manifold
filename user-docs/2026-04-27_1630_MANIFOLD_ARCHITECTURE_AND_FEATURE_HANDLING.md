# Manifold AI Architecture & Nielsen Feature Handling

**Created:** 2026-04-27 16:30:00  
**Status:** Understanding Manifold Backend + Feature Engineering  

## Part 1: Manifold's Multi-Backend Architecture

Your presentation slide shows:

```
Frontend (Multi-channel interaction) → Backend (Multi-component)
                                    └─ Customized Knowledge (Nielsen data for you)
                                    └─ External Data (Indeks Danmark)
                                    └─ Multi-Agent Orchestration (LangGraph)
                                    └─ Your ML Models HERE
                                    └─ Workflow + Security
```

**Where your models fit:** "Third-Party AI Tools" → Your models become callable tools in LangGraph.

---

## Part 2: LangGraph vs n8n

**Similarity:** Both orchestrate multi-step workflows.

**Difference:** 
- n8n = Visual UI for business automation
- LangGraph = Code-based AI agent orchestration

LangGraph is enterprise-scale in the sense that it's designed for production AI systems with persistent state across agents.

---

## Part 3: Nielsen Features Available

**Raw from Nielsen Facts Table:**
- sales_units, sales_liters, sales_value
- sales_units_any_promo, sales_liters_any_promo, sales_value_any_promo
- weighted_distribution (0–1 scale, e.g., 0.92 = 92%)

**From Nielsen Product Dimension:**
- brand (COCA COLA, FANTA, PEPSI, etc.)
- category (CSD, TotalBeer, EnergyDrink, etc.)
- type (COLA, LEMON, APPLE, etc.)
- regular_light (REGULAR or LIGHT)
- price_category (BILLIGVAND = budget, MÆRKEVARE = premium)
- organic, private_label, packaging, size

**From Nielsen Market (28 options):**
- Market names (MENY, REMA 1000, BILKA, FØTEX, etc.)
- Default: DVH EXCL. HD (unless user specifies)

**From Indeks Danmark (External):**
- consumer_sentiment, income_growth, unemployment_rate, inflation

**Engineered Features (what you'd add):**
- sales_trend = (current - prev) / prev
- promotion_intensity = promo_sales / total_sales
- seasonality_factor = current / yearly_avg
- market_concentration = share_at_market / total_share
- days_since_last_promotion
- competing_brands_count
- market_share_change

**Total: ~25–35 features** for your model.

---

## Part 4: The User Knowledge Problem

**User asks:** "What will CSD sales be in Q2 at MENY?"

**Prometheus extracts easily:**
- ✓ Category: CSD
- ✓ Market: MENY
- ✓ Period: Q2

**Prometheus cannot extract:**
- ✗ Which brands? (COCA COLA? FANTA? All?)
- ✗ Regular or Light?
- ✗ Premium or budget segment?
- ✗ Promotion planned?
- ✗ Consumer mood?

**Result:** 5 features provided, model needs 25–35.

---

## Part 5: Handling Missing Features

### Strategy 1: Use Defaults (Start here)

Fill missing features from historical averages for that market/category/period.

**Example:**
```
Historical avg for CSD at MENY in Q2:
- sales_trend: +5% (typical growth)
- promotion_intensity: 25% (typical promo level)
- consumer_sentiment: 0.68 (neutral/positive)
- distribution: 92% (historical average)
```

**Pros:** Works immediately, simple  
**Cons:** Lower confidence (~0.62 instead of 0.87)

### Strategy 2: Ask Clarifying Questions (Higher accuracy)

```
Prometheus: "To give you a more accurate forecast, I need to know:
1. Which brands? (COCA COLA, FANTA, PEPSI, or all?)
2. Regular or Light variants?
3. Premium or budget segment?
4. Promotion planned for Q2?"

User provides answers → model gets full features → high confidence (0.87)
```

**Recommendation:** Start with Strategy 1. If confidence is too low, upgrade to Strategy 2.

---

## Part 6: Your API Contract (Input/Output)

### Input Example:
```json
POST /predict
{
  "product_id": "4722",
  "market": "MENY",
  "time_period": "2026-Q2",
  "features": {
    "category": "CSD",
    "brand": "COCA COLA",
    "regular_light": "REGULAR",
    "price_category": "MÆRKEVARE",
    "sales_trend": 0.05,
    "promotion_intensity": 0.25,
    "weighted_distribution": 0.92,
    "seasonality_factor": 1.15,
    "consumer_sentiment": 0.68,
    "income_growth": 0.02,
    "unemployment_rate": 0.045,
    ... (25-35 total features)
  }
}
```

### Output Example:
```json
{
  "prediction": 152340.5,
  "prediction_unit": "units",
  "confidence": 0.87,
  "model_version": "v1.2",
  "feature_importance": {
    "sales_trend": 0.28,
    "weighted_distribution": 0.22,
    "promotion_intensity": 0.18,
    "consumer_sentiment": 0.12,
    "seasonality_factor": 0.10,
    "other": 0.10
  },
  "prediction_range": {
    "lower_95pct": 140000,
    "upper_95pct": 165000
  },
  "processing_time_ms": 45
}
```

---

## Part 7: Complete Timeline

**Week 1:** Train models locally using Nielsen + Indeks data  
**Week 2:** Build FastAPI endpoint, deploy to Railway (free)  
**Week 2-3 (parallel):** Nika integrates into LangGraph, sets up sandbox  
**Week 3:** Run 50/50/50 experiment (baseline → +v1 → +v2)  
**Week 4:** Analysis + write results  

---

## Going Forward: Filename Convention

Use: `YYYY-MM-DD_HHMM_DESCRIPTIVE_TITLE.md`

Examples:
- `2026-04-27_1630_MANIFOLD_ARCHITECTURE_AND_FEATURE_HANDLING.md`
- `2026-04-27_1545_DEPLOYMENT_OPTIONS_TECHNICAL_ANALYSIS.md`
- `2026-04-27_1430_PROMETHEUS_INTEGRATION_OVERVIEW.md`

This ensures chronological sorting, time precision, and immutable record of when analysis was done.
