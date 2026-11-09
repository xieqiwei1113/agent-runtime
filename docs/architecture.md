# M0 Architecture

M0 intentionally keeps the runtime small.

## Core objects

- Task: immutable user goal.
- AgentState: execution state, history, result, and error.
- Planner: injected callable that decides the next result/action.
- AgentRuntime: owns lifecycle transitions.

## Lifecycle

1. Create AgentState.
2. Mark task running and record an event.
3. Invoke the planner.
4. Persist the planner result into state.
5. Mark completed, or capture an exception as failed.

The runtime is independent from any model SDK or orchestration framework. Later milestones add explicit action/tool abstractions, memory, evaluation, recovery, and observability.
