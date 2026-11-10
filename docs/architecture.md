# Agent Runtime Architecture

The project is organized around three portfolio-level milestones.

## M1 — Minimal Runnable Core

Task -> Runtime -> Planner -> Result -> Finish

The runtime owns task lifecycle, state, history, success/failure, and planner injection.

## M2 — State Machine + Checkpoint

Task -> Plan -> Action -> Execute -> State Update -> Checkpoint -> Finish

Core objects:

- Action: one executable step with input, status, output, and error.
- AgentState: shared variables, actions, history, result, and checkpoints.
- ActionExecutor: injected execution boundary.
- StateCheckpoint: immutable snapshot after each action.

M2 guarantees sequential execution, state propagation between actions, checkpoint creation at each action boundary, and deterministic failure handling.

## M3 — Real Tool + Simple Planner

Task -> Rule Planner -> Tool Registry -> Tool -> Observation -> State

Core objects:

- Tool: named executable capability with a stable input/output boundary.
- ToolRegistry: deterministic registration, lookup, and execution.
- RulePlanner: deterministic planner that converts a task into an Action targeting a tool.
- ActionExecutor: bridges the runtime Action to ToolRegistry execution.

M3 proves the complete planning-to-execution path without coupling the runtime to an LLM SDK or agent framework.

An LLM planner can later replace RulePlanner because the runtime consumes the same Action contract.

## Intentional boundaries

The project deliberately stops at these three milestones. Memory, external services, replay orchestration, and model-specific planning are not part of the core runtime.

The portfolio value comes from explicit runtime contracts, state transitions, checkpointing, deterministic tool execution, and clear extension points.
