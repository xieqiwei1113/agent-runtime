# Agent Runtime

A minimal, framework-agnostic runtime for long-running AI agents.

## Three milestones

### Milestone 1 — Minimal Runnable Core

Task -> Planner -> Result -> Finish

**Completed.** The runtime provides an explicit task/state lifecycle, an injected planner, execution history, deterministic tests, and a runnable example.

### Milestone 2 — State Machine + Checkpoint

Task -> Action -> Execute -> State Update -> Checkpoint -> Action -> Finish

**Completed.** The runtime now supports multi-step Actions, shared state variables, per-step execution history, immutable checkpoints, and deterministic failure handling.

### Milestone 3 — Real Tool + Simple Planner

Task -> Rule Planner -> Tool Router -> Tool -> Observation -> State

**Next.** Adds a Tool interface/registry, one real executable tool, a deterministic rule-based planner, and end-to-end tool execution.

## Architecture boundary

```text
M1: Task -> Runtime -> Planner -> Result -> Finish

M2: Task -> Plan -> Action -> Execute -> State Update -> Checkpoint -> Finish

M3: Task -> Rule Planner -> Tool Router -> Tool -> Observation -> State
```

The runtime remains independent from LangGraph and model SDKs. An LLM planner can be added later behind the planner interface.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
python examples/basic_agent.py
python examples/m2_state_machine.py
```
