# Agent Runtime Architecture

The project is intentionally organized around three portfolio-level milestones.

## Milestone 1 — Minimal Runnable Core

The smallest executable runtime loop:

Task -> Runtime -> Planner -> Result -> Finish

Core objects:

- Task: immutable user goal.
- Planner: injected deterministic callable.
- AgentRuntime: owns lifecycle transitions.
- AgentState: records result, status, history, and error.

The purpose is to prove the runtime contract, not to demonstrate advanced agent behavior.

## Milestone 2 — State Machine + Checkpoint

The runtime becomes capable of multi-step execution:

Task -> Action -> Execute -> State Update -> Checkpoint -> Action -> Finish

This milestone owns Action, state variables, execution history, checkpoints, and replay/recovery foundations.

## Milestone 3 — Real Tool + Simple Planner

The runtime connects planning to an actual side-effect-free tool:

Task -> Rule Planner -> Tool Router -> Tool -> Observation -> State

The planner remains deterministic. Tool interfaces are kept stable so an LLM planner can replace the rule planner later without redesigning the runtime.

## Design principle

Do not add framework dependencies merely to make the demo look sophisticated. The portfolio value comes from explicit runtime contracts, deterministic tests, state transitions, tool execution, and clear extension points.
