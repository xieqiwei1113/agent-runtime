# Agent Runtime

A minimal, framework-agnostic runtime for long-running AI agents.

## M0 scope

- Explicit task/state lifecycle
- Model-independent planner interface
- Deterministic unit-testable runtime core
- No LangGraph, MCP, vector database, or persistent memory yet

Lifecycle: Task -> Runtime -> Planner -> Result -> State Update -> Finish/Re-plan

## Roadmap

M0 Runtime Core -> M1 State -> M2 Planner -> M3 Tool Registry/Router -> M4 Memory -> M5 Evaluation -> M6 Failure Recovery -> M7 Long-running Tasks -> M8 Observability -> M9 Benchmark

## Development

pip install -e ".[dev]"
pytest
ruff check .
