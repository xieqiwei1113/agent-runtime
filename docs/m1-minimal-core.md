# Milestone 1 — Minimal Runnable Core

## Goal

Build the smallest executable Agent Runtime that proves the core lifecycle is correct.

```text
Task
  ↓
AgentState
  ↓
Planner
  ↓
Result
  ↓
Completed / Failed
```

## Scope

### Included

- Immutable `Task`
- Explicit `AgentState`
- Injected planner interface
- Deterministic execution
- Success and failure lifecycle
- Execution history
- Unit tests
- Runnable example

### Explicitly excluded

- Multi-step Actions
- Checkpoints / replay
- Real tools
- LLM SDKs
- Memory
- Vector databases
- LangGraph / other orchestration frameworks

These belong to later milestones.

## Acceptance criteria

```bash
pip install -e ".[dev]"
pytest
ruff check .
python examples/basic_agent.py
```

The milestone is complete when all commands pass and the example demonstrates:

```text
Task -> Planner -> Result -> Completed
```
