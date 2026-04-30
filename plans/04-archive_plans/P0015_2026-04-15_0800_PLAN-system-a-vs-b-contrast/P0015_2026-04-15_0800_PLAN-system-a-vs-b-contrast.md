---
created: 2026-04-15 15:50:00
---

# System A vs System B: Architecture Contrast

Quick reference showing why we're enhancing System B (not System A).

---

## Side-by-Side Comparison

| Aspect | **System A (Research)** | **System B (Thesis Writing)** |
|--------|---|---|
| **Purpose** | Evaluate multi-agent predictive AI framework under 8GB RAM constraint | Produce structured thesis content (bullets, compliance checks, figures) |
| **Output** | ModelForecast, SynthesisOutput, ValidationReport (objects evaluated in thesis Ch. 5–8) | Markdown bullet files, JSON state, PNG figures (invisible scaffolding) |
| **Methodology** | Frozen DSR artefact (Hevner 2004) — the *thing being researched* | Tooling to help write up research (not evaluated, not in thesis) |
| **State type** | `ResearchState` (TypedDict, for LangGraph) | `ThesisState` (Pydantic BaseModel) |
| **Orchestration** | LangGraph StateGraph with 4 phase nodes + human interrupts | Custom Coordinator (Plan → Execute → Critic → Persist) |
| **Immutability** | ✅ **FROZEN** — no modifications allowed; any change invalidates research | ❌ **EXTENSIBLE** — designed for add-ons and enhancements |
| **External deps** | Nielsen SQL, Indeks Danmark CSV, LangGraph, LangChain | PydanticAI, custom agents, file I/O, external APIs (Semantic Scholar, etc.) |

---

## Why NOT Modify System A

### 1. Research Integrity

System A is the **artefact being evaluated**. Its outputs are analysed in Ch. 5–8 and constitute the thesis's primary contribution. Changing it after Phase 1 is complete would:
- Invalidate performance benchmarks (Ch. 6)
- Alter synthesis logic (Ch. 7)
- Compromise validation results (Ch. 8)
- Break reproducibility claims

**Timeline**: Frozen since Phase 1 data assessment (March 2026). Too late for architecture changes.

### 2. Experimental Control

The thesis makes claims like:
> "System A achieves 46% median MAPE on LightGBM under 8GB RAM constraint"

If we modify System A code after these results, we can't claim the results are from the final system. Deadline is 15 May; no time for re-runs.

### 3. Design Science Methodology

DSR (Hevner 2004) requires:
- Explicit problem statement (chapter 1: done)
- Artefact specification (chapter 5: done)
- Implementation (System A: done)
- **Evaluation on the implemented artefact** (chapters 6–8: in progress)
- Communication (thesis writeup: in progress)

Modifying System A mid-evaluation violates the methodology.

---

## Why Enhance System B (Safe & Intended)

### 1. System B Was Built for This

Your colleague explicitly designed System B with:
- **Coordinator as router**: Adding new agents is a 5-line `elif` block
- **Pydantic state**: New fields are backward-compatible
- **Critic validation**: Automatically covers new agents (falls back to generic validator)
- **Toggle pattern**: Features are opt-in, not forced

This is deliberate extensibility engineering.

### 2. System B Has No Research Claims

System B outputs are:
- Bullet skeletons (scaffolding, not content)
- Compliance reports (metadata, not contribution)
- Figures (presentation, not research)

**No thesis claims rest on System B logic.** It's pure tooling.

### 3. Integration Doesn't Touch Research

Adding features like "Semantic Scholar API citation verification" to System B:
- Validates thesis references (doesn't change research results)
- Catches errors before supervisor review (beneficial, non-invasive)
- Is completely independent of System A

The research contribution stays untouched.

---

## Data Flow: How They Connect (and Don't)

```
┌─────────────────────────────────────────────────────────────┐
│ SYSTEM A: Research Framework (Frozen)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Nielsen CSD + Indeks Danmark                               │
│         ↓                                                    │
│  [Data Assessment] → ResearchState                          │
│         ↓                                                    │
│  [Forecasting: XGBoost, LightGBM, Prophet, ARIMA, Ridge]   │
│         ↓ ModelForecast objects                             │
│  [Synthesis: Ensemble + LLM calibration]                    │
│         ↓ SynthesisOutput object                            │
│  [Validation: ML accuracy + LLM-as-judge + RAM profile]     │
│         ↓ ValidationReport object                           │
│  ╔════════════════════════════════════════════════╗          │
│  ║ OUTPUT: JSON results files (not in codebase)  ║          │
│  ║  - phase2_benchmarks.csv                      ║          │
│  ║  - phase3_synthesis_output.json               ║          │
│  ║  - phase4_validation_report.json              ║          │
│  ╚════════════════════════════════════════════════╝          │
│                                                              │
│  STATUS: ✅ FROZEN — Do not modify                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘

               ⬇️ (read-only import)

┌─────────────────────────────────────────────────────────────┐
│ SYSTEM B: Thesis Production (Extensible)                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ThesisState (Pydantic) + toggles                           │
│         ↓                                                    │
│  PlannerAgent: "What tasks should run?"                     │
│         ↓ TaskPlan                                          │
│  ThesisCoordinator: Route to agents                         │
│         ├─ LiteratureAgent (paper corpus)                   │
│         ├─ WritingAgent (bullet skeletons)                  │
│         ├─ ComplianceAgent (APA 7, CBS checks) ← [ENHANCED] │
│         ├─ DiagramAgent (figures)                           │
│         └─ [NEW: IntegrityVerificationAgent] ← [ADDED]      │
│         ↓ outputs                                           │
│  CriticAgent: Validate outputs                              │
│         ↓                                                   │
│  state.save() → JSON                                        │
│                                                              │
│  SYSTEM A RESULTS (imported as context):                    │
│  - Read phase2_benchmarks.csv → cite in Ch. 6              │
│  - Read phase3_synthesis_output.json → mention in Ch. 7    │
│  - Read phase4_validation_report.json → discuss in Ch. 8   │
│                                                              │
│  STATUS: 🔧 EXTENSIBLE — Add features safely              │
│                                                              │
└─────────────────────────────────────────────────────────────┘

               ⬇️

┌─────────────────────────────────────────────────────────────┐
│ OUTPUT: Thesis (120 pages)                                  │
│  - Chapters 1–10 (human-written prose from System B bullets)│
│  - Bibliography (compiled from System B literature state)   │
│  - Figures (System B diagram agent + System A results)      │
│  - Appendices (System A experimental log, etc.)             │
└─────────────────────────────────────────────────────────────┘
```

**Key observation**: System A → System B is a one-way data flow (read-only). System B never modifies System A.

---

## Feature Integration Points (System B Only)

### Anti-Leakage Protocol

```
WritingAgent existing logic
  ↓
  ├─ _generate_bullets() → prose
  ↓
WritingAgent new logic (toggle-gated)
  ├─ check_material_gaps() [NEW]
  └─ Flag [MATERIAL GAP: ...] in state
  ↓
CriticAgent.validate()
  ├─ Fail if gaps remain unflagged [NEW VALIDATOR]
  ↓
state.save() → JSON
```

**Impact on System A**: Zero. WritingAgent doesn't touch ResearchState.

### Semantic Scholar Citation Verification

```
ComplianceAgent existing logic
  ├─ Check APA 7 format
  ├─ Check mandatory sections
  ↓
ComplianceAgent new logic (toggle-gated)
  ├─ verify_citations_with_api() [NEW]
  └─ Compare title, DOI, year against Semantic Scholar
  ↓
ComplianceState.citation_verification_report [NEW FIELD]
  ↓
state.save() → JSON
```

**Impact on System A**: Zero. ComplianceAgent doesn't touch ResearchState.

### Integrity Verification Gates

```
ThesisCoordinator._dispatch()
  ├─ [Existing agents]
  ↓
  ├─ IntegrityVerificationAgent.run() [NEW AGENT, NEW ROUTE]
  │  ├─ Phase A: Verify claims have citations
  │  ├─ Phase B: Verify references exist (via Semantic Scholar)
  │  ├─ Phase C–E: Manual checklists
  │  └─ Output: IntegrityReport
  ↓
ComplianceState.integrity_report [NEW FIELD]
  ↓
state.save() → JSON
```

**Impact on System A**: Zero. New agent is completely independent.

---

## Why Toggles Prevent Accidents

```python
# Toggle defaults to OFF
state.toggles = {
    "anti_leakage_protocol": False,
    "semantic_scholar_verification": False,
    "writing_quality_check": False,
    # ... etc
}

# Feature only runs if explicitly enabled
if state.toggles.get("anti_leakage_protocol", False):
    gaps = check_material_gaps(prose)
else:
    # Old behavior: no gap checking
    pass
```

**Safety**: If a feature breaks something, you disable it in 1 line. The system reverts to baseline behavior.

---

## Comparison: What You Can vs Can't Do

| Action | Safety | Reasoning |
|--------|--------|-----------|
| Add new field to ThesisState (e.g., `material_gaps`) | ✅ SAFE | Pydantic backward-compatible; old JSON still loads |
| Add new method to WritingAgent (e.g., `check_material_gaps()`) | ✅ SAFE | New method, doesn't touch existing methods |
| Add new elif to Coordinator._dispatch() | ✅ SAFE | Routing logic, new branch doesn't affect existing routes |
| Add new entry to Critic.validators | ✅ SAFE | Dict lookup; new agents handled independently |
| Modify System A agent logic | ❌ UNSAFE | Invalidates research results; frozen methodology |
| Change WritingAgent to output prose instead of bullets | ❌ UNSAFE | Violates frozen decision: "Writing Agent produces ONLY bullets" |
| Swap out LangGraph in System A for a different orchestrator | ❌ UNSAFE | Changes how research is executed; invalidates results |
| Extend System B with new agents that don't touch System A | ✅ SAFE | Completely independent; new functionality |
| Import System A data (CSV/JSON results) into System B for citation | ✅ SAFE | Read-only import; no modification of System A |

---

## Testing Strategy (No System A Risk)

### Pre-Integration: Baseline

1. Run System B with all toggles OFF
2. Generate 1 chapter (e.g., Ch. 5: Framework Design)
3. Check output is valid Markdown bullet file
4. Verify state.json saves/loads correctly
5. **Baseline established**: This is the reference behavior

### Post-Integration: Feature Tests (One at a Time)

For each new feature:

1. **Enable toggle**: `state.toggles["feature"] = True`
2. **Run same chapter** (e.g., Ch. 5)
3. **Check output**: Does the feature work as intended?
4. **Check state**: Is state.json still valid?
5. **Disable toggle**: `state.toggles["feature"] = False`
6. **Re-run chapter**: Does output match baseline from Step 1?

If Step 6 matches Step 1 output exactly → **Feature is isolated**.

---

## Conclusion

| Aspect | Status |
|--------|--------|
| **Can we enhance System B safely?** | ✅ YES — Architecture supports it |
| **Will System A be affected?** | ✅ NO — Complete separation of concerns |
| **Can features be toggled on/off?** | ✅ YES — Toggles are first-class citizens |
| **Can we roll back if something breaks?** | ✅ YES — Disable feature, revert code, baseline preserved |
| **Are the frozen decisions preserved?** | ✅ YES — System A untouched, WritingAgent still bullets-only |

**You can proceed with confidence. Your colleague's architecture was designed exactly for this.**
