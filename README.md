# Agent Runtime

A minimal, framework-agnostic runtime for long-running AI agents.

## Three milestones

### Milestone 1 — Minimal Runnable Core

Goal: prove the runtime can execute a task end-to-end.

- Task input
- Injected deterministic planner
- Runtime lifecycle
- Result / success / failure
- Unit tests
- Runnable example

**Not included:** real LLM, real tools, memory, checkpoint/replay.

### Milestone 2 — State Machine + Checkpoint

Goal: prove the runtime can manage multi-step execution.

- Action abstraction
- Multi-step execution
- State variables
- Execution history
- Checkpoints
- Failure/replay foundation
- Unit tests and demo

### Milestone 3 — Real Tool + Simple Planner

Goal: connect the runtime to one real executable tool while keeping planning deterministic.

- Tool interface + registry
- One real tool (for example, text/file retrieval)
- Rule-based planner
- Tool result written back to state
- End-to-end demo
- Stable interfaces for a future LLM planner

## Current repository status

The repository has already implemented **Milestone 1 and Milestone 2**. The existing M1 code should be treated as the implementation of Milestone 2, not as extra scope that needs to be deleted.

The next development target is **Milestone 3: Real Tool + Simple Planner**.

## Architecture boundary

```text
Milestone 1
Task -> Runtime -> Planner -> Result -> Finish

Milestone 2
Task -> Plan/Action -> Execute -> State Update -> Checkpoint -> Finish

Milestone 3
Task -> Rule Planner -> Tool Router -> Tool -> Observation -> State -> Finish
```

The runtime remains independent from LangGraph and model SDKs. An LLM planner can be added later behind the planner interface.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```
