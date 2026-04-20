---
name: audit-ml-repo
description: |
  Evidence-driven ML repository verification skill. Treats every Claude Code claim as a hypothesis to test, not a statement to trust. Runs staged audits (quick / standard / forensic) across code executability, data reality, training authenticity, and metric validity. Produces claim verdicts, findings JSON, evidence manifest, and a human-readable audit report. Use before merging ML code, before model releases, or whenever AI-generated code claims need independent verification.
  Triggers on: "audit ml repo", "verify claims", "audit this repo", "check training is real", "verify metrics", "run quick audit", "run standard audit", "forensic audit", "hallucination check", "evidence-driven audit", "verify model training".
compatibility: Python 3.10+, any ML project (scikit-learn, PyTorch, pandas, etc.)
---

# Audit ML Repo Skill

## Overview

This skill implements the **evidence-driven verification framework** from the Deep Research report. It answers six questions for any ML repository:

1. **Does it run?** — clean-environment executability
2. **Does it do what it claims?** — claim-by-claim verdict
3. **Is the data real?** — access receipts, schema, split manifests
4. **Is training legitimate?** — run manifests, weight-delta proof, optimizer verification
5. **Are the metrics trustworthy?** — independent recomputation from frozen predictions
6. **Can a human independently verify this?** — complete evidence bundle

**Core principle:** Do not accept plausibility as proof. A claim is accepted only when linked to a reproducible command, captured environment, input/output digests, and independently checkable provenance.

---

## When to Use

| Trigger | Audit Level | Use Case |
|---------|-------------|----------|
| `"quick audit"` | quick | PR review, catch obvious hallucinations |
| `"audit this repo"` | standard | Pre-merge, model release, internal handoff |
| `"forensic audit"` | forensic | High-stakes deployment, contradictory evidence found |
| `"hallucination check"` | quick | Claude-generated code review |
| `"verify training is real"` | standard | Training loop authenticity only |
| `"verify metrics"` | standard | Metric recomputation focus |

---

## Audit Levels

| Level | Scope | Time Estimate | Gate Use |
|-------|-------|---------------|----------|
| **quick** | Static checks, env resolution, smoke execution, claim sampling, dependency review | 15–30 min | Pull requests, frequent local use |
| **standard** | Clean install, primary workflow execution, data access verification, metric recomputation, receipts bundle | 2–6 hours | Merge to main, model release, handoff |
| **forensic** | Cold-machine rebuild, attestation verification, historical artifact comparison, deep data lineage, repeated challenge runs | 1–3 days | Pre-production high-risk, incident response |

---

## How It Works

### Step 1: Intake — What are we auditing?

The skill asks:
- **repo_root** — path to the repository
- **audit_level** — `quick`, `standard`, or `forensic` (default: `quick`)
- **primary_workflows** — which workflows to test: `train`, `eval`, `infer`, `etl`, `all`
- **claims_file** *(optional)* — path to a `claims.yaml` if one exists; otherwise the skill extracts claims from README, notebooks, comments, and commit messages

### Step 2: Claim Extraction and Normalization

Every material statement is converted into a testable record:

```yaml
- claim_id: C001
  claim_text: "train.py trains a binary classifier and saves model.pkl"
  source: "README.md:14"
  claim_type: training         # code | data | training | metrics | output | reproducibility
  expected_evidence:
    - training/run_manifest.json
    - training/checkpoints/model.pkl
  verdict: PENDING             # VERIFIED | REFUTED | INCONCLUSIVE | NOT_TESTED | NOT_APPLICABLE
```

Claim sources searched (in order):
1. `claims.yaml` if provided
2. `README.md` — bold assertions, feature lists
3. Notebooks — markdown cells, comments
4. Training/eval scripts — docstrings, comments claiming behavior
5. `pyproject.toml` / `setup.py` — declared entry points
6. Git commit messages (last 10)

### Step 3: Eight Audit Stages

| Stage | What it checks | Key artifacts |
|-------|---------------|---------------|
| **Repository snapshot** | Commit, dirty tree, file inventory, dependency graph | `repo_manifest.json`, `git_status.txt`, `sbom.json` |
| **Environment reconstruction** | Clean install, pip check, interpreter version | `pip_install_report.json`, `pip_inspect.json`, `requirements.txt` |
| **Executable proof** | Smoke tests, unit/integration tests, notebook execution | `junit.xml`, `coverage.xml`, `commands.jsonl` |
| **Data reality** | Source existence, schema, counts, samples, split manifest | `dataset_manifest.yaml`, `schema_snapshot.json`, `split_manifest.parquet` |
| **Training authenticity** | Run manifest, optimizer/loss, checkpoint lineage, weight-delta | `run_manifest.json`, `checkpoint_hashes.txt`, `weight_delta.json` |
| **Metrics verification** | Recompute from frozen predictions, delta to claimed value | `predictions.parquet`, `metrics_report.json`, `recompute_metrics.log` |
| **Output provenance** | SHA-256 hashes, attestation linking outputs to run | `output_hashes.txt`, `evidence_manifest.json` |
| **Human review verdict** | Score, findings, gaps, gate result | `audit_report.md`, `findings.json`, `claim_verdicts.json` |

### Step 4: Evidence Bundle

The skill produces `audit_artifacts/` with this structure:

```
audit_artifacts/
  claim_inventory.yaml
  claim_verdicts.json
  findings.json
  evidence_manifest.json

  repo_snapshot/
    repo_manifest.json
    git_status.txt
    file_inventory.csv
    sbom.json

  environment/
    python_version.txt
    os_release.txt
    pyproject.toml
    requirements.txt
    pip_install_report.json
    pip_inspect.json
    pip_check.txt

  execution/
    commands.jsonl
    smoke.stdout.txt
    test.stdout.txt
    junit.xml
    coverage.xml
    executed_notebooks/

  data/
    dataset_manifest.yaml
    schema_snapshot.json
    profile_summary.json
    split_manifest.parquet
    sample_rows.redacted.parquet
    data_hashes.txt
    dataset_card.md

  training/
    run_manifest.json
    train.log
    checkpoint_hashes.txt
    weight_delta.json
    cv_results.parquet
    tuner_summary.json

  metrics/
    predictions.parquet
    metrics_report.json
    recompute_metrics.log
    scorer_spec.json

  outputs/
    output_manifest.json
    output_hashes.txt

  docs/
    model_card.md
    audit_report.md
```

### Step 5: Scoring and Verdict

| Category | Weight |
|----------|-------:|
| Repository integrity | 10 |
| Environment reproducibility | 15 |
| Dependency validity | 10 |
| Code correctness and executable proof | 15 |
| Data accessibility and provenance | 15 |
| Training validity | 10 |
| Metrics validity | 10 |
| File and output provenance | 5 |
| Security and secret handling | 5 |
| Human auditability | 5 |
| **Total** | **100** |

**Maturity bands:**
- **0–24**: Narrative-only — claims mostly unsupported
- **25–49**: Runnable-by-author — some execution proof, poor receipts
- **50–69**: Partially auditable — key gaps in data, training, or metrics
- **70–84**: Reproducible with receipts — strong standard-audit posture
- **85–100**: Forensic-ready — strong provenance, strong receipts, low ambiguity

**Gate decisions:**
- **PASS**: score ≥ 80, zero critical findings
- **CONDITIONAL PASS**: score 70–79, zero critical findings, remediation plan required
- **ESCALATE**: contradictory evidence, inaccessible private data, budget-limited rerun, unresolved provenance gaps
- **FAIL**: score < 70 or any critical finding

---

## Hallucination Detection Rubric

Run this checklist whenever Claude Code created or heavily modified the project:

1. **Nonexistent packages or methods** — verify every third-party import against the package index and every symbol against installed distributions
2. **Fake file paths and phantom outputs** — confirm every claimed path exists in the audited run, not just in comments
3. **Dead training loops** — confirm actual optimizer steps, state changes, checkpoint writes, realistic step counts
4. **Pseudo-implementations** — flag `pass`, `TODO`, `NotImplementedError`, mock return values in claim-critical paths
5. **Comments that over-claim** — match comments/docstrings against observable execution; comments are claims, not evidence
6. **Broken evaluation semantics** — recompute metrics; do not trust logged values without underlying predictions
7. **Silent leakage** — check split order, preprocessing order, entity duplication, timestamp leakage
8. **Notebook state illusions** — reject stale notebook outputs unless freshly executed in audited run
9. **Inconsistent experiment records** — hyperparameters, seeds, checkpoint metadata, logs must agree
10. **Stale artifacts** — compare artifact timestamps and digests with audited run and commit
11. **Security-smell dependencies** — run dependency review for new packages or obvious supply-chain risk
12. **Missing human receipts** — if result depends on undocumented env vars or manual notebook steps, it is not auditable

---

## Evidence Quality Reference

| Good evidence | Bad evidence |
|---------------|-------------|
| `commands.jsonl` with exact command, exit code, stdout/stderr paths, output hashes | "I ran it locally and it worked" |
| `predictions.parquet` + `metrics_report.json` + `recompute_metrics.log` | Screenshot of terminal showing "accuracy: 0.93" |
| Checkpoint hash tied to `run_manifest.json` created during audit window | Old `.pt` or `.pkl` file with no provenance |
| Dataset manifest with source listing, schema, counts, timestamps | Path in a config file the auditor never accessed |
| Executed notebook saved during audited run, paired to source text | Notebook with stale outputs checked into repo |
| SBOM tied to commit and workflow | README text claiming artifact came from "latest code" |

---

## Usage Examples

### Example 1: Quick Pre-Commit Hallucination Check

**Trigger:** `"Quick audit — I've been using Claude heavily and want to catch any hallucinated packages"`

**Skill behavior:**
1. Asks: scope (repo_root), level confirms as `quick`, workflows to smoke-test
2. Extracts claims from README + notebooks
3. Verifies all imports against installed packages
4. Runs smoke test for each entry point
5. Checks for `pass`/`TODO`/`NotImplementedError` in critical paths

**Output:**
```
QUICK AUDIT REPORT
══════════════════════════════════════════

Claims extracted: 8
Hallucination checks: 12

FINDINGS:
  C003 [REFUTED] — "model.fit() uses early stopping via EarlyStopping callback"
    → EarlyStopping not imported anywhere in training script
    → Callback argument accepted but never passed to fit()
    → Evidence: grep shows 0 references to EarlyStopping in audited run

  DEP-02 [WARNING] — Package 'sklearn_extra' imported in utils.py
    → Not present in requirements.txt
    → Not installed in audited environment
    → pip check: FAIL

Score: 41/100 — Runnable-by-author
Gate: FAIL (1 critical finding: unrecomputable metrics claim)
```

### Example 2: Standard Audit Before Model Release

**Trigger:** `"Standard audit before I hand off the forecasting model"`

**Skill behavior:**
1. Confirms: repo_root, commit SHA, primary workflows = `train,eval`
2. Checks for `claims.yaml` — not found, extracts from README + scripts
3. Runs all 8 audit stages
4. Produces full evidence bundle

**Output:**
```
STANDARD AUDIT REPORT — forecasting_model @ a3f2b19
══════════════════════════════════════════════════

Claims audited: 12
Critical findings: 0
Major findings: 2

CLAIM VERDICTS:
  C001 [VERIFIED]   train.py trains Ridge regression and saves model.pkl
  C002 [VERIFIED]   MAPE reported as 4.2% on holdout set
  C004 [INCONCLUSIVE] Model generalizes across Nielsen product groups
    → No holdout by product_group found in split_manifest
    → Recommend: stratified split or explicit group-level evaluation

Score: 78/100 — Reproducible with receipts
Gate: CONDITIONAL PASS
  Remediation required: add group-level split verification for C004

Evidence bundle: audit_artifacts/
  evidence_manifest.json — open this first
```

### Example 3: Training Authenticity Focus

**Trigger:** `"Verify that training is real — the loss curves look too clean"`

**Skill behavior:**
1. Focuses on Training authenticity stage
2. Checks: run manifest exists, optimizer steps logged, checkpoint timestamps match training log, weight-delta proof
3. Checks seed capture, hyperparameter consistency

**Output:**
```
TRAINING AUTHENTICITY AUDIT
══════════════════════════════════════════

Run manifest: FOUND (training/run_manifest.json)
Optimizer steps logged: 847 steps across 50 epochs ✓
Checkpoint timestamps: match training log window ✓
Weight delta proof:
  pre-train param hash:  sha256:a1b2c3...
  post-step-1 hash:      sha256:d4e5f6...  ← CHANGED ✓
  Change belongs to run: R001 ✓

Seed capture: MISSING
  → random.seed() not called in train.py
  → numpy.random.seed() not found
  → torch.manual_seed() not found
  → Finding: MAJOR — results may not reproduce

Hyperparameter consistency:
  config.yaml alpha=0.01 ↔ run_manifest.json alpha=0.01 ✓
  config.yaml n_epochs=50 ↔ train.log "Epoch 50/50" ✓

Verdict: Training is authentic. Seed capture gap is a reproducibility risk, not an authenticity refutation.
```

---

## Required Test Types

The skill enforces different test types because each proves something different:

| Test type | What it proves | Artifacts emitted |
|-----------|----------------|-------------------|
| Unit tests | Local invariants, parsing, helper correctness | JUnit XML, coverage |
| Integration tests | Interface contracts between modules, configs, storage | JUnit XML, service logs |
| End-to-end tests | Supported workflow executes from input to output | Command transcript, output manifest, hashes |
| Smoke tests | Imports, entrypoints, config loading, basic data connectivity | Command transcript, exit code |
| Data validation tests | Schema, domains, anomalies, skew, drift, split hygiene | Profile, schema snapshot, anomaly report |
| Training sanity checks | Real weight updates, loss/metric movement | Run manifest, step logs, weight-delta proof |
| Reproducibility tests | Reruns match within declared tolerance | Rerun receipt, delta report |

---

## Audit Report Template

When the skill runs, it fills and emits this report:

```markdown
# Audit Report

## Scope
- Repository:
- Commit:
- Audit level:
- Date:
- Primary workflows audited:

## Verdict
- Overall result: PASS / CONDITIONAL PASS / ESCALATE / FAIL
- Score: /100
- Critical findings:
- Major findings:

## Claim Verdicts
| claim_id | claim_text | status | evidence_refs | notes |

## Environment
- Python version:
- OS / architecture:
- Install result:
- Dependency compatibility:

## Code Execution
- Smoke commands run:
- Test commands run:
- Coverage summary:
- Broken entrypoints or imports:

## Data Verification
- Sources verified:
- Access receipts:
- Split verification result:
- Leakage findings:

## Training Verification
- Run manifest:
- Hyperparameters:
- Seed capture:
- Checkpoint lineage:
- Weight/state change proof:

## Metrics and Outputs
- Predictions artifact:
- Independent metric recomputation:
- Output hashes:

## Security and Auditability
- Secret-handling findings:
- Human-auditability gaps:

## Residual Risk
- What was proven:
- What remains uncertain:
- Escalation recommendations:

## Evidence Index
- Path to evidence manifest:
- Path to receipts bundle:
```

---

## Pre-Hoc Instructions for Claude Code

When asking Claude to write ML code that will be audited, prepend this to your prompt:

```
You are writing code for a repository that will be audited by an evidence-driven ML verification skill.

Mandatory requirements:
1. Do not make claims you cannot verify.
2. For each material claim, add an entry to claims.yaml.
3. Prefer executable Python scripts and package entrypoints over notebook-only workflows.
4. If you create a notebook, pair it to a text representation and ensure it can be executed programmatically.
5. Create pyproject.toml and document canonical commands for setup, test, train, eval, and infer.
6. Emit machine-verifiable artifacts: junit.xml, coverage.xml, run_manifest.json, predictions.parquet, metrics_report.json, output_manifest.json, sha256 hashes for material outputs.
7. For every data source, create dataset_manifest.yaml with source locator, access method, schema summary, row counts, split policy, provenance/licensing notes.
8. For every training run, record: effective config, hyperparameters, random seeds, dataset version, optimizer and loss, checkpoints, metrics, output hashes.
9. If a step was not executed, say so explicitly and mark the claim as unverified.
10. Never store live secrets in the repository.

Your output must be runnable by a competent engineer without further AI assistance.
```

---

## Minimal Standard vs Gold Standard

**Minimal standard (required for PASS):**
- `pyproject.toml` or equivalent package metadata
- Reproducible environment instructions
- Requirements/constraints + dependency snapshot
- Smoke tests, unit tests, JUnit XML
- Data manifest with access proof, schema, counts, split manifest
- One audited training or evaluation run manifest
- Saved predictions + metric recomputation script
- Output hashes
- No notebook-only critical paths
- No hardcoded secrets

**Gold standard (85+ score):**
- All minimal-standard items
- Container image digest or equivalent immutable environment reference
- SBOMs for software and meaningful artifact sets
- Signed provenance or linked-artifact records
- Model card + dataset card
- Challenge reruns + full representative rerun
- Fold indices and estimator/trial evidence for tuning
- Full CI integration with quick/standard gates
- Forensic-ready receipts bundle exportable for compliance review

---

## Related Workflows

- **Before running:** Use `test-codebase-integrity` to confirm basic imports and tests pass
- **After audit FAIL:** Use `/log-errors` to record findings as tooling issues
- **After audit PASS:** Use `/draft-commit` to document the audit as part of the commit
- **For new ML modules:** Reference the Pre-Hoc Instructions above before writing code
- **For thesis model results:** Use this skill before reporting metrics in any thesis section
