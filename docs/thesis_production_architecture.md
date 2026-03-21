# Thesis Production Architecture
> Last updated: 2026-03-15

---

## 1. System Separation — Why Two Systems Exist

This project contains **two completely separate multi-agent systems** that must never be confused:

| | System A | System B |
|---|---|---|
| **Name** | AI Research Framework | Thesis Production System |
| **Directory** | `/ai_research_framework/` | `/thesis_production_system/` |
| **Purpose** | The experimental architecture being **evaluated in the thesis** | Internal tooling for **writing and managing the thesis** |
| **Appears in thesis** | Yes — Chapters 5–8 describe and evaluate this system | No — production tooling is NOT the research contribution |
| **RAM constraint** | ≤ 8 GB (hard — SRQ1 evaluation dimension) | Not constrained |
| **Orchestrator** | LangGraph StateGraph + `ResearchState` (TypedDict) | `ThesisCoordinator` + `ThesisState` (Pydantic) |

**Critical rule**: Do not describe System B agents (PlannerAgent, CriticAgent, DiagramAgent, etc.) as part of the research contribution. The research framework is System A only.

---

## 2. System A — AI Research Framework

### 2.1 Purpose
The experimental multi-agent forecasting system. This is the artefact being designed, implemented, and evaluated by the thesis. Its architecture answers the four SRQs.

### 2.2 Directory structure
```
ai_research_framework/
  config.py                     ← 8GB RAM constraint, model list, LLM config
  requirements.txt
  agents/
    data_assessment_agent.py    ← Phase 1: Nielsen + Indeks Danmark quality check
    forecasting_agent.py        ← Phase 2: 5 models, sequential execution, RAM profiling
    synthesis_agent.py          ← Phase 3: ensemble + calibration + Claude API recommendation
    validation_agent.py         ← Phase 4: 3-level evaluation framework
  state/
    research_state.py           ← LangGraph TypedDict (ResearchState)
  core/
    coordinator.py              ← LangGraph StateGraph with conditional edges + interrupt nodes
```

### 2.3 Key architectural decisions
- **Sequential model execution**: models are loaded, run, and explicitly unloaded one at a time to stay within ≤8GB RAM
- **LangGraph StateGraph**: typed state with conditional routing and human-in-the-loop interrupt nodes
- **Claude API for synthesis**: no local LLM, avoiding the ~3–6GB RAM footprint of a local model
- **Post-hoc calibration**: Kuleshov et al. (ICML 2018) isotonic regression applied to all model prediction intervals

### 2.4 Agent responsibilities

| Agent | Input | Output | SRQs |
|---|---|---|---|
| Data Assessment Agent | Nielsen SQL/CSV, Indeks Danmark CSV | Feature matrix, quality report | Precondition |
| Forecasting Agent | Feature matrix | 5 × `ModelForecast` (point, interval, MAPE, RAM) | SRQ1 |
| Synthesis Agent | 5 × `ModelForecast` + consumer signals | `SynthesisOutput` (confidence score, recommendation) | SRQ2 |
| Validation Agent | All outputs | `ValidationReport` (3 levels) | SRQ1–SRQ4 |

### 2.5 State flow
```
ResearchState (TypedDict)
│
├── data_assessment → writes: nielsen_data, indeks_data, feature_matrix, consumer_signals
│                     requires_human_approval = True
├── forecasting     → writes: model_forecasts (Dict[str, ModelForecast])
│                     requires_human_approval = True
├── synthesis       → writes: synthesis_output (SynthesisOutput)
├── validation      → writes: validation_report (ValidationReport)
│                     requires_human_approval = True
└── complete
```

---

## 3. System B — Thesis Production System

### 3.1 Purpose
Tooling to assist in planning, writing, validating, and documenting the thesis. Agents in this system are production helpers — they do not constitute the research contribution.

### 3.2 Directory structure
```
thesis_production_system/
  requirements.txt
  agents/
    planner_agent.py            ← Reads state → produces TaskPlan (JSON)
    critic_agent.py             ← Validates agent outputs → CriticResult
    literature_agent.py         ← Literature scraping, corpus management
    writing_agent.py            ← Bullet point generation for thesis sections
    compliance_agent.py         ← CBS formal requirement checks
    diagram_agent.py            ← Code-generated thesis figures (graphviz + matplotlib)
  state/
    thesis_state.py             ← Pydantic ThesisState (root shared state)
  core/
    coordinator.py              ← ThesisCoordinator (Plan → Execute → Critic loop)
```

### 3.3 Shared state
`ThesisState` (Pydantic BaseModel) is the single source of truth for all System B agents:
```python
ThesisState = {
    "literature_state":  LiteratureState,   # papers, gap analysis version, RQ version
    "thesis_outline":    Dict,              # chapter structure
    "sections":          Dict[str, SectionState],  # per-chapter status
    "figures":           Dict[str, FigureState],   # generated figures
    "compliance_checks": ComplianceState,   # CBS check results, page count
}
```
State is persisted to `docs/tasks/thesis_state.json` after every session.

---

## 4. Planner Agent

### 4.1 Purpose
Produces a structured `TaskPlan` (JSON) indicating which agents should run and in what order. The Planner does NOT execute tasks.

### 4.2 Planning rules
| Rule | Trigger | Agent | Action |
|---|---|---|---|
| 1 | Papers pending confirmation | LiteratureAgent | confirm_pending_papers |
| 2 | Chapters with no bullet points | WritingAgent | draft_section_bullets |
| 3 | Approved bullets, no compliance check | ComplianceAgent | check_section_compliance |
| 4 | Core figures missing from figures/ | DiagramAgent | generate_figures |
| 5 | No scraping run completed | LiteratureAgent | run_scraping |

### 4.3 Output schema
```json
{
  "tasks": [
    {
      "agent": "LiteratureAgent",
      "action": "update_gap_analysis",
      "priority": 1,
      "context": {},
      "rationale": "3 new confirmed papers need gap analysis update."
    }
  ],
  "planning_rationale": "Session 20260315-120000 — 2 task(s) planned.",
  "session_id": "20260315-120000",
  "blocked_tasks": []
}
```

---

## 5. Critic Agent

### 5.1 Purpose
Validates the output of every execution agent before `ThesisCoordinator` accepts it and updates `ThesisState`.

### 5.2 Validation output schema
```json
{
  "status": "valid",
  "issues": [],
  "confidence": 0.92,
  "agent_evaluated": "WritingAgent",
  "action_evaluated": "draft_section_bullets",
  "suggestions": []
}
```

```json
{
  "status": "invalid",
  "issues": [
    "Section bullets missing methodology subsection",
    "No citation placeholders found"
  ],
  "confidence": 0.35,
  "agent_evaluated": "WritingAgent",
  "action_evaluated": "draft_section_bullets",
  "suggestions": ["Add 'Cite: [Author Year]' markers.", "Add ## Methodology sub-bullet."]
}
```

### 5.3 Per-agent validation rules

| Agent | Action | Checks |
|---|---|---|
| LiteratureAgent | update_gap_analysis | Required headers, SRQ references |
| WritingAgent | draft_section_bullets | Bullet format (no prose), citation placeholders, SRQ references |
| ComplianceAgent | check_section_compliance | Required compliance fields present |
| DiagramAgent | generate_figures | SVG + PNG files exist on disk |
| LiteratureAgent | run_scraping | TIER A/B tables, relevance scores |

---

## 6. Diagram Agent

### 6.1 Purpose
Generates all thesis figures as reproducible, code-generated artefacts. No manual diagram drawing. Every figure traces back to a Python function in `diagram_agent.py`.

### 6.2 Available figures

| Figure ID | Type | Tool | Status |
|---|---|---|---|
| `system_architecture_v1` | Architecture | graphviz | ⬜ Not generated |
| `agent_workflow_v1` | Workflow | graphviz | ⬜ Not generated |
| `data_flow_v1` | Data flow | graphviz | ⬜ Not generated |
| `model_performance_v1` | Bar chart | matplotlib | ⬜ Placeholder data |
| `evaluation_plot_v1` | Multi-panel | matplotlib | ⬜ Placeholder data |

Output location: `docs/thesis/figures/`
Output formats: SVG (vector, for thesis PDF) + PNG (raster, for preview)

### 6.3 Usage
```python
from thesis_production_system.agents.diagram_agent import DiagramAgent
agent = DiagramAgent()
state = agent.run(state, figure_ids=["system_architecture_v1", "agent_workflow_v1"])
```

---

## 7. Updated Execution Workflow

```
┌─────────────────────────────────────────────────┐
│               ThesisCoordinator                 │
│                                                 │
│  1. Load ThesisState (from thesis_state.json)   │
│  2. PlannerAgent.run(state) → TaskPlan          │
│  3. For each task in TaskPlan:                  │
│       a. Dispatch to agent                      │
│       b. Execute agent action                   │
│       c. CriticAgent.validate(output)           │
│       d. Valid → update state → continue        │
│          Invalid → retry once with issues       │
│          Still invalid → log + skip             │
│  4. state.save() → thesis_state.json            │
│  5. Print session summary                       │
│  ↓                                              │
│  HUMAN REVIEW of session outputs                │
│  HUMAN APPROVAL before any phase transition     │
└─────────────────────────────────────────────────┘
```

---

## 8. Migration Notes

### 8.1 What existed before this refactor
- All agents defined conceptually in `CLAUDE.md` only
- No Python code existed — pure documentation/planning phase
- Agents were not separated into System A vs System B

### 8.2 What changed
- Created `/ai_research_framework/` with System A code skeletons (research agents)
- Created `/thesis_production_system/` with System B code (Planner, Critic, Diagram + existing agents)
- Shared state formalised: `ResearchState` (TypedDict, LangGraph) for System A; `ThesisState` (Pydantic) for System B
- `docs/thesis/figures/` created as the Diagram Agent output directory
- `docs/tasks/thesis_state.json` will be the System B state persistence file (created at first run)

### 8.3 What did NOT change
- 8GB RAM constraint (System A `config.py`)
- Sequential model execution protocol
- LangGraph + PydanticAI as the System A stack
- All existing documentation in `docs/`
- CLAUDE.md (no changes to the coordinator manifest)
- Literature paper annotations and thesis chapter skeletons
