
authors: Paranjape, B., Lundberg, S., Singh, S., Hajishirzi, H., Zettlemoyer, L., & Ribeiro, M.T.

year: 2023

venue: arXiv preprint

doi:

apa7: >

  Paranjape, B., Lundberg, S., Singh, S., Hajishirzi, H., Zettlemoyer, L., &

  Ribeiro, M.T. (2023). ART: Automatic multi-step reasoning and tool-use for

  large language models. *arXiv preprint arXiv:2303.09014*.

  https://arxiv.org/abs/2303.09014

read_date: 2026-03-19

read_depth: full

---

  

## In one sentence

  

ART automates multi-step reasoning and tool use in frozen LLMs by retrieving task-decomposition demonstrations from a task library, seamlessly pausing generation to call external tools (search, code execution) and integrating their outputs — achieving 22+ percentage point improvements over automatic CoT on unseen tasks and enabling human correction of reasoning chains via library updates.

  

## Method

  

Task library of 15 BigBench tasks; evaluated on 19 unseen BigBench + 6 MMLU + SQUAD/TriviaQA/SVAMP/MAWPS tasks. Frozen GPT-3. Structured query language for intermediate steps (tool calls parsed, generation paused/resumed). Tool library: search, code generation, code execution. Compared against few-shot prompting, automatic CoT, hand-crafted CoT. Human feedback condition: task/tool library updated with corrected demonstrations.

  

## Key findings — cite these

  

- ART outperforms automatic CoT by **average 22+ percentage points** on 32/34 BigBench and all MMLU unseen tasks

- Tool use (vs. no tools) improves performance by **average 12.3 percentage points** on test tasks

- ART improves over direct few-shot prompting by **10.8 percentage points** on average across unseen tasks

- With human feedback (corrected demonstrations): **exceeds best-known GPT-3 results by 20+ percentage points** on 12 tasks

- Gradient-free — works with frozen LLMs via API; no fine-tuning required

  

## Direct quotes — copy verbatim, include page/section

  

> "ART seamlessly pauses generation whenever external tools are called, and integrates their output before resuming generation." (Abstract)

  

> "ART is also extensible, and makes it easy for humans to improve performance by correcting errors in task-specific programs or incorporating new tools." (Abstract)

  

> "Existing methods for chained reasoning with tool use are difficult to extend to new tasks and tools, requiring fine-tuning or prompt-engineering tailored for a specific task or tool." (Section 1)

  

## Where this goes in my thesis

  

- **Ch.2, Section 2.1**: Core reference for the tool-augmented LLM agent paradigm — ART establishes the pause-execute-resume pattern (generation interrupted by tool call, output integrated, generation resumed) that is the conceptual predecessor to the LangGraph node execution model used in the thesis framework; cite alongside Toolformer as the two foundational papers for tool-use in LLM agents

- **Ch.5 (Framework Design)**: The task library + tool library architecture maps onto the thesis's Coordinator + agent pool design — each LangGraph node is effectively a "tool" in the ART sense; the thesis extends this by replacing static demonstrations with a stateful TypedDict that accumulates outputs across nodes

- **Ch.9 (Discussion)**: The human feedback mechanism (correcting task library demonstrations) is the academic analogue of the thesis's `interrupt_before` human approval gates — both establish that human-in-the-loop correction of automated reasoning chains is a validated design pattern, not a limitation

  

## What this paper does NOT cover (gap it leaves)

  

ART operates on general-purpose reasoning benchmarks (BigBench, MMLU) with no domain-specific data pipelines, no RAM constraints, and no requirement to synthesise probabilistic forecasting outputs into confidence-scored managerial recommendations. The tool library paradigm assumes tools return deterministic, single-call outputs — it does not address the sequential coordination of multiple ML models with shared state, memory budgets, and heterogeneous output formats that the thesis framework requires.

  

## My critical assessment

  

- Key innovation: ART enables frozen LLMs to perform multi-step reasoning with integrated tool calls without fine-tuning, demonstrating that external tool use plus task decomposition can dramatically improve performance.  
      
    
- Human-in-the-loop: The task/tool library can be corrected by humans, providing a validated mechanism for improving reasoning chains — maps directly to the thesis’s interrupt_before gates.  
      
    
- Generality: Works gradient-free via API; no task-specific prompt engineering or model retraining required, showing that robust multi-step reasoning can be layered on top of frozen LLMs.  
      
    
- Design relevance: Establishes the pause-execute-resume pattern and modular task/tool library concept, which informs the thesis’s LangGraph node execution and Coordinator + agent pool architecture.  
      
    

Limitations / gaps relative to thesis

- Tested on general-purpose benchmarks, not domain-specific forecasting or managerial recommendation tasks.  
      
    
- Does not handle RAM-constrained sequential coordination of multiple heterogeneous ML models.  
      
    
- Assumes deterministic, single-call tool outputs; does not synthesize probabilistic outputs into weighted confidence scores.  
      
    
- No consideration of real-time multi-agent orchestration or integration of structured numerical forecasts.  
      
    
- Overall, ART is academically important because it shows how frozen LLMs can be augmented with tools and task libraries for multi-step reasoning, providing a conceptual and design foundation for the thesis framework while leaving domain-specific synthesis and sequential resource management to be implemented.
    

  
**