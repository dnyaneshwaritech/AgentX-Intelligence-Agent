
# AgentX — Research & Competitor Intelligence Agent

## Team Members

* Gayatri Dayanand Bhagwat
* Gadekar Varsha Vilas
* Gawali Shravani Ganesh
* Patil Dnyaneshwari Pravin

## Problem Statement

Organizations need to continuously monitor research, competitors and industry news. Manual monitoring is time-consuming and can miss important information.

AgentX provides an autonomous AI agent for collecting, analyzing and generating actionable intelligence.

## Project Description

AgentX is an AI-powered Research & Competitor Intelligence Agent using a **LangGraph-based agentic framework**.

It can:

* Understand user goals
* Dynamically plan tasks
* Select appropriate tools
* Coordinate multiple agents
* Analyze and verify evidence
* Detect conflicts and failures
* Replan when required
* Generate actionable intelligence

## Agent Workflow

```text
Understand → Plan → Select Tool → Act
→ Observe → Analyze → Verify
→ Self-Evaluate → Replan → Finalize
```

## Task 5 — Agent Framework

AgentX implements the required agentic capabilities using **LangGraph**:

* Dynamic planning
* Multi-agent orchestration
* Conditional routing
* Parallel execution
* Shared state
* Checkpointing
* Failure recovery
* Tool fallback
* Conflicting-evidence handling
* Uncertainty-aware decisions
* Resource-aware execution
* Self-evaluation
* Hypothesis verification
* Memory-based reasoning
* Loop/deadlock detection
* Autonomous replanning
* Adaptive task decomposition

### Multi-Agent Architecture

```text
User Task
   ↓
Dynamic Planner
   ↓
┌────────────┬────────────┐
Research    News      Competitor
 Agent      Agent        Agent
   └────────────┬─────────┘
                ↓
        Verification Agent
                ↓
          Self-Evaluation
                ↓
        Autonomous Replanner
                ↓
             Finalizer
```

## External Tools

* 🔬 Research API — scientific research
* 📚 Crossref — DOI verification
* 🌐 OpenAlex — research metadata
* 📰 News Search — industry developments
* 🏢 Competitor Intelligence — competitor analysis

## Adversarial Test

Run:

```bash
python react_agent.py
```

Select:

```text
2. Adversarial Task 5 test
```

The test intentionally demonstrates:

```text
Tool Failure
↓
Parallel Agent Execution
↓
Conflicting Evidence
↓
Verification
↓
Autonomous Replanning
↓
Self-Evaluation
↓
Final Result
```

The adversarial test successfully demonstrates failure recovery, tool fallback, conflict handling, verification, replanning and loop/deadlock detection.

## Memory

AgentX maintains short-term conversation memory using:

```text
agentx_memory.json
```

Recent interactions are used as context for follow-up tasks.

## Technologies Used

* Python
* LangGraph
* OpenRouter
* Streamlit
* ReAct Agent Architecture
* Tool Calling
* Research APIs
* Crossref
* OpenAlex
* News APIs
* Git & GitHub
* python-dotenv

## Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

Run the agent:

```bash
python react_agent.py
```

## Result

AgentX produces an intelligence report containing:

* Executive Summary
* Key Findings
* Emerging Trends
* Risks
* Opportunities
* Evidence & Confidence
* Unresolved Uncertainty
* Actionable Recommendations
* Sources
# Task 7: Advanced Tracing & Observability Report

## 1. Objective

The objective of Task 7 was to implement end-to-end tracing and observability for the AgentX multi-agent system.

The system was required to trace:

- Agent execution
- Prompts and decisions
- Tool calls
- Execution latency
- Token usage estimates
- Errors and failures
- Recovery actions

The system was also required to introduce a controlled failure, identify the root cause using trace data, automatically diagnose the failure, and demonstrate measurable improvements.

---

# 2. Observability Architecture

AgentX implements a custom observability layer that records execution events throughout the LangGraph workflow.

The tracing system records:

- Trace ID
- Task information
- Agent start and end events
- Execution decisions
- Graph execution status
- Tool calls
- Latency metrics
- Confidence metrics
- Failure counts
- Evidence conflicts
- Errors
- Estimated token usage

Each execution produces a JSON trace file.

Example trace location:

```text
observability/traces/trace_<trace_id>.json