
---

title: "Executable Code Actions Elicit Better LLM Agents"

authors: Wang, X., et al.

year: 2024

venue: International Conference on Machine Learning (ICML 2024) / OpenReview

doi:

apa7: >

  Wang, X., et al. (2024). Executable code actions elicit better LLM agents.

  *Proceedings of the 41st International Conference on Machine Learning*.

  https://openreview.net/forum?id=jJ9BoXAfFa

read_date: 2026-03-17

read_depth: full

---

  

## In one sentence

  

Replacing JSON/text action formats with executable Python code as the unified action space for LLM agents (CodeAct) yields up to 20% higher task success rates and 30% fewer required actions, because code natively supports control flow, data flow, self-debugging, and composition of multiple tools in a single action.

  

## Method

  

Benchmarked 17 LLMs on APIBank (atomic tool use) and a newly curated benchmark M3ToolEval (82 human-curated multi-tool, multi-turn tasks). Compared CodeAct against JSON and text action baselines. Additionally fine-tuned LLaMA-2 and Mistral-7B on CodeActInstruct (7k multi-turn interaction trajectories) to produce CodeActAgent.

  

## Key findings — cite these

  

- CodeAct achieves **up to 20% absolute improvement** in task success rate over JSON/text baselines on M3ToolEval

- Requires **up to 30% fewer actions** than text/JSON baselines to solve the same tasks

- Performance gains widen as underlying LLM capability increases — CodeAct scales with model quality

- CodeActAgent (fine-tuned Mistral-7B) generalises to out-of-domain agent tasks without degrading general capabilities (QA, coding, instruction following)

- 7k CodeActInstruct trajectories are sufficient for meaningful agent-oriented fine-tuning

  

## Direct quotes — copy verbatim, include page/section

  

> "CodeAct outperforms widely used alternatives (up to 20% higher success rate)." (Abstract)

  

> "Code actions allow LLM to leverage existing software packages... instead of hand-crafted task-specific tools." (Section 1)

  

> "Code inherently supports control and data flow, allowing for the storage of intermediate results as variables for reuse and the composition of multiple tools to perform complex logical operations." (Section 1)

  

> "Error messages from the environment further enable it to rectify errors autonomously through self-debugging in multi-turn interaction." (Section 4)

  

## Where this goes in my thesis

  

- **Ch.2, Section 2.1**: Primary reference for the CodeAct paradigm — establishes that executable code is the superior action format for LLM agents; grounds the Coordinator's use of Python-based tool dispatch over JSON function calling

- **Ch.5 (Framework Design)**: Justifies why the thesis framework uses Python agent code (LangGraph nodes) rather than declarative JSON configs to orchestrate forecasting sub-agents

- **Ch.9 (Limitations)**: CodeAct requires a live Python interpreter — relevant to the resource-constrained deployment constraint (RAM overhead of maintaining a persistent interpreter process)

  

## What this paper does NOT cover (gap it leaves)

  

CodeAct is evaluated exclusively on general reasoning and software tasks with no computational budget constraints; it does not address multi-agent orchestration under a fixed RAM ceiling, nor the synthesis of heterogeneous ML model outputs into probabilistic business recommendations. The gap between code-action LLM agents and domain-specific decision-support pipelines operating on real retail time-series data is entirely unaddressed.

  

## My critical assessment

JSON-based tool calling constrains the agent to sequential, stateless interactions, which are ill-suited for complex ML pipelines. In contrast, code-based action spaces allow the agent to express full computational workflows, enabling efficient multi-model orchestration and decision-making.

however limitations:  
however they introduce substantial system-level challenges:

- execution overhead
    
- memory persistence
    
- security risks: if use controlled API calls, they can expose the system to risks in terms of Data Leakage, infinite loops, resource usage (potentially infinite), they can delete/ modify data inside the files within the dataset (JSON not cus they have access only to the specified tools) 
    
- reduced controllability.
    
- ⇒ if we use CodeAct there is the need of:  
    Limit access to specific folders
    

- Block modules like os, sys, etc.
    
- Use a sandbox (isolated environment)
    
- Set time and memory limits
    



**