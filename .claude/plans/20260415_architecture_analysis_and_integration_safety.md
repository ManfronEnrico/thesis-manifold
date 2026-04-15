---
created: 2026-04-15 15:45:00
updated: 2026-04-15 15:45:00
---

# Architecture Analysis & Integration Safety Plan

## Executive Summary

Your colleague built a **modular, non-invasive agent architecture** with clear separation between System A (research) and System B (thesis writing). Integrating external skills as toggleable features will **not break anything** if we follow the architecture's patterns. This document proves it.

**Key insight**: Your architecture is designed for add-ons. Extensions are safe.

---

## 1. Current Architecture Overview

### 1.1 System B: Thesis Production (Your Writing Scaffolding)

**Pattern**: Coordinator → Planner → Dispatch → Agent → Critic → State Update

```
ThesisState (Pydantic)
    ↓
PlannerAgent.run(state) → TaskPlan (JSON)
    ↓
ThesisCoordinator._execute_task(task)
    ├─ _dispatch(task) → Agent.action() → output
    ├─ CriticAgent.validate(output) → CriticResult
    └─ If valid → update state; else → retry or skip
    ↓
state.save() → JSON persistence
```

**Key properties**:
- **Immutable state flow**: `ThesisState` is passed, agents return modified copy
- **Pluggable agents**: New agent types added via `_dispatch` routing table
- **Critic validation**: All agent outputs validated before state update
- **Retry with feedback**: Failed tasks retry once with critic issues for context

### 1.2 System A: AI Research Framework (Your Frozen Artefact)

**Pattern**: LangGraph StateGraph → Phase nodes → Human-in-the-loop interrupts

```
ResearchState (TypedDict for LangGraph)
    ↓
graph.invoke(state)
    ├─ data_assessment → _should_continue_after_data()
    ├─ forecasting → _should_continue_after_forecasting()
    ├─ synthesis → _should_continue_after_synthesis()
    ├─ validation → _should_continue_after_validation()
    └─ [human interrupts at forecasting + validation]
    ↓
Output: ModelForecast, SynthesisOutput, ValidationReport
```

**Key properties**:
- **Frozen**: No changes allowed (research artefact being evaluated)
- **Checkpointing**: MemorySaver persists state across invocations
- **Type-safe**: ResearchState is TypedDict (stricter than Pydantic)

### 1.3 Separation of Concerns

| Aspect | System A | System B |
|--------|----------|----------|
| **Data** | `ResearchState` (TypedDict) | `ThesisState` (Pydantic) |
| **Orchestration** | LangGraph | Custom Coordinator |
| **Communication** | Outputs: ModelForecast, SynthesisOutput, ValidationReport | Outputs: Markdown files + JSON state |
| **Immutability** | Frozen (no modifications) | Extensible (add agents safely) |

**The two systems do NOT share state.** System B reads System A outputs (CSV/JSON) but never modifies System A code or logic.

---

## 2. How Your Colleague Built for Extensibility

### 2.1 The Coordinator is a Router, Not Logic

**Pattern** (from `coordinator.py:112–168`):

```python
def _dispatch(self, task: Task, state: ThesisState) -> tuple[Any, ThesisState]:
    """Route task to the appropriate agent method."""
    
    if task.agent == "LiteratureAgent":
        if task.action == "run_scraping":
            new_state = self.literature_agent.run_scraping(state)
            return "scraping_complete", new_state
        elif task.action == "update_gap_analysis":
            new_state = self.literature_agent.update_gap_analysis(state)
            return "gap_analysis_updated", new_state
    
    elif task.agent == "WritingAgent":
        if task.action == "draft_section_bullets":
            # ... agent call and state update
    
    # [more agents...]
    
    raise ValueError(f"Unknown task: {task.agent}.{task.action}")
```

**Why this is extensible**:
- Adding a new agent = add one more `elif task.agent == "NewAgent"` block
- No changes to Coordinator logic, Planner, or Critic needed
- New agent inherits the Critic validation pipeline automatically

### 2.2 The Critic Validates Everything

**Pattern** (from `critic_agent.py:42–62`):

```python
def validate(self, agent: str, action: str, output: Any, context: Dict) -> CriticResult:
    """Dispatch to validator based on agent + action."""
    validators = {
        ("LiteratureAgent", "update_gap_analysis"): self._validate_gap_analysis,
        ("WritingAgent", "draft_section_bullets"): self._validate_section_bullets,
        ("ComplianceAgent", "check_section_compliance"): self._validate_compliance_check,
        # ...
    }
    validator = validators.get(key, self._validate_generic)
    return validator(output, context or {})
```

**Why this is safe**:
- Unknown agent/action combos fall back to `_validate_generic` (permissive)
- Each validator is independent (changing one doesn't affect others)
- Validators return `CriticResult` (never raise exceptions)
- Invalid outputs don't break the pipeline; they're logged and retried

### 2.3 State is Pydantic (Type-Safe)

**Pattern** (from `thesis_state.py:95–130`):

```python
class ThesisState(BaseModel):
    literature_state: LiteratureState = Field(default_factory=LiteratureState)
    thesis_outline: Dict[str, Any] = Field(default_factory=dict)
    sections: Dict[str, SectionState] = Field(default_factory=dict)
    figures: Dict[str, FigureState] = Field(default_factory=dict)
    compliance_checks: ComplianceState = Field(default_factory=ComplianceState)
    # [task tracking fields...]
    
    def save(self, path: Optional[str] = None) -> None:
        target = Path(path or self.state_file)
        target.write_text(self.model_dump_json(indent=2))
    
    @classmethod
    def load(cls, path: str = "docs/tasks/thesis_state.json") -> "ThesisState":
        p = Path(path)
        if p.exists():
            return cls.model_validate_json(p.read_text())
        return cls()
```

**Why this is safe for extensions**:
- Pydantic validates on load/save (type safety)
- Adding new fields = backward-compatible (old JSON still loads)
- All agents receive the same state object (consistency)
- State is serialized to JSON (human-readable, debuggable)

---

## 3. Integration Safety Principles

### Principle 1: Never Modify System A

**Your constraint**: System A is the research artefact being evaluated. Changing its code could invalidate the research contribution.

**Safe integration**: Only import/adapt from academic repos into System B. Example:

```python
# ✅ SAFE: Import anti-leakage protocol into System B agent
from ai_research_framework.state import ResearchState  # Read-only reference

class WritingAgentEnhanced:
    def check_material_gaps(self, prose: str) -> List[str]:
        """NEW METHOD — added to WritingAgent"""
        # Uses anti-leakage logic (NOT modifying System A)
        gaps = []
        for claim in parse_claims(prose):
            if not self._has_source(claim):
                gaps.append(f"[MATERIAL GAP: {claim}]")
        return gaps

# ❌ UNSAFE: Modify System A coordinator logic
# from ai_research_framework.core.coordinator import Coordinator
# Coordinator.run_research_with_toggles = ...  # Don't do this!
```

### Principle 2: Extend via State + Agents, Not by Modifying Existing Code

**Architecture guarantees**:
- ThesisState can grow new fields without breaking existing agents
- Coordinator._dispatch can route to new agents without touching existing ones
- Critic can validate new agents with a single dict entry

**Safe extension pattern**:

```python
# Step 1: Extend ThesisState
class ThesisState(BaseModel):
    # [existing fields...]
    toggles: Dict[str, bool] = Field(default_factory=dict)  # NEW FIELD ← non-breaking
    material_gaps: List[str] = Field(default_factory=list)  # NEW FIELD ← non-breaking

# Step 2: Add new agent to Coordinator._dispatch
def _dispatch(self, task: Task, state: ThesisState) -> tuple[Any, ThesisState]:
    # [existing elif blocks...]
    
    elif task.agent == "EnhancedWritingAgent":  # NEW AGENT
        if task.action == "check_material_gaps":
            new_state = self.enhanced_writing_agent.check_material_gaps(state)
            return "gaps_checked", new_state

# Step 3: Add validator to Critic
validators = {
    # [existing entries...]
    ("EnhancedWritingAgent", "check_material_gaps"): self._validate_material_gaps,  # NEW
}
```

**No existing code changes required.** System B stays intact; new features are add-ons.

### Principle 3: Use Toggles for Optional Features

**Your toggle pattern** (from plan):

```python
# In ThesisState
toggles = {
    "pipeline_state_machine": False,
    "anti_leakage_protocol": True,
    "semantic_scholar_verification": True,
    "writing_quality_check": False,
    "style_calibration": False,
    "integrity_verification_gates": False,
}
```

**Implementation pattern**:

```python
class WritingAgent:
    def draft_section_bullets(self, state: ThesisState, chapters: List[str]) -> ThesisState:
        # [existing logic...]
        
        # NEW: Check toggles before running enhancements
        if state.toggles.get("anti_leakage_protocol", False):
            gaps = self.check_material_gaps(prose)
            if gaps:
                state.material_gaps.extend(gaps)
        
        if state.toggles.get("writing_quality_check", False):
            issues = self.check_writing_quality(prose)
            if issues:
                # Flag for human review, don't block publication
                state.warnings.append(f"Writing QC: {issues}")
        
        return state
```

**Safety**: Toggles are off by default. Features only run when explicitly enabled. No side effects.

---

## 4. Per-Feature Integration Safety Analysis

### Feature 1: Pipeline State Machine ⚙️

**What it adds**: Chapter readiness tracking + blockers

**Integration pattern**:
- Add `chapter_states: Dict[str, str]` to ThesisState
- Planner reads chapter_states before planning tasks
- New "monitor blockers" task in TaskPlan (optional)

**Risk level**: ⚠️ LOW
- Non-invasive state tracking
- No existing agent logic changes
- Can be toggled off (Planner ignores chapter_states)

**Code safety**: 
```python
# In PlannerAgent.run()
if state.toggles.get("pipeline_state_machine", False):
    # Route around blocked chapters
    for ch_id, status in state.chapter_states.items():
        if status == "blocked":
            blocked.append(ch_id)
else:
    # Existing logic: plan all chapters
    pass
```

### Feature 2: Anti-Leakage Protocol 🚨

**What it adds**: Material gap detection in prose

**Integration pattern**:
- Add `material_gaps: List[str]` to ThesisState
- Enhance WritingAgent with `check_material_gaps()` method
- Call from within draft workflow (toggle-gated)

**Risk level**: ✅ SAFE
- Only adds validation checks
- Returns flags, doesn't block publication
- Human decides what to do with gaps

**Code safety**:
```python
class WritingAgent:
    def draft_section_bullets(self, state, chapters) -> ThesisState:
        prose = self._generate(chapters, state)
        
        if state.toggles.get("anti_leakage_protocol", False):
            gaps = self._check_gaps(prose)
            state.material_gaps = gaps
        
        return state  # State persists; gaps visible in JSON
```

### Feature 3: Semantic Scholar API ✓

**What it adds**: Citation verification via API

**Integration pattern**:
- Add `citation_verification_report: Dict[str, str]` to ComplianceState
- New ComplianceAgent validator method
- Call from compliance check step (toggle-gated)

**Risk level**: ✅ SAFE
- ComplianceAgent already validates; add one more check
- API is read-only (no side effects)
- Graceful degradation if API fails

**Code safety**:
```python
class ComplianceAgent:
    def check_section_compliance(self, state: ThesisState, chapters) -> ThesisState:
        # [existing APA 7, structure checks...]
        
        if state.toggles.get("semantic_scholar_verification", False):
            for ch_id in chapters:
                citations = self._extract_citations(state.sections[ch_id])
                report = self._verify_with_api(citations)
                state.compliance_checks.citation_verification_report[ch_id] = report
        
        return state
```

### Feature 4: Writing Quality Check 📝

**What it adds**: Prose pattern detection (em dashes, sentence rhythm, etc.)

**Integration pattern**:
- Enhance CriticAgent with prose quality validators
- Add to existing `_validate_section_bullets` method
- Toggle controls severity (fail vs. warn)

**Risk level**: ✅ SAFE
- Critic already validates prose structure
- Only adds more checks; doesn't modify existing ones
- Non-blocking (issues are warnings, not errors)

**Code safety**:
```python
class CriticAgent:
    def _validate_section_bullets(self, output, context) -> CriticResult:
        issues = []
        # [existing checks: bullet format, no prose, etc.]
        
        if context.get("toggles", {}).get("writing_quality_check", False):
            quality_issues = self._check_prose_quality(output)
            issues.extend(quality_issues)
        
        return CriticResult(
            status="valid" if not issues else "invalid",
            issues=issues,
            # ...
        )
```

### Feature 5: Style Calibration 🎨

**What it adds**: Author voice learning + soft guide

**Integration pattern**:
- Add `style_profile: Dict[str, Any]` to ThesisState
- Extract from Ch. 1 (one-time, manual)
- Pass to WritingAgent as context (toggle-gated)

**Risk level**: ✅ SAFE
- Read-only profile (no state mutation)
- Soft guide only (not hard rules)
- Completely optional

**Code safety**:
```python
class WritingAgent:
    def draft_section_bullets(self, state: ThesisState, chapters) -> ThesisState:
        context = {}
        if state.toggles.get("style_calibration", False):
            context["style_guide"] = state.style_profile
        
        prose = self._generate(chapters, state, context)
        return state
```

### Feature 6: Integrity Verification Gates 🔒

**What it adds**: 5-phase pre-submission checks (A–E)

**Integration pattern**:
- New agent: `IntegrityVerificationAgent`
- Add to Coordinator._dispatch routing
- New ComplianceState field: `integrity_verification_report`
- Called as final pre-submission step (toggle-gated)

**Risk level**: ⚠️ LOW-MEDIUM
- Self-contained agent (no touching existing agents)
- Outputs report (human decision on pass/fail)
- Can fail gracefully (Phase C, D, E are mostly manual)

**Code safety**:
```python
class IntegrityVerificationAgent:
    def run(self, state: ThesisState) -> ThesisState:
        if state.toggles.get("integrity_verification_gates", False):
            report = {
                "phase_a": self._verify_claims(state),
                "phase_b": self._verify_refs(state),
                "phase_c": self._check_data(),  # Manual checklist
                "phase_d": self._check_plagiarism(),  # Manual checklist
                "phase_e": self._check_ethics(),  # Manual checklist
            }
            state.compliance_checks.integrity_report = report
        return state

# In Coordinator._dispatch:
elif task.agent == "IntegrityVerificationAgent":
    if task.action == "run_integrity_check":
        new_state = self.integrity_agent.run(state)
        return "integrity_check_complete", new_state
```

---

## 5. Risk Mitigation Checklist

### Before You Enable Any Feature

- [ ] **System A isolation**: No imports from `ai_research_framework` core agents (read-only data structures only)
- [ ] **State backward compatibility**: New ThesisState fields have defaults (old JSON still loads)
- [ ] **Critic coverage**: New agent outputs have a validator (in CriticAgent.validators dict)
- [ ] **Toggle default**: All new features default to `False` (opt-in, not forced)
- [ ] **Error handling**: All new code catches exceptions and logs (never crashes Coordinator)
- [ ] **No prose generation**: WritingAgent still produces bullets only; prose written by human

### During Integration

- [ ] Run 1 chapter through full Coordinator cycle (Plan → Execute → Critic → Persist)
- [ ] Verify state.json is valid JSON after each step
- [ ] Check git status for unexpected file changes
- [ ] Ensure Critic catches invalid outputs (test by intentionally breaking an agent)
- [ ] Confirm toggles work (enable feature, run session, verify behavior; disable, re-run, verify reverted)

### After Integration

- [ ] Disable all new features (revert to baseline System B)
- [ ] Run full session cycle (should work identically to pre-integration)
- [ ] Re-enable one feature at a time
- [ ] Document which chapters tested with which features

---

## 6. Integration Roadmap (Safe Sequencing)

### Phase 0: Setup (No Code Changes)

- [ ] Clone external repos to `.claude/imports/`
- [ ] Review this document (architecture + safety)
- [ ] Create feature toggle structure in ThesisState

### Phase 1: Add Infrastructure (Safe Foundation)

1. **Extend ThesisState** (1 hour)
   - Add `toggles: Dict[str, bool]`
   - Add `material_gaps: List[str]`
   - Add new ComplianceState fields

2. **Test state round-trip** (30 min)
   - Save modified state to JSON
   - Load it back
   - Verify backward compatibility

### Phase 2: Add Feature Agents (One at a Time)

1. **Anti-Leakage Protocol** (3–4 hours)
   - Add method to WritingAgent
   - Add validator to CriticAgent
   - Test on Ch. 4 (data-dependent chapter)
   - Run Coordinator cycle with toggle ON and OFF

2. **Semantic Scholar API** (5–6 hours)
   - Add method to ComplianceAgent
   - Test on Ch. 2 (37 citations)
   - Verify API calls and error handling
   - Run Coordinator cycle

3. **Writing Quality Check** (2–3 hours)
   - Add validators to CriticAgent
   - Test on existing Ch. 1 prose
   - Verify no false positives

4. **Remaining features** (if time)

### Phase 3: Integration Testing (No Code Changes to System A)

- [ ] Full thesis cycle with all toggles ON
- [ ] Full thesis cycle with all toggles OFF (should match baseline)
- [ ] Verify System A is completely untouched

---

## 7. Rollback Procedure (If Something Breaks)

**If a feature causes issues**:

1. **Immediate**: Disable the toggle
   ```python
   state.toggles["feature_name"] = False
   ```

2. **Investigate**: Check state.json and recent logs

3. **Fix or revert**:
   - If fixable in <1 hour: debug and re-test
   - If >1 hour: `git diff` the agent code and revert

4. **Test baseline**: Run full session with all toggles OFF
   - Must match pre-integration behavior exactly

**Why rollback is safe**:
- Features are additive (only new methods in agents)
- Toggles are off by default (no forced behavior)
- State is persisted to JSON (can be inspected + reverted manually)

---

## 8. Summary: Why This Won't Break

| Element | Why Safe |
|---------|----------|
| **System A is frozen** | No imports of System A core logic; only read data structures |
| **State is Pydantic** | New fields are backward-compatible; old JSON still loads |
| **Coordinator routes via dict** | New agents added with one more elif; no touching existing logic |
| **Critic validates all outputs** | Unknown agent/action combos fall back to generic validator |
| **Features are toggles** | All default OFF; opt-in only; can be disabled instantly |
| **Error handling** | All new code catches exceptions; no crashes to Coordinator |
| **WritingAgent still bullets-only** | No changes to core output format; prose by human still |

**Conclusion**: Your architecture is specifically designed for safe extensibility. Following these patterns, you can add features without risk.

---

**Next step**: Confirm you're comfortable with this approach, then we'll start Phase 1 (state extension).
