# Deployment Options: Technical Analysis & Clarifications

**Created:** 2026-04-27 15:45:00  
**Status:** Planning Phase (Detailed Technical Analysis)  
**Audience:** Brian & Enrico (thesis team)  
**Context:** Clarifying deployment options, sandbox setup, feature handling, and server requirements

---

## Part 1: Clarifying Docker & Server Deployment

### Your Concern: "Docker uses too much RAM on my laptop"

**This is a real problem, but the solution is NOT to skip Docker.**

### What "Deploy and maintain a server" means:

It means: somewhere, somewhere, there needs to be a **computer running continuously** that:
1. Has your API code loaded
2. Listens for HTTP requests from Prometheus
3. Processes predictions
4. Returns responses

**Three options for WHERE that computer is:**

#### **Option A: Your Local Laptop (Not Recommended)**
```
Your Laptop
└─ Docker container running FastAPI + model
   └─ Listening on http://localhost:8000/predict
```

**Problem:** Your laptop dies, internet connection drops → Nika can't call your model.  
**Good for:** Local testing only, not for the actual 50/50/50 experiment.

---

#### **Option B: Free Cloud Server (RECOMMENDED for your thesis)**

Services that offer **free tier**:

1. **Railway.app** (easiest)
   - Free tier: $5/month credit (enough for 1 small API)
   - Push Docker image → runs automatically
   - Cost: Free or ~$5/month max
   - Time to set up: 15 minutes

2. **Render.com**
   - Free tier: one free instance
   - Cost: Free
   - Time to set up: 20 minutes

3. **Fly.io**
   - Free tier: 3 shared-cpu-1x 256MB VMs
   - Cost: Free
   - Time to set up: 25 minutes

4. **Google Cloud Run**
   - Free tier: 2M requests/month
   - For your test (150 calls max): Free
   - Cost: Free for your use case
   - Time to set up: 30 minutes

**My recommendation: Railway.app or Render.com** — simplest, least setup.

**How it works:**
```
Your Computer (Train model locally)
  ↓
Push Docker image to Docker Hub (free, one command)
  ↓
Railway/Render pulls image automatically
  ↓
Your API runs on their server (https://your-api.railway.app/predict)
  ↓
Nika calls your endpoint from anywhere
```

**Zero maintenance:** Their server, their responsibility.

---

#### **Option C: Paid VPS (Overkill for thesis)**
- DigitalOcean: $6-12/month
- AWS: ~$10/month small instance
- Linode: ~$6/month

**Why skip:** Not needed. Railway is free and simpler.

---

### Docker Confusion: Why Does Option 1 (REST API) Need Docker?

**Short answer:** It doesn't HAVE to use Docker.

But let me clarify the options:

#### **Without Docker (Direct Server):**
```python
# install.sh (you run this on a server)
pip install fastapi uvicorn scikit-learn
python api.py  # Starts server on port 8000
```

**Problem:** 
- Different servers have different Python versions, dependencies, OS
- Your code works on your laptop but might break on Nika's server
- Hard to reproduce

#### **With Docker (Containerized):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY api.py model.pkl .
CMD ["uvicorn", "api:app", "--port", "8000"]
```

Then:
```bash
docker build -t my-model-api:v1 .
docker push docker.io/myname/my-model-api:v1
```

**Benefit:** 
- Same code, same environment, runs **identically** on any server
- Nika just does: `docker pull myname/my-model-api:v1` and runs it
- Easy to version (v1, v2, v3)

---

### **REST API vs Docker Container: What's the Difference?**

**They're not competing options. They're different layers:**

```
REST API       = What your server DOES (HTTP interface)
Docker         = HOW your server RUNS (containerized environment)
```

Think of it like a restaurant:

```
REST API    = The menu + how you order (HTTP requests/responses)
Docker      = The kitchen (isolated, reproducible environment)
Server      = The physical location (your laptop, Railway, AWS, etc.)
```

**Analogy:**
- Option 1: "I'll run a REST server on my laptop" → No Docker
- Option 4: "I'll run a REST server in a Docker container on Railway" → Docker + REST

**Option 4 is strictly better** because:
1. You can test locally in Docker
2. Same code runs on Railway (zero surprises)
3. Nika can run it anywhere
4. Easy to version models

---

## Part 2: Clarifying API Contracts & Function Signatures

### **Do we have to DEVELOP the API contract, or does it already exist?**

**Answer: You develop it together with Nika.**

Here's the workflow:

**Step 1: You propose a contract**
```
You: "Our model takes: product_id, market, time_period, price, promotion, distribution_percent
     It returns: prediction (units sold) + confidence score"

Nika: "Great. But can you also return which features were most important for this prediction?
       And can you handle missing values gracefully?"

You: "Yes, we can do that. Here's the updated contract..."
```

**Step 2: Document it formally**
```json
POST /predict
Request body:
{
  "product_id": "BEER_001",        // Required
  "market": "SUPERMARKET",          // Required
  "features": {
    "price": 99.5,                 // Optional: if missing, use last known value
    "promotion": true,              // Optional
    "distribution_percent": 85.0    // Optional
  }
}

Response:
{
  "prediction": 150000,
  "confidence": 0.87,
  "feature_importance": {
    "price": 0.35,
    "distribution_percent": 0.28,
    "promotion": 0.15
  },
  "model_version": "v1.2"
}
```

**Step 3: Both of you follow it**

You: Implement exactly that in your API  
Nika: Calls exactly that from her LangGraph code

---

### **Function Signature = The Blueprint**

In Python, a function signature is literally the first line:

```python
def predict_sales(
    product_id: str,
    market: str,
    features: dict[str, float]
) -> dict:
```

This tells you:
- **Inputs:** 3 things (product_id as string, market as string, features as dict)
- **Output:** returns a dict

**For Nika to understand what to send:**

"Your model function signature is:
```
predict_sales(product_id: str, market: str, features: dict) → dict
```

Which means: Send these 3 things, get a dict back."

---

## Part 3: The Sandbox & How It Works

### **What is a "Sandbox"?**

A sandbox is a **test version of Prometheus** that:
1. Runs in an isolated environment (not affecting production)
2. Can call external APIs (like your model server)
3. Provides logging/monitoring so you can see what's happening
4. Is safe to break without consequences

### **How Nika Likely Provides Sandbox Access**

Nika probably gives you:

**Option A: A URL you can test**
```
https://prometheus-sandbox.manifold-ai.com/chat

You type: "What will beer sales be next quarter?"
Prometheus (in sandbox):
1. Understands the question
2. Decides: "I need to call Brian's sales model"
3. Makes HTTP request to: http://your-api-server:8000/predict
4. Gets response: {"prediction": 150000, "confidence": 0.87}
5. Uses that in reasoning
6. Returns: "Based on current market data and ML prediction, I estimate 150,000 units..."
```

**Option B: A Python script/notebook**
```python
from prometheus import SandboxClient

client = SandboxClient(api_key="sk_test_xxxxx")

# Register your model endpoint
client.register_tool(
    name="sales_predictor",
    url="http://your-api-server:8000/predict",
    schema={...}  # The contract we discussed
)

# Now test
response = client.chat("What will beer sales be in Q2?")
print(response)
# Prometheus uses your model internally
```

**Option C: A webhook approach**
```
Nika tells you: "Register your endpoint here"
You: POST http://prometheus-setup.manifold-ai.com/register
Body: {
  "endpoint": "http://your-api-server:8000/predict",
  "model_name": "sales_forecaster",
  "version": "1.2"
}

Later, Nika's system automatically calls your endpoint when needed.
```

---

### **What We Don't Know Yet**

You need to ask Nika:

1. **"How do we register our model endpoint with the sandbox?"**
   - Is it a webhook? A config file? An API call?

2. **"Can we test locally first?"**
   - Can we run your API on localhost:8000 while testing with sandbox?
   - Or does the sandbox only accept publicly available URLs?

3. **"How do we monitor the calls?"**
   - Can we see logs of when Prometheus called our model?
   - Can we see request/response pairs?

4. **"What's the latency requirement?"**
   - Does each prediction need to return in <100ms? <1s?
   - If model takes 200ms, is that okay?

---

## Part 4: Feature Handling & Missing Values

### **Your Question: "What if Prometheus only provides a few features?"**

**This is a CRITICAL question.** The answer determines your entire approach.

### **Scenario:**

You trained your model on these 10 features:
```
1. price
2. promotion_active
3. distribution_percent
4. competitor_price
5. consumer_sentiment (from Indeks Danmark)
6. day_of_week
7. competitor_promotion
8. inventory_level
9. seasonality_factor
10. market_growth_trend
```

But Prometheus can only extract from the user prompt:
```
- product_id: "BEER"
- market: "SUPERMARKET"
- price: 99.50
- promotion_active: true
```

### **What do you do?**

#### **Option 1: Reject incomplete requests (Bad idea)**
```python
if "consumer_sentiment" not in features:
    return {"error": "Missing consumer_sentiment", "status": 400}
```

**Problem:** Your model can never be used.

---

#### **Option 2: Use default/placeholder values (Okay)**
```python
features = {
    "price": 99.50,
    "promotion_active": True,
    "distribution_percent": 85.0,  # Use last-known average
    "competitor_price": 95.0,       # Use historical average
    "consumer_sentiment": 0.72,     # Use market average
    "day_of_week": 3,               # Use middle value (Wednesday)
    "competitor_promotion": False,  # Use most common value
    "inventory_level": 1000,        # Use typical inventory
    "seasonality_factor": 1.0,      # No seasonality adjustment
    "market_growth_trend": 0.02     # Use historical trend
}

# Model makes prediction with these defaults
prediction = model.predict(features)
return {"prediction": prediction, "confidence": 0.62}  # Lower confidence
```

**Trade-off:** Model still works, but accuracy is lower (hence lower confidence score).

---

#### **Option 3: Have Prometheus ASK for missing features (Best idea)**

```python
# Your API receives: product, market, price, promotion
# Your model needs: all 10 features

# Your API returns:
{
    "missing_features": [
        "consumer_sentiment",
        "distribution_percent",
        "competitor_price"
    ],
    "clarifying_questions": [
        "What is the distribution percentage for this product in this market?",
        "What's the competitor's price for comparable products?",
        "Based on recent consumer data, how would you rate consumer sentiment?"
    ],
    "can_predict_with_defaults": True,
    "default_prediction": {
        "prediction": 145000,
        "confidence": 0.62,
        "note": "Low confidence because 3 key features are missing"
    }
}
```

Then Prometheus (via LLM) can:
- Ask the user follow-up questions
- Fill in the missing context
- Call your model again with complete features
- Get a higher-confidence prediction

**Example flow:**
```
User: "What will beer sales be next quarter?"

Prometheus (LLM): "I need some additional information to give you a better forecast.
- What's your estimated distribution for this product?
- Any major competitive activity expected?
- How's consumer sentiment in your market?"

User: "Distribution is 80%, no major competition changes, sentiment is stable."

Prometheus calls your API with complete features → 
Gets prediction with confidence 0.87 instead of 0.62
```

---

### **What You Should Do**

**Brainstorm with Nika:**

1. "What features can you reliably extract from user prompts?"
2. "For features you can't extract, would you rather:
   - Use default values (lower accuracy), OR
   - Have the LLM ask clarifying questions (higher accuracy)?"
3. "What's the acceptable confidence threshold?"

**My recommendation:** 
- Start with **Option 2 (defaults)** — simple, gets you going
- If accuracy is too low, upgrade to **Option 3 (clarifying questions)**

---

## Part 5: Complete Workflow for Your Thesis

### **Week 1: Model Training (Local)**
```
Your Laptop
└─ Train on Nielsen data
   ├─ Model v1 (untuned): sales_forecast_v1.pkl
   └─ Model v2 (tuned): sales_forecast_v2.pkl

Test locally:
  python test_model.py
  # Both models work, v2 is more accurate
```

---

### **Week 2: API Development (Local + Free Cloud)**

**Step 1: Build API locally**
```python
# api.py
from fastapi import FastAPI
import pickle

app = FastAPI()
model = pickle.load(open('sales_forecast_v1.pkl', 'rb'))

@app.post("/predict")
def predict(product_id: str, market: str, features: dict):
    # Handle missing features
    features_full = fill_missing_features(features)
    pred = model.predict([features_full])
    return {
        "prediction": float(pred[0]),
        "confidence": 0.75,  # You'd calculate this properly
        "model_version": "v1"
    }
```

**Step 2: Dockerize**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY api.py sales_forecast_v1.pkl .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Step 3: Test locally in Docker**
```bash
docker build -t my-sales-api:v1 .
docker run -p 8000:8000 my-sales-api:v1

# Test from another terminal
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"product_id":"BEER","market":"SUPER","features":{"price":99.5}}'
```

**Step 4: Push to free cloud (Railway)**
```bash
# Sign up at railway.app
# Connect your GitHub repo
# Railway auto-builds and deploys

# Your API is now at: https://my-sales-api-xxxxx.railway.app/predict
```

---

### **Week 2-3: Nika Integration (Parallel)**

**You:** Tell Nika your endpoint URL and API contract

**Nika:** 
1. Integrates into LangGraph
2. Sets up sandbox
3. Gives you sandbox access

**You:** Test the sandbox
```bash
# Test if Prometheus can call your model
curl -X POST https://prometheus-sandbox.manifold-ai.com/test_integration \
  -H "Authorization: Bearer sk_test_xxxxx" \
  -d '{"model": "sales_forecast", "test_case": 1}'

# Check logs to see if your endpoint was called
```

---

### **Week 3: Run 50/50/50 Experiment**

**Test 1: Baseline (Prometheus without your model)**
- Send 50 prompts to sandbox
- Log all responses
- Measure: accuracy, consistency, tone

**Test 2: With v1 (untuned models)**
- Deploy your API (already done)
- Send same 50 prompts
- Log responses
- Measure improvements

**Test 3: With v2 (tuned models)**
- Push new Docker image with v2 model
- Railway auto-deploys
- Send same 50 prompts
- Log responses
- Measure improvements

**Analysis:**
```
Response Quality Scores (0-10):
┌─────────────┬──────────────┬──────────────┬──────────────┐
│ Metric      │ Baseline     │ + v1 Model   │ + v2 Model   │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ Accuracy    │ 6.5          │ 7.2          │ 8.1          │
│ Consistency │ 6.0          │ 7.5          │ 7.9          │
│ Actionable  │ 7.0          │ 8.0          │ 8.5          │
│ Confidence  │ 6.2          │ 7.3          │ 8.0          │
└─────────────┴──────────────┴──────────────┴──────────────┘

Conclusion: ML-enhanced Prometheus significantly improves response quality,
with tuned models providing ~22% improvement over baseline.
```

---

## Summary Table: Your Setup

| Component | Technology | Location | Effort |
|-----------|-----------|----------|--------|
| **Model Training** | scikit-learn/XGBoost | Your laptop | 1 week |
| **API Framework** | FastAPI | Your laptop | 2-3 days |
| **Containerization** | Docker | Your laptop | 1 day |
| **Deployment** | Railway.app (free) | Cloud | 1 day |
| **Integration** | Nika handles | Her servers | ~1 week (parallel) |
| **Testing** | Sandbox endpoint | Cloud | 2-3 days |
| **Experiment** | 50/50/50 runs | Cloud + local analysis | 3 days |

**Total time: ~3 weeks (fits your deadline)**

---

## Next Steps: Questions for Nika

Before the meeting, prepare these questions:

1. **Sandbox Access:**
   - "How do we register our model endpoint?"
   - "Can we test locally (localhost) or does it need a public URL?"
   - "Can you show us a sandbox access example?"

2. **API Contract:**
   - "Which features can you reliably extract from user prompts?"
   - "For features you can't extract, should we use defaults or ask clarifying questions?"

3. **Monitoring:**
   - "How will we see logs of when our model is called?"
   - "Can we monitor latency and error rates?"

4. **Versioning:**
   - "If we push a new model version, how do we tell you to update?"
   - "Can we do it without restarting Prometheus?"

5. **Error Handling:**
   - "What happens if our model times out or returns an error?"
   - "Should we implement retries on your end or ours?"

---

## References

- [Railway.app Docs](https://docs.railway.app) — Easy Docker deployment
- [FastAPI Docs](https://fastapi.tiangolo.com) — API framework
- [Docker Docs](https://docs.docker.com) — Containerization basics
- [LangGraph Docs](https://langchain-ai.github.io/langgraph) — Prometheus's orchestration framework

