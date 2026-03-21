---
title: "LangGraph: Building Stateful, Multi-Actor Applications with LLMs"
authors: LangChain AI (Harrison Chase et al.)
year: 2024
venue: Software framework / GitHub repository (langchain-ai/langgraph). No formal academic paper — cite as software.
url: https://github.com/langchain-ai/langgraph
tier: 2 — Recommended (Scraping Run 2)
score: 8
angles: SRQ2, Multi-Agent Orchestration, Framework Design
srqs: [SRQ2]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
LangGraph is an open-source library (MIT licence) built on LangChain that provides a graph-based abstraction for building stateful, multi-actor LLM applications — enabling cycles, shared state, human-in-the-loop interrupts, and persistent memory across sessions, which are absent from standard LangChain pipelines.

## Method
Software framework released in January 2024. Implements a directed graph (StateGraph) where nodes are agents or tools and edges encode conditional routing logic. State is persisted via a checkpointer (in-memory or SQLite), enabling durable execution and rollback. Demonstrated through multi-agent workflows including ReAct agents, supervisor patterns, and hierarchical agent networks.

## Key finding
LangGraph's graph-based state machine model resolves a key limitation of chain-based orchestration (no cycles, no shared mutable state), enabling the coordination patterns required for complex multi-agent workflows — including the supervisor-subagent architecture used in this thesis.

## Relevance to thesis
- SRQ2: the thesis's multi-agent Coordinator + sub-agent architecture is implemented in LangGraph — this is the primary implementation reference for Ch.5 (Framework Design) and Ch.7 (Implementation)
- The StateGraph abstraction directly maps to the thesis's phase-transition and approval workflow
- Human-in-the-loop interrupt capability supports the mandatory human approval gates defined in CLAUDE.md

## Gap / limitation
LangGraph is a software framework, not a peer-reviewed contribution — its architectural claims are not independently validated. Academic citation should note this and complement with peer-reviewed multi-agent coordination literature.
