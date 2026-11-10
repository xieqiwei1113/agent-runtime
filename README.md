# Agent Runtime

A minimal, framework-agnostic runtime for long-running AI agents.

## Three milestones

### Milestone 1 — Minimal Runnable Core

Task -> Planner -> Result -> Finish

**Completed.** Explicit task/state lifecycle, planner injection, execution history, deterministic tests, and a runnable example.

### Milestone 2 — State Machine + Checkpoint

Task -> Action -> Execute -> State Update -> Checkpoint -> Action -> Finish

**Completed.** Multi-step Actions, shared state variables, per-step history, immutable checkpoints, and deterministic failure handling.

### Milestone 3 — Real Tool + Simple Planner

Task -> Rule Planner -> Tool Registry -> Tool -> Observation -> State

**Completed.** The runtime now has a framework-independent Tool interface, deterministic ToolRegistry routing, a RulePlanner, and an end-to-end executable example.

## Architecture boundary

```text
M1: Task -> Runtime -> Planner -> Result -> Finish

M2: Task -> Plan -> Action -> Execute -> State Update -> Checkpoint -> Finish

M3: Task -> Rule Planner -> Tool Registry -> Tool -> Observation -> State
```

The runtime remains independent from LangGraph and model SDKs. An LLM planner can replace RulePlanner later without changing the Tool or Runtime contracts.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
python examples/basic_agent.py
python examples/m2_state_machine.py
python examples/m3_tool_agent.py
```
